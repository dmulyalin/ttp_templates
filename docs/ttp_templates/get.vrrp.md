Reference path:
```
ttp://get/vrrp.txt
```

---



Template to parse and normalize Cisco IOS-XR VRRP formal configuration.

This template requires output of:

- `show running-config formal router vrrp`

Configuration belonging to the same interface, address family, and VRRP group
is combined by the TTP group hierarchy. The default VRRP priority of 100 is
returned when priority is not explicitly configured. Text authentication
credentials are not included in the normalized output.

Returns a normalized list of dictionaries with these keys:

- `interface` - interface name string
- `group` - VRRP group number integer
- `virtual_address` - virtual IPv4 or IPv6 address string
- `priority` - VRRP priority integer
- `authentication_type` - authentication type string or `null`

Example normalized output (YAML):

```yaml
- interface: BVI123
  group: 1
  virtual_address: 123.123.123.97
  priority: 123
  authentication_type: text
```




Template to parse and normalize Juniper Junos VRRP configuration.

This template requires output of:

- `show configuration | display set | match vrrp-group`

Statements belonging to the same interface address and VRRP group are merged.
The default Junos VRRP priority of 100 is returned when priority is not
explicitly configured.

Returns a normalized list of dictionaries with these keys:

- `interface` - logical interface name string
- `group` - VRRP group number integer
- `virtual_address` - virtual IPv4 address string
- `priority` - VRRP priority integer
- `authentication_type` - authentication type string or `null`

Example normalized output (YAML):

```yaml
- interface: ae123.123
  group: 1
  virtual_address: 123.123.102.233
  priority: 123
  authentication_type: md5
```




---

<details><summary>Template Content</summary>
```
<template name="vrrp" results="per_template">
<doc>
Getter template to parse VRRP configuration from network devices.

Supported platforms:

- Cisco IOS-XR
- Juniper Junos

Returns a normalized list of dictionaries, each dictionary has these keys:

- 'interface' - logical interface name string
- 'group' - VRRP group number integer
- 'virtual_address' - virtual IPv4 or IPv6 address string
- 'priority' - VRRP priority integer
- 'authentication_type' - authentication type string or 'null'

Example normalized output (YAML):

'''yaml
- interface: ae123.123
  group: 1
  virtual_address: 123.123.102.233
  priority: 123
  authentication_type: md5
'''

</doc>

<extend template="ttp://platform/cisco_xr_show_running_config_formal_router_vrrp.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_pipe_display_set_pipe_match_vrrp_group.txt"/>

</template>

```
</details>