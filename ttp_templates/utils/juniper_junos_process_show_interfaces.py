"""Normalize Juniper Junos ``show interfaces`` output.

Used by:
- ttp_templates/platform/juniper_junos_show_interfaces.txt
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

        mtu_raw = item.get("mtu_raw", "")
        mtu = int(mtu_raw) if mtu_raw.isdigit() else None

        displayed_speed = item.get("displayed_speed", "").lower()
        speed_bps = None
        speed_units = {
            "gbps": 1_000_000_000,
            "mbps": 1_000_000,
            "kbps": 1_000,
            "bps": 1,
        }
        for unit, multiplier in speed_units.items():
            if displayed_speed.endswith(unit):
                speed_bps = int(float(displayed_speed.removesuffix(unit)) * multiplier)
                break

        record = {
            "name": item["name"],
            "description": item.get("description") or None,
            "mtu": mtu,
            "mac_address": item.get("mac_address"),
            "duplex": str(item.get("duplex") or "").strip().lower() or None,
            "status_admin": "up"
            if item.get("status_admin_raw", "").lower() == "enabled"
            else "down",
            "status_oper": item.get("status_oper_raw", "").lower(),
            "speed_bps": speed_bps,
            "last_cleared": None,
            "transitions": None,
            "errors_in": None,
            "errors_out": None,
            "crc_errors": None,
            "packets_in": item.get("packets_in"),
            "packets_out": item.get("packets_out"),
            "rate_bps_in": item.get("rate_bps_in"),
            "rate_bps_out": item.get("rate_bps_out"),
            "rate_pps_in": item.get("rate_pps_in"),
            "rate_pps_out": item.get("rate_pps_out"),
            "rate_interval": None,
        }
        records.append(InterfaceStatusRecord(**record).model_dump())

    return records
