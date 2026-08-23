"""Normalize Arista EOS ``show interfaces`` output.

Used by:
- ttp_templates/platform/arista_eos_show_interfaces.txt
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

        interface_status = item.get("interface_status", "").lower()
        displayed_speed = item.get("displayed_speed", "")
        speed_bps = item.get("speed_kbps")
        if speed_bps is not None:
            speed_bps *= 1_000

        if speed_bps is None and displayed_speed and displayed_speed != "Unconfigured":
            speed_units = {"Kb/s": 1_000, "Mb/s": 1_000_000, "Gb/s": 1_000_000_000}
            for unit, multiplier in speed_units.items():
                if displayed_speed.endswith(unit):
                    speed_bps = int(
                        float(displayed_speed.removesuffix(unit)) * multiplier
                    )
                    break

        rate_bps_in = None
        if item.get("rate_bps_in_value") is not None:
            rate_bps_in = int(
                float(item["rate_bps_in_value"])
                * {"bps": 1, "kbps": 1_000, "Mbps": 1_000_000, "Gbps": 1_000_000_000}[
                    item["rate_bps_in_unit"]
                ]
            )

        rate_bps_out = None
        if item.get("rate_bps_out_value") is not None:
            rate_bps_out = int(
                float(item["rate_bps_out_value"])
                * {"bps": 1, "kbps": 1_000, "Mbps": 1_000_000, "Gbps": 1_000_000_000}[
                    item["rate_bps_out_unit"]
                ]
            )

        rate_interval = item.get("rate_interval_in")
        if rate_interval is None:
            rate_interval = item.get("rate_interval_out")
        if rate_interval is not None:
            rate_interval *= 60

        record = {
            "name": item["name"],
            "description": item.get("description", "").strip('"') or None,
            "mtu": item.get("mtu"),
            "mac_address": item.get("mac_address"),
            "duplex": item.get("duplex", "").lower() or None,
            "status_admin": "down"
            if interface_status == "administratively down"
            else "up",
            "status_oper": "up" if interface_status == "up" else "down",
            "speed_bps": speed_bps,
            "last_cleared": item.get("last_cleared"),
            "transitions": item.get("transitions"),
            "errors_in": item.get("errors_in"),
            "errors_out": item.get("errors_out"),
            "crc_errors": item.get("crc_errors"),
            "packets_in": item.get("packets_in"),
            "packets_out": item.get("packets_out"),
            "rate_bps_in": rate_bps_in,
            "rate_bps_out": rate_bps_out,
            "rate_pps_in": item.get("rate_pps_in"),
            "rate_pps_out": item.get("rate_pps_out"),
            "rate_interval": rate_interval,
        }
        records.append(InterfaceStatusRecord(**record).model_dump())

    return records
