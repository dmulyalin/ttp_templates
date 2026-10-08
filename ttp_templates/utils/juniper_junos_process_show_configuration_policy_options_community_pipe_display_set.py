"""Normalize Junos policy communities and routing-instance targets.

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

    # Process all policy communities first so their names always take precedence.
    seen_targets = {record["value"] for record in records if record["type"] == "rt"}
    instance_types = {
        "virtual-switch": "L2VPN",
        "evpn": "L2VPN",
        "vpls": "L2VPN",
        "vrf": "L3VPN",
    }
    for item in items:
        if not isinstance(item, dict):
            continue
        for instance, config in item.get("routing_instances", {}).items():
            instance_type = instance_types.get(config.get("instance_type"))
            if not instance_type:
                continue
            for raw_value in config.get("route_targets", []):
                value, community_type = _normalize_value(raw_value)
                if (
                    community_type != "rt"
                    or not is_concrete_community(value, community_type)
                    or value in seen_targets
                ):
                    continue
                records.append(
                    BgpCommunityRecord(
                        value=value,
                        type="rt",
                        name=f"{instance}_{instance_type}_RT",
                    ).model_dump()
                )
                seen_targets.add(value)

    return records
