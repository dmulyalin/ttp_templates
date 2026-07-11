"""
Post-process Cisco IOS LLDP data into OpenConfig LLDP shape.

Used by:
- ttp_templates/yang/openconfig-lldp_cisco_ios.txt
"""

from typing import Any, Dict, List


def process(data: list) -> List[Dict[str, Any]]:
    """
    Convert parsed LLDP neighbors into the OpenConfig LLDP structure.

    TTP first builds a dictionary keyed by interface name. OpenConfig expects a
    list of interface entries, and each neighbor needs an ``id`` plus a nested
    ``state`` dictionary.
    """
    ret = []

    for res_item in data:
        ret_template = {
            "opencondig-lldp": {
                "lldp": {
                    "interfaces": {"interface": []},
                    "config": {
                        "system-name": res_item.get("system_name", {}).get("hostname")
                    },
                }
            }
        }
        interfaces = res_item.get("lldp", {}).get("interfaces", {}).get("inderface", {})
        for interface_name, interface_data in interfaces.items():
            neighbors = interface_data["neighbors"]["neighbor"]
            interface_data["neighbors"]["neighbor"] = []

            for neighbor_id, neighbor in enumerate(neighbors, 1):
                interface_data["neighbors"]["neighbor"].append(
                    {"id": neighbor_id, "state": {"id": neighbor_id, **neighbor}}
                )

            ret_template["opencondig-lldp"]["lldp"]["interfaces"][
                "interface"
            ].append({"name": interface_name, **interface_data})

        ret.append(ret_template)

    return ret
