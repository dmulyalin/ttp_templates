"""
Normalize Juniper JunOS BGP neighbors JSON output to a standardized format.

Transforms raw JSON output from 'show bgp neighbor | display json' into a
normalized list of dictionaries suitable for further processing and integrations.

Produced with Copilot Assistance.
"""
import json
from typing import Any, Dict, List, Optional

# Juniper RIB name suffix -> IANA AFI/SAFI name
_RIB_SUFFIX_TO_AFI = [
    ("inet6.0", "ipv6_unicast"),
    ("inet.0", "ipv4_unicast"),
    ("inet.2", "ipv4_multicast"),
    ("inet6.2", "ipv6_multicast"),
]

# Juniper global RIB names (bgp.* tables) -> IANA AFI/SAFI name
_RIB_NAME_TO_AFI = {
    "bgp.l3vpn.0": "ipv4_mpls_vpn",
    "bgp.l3vpn-inet6.0": "ipv6_mpls_vpn",
    "bgp.evpn.0": "l2vpn_evpn",
    "bgp.l2vpn.0": "l2vpn_vpls",
    "bgp.labeled-unicast.0": "ipv4_labeled_unicast",
    "bgp.labeled-unicast6.0": "ipv6_labeled_unicast",
    "bgp.flow.0": "ipv4_flow_spec",
    "bgp.flow6.0": "ipv6_flow_spec",
    "lsdist.0": "link_state",
}

_BGP_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}
_LINK_TYPES = {"external", "internal"}


def _get_data(obj: Dict[str, Any], field: str, default: Any = None) -> Any:
    """Extract the first .data value from a Juniper JSON array field."""
    items = obj.get(field)
    if items and isinstance(items, list) and isinstance(items[0], dict):
        return items[0].get("data", default)
    return default


def _rib_name_to_afi(rib_name: str) -> Optional[str]:
    """Map a Juniper RIB table name to an IANA AFI/SAFI string."""
    if not rib_name:
        return None
    if rib_name in _RIB_NAME_TO_AFI:
        return _RIB_NAME_TO_AFI[rib_name]
    for suffix, afi in _RIB_SUFFIX_TO_AFI:
        if rib_name.endswith(suffix):
            return afi
    return None


def _strip_port(address: Optional[str]) -> Optional[str]:
    """Remove the '+port' suffix from a Juniper peer/local address field."""
    if not address:
        return None
    return address.split("+")[0]


def _normalize_peer(peer: Dict[str, Any]) -> Dict[str, Any]:
    # VRF: peer-cfg-rti "master" -> "default"
    vrf_raw = _get_data(peer, "peer-cfg-rti") or "master"
    vrf = "default" if vrf_raw == "master" else vrf_raw

    remote_address = _strip_port(_get_data(peer, "peer-address"))
    local_address = _strip_port(_get_data(peer, "local-address"))

    state = (_get_data(peer, "peer-state") or "").lower()
    peer_type = (_get_data(peer, "peer-type") or "").lower()

    # Import/export policies are space-separated strings in Juniper
    opt_info = (peer.get("bgp-option-information") or [{}])[0]
    import_policy_str = _get_data(opt_info, "import-policy") or ""
    export_policy_str = _get_data(opt_info, "export-policy") or ""
    import_policies = import_policy_str.split() if import_policy_str else []
    export_policies = export_policy_str.split() if export_policy_str else []

    # Hold time: prefer bgp-option-information holdtime, fall back to active-holdtime
    hold_time_raw = _get_data(opt_info, "holdtime") or _get_data(peer, "active-holdtime")
    hold_time = int(hold_time_raw) if hold_time_raw is not None else None

    keepalive_raw = _get_data(peer, "keepalive-interval")
    keepalive = int(keepalive_raw) if keepalive_raw is not None else None

    # Uptime: elapsed-time may be present in some JunOS versions (not guaranteed)
    uptime_seconds = None
    elapsed = _get_data(peer, "elapsed-time")
    if elapsed is not None and str(elapsed).isdigit():
        uptime_seconds = int(elapsed)

    # AFI/SAFI and per-AFI prefix counts from bgp-rib list
    afi_list: List[str] = []
    per_afi: Dict[str, int] = {}
    for rib in peer.get("bgp-rib") or []:
        rib_name = _get_data(rib, "name") or ""
        afi = _rib_name_to_afi(rib_name)
        if afi and afi not in afi_list:
            afi_list.append(afi)
        if afi:
            recv = _get_data(rib, "received-prefix-count")
            sent = _get_data(rib, "advertised-prefix-count")
            if recv is not None:
                per_afi[f"{afi}_prefixes_received"] = int(recv)
            if sent is not None:
                per_afi[f"{afi}_prefixes_sent"] = int(sent)

    return {
        "state": state if state in _BGP_STATES else None,
        "local_address": local_address,
        "local_interface": _get_data(peer, "local-interface-name"),
        "remote_address": remote_address,
        "local_as": _get_data(peer, "local-as"),
        "remote_as": _get_data(peer, "peer-as"),
        "peer_group": _get_data(peer, "peer-group"),
        "import_policies": import_policies,
        "export_policies": export_policies,
        "prefix_list_in": None,
        "prefix_list_out": None,
        "name": f"{vrf}_{remote_address}" if remote_address else None,
        "description": _get_data(peer, "description"),
        "router_id": _get_data(peer, "peer-id"),
        "peering_type": peer_type if peer_type in _LINK_TYPES else None,
        "vrf": vrf,
        "hold_time": hold_time,
        "keepalive": keepalive,
        "uptime_seconds": uptime_seconds,
        "max_ttl": None,
        "afi": afi_list,
        **per_afi,
    }


def transform_bgp_neighbors(payload: list) -> List[Dict[str, Any]]:
    """
    Main transformation function to be used as TTP macro.

    Args:
        payload: Parsing results, JSON string of show command output.

    Returns:
        List of normalized BGP neighbor dictionaries.
    """
    if payload:
        payload = json.loads("{" + payload[0]["data"] + "}")
    else:
        return []

    if isinstance(payload, list) and payload:
        payload = payload[0]

    peers = []
    for bgp_info in payload.get("bgp-information") or []:
        for peer in bgp_info.get("bgp-peer") or []:
            peers.append(_normalize_peer(peer))
    return peers
