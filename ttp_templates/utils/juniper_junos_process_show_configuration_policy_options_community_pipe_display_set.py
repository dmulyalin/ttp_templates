"""Normalize Junos policy-options community ``display set`` output.

Used by:
- ttp_templates/platform/juniper_junos_show_configuration_policy_options_community_pipe_display_set.txt
"""

import shlex
from typing import Any, Dict, List, Tuple

from .bgp_communities import is_concrete_community
from .models import BgpCommunityRecord


def _normalize_value(value: str) -> Tuple[str, str]:
    """Return the normalized value and community type."""
    prefix, separator, remainder = value.partition(":")
    community_types = {"target": "rt", "origin": "soo", "large": "large"}
    if separator and value.count(":") >= 2:
        return remainder, community_types.get(prefix, prefix)
    return value, "standard"


def transform_community_sets(payload: Any) -> List[Dict[str, str]]:
    """Convert Junos community members into one record per community value."""
    items = [payload] if isinstance(payload, dict) else payload or []
    records: List[Dict[str, str]] = []

    for item in items:
        if not isinstance(item, dict):
            continue
        community_sets = item.get("community_sets", [])
        community_sets = (
            [community_sets] if isinstance(community_sets, dict) else community_sets
        )
        for community_set in community_sets:
            values = shlex.split(community_set.get("values", ""))
            for raw_value in values:
                if raw_value in ("[", "]"):
                    continue
                value, community_type = _normalize_value(raw_value)
                if not is_concrete_community(value, community_type):
                    continue
                record = {
                    "value": value,
                    "type": community_type,
                    "name": community_set["name"],
                }
                records.append(BgpCommunityRecord(**record).model_dump())

    return records
