"""
Normalize Cisco IOS-XR VRF configuration parsed by TTP.

Transforms ``show running-config vrf`` output into a flat list of VRF
dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/cisco_xr_show_running_config_vrf.txt
"""

from typing import Any, Dict, List

from .models import VrfRecord


def _as_list(value: Any) -> List[str]:
    """Return a deduplicated list of non-empty strings while preserving order."""
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    result: List[str] = []
    for item in values:
        if isinstance(item, dict):
            item = item.get("rt")
        item = str(item).strip().strip('"')
        if item and item not in result:
            result.append(item)
    return result


def _collect_values(vrf: Dict[str, Any], key: str) -> List[str]:
    """Collect values from VRF root and address-family sections."""
    values = _as_list(vrf.get(key))
    address_families = vrf.get("address_families")
    if isinstance(address_families, dict):
        for afi in address_families.values():
            if isinstance(afi, dict):
                values.extend(v for v in _as_list(afi.get(key)) if v not in values)
    return values


def _first_value(vrf: Dict[str, Any], key: str) -> Any:
    """Return the first value captured at VRF root or address-family level."""
    values = _collect_values(vrf, key)
    return values[0] if values else None


def transform_vrfs_config(payload: list) -> List[Dict[str, Any]]:
    """
    Convert parsed Cisco IOS-XR VRF configuration into normalized VRF records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of dictionaries with normalized VRF keys.
    """
    if not payload:
        return []

    items = [payload] if isinstance(payload, dict) else payload
    vrfs: Dict[str, Dict[str, Any]] = {}

    for item in items:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("vrfs"), dict):
            vrfs.update(item["vrfs"])

    records: List[Dict[str, Any]] = []
    for name, vrf in vrfs.items():
        if not isinstance(vrf, dict):
            vrf = {}
        record = {
            "name": name,
            "description": vrf.get("description") or None,
            "rd": vrf.get("rd") or None,
            "rt_import": _collect_values(vrf, "rt_import"),
            "rt_export": _collect_values(vrf, "rt_export"),
            "route_policy_import": _first_value(vrf, "route_policy_import"),
            "route_policy_export": _first_value(vrf, "route_policy_export"),
        }
        for route_target in _collect_values(vrf, "rt_both"):
            if route_target not in record["rt_import"]:
                record["rt_import"].append(route_target)
            if route_target not in record["rt_export"]:
                record["rt_export"].append(route_target)
        records.append(VrfRecord(**record).model_dump())

    return records
