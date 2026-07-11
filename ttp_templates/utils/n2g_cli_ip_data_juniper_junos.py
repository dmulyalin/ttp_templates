"""
Post-process N2G Juniper Junos IP data.

Used by:
- ttp_templates/misc/N2G/cli_ip_data/juniper_junos.txt
"""

from typing import Any, Dict


def postprocess(data: Dict[str, Any]) -> Dict[str, Any]:
    """Turn VRF dictionaries into lists and copy VRF names onto interfaces."""
    for hostname in data.keys():
        data[hostname]["vrf"] = [
            {"name": k, **v} for k, v in data[hostname].get("vrf", {}).items()
        ]

        for vrf in data[hostname]["vrf"]:
            for interface in vrf.get("interfaces", []):
                if data[hostname]["interfaces"].get(interface):
                    data[hostname]["interfaces"][interface]["vrf"] = vrf["name"]

        data[hostname].pop("vrf")

    return data
