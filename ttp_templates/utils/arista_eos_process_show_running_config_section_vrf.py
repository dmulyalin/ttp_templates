"""
Normalize Arista EOS VRF configuration parsed by TTP.

Transforms ``show running-config section vrf`` output into a flat list of VRF
dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/arista_eos_show_running_config_section_vrf.txt
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
        item = str(item).strip().strip('"')
        if item and item not in result:
            result.append(item)
    return result


def _merge_vrf(target: Dict[str, Any], source: Dict[str, Any]) -> None:
    """Merge one parsed VRF fragment into a normalized intermediate dict."""
    for key in ["description", "rd", "route_policy_import", "route_policy_export"]:
        if source.get(key) and not target.get(key):
            target[key] = source[key]

    for key in ["rt_import", "rt_export", "rt_both"]:
        target.setdefault(key, [])
        for value in _as_list(source.get(key)):
            if value not in target[key]:
                target[key].append(value)


def _walk_items(value: Any) -> List[Dict[str, Any]]:
    """Flatten nested TTP payload fragments into dictionaries."""
    if isinstance(value, dict):
        items = [value]
        for child in value.values():
            if isinstance(child, (dict, list)):
                items.extend(_walk_items(child))
        return items
    if isinstance(value, list):
        items: List[Dict[str, Any]] = []
        for child in value:
            items.extend(_walk_items(child))
        return items
    return []


def transform_vrfs_config(payload: list) -> List[Dict[str, Any]]:
    """
    Convert parsed Arista EOS VRF configuration into normalized VRF records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of dictionaries with normalized VRF keys.
    """
    if not payload:
        return []

    vrfs: Dict[str, Dict[str, Any]] = {}

    for item in _walk_items(payload):
        parsed_vrfs = item.get("vrfs")
        if not isinstance(parsed_vrfs, dict):
            continue
        for name, vrf in parsed_vrfs.items():
            if not isinstance(vrf, dict):
                continue
            _merge_vrf(vrfs.setdefault(name, {}), vrf)

    records: List[Dict[str, Any]] = []
    for name, vrf in vrfs.items():
        record = {
            "name": name,
            "description": vrf.get("description") or None,
            "rd": vrf.get("rd") or None,
            "rt_import": _as_list(vrf.get("rt_import")),
            "rt_export": _as_list(vrf.get("rt_export")),
            "route_policy_import": vrf.get("route_policy_import") or None,
            "route_policy_export": vrf.get("route_policy_export") or None,
        }
        for route_target in _as_list(vrf.get("rt_both")):
            if route_target not in record["rt_import"]:
                record["rt_import"].append(route_target)
            if route_target not in record["rt_export"]:
                record["rt_export"].append(route_target)
        records.append(VrfRecord(**record).model_dump())

    return records
