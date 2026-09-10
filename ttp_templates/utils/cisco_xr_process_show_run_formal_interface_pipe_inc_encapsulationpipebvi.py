"""Normalize IOS-XR formal interface encapsulation into VLAN records.

Used by:
- ttp_templates/platform/cisco_xr_show_run_formal_interface_pipe_inc_encapsulationpipebvi.txt
"""

from typing import Any, Dict, List

from .models import VlanRecord


def transform_vlans_config(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return VLAN records derived from parsed interface encapsulations."""
    if not payload:
        return []

    records: Dict[int, Dict[str, Any]] = {}

    for name, interface in payload.get("interfaces", {}).items():
        mode = interface.get("mode") or "tagged"
        vid = interface.get("vlan")

        if vid is None:
            continue

        vid = int(vid)
        record = records.setdefault(
            vid,
            {
                "vid": vid,
                "name": f"VLAN{vid}",
                "description": None,
                "tagged_interfaces": [],
                "untagged_interfaces": [],
            },
        )

        if mode == "access":
            if name not in record["untagged_interfaces"]:
                record["untagged_interfaces"].append(name)
        elif mode == "tagged":
            if name not in record["tagged_interfaces"]:
                record["tagged_interfaces"].append(name)

    for interface in payload.get("bvi_interfaces", []):
        vid = interface["vid"]
        record = records.setdefault(
            vid,
            {
                "vid": vid,
                "name": f"VLAN{vid}",
                "description": None,
                "tagged_interfaces": [],
                "untagged_interfaces": [],
            },
        )
        name = f"BVI{vid}"
        if name not in record["untagged_interfaces"]:
            record["untagged_interfaces"].append(name)

    return [VlanRecord(**record).model_dump() for record in records.values()]
