"""Normalize Cisco IOS-XR formal BGP AS configuration output.

Used by:
- ttp_templates/platform/cisco_xr_show_run_formal_pipe_inc_local_aspipe_remote_as.txt
"""

from typing import Any, Dict, List

from .models import BgpAsnRecord


def transform_bgp_asns(payload: Any) -> List[Dict[str, Any]]:
    """Return unique ASNs in configuration order, keeping the first description."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, Any]] = []
    seen_asns = set()

    for item in items:
        if not isinstance(item, dict):
            continue

        statements = item.get("statements", [])
        statements = [statements] if isinstance(statements, dict) else statements

        for statement in statements:
            if not isinstance(statement, dict):
                continue

            for key in ("router_asn", "peer_asn"):
                asn = statement.get(key)
                if asn is None or asn in seen_asns:
                    continue

                description = (
                    statement.get("description") if key == "peer_asn" else None
                )
                record = BgpAsnRecord(
                    asn=asn,
                    description=description or None,
                ).model_dump()
                records.append(record)
                seen_asns.add(asn)

    return records
