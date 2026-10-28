"""Normalize Cisco ASA BGP neighbor output and running configuration.

Used by:
- ttp_templates/platform/cisco_asa_show_bgp_neighbors.txt
"""

import re
from typing import Any

from .models import BgpNeighborRecord

_AFI_TO_IANA = {
    "IPv4 Unicast": "ipv4_unicast",
    "IPv6 Unicast": "ipv6_unicast",
}
_STATES = {"idle", "connect", "active", "opensent", "openconfirm", "established"}
_UNITS = {"y": 31536000, "w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}


def _asn(value: str) -> int:
    """Return an ASN given as plain or asdot (``1.10``) notation."""
    high, _, low = value.partition(".")
    return int(high) * 65536 + int(low) if low else int(high)


def _uptime_seconds(bgp_state: str) -> int | None:
    """Return seconds from ``Established, up for 00:00:24`` or ``1d02h``."""
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
    """Merge IPv4 and IPv6 neighbor output with the running configuration and
    validate normalized neighbor records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    router_asn = None
    configs: dict[str, dict[str, Any]] = {}
    for item in items:
        bgp = item.get("bgp_config", {})
        if "router_asn" in bgp:
            router_asn = _asn(bgp["router_asn"])
        for family in bgp.get("families", []):
            for statement in family.get("statements", []):
                config = configs.setdefault(statement["peer"], {})
                if "policy" in statement:
                    policies = config.setdefault(statement["direction"], [])
                    if statement["policy"] not in policies:
                        policies.append(statement["policy"])
                elif "description" in statement:
                    config["description"] = statement["description"]

    records: dict[str, dict[str, Any]] = {}
    for item in items:
        for neighbor in item.get("neighbors", []):
            address = neighbor["remote_address"]
            state = (neighbor.get("bgp_state") or "").split(",", 1)[0].strip().lower()
            peering_type = (neighbor.get("peering_type") or "").lower()
            record = records.setdefault(
                address,
                {
                    "name": f"default_{address}",
                    "vrf": None,
                    "remote_address": address,
                    "remote_as": neighbor["remote_as"],
                    "description": neighbor.get("description"),
                    "state": state if state in _STATES else None,
                    "local_address": None,
                    "local_as": router_asn,
                    "local_interface": None,
                    "router_id": neighbor.get("router_id"),
                    "peer_group": None,
                    "peering_type": peering_type
                    if peering_type in {"internal", "external"}
                    else None,
                    "hold_time": neighbor.get("hold_time"),
                    "keepalive": neighbor.get("keepalive"),
                    "uptime_seconds": _uptime_seconds(neighbor.get("bgp_state") or ""),
                    "max_ttl": None,
                    "afi": [],
                    "import_policies": [],
                    "export_policies": [],
                    "prefix_list_in": None,
                    "prefix_list_out": None,
                },
            )
            for family in neighbor.get("families", []):
                afi_name = family["afi_name"].strip()
                afi = _AFI_TO_IANA.get(afi_name, afi_name.lower().replace(" ", "_"))
                if afi not in record["afi"]:
                    record["afi"].append(afi)
                for direction in ("sent", "received"):
                    count = family.get(f"prefixes_{direction}")
                    if count is not None:
                        record[f"{afi}_prefixes_{direction}"] = count
                for source, target in (
                    ("import_policy", "import_policies"),
                    ("export_policy", "export_policies"),
                ):
                    policy = family.get(source)
                    if policy and policy not in record[target]:
                        record[target].append(policy)

    for address, record in records.items():
        config = configs.get(address, {})
        if "description" in config:
            record["description"] = config["description"]
        for direction, target in (
            ("in", "import_policies"),
            ("out", "export_policies"),
        ):
            for policy in config.get(direction, []):
                if policy not in record[target]:
                    record[target].append(policy)
    return [
        BgpNeighborRecord(**record).model_dump(exclude_unset=True)
        for record in records.values()
    ]
