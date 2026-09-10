"""
Normalize Juniper Junos VLAN configuration parsed by TTP.

Transforms Junos VLAN and VLAN-related interface configuration into a flat
list of VLAN dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt
"""

from typing import Any, Dict, List

from .models import VlanRecord


def transform_vlans_config(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert parsed Juniper VLAN configuration into normalized VLAN records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of normalized VLAN dictionaries including interface membership.
    """
    if not payload:
        return []

    records: Dict[int, Dict[str, Any]] = {}
    vlan_names: Dict[str, int] = {}
    memberships = []
    l3_memberships = []

    for name, vlan in payload.get("vlans", {}).items():
        vid = int(vlan["vid"])
        records[vid] = {
            "vid": vid,
            "name": name,
            "description": vlan.get("description") or None,
            "tagged_interfaces": [],
            "untagged_interfaces": [],
        }
        vlan_names[name] = vid

        if vlan.get("l3_interface"):
            l3_memberships.append((vid, "untagged_interfaces", vlan["l3_interface"]))

    for name, interface in payload.get("interfaces", {}).items():
        untagged_value = interface.get("untagged_vlan")
        if name.lower().startswith("irb.") and name[4:].isdigit():
            untagged_value = int(name[4:])

        tagged_values = []
        dot1q = interface.get("dot1q")
        if dot1q is not None:
            tagged_values.append(dot1q)

        switching = interface.get("switching")
        if switching:
            vlan_members = [
                member["vlan"] for member in switching.get("vlans", [])
            ]
            if switching.get("dot1q_mode") == "access":
                if vlan_members:
                    untagged_value = vlan_members[0]
            elif switching.get("dot1q_mode") == "trunk":
                tagged_values.extend(vlan_members)

        if untagged_value is not None:
            try:
                untagged_vid = int(untagged_value)
            except (TypeError, ValueError):
                untagged_vid = vlan_names.get(str(untagged_value).strip('"'))
            if untagged_vid is not None:
                memberships.append((untagged_vid, "untagged_interfaces", name))

        for value in tagged_values:
            try:
                vid = int(value)
            except (TypeError, ValueError):
                vid = vlan_names.get(str(value).strip('"'))
            if vid is not None:
                memberships.append((vid, "tagged_interfaces", name))

    memberships.extend(l3_memberships)

    for vid, membership_type, name in memberships:
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
        if name not in record[membership_type]:
            record[membership_type].append(name)

    return [VlanRecord(**record).model_dump() for record in records.values()]
