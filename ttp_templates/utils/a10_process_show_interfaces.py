"""Normalize A10 ACOS ``show interfaces`` output.

Used by:
- ttp_templates/platform/a10_show_interfaces.txt
"""

from typing import Any

from .models import InterfaceStatusRecord


def _normalize_name(kind: Any, identifier: Any) -> str:
    """Return names consistent with the A10 interface configuration getter."""
    return f"{str(kind).strip().lower()} {str(identifier).strip()}"


def _speed_to_bps(displayed_speed: Any) -> int | None:
    """Convert ACOS speed strings such as 100Gbit to bit/s."""
    value = str(displayed_speed or "").strip().lower()
    units = {
        "gbit": 1_000_000_000,
        "mbit": 1_000_000,
        "kbit": 1_000,
        "bit": 1,
    }
    for unit, multiplier in units.items():
        if value.endswith(unit):
            try:
                return int(float(value.removesuffix(unit)) * multiplier)
            except ValueError:
                return None
    return None


def _normalize_duplex(duplex: Any) -> str | None:
    """Expand ACOS duplex abbreviations."""
    value = str(duplex or "").strip().lower()
    return {"fdx": "full", "hdx": "half"}.get(value, value or None)


def transform_interfaces_status(payload: Any) -> list[dict[str, Any]]:
    """Return normalized operational interface records."""
    items = [payload] if isinstance(payload, dict) else payload
    records: list[dict[str, Any]] = []

    for item in items or []:
        if (
            not isinstance(item, dict)
            or not item.get("kind")
            or not item.get("identifier")
        ):
            continue

        admin_state = str(item.get("status_admin_raw", "")).strip().lower()
        oper_state = str(item.get("status_oper_raw", "")).strip().lower()
        last_cleared = item.get("last_cleared")
        if isinstance(last_cleared, str) and last_cleared.lower() == "never":
            last_cleared = "never"

        rate_interval = item.get("rate_interval_in")
        if rate_interval is None:
            rate_interval = item.get("rate_interval_out")

        record = {
            "name": _normalize_name(item["kind"], item["identifier"]),
            "description": item.get("description") or None,
            "mtu": item.get("mtu"),
            "mac_address": item.get("mac_address"),
            "duplex": _normalize_duplex(item.get("duplex_raw")),
            "status_admin": "down"
            if admin_state in {"administratively down", "disabled"}
            else "up",
            "status_oper": "up" if oper_state.startswith("up") else "down",
            "speed_bps": _speed_to_bps(item.get("displayed_speed")),
            "last_cleared": last_cleared,
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
