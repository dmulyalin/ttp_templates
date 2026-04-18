# Arista BGP Neighbors Normalizer

Transforms Arista EOS `show ip bgp neighbors vrf all | json` output to standardized flat-list format.

## Features

- All fields present in every record (missing values = `None`)
- RFC-normalized state values (established, idle, etc.)
- Per-AFI prefix counts automatically extracted
- Consistent field naming across all records

## Quick Start

```python
from arista_bgp_neighbors_normalizer import normalize_bgp_neighbors_data

neighbors = normalize_bgp_neighbors_data(json_data, device_name="spine-1")

for n in neighbors:
    print(f"{n['name']}: {n['state']} AS{n['remote_as']}")
```

## Output Fields (20+)

**Session/Peering:** state, peering_type, hold_time, keepalive, uptime

**Addressing:** local_address, local_interface, remote_address

**AS Info:** local_as, remote_as, router_id

**Identification:** name, description, vrf, peer_group

**Policies:** import_policies, export_policies, prefix_list_in, prefix_list_out

**AFI:** afi (list), per-AFI prefix counts (e.g., `ipv4Unicast_prefixes_sent`)

**Other:** max_ttl

## Supported AFIs

- ipv4Unicast
- ipv6Unicast  
- l2VpnEvpn
- ipv4LabeledUnicast
- ipv6LabeledUnicast

## API Reference

### `normalize_bgp_neighbors_data(json_data, device_name)`
Transforms complete BGP neighbors JSON. Returns list of dicts.

### `normalize_bgp_neighbor(peer_data, device_name, vrf_name)`
Normalizes a single peer entry.

### `ensure_all_fields_present(neighbors)`
Adds missing fields (set to None).

### `normalize_state(state)`
Converts Arista state to RFC format (lowercase).

### `extract_afi_list(neighbor_caps)`
Returns list of enabled AFI names.

### `get_prefixes_for_afi(peer_data, afi)`
Returns (sent_count, received_count) tuple.

## Usage Examples

**Find established external peers:**
```python
established = [n for n in neighbors if n['state'] == 'established' and n['peering_type'] == 'external']
```

**Find EVPN-enabled peers:**
```python
evpn = [n for n in neighbors if 'l2VpnEvpn' in (n['afi'] or [])]
```

**Group by VRF:**
```python
by_vrf = {}
for n in neighbors:
    vrf = n['vrf']
    if vrf not in by_vrf:
        by_vrf[vrf] = []
    by_vrf[vrf].append(n)
```

## TTP Integration

```xml
<template name="bgp_neighbors">
    <input>commands = ["show bgp neighbors vrf all | json"]</input>
    <group>
    { {{ _start_ }}
    {{ data | _line_ | joinmatches }}
    } {{ _end_ }}
    </group>
    <output macro="load_json"/>
    <output macro="transform_bgp_neighbors_to_records"/>
</template>
```

## Testing

```bash
python test_bgp_normalizer.py
```

## Notes

- Missing fields always present (None)
- Prefix lists unavailable in Arista JSON (None)
- "DEFAULT" route maps → None
- Name format: `{device}_{vrf}_{peer_ip}`
- See template docstring for field mapping details
