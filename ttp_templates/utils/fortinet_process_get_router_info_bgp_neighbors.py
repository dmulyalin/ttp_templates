"""Normalize Fortinet FortiOS ``get router info bgp neighbors`` output.

Used by:
- ttp_templates/platform/fortinet_get_router_info_bgp_neighbors.txt
"""

import re
from typing import Any

from .models import BgpNeighborRecord

_AFI_TO_IANA = {
    "IPv4 Unicast": "ipv4_unicast",
    "IPv6 Unicast": "ipv6_unicast",
    "VPNv4 Unicast": "ipv4_mpls_vpn",
    "VPNv6 Unicast": "ipv6_mpls_vpn",
    "L2VPN EVPN": "l2vpn_evpn",
}
_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}
_UNITS = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}


def _uptime_seconds(bgp_state: str) -> int | None:
    """Return seconds from ``Established, up for 00:00:26`` or ``1d02h``."""
    match = re.search(r"up for\s+(\S+)", bgp_state)
    if not match:
        return None
    value = match.group(1)
    if re.fullmatch(r"\d+:\d+:\d+", value):
        hours, minutes, seconds = map(int, value.split(":"))
        return hours * 3600 + minutes * 60 + seconds
    if re.fullmatch(r"(?:\d+[ywdhms])+", value):
        return sum(
            int(number) * _UNITS[unit]
            for number, unit in re.findall(r"(\d+)([ywdhms])", value)
        )
    return None


def transform_bgp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return validated normalized neighbor records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: list[dict[str, Any]] = []
    for item in items:
        for vrf_table in item.get("vrfs", []):
            vrf = None if vrf_table["vrf"] == "0" else vrf_table["vrf"]
            for neighbor in vrf_table.get("neighbors", []):
                address = neighbor["remote_address"]
                bgp_state = neighbor.get("bgp_state") or ""
                state = bgp_state.split(",", 1)[0].strip().lower()
                established = state == "established"
                peering_type = (neighbor.get("peering_type") or "").lower()
                record = {
                    "name": f"{vrf or 'default'}_{address}",
                    "vrf": vrf,
                    "remote_address": address,
                    "remote_as": neighbor["remote_as"],
                    "description": None,
                    "state": state if state in _STATES else None,
                    "local_address": neighbor.get("local_address"),
                    "local_as": neighbor.get("local_as"),
                    "local_interface": None,
                    "router_id": neighbor.get("router_id"),
                    "peer_group": None,
                    "peering_type": peering_type
                    if peering_type in {"internal", "external"}
                    else None,
                    "hold_time": neighbor.get("hold_time") if established else None,
                    "keepalive": neighbor.get("keepalive") if established else None,
                    "uptime_seconds": _uptime_seconds(bgp_state),
                    "max_ttl": None,
                    "afi": [],
                    "import_policies": [],
                    "export_policies": [],
                    "prefix_list_in": None,
                    "prefix_list_out": None,
                }
                for family in neighbor.get("families", []):
                    afi_name = family["afi_name"].strip()
                    afi = _AFI_TO_IANA.get(afi_name, afi_name.lower().replace(" ", "_"))
                    if afi not in record["afi"]:
                        record["afi"].append(afi)
                    for direction in ("sent", "received"):
                        count = family.get(f"prefixes_{direction}")
                        if count is not None:
                            record[f"{afi}_prefixes_{direction}"] = count
                records.append(
                    BgpNeighborRecord(**record).model_dump(exclude_unset=True)
                )
    return records
