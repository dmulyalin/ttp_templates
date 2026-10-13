"""Normalize Cisco IOS BGP neighbor output and running configuration.

Used by:
- ttp_templates/platform/cisco_ios_show_ip_bgp_all_neighbors.txt
"""

import re
from typing import Any

from .models import BgpNeighborRecord


_AFI_TO_IANA = {
    "IPv4 Unicast": "ipv4_unicast",
    "IPv6 Unicast": "ipv6_unicast",
    "IPv4 Multicast": "ipv4_multicast",
    "IPv6 Multicast": "ipv6_multicast",
    "VPNv4 Unicast": "ipv4_mpls_vpn",
    "VPNv6 Unicast": "ipv6_mpls_vpn",
    "IPv4 Label-Unicast": "ipv4_labeled_unicast",
    "IPv6 Label-Unicast": "ipv6_labeled_unicast",
    "IPv4 Labeled Unicast": "ipv4_labeled_unicast",
    "IPv6 Labeled Unicast": "ipv6_labeled_unicast",
    "L2VPN E-VPN": "l2vpn_evpn",
    "L2VPN EVPN": "l2vpn_evpn",
    "L2VPN VPLS": "l2vpn_vpls",
    "IPv4 MDT": "ipv4_mdt",
    "IPv4 Flowspec": "ipv4_flow_spec",
    "IPv6 Flowspec": "ipv6_flow_spec",
    "IPv4 Flow Specification": "ipv4_flow_spec",
    "IPv6 Flow Specification": "ipv6_flow_spec",
    "IPv4 SR-TE": "ipv4_sr_te",
    "IPv6 SR-TE": "ipv6_sr_te",
    "Link-state": "link_state",
}


def transform_bgp_neighbors(payload: Any) -> list[dict[str, Any]]:
    """Merge address-family sections and validate normalized neighbor records."""
    records = {}
    items = [payload] if isinstance(payload, dict) else payload or []
    router_asn = None
    configs = {}
    for item in items:
        bgp = item.get("bgp_config", {})
        if "router_asn" in bgp:
            asn = bgp["router_asn"].split(".")
            router_asn = (
                int(asn[0]) * 65536 + int(asn[1]) if len(asn) == 2 else int(asn[0])
            )
        for scope in [bgp, *bgp.get("families", [])]:
            for statement in scope.get("statements", []):
                config = configs.setdefault((scope.get("vrf"), statement["peer"]), {})
                if "policy" in statement:
                    policies = config.setdefault(statement["direction"], [])
                    if statement["policy"] not in policies:
                        policies.append(statement["policy"])
                else:
                    config.update(
                        {
                            key: value
                            for key, value in statement.items()
                            if key != "peer"
                        }
                    )
    for item in items:
        for family in item.get("address_families", []):
            afi_name = family["afi_name"].strip()
            afi = _AFI_TO_IANA.get(afi_name, afi_name.lower().replace(" ", "_"))
            for neighbor in family.get("neighbors", []):
                vrf = neighbor.get("vrf")
                if vrf and vrf.lower() in {"default", "global", "master"}:
                    vrf = None
                address = neighbor["remote_address"]
                key = (vrf, address)
                if key not in records:
                    records[key] = {
                        "name": f"{vrf or 'default'}_{address}",
                        "vrf": vrf,
                        "remote_address": address,
                        "remote_as": neighbor["remote_as"],
                        **dict.fromkeys(
                            [
                                "description",
                                "state",
                                "local_address",
                                "local_as",
                                "local_interface",
                                "router_id",
                                "peer_group",
                                "peering_type",
                                "hold_time",
                                "keepalive",
                                "uptime_seconds",
                                "max_ttl",
                                "prefix_list_in",
                                "prefix_list_out",
                            ]
                        ),
                        "afi": [],
                        "import_policies": [],
                        "export_policies": [],
                    }
                record = records[key]
                for field in (
                    "description",
                    "local_address",
                    "router_id",
                    "peer_group",
                    "hold_time",
                    "keepalive",
                    "local_interface",
                ):
                    value = neighbor.get(field)
                    if value is not None and value != "(none)":
                        record[field] = value
                peering_type = (neighbor.get("peering_type") or "").strip().lower()
                if peering_type in {"internal", "external"}:
                    record["peering_type"] = peering_type
                state = (
                    (neighbor.get("bgp_state") or "").split(",", 1)[0].strip().lower()
                )
                if state in {
                    "idle",
                    "connect",
                    "active",
                    "opensent",
                    "openconfirm",
                    "established",
                }:
                    record["state"] = state
                uptime = re.search(r"up for\s+(\S+)", neighbor.get("bgp_state") or "")
                if uptime:
                    value = uptime.group(1)
                    if re.fullmatch(r"\d+:\d+:\d+", value):
                        hours, minutes, seconds = map(int, value.split(":"))
                        record["uptime_seconds"] = hours * 3600 + minutes * 60 + seconds
                    elif re.fullmatch(r"(?:\d+[ywdhms])+", value):
                        units = {
                            "y": 31536000,
                            "w": 604800,
                            "d": 86400,
                            "h": 3600,
                            "m": 60,
                            "s": 1,
                        }
                        record["uptime_seconds"] = sum(
                            int(number) * units[unit]
                            for number, unit in re.findall(r"(\d+)([ywdhms])", value)
                        )
                if afi not in record["afi"]:
                    record["afi"].append(afi)
                for direction in ("sent", "received"):
                    count = neighbor.get(f"prefixes_{direction}")
                    if count is not None:
                        record[f"{afi}_prefixes_{direction}"] = count
                for source, target in (
                    ("import_policy", "import_policies"),
                    ("export_policy", "export_policies"),
                ):
                    policy = (neighbor.get(source) or "").strip()
                    if policy and policy not in record[target]:
                        record[target].append(policy)
    # Enrich operational peers only; direct settings override inherited groups.
    for (vrf, address), record in records.items():
        config = configs.get((vrf, address), {})
        peer_group = config.get("peer_group") or record["peer_group"]
        group = configs.get((vrf, peer_group), {})
        effective = {**group, **config}
        local_as = effective.get("local_as")
        if local_as is not None:
            asn = local_as.split(".")
            record["local_as"] = (
                int(asn[0]) * 65536 + int(asn[1]) if len(asn) == 2 else int(asn[0])
            )
        else:
            record["local_as"] = router_asn
        record["peer_group"] = peer_group
        for source, target in (
            ("description", "description"),
            ("update_source", "local_interface"),
        ):
            if source in effective:
                record[target] = effective[source]
        for direction, target in (
            ("in", "import_policies"),
            ("out", "export_policies"),
        ):
            if direction in effective:
                record[target] = effective[direction]
    return [
        BgpNeighborRecord(**record).model_dump(exclude_unset=True)
        for record in records.values()
    ]
