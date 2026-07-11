Reference path:
```
ttp://get/interfaces.txt
```

---



Template to parse Arista interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. Ethernet1, Ethernet1.10)
- `type`: ``other`` by default; ``bridge`` if "vlan" in name;
    ``lag`` if "port-channel" in name; ``virtual`` if "loopback" in name
    or if the interface name contains a dot (`.`)
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    shutdown in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (channel-group / mlag number) or `null`
- `lag_type`: ``lag`` for standart port channels, ``mlag`` for mlag port channels, or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
- `lag`: Name of parent LAG interface e.g. `Port-Channel1` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: string in MAC EUI format or `null`
- `speed`: integer or `null`
- `duplex`: string or `null`
- `description`: string (empty string when not set)
- `mode`: 'tagged' / 'access' or `null`
- `untagged_vlan`: integer or `null`
- `tagged_vlans`: list of integers (empty list when none)
- `qinq_svlan`: integer or `null`
- `vrf`: string or `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/24)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: Router ID
  duplex: null
  enabled: true
  ipv4_addresses: []
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_type: null
  mac_address: null
  mode: null
  mtu: null
  name: Loopback0
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: virtual
  untagged_vlan: null
  vrf: null
```




Template to parse Cisco IOS-XR interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. GigabitEthernet0/0/0/0, Bundle-Ether1)
- `type`: ``other`` by default; ``bridge`` if "bvi" in name;
    ``lag`` if "bundle" in name; ``virtual`` if "loopback" or "tunnel" in name
    or if the interface name contains a dot (`.`)
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    shutdown in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (bundle id number) or `null`
- `lag_type`: ``lag`` for bundle-ether port channels or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
- `lag`: Name of parent LAG interface e.g. `Bundle-Ether1` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: string MAC address in EUI format or `null`
- `speed`: integer speed in kbit/s or `null`
- `duplex`: string duplex setting or `null`
- `description`: string (empty string when not set)
- `mode`: ``tagged`` when `encapsulation dot1q` is present; ``access`` for BVI interfaces; `null` otherwise
- `untagged_vlan`: integer VLAN derived from BVI interface name (e.g. BVI100 → 100) or `null`
- `tagged_vlans`: list with the dot1q VLAN integer when `encapsulation dot1q` is present; empty list otherwise
- `qinq_svlan`: always `null`
- `vrf`: string or `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/30)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: Router ID
  duplex: null
  enabled: true
  ipv4_addresses:
  - 10.0.0.1/32
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_id: null
  lag_type: null
  mac_address: null
  mode: null
  mtu: null
  name: Loopback0
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: virtual
  untagged_vlan: null
  vrf: null
```




Template to parse Juniper JunOS interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show configuration interfaces | display set'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. xe-0/0/0, xe-0/0/0.100, ae0, lo0.0)
- `type`: ``other`` by default; ``bridge`` if name starts with "irb";
    ``lag`` if name starts with "ae" and has no dot; ``virtual`` if name has
    a dot (sub-interface/unit) or starts with a loopback/tunnel prefix
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    disabled in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (ae group number) or `null`
- `lag_type`: ``lag`` when interface is a member of an aggregated ethernet
    group, or `null`
- `lacp_mode`: LACP mode string on AE interface (e.g. ``active``, ``passive``)
    or `null`
- `lag`: Name of parent LAG interface e.g. `ae0` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: MAC address string of the unit or `null`
- `speed`: integer in kbit/s or `null`
- `duplex`: always `null` (not exposed in display set format)
- `description`: string (empty string when not set)
- `mode`: 'tagged' / 'access' or `null`
- `untagged_vlan`: integer or `null`
- `tagged_vlans`: list of integers (empty list when none)
- `qinq_svlan`: always `null`
- `vrf`: always `null` (routing-instance assignment not captured here)
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/24)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: P2P to PE1
  duplex: null
  enabled: true
  ipv4_addresses: []
  ipv6_addresses: []
  lacp_mode: null
  lag: ae0
  lag_id: 0
  lag_type: lag
  mac_address: null
  mode: null
  mtu: 9192
  name: xe-0/0/0
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: other
  untagged_vlan: null
  vrf: null
```




---

<details><summary>Template Content</summary>
```
<template name="interfaces" results="per_template">
<doc>
Getter template to parse interface configuration for network devices. Designed to work with 
[Network Automation Fabric](https://docs.norfablabs.com/) 
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/) 
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Arista EOS
- Cisco IOS-XR
- Juniper Junos

Returns normalized list of dictionaries, each dictionary has these keys:

- 'name' - interface name string (e.g. Ethernet1, Ethernet1.10)
- 'type' - ''other'' by default; ''bridge'' if "vlan" in name;
    ''lag'' if "port-channel" in name; ''virtual'' if "loopback" in name
    or if the interface name contains a dot ('.')
- 'enabled' - boolean; interfaces are 'True' by default unless explicitly shutdown
- 'parent' - parent interface name or 'null' (set when interface name contains a dot)
- 'lag' - lag identifier integer (channel-group / mlag number) or 'null'
- 'lag_type' - ''lag'' for standard port channels, ''mlag'' for mlag port channels, or 'null'
- 'lacp_mode' - LACP mode string (e.g. ''active'', ''passive'') or 'null'
- 'mtu' - integer MTU or 'null'
- 'mac_address' - string in MAC EUI format or 'null'
- 'speed' - integer or 'null'
- 'duplex' - string or 'null'
- 'description' - string (empty string when not set)
- 'mode' - ''tagged'' / ''access'' or 'null'
- 'untagged_vlan' - integer or 'null'
- 'tagged_vlans' - list of integers (empty list when none)
- 'qinq_svlan' - integer or 'null'
- 'vrf' - string or 'null'
- 'ipv4_addresses' - list of strings with IP/prefix (e.g. ''10.0.0.1/24'')
- 'ipv6_addresses' - list of strings with IP/prefix (e.g. ''2001:db8::1/64'')

Example normalized output (YAML):

'''yaml
- description: Router ID
  duplex: null
  enabled: true
  ipv4_addresses: []
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_type: null
  mac_address: null
  mode: null
  mtu: null
  name: Loopback0
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: virtual
  untagged_vlan: null
  vrf: null
'''

</doc>

<extend template="ttp://platform/arista_eos_show_running_config_section_interface.txt"/>

<extend template="ttp://platform/cisco_xr_show_running_config_interface.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_interfaces_pipe_display_set.txt"/>

</template>
```
</details>
