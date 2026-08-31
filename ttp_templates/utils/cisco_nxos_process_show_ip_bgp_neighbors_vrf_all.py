"""Normalize Cisco NX-OS ``show ip bgp neighbors vrf all`` output.

Used by:
- ttp_templates/platform/cisco_nxos_show_ip_bgp_neighbors_vrf_all.txt
"""

import re
from typing import Any

from .models import BgpNeighborRecord


_AFI_TO_IANA = {
    "IPv4 Unicast": "ipv4_unicast",
    "IPv6 Unicast": "ipv6_unicast",
    "IPv4 Multicast": "ipv4_multicast",
    "IPv6 Multicast": "ipv6_multicast",
    "VPNv4 Unicast": "ipv4_mpls_vpn",
    "VPNv6 Unicast": "ipv6_mpls_vpn",
    "IPv4 Labeled Unicast": "ipv4_labeled_unicast",
    "IPv6 Labeled Unicast": "ipv6_labeled_unicast",
    "L2VPN EVPN": "l2vpn_evpn",
    "L2VPN VPLS": "l2vpn_vpls",
    "IPv4 MDT": "ipv4_mdt",
    "IPv4 Flow Specification": "ipv4_flow_spec",
    "IPv6 Flow Specification": "ipv6_flow_spec",
    "IPv4 SR-TE": "ipv4_sr_te",
    "IPv6 SR-TE": "ipv6_sr_te",
    "Link-state": "link_state",
}
_BGP_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}


def _uptime_to_seconds(value: str | None) -> int | None:
    """Convert NX-OS colon or compact duration notation to seconds."""
    if not value:
        return None

    colon_match = re.fullmatch(r"(\d+):(\d+):(\d+)", value)
    if colon_match:
        hours, minutes, seconds = map(int, colon_match.groups())
        return hours * 3600 + minutes * 60 + seconds

    duration_match = re.fullmatch(
        r"(?:(\d+)y)?(?:(\d+)w)?(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?",
        value,
    )
    if not duration_match or not any(duration_match.groups()):
        return None

    years, weeks, days, hours, minutes, seconds = (
        int(part or 0) for part in duration_match.groups()
    )
    return (
        years * 365 * 86400
        + weeks * 7 * 86400
        + days * 86400
        + hours * 3600
        + minutes * 60
        + seconds
    )


def _get_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return parsed neighbor dictionaries from TTP macro payload shapes."""
    items = [payload] if isinstance(payload, dict) else payload or []
    neighbors: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        parsed = item.get("neighbors", [])
        if isinstance(parsed, dict):
            parsed = [parsed]
        neighbors.extend(entry for entry in parsed if isinstance(entry, dict))
    return neighbors


def _normalize_neighbor(neighbor: dict[str, Any]) -> dict[str, Any]:
    """Map a parsed NX-OS neighbor to the common BGP getter contract."""
    raw_state = str(neighbor.get("bgp_state") or "")
    state_token = raw_state.split(",", 1)[0].strip().lower()
    uptime_match = re.search(r"up for\s+(\S+)", raw_state)

    link_type = str(neighbor.get("link_type") or "").lower()
    peering_type = {"ibgp": "internal", "ebgp": "external"}.get(link_type)
    remote_as = int(neighbor["remote_as"])
    local_as = remote_as if peering_type == "internal" else None

    afi: list[str] = []
    import_policies: list[str] = []
    export_policies: list[str] = []
    per_afi: dict[str, int] = {}
    for address_family in neighbor.get("address_families") or []:
        afi_name = str(address_family.get("afi_name") or "").strip()
        afi_key = _AFI_TO_IANA.get(afi_name, afi_name.lower().replace(" ", "_"))
        if afi_key and afi_key not in afi:
            afi.append(afi_key)

        if address_family.get("prefixes_received") is not None:
            per_afi[f"{afi_key}_prefixes_received"] = address_family[
                "prefixes_received"
            ]
        if address_family.get("prefixes_sent") is not None:
            per_afi[f"{afi_key}_prefixes_sent"] = address_family["prefixes_sent"]

        import_policy = address_family.get("import_policy")
        if import_policy and import_policy not in import_policies:
            import_policies.append(import_policy)
        export_policy = address_family.get("export_policy")
        if export_policy and export_policy not in export_policies:
            export_policies.append(export_policy)

    vrf_raw = neighbor.get("vrf") or "default"
    vrf = None if str(vrf_raw).lower() in {"default", "master"} else vrf_raw
    remote_address = neighbor["remote_address"]
    record = {
        "name": f"{vrf or 'default'}_{remote_address}",
        "vrf": vrf,
        "state": state_token if state_token in _BGP_STATES else None,
        "peering_type": peering_type,
        "remote_address": remote_address,
        "remote_as": remote_as,
        "local_address": neighbor.get("local_address"),
        "local_as": local_as,
        "local_interface": neighbor.get("local_interface"),
        "router_id": neighbor.get("router_id"),
        "peer_group": None,
        "description": neighbor.get("description") or None,
        "hold_time": neighbor.get("hold_time"),
        "keepalive": neighbor.get("keepalive"),
        "uptime_seconds": _uptime_to_seconds(
            uptime_match.group(1) if uptime_match else None
        ),
        "max_ttl": neighbor.get("max_ttl"),
        "afi": afi,
        "import_policies": import_policies,
        "export_policies": export_policies,
        "prefix_list_in": None,
        "prefix_list_out": None,
        **per_afi,
    }
    return BgpNeighborRecord(**record).model_dump(exclude_unset=True)


def transform_bgp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return validated normalized NX-OS BGP neighbor records."""
    return [_normalize_neighbor(neighbor) for neighbor in _get_neighbors(payload)]
