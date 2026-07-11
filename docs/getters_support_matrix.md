# Getter templates vendor support matrix.

| Getter template | A10 | Arista EOS | Cisco IOS-XR | Cisco NX-OS | Juniper Junos | Opengear | Linux |
|---|---|---|---|---|---|---|---|
| bgp_neighbors | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| inventory | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| netbox | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| interfaces | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| lldp_neighbors | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |

Notes:

- Cisco NX-OS inventory getter support uses `show inventory | json-pretty`.
- A10 inventory getter support uses `show hardware`.
