# Getter templates vendor support matrix.

| Getter template | A10 | Arista EOS | Cisco IOS | Cisco IOS-XR | Cisco NX-OS | Juniper Junos | Opengear | Linux |
|---|---|---|---|---|---|---|---|---|
| arp | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| bgp_neighbors | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| communities | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| inventory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| netbox | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| interfaces | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| interfaces_status | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| lldp_neighbors | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| mac-addresses | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| prefixes | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| vlans | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ |
| vrfs | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

## Notes

### bgp_neighbors

Collected commands by platform:

- Arista EOS: `show ip bgp neighbors vrf all | json`
- Cisco IOS-XR: `show bgp neighbors` or `show bgp vrf all neighbors`
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

### lldp_neighbors

Collected commands by platform:

- Arista EOS: `show lldp neighbors detail | json`
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
- Cisco NX-OS: `show running-config vrf`
- Juniper Junos: `show configuration routing-instances | display set`

### netbox

Collected commands by platform:

- Arista EOS: `show running-config`
- Cisco IOS-XR: `show running-config`
- Cisco NX-OS: `show running-config`
- Juniper Junos: `show configuration | display set`
- Opengear: `config -g config`
