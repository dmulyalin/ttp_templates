# Getter templates vendor support matrix.

| Getter template | A10 | Arista EOS | Cisco IOS | Cisco IOS-XR | Cisco NX-OS | Juniper Junos | Opengear | Linux |
|---|---|---|---|---|---|---|---|---|
| bgp_neighbors | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| bgp_communities | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| inventory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| netbox | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| interfaces | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| interfaces_status | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| lldp_neighbors | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| vlans | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| vrfs | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| vrrp | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| mac_addresses | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| bgp_asn | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| prefixes | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| arp | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Notes

### bgp_asn

Collected commands by platform:

- Arista EOS: `show running-config section router bgp`
- Cisco IOS: `show running-config | section router bgp`
- Cisco IOS-XR: `show run formal | inc "local-as|remote-as"`
- Cisco NX-OS: `show running-config bgp`
- Juniper Junos: `show configuration | display set | match "autonomous-system|local-as|peer-as"`

### bgp_communities

Collected commands by platform:

- Arista EOS: `show running-config | include community-list`
- Cisco IOS: `show running-config | include community-list`
- Cisco IOS-XR: `show rpl community-set`, `show rpl extcommunity-set`, and `show rpl large-community-set`
- Cisco NX-OS: `show running-config rpm`
- Juniper Junos: `show configuration policy-options community | display set`

### bgp_neighbors

Collected commands by platform:

- A10: `show ip bgp neighbors`
- Arista EOS: `show ip bgp neighbors vrf all | json`
- Cisco IOS-XR: `show bgp neighbors` or `show bgp vrf all neighbors`
- Cisco NX-OS: `show ip bgp neighbors vrf all`
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
- Juniper Junos: `show configuration interfaces | display set` and `show configuration routing-instances | display set | match interface`
- Linux: `ip address show`

### interfaces_status

Collected commands by platform:

- A10: `show interfaces`
- Arista EOS: `show interfaces`
- Cisco IOS: `show interfaces`
- Cisco IOS-XR: `show interfaces`
- Cisco NX-OS: `show interface`
- Juniper Junos: `show interfaces`

### lldp_neighbors

Collected commands by platform:

- A10: `show lldp neighbors`
- Arista EOS: `show lldp neighbors detail | json`
- Cisco IOS-XR: `show lldp neighbors detail`
- Cisco NX-OS: `show lldp neighbors detail`
- Juniper Junos: `show lldp neighbors detail | display json`

### vlans

Collected commands by platform:

- Arista EOS: `show running-config section vlan`
- Cisco IOS: `show running-config | section vlan`
- Cisco NX-OS: `show running-config vlan`
- Juniper Junos: `show configuration vlans | display set`

### vrfs

Collected commands by platform:

- Arista EOS: `show running-config section vrf`
- Cisco IOS: `show running-config | section vrf`
- Cisco IOS-XR: `show running-config vrf`
- Cisco NX-OS: `show running-config | section "vrf context"`
- Juniper Junos: `show configuration routing-instances | display set`

### vrrp

Collected commands by platform:

- Cisco IOS-XR: `show running-config formal router vrrp`
- Juniper Junos: `show configuration | display set | match vrrp-group`

### netbox

Collected commands by platform:

- Arista EOS: `show running-config`
- Cisco IOS-XR: `show running-config`
- Cisco NX-OS: `show running-config`
- Juniper Junos: `show configuration | display set`
- Opengear: `config -g config`
