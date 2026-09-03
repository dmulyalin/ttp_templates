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
one. `local_asn` is true for router and `local-as` ASNs, and false for
`remote-as` ASNs. Results are deduplicated by ASN, preserving the first
occurrence and its description while keeping `local_asn` true if any occurrence
marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - peer-group name or `null`
- `local_asn` - boolean indicating ASN belongs to the device

Example normalized output (YAML):

```yaml
- asn: 65000
  description: null
  local_asn: true
- asn: 64500
  description: TRANSIT
  local_asn: false
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
one. 'local_asn' is true for router and 'local-as' ASNs, and false for
'remote-as' ASNs. Results are deduplicated by ASN, preserving the first
occurrence and its description while keeping 'local_asn' true if any occurrence
marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- 'asn' - AS number integer
- 'description' - peer-group name or 'null'
- 'local_asn' - boolean indicating ASN belongs to the device

Example normalized output (YAML):

'''yaml
- asn: 65000
  description: null
  local_asn: true
- asn: 64500
  description: TRANSIT
  local_asn: false
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
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }}

   <group name="statements*">
   neighbor {{ peer_group | _start_ | let("kind", "peer_group") }} peer group
   neighbor {{ neighbor | _start_ | let("kind", "membership") }} peer group {{ peer_group }}
   neighbor {{ neighbor | _start_ }} remote-as {{ asn | to_int | let("local_asn", False) }}
   neighbor {{ neighbor | _start_ }} local-as {{ asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
   neighbor {{ neighbor | _start_ }} local-as {{ asn | to_int | let("local_asn", True) }}
   </group>

   <group name="vrfs*">
   vrf {{ vrf | _start_ }}

      <group name="statements*">
      neighbor {{ peer_group | _start_ | let("kind", "peer_group") }} peer group
      neighbor {{ neighbor | _start_ | let("kind", "membership") }} peer group {{ peer_group }}
      neighbor {{ neighbor | _start_ }} remote-as {{ asn | to_int | let("local_asn", False) }}
      neighbor {{ neighbor | _start_ }} local-as {{ asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
      neighbor {{ neighbor | _start_ }} local-as {{ asn | to_int | let("local_asn", True) }}
      local-as {{ asn | _start_ | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
      local-as {{ asn | _start_ | to_int | let("local_asn", True) }}
      </group>
   </group>
!{{ _end_ }}
</group>

<output macro="transform_bgp_asns_to_records"/>

</template>

```
</details>