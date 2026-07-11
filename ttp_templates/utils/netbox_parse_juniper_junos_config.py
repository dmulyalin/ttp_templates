"""
Post-process Juniper Junos configuration data for Netbox imports.

Used by:
- ttp_templates/misc/Netbox/parse_juniper_junos_config.txt
"""

from typing import Any, Dict


def postprocess(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize VRF and interface dictionaries into Netbox-friendly lists."""
    data["vrf"] = [{"name": k, **v} for k, v in data.get("vrf", {}).items()]

    for vrf in data["vrf"]:
        for interface in vrf.get("interfaces", []):
            if data["interfaces"].get(interface):
                data["interfaces"][interface]["vrf"] = vrf["name"]

    data["interfaces"] = [
        {"name": k, **v} for k, v in data.get("interfaces", {}).items()
    ]

    for interface in data["interfaces"]:
        interface["interface_type"] = "other"
        if "irb" in interface["name"]:
            interface["interface_type"] = "bridge"
            interface["switching"] = {
                "dot1q_mode": "access",
                "vlans": [int(interface["name"].split(".")[1])],
            }
        elif any(k in interface["name"] for k in [".", "gr-", "lo0", "vlan"]):
            interface["interface_type"] = "virtual"
        elif "ae" in interface["name"]:
            interface["interface_type"] = "lag"

        if "." in interface["name"] and not any(
            k in interface["name"] for k in ["lo0", "vlan", "irb", "gr-"]
        ):
            interface["parent"] = interface["name"].split(".")[0]

        if interface.get("switching", {}).get("vlans", []):
            vlans = []
            for vlan in interface.get("switching", {}).get("vlans", []):
                if isinstance(vlan, dict):
                    vlans.append(vlan["vlan"])
                else:
                    vlans.append(vlan)
            interface["switching"]["vlans"] = vlans

        switching = interface.get("switching", {})
        if switching.get("dot1q_mode") == "trunk":
            if "all" in switching.get("vlans", []):
                interface["switching"]["dot1q_mode"] = "tagged-all"
            else:
                interface["switching"]["dot1q_mode"] = "tagged"
        elif switching.get("dot1q_mode") == "access":
            interface["switching"]["dot1q_mode"] = "access"

        interface.setdefault("enabled", True)
        interface.setdefault("description", "")

    return data
