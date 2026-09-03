Reference path:
```
ttp://get/bgp_asn.txt
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




Template to parse unique BGP ASNs from Cisco IOS configuration.

This template requires output of:

- `show running-config | section router bgp`

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




Template to parse unique BGP ASNs from Cisco NX-OS configuration.

This template requires output of:

- `show running-config bgp`

ASNs are collected from the `router bgp` process and global or VRF
`remote-as` and `local-as` statements. A peer-template name is used as the
description for ASNs configured on a template or on a neighbor that inherits
one. `local_asn` is true for router and `local-as` ASNs, and false for
`remote-as` ASNs. Results are deduplicated by ASN, preserving the first
occurrence and its description while keeping `local_asn` true if any occurrence
marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - peer-template name or `null`
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




Template to parse unique BGP ASNs from Juniper Junos configuration.

This template requires output of:

- `show configuration | display set | match "autonomous-system|local-as|peer-as"`

ASNs are collected from global and routing-instance `autonomous-system`,
`local-as`, and `peer-as` statements. For BGP group and neighbor statements,
the group name is used as the description. `local_asn` is true for
`autonomous-system` and `local-as` ASNs, and false for `peer-as` ASNs. Results
are deduplicated by ASN, preserving the first occurrence and its description
while keeping `local_asn` true if any occurrence marks the ASN as local.

Returns a normalized list of dictionaries with these keys:

- `asn` - AS number integer
- `description` - BGP group name or `null`
- `local_asn` - boolean indicating ASN belongs to the device

Example normalized output (YAML):

```yaml
- asn: 1234
  description: null
  local_asn: true
- asn: 4321
  description: GROUP_1
  local_asn: false
```




---

<details><summary>Template Content</summary>
```
<template name="bgp_asn" results="per_template">
<doc>
Getter template to parse BGP AS numbers from network-device configuration.

Supported platforms:

- Arista EOS
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Juniper Junos

Returns a normalized list of dictionaries, each dictionary has these keys:

- 'asn' - AS number integer
- 'description' - peer-group name or 'null'
- 'local_asn' - boolean indicating ASN belongs to the device

Records are deduplicated by ASN. The description from the first occurrence is
retained, and 'local_asn' is true if any occurrence marks the ASN as local.

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

<extend template="ttp://platform/arista_eos_show_running_config_section_router_bgp.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_router_bgp.txt"/>

<extend template="ttp://platform/cisco_xr_show_run_formal_pipe_inc_local_aspipe_remote_as.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_bgp.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_autonomous_system.txt"/>

</template>

```
</details>