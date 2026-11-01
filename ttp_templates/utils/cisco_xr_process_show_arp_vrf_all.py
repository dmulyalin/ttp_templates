"""Normalize cisco_xr ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/cisco_xr_show_arp_vrf_all.txt
"""

import ipaddress
import re
from .models import ArpRecord


def transform_cisco_xr(payload):
    """Return normalized IPv4 and IPv6 neighbor records from TTP groups."""
    groups = {}
    for item in payload if isinstance(payload, list) else [payload]:
        for name, rows in item.items():
            groups.setdefault(name, []).extend(
                rows if isinstance(rows, list) else [rows]
            )
    ipv4_vrfs = {
        row["interface"]: row.get("vrf") for row in groups.get("ipv4_interfaces", [])
    }
    ipv6_vrfs = {
        row["interface"]: row.get("vrf") for row in groups.get("ipv6_interfaces", [])
    }
    interfaces = {**ipv4_vrfs, **ipv6_vrfs}
    result = []
    seen = set()
    for family in ("ipv4", "ipv6"):
        for row in groups.get(family, []):
            if (row.get("state") or "").lower() == "interface":
                continue
            interface = row.get("interface")
            if family == "ipv6" and interface and (interface not in interfaces):
                short = re.match("^([A-Za-z-]+)(.*)$", interface)
                matches = []
                for name in interfaces:
                    full = re.match("^([A-Za-z-]+)(.*)$", name)
                    if (
                        short
                        and full
                        and (short[2] == full[2])
                        and full[1].lower().startswith(short[1].lower())
                    ):
                        matches.append(name)
                if len(matches) == 1:
                    interface = matches[0]
            age = None
            clock = re.fullmatch("(\\d+):(\\d{2}):(\\d{2})", row.get("age") or "")
            if family == "ipv4" and clock:
                age = int(clock[1]) * 3600 + int(clock[2]) * 60 + int(clock[3])
            record = dict(
                ip=row.get("ip"),
                mac=row.get("mac"),
                interface=interface,
                vrf=(ipv4_vrfs if family == "ipv4" else interfaces).get(interface),
                age=age,
                state=row.get("state"),
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
            if record["vrf"] in (None, "", "default", "master", "global", "0"):
                record["vrf"] = None
            else:
                record["vrf"] = str(record["vrf"])
            normalized = ArpRecord(**record).model_dump()
            key = (
                normalized["ip"],
                normalized["mac"],
                normalized["interface"],
                normalized["vrf"],
            )
            if key not in seen:
                seen.add(key)
                result.append(normalized)
    return result
