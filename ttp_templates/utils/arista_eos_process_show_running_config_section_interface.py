"""
Normalize Arista EOS interface configuration parsed by TTP into a
standardized list of dictionaries suitable for Netbox imports.

Transforms the parsed result of ``show running-config section interface``
into a flat list where each interface dictionary contains a fixed set of
keys. Missing or unknown values are returned as ``None`` (except
``description`` which is returned as an empty string when unset, and
``tagged_vlans`` which is an empty list when none).

Produced with Copilot Assistance.
"""
from typing import Any, Dict, List, Optional


def transform_interfaces_config(payload: list) -> List[Dict[str, Any]]:
    """
    Transform TTP parse payload for Arista interface blocks into a
    normalized list of interface dictionaries.

    Args:
        payload: TTP macro payload. 

    Returns:
        Normilized list of dictionaries with the fixed set of keys described in the
        template documentation.
    """
    if not payload:
        return []

    interfaces: List[Dict[str, Any]] = []

    for item in payload:
        if not isinstance(item, dict):
            continue

        # Top-level container with "interfaces": { <name>: {...} }
        if "interfaces" in item and isinstance(item["interfaces"], dict):
            for nm, data in item["interfaces"].items():
                d = dict(data) if isinstance(data, dict) else {}
                d["name"] = nm
                interfaces.append(d)

        # Items where keys are interface names mapping to dicts
        elif any(isinstance(v, dict) for v in item.values()) and not item.get("name"):
            for nm, data in item.items():
                if isinstance(data, dict):
                    d = dict(data)
                    d["name"] = nm
                    interfaces.append(d)

        # Individual records with a "name" key
        elif item.get("name"):
            interfaces.append(dict(item))

    normalized_interfaces: List[Dict[str, Any]] = []

    for iface in interfaces:
        name = iface.get("name")
        name_lower = str(name).lower() if name is not None else ""

        # Determine type according to rules in the template doc
        if "vlan" in name_lower:
            interface_type = "bridge"
        elif "port-channel" in name_lower:
            interface_type = "lag"
        elif any(k in name_lower for k in [".", "loopback"]):
            interface_type = "virtual"
        else:
            interface_type = "other"

        # `enabled` is produced by the template as a boolean; default to
        # True when the key is absent.
        enabled = iface.get("enabled", True)

        parent: Optional[str] = None
        if name and "." in str(name):
            parent = str(name).split(".", 1)[0]

        lag = iface.get("lag_id")
        lag_type = iface.get("lag_type") or None
        lacp_mode = iface.get("lacp_mode") or None
        mtu = iface.get("mtu")
        description = iface.get("description") or ""
        mode = iface.get("mode") or None
        untagged = iface.get("untagged_vlan")

        # Convert template-provided tagged VLAN list elements to ints
        raw_tagged = iface.get("tagged_vlans")
        tagged_vlans: List[int] = []
        if isinstance(raw_tagged, list):
            for v in raw_tagged:
                try:
                    tagged_vlans.append(int(v))
                except (TypeError, ValueError):
                    continue
            tagged_vlans = sorted(set(tagged_vlans))

        vrf = iface.get("vrf") or None

        speed = iface.get("speed")

        ipv4_addresses = [f"{i['ip']}/{i['mask']}" for i in iface.get("ipv4_addresses", [])]
        ipv6_addresses = [f"{i['ip']}/{i['mask']}" for i in iface.get("ipv6_addresses", [])]

        record: Dict[str, Any] = {
            "name": name,
            "type": interface_type,
            "enabled": enabled,
            "parent": parent,
            "lag": lag,
            "lag_type": lag_type,
            "lacp_mode": lacp_mode,
            "mtu": mtu,
            "mac_address": iface.get("mac_address"),
            "speed": speed,
            "duplex": iface.get("duplex"),
            "description": description,
            "mode": mode,
            "untagged_vlan": untagged,
            "tagged_vlans": tagged_vlans,
            "ipv4_addresses": ipv4_addresses,
            "ipv6_addresses": ipv6_addresses,
            "qinq_svlan": iface.get("qinq_svlan"),
            "vrf": vrf,
        }

        normalized_interfaces.append(record)

    return normalized_interfaces
