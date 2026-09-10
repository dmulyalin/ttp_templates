Reference path:
```
ttp://platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt
```

---



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
<template name="juniper_junos_vlans" results="per_template">
<doc>
Template to parse Juniper Junos VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show configuration vlans | display set' and
'show configuration interfaces | display set | match "vlan|interface-mode|irb"'.

Returns normalized list of dictionaries, each dictionary has these keys:

- 'vid' - VLAN ID as integer
- 'name' - VLAN name string
- 'description' - VLAN description string or 'null' when not configured
- 'tagged_interfaces' - interface names carrying the VLAN tagged
- 'untagged_interfaces' - interface names carrying the VLAN untagged

Example normalized output (YAML):

'''yaml
- vid: 100
  name: USERS
  description: User access VLAN
  tagged_interfaces: []
  untagged_interfaces: []
'''

</doc>

<input>
commands = [
    "show configuration vlans | display set",
    "show configuration interfaces | display set | match \"vlan|interface-mode|irb\""
]
platform = [
    "juniper_junos", # scrapli and netmiko
    "junos", # NAPALM
]
</input>

<macro>
def transform_vlans_to_records(data):
    from ttp_templates.utils.juniper_junos_process_show_configuration_vlans_pipe_display_set import transform_vlans_config

    return transform_vlans_config(data)
</macro>

<group name="vlans**.{{ name }}**" method="table">
set vlans {{ name }} vlan-id {{ vid | to_int }}
set vlans {{ name }} description "{{ description | re(".+") }}"
set vlans {{ name }} l3-interface {{ l3_interface }}
</group>

<group name="interfaces**.{{ name }}**" method="table">
set interfaces {{ name }} native-vlan-id {{ untagged_vlan | to_int }}
</group>

<group name="interfaces**.{{ name }}**" functions="sformat('{name}.{unit}', 'name') | del('unit')" method="table">
set interfaces {{ name }} unit {{ unit }} vlan-id {{ dot1q | to_int }}
set interfaces {{ name | re("irb") }} unit {{ unit }} {{ irb_config | re(".+") }}
</group>

<group name="interfaces**.{{ name }}**.switching**" functions="sformat('{name}.{unit}', 'name') | del('unit')" method="table">
set interfaces {{ name }} unit {{ unit }} family ethernet-switching interface-mode {{ dot1q_mode }}
</group>

<group name="interfaces**.{{ name }}**.switching**.vlans*" functions="sformat('{name}.{unit}', 'name') | del('unit')" method="table">
set interfaces {{ name }} unit {{ unit }} family ethernet-switching vlan members {{ vlan }}
</group>

<output macro="transform_vlans_to_records"/>

</template>

```
</details>