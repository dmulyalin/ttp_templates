"""
Normalize Arista EOS inventory JSON output.

The TTP template captures the body of ``show inventory | json`` as one string.
This module loads that JSON, walks known inventory sections, and returns the
common inventory record shape used by the getter.

Used by:
- ttp_templates/platform/arista_eos_show_inventory_pipe_json.txt
"""

import json
from typing import Any, Dict, List

from .models import InventoryRecord


def _validate_record(record: Dict[str, str]) -> Dict[str, str]:
    """Use Pydantic to make sure each record has the expected keys and types."""
    return InventoryRecord(**record).model_dump()


def _load_json(payload: list) -> Dict[str, Any]:
    """Load the JSON object captured by TTP."""
    if not payload:
        return {}
    return json.loads("{" + payload[0]["data"] + "}")


def transform_inventory(payload: list) -> List[Dict[str, str]]:
    """
    Convert Arista inventory JSON into normalized inventory records.

    Args:
        payload: TTP match data with captured JSON text.

    Returns:
        List of dictionaries with description, module, serial, and slot keys.
    """
    data = _load_json(payload)
    records: List[Dict[str, str]] = []

    def add_item(item: Any, slot: str) -> None:
        # Arista stores chassis and module details in slightly different
        # sections, but the useful fields have the same names.
        if not isinstance(item, dict):
            return

        serial = str(item.get("serialNum", "")).strip()
        if not serial or serial.upper() == "N/A":
            return

        records.append(
            _validate_record(
                {
                    "module": str(
                        item.get("name") or item.get("modelName") or ""
                    ).strip(),
                    "serial": serial,
                    "slot": slot,
                    "description": str(item.get("description", "")).strip(),
                }
            )
        )

    add_item(data.get("systemInformation", {}), "chassis")

    for top_key, top_value in data.items():
        if not top_key.endswith("Slots") or not isinstance(top_value, dict):
            continue

        slot_prefix = top_key[: -len("Slots")].lower()
        for key, item in top_value.items():
            add_item(item, f"{slot_prefix}-{key}")

    return records
