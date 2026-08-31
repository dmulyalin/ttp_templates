Reference path:
```
ttp://platform/arista_eos_show_running_config_section_router_bgp.txt
```

---



Template to parse unique BGP ASNs from Arista EOS configuration.

This template requires output of:

- `show running-config section router bgp`

ASNs are collected from the `router bgp` process and global or VRF
`remote-as` and `local-as` statements. A peer-group name is used as the
description for ASNs configured on a peer group or on a neighbor assigned to
one. Results are deduplicated by ASN, preserving the first occurrence and its
description.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - peer-group name or `null`

Example normalized output (YAML):

```yaml
- asn: 65000
  description: null
- asn: 64500
  description: TRANSIT
```




---

<details><summary>Template Content</summary>
```
<template name="arista_eos_bgp_asn" results="per_template">
<doc>
Template to parse unique BGP ASNs from Arista EOS configuration.

This template requires output of:

- 'show running-config section router bgp'

ASNs are collected from the 'router bgp' process and global or VRF
'remote-as' and 'local-as' statements. A peer-group name is used as the
description for ASNs configured on a peer group or on a neighbor assigned to
one. Results are deduplicated by ASN, preserving the first occurrence and its
description.

Returns a normalized list of dictionaries with these keys:

- 'asn' - AS number integer
- 'description' - peer-group name or 'null'

Example normalized output (YAML):

'''yaml
- asn: 65000
  description: null
- asn: 64500
  description: TRANSIT
'''

</doc>

<input>
commands = [
    "show running-config section router bgp"
]
platform = [
    "arista_eos",
    "eos",
]
</input>

<macro>
def transform_bgp_asns_to_records(data):
    from ttp_templates.utils.arista_eos_process_show_running_config_section_router_bgp import transform_bgp_asns

    return transform_bgp_asns(data)
</macro>

<group name="bgp">
router bgp {{ router_asn | _start_ | to_int }}

   <group name="statements*">
   neighbor {{ peer_group | _start_ | let("kind", "peer_group") }} peer group
   neighbor {{ neighbor | _start_ | let("kind", "membership") }} peer group {{ peer_group }}
   neighbor {{ neighbor | _start_ | let("kind", "asn") }} remote-as {{ asn | to_int }}
   neighbor {{ neighbor | _start_ | let("kind", "asn") }} local-as {{ asn | to_int }} {{ local_as_options | ORPHRASE }}
   neighbor {{ neighbor | _start_ | let("kind", "asn") }} local-as {{ asn | to_int }}
   </group>

   <group name="vrfs*">
   vrf {{ vrf | _start_ }}

      <group name="statements*">
      neighbor {{ peer_group | _start_ | let("kind", "peer_group") }} peer group
      neighbor {{ neighbor | _start_ | let("kind", "membership") }} peer group {{ peer_group }}
      neighbor {{ neighbor | _start_ | let("kind", "asn") }} remote-as {{ asn | to_int }}
      neighbor {{ neighbor | _start_ | let("kind", "asn") }} local-as {{ asn | to_int }} {{ local_as_options | ORPHRASE }}
      neighbor {{ neighbor | _start_ | let("kind", "asn") }} local-as {{ asn | to_int }}
      local-as {{ asn | _start_ | to_int | let("kind", "asn") }} {{ local_as_options | ORPHRASE }}
      local-as {{ asn | _start_ | to_int | let("kind", "asn") }}
      </group>
   </group>
!{{ _end_ }}
</group>

<output macro="transform_bgp_asns_to_records"/>

</template>

```
</details>