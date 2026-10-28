"""Normalize Cisco ASA ``show interface`` output.

Used by:
- ttp_templates/platform/cisco_asa_show_interface.txt
"""

from typing import Any

from .models import InterfaceStatusRecord


def _duplex(duplex_status: str) -> str | None:
    """Return the operational duplex from ``Auto-Duplex(Full-duplex)`` or
    ``Full-Duplex``; ``Auto-Duplex`` alone (no link) has none."""
    value = duplex_status
    if "(" in value:
        value = value.split("(", 1)[1].rstrip(")")
    value = value.lower().replace("-duplex", "")
    return None if value == "auto" else value or None


def _bps(bytes_per_second: int | None) -> int | None:
    return None if bytes_per_second is None else bytes_per_second * 8


def transform_interfaces_status(payload: list) -> list[dict[str, Any]]:
    """Return normalized operational interface records."""
    items = [payload] if isinstance(payload, dict) else payload
    records: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict) or not item.get("name"):
            continue

        interface_status = item.get("interface_status", "").lower()
        protocol_status = item.get("protocol_status", "").lower()
        has_rates = "rate_pps_in" in item or "rate_pps_out" in item
        record = {
            "name": item["name"],
            "description": item.get("description") or None,
            "mtu": item.get("mtu"),
            "mac_address": item.get("mac_address"),
            "duplex": _duplex(item["duplex_status"])
            if item.get("duplex_status")
            else None,
            "status_admin": "down"
            if interface_status == "administratively down"
            else "up",
            "status_oper": "up"
            if interface_status == "up" and protocol_status.startswith("up")
            else "down",
            "speed_bps": item["speed_mbps"] * 1_000_000
            if item.get("speed_mbps") is not None
            else None,
            "last_cleared": None,
            "transitions": None,
            "errors_in": item.get("errors_in"),
            "errors_out": item.get("errors_out"),
            "crc_errors": item.get("crc_errors"),
            "packets_in": item.get("packets_in"),
            "packets_out": item.get("packets_out"),
            "rate_bps_in": _bps(item.get("rate_bytes_in")),
            "rate_bps_out": _bps(item.get("rate_bytes_out")),
            "rate_pps_in": item.get("rate_pps_in"),
            "rate_pps_out": item.get("rate_pps_out"),
            "rate_interval": 300 if has_rates else None,
        }
        records.append(InterfaceStatusRecord(**record).model_dump())

    return records
