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

    for key in [
        "rt_import",
        "rt_export",
        "rt_both",
        "rt_import_ipv4",
        "rt_export_ipv4",
        "rt_both_ipv4",
    ]:
        target.setdefault(key, [])
        for value in _as_list(source.get(key)):
            if value not in target[key]:
                target[key].append(value)


def transform_vrfs_config(payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
    vrf_interfaces: Dict[str, List[str]] = {}

    for item in payload:
        for name, vrf in item.get("vrfs", {}).items():
            _merge_vrf(vrfs.setdefault(name, {}), vrf)
        for interface in item.get("interfaces", []):
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

        for key in ["rt_import", "rt_export"]:
            for route_target in _as_list(vrf.get(f"{key}_ipv4")):
                if route_target not in address_families["ipv4"][key]:
                    address_families["ipv4"][key].append(route_target)
        for route_target in _as_list(vrf.get("rt_both")) + _as_list(
            vrf.get("rt_both_ipv4")
        ):
            for key in ["rt_import", "rt_export"]:
                if route_target not in address_families["ipv4"][key]:
                    address_families["ipv4"][key].append(route_target)

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
