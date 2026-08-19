"""
Normalize Juniper Junos routing-instance configuration parsed by TTP.

Transforms ``show configuration routing-instances | display set`` output into
a flat list of VRF dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_routing_instances_pipe_display_set.txt
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
        if item.startswith("target:"):
            item = item[len("target:") :]
        if item and item not in result:
            result.append(item)
    return result


def transform_vrfs_config(payload: list) -> List[Dict[str, Any]]:
    """
    Convert parsed Juniper Junos routing-instances into normalized VRF records.

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
            "description": (vrf.get("description") or "").strip('"') or None,
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
