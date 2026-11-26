"""
Normalize Junos BGP neighbors and configured dynamic peer ranges.

Combines 'show bgp neighbor | display json' with optional group configuration
from 'show configuration | display inheritance | display set'.

Used by:
- ttp_templates/platform/juniper_junos_show_bgp_neighbor_pipe_display_json.txt

Produced with Copilot Assistance.
"""

import json
from ipaddress import ip_address, ip_network
from typing import Any, Dict, List, Optional, Union

from ttp_templates.utils.models import BgpNeighborRecord

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

_JUNOS_FAMILY_TO_AFI = {
    ("inet", "unicast"): "ipv4_unicast",
    ("inet6", "unicast"): "ipv6_unicast",
    ("inet", "multicast"): "ipv4_multicast",
    ("inet6", "multicast"): "ipv6_multicast",
    ("inet", "labeled-unicast"): "ipv4_labeled_unicast",
    ("inet6", "labeled-unicast"): "ipv6_labeled_unicast",
    ("inet-vpn", "unicast"): "ipv4_mpls_vpn",
    ("inet6-vpn", "unicast"): "ipv6_mpls_vpn",
    ("evpn", "signaling"): "l2vpn_evpn",
    ("l2vpn", "signaling"): "l2vpn_vpls",
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
    vrf = _get_data(peer, "peer-cfg-rti") or "default"
    if vrf == "master":
        vrf = "default"

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
    hold_time_raw = _get_data(opt_info, "holdtime") or _get_data(
        peer, "active-holdtime"
    )
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

    local_as = _get_data(peer, "local-as")
    remote_as = _get_data(peer, "peer-as")

    return {
        "state": state if state in _BGP_STATES else None,
        "local_address": local_address,
        "local_interface": _get_data(peer, "local-interface-name"),
        "remote_address": remote_address,
        "remote_address_range": None,
        "local_as": int(local_as) if local_as is not None else None,
        "remote_as": int(remote_as) if remote_as is not None else None,
        "peer_group": _get_data(peer, "peer-group"),
        "import_policies": import_policies,
        "export_policies": export_policies,
        "prefix_list_in": None,
        "prefix_list_out": None,
        "name": f"{vrf}_{remote_address}",
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


def transform_bgp_neighbors(payload: Union[dict, list]) -> List[Dict[str, Any]]:
    """Normalize operational neighbors and configured dynamic ranges."""
    items = [payload] if isinstance(payload, dict) else payload or []
    ranges = {}
    group_settings = {}
    # Parse each distinct allow/dynamic peer prefix once and keep its VRF and peer-group associations.
    for item in items:
        for vrf, configs in item.get("bgp_peers_config", {}).items():
            for peer_group, config in configs.items():
                group = (vrf, peer_group)
                for prefix in config.get("remote_address_range", "").strip("[] ").split():
                    if "/" not in prefix:
                        continue
                    if prefix not in ranges:
                        try:
                            ranges[prefix] = (ip_network(prefix, strict=False), {})
                        except ValueError:
                            continue
                    _, groups = ranges[prefix]
                    groups[group] = None
                    group_settings[group] = config

    peers = []
    # Restore the JSON braces stripped by the template and normalize the operational peers.
    for item in items:
        for output in item.get("operational_peers", []):
            operational = json.loads("{" + output["data"] + "}")
            for bgp_info in operational.get("bgp-information") or []:
                peers.extend(
                    _normalize_peer(peer) for peer in bgp_info.get("bgp-peer") or []
                )

    # Attribute each operational peer to the first containing dynamic peers range in its VRF and group.
    for peer in peers:
        if not ranges:
            break
        try:
            address = ip_address(peer["remote_address"])
        except ValueError:
            continue
        group = (peer["vrf"], peer["peer_group"])
        for prefix, (network, groups) in ranges.items():
            if group in groups and address in network:
                peer["remote_address_range"] = prefix
                break

    # Emit configured peer ranges even without active sessions, using the peer group's settings.
    defaults = _normalize_peer({})
    for prefix, (_, groups) in ranges.items():
        for vrf, peer_group in groups:
            settings = group_settings[(vrf, peer_group)]
            record = {
                **defaults,
                "name": f"{vrf}_{prefix}",
                "vrf": vrf,
                "peer_group": peer_group,
                "remote_address": prefix,
                "remote_address_range": prefix,
                "remote_as": int(settings["remote_as"]),
            }
            for field in ("local_as", "hold_time", "max_ttl"):
                value = settings.get(field, "")
                if value.isascii() and value.isdigit():
                    record[field] = int(value)
            for field in ("local_address", "description", "peering_type"):
                if field in settings:
                    record[field] = settings[field].strip('"')
            # Combine repeated policy lines and bracketed lists in configuration order.
            for field in ("import_policies", "export_policies"):
                record[field] = list(dict.fromkeys(
                    policy.strip('"')
                    for line in settings.get("policy_lines", [])
                    for policy in line.get(field, "").strip("[] ").split()
                ))
            afi = _JUNOS_FAMILY_TO_AFI.get((settings.get("afi"), settings.get("safi")))
            if afi:
                record["afi"] = [afi]
            peers.append(record)

    return [BgpNeighborRecord(**peer).model_dump(exclude_unset=True) for peer in peers]
