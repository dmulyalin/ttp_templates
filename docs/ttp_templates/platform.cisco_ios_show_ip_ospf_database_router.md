Reference path:
```
ttp://platform/cisco_ios_show_ip_ospf_database_router.txt
```

---



This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses router-lsa only out of output produced by 
"show ip ospf database router" command.

Caveats:

 - need `ttp>=0.7.0`, `ttp==0.6.0` will not work due to bugs in it
 
Produces this structure for each input datum/device output:
```
[
    [
        {
            "ospf_processes": {
                "1": {
                    "local_rid": "10.0.0.4",
                    "router_lsa": [
                        {
                            "area": "0",
                            "asbr": False,
                            "bma_peers": [
                                {
                                    "link_data": "10.1.117.4",
                                    "link_id": "10.1.117.7",
                                    "metric": "10",
                                }
                            ],
                            "connected_stub": [
                                {
                                    "link_data": "255.255.255.128",
                                    "link_id": "10.1.14.0",
                                    "metric": "10",
                                }
                            ],
                            "originator_rid": "10.0.0.4",
                            "ptp_peers": [
                                {
                                    "link_data": "10.1.14.4",
                                    "link_id": "10.0.0.10",
                                    "metric": "10",
                                }
                            ],
                        }
                    ],
                }
            }
        }
    ]
]
```



---

<details><summary>Template Content</summary>
```
<doc>
This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses router-lsa only out of output produced by 
"show ip ospf database router" command.

Caveats:

 - need 'ttp>=0.7.0', 'ttp==0.6.0' will not work due to bugs in it
 
Produces this structure for each input datum/device output:
'''
[
    [
        {
            "ospf_processes": {
                "1": {
                    "local_rid": "10.0.0.4",
                    "router_lsa": [
                        {
                            "area": "0",
                            "asbr": False,
                            "bma_peers": [
                                {
                                    "link_data": "10.1.117.4",
                                    "link_id": "10.1.117.7",
                                    "metric": "10",
                                }
                            ],
                            "connected_stub": [
                                {
                                    "link_data": "255.255.255.128",
                                    "link_id": "10.1.14.0",
                                    "metric": "10",
                                }
                            ],
                            "originator_rid": "10.0.0.4",
                            "ptp_peers": [
                                {
                                    "link_data": "10.1.14.4",
                                    "link_id": "10.0.0.10",
                                    "metric": "10",
                                }
                            ],
                        }
                    ],
                }
            }
        }
    ]
]
'''
</doc>

<group name="ospf_processes.{{ pid }}**">
            OSPF Router with ID ({{ local_rid }}) (Process ID {{ pid }})
            
<group name="router_lsa*" functions="record('area') | del('area') | void">
                Router Link States (Area {{ area }}) 
				
  <group set="area">
  LS Type: Router Links {{ _start_ }}
  Advertising Router: {{ originator_rid }}
  AS Boundary Router {{ asbr | set(True) | default(False) }}
  
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