Reference path:
```
ttp://platform/arista_eos_show_running_config_section_interface.txt
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
- `lag`: lag identifier integer (channel-group / mlag number) or `null`
- `lag_type`: ``lag`` for standart port channels, ``mlag`` for mlag port channels, or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
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




---

<details><summary>Template Content</summary>
```
<template name="arista_eos_interface_config" results="per_template">
<doc>
Template to parse Arista interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to 'null' / 'None'):

- 'name': interface name string (e.g. Ethernet1, Ethernet1.10)
- 'type': ''other'' by default; ''bridge'' if "vlan" in name;
    ''lag'' if "port-channel" in name; ''virtual'' if "loopback" in name
    or if the interface name contains a dot ('.')
- 'enabled': boolean; interfaces are 'True' by default unless explicitly
    shutdown in the config
- 'parent': parent interface name or 'null' (if the interface name contains
    a dot the parent is the part before the dot)
- 'lag': lag identifier integer (channel-group / mlag number) or 'null'
- 'lag_type': ''lag'' for standart port channels, ''mlag'' for mlag port channels, or 'null'
- 'lacp_mode': LACP mode string (e.g. ''active'', ''passive'') or 'null'
- 'mtu': integer MTU or 'null'
- 'mac_address': string in MAC EUI format or 'null'
- 'speed': integer or 'null'
- 'duplex': string or 'null'
- 'description': string (empty string when not set)
- 'mode': 'tagged' / 'access' or 'null'
- 'untagged_vlan': integer or 'null'
- 'tagged_vlans': list of integers (empty list when none)
- 'qinq_svlan': integer or 'null'
- 'vrf': string or 'null'
- 'ipv4_addresses': list of strings with IP/prefix (e.g. 10.0.0.1/24)
- 'ipv6_addresses': list of strings with IP/prefix (e.g. 2001:db8::1/64)

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

<input>
commands = [
    "show running-config section interface"
]
platform = [
    "arista_eos", # scrapli and netmiko
    "eos", # NAPALM
]
</input>

<macro>
def transform_interfaces_to_records(data):
    from ttp_templates.utils.arista_eos_process_show_running_config_section_interface import transform_interfaces_config
        
    return transform_interfaces_config(data)
</macro>

<group>
interface {{ name | _start_ }}
   description {{ description | re(".+") }}
   mtu {{ mtu | to_int }}
   no switchport {{ is_l3_interface | set(True) }}
   vrf {{ vrf }}
   shutdown {{ enabled | set(False) | default(True) }}
   speed forced {{ speed | to_int }}
   mlag {{ lag_id | to_int | let("lag_type", "mlag") }}
   channel-group {{ lag_id | to_int | let("lag_type", "lag") }} mode {{ lacp_mode }}
   switchport trunk allowed vlan {{ tagged_vlans | unrange(rangechar='-', joinchar=',') | split(",") | joinmatches }}
   switchport mode trunk {{ mode | set("tagged") }}
   switchport access vlan {{ untagged_vlan | to_int | let("mode", "access") }}
   mac-address {{ mac_address | mac_eui }}

   <group name="ipv4_addresses*" method="table">
   ip address {{ ip | IP }}/{{ mask }}
   ip address {{ ip | IP }}/{{ mask }} secondary
   ipv4 address {{ ip | IP }}/{{ mask}}
   ipv4 address {{ ip | IP }}/{{ mask}} secondary
   </group>

   <group name="ipv6_addresses*" method="table">
   ipv6 address {{ ip | IPV6 }}/{{ mask}}
   </group>

!{{ _end_ }}
</group>

<output macro="transform_interfaces_to_records"/>

</template>
```
</details>