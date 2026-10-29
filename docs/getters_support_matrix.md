# Getter templates vendor support matrix.

| Getter template | A10 | Arista EOS | Cisco ASA | Cisco IOS | Cisco IOS-XR | Cisco NX-OS | Fortinet FortiOS | Juniper Junos | Opengear | Linux |
|---|---|---|---|---|---|---|---|---|---|---|
| bgp_neighbors | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| bgp_communities | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| inventory | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| netbox | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| interfaces | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| interfaces_status | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| lldp_neighbors | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| vlans | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| vrfs | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| vrrp | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| mac_addresses | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| bgp_asn | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| prefixes | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| arp | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| ping | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |

## Notes

### arp

Collected commands by platform, the IPv4 table, the IPv6 table and, where
those don't name the VRF, the interfaces' VRFs:

- Arista EOS: `show ip arp vrf all | json` and `show ipv6 neighbors vrf all | json`
- Cisco ASA: `show arp`, `show ipv6 neighbor` and `show nameif`
- Cisco IOS: `show ip arp` and `show ipv6 neighbors` for the global table; for a VRF,
  `show ip arp vrf NAME` and `show ipv6 neighbors vrf NAME`, parsed with
  `template_vars={"vrf": "NAME"}`
- Cisco IOS-XR: `show arp`, `show arp vrf all`, `show ipv6 neighbors`, `show ipv4 vrf all interface brief` and `show ipv6 vrf all interface brief`
- Cisco NX-OS: `show ip arp detail vrf all | json` and `show ipv6 neighbor vrf all | json`
- Fortinet FortiOS: `diagnose ip arp list`, `diagnose ipv6 neighbor-cache list` and `show system interface`
- Juniper Junos: `show arp no-resolve | display json`, `show ipv6 neighbors | display json` and `show route instance detail | display json`
- Linux: `ip -j -s neigh show` and `ip -j -d link show`

### bgp_asn

Collected commands by platform:

- A10: `show running-config partition-config all | inc router bgp` and `show running-config partition-config all | inc router remote-as`
- Arista EOS: `show running-config section router bgp`
- Cisco IOS: `show running-config | section router bgp`
- Cisco IOS-XR: `show run formal | inc "local-as|remote-as"`
- Cisco NX-OS: `show running-config bgp`
- Juniper Junos: `show configuration | display inheritance | display set | match "autonomous-system|local-as|peer-as"`

### bgp_communities

Collected commands by platform:

- Arista EOS: `show running-config | include community-list`
- Cisco IOS: `show running-config | include community-list`
- Cisco IOS-XR: `show rpl community-set`, `show rpl extcommunity-set`, `show rpl large-community-set`, and `show running-config formal  | inc route-target`
- Cisco NX-OS: `show running-config rpm`
- Juniper Junos: `show configuration | display inheritance | display set | match "policy-options community"` and `show configuration routing-instances | display inheritance | display set | match "vrf-target|instance-type"`

### bgp_neighbors

Collected commands by platform:

- A10: `show ip bgp neighbors`
- Arista EOS: `show ip bgp neighbors vrf all | json`
- Cisco ASA: `show bgp neighbors`, `show bgp ipv6 unicast neighbors` and `show running-config router bgp`
- Cisco IOS: `show ip bgp all neighbors` and `show running-config | section bgp`
- Cisco IOS-XR: `show bgp neighbors` or `show bgp vrf all neighbors`, and `show run formal router bgp | inc neighbor`
- Cisco NX-OS: `show ip bgp neighbors vrf all` and `show running-config section bgp`
- Fortinet FortiOS: `get router info bgp neighbors`
- Juniper Junos: `show bgp neighbor | display json`

### inventory

Collected commands by platform:

- A10: `show hardware`
- Arista EOS: `show inventory | json`
- Cisco IOS: `show inventory`
- Cisco IOS-XR: `show inventory`
- Cisco NX-OS: `show inventory | json-pretty`
- Juniper Junos: `show chassis hardware | display json`

### interfaces

Collected commands by platform:

- A10: `show running-config partition-config all | section interface`
- Arista EOS: `show running-config section interface`
- Cisco IOS: `show running-config | section interface`
- Cisco IOS-XR: `show running-config interface`, `show running-config router vrrp`, and `show running-config router hsrp`
- Cisco NX-OS: `show running-config interface`
- Juniper Junos: `show configuration interfaces | display inheritance | display set` and `show configuration routing-instances | display inheritance | display set | match interface`
- Linux: `ip address show`

### interfaces_status

Collected commands by platform:

- A10: `show interfaces`
- Arista EOS: `show interfaces`
- Cisco ASA: `show interface`
- Cisco IOS: `show interfaces`
- Cisco IOS-XR: `show interfaces`
- Cisco NX-OS: `show interface`
- Juniper Junos: `show interfaces`

### lldp_neighbors

Collected commands by platform:

- A10: `show lldp neighbors`
- Arista EOS: `show lldp neighbors detail | json`
- Cisco IOS: `show lldp neighbors detail`
- Cisco IOS-XR: `show lldp neighbors detail`
- Cisco NX-OS: `show lldp neighbors detail`
- Juniper Junos: `show lldp neighbors detail | display json`

### ping

Collected command, followed by the destination and options:

- Arista EOS: `ping`
- Cisco ASA: `ping`
- Cisco IOS: `ping`
- Cisco NX-OS: `ping` or `ping6`
- Linux: `ping -c 5`

### vlans

Collected commands by platform:

- Arista EOS: `show run section vlan`
- Cisco IOS: `show running-config | section vlan` and `show running-config | section interface`
- Cisco IOS-XR: `show run formal interface | inc "encapsulation|BVI"`
- Cisco NX-OS: `show running-config vlan` and `show running-config interface`
- Juniper Junos: `show configuration vlans | display inheritance | display set` and `show configuration interfaces | display inheritance | display set | match "vlan|interface-mode|irb"`

### vrfs

Collected commands by platform:

- Arista EOS: `show running-config section vrf`
- Cisco IOS: `show running-config vrf`
- Cisco IOS-XR: `show running-config vrf` and `show run formal interface | inc vrf`
- Cisco NX-OS: `show running-config | section "vrf context"` and `show run interface | include "interface|vrf"`
- Juniper Junos: `show configuration routing-instances | display inheritance | display set`

### vrrp

Collected commands by platform:

- Arista EOS: `show running-config section vrrp`
- Cisco IOS-XR: `show running-config formal router vrrp`
- Cisco NX-OS: `show running-config vrrp` or `show running-config vrrpv3`
- Juniper Junos: `show configuration | display inheritance | display set | match vrrp`

### netbox

Collected commands by platform:

- Arista EOS: `show running-config`
- Cisco IOS-XR: `show running-config`
- Cisco NX-OS: `show running-config`
- Juniper Junos: `show configuration | display inheritance | display set`
- Opengear: `config -g config`
