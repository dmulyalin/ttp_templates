"""
Normalize Juniper Junos VLAN configuration parsed by TTP.

Transforms ``show configuration vlans | display set`` lines into a flat list
of VLAN dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt
"""

from typing import Any, Dict, List

from .models import VlanRecord


def transform_vlans_config(payload: list) -> List[Dict[str, Any]]:
    """
    Convert parsed Juniper VLAN configuration into normalized VLAN records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of dictionaries with vid, name, and description keys.
    """
    if not payload:
        return []

    items = [payload] if isinstance(payload, dict) else payload
    vlans: Dict[str, Dict[str, Any]] = {}

    for item in items:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("vlans"), dict):
            vlans.update(item["vlans"])

    records: List[Dict[str, Any]] = []
    for name, vlan in vlans.items():
        if not isinstance(vlan, dict) or vlan.get("vid") is None:
            continue
        record = {
            "vid": vlan["vid"],
            "name": name,
            "description": vlan.get("description") or None,
        }
        records.append(VlanRecord(**record).model_dump())

    return records
