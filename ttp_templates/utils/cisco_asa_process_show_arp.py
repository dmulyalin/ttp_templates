"""Normalize cisco_asa ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/cisco_asa_show_arp.txt
"""

import ipaddress
import re
from .models import ArpRecord


def transform_cisco_asa(payload):
    """Return normalized IPv4 and IPv6 neighbor records from TTP groups."""
    groups = {}
    for item in payload if isinstance(payload, list) else [payload]:
        for name, rows in item.items():
            groups.setdefault(name, []).extend(
                rows if isinstance(rows, list) else [rows]
            )
    names = {row["name"]: row["interface"] for row in groups.get("nameif", [])}
    result = []
    for family in ("ipv4", "ipv6"):
        for row in groups.get(family, []):
            age = row.get("age")
            if family == "ipv4" and age == "alias":
                continue
            interface = row.get("interface")
            record = dict(
                ip=row.get("ip"),
                mac=row.get("mac"),
                interface=names.get(interface, interface),
                vrf=None,
                age=int(age) * (60 if family == "ipv6" else 1)
                if str(age).isdigit()
                else None,
                state="static" if age == "-" else row.get("state"),
            )
            try:
                address = ipaddress.ip_address(str(record["ip"]).split("%")[0].strip())
            except ValueError:
                continue
            if address.is_multicast or address.is_unspecified:
                continue
            record["ip"] = str(address)
            mac = (record["mac"] or "").strip().lower()
            if re.fullmatch(
                "(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}|(?:[0-9a-f]{4}\\.){2}[0-9a-f]{4}",
                mac,
            ):
                digits = re.sub("[^0-9a-f]", "", mac)
                mac = (
                    ":".join((digits[i : i + 2] for i in range(0, 12, 2)))
                    if int(digits, 16)
                    else None
                )
            else:
                mac = None
            record["mac"] = mac
            record["state"] = {
                "incmp": "incomplete",
                "incomplete": "incomplete",
                "reach": "reachable",
                "reachable": "reachable",
                "stale": "stale",
                "delay": "delay",
                "probe": "probe",
                "failed": "failed",
                "permanent": "static",
                "static": "static",
            }.get((record["state"] or "").lower())
            if record["state"] is None and mac is None:
                record["state"] = "incomplete"
            if record["state"] == "static":
                record["age"] = None
            record["interface"] = record["interface"] or None
            result.append(ArpRecord(**record).model_dump())
    return result
