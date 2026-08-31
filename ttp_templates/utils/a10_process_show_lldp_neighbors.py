"""Normalize A10 ACOS ``show lldp neighbors`` output.

Used by:
- ttp_templates/platform/a10_show_lldp_neighbors.txt
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
    """Convert a space-delimited MAC chassis ID to colon notation."""
    chassis_id = str(value or "").strip().lower()
    octets = chassis_id.split()
    if len(octets) == 6 and all(
        len(octet) == 2 and all(char in "0123456789abcdef" for char in octet)
        for octet in octets
    ):
        return ":".join(octets)
    return chassis_id or None


def _normalize_neighbor(neighbor: dict[str, Any]) -> dict[str, Any]:
    """Map parsed A10 fields to the LLDP getter contract."""
    return {
        "interface": str(neighbor["interface"]).strip().lower(),
        "remote_device": neighbor.get("remote_device") or None,
        "remote_interface": neighbor.get("remote_interface") or None,
        "remote_system_description": neighbor.get("remote_system_description")
        or None,
        "remote_chassi_id": _normalize_chassis_id(
            neighbor.get("remote_chassi_id_raw")
        ),
        "remote_interface_description": neighbor.get(
            "remote_interface_description"
        )
        or None,
        "remote_device_management_ip": neighbor.get(
            "remote_device_management_ip"
        )
        or None,
    }


def transform_lldp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return validated normalized LLDP neighbor records."""
    return [
        LldpNeighborRecord(**_normalize_neighbor(neighbor)).model_dump()
        for neighbor in _iter_neighbors(payload)
        if neighbor.get("interface")
    ]
