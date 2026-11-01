"""Normalize fortinet ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/fortinet_diagnose_ip_arp_list.txt
"""

import ipaddress
import re
from .models import ArpRecord

_NUD = {
    1: "incomplete",
    2: "reachable",
    4: "stale",
    8: "delay",
    16: "probe",
    32: "failed",
    128: "static",
}


def transform_fortinet(payload):
    """Return normalized IPv4 and IPv6 neighbor records from TTP groups."""
    groups = {}
    for item in payload if isinstance(payload, list) else [payload]:
        for name, rows in item.items():
            groups.setdefault(name, []).extend(
                rows if isinstance(rows, list) else [rows]
            )
    vrfs = {row["interface"]: row.get("vrf") for row in groups.get("interfaces", [])}
    result = []
    for row in groups.get("ipv4", []) + groups.get("ipv6", []):
        try:
            flags = int(row.get("state", ""), 16)
        except ValueError:
            continue
        if flags & 64:
            continue
        confirm = row.get("confirm")
        record = dict(
            ip=row.get("ip"),
            mac=row.get("mac"),
            interface=row.get("interface"),
            vrf=vrfs.get(row.get("interface")),
            age=int(confirm) // 100 if str(confirm).isdigit() else None,
            state=next((name for bit, name in _NUD.items() if flags & bit), None),
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
            "(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}|(?:[0-9a-f]{4}\\.){2}[0-9a-f]{4}", mac
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
        record["state"] = record["state"] or ("incomplete" if mac is None else None)
        if record["state"] == "static":
            record["age"] = None
        record["interface"] = record["interface"] or None
        if record["vrf"] in (None, "", "default", "master", "global", "0"):
            record["vrf"] = None
        else:
            record["vrf"] = str(record["vrf"])
        result.append(ArpRecord(**record).model_dump())
    return result
