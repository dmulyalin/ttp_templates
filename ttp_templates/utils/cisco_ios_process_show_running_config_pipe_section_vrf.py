"""
Normalize Cisco IOS VRF configuration parsed by TTP.

Transforms ``show running-config | section vrf`` output into a flat list of
VRF dictionaries suitable for getter-style consumption.

Used by:
- ttp_templates/platform/cisco_ios_show_running_config_pipe_section_vrf.txt
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
        item = str(item).strip()
        if item and item not in result:
            result.append(item)
    return result


def transform_vrfs_config(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert parsed Cisco IOS VRF configuration into normalized VRF records.

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
        address_families = {
            "ipv4": {
                "rt_import": _as_list(vrf.get("rt_import")),
                "rt_export": _as_list(vrf.get("rt_export")),
                "route_policy_import": vrf.get("route_policy_import") or None,
                "route_policy_export": vrf.get("route_policy_export") or None,
            },
            "ipv6": {
                "rt_import": [],
                "rt_export": [],
                "route_policy_import": None,
                "route_policy_export": None,
            },
        }

        for route_target in _as_list(vrf.get("rt_both")):
            for key in ["rt_import", "rt_export"]:
                if route_target not in address_families["ipv4"][key]:
                    address_families["ipv4"][key].append(route_target)

        for afi_name, afi in vrf.get("address_families", {}).items():
            if afi_name.lower().startswith("ipv4"):
                family = address_families["ipv4"]
            elif afi_name.lower().startswith("ipv6"):
                family = address_families["ipv6"]
            else:
                continue

            for key in ["rt_import", "rt_export"]:
                for route_target in _as_list(afi.get(key)):
                    if route_target not in family[key]:
                        family[key].append(route_target)
            for route_target in _as_list(afi.get("rt_both")):
                for key in ["rt_import", "rt_export"]:
                    if route_target not in family[key]:
                        family[key].append(route_target)
            for key in ["route_policy_import", "route_policy_export"]:
                if afi.get(key):
                    family[key] = afi[key]

        record = {
            "name": name,
            "instance_type": "vrf",
            "description": vrf.get("description") or None,
            "rd": vrf.get("rd") or None,
            "interfaces": vrf_interfaces.get(name, []),
            "address_families": address_families,
        }
        records.append(VrfRecord(**record).model_dump())

    return records
