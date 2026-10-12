Reference path:
```
ttp://platform/cisco_ios_show_ip_bgp_all_neighbors.txt
```

---



Parse Cisco IOS `show ip bgp all neighbors` for the `bgp_neighbors` getter.

Returns one normalized record per VRF and neighbor address, merging address
families across repeated neighbor sections. Session state, peering type,
addresses, remote ASN, router ID, description, timers, BGP uptime, policies,
and prefix counts are collected when present. Unreported fields are null or
empty lists. Local AS is null unless explicitly reported. Address families
come from section headers, rather than advertised capability lines.



---

<details><summary>Template Content</summary>
```
<template name="cisco_ios_bgp_neighbors" results="per_template">
<doc>
Parse Cisco IOS 'show ip bgp all neighbors' for the 'bgp_neighbors' getter.

Returns one normalized record per VRF and neighbor address, merging address
families across repeated neighbor sections. Session state, peering type,
addresses, remote ASN, router ID, description, timers, BGP uptime, policies,
and prefix counts are collected when present. Unreported fields are null or
empty lists. Local AS is null unless explicitly reported. Address families
come from section headers, rather than advertised capability lines.
</doc>

<input>
commands = ["show ip bgp all neighbors"]
platform = ["cisco_ios", "ios", "cisco_iosxe"]
</input>

<macro>
def transform(payload):
    from ttp_templates.utils.cisco_ios_process_show_ip_bgp_all_neighbors import transform_bgp_neighbors
    return transform_bgp_neighbors(payload)
</macro>

<group name="address_families*">
For address family: {{ afi_name | ORPHRASE | _start_ }}
  <group name="neighbors*">
BGP neighbor is {{ remote_address | _start_ }}, remote AS {{ remote_as | to_int }}, {{ peering_type }} link
BGP neighbor is {{ remote_address | _start_ }}, vrf {{ vrf }}, remote AS {{ remote_as | to_int }}, {{ peering_type }} link
BGP neighbor is {{ remote_address | _start_ }}, remote AS {{ remote_as | to_int }}, local AS {{ local_as | to_int }}, {{ peering_type }} link
BGP neighbor is {{ remote_address | _start_ }}, vrf {{ vrf }}, remote AS {{ remote_as | to_int }}, local AS {{ local_as | to_int }}, {{ peering_type }} link
 Description: {{ description | ORPHRASE }}
  BGP version {{ ignore }}, remote router ID {{ router_id }}
  BGP state = {{ bgp_state | ORPHRASE }}
  Last read {{ ignore }}, last write {{ ignore }}, hold time is {{ hold_time | to_int }}, keepalive interval is {{ keepalive | to_int }} seconds
  Interface associated: {{ local_interface }} {{ _interface_details | ORPHRASE }}
  Interface associated: {{ local_interface }}
  Member of peer-group {{ peer_group }} for session parameters
  Route map for incoming advertisements is {{ import_policy }}
  Route map for outgoing advertisements is {{ export_policy }}
  {{ prefixes_received | to_int }} accepted prefixes, {{ _prefix_details | ORPHRASE }}
  {{ prefixes_received | to_int }} accepted prefixes
  {{ prefixes_sent | to_int }} announced prefixes
Local host: {{ local_address }}, Local port: {{ ignore }}
  </group>
</group>

<output macro="transform"/>
</template>

```
</details>