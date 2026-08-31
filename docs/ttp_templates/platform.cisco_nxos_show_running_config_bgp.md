Reference path:
```
ttp://platform/cisco_nxos_show_running_config_bgp.txt
```

---



Template to parse unique BGP ASNs from Cisco NX-OS configuration.

This template requires output of:

- `show running-config bgp`

ASNs are collected from the `router bgp` process and global or VRF
`remote-as` and `local-as` statements. A peer-template name is used as the
description for ASNs configured on a template or on a neighbor that inherits
one. Results are deduplicated by ASN, preserving the first occurrence and its
description.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - peer-template name or `null`

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
<template name="cisco_nxos_bgp_asn" results="per_template">
<doc>
Template to parse unique BGP ASNs from Cisco NX-OS configuration.

This template requires output of:

- 'show running-config bgp'

ASNs are collected from the 'router bgp' process and global or VRF
'remote-as' and 'local-as' statements. A peer-template name is used as the
description for ASNs configured on a template or on a neighbor that inherits
one. Results are deduplicated by ASN, preserving the first occurrence and its
description.

Returns a normalized list of dictionaries with these keys:

- 'asn' - AS number integer
- 'description' - peer-template name or 'null'

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
    "show running-config bgp"
]
platform = [
    "cisco_nxos",
    "nxos",
]
</input>

<macro>
def transform_bgp_asns_to_records(data):
    from ttp_templates.utils.cisco_nxos_process_show_running_config_bgp import transform_bgp_asns

    return transform_bgp_asns(data)
</macro>

<group name="bgp">
router bgp {{ router_asn | _start_ | to_int }}

  <group name="peers*">
  template peer {{ neighbor | _start_ | let("is_peer_group", True) }}
  neighbor {{ neighbor | _start_ | let("is_peer_group", False) }}
    inherit peer {{ peer_group }}

    <group name="asns*">
    remote-as {{ asn | _start_ | to_int }}
    local-as {{ asn | _start_ | to_int }} {{ local_as_options | ORPHRASE }}
    local-as {{ asn | _start_ | to_int }}
    </group>
  </group>

  <group name="vrfs*">
  vrf {{ vrf | _start_ }}

    <group name="local_asns*">
    local-as {{ asn | _start_ | to_int }} {{ local_as_options | ORPHRASE }}
    local-as {{ asn | _start_ | to_int }}
    </group>

    <group name="peers*">
    template peer {{ neighbor | _start_ | let("is_peer_group", True) }}
    neighbor {{ neighbor | _start_ | let("is_peer_group", False) }}
      inherit peer {{ peer_group }}

      <group name="asns*">
      remote-as {{ asn | _start_ | to_int }}
      local-as {{ asn | _start_ | to_int }} {{ local_as_options | ORPHRASE }}
      local-as {{ asn | _start_ | to_int }}
      </group>
    </group>
  </group>
</group>

<output macro="transform_bgp_asns_to_records"/>

</template>

```
</details>