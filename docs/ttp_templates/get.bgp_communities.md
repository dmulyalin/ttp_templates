Reference path:
```
ttp://get/bgp_communities.txt
```

---



Template to parse Arista EOS BGP community-list configuration from
`show running-config | include community-list`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and regexp entries are excluded. Standard, extended (`rt`,
`soo`, and `lbw`), and large community lists are supported.



Template to parse Cisco IOS BGP community-list configuration from
`show running-config | include community-list`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each permitted concrete community value is returned as a separate
dictionary; pattern entries are excluded. Standard, extended (`rt` and `soo`),
and large community lists are supported.



Template to parse Cisco IOS-XR BGP community sets from these commands:

- `show rpl community-set`
- `show rpl extcommunity-set`
- `show rpl large-community-set`

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded.



Template to parse Cisco NX-OS BGP community-list configuration from
`show running-config rpm`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and expanded entries are excluded. Standard, extended, and
large community lists with optional sequence numbers are supported.



Template to parse Juniper Junos BGP community configuration from
`show configuration policy-options community | display set`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded. Junos `target`, `origin`, and `large` prefixes
are normalized to `rt`, `soo`, and `large` types respectively.



---

<details><summary>Template Content</summary>
```
<template name="bgp_communities" results="per_template">
<doc>
Getter template to parse BGP community sets for network devices.

Supported platforms:

- Arista EOS
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Juniper Junos

Returns a normalized list of dictionaries, each dictionary has these keys:

- 'value' - one BGP community value
- 'type' - community type, such as 'standard', 'rt', or 'large'
- 'name' - community-set name

When a set contains multiple communities, one dictionary is returned for each
concrete value with the same name and type. Pattern entries are excluded.

Example normalized output (YAML):

'''yaml
- value: 65000:100
  type: standard
  name: CUSTOMER_COMMUNITIES
'''

</doc>

<extend template="ttp://platform/arista_eos_show_running_config_pipe_include_community_list.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_include_community_list.txt"/>

<extend template="ttp://platform/cisco_xr_show_rpl_community_set.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_rpm.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_policy_options_community_pipe_display_set.txt"/>

</template>

```
</details>