"""Normalize Cisco IOS-XR formal VRRP configuration output.

Used by:
- ttp_templates/platform/cisco_xr_show_running_config_formal_router_vrrp.txt
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

        for interface, address_families in item.get("vrrp", {}).items():
            for address_family, groups in address_families.items():
                for group, values in groups.items():
                    record = {
                        "interface": interface,
                        "group": int(group),
                        "protocol": (
                            "vrrpv3"
                            if address_family == "ipv6"
                            else f"vrrpv{values.get('version', 2)}"
                        ),
                        "virtual_address": values.get("virtual_address", ""),
                        "priority": values.get("priority", 100),
                        "authentication_type": values.get(
                            "authentication_type"
                        ),
                    }
                    records.append(VrrpRecord(**record).model_dump())

    return records
