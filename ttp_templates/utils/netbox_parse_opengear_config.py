"""
Post-process Opengear configuration data for Netbox imports.

Used by:
- ttp_templates/misc/Netbox/parse_opengear_config.txt
"""

from typing import Any, Dict


def process_interface(data: Dict[str, Any]) -> Dict[str, Any] | bool:
    """
    Normalize Opengear interface names and enabled state.

    Only the ``wan`` and ``lan`` interfaces are kept. Other Opengear config
    entries are ignored by returning ``False`` for the TTP group function.
    """
    if not data.get("name"):
        return False

    data["description"] = ""

    if data["disabled"] == "on":
        data.pop("disabled")
        data["enabled"] = False
    else:
        data.pop("disabled")
        data["enabled"] = True

    if data["name"] == "wan":
        data["name"] = "eth0"
        data["label"] = "wan"
        data["interface_type"] = "bridge"
    elif data["name"] == "lan":
        data["name"] = "eth1"
        data["label"] = "lan"
        data["interface_type"] = "bridge"
    else:
        return False

    return data


def process_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert interface dictionaries into Netbox-friendly interface lists."""
    interfaces = []
    for intf_name, intf_data in data.get("interfaces", {}).items():
        if intf_data.get("ipv4") and intf_data.get("maskv4"):
            intf_data["ipv4"] = [
                {"ip": intf_data.pop("ipv4"), "mask": intf_data.pop("maskv4")}
            ]

        interfaces.append(intf_data)
        interfaces[-1]["name"] = intf_name

    data["interfaces"] = interfaces

    return data
