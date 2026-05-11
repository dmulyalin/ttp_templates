"""
Normalize Cisco IOS-XR interface configuration parsed by TTP into a
standardized list of dictionaries suitable for Netbox imports.

Transforms the parsed result of ``show running-config interface``
into a flat list where each interface dictionary contains a fixed set of
keys. Missing or unknown values are returned as ``None`` (except
``description`` which is returned as an empty string when unset, and
``tagged_vlans`` which is an empty list when none).

IPv4 masks are stored in dotted notation by IOS-XR (e.g. 255.255.255.252)
and are converted to prefix-length notation in the output (e.g. /30).
"""

import ipaddress
from .models import InterfaceConfigRecord
from typing import Any, Dict, List


def _dotted_mask_to_prefix_len(mask: str) -> int:
    """Convert a dotted subnet mask to an integer prefix length.

    If ``mask`` is already an integer string (e.g. IPv6 prefix length),
    it is returned as-is.
    """
    if "." in mask:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
    return int(mask)


def transform_interfaces_config(payload: list) -> List[Dict[str, Any]]:
    """
    Transform TTP parse payload for Cisco IOS-XR interface blocks into a
    normalized list of interface dictionaries.

    Args:
        payload: TTP macro payload – a list of interface match dicts produced
            by the flat (unnamed) TTP group.

    Returns:
        Normalized list of dictionaries with the fixed set of keys described
        in the template documentation.
    """
    if not payload:
        return []

    normalized = []

    for iface in payload:
        if not isinstance(iface, dict) or not iface.get("name"):
            continue

        name = iface["name"]
        name_lower = name.lower()
        mode = iface.get("mode")
        untagged = iface.get("untagged")

        # Determine interface type – check "." first so Bundle-Ether sub-interfaces
        # are typed as virtual, not lag.
        if "bvi" in name_lower:
            interface_type = "bridge"
            untagged = int(name_lower.replace("bvi", ""))
            mode = "access"
        elif any(k in name_lower for k in [".", "loopback", "tunnel"]):
            interface_type = "virtual"
        elif "bundle" in name_lower:
            interface_type = "lag"
        else:
            interface_type = "other"

        lag_id = iface.get("lag_id")
        lag = None
        if lag_id and interface_type != "lag":
            lag = f"Bundle-Ether{lag_id}"
        speed = iface.get("speed")
        if speed is not None:
            speed = speed * 1000
        dot1q = iface.get("dot1q")
        tagged_vlans = [dot1q] if dot1q is not None else []

        ipv4_addresses = []
        for addr in iface.get("ipv4_addresses", []):
            if isinstance(addr, dict) and addr.get("ip") and addr.get("mask"):
                try:
                    prefix_len = _dotted_mask_to_prefix_len(str(addr["mask"]))
                    ipv4_addresses.append(f"{addr['ip']}/{prefix_len}")
                except (ValueError, TypeError):
                    ipv4_addresses.append(f"{addr['ip']}/{addr['mask']}")

        ipv6_addresses = [
            f"{a['ip']}/{a['mask']}"
            for a in iface.get("ipv6_addresses", [])
            if isinstance(a, dict) and a.get("ip") and a.get("mask")
        ]

        record = {
            "name": name,
            "type": interface_type,
            "enabled": iface.get("enabled", True),
            "parent": name.split(".")[0] if "." in name else None,
            "lag": lag,
            "lag_id": lag_id,
            "lag_type": iface.get("lag_type"),
            "lacp_mode": iface.get("lacp_mode"),
            "mtu": iface.get("mtu"),
            "mac_address": iface.get("mac_address"),
            "speed": speed,
            "duplex": iface.get("duplex"),
            "description": iface.get("description") or "",
            "mode": mode,
            "untagged_vlan": untagged,
            "tagged_vlans": tagged_vlans,
            "ipv4_addresses": ipv4_addresses,
            "ipv6_addresses": ipv6_addresses,
            "qinq_svlan": None,
            "vrf": iface.get("vrf"),
        }

        InterfaceConfigRecord(**record)
        normalized.append(record)

    return normalized
