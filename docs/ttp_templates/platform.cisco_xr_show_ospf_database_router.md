Reference path:
```
ttp://platform/cisco_xr_show_ospf_database_router.txt
```

---



This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS-XR devices.

This template parses router-lsa only out of output produced by 
"show ospf database router" command.

Caveats:

 - need `ttp>=0.7.0`, `ttp==0.6.0` will not work due to bugs in it
 
Produces this structure for each input datum/device output:
```
[[{'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'bma_peers': [{'link_data': '10.3.162.14',
                                                           'link_id': '10.3.162.13',
                                                           'metric': '1'}],
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.0',
                                                                'metric': '9100'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.61.1',
                                                           'link_id': '10.1.1.251',
                                                           'metric': '9100'}]},
                                           {'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.96',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.92',
                                            'ptp_peers': [{'link_data': '0.0.2.5',
                                                           'link_id': '10.1.2.6',
                                                           'metric': '1100'}]}]}}},
  {'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.204',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'}]},
                                           {'area': '0.0.0.1',
                                            'asbr': True,
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'}]}]}}}]]
```



---

<details><summary>Template Content</summary>
```
<doc>
This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS-XR devices.

This template parses router-lsa only out of output produced by 
"show ospf database router" command.

Caveats:

 - need 'ttp>=0.7.0', 'ttp==0.6.0' will not work due to bugs in it
 
Produces this structure for each input datum/device output:
'''
[[{'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'bma_peers': [{'link_data': '10.3.162.14',
                                                           'link_id': '10.3.162.13',
                                                           'metric': '1'}],
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.0',
                                                                'metric': '9100'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.61.1',
                                                           'link_id': '10.1.1.251',
                                                           'metric': '9100'}]},
                                           {'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.96',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.92',
                                            'ptp_peers': [{'link_data': '0.0.2.5',
                                                           'link_id': '10.1.2.6',
                                                           'metric': '1100'}]}]}}},
  {'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.204',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'}]},
                                           {'area': '0.0.0.1',
                                            'asbr': True,
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'}]}]}}}]]
'''
</doc>

<group name="ospf_processes.{{ pid }}**">
            OSPF Router with ID ({{ local_rid }}) (Process ID {{ pid | _start_ }})
            OSPF Router with ID ({{ local_rid }}) (Process ID {{ pid | _start_ }}, VRF {{ vrf }})

<group name="router_lsa*" functions="record('area') | del('area') | void">
                Router Link States (Area {{ area }})

  <group set="area">
  LS Type: Router Links {{ _start_ }}
  Advertising Router: {{ originator_rid }}
  Area Border Router {{ asbr | set(True) | default(False) }}

    <group name="ptp_peers*">
    Link connected to: another Router (point-to-point) {{ _start_ }}
     (Link ID) Neighboring Router ID: {{ link_id }}
     (Link Data) Router Interface address: {{ link_data }}
       TOS 0 Metrics: {{ metric }}
{{ _end_ }}
    </group>

    <group name="connected_stub*">
    Link connected to: a Stub Network {{ _start_ }}
     (Link ID) Network/subnet number: {{ link_id }}
     (Link Data) Network Mask: {{ link_data }}
       TOS 0 Metrics: {{ metric }}
{{ _end_ }}
    </group>

    <group name="bma_peers*">
    Link connected to: a Transit Network {{ _start_ }}
     (Link ID) Designated Router address: {{ link_id }}
     (Link Data) Router Interface address: {{ link_data }}
       TOS 0 Metrics: {{ metric }}
{{ _end_ }}
    </group>
  </group>
</group>
</group>
```
</details>