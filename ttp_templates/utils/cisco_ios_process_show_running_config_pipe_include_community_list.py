"""Normalize Cisco IOS BGP community-list configuration.

Used by:
- ttp_templates/platform/cisco_ios_show_running_config_pipe_include_community_list.txt
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


def transform_community_lists(payload: Any) -> List[Dict[str, str]]:
    """Convert permitted community-list values into normalized records."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, str]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        for community_list in _as_list(item.get("standard_lists")):
            for value in shlex.split(community_list.get("values", "")):
                if not is_concrete_community(value, "standard"):
                    continue
                record = {
                    "value": value,
                    "type": "standard",
                    "name": community_list["name"],
                }
                records.append(BgpCommunityRecord(**record).model_dump())

        for community_list in _as_list(item.get("extended_lists")):
            community_type = None
            for value in shlex.split(community_list.get("values", "")):
                if value in ("rt", "soo"):
                    community_type = value
                    continue
                if community_type and is_concrete_community(value, community_type):
                    record = {
                        "value": value,
                        "type": community_type,
                        "name": community_list["name"],
                    }
                    records.append(BgpCommunityRecord(**record).model_dump())

        for community_list in _as_list(item.get("large_lists")):
            for value in shlex.split(community_list.get("values", "")):
                if not is_concrete_community(value, "large"):
                    continue
                record = {
                    "value": value,
                    "type": "large",
                    "name": community_list["name"],
                }
                records.append(BgpCommunityRecord(**record).model_dump())

    return records
