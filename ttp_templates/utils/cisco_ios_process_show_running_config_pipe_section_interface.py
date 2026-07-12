"""
Normalize Cisco IOS interface configuration parsed by TTP into a standardized
list of dictionaries suitable for Netbox imports.

Transforms the parsed result of ``show running-config | section interface``
into a flat list where each interface dictionary contains a fixed set of keys.
Missing or unknown values are returned as ``None`` (except ``description``
which is returned as an empty string when unset, and ``tagged_vlans`` which is
an empty list when none).

Used by:
- ttp_templates/platform/cisco_ios_show_running_config_pipe_section_interface.txt
"""

import ipaddress
from typing import Any

from .models import InterfaceConfigRecord


def _mask_to_prefix_len(mask: str) -> int:
    """Convert a dotted IPv4 mask or numeric mask to a prefix length."""
    if "." in mask:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
    return int(mask)


def _flatten_vlan_values(values: Any) -> list[int]:
    """Flatten TTP VLAN captures into a sorted list of unique integers."""
    if values is None:
        return []

    raw_values = values if isinstance(values, list) else [values]
    vlans: list[int] = []
    for item in raw_values:
        if isinstance(item, list):
            vlans.extend(_flatten_vlan_values(item))
            continue

        for value in str(item).split(","):
            try:
                vlans.append(int(value))
            except (TypeError, ValueError):
                continue

    return sorted(set(vlans))


def _normalize_ip_addresses(addresses: Any) -> list[str]:
    """Return IP addresses as strings in IP/prefix notation."""
    if not isinstance(addresses, list):
        return []

    normalized: list[str] = []
    for addr in addresses:
        if not isinstance(addr, dict) or not addr.get("ip") or not addr.get("mask"):
            continue

        try:
            mask = _mask_to_prefix_len(str(addr["mask"]))
        except (TypeError, ValueError):
            mask = addr["mask"]
        normalized.append(f"{addr['ip']}/{mask}")

    return normalized


def _normalize_speed(speed: Any) -> int | None:
    """Return interface speed in kbit/s when IOS speed is numeric."""
    try:
        return int(speed) * 1000
    except (TypeError, ValueError):
        return None


def _interface_type(name: str) -> str:
    """Infer the normalized interface type from an IOS interface name."""
    name_lower = name.lower()

    if "vlan" in name_lower or "bvi" in name_lower:
        return "bridge"
    if "port-channel" in name_lower:
        return "lag"
    if any(marker in name_lower for marker in [".", "loopback", "tunnel"]):
        return "virtual"
    return "other"


def _vlan_id_from_name(name: str, prefix: str) -> int | None:
    """Extract a VLAN id from names such as Vlan100 or BVI100."""
    try:
        return int(name.lower().replace(prefix, "", 1))
    except ValueError:
        return None


def transform_interfaces_config(payload: list) -> list[dict[str, Any]]:
    """
    Transform TTP parse payload for Cisco IOS interface blocks into a
    normalized list of interface dictionaries.

    Args:
        payload: TTP macro payload.

    Returns:
        Normalized list of dictionaries with the fixed set of keys described
        in the template documentation.
    """
    if not payload:
        return []

    normalized_interfaces: list[dict[str, Any]] = []

    for iface in payload:
        if not isinstance(iface, dict) or not iface.get("name"):
            continue

        name = iface["name"]
        name_lower = name.lower()
        interface_type = _interface_type(name)
        lag_id = iface.get("lag_id")
        lag_type = iface.get("lag_type")
        lag = None
        if lag_id and interface_type != "lag":
            lag = f"Port-channel{lag_id}"

        mode = iface.get("mode")
        untagged_vlan = iface.get("untagged_vlan")
        tagged_vlans = _flatten_vlan_values(iface.get("tagged_vlans"))

        dot1q = iface.get("dot1q")
        if dot1q is not None and dot1q not in tagged_vlans:
            tagged_vlans.append(dot1q)
            tagged_vlans = sorted(set(tagged_vlans))
            mode = mode or "tagged"

        if interface_type == "bridge":
            if "vlan" in name_lower:
                untagged_vlan = _vlan_id_from_name(name, "vlan")
            elif "bvi" in name_lower:
                untagged_vlan = _vlan_id_from_name(name, "bvi")
            mode = "access"
        elif untagged_vlan is not None and mode is None:
            mode = "access"
        elif tagged_vlans and mode is None:
            mode = "tagged"

        record: dict[str, Any] = {
            "name": name,
            "type": interface_type,
            "enabled": iface.get("enabled", True),
            "parent": name.split(".", 1)[0] if "." in name else None,
            "lag": lag,
            "lag_id": lag_id,
            "lag_type": lag_type,
            "lacp_mode": iface.get("lacp_mode"),
            "mtu": iface.get("mtu") or None,
            "mac_address": iface.get("mac_address"),
            "speed": _normalize_speed(iface.get("speed")),
            "duplex": iface.get("duplex"),
            "description": iface.get("description") or "",
            "mode": mode,
            "untagged_vlan": untagged_vlan,
            "tagged_vlans": tagged_vlans,
            "ipv4_addresses": _normalize_ip_addresses(iface.get("ipv4_addresses")),
            "ipv6_addresses": _normalize_ip_addresses(iface.get("ipv6_addresses")),
            "qinq_svlan": iface.get("qinq_svlan"),
            "vrf": iface.get("vrf"),
        }

        record = InterfaceConfigRecord(**record).model_dump()
        normalized_interfaces.append(record)

    return normalized_interfaces
