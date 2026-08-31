"""
Normalize Cisco NX-OS VLAN configuration parsed by TTP.

Transforms ``show running-config vlan`` output into a flat list of VLAN
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
    Convert parsed Cisco NX-OS VLAN stanzas into normalized VLAN records.

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

    records_by_vid: Dict[int, tuple[bool, Dict[str, Any]]] = {}
    for vlan in vlans:
        has_explicit_name = bool(vlan.get("name"))
        for vid in _expand_vlan_ids(vlan.get("vid")):
            record = {
                "vid": vid,
                "name": vlan.get("name") or f"VLAN{vid}",
                "description": vlan.get("description") or None,
            }
            existing = records_by_vid.get(vid)
            if existing and existing[0] and not has_explicit_name:
                continue

            records_by_vid[vid] = (
                has_explicit_name,
                VlanRecord(**record).model_dump(),
            )

    return [records_by_vid[vid][1] for vid in sorted(records_by_vid)]
