"""Normalize Arista EOS BGP community-list configuration.

Used by:
- ttp_templates/platform/arista_eos_show_running_config_pipe_include_community_list.txt
"""

import shlex
from typing import Any, Dict, List

from .bgp_communities import is_concrete_community
from .models import BgpCommunityRecord


def _as_list(value: Any) -> List[Dict[str, str]]:
    """Return TTP table output as a list."""
    if isinstance(value, dict):
        return [value]
    return value or []


def _append_record(
    records: List[Dict[str, str]], name: str, value: str, community_type: str
) -> None:
    """Append a validated concrete community record."""
    if is_concrete_community(value, community_type):
        record = {"value": value, "type": community_type, "name": name}
        records.append(BgpCommunityRecord(**record).model_dump())


def transform_community_lists(payload: Any) -> List[Dict[str, str]]:
    """Convert permitted EOS community-list values into normalized records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, str]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        for community_list in _as_list(item.get("standard_lists")):
            for value in shlex.split(community_list.get("values", "")):
                _append_record(records, community_list["name"], value, "standard")

        for community_list in _as_list(item.get("extended_lists")):
            community_type = None
            for value in shlex.split(community_list.get("values", "")):
                if value in ("rt", "soo", "lbw"):
                    community_type = value
                    continue
                if community_type:
                    _append_record(
                        records, community_list["name"], value, community_type
                    )

        for community_list in _as_list(item.get("large_lists")):
            for value in shlex.split(community_list.get("values", "")):
                _append_record(records, community_list["name"], value, "large")

    return records
