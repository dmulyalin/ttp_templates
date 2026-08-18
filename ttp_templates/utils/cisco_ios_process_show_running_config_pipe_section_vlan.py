"""
Normalize Cisco IOS VLAN configuration parsed by TTP.

Transforms ``show running-config | section vlan`` output into a flat list of
VLAN dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/cisco_ios_show_running_config_pipe_section_vlan.txt
"""

from typing import Any, Dict, List

from .models import VlanRecord


def _expand_vlan_ids(value: Any) -> List[int]:
    """Expand VLAN strings such as ``2,100-105`` into integer IDs."""
    vlans: List[int] = []
    for part in str(value).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            vlans.extend(range(int(start), int(end) + 1))
        else:
            vlans.append(int(part))
    return vlans


def transform_vlans_config(payload: list) -> List[Dict[str, Any]]:
    """
    Convert parsed Cisco IOS VLAN stanzas into normalized VLAN records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of dictionaries with vid, name, and description keys.
    """
    if not payload:
        return []

    items = [payload] if isinstance(payload, dict) else payload
    vlans: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("vlans"), list):
            vlans.extend(v for v in item["vlans"] if isinstance(v, dict))
        elif item.get("vid") is not None:
            vlans.append(item)

    records: List[Dict[str, Any]] = []
    for vlan in vlans:
        for vid in _expand_vlan_ids(vlan.get("vid")):
            record = {
                "vid": vid,
                "name": vlan.get("name") or f"VLAN{vid}",
                "description": vlan.get("description") or None,
            }
            records.append(VlanRecord(**record).model_dump())

    return records
