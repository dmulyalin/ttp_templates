"""
Helpers for Cisco NX-OS Netbox configuration parsing.

Used by:
- ttp_templates/misc/Netbox/parse_cisco_nxos_config.txt
"""

from typing import Any, Dict


def add_interface_type(data: Dict[str, Any]) -> Dict[str, Any]:
    """Classify Cisco NX-OS interface type for Netbox."""
    data["interface_type"] = "other"
    virtual_markers = [".", "loopback", "tunnel", "vlan", "nve"]
    if any(i in data["name"].lower() for i in virtual_markers):
        data["interface_type"] = "virtual"
    elif any(i in data["name"].lower() for i in ["vlan", "nve"]):
        data["interface_type"] = "bridge"
    elif "port-channel" in data["name"].lower():
        data["interface_type"] = "lag"
    return data
