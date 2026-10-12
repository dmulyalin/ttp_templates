"""Normalize Cisco IOS ``show lldp neighbors detail`` output.

Used by:
- ttp_templates/platform/cisco_ios_show_lldp_neighbors_detail.txt
"""

from typing import Any

from .models import LldpNeighborRecord


def transform_lldp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Return validated LLDP records, preserving every advertised neighbor."""
    records = []
    items = [payload] if isinstance(payload, dict) else payload or []
    for item in items:
        neighbors = item.get("neighbors", [])
        if isinstance(neighbors, dict):
            neighbors = [neighbors]
        for neighbor in neighbors:
            if not neighbor.get("interface"):
                continue
            record = {
                "interface": neighbor["interface"].strip(),
                "remote_system_description": None,
            }
            for field in (
                "remote_device",
                "remote_interface",
                "remote_chassi_id",
                "remote_interface_description",
            ):
                value = (neighbor.get(field) or "").strip()
                record[field] = (
                    None if value.lower() in {"", "-", "not advertised"} else value
                )
            chassis = record["remote_chassi_id"]
            if chassis:
                compact = chassis.replace(".", "").replace(":", "").replace("-", "")
                if len(compact) == 12 and all(
                    c in "0123456789abcdefABCDEF" for c in compact
                ):
                    record["remote_chassi_id"] = ":".join(
                        compact[i : i + 2].lower() for i in range(0, 12, 2)
                    )
            record["remote_device_management_ip"] = None
            for management in neighbor.get("management_addresses", []):
                address = (management.get("address") or "").strip()
                if address.lower() not in {"", "-", "not advertised"}:
                    record["remote_device_management_ip"] = address
                    break
            records.append(LldpNeighborRecord(**record).model_dump())
    return records
