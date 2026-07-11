Reference path:
```
ttp://platform/linux_ip_address_show.txt
```

---



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
<template name="linux_ip_address_show" results="per_template">
<doc>
Template to parse Linux 'ip address show' command output and normalize it to a
flat list of dictionaries suitable for the 'get/interfaces' getter.

This template requires output of 'ip address show'.

The transform macro returns a list of dictionaries where each dictionary
contains the common interfaces getter keys. Linux 'ip address show' is
operational output, so fields that only exist in device configuration are set
to 'null' or empty lists.

- 'name': interface name string (e.g. 'ens32', 'brblue')
- 'type': 'bridge' for Linux bridge-style names, 'lag' for bond/team
    interfaces, 'virtual' for loopback/VRF/tunnel-style interfaces, and
    'other' otherwise
- 'enabled': boolean derived from the 'UP' interface flag
- 'parent': parent interface name for dotted sub-interface names, or 'null'
- 'lag': always 'null'
- 'lag_id': always 'null'
- 'lag_type': always 'null'
- 'lacp_mode': always 'null'
- 'mtu': integer MTU or 'null'
- 'mac_address': link-layer MAC address or 'null'
- 'speed': always 'null'
- 'duplex': always 'null'
- 'description': empty string
- 'mode': always 'null'
- 'untagged_vlan': always 'null'
- 'tagged_vlans': empty list
- 'qinq_svlan': always 'null'
- 'vrf': Linux master interface name when the interface is enslaved to a VRF
- 'ipv4_addresses': list of strings with IP/prefix
- 'ipv6_addresses': list of strings with IP/prefix

Example normalized output (YAML):

'''yaml
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
'''

</doc>

<input>
commands = [
    "ip address show"
]
platform = [
    "linux",
]
</input>

<macro>
def transform_interfaces_to_records(data):
    from ttp_templates.utils.linux_process_ip_address_show import transform_interfaces

    return transform_interfaces(data)
</macro>

<group>
{{ index | to_int | _start_ }}: {{ name }}: {{ ignore("\\x3c") }}{{ flags | re("[^\\x3e]+") }}{{ ignore("\\x3e") }} mtu {{ mtu | to_int }} {{ ignore(".*") }} master {{ master }} {{ ignore(".*") }}
{{ index | to_int | _start_ }}: {{ name }}: {{ ignore("\\x3c") }}{{ flags | re("[^\\x3e]+") }}{{ ignore("\\x3e") }} mtu {{ mtu | to_int }} {{ ignore(".*") }}
    link/ether {{ mac_address | mac_eui }} {{ ignore(".+") }}

    <group name="ipv4_addresses*" method="table">
    inet {{ ip | IP }}/{{ mask }} {{ ignore(".+") }}
    </group>

    <group name="ipv6_addresses*" method="table">
    inet6 {{ ip | IPV6 }}/{{ mask }} {{ ignore(".*") }}
    </group>
</group>

<output macro="transform_interfaces_to_records"/>

</template>

```
</details>