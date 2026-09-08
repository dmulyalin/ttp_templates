Reference path:
```
ttp://platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_vrrp.txt
```

---



Template to parse and normalize Juniper Junos VRRP configuration.

This template requires output of:

- `show configuration | display set | match vrrp`

Statements belonging to the same interface address and VRRP group are merged.
The default Junos VRRP priority of 100 is returned when priority is not
explicitly configured. IPv4 defaults to VRRPv2 unless the global
`set protocols vrrp version-3` statement is present; IPv6 uses VRRPv3.

Returns a normalized list of dictionaries with these keys:

- `interface` - logical interface name string
- `group` - VRRP group number integer
- `protocol` - normalized protocol version (`vrrpv2` or `vrrpv3`)
- `virtual_address` - virtual IPv4 or IPv6 address string
- `priority` - VRRP priority integer
- `authentication_type` - authentication type string or `null`

Example normalized output (YAML):

```yaml
- interface: ae123.123
  group: 1
  protocol: vrrpv2
  virtual_address: 123.123.102.233
  priority: 123
  authentication_type: md5
```




---

<details><summary>Template Content</summary>
```
<template name="juniper_junos_vrrp" results="per_template">
<doc>
Template to parse and normalize Juniper Junos VRRP configuration.

This template requires output of:

- 'show configuration | display set | match vrrp'

Statements belonging to the same interface address and VRRP group are merged.
The default Junos VRRP priority of 100 is returned when priority is not
explicitly configured. IPv4 defaults to VRRPv2 unless the global
'set protocols vrrp version-3' statement is present; IPv6 uses VRRPv3.

Returns a normalized list of dictionaries with these keys:

- 'interface' - logical interface name string
- 'group' - VRRP group number integer
- 'protocol' - normalized protocol version ('vrrpv2' or 'vrrpv3')
- 'virtual_address' - virtual IPv4 or IPv6 address string
- 'priority' - VRRP priority integer
- 'authentication_type' - authentication type string or 'null'

Example normalized output (YAML):

'''yaml
- interface: ae123.123
  group: 1
  protocol: vrrpv2
  virtual_address: 123.123.102.233
  priority: 123
  authentication_type: md5
'''

</doc>

<input>
commands = [
    "show configuration | display set | match vrrp"
]
platform = [
    "juniper_junos",
    "junos",
]
</input>

<macro>
def transform_vrrp_to_records(data):
    from ttp_templates.utils.juniper_junos_process_show_configuration_pipe_display_set_pipe_match_vrrp import transform_vrrp_config

    return transform_vrrp_config(data)
</macro>

<group name="settings">
set protocols vrrp version-3 {{ version_3 | set(True) }}
</group>

<group name="vrrp**.{{ interface }}**.{{ unit }}**.ipv4**.{{ address }}**.{{ group }}**" method="table">
set interfaces {{ interface }} unit {{ unit }} family inet address {{ address }} vrrp-group {{ group | DIGIT | to_int }} virtual-address {{ virtual_address }}
set interfaces {{ interface }} unit {{ unit }} family inet address {{ address }} vrrp-group {{ group | DIGIT | to_int }} priority {{ priority | DIGIT | to_int }}
set interfaces {{ interface }} unit {{ unit }} family inet address {{ address }} vrrp-group {{ group | DIGIT | to_int }} authentication-type {{ authentication_type }}
</group>

<group name="vrrp**.{{ interface }}**.{{ unit }}**.ipv6**.{{ address }}**.{{ group }}**" method="table">
set interfaces {{ interface }} unit {{ unit }} family inet6 address {{ address }} vrrp-inet6-group {{ group | DIGIT | to_int }} virtual-inet6-address {{ virtual_address }}
set interfaces {{ interface }} unit {{ unit }} family inet6 address {{ address }} vrrp-inet6-group {{ group | DIGIT | to_int }} priority {{ priority | DIGIT | to_int }}
</group>

<output macro="transform_vrrp_to_records"/>

</template>

```
</details>