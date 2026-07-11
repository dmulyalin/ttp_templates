"""
Normalize Cisco NX-OS pretty inventory JSON output.

NX-OS returns inventory rows under ``TABLE_inv.ROW_inv`` for
``show inventory | json-pretty``. This module converts those rows into the
getter's common inventory record shape.
"""

import json
from typing import Any, Dict, List

from .models import InventoryRecord


def _clean(value: Any) -> str:
    """Convert NX-OS inventory values to clean strings."""
    if value is None:
        return ""
    return str(value).replace('"', "").strip()


def _load_json(payload: list) -> Dict[str, Any]:
    """Load the JSON object captured by TTP."""
    if not payload:
        return {}
    return json.loads("{" + payload[0]["data"] + "}")


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Convert NX-OS pretty inventory JSON into normalized inventory records.

    Args:
        payload: TTP match data with captured JSON text.

    Returns:
        List of dictionaries with description, module, serial, and slot keys.
    """
    data = _load_json(payload)
    rows = data.get("TABLE_inv", {}).get("ROW_inv", [])
    if isinstance(rows, dict):
        rows = [rows]

    records: List[Dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue

        serial = _clean(row.get("serialnum"))
        if not serial or serial.upper() == "N/A":
            continue

        record = {
            "module": _clean(row.get("productid")),
            "serial": serial,
            "slot": _clean(row.get("name")),
            "description": _clean(row.get("desc")),
        }
        records.append(InventoryRecord(**record).model_dump())

    return records
