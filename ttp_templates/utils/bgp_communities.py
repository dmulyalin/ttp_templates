"""Shared validation for normalized BGP community getter records."""

import re


_WELL_KNOWN = {
    "accept-own",
    "blackhole",
    "graceful-shutdown",
    "gshut",
    "internet",
    "llgr-stale",
    "local-as",
    "no-advertise",
    "no-export",
    "no-export-subconfed",
    "no-llgr",
    "no-peer",
}


def is_concrete_community(value: str, community_type: str) -> bool:
    """Return whether a value is a concrete community rather than a pattern."""
    if community_type == "standard":
        return bool(
            re.fullmatch(r"(?:\d+|0x[0-9A-Fa-f]+|(?:\d+|\d+\.\d+):\d+)", value)
        ) or value.lower() in _WELL_KNOWN
    if community_type == "large":
        return bool(re.fullmatch(r"\d+:\d+:\d+", value))
    return bool(value) and not re.search(r"[\[\]()*+?^$|\\_]", value)
