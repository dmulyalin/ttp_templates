Reference path:
```
ttp://get/vlans.txt
```

---



Template to parse Arista EOS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show running-config section vlan'.

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




Template to parse Cisco NX-OS VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show running-config vlan'.

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




Template to parse Juniper Junos VLAN configuration and normalize it to a flat
list of VLAN dictionaries.

This template requires output of 'show configuration vlans | display set'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `vid` - VLAN ID as integer
- `name` - VLAN name string
- `description` - VLAN description string or `null` when not configured

Example normalized output (YAML):

```yaml
- vid: 100
  name: USERS
  description: User access VLAN
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
- Cisco NX-OS
- Juniper Junos

Returns normalized list of dictionaries, each dictionary has these keys:

- 'vid' - VLAN ID as integer
- 'name' - VLAN name string
- 'description' - VLAN description string or 'null' when not configured

Example normalized output (YAML):

'''yaml
- vid: 100
  name: USERS
  description: null
'''

</doc>

<extend template="ttp://platform/arista_eos_show_running_config_section_vlan.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_vlan.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_vlan.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt"/>

</template>

```
</details>