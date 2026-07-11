"""
Helpers for the N2G Juniper Junos L2 data template.

Used by:
- ttp_templates/misc/N2G/cli_l2_data/juniper_junos.txt
"""

from typing import Callable


def extract_lldp_peer(data: dict, resuball: Callable) -> dict:
    """Split Junos compact LLDP peer info into graph source and target fields."""
    if " " in data["info"]:
        *port_info, peer_name = data.pop("info").split(" ")
        data["data.peer_port_description"] = " ".join(port_info).strip()
    else:
        port_info, peer_name = data.pop("info"), data["data.chassis_id"]
        data["data.peer_port_description"] = port_info

    data["target.id"] = peer_name
    data["trgt_label"] = ""

    if len(port_info) == 1 and not port_info[0].isdigit():
        data["trgt_label"], _ = resuball(port_info[0], "IfsNormalize")

    return data
