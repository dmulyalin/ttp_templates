"""Normalize Arista EOS VRRP interface configuration output.

Used by:
- ttp_templates/platform/arista_eos_show_running_config_section_vrrp.txt
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

        for interface, address_families in item.get("interfaces", {}).items():
            for groups in address_families.values():
                for group, values in groups.items():
                    if not values.get("virtual_address"):
                        continue
                    record = {
                        "interface": interface,
                        "group": int(group),
                        "virtual_address": values["virtual_address"],
                        "priority": values.get("priority", 100),
                        "authentication_type": values.get(
                            "authentication_type"
                        ),
                    }
                    records.append(VrrpRecord(**record).model_dump())

    return records
