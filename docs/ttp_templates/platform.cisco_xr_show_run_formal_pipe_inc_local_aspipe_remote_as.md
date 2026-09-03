Reference path:
```
ttp://platform/cisco_xr_show_run_formal_pipe_inc_local_aspipe_remote_as.txt
```

---



Template to parse unique BGP ASNs from Cisco IOS-XR formal configuration.

This template requires output of:

- `show run formal | inc "local-as|remote-as"`

The local router ASN is collected from each `router bgp` prefix. Peer ASNs are
collected from `remote-as` and `local-as` statements. When a statement belongs
to a neighbor group, that group name is used as the description. `local_asn` is
true for router and `local-as` ASNs, and false for `remote-as` ASNs. Results
are deduplicated by ASN, preserving the first occurrence and its description
while keeping `local_asn` true if any occurrence marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - peer-group name or `null`
- `local_asn` - boolean indicating ASN belongs to the device

Example normalized output (YAML):

```yaml
- asn: 12345
  description: null
  local_asn: true
- asn: 54321
  description: PEER_GROUP_1
  local_asn: false
```




---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_bgp_asn" results="per_template">
<doc>
Template to parse unique BGP ASNs from Cisco IOS-XR formal configuration.

This template requires output of:

- 'show run formal | inc "local-as|remote-as"'

The local router ASN is collected from each 'router bgp' prefix. Peer ASNs are
collected from 'remote-as' and 'local-as' statements. When a statement belongs
to a neighbor group, that group name is used as the description. 'local_asn' is
true for router and 'local-as' ASNs, and false for 'remote-as' ASNs. Results
are deduplicated by ASN, preserving the first occurrence and its description
while keeping 'local_asn' true if any occurrence marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- 'asn' - AS number integer
- 'description' - peer-group name or 'null'
- 'local_asn' - boolean indicating ASN belongs to the device

Example normalized output (YAML):

'''yaml
- asn: 12345
  description: null
  local_asn: true
- asn: 54321
  description: PEER_GROUP_1
  local_asn: false
'''

</doc>

<input>
commands = [
    'show running-config formal | include "local-as|remote-as"',
]
platform = [
    "cisco_xr",
    "iosxr",
    "cisco_iosxr",
]
</input>

<macro>
def transform_bgp_asns_to_records(data):
    from ttp_templates.utils.cisco_xr_process_show_run_formal_pipe_inc_local_aspipe_remote_as import transform_bgp_asns

    return transform_bgp_asns(data)
</macro>

<group name="statements*">
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor-group {{ description }} remote-as {{ peer_asn | to_int | let("local_asn", False) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor-group {{ description }} local-as {{ peer_asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor-group {{ description }} local-as {{ peer_asn | to_int | let("local_asn", True) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor {{ neighbor }} remote-as {{ peer_asn | to_int | let("local_asn", False) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor {{ neighbor }} local-as {{ peer_asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} neighbor {{ neighbor }} local-as {{ peer_asn | to_int | let("local_asn", True) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor-group {{ description }} remote-as {{ peer_asn | to_int | let("local_asn", False) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor-group {{ description }} local-as {{ peer_asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor-group {{ description }} local-as {{ peer_asn | to_int | let("local_asn", True) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor {{ neighbor }} remote-as {{ peer_asn | to_int | let("local_asn", False) }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor {{ neighbor }} local-as {{ peer_asn | to_int | let("local_asn", True) }} {{ local_as_options | ORPHRASE }}
router bgp {{ router_asn | _start_ | to_int | let("local_asn", True) }} vrf {{ vrf }} neighbor {{ neighbor }} local-as {{ peer_asn | to_int | let("local_asn", True) }}
</group>

<output macro="transform_bgp_asns_to_records"/>

</template>

```
</details>