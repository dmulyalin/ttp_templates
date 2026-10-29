"""Shared normalization for ``ping`` getter records.

The platform templates capture the destination, the packets sent and received,
and the round-trip times as the device prints them (``min/avg/max`` or
``min/avg/max/mdev``, in milliseconds).

Used by:
- ttp_templates/platform/arista_eos_ping.txt
- ttp_templates/platform/cisco_asa_ping.txt
- ttp_templates/platform/cisco_ios_ping.txt
- ttp_templates/platform/cisco_nxos_ping.txt
- ttp_templates/platform/linux_ping.txt
"""

from typing import Any

from .models import PingRecord


def _rtt(rtt: str | None) -> list[float | None]:
    """Return min, avg and max from ``1/2/3`` or ``1/2/3/0.5`` (mdev)."""
    if not rtt:
        return [None, None, None]
    return [float(value) for value in rtt.split("/")[:3]]


def transform_ping(payload: list) -> list[dict[str, Any]]:
    """Return normalized ping records."""
    items = [payload] if isinstance(payload, dict) else payload
    records: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict) or "sent" not in item:
            continue

        sent = item["sent"]
        received = item["received"]
        rtt_min, rtt_avg, rtt_max = _rtt(item.get("rtt"))
        record = {
            "destination": item["destination"].lower(),
            "packets_sent": sent,
            "packets_received": received,
            "packet_loss_percent": round((sent - received) * 100 / sent, 2)
            if sent
            else None,
            "rtt_min_ms": rtt_min,
            "rtt_avg_ms": rtt_avg,
            "rtt_max_ms": rtt_max,
        }
        records.append(PingRecord(**record).model_dump())

    return records
