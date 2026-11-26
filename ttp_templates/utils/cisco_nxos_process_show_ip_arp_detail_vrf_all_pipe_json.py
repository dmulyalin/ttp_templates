"""Normalize cisco_nxos ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/cisco_nxos_show_ip_arp_detail_vrf_all_pipe_json.txt
"""

import ipaddress
import re
import json
from .models import ArpRecord


def transform_cisco_nxos(payload):
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
    for family in ("ipv4", "ipv6"):
        for document in groups.get(family, []):
            vrfs = document.get("TABLE_vrf", {}).get("ROW_vrf", [])
            for vrf in vrfs if isinstance(vrfs, list) else [vrfs]:
                tables = [vrf]
                if family == "ipv6":
                    tables = vrf.get("TABLE_afi", {}).get("ROW_afi", [])
                    tables = tables if isinstance(tables, list) else [tables]
                for table in tables:
                    rows = table.get("TABLE_adj", {}).get("ROW_adj", [])
                    for row in rows if isinstance(rows, list) else [rows]:
                        stamp = row.get("time-stamp") or ""
                        age = None
                        clock = re.fullmatch("(\\d+):(\\d{2}):(\\d{2})", stamp)
                        duration = re.fullmatch(
                            "P(?:(\\d+)D)?(?:T(?:(\\d+)H)?(?:(\\d+)M)?(?:(\\d+)S)?)?",
                            stamp,
                            re.I,
                        )
                        if clock:
                            age = (
                                int(clock[1]) * 3600
                                + int(clock[2]) * 60
                                + int(clock[3])
                            )
                        elif duration and stamp.upper() not in ("P", "PT"):
                            days, hours, minutes, seconds = (
                                int(part or 0) for part in duration.groups()
                            )
                            age = ((days * 24 + hours) * 60 + minutes) * 60 + seconds
                        record = dict(
                            ip=row.get(
                                "ip-addr-out" if family == "ipv4" else "ipv6-addr"
                            ),
                            mac=row.get("mac"),
                            interface=row.get("intf-out"),
                            vrf=row.get("adj-vrf-name"),
                            age=age,
                            state=None,
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
                        record["state"] = "incomplete" if mac is None else None
                        record["interface"] = record["interface"] or None
                        if record["vrf"] in (
                            None,
                            "",
                            "default",
                            "master",
                            "global",
                            "0",
                        ):
                            record["vrf"] = None
                        else:
                            record["vrf"] = str(record["vrf"])
                        result.append(ArpRecord(**record).model_dump())
    return result
