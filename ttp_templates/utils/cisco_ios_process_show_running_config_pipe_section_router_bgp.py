"""Normalize Cisco IOS BGP AS configuration output.

Used by:
- ttp_templates/platform/cisco_ios_show_running_config_pipe_section_router_bgp.txt
"""

from typing import Any, Dict, List

from .models import BgpAsnRecord


def _as_list(value: Any) -> List[Any]:
    """Return a TTP value as a list."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _scope_records(scope: Any) -> List[Dict[str, Any]]:
    """Return parsed ASN records for one global or VRF BGP scope."""
    if not isinstance(scope, dict):
        return []

    statements = _as_list(scope.get("statements"))
    peer_groups = {
        item.get("peer_group")
        for item in statements
        if isinstance(item, dict) and item.get("kind") == "peer_group"
    }
    memberships = {
        item.get("neighbor"): item.get("peer_group")
        for item in statements
        if isinstance(item, dict) and item.get("kind") == "membership"
    }

    records: List[Dict[str, Any]] = []
    for statement in statements:
        if not isinstance(statement, dict) or statement.get("kind") != "asn":
            continue

        neighbor = statement.get("neighbor")
        description = None
        if neighbor in peer_groups:
            description = neighbor
        elif neighbor in memberships:
            description = memberships[neighbor]

        records.append(
            {
                "asn": statement.get("asn"),
                "description": description,
            }
        )

    return records


def transform_bgp_asns(payload: Any) -> List[Dict[str, Any]]:
    """Return unique ASNs in configuration order, keeping the first description."""
    items = [payload] if isinstance(payload, dict) else payload or []
    candidates: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("bgp"), dict):
            continue

        bgp = item["bgp"]
        candidates.append({"asn": bgp.get("router_asn"), "description": None})
        candidates.extend(_scope_records(bgp))
        for vrf in _as_list(bgp.get("vrfs")):
            candidates.extend(_scope_records(vrf))

    records: List[Dict[str, Any]] = []
    seen_asns = set()
    for candidate in candidates:
        asn = candidate.get("asn")
        if asn is None or asn in seen_asns:
            continue

        records.append(BgpAsnRecord(**candidate).model_dump())
        seen_asns.add(asn)

    return records
