Reference path:
```
ttp://get/bgp_neighbors.txt
```

---



Normalizes Arista EOS BGP neighbors JSON to flat list format.

Transforms nested vrfs-peerList structure into standardized dictionaries with:

- All fields present (missing set to None)
- RFC-normalized state values (established, idle, etc.)
- Per-AFI prefix counts (ipv4Unicast_prefixes_sent, etc.)
- Consistent field naming

Example normalized output (YAML):

```yaml
- afi:
  - ipv4_unicast
  description: ceos-leaf-1 Ethernet1
  export_policies: ALLOW-ALL
  hold_time: 180
  import_policies: ALLOW-ALL
  ipv4_unicast_prefixes_received: 2
  ipv4_unicast_prefixes_sent: 3
  keepalive: 60
  local_address: 10.0.0.0
  local_as: '65001'
  local_interface: Ethernet2
  max_ttl: 255
  name: default_10.0.0.1
  peer_group: null
  peering_type: external
  prefix_list_in: null
  prefix_list_out: null
  remote_address: 10.0.0.1
  remote_as: '65101'
  router_id: 10.10.10.11
  state: established
  uptime_seconds: 8791
  vrf: default
```



Normalizes Juniper JunOS BGP neighbors JSON to flat list format.

Transforms the nested bgp-information/bgp-peer structure returned by
'show bgp neighbor | display json' into standardized dictionaries with:

- All fields present (missing set to None)
- RFC-normalized state values (established, idle, etc.)
- Per-AFI prefix counts (ipv4_unicast_prefixes_sent, etc.)
- VRF name normalized ('master' -> 'default')
- Peer/local addresses stripped of port suffix (e.g. '10.0.0.1+179' -> '10.0.0.1')
- Consistent field naming matching the Arista EOS BGP neighbor output format

Example normalized output (YAML):

```yaml
- afi:
  - ipv4_unicast
  description: null
  export_policies:
  - ALLOW-10_8
  - ALLOW-ALL
  hold_time: 90
  import_policies:
  - ALLOW-10_8
  - ALLOW-ALL
  ipv4_unicast_prefixes_received: 5
  ipv4_unicast_prefixes_sent: 2
  keepalive: 30
  local_address: 10.10.0.15
  local_as: '65104'
  local_interface: ge-0/0/0.0
  max_ttl: null
  name: default_10.10.0.14
  peer_group: CLOS
  peering_type: external
  prefix_list_in: null
  prefix_list_out: null
  remote_address: 10.10.0.14
  remote_as: '65002'
  router_id: 10.10.10.2
  state: established
  uptime_seconds: null
  vrf: default
```



Template to parse Cisco IOS XR BGP neighbors.

This template requires output of 'show bgp neighbors' command.

Returns a normalized list of dictionaries, one per BGP neighbor, with the
following keys (fields unavailable from this command are set to None/[]):

```yaml
- afi:
  - ipv4_unicast
  - ipv6_unicast
  description: iBGP_Neighbor
  export_policies:
  - PASS-ALL
  hold_time: 180
  import_policies:
  - DENY-ALL
  ipv4_unicast_prefixes_received: 0
  ipv4_unicast_prefixes_sent: 0
  ipv6_unicast_prefixes_received: 0
  ipv6_unicast_prefixes_sent: 0
  keepalive: 60
  local_address: 10.0.0.1
  local_as: '65001'
  local_interface: null
  max_ttl: null
  name: default_10.0.0.42
  peer_group: null
  peering_type: internal
  prefix_list_in: null
  prefix_list_out: null
  remote_address: 10.0.0.42
  remote_as: '65001'
  router_id: 0.0.0.0
  state: opensent
  uptime_seconds: null
  vrf: default
```



---

<details><summary>Template Content</summary>
```
<template name="bgp_neighbors" results="per_template">
<doc>
Getter template to parse inventory for network devices. Designed to work with 
[Network Automation Fabric](https://docs.norfablabs.com/) 
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/) 
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Arista EOS
- Juniper Junos
- Cisco IOS XR

Returns normalized list of dictionaries, each dictionary has these keys:

- 'name' - unique neighbor identifier composed as 'vrf_remote_address'
- 'vrf' - VRF the BGP session belongs to
- 'state' - BGP session state (idle, connect, active, opensent, openconfirm, established)
- 'peering_type' - peering relationship type: 'external' or 'internal'
- 'remote_address' - IP address of the remote BGP peer
- 'remote_as' - AS number of the remote peer
- 'local_address' - local BGP update-source IP address
- 'local_as' - local AS number
- 'local_interface' - local interface used for the BGP session
- 'router_id' - router ID of the remote peer
- 'peer_group' - BGP peer-group name the neighbor belongs to, or 'null'
- 'description' - neighbor description string, or 'null'
- 'hold_time' - negotiated BGP hold-time in seconds
- 'keepalive' - negotiated BGP keepalive interval in seconds
- 'uptime' - session uptime in seconds (time since last transition to Established)
- 'max_ttl' - maximum TTL hops configured (relevant for eBGP multihop)
- 'afi' - list of IANA AFI/SAFI names negotiated for this session (e.g. 'ipv4_unicast', 'l2vpn_evpn')
- 'import_policies' - inbound route-map name, or 'null' if none configured
- 'export_policies' - outbound route-map name, or 'null' if none configured
- 'prefix_list_in' - inbound prefix-list name, or 'null' if none configured
- 'prefix_list_out' - outbound prefix-list name, or 'null' if none configured
- 'afi_prefixes_sent' - number of prefixes advertised for each negotiated AFI/SAFI (e.g. 'ipv4_unicast_prefixes_sent')
- 'afi_prefixes_received' - number of prefixes received for each negotiated AFI/SAFI (e.g. 'ipv4_unicast_prefixes_received')

</doc>

<extend template="ttp://platform/arista_eos_show_bgp_neighbors_vrf_all_pipe_json.txt"/>

<extend template="ttp://platform/juniper_junos_show_bgp_neighbor_pipe_display_json.txt"/>

<extend template="ttp://platform/cisco_xr_show_bgp_neighbors.txt"/>

</template>
```
</details>