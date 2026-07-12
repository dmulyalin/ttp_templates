"""
Normalize A10 interface configuration parsed by TTP into a standardized list
of dictionaries suitable for Netbox imports.

Transforms the parsed result of
``show running-config partition-config all | section interface`` into a flat
list where each interface dictionary contains a fixed set of keys. Missing or
unknown values are returned as ``None`` (except ``description`` which is
returned as an empty string when unset, and ``tagged_vlans`` which is an empty
list when none).

Used by:
- ttp_templates/platform/a10_show_running_config_partition_config_all_pipe_section_interface.txt
"""

import ipaddress
from typing import Any

from .models import InterfaceConfigRecord


def _mask_to_prefix_len(mask: str) -> int:
    """Convert a dotted IPv4 mask or numeric mask to a prefix length."""
    if "." in mask:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask}", strict=False).prefixlen
    return int(mask)


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


def _vlan_id_from_identifier(identifier: Any) -> int | None:
    """Extract VLAN ID from A10 identifiers such as 1/100 or 100."""
    if identifier is None:
        return None

    vlan_id = str(identifier).rsplit("/", 1)[-1]
    try:
        return int(vlan_id)
    except ValueError:
        return None


def _context_from_identifier(identifier: Any) -> str | None:
    """Return the leading context from an A10 slash-delimited identifier."""
    if identifier is None:
        return None

    value = str(identifier)
    if "/" not in value:
        return None
    return value.split("/", 1)[0]


def _interface_name(iface: dict[str, Any]) -> str:
    """Build normalized A10 interface name from parsed kind and identifier."""
    kind = iface.get("kind")
    if kind == "management":
        return "management"
    return f"{kind} {iface.get('identifier')}"


def _interface_type(kind: str | None) -> str:
    """Infer normalized interface type from A10 interface kind."""
    if kind == "trunk":
        return "lag"
    if kind == "ve":
        return "bridge"
    return "other"


def _coerce_payload(payload: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return interface and VLAN records from TTP macro payload."""
    interfaces: list[dict[str, Any]] = []
    vlans: list[dict[str, Any]] = []

    items = payload if isinstance(payload, list) else [payload]
    for item in items:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("interfaces"), list):
            interfaces.extend(i for i in item["interfaces"] if isinstance(i, dict))
        if isinstance(item.get("vlans"), list):
            vlans.extend(v for v in item["vlans"] if isinstance(v, dict))
        if item.get("kind") or item.get("name") == "management":
            interfaces.append(item)
        if item.get("tagged_trunk_id") or item.get("router_interface"):
            vlans.append(item)

    return interfaces, vlans


def _trunk_name_by_id(interfaces: list[dict[str, Any]]) -> dict[int, str]:
    """Map trunk-group IDs to full A10 trunk interface names."""
    trunks: dict[int, str] = {}
    for iface in interfaces:
        if iface.get("kind") != "trunk":
            continue

        trunk_id = _vlan_id_from_identifier(iface.get("identifier"))
        if trunk_id is not None:
            trunks[trunk_id] = _interface_name(iface)

    return trunks


def _tagged_vlans_by_trunk(vlans: list[dict[str, Any]]) -> dict[int, list[int]]:
    """Map A10 trunk IDs to tagged VLAN IDs."""
    tagged: dict[int, set[int]] = {}
    for vlan in vlans:
        trunk_id = vlan.get("tagged_trunk_id")
        vlan_id = _vlan_id_from_identifier(vlan.get("identifier"))
        if trunk_id is None or vlan_id is None:
            continue

        tagged.setdefault(trunk_id, set()).add(vlan_id)

    return {trunk_id: sorted(vlan_ids) for trunk_id, vlan_ids in tagged.items()}


def _vlan_by_router_interface(vlans: list[dict[str, Any]]) -> dict[tuple[str | None, int], int]:
    """Map A10 router-interface VE IDs to VLAN IDs."""
    router_interfaces: dict[tuple[str | None, int], int] = {}
    for vlan in vlans:
        router_interface = vlan.get("router_interface")
        vlan_id = _vlan_id_from_identifier(vlan.get("identifier"))
        if router_interface is None or vlan_id is None:
            continue

        key = (_context_from_identifier(vlan.get("identifier")), router_interface)
        router_interfaces[key] = vlan_id

    return router_interfaces


def transform_interfaces_config(payload: Any) -> list[dict[str, Any]]:
    """
    Transform TTP parse payload for A10 interface blocks into normalized records.

    Args:
        payload: TTP macro payload.

    Returns:
        Normalized list of dictionaries with the fixed set of keys described in
        the template documentation.
    """
    interfaces, vlans = _coerce_payload(payload)
    if not interfaces:
        return []

    trunk_names = _trunk_name_by_id(interfaces)
    tagged_vlans = _tagged_vlans_by_trunk(vlans)
    router_vlans = _vlan_by_router_interface(vlans)

    normalized_interfaces: list[dict[str, Any]] = []

    for iface in interfaces:
        kind = iface.get("kind")
        if not kind and iface.get("name") == "management":
            kind = "management"
        if kind not in {"management", "ethernet", "trunk", "ve"}:
            continue

        name = _interface_name({**iface, "kind": kind})
        interface_type = _interface_type(kind)
        lag_id = iface.get("lag_id")
        lag_type = iface.get("lag_type")
        lacp_mode = iface.get("lacp_mode")
        lag = None
        if lag_id is not None and interface_type != "lag":
            lag = trunk_names.get(lag_id) or f"trunk {lag_id}"

        mode = None
        untagged_vlan = None
        interface_tagged_vlans: list[int] = []
        if kind == "trunk":
            trunk_id = _vlan_id_from_identifier(iface.get("identifier"))
            interface_tagged_vlans = tagged_vlans.get(trunk_id, [])
            if interface_tagged_vlans:
                mode = "tagged"
        elif kind == "ve":
            ve_id = _vlan_id_from_identifier(iface.get("identifier"))
            context = _context_from_identifier(iface.get("identifier"))
            untagged_vlan = router_vlans.get((context, ve_id)) or ve_id
            mode = "access"

        record: dict[str, Any] = {
            "name": name,
            "type": interface_type,
            "enabled": iface.get("enabled", True),
            "parent": None,
            "lag": lag,
            "lag_id": lag_id,
            "lag_type": lag_type,
            "lacp_mode": lacp_mode,
            "mtu": iface.get("mtu"),
            "mac_address": None,
            "speed": None,
            "duplex": None,
            "description": iface.get("description") or "",
            "mode": mode,
            "untagged_vlan": untagged_vlan,
            "tagged_vlans": interface_tagged_vlans,
            "ipv4_addresses": _normalize_ip_addresses(iface.get("ipv4_addresses")),
            "ipv6_addresses": _normalize_ip_addresses(iface.get("ipv6_addresses")),
            "qinq_svlan": None,
            "vrf": None,
        }

        record = InterfaceConfigRecord(**record).model_dump()
        normalized_interfaces.append(record)

    return normalized_interfaces
