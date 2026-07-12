Reference path:
```
ttp://platform/a10_show_running_config_partition_config_all_pipe_section_interface.txt
```

---



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




---

<details><summary>Template Content</summary>
```
<template name="a10_interface_config" results="per_template">
<doc>
Template to parse A10 interface configuration and normalize it to a flat list
of dictionaries suitable for Netbox import.

This template requires output of
'show running-config partition-config all | section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to 'null' / 'None'):

- 'name': interface name string (e.g. management, ethernet 1/1, trunk 1/10,
    ve 1/100)
- 'type': ''other'' by default; ''lag'' for trunk interfaces; ''bridge'' for
    VE interfaces
- 'enabled': boolean; interfaces are 'True' by default unless explicitly
    disabled in the config
- 'parent': parent interface name or 'null'
- 'lag_id': trunk-group identifier integer or 'null'
- 'lag_type': ''lag'' for trunk-group member interfaces or 'null'
- 'lacp_mode': LACP mode string (e.g. ''lacp'') or 'null'
- 'lag': name of parent trunk interface or 'null'
- 'mtu': integer MTU or 'null'
- 'mac_address': always 'null'
- 'speed': always 'null'
- 'duplex': always 'null'
- 'description': string from A10 interface 'name' command, empty string when
    not set
- 'mode': ''tagged'' for trunk interfaces carrying tagged VLANs, ''access'' for
    VE interfaces, or 'null'
- 'untagged_vlan': VLAN ID inferred from VE interface name or 'null'
- 'tagged_vlans': list of VLAN IDs tagged on a trunk interface
- 'qinq_svlan': always 'null'
- 'vrf': always 'null'
- 'ipv4_addresses': list of strings with IP/prefix (e.g. 192.0.2.1/30)
- 'ipv6_addresses': list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

'''yaml
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
'''

</doc>

<input>
commands = [
    "show running-config partition-config all | section interface"
]
platform = [
    "a10",
    "a10_ssh",
]
</input>

<macro>
def transform_interfaces_to_records(data):
    from ttp_templates.utils.a10_process_show_running_config_partition_config_all_pipe_section_interface import transform_interfaces_config

    return transform_interfaces_config(data)
</macro>

## ------------------------------------------------------------------------------------------
## Management interface configuration
## ------------------------------------------------------------------------------------------
<group name="interfaces*">
device-context {{ device_context | _start_ }}
  interface {{ name | re("management") | let("kind", "management") }}
    name {{ description | re(".+") }}
    enable {{ enabled | set(True) | default(True) }}
    disable {{ enabled | set(False) }}
    ip default-gateway {{ default_gateway }}
    lldp enable {{ lldp | re(".+") }}

    <group name="ipv4_addresses*" method="table">
    ip address {{ ip | _exact_ }} {{ mask }}
    </group>

    <group name="ipv6_addresses*" method="table">
    ipv6 address {{ ip | _exact_ }}/{{ mask }}
    </group>

!{{ _end_ }}
</group>

## ------------------------------------------------------------------------------------------
## Ethernet, trunk, and VE interface configuration
## ------------------------------------------------------------------------------------------
<group name="interfaces*">
interface {{ kind }} {{ identifier | _start_ }}
  name {{ description | re(".+") }}
  enable {{ enabled | set(True) | default(True) }}
  disable {{ enabled | set(False) }}
  mtu {{ mtu | to_int }}
  lldp enable {{ lldp | re(".+") }}
  trunk-group {{ lag_id | to_int | let("lag_type", "lag") }} {{ lacp_mode }}
  ip nat {{ ip_nat_direction }}
  ipv6 nat {{ ipv6_nat_direction }}

  <group name="ipv4_addresses*" method="table">
  ip address {{ ip | _exact_ }} {{ mask }}
  </group>

  <group name="ipv6_addresses*" method="table">
  ipv6 address {{ ip | _exact_ }}/{{ mask }}
  </group>

!{{ _end_ }}
</group>

## ------------------------------------------------------------------------------------------
## VLAN configuration used to enrich trunk and VE records
## ------------------------------------------------------------------------------------------
<group name="vlans*">
vlan {{ identifier | _start_ }}
  tagged trunk {{ tagged_trunk_id | to_int }}
  untagged trunk {{ untagged_trunk_id | to_int }}
  router-interface ve {{ router_interface | to_int }}
  name {{ description | re(".+") }}
!{{ _end_ }}
</group>

<output macro="transform_interfaces_to_records"/>

</template>

```
</details>