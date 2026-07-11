"""
Validate A10 hardware inventory records parsed by TTP.

The A10 template parses ``show hardware`` text output directly into the common
inventory getter field names. This module validates parsed rows against the
shared inventory record model.

Used by:
- ttp_templates/platform/a10_show_hardware.txt
"""

from typing import Any, Dict, List

from .models import InventoryRecord


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Validate A10 hardware inventory records.

    Args:
        payload: TTP records parsed from ``show hardware`` text output.

    Returns:
        List of validated inventory dictionaries.
    """
    records: List[Dict[str, str]] = []

    def collect_records(item: Any) -> None:
        if isinstance(item, list):
            for child in item:
                collect_records(child)
            return
        if not isinstance(item, dict) or not item:
            return
        records.append(InventoryRecord(**item).model_dump())

    collect_records(payload)
    return records
