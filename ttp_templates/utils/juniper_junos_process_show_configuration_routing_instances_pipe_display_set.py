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


def transform_vrfs_config(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert parsed Juniper Junos routing-instances into normalized VRF records.

    Args:
        payload: TTP macro payload.

    Returns:
        List of dictionaries with normalized VRF keys.
    """
    if not payload:
        return []

    vrfs = payload.get("vrfs", {})
    vrf_interfaces: Dict[str, List[str]] = {}

    for interface in payload.get("interfaces", []):
        interfaces = vrf_interfaces.setdefault(interface["vrf"], [])
        if interface["name"] not in interfaces:
            interfaces.append(interface["name"])

    records: List[Dict[str, Any]] = []
    for name, vrf in vrfs.items():
        rt_import = _as_list(vrf.get("rt_import"))
        rt_export = _as_list(vrf.get("rt_export"))
        for route_target in _as_list(vrf.get("rt_both")):
            if route_target not in rt_import:
                rt_import.append(route_target)
            if route_target not in rt_export:
                rt_export.append(route_target)

        address_families = {}
        for afi in ["ipv4", "ipv6"]:
            address_families[afi] = {
                "rt_import": rt_import.copy(),
                "rt_export": rt_export.copy(),
                "route_policy_import": vrf.get("route_policy_import") or None,
                "route_policy_export": vrf.get("route_policy_export") or None,
            }

        record = {
            "name": name,
            "instance_type": vrf.get("instance_type") or "vrf",
            "description": (vrf.get("description") or "").strip('"') or None,
            "rd": vrf.get("rd") or None,
            "interfaces": vrf_interfaces.get(name, []),
            "address_families": address_families,
        }
        records.append(VrfRecord(**record).model_dump())

    return records
