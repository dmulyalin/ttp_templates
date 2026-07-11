"""
Validate Cisco IOS-XR inventory records parsed by TTP.

The IOS-XR template parses text output directly into normalized field names.
This module only validates that every parsed row matches the getter record
model.

Used by:
- ttp_templates/platform/cisco_xr_show_inventory.txt
"""

from typing import Dict, List

from .models import InventoryRecord


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Validate IOS-XR inventory records.

    Args:
        payload: TTP records parsed from ``show inventory`` text output.

    Returns:
        List of validated inventory dictionaries.
    """
    records: List[Dict[str, str]] = []

    for item in payload:
        if not isinstance(item, dict):
            continue
        records.append(InventoryRecord(**item).model_dump())

    return records
