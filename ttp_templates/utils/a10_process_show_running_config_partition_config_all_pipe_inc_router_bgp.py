"""Normalize A10 BGP AS configuration output.

Used by:
- ttp_templates/platform/a10_show_running_config_partition_config_all_pipe_inc_router_bgp.txt
"""

from typing import Any, Dict, List

from .models import BgpAsnRecord


def transform_bgp_asns(payload: Any) -> List[Dict[str, Any]]:
    """Return unique ASNs in configuration order, keeping the first description."""
    items = [payload] if isinstance(payload, dict) else payload or []
    candidates: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        statements = item.get("statements", [])
        statements = [statements] if isinstance(statements, dict) else statements
        for statement in statements:
            if not isinstance(statement, dict) or "asn" not in statement:
                continue
            candidates.append(
                {
                    "asn": statement.get("asn"),
                    "description": statement.get("description"),
                    "local_asn": statement.get("local_asn", False),
                }
            )

    records: List[Dict[str, Any]] = []
    seen_asns: Dict[int, Dict[str, Any]] = {}
    for candidate in candidates:
        asn = candidate.get("asn")
        if asn is None:
            continue
        if asn in seen_asns:
            seen_asns[asn]["local_asn"] = (
                seen_asns[asn]["local_asn"] or candidate.get("local_asn", False)
            )
            continue

        record = BgpAsnRecord(**candidate).model_dump()
        records.append(record)
        seen_asns[asn] = record

    return records
