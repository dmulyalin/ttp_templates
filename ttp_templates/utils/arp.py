"""Shared normalization for ``arp`` getter records: the IPv4 ARP table and the
IPv6 neighbor cache.

The platform templates capture each table's rows, as the device prints them,
in an ``ipv4`` and an ``ipv6`` group (JSON output as a ``data`` blob), and
where the tables don't name the VRF, a third group mapping interfaces to
VRFs. Each platform has one function here turning those groups into records.

Used by:
- ttp_templates/platform/arista_eos_show_ip_arp_vrf_all_pipe_json.txt
- ttp_templates/platform/cisco_asa_show_arp.txt
- ttp_templates/platform/cisco_ios_show_ip_arp.txt
- ttp_templates/platform/cisco_nxos_show_ip_arp_detail_vrf_all_pipe_json_pretty.txt
- ttp_templates/platform/cisco_xr_show_arp_vrf_all.txt
- ttp_templates/platform/fortinet_diagnose_ip_arp_list.txt
- ttp_templates/platform/juniper_junos_show_arp_no_resolve_pipe_display_json.txt
- ttp_templates/platform/linux_ip_neigh_show.txt
"""

import ipaddress
import json
import re
from typing import Any, Callable, Dict, List, Optional

from .models import ArpRecord

# RFC 4861 neighbor states, plus static for configured entries
_STATES = {
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
}
# Linux kernel NUD_* flags, as FortiOS prints them in hex
_NUD = {
    0x01: "incomplete",
    0x02: "reachable",
    0x04: "stale",
    0x08: "delay",
    0x10: "probe",
    0x20: "failed",
    0x80: "static",
}
_NUD_NOARP = 0x40
_MAC = re.compile(
    r"^(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}$|^(?:[0-9a-f]{4}\.){2}[0-9a-f]{4}$", re.I
)
_ISO_DURATION = re.compile(
    r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$", re.I
)
_CLOCK = re.compile(r"^(\d+):(\d{2}):(\d{2})$")


def groups(payload: Any) -> Dict[str, List[Dict[str, Any]]]:
    """Return the template's groups as one dictionary of lists, whether TTP
    passed a dictionary or a list of them."""
    items = payload if isinstance(payload, list) else [payload]
    merged: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        for name, rows in item.items():
            rows = rows if isinstance(rows, list) else [rows]
            merged.setdefault(name, []).extend(r for r in rows if isinstance(r, dict))
    return merged


def documents(rows: List[Dict[str, Any]]) -> List[Any]:
    """Return the JSON documents in a group's captured lines (``data``, one
    row per line): pretty-printed or on one line, one or more of them."""
    text = "\n".join(str(row.get("data", "")) for row in rows)
    decoder = json.JSONDecoder()
    found = []
    position = 0
    while True:
        starts = [
            i for i in (text.find("{", position), text.find("[", position)) if i >= 0
        ]
        if not starts:
            return found
        document, position = decoder.raw_decode(text, min(starts))
        found.append(document)


def _ip(text: Optional[str]) -> Optional[str]:
    """Return the address in its compressed lowercase form, or None for one
    that isn't a neighbor (multicast, unspecified) or not an address."""
    try:
        address = ipaddress.ip_address(str(text).split("%")[0].strip())
    except ValueError:
        return None
    if address.is_multicast or address.is_unspecified:
        return None
    return str(address)


def _mac(text: Optional[str]) -> Optional[str]:
    """Return a MAC address as lowercase colon-separated hex, or None for an
    unresolved entry (``Incomplete``, ``-``, all zeros)."""
    text = (text or "").strip()
    if not _MAC.match(text):
        return None
    digits = re.sub(r"[^0-9a-f]", "", text.lower())
    if not digits.strip("0"):
        return None
    return ":".join(digits[i : i + 2] for i in range(0, 12, 2))


def _state(word: Optional[str]) -> Optional[str]:
    return _STATES.get((word or "").strip().lower())


def _int(text: Any) -> Optional[int]:
    try:
        value = int(text)
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


def _seconds(text: Optional[str]) -> Optional[int]:
    """Return seconds from ``h:mm:ss`` or an ISO 8601 duration (``PT11M23S``)."""
    text = (text or "").strip()
    clock = _CLOCK.match(text)
    if clock:
        return int(clock[1]) * 3600 + int(clock[2]) * 60 + int(clock[3])
    duration = _ISO_DURATION.match(text)
    if duration and text.upper() not in ("P", "PT"):
        days, hours, minutes, seconds = (int(x or 0) for x in duration.groups())
        return ((days * 24 + hours) * 60 + minutes) * 60 + seconds
    return None


def _minutes(text: Optional[str]) -> Optional[int]:
    value = _int(text)
    return None if value is None else value * 60


def record(
    ip: Optional[str],
    mac: Optional[str] = None,
    interface: Optional[str] = None,
    vrf: Optional[str] = None,
    age: Optional[int] = None,
    state: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Return one validated record, or None for an entry that isn't a
    neighbor. An entry with no MAC address and no state is incomplete; a
    static entry has no age."""
    address = _ip(ip)
    if address is None:
        return None
    mac = _mac(mac)
    if state is None and mac is None:
        state = "incomplete"
    if state == "static":
        age = None
    vrf = None if vrf in (None, "", "default", "master", "global", "0") else str(vrf)
    return ArpRecord(
        ip=address,
        mac=mac,
        interface=interface or None,
        vrf=vrf,
        age=age,
        state=state,
    ).model_dump()


def _kept(records: List[Optional[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    return [r for r in records if r is not None]


def _abbreviated(name: str, full: List[str]) -> str:
    """Return the one name in ``full`` that ``name`` abbreviates (``Gi1.977``
    for ``GigabitEthernet1.977``), or ``name`` when there isn't exactly one."""
    if name in full:
        return name
    short = re.match(r"^([A-Za-z-]+)(.*)$", name)
    if not short:
        return name
    found = []
    for candidate in full:
        long = re.match(r"^([A-Za-z-]+)(.*)$", candidate)
        if (
            long
            and long[2] == short[2]
            and long[1].lower().startswith(short[1].lower())
        ):
            found.append(candidate)
    return found[0] if len(found) == 1 else name


def _vrf_of(vrfs: Dict[str, str]) -> Callable[[Optional[str]], Optional[str]]:
    names = list(vrfs)

    def vrf(interface: Optional[str]) -> Optional[str]:
        if not interface:
            return None
        return vrfs.get(_abbreviated(interface, names))

    return vrf


def _expanded(name: Optional[str], prefixes: Dict[str, str]) -> Optional[str]:
    """Return an abbreviated interface name (``Gi1.977``) in full, where its
    letters are a known abbreviation; otherwise as printed."""
    if not name:
        return name
    match = re.match(r"^([A-Za-z]+)(\d.*)$", name)
    if match and match[1] in prefixes:
        return prefixes[match[1]] + match[2]
    return name


# Abbreviations IOS and IOS-XE print in `show ipv6 neighbors`
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
# Abbreviations EOS prints in `show ipv6 neighbors`
_EOS_NAMES = {
    "Et": "Ethernet",
    "Lo": "Loopback",
    "Ma": "Management",
    "Po": "Port-Channel",
    "Tu": "Tunnel",
    "Vl": "Vlan",
    "Vx": "Vxlan",
}


def transform_cisco_ios(payload: Any) -> List[Dict[str, Any]]:
    """`show ip arp` (ages in minutes) and `show ipv6 neighbors` (minutes,
    abbreviated interface names). A `-` for the age marks a configured entry
    or one of the router's own addresses; both are static."""
    g = groups(payload)
    out = []
    for row in g.get("ipv4", []):
        static = row.get("age") == "-"
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                row.get("interface"),
                age=_minutes(row.get("age")),
                state="static" if static else None,
            )
        )
    for row in g.get("ipv6", []):
        static = row.get("age") == "-"
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                _expanded(row.get("interface"), _IOS_NAMES),
                age=_minutes(row.get("age")),
                state="static" if static else _state(row.get("state")),
            )
        )
    return _kept(out)


def transform_cisco_asa(payload: Any) -> List[Dict[str, Any]]:
    """`show arp` (by nameif, ages in seconds; `alias` marks the ASA's own
    proxy entries, which are left out) and `show ipv6 neighbor` (minutes),
    with `show nameif` for the interface names. The ASA has no VRFs."""
    g = groups(payload)
    names = {r["name"]: r["interface"] for r in g.get("nameif", []) if "name" in r}
    out = []
    for row in g.get("ipv4", []):
        if row.get("age") == "alias":
            continue
        static = row.get("age") == "-"
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                names.get(row.get("interface"), row.get("interface")),
                age=_int(row.get("age")),
                state="static" if static else None,
            )
        )
    for row in g.get("ipv6", []):
        static = row.get("age") == "-"
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                names.get(row.get("interface"), row.get("interface")),
                age=_minutes(row.get("age")),
                state="static" if static else _state(row.get("state")),
            )
        )
    return _kept(out)


def transform_cisco_xr(payload: Any) -> List[Dict[str, Any]]:
    """`show arp vrf all` (ages `h:mm:ss`; the router's own addresses,
    `Interface`, are left out) and `show ipv6 neighbors` (abbreviated
    interface names), with each interface's VRF from
    `show ipv4 vrf all interface brief` and `show ipv6 vrf all interface brief`."""
    g = groups(payload)
    v4 = {
        r["interface"]: r.get("vrf")
        for r in g.get("ipv4_interfaces", [])
        if "interface" in r
    }
    v6 = {
        r["interface"]: r.get("vrf")
        for r in g.get("ipv6_interfaces", [])
        if "interface" in r
    }
    out = []
    for row in g.get("ipv4", []):
        state = (row.get("state") or "").lower()
        if state == "interface":
            continue
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                row.get("interface"),
                v4.get(row.get("interface")),
                _seconds(row.get("age")),
                _state(state),
            )
        )
    full = list(v6) + [n for n in v4 if n not in v6]
    for row in g.get("ipv6", []):
        interface = _abbreviated(row.get("interface") or "", full) or None
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                interface,
                v6.get(interface or "", v4.get(interface or "")),
                None,
                _state(row.get("state")),
            )
        )
    return _kept(out)


def _rows(table: Any, key: str) -> List[Dict[str, Any]]:
    """NX-OS JSON's ``TABLE_x``/``ROW_x``: a dictionary for one row, a list
    for several."""
    rows = (table or {}).get(key, []) if isinstance(table, dict) else []
    return [rows] if isinstance(rows, dict) else list(rows)


def transform_cisco_nxos(payload: Any) -> List[Dict[str, Any]]:
    """`show ip arp detail vrf all | json` and `show ipv6 neighbor vrf all
    | json`: each entry names its VRF (`adj-vrf-name`); ages are ISO 8601
    durations for IPv4 (`PT11M23S`) and `hh:mm:ss` for IPv6."""
    g = groups(payload)
    out = []
    for document in documents(g.get("ipv4", [])):
        for vrf in _rows(document.get("TABLE_vrf"), "ROW_vrf"):
            for row in _rows(vrf.get("TABLE_adj"), "ROW_adj"):
                out.append(
                    record(
                        row.get("ip-addr-out"),
                        row.get("mac"),
                        row.get("intf-out"),
                        row.get("adj-vrf-name"),
                        _seconds(row.get("time-stamp")),
                    )
                )
    for document in documents(g.get("ipv6", [])):
        for vrf in _rows(document.get("TABLE_vrf"), "ROW_vrf"):
            for afi in _rows(vrf.get("TABLE_afi"), "ROW_afi"):
                for row in _rows(afi.get("TABLE_adj"), "ROW_adj"):
                    out.append(
                        record(
                            row.get("ipv6-addr"),
                            row.get("mac"),
                            row.get("intf-out"),
                            row.get("adj-vrf-name"),
                            _seconds(row.get("time-stamp")),
                        )
                    )
    return _kept(out)


def transform_arista_eos(payload: Any) -> List[Dict[str, Any]]:
    """`show ip arp vrf all | json` (ages in seconds) and `show ipv6
    neighbors vrf all | json` (abbreviated interface names; its `age` is not
    an age in seconds, so IPv6 entries have none). An SVI's entry names the
    VLAN interface and the port (`Vlan10, Ethernet1`); the VLAN interface is
    kept."""
    g = groups(payload)
    out = []
    for family, key in (("ipv4", "ipV4Neighbors"), ("ipv6", "ipV6Neighbors")):
        for document in documents(g.get(family, [])):
            for vrf, table in document.get("vrfs", {}).items():
                for row in table.get(key, []):
                    interface = (row.get("interface") or "").split(",")[0].strip()
                    out.append(
                        record(
                            row.get("address"),
                            row.get("hwAddress"),
                            _expanded(interface, _EOS_NAMES),
                            vrf,
                            _int(row.get("age")) if family == "ipv4" else None,
                        )
                    )
    return _kept(out)


def _junos(entry: Dict[str, Any], key: str) -> Optional[str]:
    """One leaf of Junos JSON (``{"key": [{"data": "value"}]}``)."""
    values = entry.get(key) or [{}]
    return values[0].get("data") if isinstance(values[0], dict) else None


def transform_juniper_junos(payload: Any) -> List[Dict[str, Any]]:
    """`show arp no-resolve | display json` (no age; `permanent` marks a
    static entry) and `show ipv6 neighbors | display json` (its `expire` is
    a countdown, not an age), with each unit's routing instance from
    `show route instance detail | display json`. Entries on units in Junos's
    own instances (`__juniper_private1__`) are left out."""
    g = groups(payload)
    instance_of = {}
    for document in documents(g.get("instances", [])):
        for information in document.get("instance-information", []):
            for instance in information.get("instance-core", []):
                name = _junos(instance, "instance-name")
                for member in instance.get("instance-interface", []):
                    unit = _junos(member, "interface-name")
                    if unit:
                        instance_of[unit] = name
    out = []
    for document in documents(g.get("ipv4", [])):
        for table in document.get("arp-table-information", []):
            for entry in table.get("arp-table-entry", []):
                unit = _junos(entry, "interface-name")
                if (instance_of.get(unit) or "").startswith("__"):
                    continue
                flags = (entry.get("arp-table-entry-flags") or [{}])[0]
                out.append(
                    record(
                        _junos(entry, "ip-address"),
                        _junos(entry, "mac-address"),
                        unit,
                        instance_of.get(unit),
                        state="static" if "permanent" in flags else None,
                    )
                )
    for document in documents(g.get("ipv6", [])):
        for table in document.get("ipv6-nd-information", []):
            for entry in table.get("ipv6-nd-entry", []):
                unit = _junos(entry, "ipv6-nd-interface-name")
                if (instance_of.get(unit) or "").startswith("__"):
                    continue
                out.append(
                    record(
                        _junos(entry, "ipv6-nd-neighbor-address"),
                        _junos(entry, "ipv6-nd-neighbor-l2-address"),
                        unit,
                        instance_of.get(unit),
                        state=_state(_junos(entry, "ipv6-nd-state")),
                    )
                )
    return _kept(out)


def transform_fortinet(payload: Any) -> List[Dict[str, Any]]:
    """`diagnose ip arp list` and `diagnose ipv6 neighbor-cache list`, the
    kernel's tables: the state a hex NUD flag (NOARP entries, such as
    multicast and the VDOM's own, are left out), `confirm` in hundredths of
    a second. Each interface's VRF from `show system interface`."""
    g = groups(payload)
    vrfs = {
        r["interface"]: r.get("vrf")
        for r in g.get("interfaces", [])
        if "interface" in r
    }
    out = []
    for row in g.get("ipv4", []) + g.get("ipv6", []):
        try:
            flags = int(row.get("state", ""), 16)
        except ValueError:
            continue
        if flags & _NUD_NOARP:
            continue
        state = next((name for bit, name in _NUD.items() if flags & bit), None)
        confirm = _int(row.get("confirm"))
        out.append(
            record(
                row.get("ip"),
                row.get("mac"),
                row.get("interface"),
                vrfs.get(row.get("interface")),
                None if confirm is None else confirm // 100,
                state,
            )
        )
    return _kept(out)


def transform_linux(payload: Any) -> List[Dict[str, Any]]:
    """`ip -j -s neigh show` (IPv4 and IPv6 together; `confirmed` in
    seconds), with each link's VRF, its master where that is a VRF, from
    `ip -j -d link show`. NOARP entries are left out."""
    g = groups(payload)
    links = [link for d in documents(g.get("links", [])) for link in d]
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
    out = []
    for document in documents(g.get("neighbors", [])):
        for entry in document:
            states = [s.lower() for s in entry.get("state", [])]
            if "noarp" in states:
                continue
            state = next((_state(s) for s in states if _state(s)), None)
            out.append(
                record(
                    entry.get("dst"),
                    entry.get("lladdr"),
                    entry.get("dev"),
                    vrfs.get(entry.get("dev")),
                    _int(entry.get("confirmed")),
                    state,
                )
            )
    return _kept(out)
