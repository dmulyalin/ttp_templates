Reference path:
```
ttp://get/vlans.txt
```

---



Template to parse Arista EOS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of `show run section vlan`.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string; defaults to `VLAN<vid>` when no name is configured
- `description` - VLAN description string or `null` when not configured
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces: []
  untagged_interfaces: []
```




Template to parse Cisco IOS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of `show running-config | section vlan` and
`show running-config | section interface`.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string; defaults to `VLAN<vid>` when no name is configured
- `description` - VLAN description string or `null` when not configured
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces: []
  untagged_interfaces: []
```




Template to derive Cisco IOS-XR VLANs and interface membership from formal
interface configuration.

This template requires output of
`show run formal interface | inc "encapsulation|BVI"`.

Every VLAN referenced by a dot1q or untagged subinterface encapsulation, or by
a BVI interface name, is returned, including VLANs that do not have a separate
global VLAN definition. Parsed interface mode uses the existing normalized
values `tagged` and `access`; BVI interfaces are untagged members.

Returns normalized list of dictionaries with these keys:

- `vid` - VLAN ID as integer
- `name` - defaults to `VLAN<vid>`
- `description` - always `null`
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged




Template to parse Cisco NX-OS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of `show running-config vlan` and
`show running-config interface`.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string; defaults to `VLAN<vid>` when no name is configured
- `description` - VLAN description string or `null` when not configured
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged

Duplicate VLAN IDs produced by overlapping list/range declarations and VLAN
definition blocks are collapsed into one record. A record with an explicitly
configured name takes precedence over an unnamed record; otherwise the later
record takes precedence.

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces: []
  untagged_interfaces: []
```




Template to parse Juniper Junos VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of `show configuration vlans | display set` and
`show configuration interfaces | display set | match "vlan|interface-mode|irb"`.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string
- `description` - VLAN description string or `null` when not configured
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: User access VLAN
  tagged_interfaces: []
  untagged_interfaces: []
```




---

<details><summary>Template Content</summary>
```
<template name="vlans" results="per_template">
<doc>
Getter template to parse VLANs for network devices. Designed to work with
[Network Automation Fabric](https://docs.norfablabs.com/)
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/)
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Arista EOS
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Juniper Junos

Returns normalized list of dictionaries, each dictionary has these keys:

- 'vid' - VLAN ID as integer
- 'name' - VLAN name string
- 'description' - VLAN description string or 'null' when not configured
- 'tagged_interfaces' - list of interface names carrying the VLAN tagged
- 'untagged_interfaces' - list of interface names carrying the VLAN untagged

Example normalized output (YAML):

'''yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces: []
  untagged_interfaces: []
'''

</doc>

<extend template="ttp://platform/arista_eos_show_running_config_section_vlan.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_vlan.txt"/>

<extend template="ttp://platform/cisco_xr_show_run_formal_interface_pipe_inc_encapsulationpipebvi.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_vlan.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt"/>

</template>

```
</details>