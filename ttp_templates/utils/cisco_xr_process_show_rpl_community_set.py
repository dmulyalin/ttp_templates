"""Normalize Cisco IOS-XR ``show rpl *community-set`` output.

Used by:
- ttp_templates/platform/cisco_xr_show_rpl_community_set.txt
"""

import shlex
from typing import Any, Dict, List

from .bgp_communities import is_concrete_community
from .models import BgpCommunityRecord


def transform_community_sets(payload: Any) -> List[Dict[str, str]]:
    """Convert parsed community sets into one record per community value."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, str]] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        for key, default_type in (
            ("standard_sets", "standard"),
            ("extended_sets", None),
            ("large_sets", "large"),
        ):
            sets = item.get(key, [])
            sets = [sets] if isinstance(sets, dict) else sets
            for community_set in sets:
                community_type = community_set.get("type") or default_type
                values = shlex.split(
                    community_set.get("values", "").replace(",", " ")
                )
                skip_pattern = False
                for value in values:
                    if value in ("dfa-regex", "ios-regex"):
                        skip_pattern = True
                        continue
                    if skip_pattern:
                        skip_pattern = False
                        continue
                    if not is_concrete_community(value, community_type):
                        continue
                    record = {
                        "value": value,
                        "type": community_type,
                        "name": community_set["name"],
                    }
                    records.append(BgpCommunityRecord(**record).model_dump())

    return records
