"""
Normalize Juniper Junos chassis hardware JSON output.

The command returns a nested tree where inventory items can appear at many
levels. This module walks that tree and extracts nodes that have a serial
number.
"""

import json
from typing import Any, Dict, List, Optional

from .models import InventoryRecord


def _load_json(payload: list) -> Dict[str, Any]:
    """Load the JSON object captured by TTP."""
    if not payload:
        return {}
    return json.loads("{" + payload[0]["data"] + "}")


def _pick(node: Dict[str, Any], key: str) -> Optional[str]:
    """Return Junos JSON text stored under a key's first ``data`` field."""
    value = node.get(key)
    if not isinstance(value, list):
        return None

    for item in value:
        if isinstance(item, dict):
            data = item.get("data")
            if isinstance(data, str) and data.strip():
                return data.strip()

    return None


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Convert Junos chassis hardware JSON into normalized inventory records.

    Args:
        payload: TTP match data with captured JSON text.

    Returns:
        List of dictionaries with description, module, serial, and slot keys.
    """
    data = _load_json(payload)
    records: List[Dict[str, str]] = []
    stack = [data]

    while stack:
        node = stack.pop()

        if isinstance(node, list):
            stack.extend(node)
            continue
        if not isinstance(node, dict):
            continue

        serial = _pick(node, "serial-number")
        if serial:
            description = _pick(node, "description") or ""
            record = {
                "module": description or (_pick(node, "part-number") or ""),
                "serial": serial,
                "slot": _pick(node, "name") or "",
                "description": description,
            }
            records.append(InventoryRecord(**record).model_dump())

        stack.extend(node.values())

    return records
