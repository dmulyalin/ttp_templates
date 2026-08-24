"""
Normalize Cisco IOS-XR LLDP neighbor detail output to a standardized format.

Used by:
- ttp_templates/platform/cisco_xr_show_lldp_neighbors_detail.txt
"""

from typing import Any, Dict, Iterable, List

from ttp_templates.utils.models import LldpNeighborRecord


def _iter_neighbors(payload: Any) -> Iterable[Dict[str, Any]]:
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


def _normalize_neighbor(neighbor: Dict[str, Any]) -> Dict[str, Any]:
    """Map raw IOS-XR fields to the LLDP getter record contract."""
    system_description = neighbor.get("remote_system_description") or None

    return {
        "interface": neighbor["interface"],
        "remote_device": neighbor.get("remote_device") or None,
        "remote_interface": neighbor.get("remote_interface") or None,
        "remote_system_description": system_description,
        "remote_chassi_id": neighbor.get("remote_chassi_id") or None,
        "remote_interface_description": neighbor.get(
            "remote_interface_description"
        )
        or None,
        "remote_device_management_ip": neighbor.get("ipv4_address")
        or neighbor.get("ipv6_address")
        or None,
    }


def transform_lldp_neighbors(payload: Any) -> List[Dict[str, Any]]:
    """Return validated normalized LLDP neighbor records."""
    return [
        LldpNeighborRecord(**_normalize_neighbor(neighbor)).model_dump()
        for neighbor in _iter_neighbors(payload)
    ]
