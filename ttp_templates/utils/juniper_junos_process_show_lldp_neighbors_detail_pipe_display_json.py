"""
Normalize Juniper JunOS LLDP neighbors JSON output to a standardized format.

Transforms raw JSON output from 'show lldp neighbors detail | display json' into a
normalized list of dictionaries suitable for further processing and integrations.

Used by:
- ttp_templates/platform/juniper_junos_show_lldp_neighbors_detail_pipe_display_json.txt
"""

import json
from typing import Any, Dict, List, Optional

from ttp_templates.utils.models import LldpNeighborRecord


def _get_data(obj: Dict[str, Any], field: str, default: Any = None) -> Any:
    """Extract the first .data value from a Juniper JSON array field."""
    items = obj.get(field)
    if items and isinstance(items, list) and isinstance(items[0], dict):
        return items[0].get("data", default)
    return default


def _get_system_description(neighbor: Dict[str, Any]) -> Optional[str]:
    """Extract lldp-remote-system-description from the nested lldp-system-description block."""
    outer = neighbor.get("lldp-system-description")
    if outer and isinstance(outer, list) and isinstance(outer[0], dict):
        return _get_data(outer[0], "lldp-remote-system-description")
    return None


def _normalize_neighbor(neighbor: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "interface": _get_data(neighbor, "lldp-local-interface"),
        "remote_device": _get_data(neighbor, "lldp-remote-system-name"),
        "remote_interface": _get_data(neighbor, "lldp-remote-port-id"),
        "remote_system_description": _get_system_description(neighbor),
        "remote_chassi_id": _get_data(neighbor, "lldp-remote-chassis-id"),
        "remote_interface_description": _get_data(
            neighbor, "lldp-remote-port-description"
        ),
        "remote_device_management_ip": _get_data(
            neighbor, "lldp-remote-management-address"
        ),
    }


def transform_lldp_neighbors(payload: list) -> List[Dict[str, Any]]:
    """
    Main transformation function to be used as TTP macro.

    Args:
        payload: Parsing results, JSON string of show command output.

    Returns:
        List of normalized LLDP neighbor dictionaries, one entry per
        (local_interface, remote_neighbor) pair.
    """
    if payload:
        payload = json.loads("{" + payload[0]["data"] + "}")
    else:
        return []

    if isinstance(payload, list) and payload:
        payload = payload[0]

    return [
        LldpNeighborRecord(**_normalize_neighbor(neighbor)).model_dump()
        for info_block in payload.get("lldp-neighbors-information", [])
        for neighbor in info_block.get("lldp-neighbor-information", [])
    ]
