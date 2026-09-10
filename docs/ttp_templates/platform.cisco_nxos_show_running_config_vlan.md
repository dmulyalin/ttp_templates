Reference path:
```
ttp://platform/cisco_nxos_show_running_config_vlan.txt
```

---



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




---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_vlans" results="per_template">
<doc>
Template to parse Cisco NX-OS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show running-config vlan' and
'show running-config interface'.

Returns normalized list of dictionaries, each dictionary has these keys:

- 'vid' - VLAN ID as integer
- 'name' - VLAN name string; defaults to 'VLAN&lt;vid&gt;' when no name is configured
- 'description' - VLAN description string or 'null' when not configured
- 'tagged_interfaces' - interface names carrying the VLAN tagged
- 'untagged_interfaces' - interface names carrying the VLAN untagged

Duplicate VLAN IDs produced by overlapping list/range declarations and VLAN
definition blocks are collapsed into one record. A record with an explicitly
configured name takes precedence over an unnamed record; otherwise the later
record takes precedence.

Example normalized output (YAML):

'''yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces: []
  untagged_interfaces: []
'''

</doc>

<input>
commands = [
    "show running-config vlan",
    "show running-config interface"
]
platform = [
    "cisco_nxos",
    "nxos",
]
</input>

<macro>
def transform_vlans_to_records(data):
    from ttp_templates.utils.cisco_nxos_process_show_running_config_vlan import transform_vlans_config

    return transform_vlans_config(data)
</macro>

<group name="vlans*">
vlan {{ vid | re("[0-9,-]+") | _start_ }}
  name {{ name | re(".+") }}
  description {{ description | re(".+") }}
</group>

<group name="interfaces*">
interface {{ name | _start_ }}
  encapsulation dot1q {{ tagged_vlans | to_int | joinmatches }}
  switchport access vlan {{ untagged_vlan | to_int }}
  switchport trunk native vlan {{ untagged_vlan | to_int }}
  switchport trunk allowed vlan {{ tagged_vlans | unrange(rangechar='-', joinchar=',') | split(",") | joinmatches }}
  switchport trunk allowed vlan add {{ tagged_vlans | unrange(rangechar='-', joinchar=',') | split(",") | joinmatches }}
!{{ _end_ }}
</group>

<output macro="transform_vlans_to_records"/>

</template>

```
</details>