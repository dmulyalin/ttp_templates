Reference path:
```
ttp://platform/cisco_nxos_show_running_config_vrrpv3.txt
```

---



Template to parse and normalize Cisco NX-OS VRRPv3 configuration.

This template accepts output collected with any of these commands:

- `show running-config vrrp`
- `show running-config vrrpv3`

IPv4 and IPv6 address families, multiple interfaces and groups, primary
addresses with or without the `primary` keyword, and explicit or default
priorities are supported. Secondary virtual addresses are not returned. The
default VRRP priority is 100. VRRPv3 does not provide authentication, so
`authentication_type` is returned as `null`.

Returns a normalized list of dictionaries with these keys:

- `interface` - interface name string
- `group` - VRRP group number integer
- `protocol` - always `vrrpv3`
- `virtual_address` - primary virtual IPv4 or IPv6 address string
- `priority` - VRRP priority integer
- `authentication_type` - always `null`

Example normalized output (YAML):

```yaml
- interface: Vlan20
  group: 10
  protocol: vrrpv3
  virtual_address: 20.1.1.1
  priority: 150
  authentication_type: null
```




---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_vrrp" results="per_template">
<doc>
Template to parse and normalize Cisco NX-OS VRRPv3 configuration.

This template accepts output collected with any of these commands:

- 'show running-config vrrp'
- 'show running-config vrrpv3'

IPv4 and IPv6 address families, multiple interfaces and groups, primary
addresses with or without the 'primary' keyword, and explicit or default
priorities are supported. Secondary virtual addresses are not returned. The
default VRRP priority is 100. VRRPv3 does not provide authentication, so
'authentication_type' is returned as 'null'.

Returns a normalized list of dictionaries with these keys:

- 'interface' - interface name string
- 'group' - VRRP group number integer
- 'protocol' - always 'vrrpv3'
- 'virtual_address' - primary virtual IPv4 or IPv6 address string
- 'priority' - VRRP priority integer
- 'authentication_type' - always 'null'

Example normalized output (YAML):

'''yaml
- interface: Vlan20
  group: 10
  protocol: vrrpv3
  virtual_address: 20.1.1.1
  priority: 150
  authentication_type: null
'''

</doc>

<input>
commands = [
    "show running-config vrrp",
    "show running-config vrrpv3"
]
platform = [
    "cisco_nxos",
    "nxos",
]
</input>

<macro>
def transform_vrrp_to_records(data):
    from ttp_templates.utils.cisco_nxos_process_show_running_config_vrrpv3 import transform_vrrp_config

    return transform_vrrp_config(data)
</macro>

<group name="interfaces**.{{ interface }}**">
interface {{ interface | _start_ }}

  <group name="vrrp**.{{ address_family }}**.{{ group }}**">
  {{ protocol | _start_ | re("vrrpv3") }} {{ group | DIGIT | to_int }} address-family {{ address_family }}
    address {{ virtual_address }} primary
    address {{ virtual_address }}
    priority {{ priority | DIGIT | to_int }}
  </group>

!{{ _end_ }}
</group>

<output macro="transform_vrrp_to_records"/>

</template>

```
</details>