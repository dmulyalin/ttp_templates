Reference path:
```
ttp://platform/cisco_asa_show_bgp_neighbors.txt
```

---



Parse Cisco ASA `show bgp neighbors`, `show bgp ipv6 unicast neighbors` and
`show running-config router bgp` for the `bgp_neighbors` getter.

The ASA has no `show bgp all neighbors`: `show bgp neighbors` lists the IPv4
unicast neighbors and `show bgp ipv6 unicast neighbors` the IPv6 ones, so both
outputs are parsed together. Returns one normalized record per neighbor
address. Session state, peering type, remote ASN, router ID, description,
timers, BGP uptime, route maps, and prefix counts are collected when present.
Local AS comes from `router bgp` in the running configuration, which also
supplies descriptions and route maps; it is `null` without that output. The ASA
prints no local address or interface for a session, so those are `null`. `vrf`
is always `null`: the ASA has no VRFs.



---

<details><summary>Template Content</summary>
```
<template name="cisco_asa_bgp_neighbors" results="per_template">
<doc>
Parse Cisco ASA 'show bgp neighbors', 'show bgp ipv6 unicast neighbors' and
'show running-config router bgp' for the 'bgp_neighbors' getter.

The ASA has no 'show bgp all neighbors': 'show bgp neighbors' lists the IPv4
unicast neighbors and 'show bgp ipv6 unicast neighbors' the IPv6 ones, so both
outputs are parsed together. Returns one normalized record per neighbor
address. Session state, peering type, remote ASN, router ID, description,
timers, BGP uptime, route maps, and prefix counts are collected when present.
Local AS comes from 'router bgp' in the running configuration, which also
supplies descriptions and route maps; it is 'null' without that output. The ASA
prints no local address or interface for a session, so those are 'null'. 'vrf'
is always 'null': the ASA has no VRFs.
</doc>

<input>
commands = [
    "show bgp neighbors",
    "show bgp ipv6 unicast neighbors",
    "show running-config router bgp",
]
platform = [
    "cisco_asa", # scrapli community and netmiko
    "asa", # NAPALM community driver
]
</input>

<macro>
def transform(payload):
    from ttp_templates.utils.cisco_asa_process_show_bgp_neighbors import transform_bgp_neighbors

    return transform_bgp_neighbors(payload)
</macro>

<group name="neighbors*">
BGP neighbor is {{ remote_address | _start_ }}, context {{ context }}, remote AS {{ remote_as | to_int }}, {{ peering_type }} link
 Description: {{ description | ORPHRASE }}
  BGP version {{ ignore }}, remote router ID {{ router_id }}
  BGP state = {{ bgp_state | ORPHRASE }}
  Last read {{ ignore }}, last write {{ ignore }}, hold time is {{ hold_time | to_int }}, keepalive interval is {{ keepalive | to_int }} seconds
 <group name="families*">
 For address family: {{ afi_name | ORPHRASE | _start_ }}
  Route map for incoming advertisements is {{ import_policy }}
  Route map for outgoing advertisements is {{ export_policy }}
    Prefixes Current: {{ prefixes_sent | to_int }} {{ prefixes_received | to_int }}
 </group>
</group>

<group name="bgp_config">
router bgp {{ router_asn | _start_ }}
 <group name="families*">
 address-family {{ afi | _start_ }} {{ safi }}
  <group name="statements*">
  neighbor {{ peer | _start_ }} description {{ description | ORPHRASE }}
  neighbor {{ peer | _start_ }} route-map {{ policy }} {{ direction }}
  </group>
 exit-address-family {{ _end_ }}
 </group>
</group>

<output macro="transform"/>
</template>

```
</details>