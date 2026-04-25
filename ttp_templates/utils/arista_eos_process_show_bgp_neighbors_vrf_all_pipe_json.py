"""
Normalize Arista EOS BGP neighbors JSON output to a standardized format.

Transforms raw JSON output from 'show bgp neighbors vrf all | json' into a
normalized list of dictionaries suitable for further processing and integrations.

Produced with Copilot Assistance.
"""
import json
from typing import Any, Dict, List

# Arista camelCase AFI/SAFI names -> IANA snake_case names
_AFI_TO_IANA = {
    "ipv4Unicast": "ipv4_unicast",
    "ipv6Unicast": "ipv6_unicast",
    "ipv4Multicast": "ipv4_multicast",
    "ipv6Multicast": "ipv6_multicast",
    "ipv4LabeledUnicast": "ipv4_labeled_unicast",
    "ipv6LabeledUnicast": "ipv6_labeled_unicast",
    "ipv4MplsVpn": "ipv4_mpls_vpn",
    "ipv6MplsVpn": "ipv6_mpls_vpn",
    "ipv4SrTe": "ipv4_sr_te",
    "ipv6SrTe": "ipv6_sr_te",
    "l2VpnEvpn": "l2vpn_evpn",
    "l2VpnVpls": "l2vpn_vpls",
    "linkState": "link_state",
    "ipv4FlowSpec": "ipv4_flow_spec",
    "ipv6FlowSpec": "ipv6_flow_spec",
}

# IANA AFI name -> (sent_field, received_field) in Arista JSON
_AFI_PREFIX_FIELDS = {
    "ipv4_unicast": ("prefixesSent", "prefixesReceived"),
    "ipv6_unicast": ("v6PrefixesSent", "v6PrefixesReceived"),
    "l2vpn_evpn": ("evpnSent", "evpnReceived"),
    "ipv4_labeled_unicast": (
        "v4LabeledUnicastPrefixesSent",
        "v4LabeledUnicastPrefixesReceived",
    ),
    "ipv6_labeled_unicast": (
        "v6LabeledUnicastPrefixesSent",
        "v6LabeledUnicastPrefixesReceived",
    ),
}

_BGP_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}
_LINK_TYPES = {"external", "internal"}


def _normalize_peer(peer: Dict[str, Any], vrf: str) -> Dict[str, Any]:
    # AFI/SAFI: collect enabled entries from multiprotocolCaps, normalize to IANA names
    afi_list = [
        _AFI_TO_IANA.get(name, name)
        for name, data in peer.get("neighborCapabilities", {})
        .get("multiprotocolCaps", {})
        .items()
        if isinstance(data, dict) and data.get("enabled", False)
    ]

    # Per-AFI prefix counts keyed by IANA AFI name
    per_afi = {}
    for afi in afi_list:
        if afi in _AFI_PREFIX_FIELDS:
            sent_f, recv_f = _AFI_PREFIX_FIELDS[afi]
            if (v := peer.get(sent_f)) is not None:
                per_afi[f"{afi}_prefixes_sent"] = v
            if (v := peer.get(recv_f)) is not None:
                per_afi[f"{afi}_prefixes_received"] = v

    prefix_list_info = peer.get("prefixListInfo") or {}
    remote_address = peer.get("peerAddress")
    state = peer.get("state", "").lower()
    link_type = peer.get("linkType", "").lower()
    route_map_in = peer.get("routeMapInbound", "")
    route_map_out = peer.get("routeMapOutbound", "")

    return {
        "state": state if state in _BGP_STATES else None,
        "local_address": peer.get("updateSource"),
        "local_interface": peer.get("ifName"),
        "remote_address": remote_address,
        "local_as": int(peer["localAsn"]),
        "remote_as": int(peer["asn"]),
        "peer_group": peer.get("peerGroupName"),
        "import_policies": [route_map_in] if route_map_in else [],
        "export_policies": [route_map_out] if route_map_out else [],
        "prefix_list_in": prefix_list_info.get("inboundIpv4Uni"),
        "prefix_list_out": prefix_list_info.get("outboundIpv4Uni"),
        "name": f"{vrf}_{remote_address}" if remote_address else None,
        "description": peer.get("description"),
        "router_id": peer.get("routerId"),
        "peering_type": link_type if link_type in _LINK_TYPES else None,
        "vrf": vrf,
        "hold_time": peer.get("holdTime"),
        "keepalive": peer.get("keepaliveTime"),
        "uptime_seconds": peer.get("establishedTime"),
        "max_ttl": peer.get("maxTtlHops"),
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

    return [
        _normalize_peer(peer, vrf)
        for vrf, vrf_data in payload.get("vrfs", {}).items()
        for peer in vrf_data.get("peerList", [])
    ]
