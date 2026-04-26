"""
Normalize Cisco IOS-XR BGP neighbors text output to a standardized format.

Transforms TTP-parsed output from 'show bgp neighbors' into a normalized
list of dictionaries suitable for further processing and integrations.
"""

import re

# XR display name -> IANA AFI/SAFI name
_AFI_TO_IANA = {
    "IPv4 Unicast": "ipv4_unicast",
    "IPv6 Unicast": "ipv6_unicast",
    "IPv4 Multicast": "ipv4_multicast",
    "IPv6 Multicast": "ipv6_multicast",
    "VPNv4 Unicast": "ipv4_mpls_vpn",
    "VPNv6 Unicast": "ipv6_mpls_vpn",
    "IPv4 Labeled-unicast": "ipv4_labeled_unicast",
    "IPv6 Labeled-unicast": "ipv6_labeled_unicast",
    "L2VPN EVPN": "l2vpn_evpn",
    "L2VPN Vpls": "l2vpn_vpls",
    "IPv4 MDT": "ipv4_mdt",
    "IPv4 Flowspec": "ipv4_flow_spec",
    "IPv6 Flowspec": "ipv6_flow_spec",
    "IPv4 SR policy": "ipv4_sr_te",
    "IPv6 SR policy": "ipv6_sr_te",
    "Link-state Link-state": "link_state",
}

_BGP_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}
_LINK_TYPES = {"external", "internal"}


def _uptime_to_seconds(uptime):
    if not uptime:
        return None
    m = re.match(r"^(\d+):(\d+):(\d+)$", uptime)
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    m = re.match(r"(?:(\d+)w)?(?:(\d+)d)?(?:(\d+)h)?", uptime)
    if m:
        return (
            int(m.group(1) or 0) * 604800
            + int(m.group(2) or 0) * 86400
            + int(m.group(3) or 0) * 3600
        )
    return None


def transform_bgp_neighbors(data):
    if isinstance(data, dict):
        neighbors = data.get("neighbors") or []
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        neighbors = data[0].get("neighbors") or []
    else:
        return []

    result = []
    for n in neighbors:
        raw_state = n.get("bgp_state") or ""
        state_token = raw_state.split(",")[0].strip().lower()
        state = state_token if state_token in _BGP_STATES else None

        uptime_match = re.search(r"up for\s+(\S+)", raw_state)
        uptime = _uptime_to_seconds(uptime_match.group(1) if uptime_match else None)

        peering_raw = (n.get("peering_type") or "").lower()
        remote_address = n.get("remote_address")

        afi_list = []
        per_afi = {}
        import_policy = None
        export_policy = None
        local_address = n.get("local_address")

        for af in n.get("address_families") or []:
            afi_raw = af.get("afi_name") or ""
            afi_key = (
                _AFI_TO_IANA.get(afi_raw, afi_raw.lower().replace(" ", "_"))
                if afi_raw
                else None
            )
            if afi_key and afi_key not in afi_list:
                afi_list.append(afi_key)
            if afi_key:
                try:
                    per_afi[f"{afi_key}_prefixes_received"] = int(
                        af["accepted_prefixes"]
                    )
                except (KeyError, TypeError, ValueError):
                    pass
                try:
                    per_afi[f"{afi_key}_prefixes_sent"] = int(af["prefixes_sent"])
                except (KeyError, TypeError, ValueError):
                    pass
            if import_policy is None:
                import_policy = (af.get("import_policy") or "").strip() or None
            if export_policy is None:
                export_policy = (af.get("export_policy") or "").strip() or None
            if local_address is None:
                local_address = af.get("local_address")

        result.append(
            {
                "name": f"default_{remote_address}" if remote_address else None,
                "vrf": "default",
                "state": state,
                "peering_type": peering_raw if peering_raw in _LINK_TYPES else None,
                "remote_address": remote_address,
                "remote_as": int(n.get("remote_as")),
                "local_address": local_address,
                "local_as": int(n.get("local_as")),
                "local_interface": None,
                "router_id": n.get("router_id"),
                "peer_group": None,
                "description": n.get("description"),
                "hold_time": int(n["hold_time"]) if n.get("hold_time") else None,
                "keepalive": int(n["keepalive"]) if n.get("keepalive") else None,
                "uptime_seconds": uptime,
                "max_ttl": None,
                "afi": afi_list,
                "import_policies": [import_policy] if import_policy else [],
                "export_policies": [export_policy] if export_policy else [],
                "prefix_list_in": None,
                "prefix_list_out": None,
                **per_afi,
            }
        )

    return result
