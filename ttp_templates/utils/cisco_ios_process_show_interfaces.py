"""Normalize Cisco IOS ``show interfaces`` output.

Used by:
- ttp_templates/platform/cisco_ios_show_interfaces.txt
"""

from typing import Any

from .models import InterfaceStatusRecord


def transform_interfaces_status(payload: list) -> list[dict[str, Any]]:
    """Return normalized operational interface records."""
    items = [payload] if isinstance(payload, dict) else payload
    records: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict) or not item.get("name"):
            continue

        rate_interval = item.get("rate_interval_in")
        rate_interval_unit = item.get("rate_interval_unit_in", "")
        if rate_interval is None:
            rate_interval = item.get("rate_interval_out")
            rate_interval_unit = item.get("rate_interval_unit_out", "")
        if rate_interval is not None and rate_interval_unit.lower().startswith(
            "minute"
        ):
            rate_interval *= 60

        interface_status = item.get("interface_status", "").lower()
        protocol_status = item.get("protocol_status", "").lower()
        record = {
            "name": item["name"],
            "description": item.get("description") or None,
            "mtu": item.get("mtu"),
            "mac_address": item.get("mac_address"),
            "duplex": str(item.get("duplex") or "").strip().lower() or None,
            "status_admin": "down"
            if interface_status == "administratively down"
            else "up",
            "status_oper": "up" if protocol_status.startswith("up") else "down",
            "speed_bps": item["speed_kbps"] * 1_000
            if item.get("speed_kbps") is not None
            else None,
            "last_cleared": item.get("last_cleared"),
            "transitions": None,
            "errors_in": item.get("errors_in"),
            "errors_out": item.get("errors_out"),
            "crc_errors": item.get("crc_errors"),
            "packets_in": item.get("packets_in"),
            "packets_out": item.get("packets_out"),
            "rate_bps_in": item.get("rate_bps_in"),
            "rate_bps_out": item.get("rate_bps_out"),
            "rate_pps_in": item.get("rate_pps_in"),
            "rate_pps_out": item.get("rate_pps_out"),
            "rate_interval": rate_interval,
        }
        records.append(InterfaceStatusRecord(**record).model_dump())

    return records
