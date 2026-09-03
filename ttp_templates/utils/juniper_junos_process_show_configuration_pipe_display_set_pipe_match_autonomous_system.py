"""Normalize Juniper Junos BGP AS configuration output.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_autonomous_system.txt
"""

from typing import Any, Dict, List

from .models import BgpAsnRecord


def transform_bgp_asns(payload: Any) -> List[Dict[str, Any]]:
    """Return unique ASNs in configuration order, keeping the first description."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, Any]] = []
    seen_asns: Dict[int, Dict[str, Any]] = {}

    for item in items:
        if not isinstance(item, dict):
            continue

        statements = item.get("statements", [])
        statements = [statements] if isinstance(statements, dict) else statements

        for statement in statements:
            if not isinstance(statement, dict):
                continue

            asn = statement.get("asn")
            if asn is None:
                continue
            if asn in seen_asns:
                seen_asns[asn]["local_asn"] = (
                    seen_asns[asn]["local_asn"] or statement.get("local_asn", False)
                )
                continue

            record = BgpAsnRecord(
                asn=asn,
                description=statement.get("description") or None,
                local_asn=statement.get("local_asn", False),
            ).model_dump()
            records.append(record)
            seen_asns[asn] = record

    return records
