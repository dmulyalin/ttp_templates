Reference path:
```
ttp://get/vrfs.txt
```

---



Template to parse Arista EOS VRF configuration and normalize it to a flat list
of VRF dictionaries.

This template requires output of 'show running-config section vrf'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - always `vrf`
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `interfaces` - list of interface names assigned to the VRF
- `address_families` - dictionary containing `ipv4` and `ipv6`; each family
  contains `rt_import`, `rt_export`, `route_policy_import`, and
  `route_policy_export`

EVPN route targets are excluded.




Template to parse Cisco IOS VRF configuration and normalize it to a flat list
of VRF dictionaries.

This template requires output of 'show running-config | section vrf'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - always `vrf`
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `interfaces` - list of interface names assigned to the VRF
- `address_families` - dictionary containing `ipv4` and `ipv6`; each family
  contains `rt_import`, `rt_export`, `route_policy_import`, and
  `route_policy_export`

Example normalized output (YAML):

```yaml
- name: CUSTOMER_A
  instance_type: vrf
  description: Customer A VRF
  rd: 65000:100
  interfaces:
  - GigabitEthernet0/0.100
  address_families:
    ipv4:
      rt_import:
      - 65000:100
      rt_export:
      - 65000:100
      route_policy_import: IMPORT-CUSTOMER-A
      route_policy_export: EXPORT-CUSTOMER-A
    ipv6:
      rt_import: []
      rt_export: []
      route_policy_import: null
      route_policy_export: null
```




Template to parse Cisco IOS-XR VRF configuration and normalize it to a flat
list of VRF dictionaries.

This template requires output of 'show running-config vrf' and
'show run formal interface | inc vrf'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - always `vrf`
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `interfaces` - list of interface names assigned to the VRF
- `address_families` - dictionary containing `ipv4` and `ipv6`; each family
  contains `rt_import`, `rt_export`, `route_policy_import`, and
  `route_policy_export`

Example normalized output (YAML):

```yaml
- name: CUSTOMER_A
  instance_type: vrf
  description: Customer A VRF
  rd: 65000:100
  interfaces:
  - TenGigE0/0/0/20
  address_families:
    ipv4:
      rt_import:
      - 65000:100
      rt_export:
      - 65000:100
      route_policy_import: IMPORT-CUSTOMER-A
      route_policy_export: EXPORT-CUSTOMER-A
    ipv6:
      rt_import: []
      rt_export: []
      route_policy_import: null
      route_policy_export: null
```




Template to parse Cisco NX-OS VRF configuration and normalize it to a flat
list of VRF dictionaries.

This template requires output of
'show running-config | section "vrf context"' and
'show run interface | include "interface|vrf"'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - always `vrf`
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `interfaces` - list of interface names assigned to the VRF
- `address_families` - dictionary containing `ipv4` and `ipv6`; each family
  contains `rt_import`, `rt_export`, `route_policy_import`, and
  `route_policy_export`

EVPN route targets are excluded.




Template to parse Juniper Junos routing-instance configuration and normalize
it to a flat list of VRF dictionaries.

This template requires output of
'show configuration routing-instances | display inheritance | display set'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - routing instance type string
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `interfaces` - list of interface names assigned to the VRF
- `address_families` - dictionary containing `ipv4` and `ipv6`; each family
  contains `rt_import`, `rt_export`, `route_policy_import`, and
  `route_policy_export`

Junos routing-instance route targets and policies are unqualified and are
returned for both IPv4 and IPv6.




---

<details><summary>Template Content</summary>
```
<template name="vrfs" results="per_template">
<doc>
Getter template to parse VRFs for network devices. Designed to work with
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

- 'name' - VRF name string
- 'instance_type' - VRF instance type string
- 'description' - VRF description string or 'null' when not configured
- 'rd' - route distinguisher string or 'null' when not configured
- 'interfaces' - list of interface names assigned to the VRF
- 'address_families' - dictionary containing 'ipv4' and 'ipv6'; each family
  contains 'rt_import', 'rt_export', 'route_policy_import', and
  'route_policy_export'

EVPN route targets are excluded. Juniper Junos routing-instance route targets
and policies are unqualified and are returned for both IPv4 and IPv6.

Example normalized output (YAML):

'''yaml
- name: CUSTOMER_A
  instance_type: vrf
  description: Customer A VRF
  rd: 65000:100
  interfaces:
  - Ethernet1.100
  address_families:
    ipv4:
      rt_import:
      - 65000:100
      rt_export:
      - 65000:100
      route_policy_import: IMPORT-CUSTOMER-A
      route_policy_export: EXPORT-CUSTOMER-A
    ipv6:
      rt_import: []
      rt_export: []
      route_policy_import: null
      route_policy_export: null
'''

</doc>

<extend template="ttp://platform/arista_eos_show_running_config_section_vrf.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_vrf.txt"/>

<extend template="ttp://platform/cisco_xr_show_running_config_vrf.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_pipe_section_vrf_context.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_routing_instances_pipe_display_set.txt"/>

</template>

```
</details>