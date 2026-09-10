"""
Normalize Cisco NX-OS VLAN configuration parsed by TTP.

Transforms NX-OS VLAN and interface configuration into a flat list of VLAN
dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/cisco_nxos_show_running_config_vlan.txt
"""

from typing import Any, Dict, List

from .models import VlanRecord


def _expand_vlan_ids(value: Any) -> List[int]:
    """Expand VLAN strings such as ``10,20-22`` into integer IDs."""
    vlans: List[int] = []
    for part in str(value).split(","):
        if "-" in part:
            start, end = part.split("-", 1)
            vlans.extend(range(int(start), int(end) + 1))
        else:
            vlans.append(int(part))
    return vlans


def transform_vlans_config(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert parsed Cisco NX-OS VLAN stanzas into normalized VLAN records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of normalized VLAN dictionaries including interface membership.
    """
    if not payload:
        return []

    records: Dict[int, Dict[str, Any]] = {}
    for vlan in payload.get("vlans", []):
        for vid in _expand_vlan_ids(vlan.get("vid")):
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
            if vlan.get("name"):
                record["name"] = vlan["name"]
            if vlan.get("description"):
                record["description"] = vlan["description"]

    records = dict(sorted(records.items()))

    for interface in payload.get("interfaces", []):
        name = interface["name"]
        memberships = []
        untagged_vid = interface.get("untagged_vlan")
        name_lower = name.lower()
        if name_lower.startswith("vlan") and name_lower[4:].isdigit():
            untagged_vid = int(name_lower[4:])

        if untagged_vid is not None:
            memberships.append((int(untagged_vid), "untagged_interfaces"))

        tagged_values = interface.get("tagged_vlans") or []
        if not isinstance(tagged_values, list):
            tagged_values = [tagged_values]
        for value in tagged_values:
            memberships.append((int(value), "tagged_interfaces"))

        for vid, membership_type in memberships:
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
