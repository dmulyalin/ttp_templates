Reference path:
```
ttp://platform/cisco_ios_show_running_config_pipe_section_vlan.txt
```

---



Template to parse Cisco IOS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show running-config | section vlan'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string; defaults to `VLAN<vid>` when no name is configured
- `description` - VLAN description string or `null` when not configured

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: null
```




---

<details><summary>Template Content</summary>
```
<template name="cisco_ios_vlans" results="per_template">
<doc>
Template to parse Cisco IOS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show running-config | section vlan'.

Returns normalized list of dictionaries, each dictionary has these keys:

- 'vid' - VLAN ID as integer
- 'name' - VLAN name string; defaults to 'VLAN&lt;vid&gt;' when no name is configured
- 'description' - VLAN description string or 'null' when not configured

Example normalized output (YAML):

'''yaml
- vid: 100
  name: USERS
  description: null
'''

</doc>

<input>
commands = [
    "show running-config | section vlan"
]
platform = [
    "cisco_ios", # Netmiko and Scrapli
    "ios", # NAPALM
]
</input>

<macro>
def transform_vlans_to_records(data):
    from ttp_templates.utils.cisco_ios_process_show_running_config_pipe_section_vlan import transform_vlans_config

    return transform_vlans_config(data)
</macro>

<group name="vlans*">
vlan {{ vid | re("[0-9,-]+") | _start_ }}
 name {{ name | re(".+") }}
 description {{ description | re(".+") }}
!{{ _end_ }}
</group>

<output macro="transform_vlans_to_records"/>

</template>

```
</details>