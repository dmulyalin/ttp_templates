"""
Normalize Arista EOS LLDP neighbors JSON output to a standardized format.

Transforms raw JSON output from 'show lldp neighbors detail | json' into a
normalized list of dictionaries suitable for further processing and integrations.
"""

import json
from typing import Any, Dict, List, Optional


def _first_mgmt_ip(management_addresses: list) -> Optional[str]:
    """Return the first management IP address, or None."""
    for entry in management_addresses:
        if isinstance(entry, dict) and "address" in entry:
            return entry["address"]
    return None


def _normalize_neighbor(interface: str, neighbor: Dict[str, Any]) -> Dict[str, Any]:
    neighbor_iface = neighbor.get("neighborInterfaceInfo") or {}
    mgmt_addresses = neighbor.get("managementAddresses") or []

    return {
        "interface": interface,
        "remote_device": neighbor.get("systemName"),
        "remote_interface": neighbor_iface.get("interfaceId_v2"),
        "remote_system_description": neighbor.get("systemDescription"),
        "remote_chassi_id": neighbor.get("chassisId"),
        "remote_interface_description": neighbor_iface.get("interfaceDescription"),
        "remote_device_management_ip": _first_mgmt_ip(mgmt_addresses),
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
        _normalize_neighbor(interface, neighbor)
        for interface, iface_data in payload.get("lldpNeighbors", {}).items()
        for neighbor in iface_data.get("lldpNeighborInfo", [])
    ]
