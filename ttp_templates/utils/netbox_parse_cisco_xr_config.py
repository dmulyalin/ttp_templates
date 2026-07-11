"""
Helpers for Cisco IOS-XR Netbox configuration parsing.

Used by:
- ttp_templates/misc/Netbox/parse_cisco_xr_config.txt
"""

from typing import Any, Dict


def add_interface_type(data: Dict[str, Any]) -> Dict[str, Any]:
    """Classify Cisco IOS-XR interface type for Netbox."""
    data["interface_type"] = "other"
    if any(i in data["name"].lower() for i in [".", "loopback", "tunnel"]):
        data["interface_type"] = "virtual"
    elif any(i in data["name"].lower() for i in ["bvi"]):
        data["interface_type"] = "bridge"
    elif "bundle" in data["name"].lower():
        data["interface_type"] = "lag"
    return data
