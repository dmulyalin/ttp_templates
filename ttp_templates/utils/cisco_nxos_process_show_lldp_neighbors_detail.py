"""Normalize Cisco NX-OS ``show lldp neighbors detail`` output.

Used by:
- ttp_templates/platform/cisco_nxos_show_lldp_neighbors_detail.txt
"""

from collections.abc import Iterable
from typing import Any

from .models import LldpNeighborRecord


def _iter_neighbors(payload: Any) -> Iterable[dict[str, Any]]:
    """Yield parsed neighbor dictionaries from supported TTP payload shapes."""
    items = [payload] if isinstance(payload, dict) else payload or []
    for item in items:
        if not isinstance(item, dict):
            continue

        neighbors = item.get("neighbors", [])
        if isinstance(neighbors, dict):
            neighbors = [neighbors]
        for neighbor in neighbors:
            if isinstance(neighbor, dict):
                yield neighbor


def _normalize_chassis_id(value: Any) -> str | None:
    """Convert dotted, colon, hyphen, or plain MAC chassis IDs to colons."""
    chassis_id = str(value or "").strip().lower()
    compact = chassis_id.replace(".", "").replace(":", "").replace("-", "")
    if len(compact) == 12 and all(char in "0123456789abcdef" for char in compact):
        return ":".join(compact[index : index + 2] for index in range(0, 12, 2))
    return chassis_id or None


def _advertised_value(value: Any) -> str | None:
    """Return None for missing or explicitly unadvertised LLDP values."""
    normalized = str(value or "").strip()
    return None if not normalized or normalized.lower() == "not advertised" else normalized


def _normalize_neighbor(neighbor: dict[str, Any]) -> dict[str, Any]:
    """Map parsed NX-OS fields to the LLDP getter contract."""
    management_ip = _advertised_value(neighbor.get("management_ipv4"))
    if management_ip is None:
        management_ip = _advertised_value(neighbor.get("management_ipv6"))

    return {
        "interface": str(neighbor["interface"]).strip(),
        "remote_device": _advertised_value(neighbor.get("remote_device")),
        "remote_interface": _advertised_value(neighbor.get("remote_interface")),
        "remote_system_description": _advertised_value(
            neighbor.get("remote_system_description")
        ),
        "remote_chassi_id": _normalize_chassis_id(
            neighbor.get("remote_chassi_id_raw")
        ),
        "remote_interface_description": _advertised_value(
            neighbor.get("remote_interface_description")
        ),
        "remote_device_management_ip": management_ip,
    }


def transform_lldp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return validated normalized NX-OS LLDP neighbor records."""
    return [
        LldpNeighborRecord(**_normalize_neighbor(neighbor)).model_dump()
        for neighbor in _iter_neighbors(payload)
        if neighbor.get("interface")
    ]
