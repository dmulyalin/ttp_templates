"""Normalize linux ARP and IPv6 neighbor output.

Used by: ttp_templates/platform/linux_ip_neigh_show.txt
"""

import ipaddress
import re
import json
from .models import ArpRecord


def transform_linux(payload):
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
    links = [link for document in groups.get("links", []) for link in document]
    vrf_names = {
        link.get("ifname")
        for link in links
        if (link.get("linkinfo") or {}).get("info_kind") == "vrf"
    }
    vrfs = {
        link.get("ifname"): link.get("master")
        for link in links
        if link.get("master") in vrf_names
    }
    result = []
    for document in groups.get("neighbors", []):
        for row in document:
            states = [state.lower() for state in row.get("state", [])]
            if "noarp" in states:
                continue
            state = next(
                (
                    state
                    for state in states
                    if state
                    in (
                        "incomplete",
                        "reachable",
                        "stale",
                        "delay",
                        "probe",
                        "failed",
                        "permanent",
                        "static",
                    )
                ),
                None,
            )
            record = dict(
                ip=row.get("dst"),
                mac=row.get("lladdr"),
                interface=row.get("dev"),
                vrf=vrfs.get(row.get("dev")),
                age=row.get("confirmed"),
                state=state,
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
            record["state"] = "static" if state == "permanent" else state
            if record["state"] is None and mac is None:
                record["state"] = "incomplete"
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
