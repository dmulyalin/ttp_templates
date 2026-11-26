"""Normalize juniper_junos ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/juniper_junos_show_arp_no_resolve_pipe_display_json.txt
"""

import ipaddress
import re
import json
from .models import ArpRecord


def transform_juniper_junos(payload):
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
    instances = {}
    for document in groups.get("instances", []):
        for information in document.get("instance-information", []):
            for instance in information.get("instance-core", []):
                name = (instance.get("instance-name") or [{}])[0].get("data")
                for member in instance.get("instance-interface", []):
                    unit = (member.get("interface-name") or [{}])[0].get("data")
                    instances[unit] = name
    result = []
    for family, table_key, row_key in (
        ("ipv4", "arp-table-information", "arp-table-entry"),
        ("ipv6", "ipv6-nd-information", "ipv6-nd-entry"),
    ):
        for document in groups.get(family, []):
            for table in document.get(table_key, []):
                for entry in table.get(row_key, []):
                    row = {
                        key: (values or [{}])[0].get("data")
                        for key, values in entry.items()
                        if isinstance(values, list)
                    }
                    interface = row.get(
                        "interface-name"
                        if family == "ipv4"
                        else "ipv6-nd-interface-name"
                    )
                    vrf = instances.get(interface)
                    if (vrf or "").startswith("__"):
                        continue
                    flags = (entry.get("arp-table-entry-flags") or [{}])[0]
                    record = dict(
                        ip=row.get(
                            "ip-address"
                            if family == "ipv4"
                            else "ipv6-nd-neighbor-address"
                        ),
                        mac=row.get(
                            "mac-address"
                            if family == "ipv4"
                            else "ipv6-nd-neighbor-l2-address"
                        ),
                        interface=interface,
                        vrf=vrf,
                        age=None,
                        state="static"
                        if "permanent" in flags
                        else row.get("ipv6-nd-state"),
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
                    record["interface"] = record["interface"] or None
                    if record["vrf"] in (None, "", "default", "master", "global", "0"):
                        record["vrf"] = None
                    else:
                        record["vrf"] = str(record["vrf"])
                    result.append(ArpRecord(**record).model_dump())
    return result
