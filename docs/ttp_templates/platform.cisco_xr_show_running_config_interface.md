Reference path:
```
ttp://platform/cisco_xr_show_running_config_interface.txt
```

---



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




---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_interface_config" results="per_template">
<doc>
Template to parse Cisco IOS-XR interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to 'null' / 'None'):

- 'name': interface name string (e.g. GigabitEthernet0/0/0/0, Bundle-Ether1)
- 'type': ''other'' by default; ''bridge'' if "bvi" in name;
    ''lag'' if "bundle" in name; ''virtual'' if "loopback" or "tunnel" in name
    or if the interface name contains a dot ('.')
- 'enabled': boolean; interfaces are 'True' by default unless explicitly
    shutdown in the config
- 'parent': parent interface name or 'null' (if the interface name contains
    a dot the parent is the part before the dot)
- 'lag_id': lag identifier integer (bundle id number) or 'null'
- 'lag_type': ''lag'' for bundle-ether port channels or 'null'
- 'lacp_mode': LACP mode string (e.g. ''active'', ''passive'') or 'null'
- 'lag': Name of parent LAG interface e.g. 'Bundle-Ether1' or 'null'
- 'mtu': integer MTU or 'null'
- 'mac_address': string MAC address in EUI format or 'null'
- 'speed': integer speed in kbit/s or 'null'
- 'duplex': string duplex setting or 'null'
- 'description': string (empty string when not set)
- 'mode': ''tagged'' when 'encapsulation dot1q' is present; ''access'' for BVI interfaces; 'null' otherwise
- 'untagged_vlan': integer VLAN derived from BVI interface name (e.g. BVI100 â†’ 100) or 'null'
- 'tagged_vlans': list with the dot1q VLAN integer when 'encapsulation dot1q' is present; empty list otherwise
- 'qinq_svlan': always 'null'
- 'vrf': string or 'null'
- 'ipv4_addresses': list of strings with IP/prefix (e.g. 10.0.0.1/30)
- 'ipv6_addresses': list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

'''yaml
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
'''

</doc>

<input>
commands = [
    "show running-config interface"
]
platform = [
    "cisco_xr",
    "iosxr",
]
</input>

<macro>
def transform_interfaces_to_records(data):
    from ttp_templates.utils.cisco_xr_process_show_running_config_interface import transform_interfaces_config
    return transform_interfaces_config(data)
</macro>

## ------------------------------------------------------------------------------------------
## Interfaces configuration
## ------------------------------------------------------------------------------------------
<group functions="contains('name')">
interface {{ name | _start_ }}
interface {{ name | _start_ | let("l2transport", True) }} l2transport
 description {{ description | re(".*") | default("") }}
 mtu {{ mtu | to_int }}
 service-policy input {{ qos_policy_in }}
 service-policy output {{ qos_policy_out }}
 encapsulation dot1q {{ dot1q | to_int | let("mode", "tagged") }}
 vrf {{ vrf }}
 bundle id {{ lag_id | to_int | let("lag_type", "lag") }} mode {{ lacp_mode }}
 lacp period {{ lacp_period }}
 shutdown {{ enabled | set(False) | default(True) }}
 rewrite ingress tag {{ rewrite_ingress_tag | PHRASE }}
 mac-address {{ mac_address | mac_eui }}
 duplex {{ duplex }}
 speed {{ speed | to_int }}
 
 <group name="ipv4_addresses*" method="table">
 ipv4 address {{ ip | _exact_ }} {{ mask }}
 ipv4 address {{ ip | _exact_ }} {{ mask }} secondary
 </group>
 
 <group name="ipv6_addresses*" method="table">
 ipv6 address {{ ip | _exact_ }}/{{ mask }}
 </group>

!{{ _end_ }}
</group>

<output macro="transform_interfaces_to_records"/>

</template>
```
</details>