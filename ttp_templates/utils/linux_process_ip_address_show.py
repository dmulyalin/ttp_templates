"""
Normalize Linux interface state parsed by TTP into the interfaces getter shape.

Transforms the parsed result of ``ip address show`` into a flat list where each
interface dictionary contains the same keys used by network OS interface
templates. Linux output is operational state, so configuration-only fields
such as VLAN mode, LAG membership, speed and duplex are returned as ``None`` or
empty lists.

Used by:
- ttp_templates/platform/linux_ip_address_show.txt
"""

from typing import Any, Dict, List

from .models import InterfaceConfigRecord


def _get_interface_type(name: str, flags: List[str]) -> str:
    """Map Linux interface name and flags to the common getter type values."""
    name_lower = name.lower()

    if name_lower.startswith(("br", "docker")):
        return "bridge"
    if name_lower.startswith(("bond", "team")):
        return "lag"
    if (
        name_lower == "lo"
        or name_lower.startswith(
            ("dummy", "gpd", "gre", "ipip", "sit", "tun", "tap", "vrf", "wg")
        )
        or "LOOPBACK" in flags
        or "POINTOPOINT" in flags
        or "MASTER" in flags
        or "." in name
    ):
        return "virtual"
    return "other"


def _build_ip_list(items: Any) -> List[str]:
    """Convert TTP IP/mask dictionaries into ``address/prefix`` strings."""
    if not isinstance(items, list):
        return []

    addresses = []
    for item in items:
        if isinstance(item, dict) and item.get("ip") and item.get("mask"):
            addresses.append(f"{item['ip']}/{item['mask']}")
    return addresses


def transform_interfaces(payload: list) -> List[Dict[str, Any]]:
    """
    Transform TTP parse payload for Linux ``ip address show`` into normalized
    interface records.

    Args:
        payload: TTP macro payload, usually a list of dictionaries produced by
            the interface group.

    Returns:
        Normalized list of dictionaries with the fixed interfaces getter keys.
    """
    if not payload:
        return []

    normalized = []

    for iface in payload:
        if not isinstance(iface, dict) or not iface.get("name"):
            continue

        name = iface["name"]
        flags = [flag.strip() for flag in iface.get("flags", "").split(",")]
        master = iface.get("master")

        record = {
            "name": name,
            "type": _get_interface_type(name, flags),
            "enabled": "UP" in flags,
            "parent": name.split(".", 1)[0] if "." in name else None,
            "lag": None,
            "lag_id": None,
            "lag_type": None,
            "lacp_mode": None,
            "mtu": iface.get("mtu") or None,
            "mac_address": iface.get("mac_address"),
            "speed": None,
            "duplex": None,
            "description": "",
            "mode": None,
            "untagged_vlan": None,
            "tagged_vlans": [],
            "ipv4_addresses": _build_ip_list(iface.get("ipv4_addresses")),
            "ipv6_addresses": _build_ip_list(iface.get("ipv6_addresses")),
            "qinq_svlan": None,
            "vrf": master if master and master.lower().startswith("vrf") else None,
        }

        normalized.append(InterfaceConfigRecord(**record).model_dump())

    return normalized
