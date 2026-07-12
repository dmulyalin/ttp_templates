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




Template to parse A10 interface configuration and normalize it to a flat list
of dictionaries suitable for Netbox import.

This template requires output of
'show running-config partition-config all | section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. management, ethernet 1/1, trunk 1/10,
    ve 1/100)
- `type`: ``other`` by default; ``lag`` for trunk interfaces; ``bridge`` for
    VE interfaces
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    disabled in the config
- `parent`: parent interface name or `null`
- `lag_id`: trunk-group identifier integer or `null`
- `lag_type`: ``lag`` for trunk-group member interfaces or `null`
- `lacp_mode`: LACP mode string (e.g. ``lacp``) or `null`
- `lag`: name of parent trunk interface or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: always `null`
- `speed`: always `null`
- `duplex`: always `null`
- `description`: string from A10 interface `name` command, empty string when
    not set
- `mode`: ``tagged`` for trunk interfaces carrying tagged VLANs, ``access`` for
    VE interfaces, or `null`
- `untagged_vlan`: VLAN ID inferred from VE interface name or `null`
- `tagged_vlans`: list of VLAN IDs tagged on a trunk interface
- `qinq_svlan`: always `null`
- `vrf`: always `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 192.0.2.1/30)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: uplink trunk
  duplex: null
  enabled: true
  ipv4_addresses: []
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_id: null
  lag_type: null
  mac_address: null
  mode: tagged
  mtu: null
  name: trunk 1/10
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans:
  - 100
  type: lag
  untagged_vlan: null
  vrf: null
```




*Authored by Codex GPT-5.*

Template to parse Cisco IOS interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config | section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. GigabitEthernet0/1, Vlan100)
- `type`: ``other`` by default; ``bridge`` if "vlan" or "bvi" in name;
    ``lag`` if "port-channel" in name; ``virtual`` if "loopback", "tunnel",
    or if the interface name contains a dot (`.`)
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    shutdown in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (channel-group number) or `null`
- `lag_type`: ``lag`` for standard port channels or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
- `lag`: Name of parent LAG interface e.g. `Port-channel10` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: string in MAC EUI format or `null`
- `speed`: integer speed in kbit/s or `null`
- `duplex`: string duplex setting or `null`
- `description`: string (empty string when not set)
- `mode`: ``tagged`` / ``access`` or `null`
- `untagged_vlan`: integer or `null`
- `tagged_vlans`: list of integers (empty list when none)
- `qinq_svlan`: integer inner VLAN from `second-dot1q` or `null`
- `vrf`: string or `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/24)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: Users SVI
  duplex: null
  enabled: true
  ipv4_addresses:
  - 192.0.2.1/24
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_id: null
  lag_type: null
  mac_address: null
  mode: access
  mtu: 1500
  name: Vlan100
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: bridge
  untagged_vlan: 100
  vrf: USERS
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




Template to parse Cisco NX-OS interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. Ethernet1/1, Port-channel10)
- `type`: ``other`` by default; ``bridge`` if "vlan" in name;
    ``lag`` if "port-channel" in name; ``virtual`` if "loopback", "tunnel",
    or "nve" in name, or if the interface name contains a dot (`.`)
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    shutdown in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (channel-group / vPC number) or `null`
- `lag_type`: ``lag`` for standard port channels, ``mlag`` for vPC port
    channels, or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
- `lag`: Name of parent LAG interface e.g. `Port-channel10` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: string in MAC EUI format or `null`
- `speed`: integer speed in kbit/s or `null`
- `duplex`: string or `null`
- `description`: string (empty string when not set)
- `mode`: ``tagged`` / ``access`` or `null`
- `untagged_vlan`: integer or `null`
- `tagged_vlans`: list of integers (empty list when none)
- `qinq_svlan`: always `null`
- `vrf`: string or `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/24)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: Server access
  duplex: null
  enabled: true
  ipv4_addresses: []
  ipv6_addresses: []
  lacp_mode: active
  lag: Port-channel10
  lag_id: 10
  lag_type: lag
  mac_address: null
  mode: access
  mtu: null
  name: Ethernet1/1
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: other
  untagged_vlan: 100
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




Template to parse Linux `ip address show` command output and normalize it to a
flat list of dictionaries suitable for the `get/interfaces` getter.

This template requires output of `ip address show`.

The transform macro returns a list of dictionaries where each dictionary
contains the common interfaces getter keys. Linux `ip address show` is
operational output, so fields that only exist in device configuration are set
to `null` or empty lists.

- `name`: interface name string (e.g. `ens32`, `brblue`)
- `type`: `bridge` for Linux bridge-style names, `lag` for bond/team
    interfaces, `virtual` for loopback/VRF/tunnel-style interfaces, and
    `other` otherwise
- `enabled`: boolean derived from the `UP` interface flag
- `parent`: parent interface name for dotted sub-interface names, or `null`
- `lag`: always `null`
- `lag_id`: always `null`
- `lag_type`: always `null`
- `lacp_mode`: always `null`
- `mtu`: integer MTU or `null`
- `mac_address`: link-layer MAC address or `null`
- `speed`: always `null`
- `duplex`: always `null`
- `description`: empty string
- `mode`: always `null`
- `untagged_vlan`: always `null`
- `tagged_vlans`: empty list
- `qinq_svlan`: always `null`
- `vrf`: Linux master interface name when the interface is enslaved to a VRF
- `ipv4_addresses`: list of strings with IP/prefix
- `ipv6_addresses`: list of strings with IP/prefix

Example normalized output (YAML):

```yaml
- description: ''
  duplex: null
  enabled: true
  ipv4_addresses:
  - 192.168.131.128/24
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_id: null
  lag_type: null
  mac_address: 00:0c:29:56:07:1b
  mode: null
  mtu: 1500
  name: ens32
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
- A10
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Juniper Junos
- Linux

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

<extend template="ttp://platform/a10_show_running_config_partition_config_all_pipe_section_interface.txt"/>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_interface.txt"/>

<extend template="ttp://platform/cisco_xr_show_running_config_interface.txt"/>

<extend template="ttp://platform/cisco_nxos_show_running_config_interface.txt"/>

<extend template="ttp://platform/juniper_junos_show_configuration_interfaces_pipe_display_set.txt"/>

<extend template="ttp://platform/linux_ip_address_show.txt"/>

</template>

```
</details>