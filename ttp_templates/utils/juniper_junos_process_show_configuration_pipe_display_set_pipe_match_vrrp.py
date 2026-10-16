"""Normalize Juniper Junos VRRP configuration output.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_vrrp.txt
"""

from typing import Any, Dict, List

from .models import VrrpRecord


def transform_vrrp_config(payload: Any) -> List[Dict[str, Any]]:
    """Flatten parsed VRRP data into normalized records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, Any]] = []

    iface_to_vrf = {}
    for item in items:
        vrf_data = item.get("vrf") if isinstance(item, dict) else None
        if not isinstance(vrf_data, dict):
            continue
        for vrf_name, vrf_info in vrf_data.items():
            for iface_name in vrf_info.get("interfaces") or []:
                iface_to_vrf[iface_name] = vrf_name

    for item in items:
        if not isinstance(item, dict):
            continue

        version_3 = item.get("settings", {}).get("version_3", False)
        for interface, units in item.get("vrrp", {}).items():
            for unit, address_families in units.items():
                for address_family, addresses in address_families.items():
                    for groups in addresses.values():
                        for group, values in groups.items():
                            record = {
                                "interface": f"{interface}.{unit}",
                                "vrf": iface_to_vrf.get(f"{interface}.{unit}"),
                                "group": int(group),
                                "protocol": (
                                    "vrrpv3"
                                    if version_3 or address_family == "ipv6"
                                    else "vrrpv2"
                                ),
                                "virtual_address": values.get(
                                    "virtual_address", ""
                                ),
                                "priority": values.get("priority", 100),
                                "authentication_type": values.get(
                                    "authentication_type"
                                ),
                            }
                            records.append(VrrpRecord(**record).model_dump())

    return records
