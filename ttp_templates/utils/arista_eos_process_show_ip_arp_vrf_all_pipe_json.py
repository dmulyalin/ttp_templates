"""Normalize arista_eos ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/arista_eos_show_ip_arp_vrf_all_pipe_json.txt
"""

import ipaddress
import re
import json
from .models import ArpRecord

_EOS_NAMES = {
    "Et": "Ethernet",
    "Lo": "Loopback",
    "Ma": "Management",
    "Po": "Port-Channel",
    "Tu": "Tunnel",
    "Vl": "Vlan",
    "Vx": "Vxlan",
}


def transform_arista_eos(payload):
    """Return normalized IPv4 and IPv6 neighbor records from TTP groups."""
    groups = {}
    for item in payload if isinstance(payload, list) else [payload]:
        for name, rows in item.items():
            groups.setdefault(name, []).extend(
                rows if isinstance(rows, list) else [rows]
            )
    for name, rows in groups.items():
        text = "\n".join((row.get("data", "") for row in rows))
        documents = []
        decoder = json.JSONDecoder()
        while text.strip():
            document, end = decoder.raw_decode(text.lstrip())
            documents.append(document)
            text = text.lstrip()[end:]
        groups[name] = documents
    result = []
    for family, key in (("ipv4", "ipV4Neighbors"), ("ipv6", "ipV6Neighbors")):
        for document in groups.get(family, []):
            for vrf, table in document.get("vrfs", {}).items():
                for row in table.get(key, []):
                    interface = (row.get("interface") or "").split(",")[0].strip()
                    match = re.match("^([A-Za-z]+)(\\d.*)$", interface)
                    if match:
                        interface = _EOS_NAMES.get(match[1], match[1]) + match[2]
                    record = dict(
                        ip=row.get("address"),
                        mac=row.get("hwAddress"),
                        interface=interface,
                        vrf=vrf,
                        age=row.get("age") if family == "ipv4" else None,
                        state="static" if "age" not in row else None,
                    )
                    try:
                        address = ipaddress.ip_address(
                            str(record["ip"]).split("%")[0].strip()
                        )
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
                    record["state"] = record["state"] or (
                        "incomplete" if mac is None else None
                    )
                    age = record["age"]
                    try:
                        record["age"] = (
                            int(age)
                            if float(age) >= 0 and record["state"] != "static"
                            else None
                        )
                    except (TypeError, ValueError, OverflowError):
                        record["age"] = None
                    record["interface"] = record["interface"] or None
                    if record["vrf"] in (None, "", "default", "master", "global", "0"):
                        record["vrf"] = None
                    else:
                        record["vrf"] = str(record["vrf"])
                    result.append(ArpRecord(**record).model_dump())
    return result
