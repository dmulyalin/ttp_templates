"""Normalize Cisco NX-OS VRRPv3 configuration output.

Used by:
- ttp_templates/platform/cisco_nxos_show_running_config_vrrpv3.txt
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

        for interface, interface_data in item.get("interfaces", {}).items():
            for groups in interface_data.get("vrrp", {}).values():
                for group, values in groups.items():
                    if not values.get("virtual_address"):
                        continue
                    record = {
                        "interface": interface,
                        "group": int(group),
                        "virtual_address": values["virtual_address"],
                        "priority": values.get("priority", 100),
                        "authentication_type": None,
                    }
                    records.append(VrrpRecord(**record).model_dump())

    return records
