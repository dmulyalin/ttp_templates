"""Normalize cisco_ios ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/cisco_ios_show_ip_arp.txt
"""

import ipaddress
import re
from .models import ArpRecord

_IOS_NAMES = {
    "Ap": "AppGigabitEthernet",
    "BD": "BDI",
    "Et": "Ethernet",
    "Fa": "FastEthernet",
    "Fo": "FortyGigabitEthernet",
    "Gi": "GigabitEthernet",
    "Hu": "HundredGigE",
    "Lo": "Loopback",
    "Po": "Port-channel",
    "Se": "Serial",
    "Te": "TenGigabitEthernet",
    "Tu": "Tunnel",
    "Tw": "TwoGigabitEthernet",
    "Twe": "TwentyFiveGigE",
    "Vl": "Vlan",
}


def transform_cisco_ios(payload, vrf=None):
    """Return normalized IPv4 and IPv6 neighbor records from TTP groups."""
    groups = {}
    for item in payload if isinstance(payload, list) else [payload]:
        for name, rows in item.items():
            groups.setdefault(name, []).extend(
                rows if isinstance(rows, list) else [rows]
            )
    result = []
    for family in ("ipv4", "ipv6"):
        for row in groups.get(family, []):
            interface = row.get("interface")
            if family == "ipv6" and interface:
                match = re.match("^([A-Za-z]+)(\\d.*)$", interface)
                if match:
                    interface = _IOS_NAMES.get(match[1], match[1]) + match[2]
            age = row.get("age")
            record = dict(
                ip=row.get("ip"),
                mac=row.get("mac"),
                interface=interface,
                vrf=vrf,
                age=int(age) * 60 if str(age).isdigit() else None,
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
            if record["vrf"] in (None, "", "default", "master", "global", "0"):
                record["vrf"] = None
            else:
                record["vrf"] = str(record["vrf"])
            result.append(ArpRecord(**record).model_dump())
    return result
