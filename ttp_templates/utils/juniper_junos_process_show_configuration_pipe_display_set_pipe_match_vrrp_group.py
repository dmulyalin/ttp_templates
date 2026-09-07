"""Normalize Juniper Junos VRRP configuration output.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_vrrp_group.txt
"""

from typing import Any, Dict, List

from .models import VrrpRecord


def transform_vrrp_config(payload: Any) -> List[Dict[str, Any]]:
    """Flatten parsed VRRP data into normalized records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        for interface, units in item.get("vrrp", {}).items():
            for unit, addresses in units.items():
                for groups in addresses.values():
                    for group, values in groups.items():
                        record = {
                            "interface": f"{interface}.{unit}",
                            "group": int(group),
                            "virtual_address": values.get("virtual_address", ""),
                            "priority": values.get("priority", 100),
                            "authentication_type": values.get(
                                "authentication_type"
                            ),
                        }
                        records.append(VrrpRecord(**record).model_dump())

    return records
