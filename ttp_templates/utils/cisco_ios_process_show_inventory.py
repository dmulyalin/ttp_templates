"""
Validate Cisco IOS inventory records parsed by TTP.

The Cisco IOS template parses text output directly into normalized inventory
getter field names. This module validates parsed rows against the shared
inventory record model.

Used by:
- ttp_templates/platform/cisco_ios_show_inventory.txt
"""

from typing import Dict, List

from .models import InventoryRecord


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Validate Cisco IOS inventory records.

    Args:
        payload: TTP records parsed from ``show inventory`` text output.

    Returns:
        List of validated inventory dictionaries.
    """
    records: List[Dict[str, str]] = []

    for item in payload:
        if not isinstance(item, dict):
            continue
        if not all(item.get(key) for key in ("description", "serial", "slot")):
            continue
        item.setdefault("module", "")
        records.append(InventoryRecord(**item).model_dump())

    return records
