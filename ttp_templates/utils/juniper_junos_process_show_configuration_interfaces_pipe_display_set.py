"""
Normalize Juniper JunOS interface configuration parsed by TTP into a
standardized list of dictionaries suitable for Netbox imports.

Transforms the parsed result of ``show configuration interfaces | display set``
into a flat list where each interface dictionary contains a fixed set of
keys. Missing or unknown values are returned as ``None`` (except
``description`` which is returned as an empty string when unset, and
``tagged_vlans`` which is an empty list when none).

Each logical unit appears as a separate record with name ``<iface>.<unit>``
(e.g. ``xe-0/0/1.0``, ``ae0.100``).  Physical-level properties (MTU, speed,
LAG membership) are stored on the physical interface record.
"""

from .models import InterfaceConfigRecord
from typing import Any, Dict, List

# JunOS interface speed config strings → kbit/s
_SPEED_MAP: Dict[str, int] = {
    "10m": 10_000,
    "100m": 100_000,
    "1g": 1_000_000,
    "10g": 10_000_000,
    "25g": 25_000_000,
    "40g": 40_000_000,
    "100g": 100_000_000,
    "400g": 400_000_000,
}

# Interface name prefixes that indicate a virtual (loopback/tunnel) interface
_VIRTUAL_PREFIXES = ("lo0", "st0", "ip-", "gr-", "si-", "pd-")


def transform_interfaces_config(payload: list) -> List[Dict[str, Any]]:
    """
    Transform TTP parse payload for Juniper JunOS interface blocks into a
    normalized list of interface dictionaries.

    Args:
        payload: TTP macro payload – a list produced by the ``interfaces**``
            table group, typically
            ``[{"interfaces": {<name>: {<props>}, ...}}]``.

    Returns:
        Normalized list of dictionaries with the fixed set of keys described
        in the template documentation.
    """
    if not payload:
        return []

    # With results="per_template" and a named table group, TTP passes a single
    # dict {"interfaces": {...}} to the macro.  Wrap it so the loop below works
    # for both list-of-dicts and bare-dict payloads.
    items = [payload] if isinstance(payload, dict) else payload

    # Flatten the nested {"interfaces": {name: data}} structure produced by
    # the TTP table groups into a simple {name: data} dict.
    raw = {}
    for item in items:
        if (
            isinstance(item, dict)
            and "interfaces" in item
            and isinstance(item["interfaces"], dict)
        ):
            raw.update(item["interfaces"])

    if not raw:
        return []

    # Build interface → VRF mapping from routing-instances groups.
    # The "vrf" key is only present when routing-instance lines appear in the
    iface_to_vrf = {}
    for item in items:
        vrf_data = item.get("vrf") if isinstance(item, dict) else None
        if not isinstance(vrf_data, dict):
            continue
        for vrf_name, vrf_info in vrf_data.items():
            for iface_name in vrf_info.get("interfaces") or []:
                iface_to_vrf[iface_name] = vrf_name

    normalized = []

    for name, data in raw.items():
        if not isinstance(data, dict):
            data = {}

        name_lower = name.lower()

        # Interface type
        if name_lower.startswith("irb"):
            interface_type = "bridge"
        elif name_lower.startswith("ae") and "." not in name:
            interface_type = "lag"
        elif "." in name or any(name_lower.startswith(p) for p in _VIRTUAL_PREFIXES):
            interface_type = "virtual"
        else:
            interface_type = "other"

        # extract interface parent except for irb and lo0 interfaces
        parent = None
        parent_interface_data = {}
        if (
            "." in name
            and not any(name.startswith(k) for k in ["irb.", "lo0."])
            and not any(name.startswith(p) for p in _VIRTUAL_PREFIXES)
        ):
            parent = name.split(".")[0]
            # extract parent data, not always device config has configuration for parent though
            parent_interface_data = raw.get(parent, {})

        speed_raw = data.get("speed")
        speed = _SPEED_MAP.get(speed_raw.lower() if speed_raw else "", None)
        description = (data.get("description") or "").strip('"')
        enabled = data.get("enabled", True)
        lag_id = data.get("lag_id")
        lag = None
        if lag_id:
            lag_id = int(lag_id.replace("ae", ""))
            if interface_type != "lag":
                lag = f"ae{lag_id}"

        # VLAN mode and untagged/tagged VLAN assignments
        mode = None
        untagged_vlan = None
        tagged_vlans = []

        # IRB units: untagged VLAN derived from the unit number (e.g. irb.10 → 10)
        if interface_type == "bridge":
            untagged_vlan = int(name.split(".")[1]) if "." in name else None
            mode = "access"

        # L3 sub-interface with explicit vlan-id tag
        dot1q = data.get("dot1q")
        if dot1q is not None:
            # handle case with natvie vlan id
            if parent_interface_data.get("untagged_vlan") == dot1q:
                untagged_vlan = parent_interface_data["untagged_vlan"]
                mode = "access"
            else:
                tagged_vlans = [int(dot1q)]
                mode = "tagged"

        # Ethernet-switching (L2) mode on units
        switching = data.get("switching")
        if isinstance(switching, dict):
            dot1q_mode = switching.get("dot1q_mode")
            vlans_raw = switching.get("vlans", [])
            vlan_ints = []
            for v in (vlans_raw if isinstance(vlans_raw, list) else []):
                if isinstance(v, dict) and v.get("vlan"):
                    try:
                        vlan_ints.append(int(v["vlan"]))
                    except (ValueError, TypeError):
                        pass
            if dot1q_mode == "trunk":
                mode = "tagged"
                tagged_vlans = sorted(set(tagged_vlans + vlan_ints))
            elif dot1q_mode == "access":
                mode = "access"
                if vlan_ints:
                    untagged_vlan = vlan_ints[0]

        ipv4_addresses = [
            f"{a['ip']}/{a['mask']}"
            for a in data.get("ipv4", [])
            if isinstance(a, dict) and a.get("ip") and a.get("mask")
        ]
        ipv6_addresses = [
            f"{a['ip']}/{a['mask']}"
            for a in data.get("ipv6", [])
            if isinstance(a, dict) and a.get("ip") and a.get("mask")
        ]
        ipv4_addresses.extend(
            [
                f"{a['vip']}/{a['mask']}"
                for a in data.get("ipv4", [])
                if isinstance(a, dict) and a.get("vip") and a.get("mask")
            ]
        )
        ipv6_addresses.extend(
            [
                f"{a['vip']}/{a['mask']}"
                for a in data.get("ipv6", [])
                if isinstance(a, dict) and a.get("vip") and a.get("mask")
            ]
        )

        record = {
            "name": name,
            "type": interface_type,
            "enabled": enabled,
            "parent": parent,
            "lag": lag,
            "lag_id": lag_id,
            "lag_type": data.get("lag_type"),
            "lacp_mode": data.get("lacp_mode"),
            "mtu": data.get("mtu"),
            "mac_address": data.get("mac_address"),
            "speed": speed,
            "duplex": data.get("duplex"),
            "description": description,
            "mode": mode,
            "untagged_vlan": untagged_vlan,
            "tagged_vlans": tagged_vlans,
            "ipv4_addresses": ipv4_addresses,
            "ipv6_addresses": ipv6_addresses,
            "qinq_svlan": None,
            "vrf": iface_to_vrf.get(name),
        }

        InterfaceConfigRecord(**record)
        normalized.append(record)

    return normalized
