Reference path:
```
ttp://platform/huawei_display_ospf_lsdb_router.txt
```

---



This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Huawei devices.

This template parses router-lsa only out of output produced by 
"display ospf lsdb router" command.
 
Produces this structure for each input datum/device output:
```
[
    [
        {
            "ospf_processes": {
                "123": {
                    "local_rid": "123.123.24.158",
                    "router_lsa": [
                        {
                            "area": "0.0.0.123",
                            "connected_stub": [
                                {
                                    "link_data": "255.255.255.252",
                                    "link_id": "123.123.60.108",
                                    "metric": "1",
                                }
                            ],
                            "originator_rid": "10.123.0.92",
                            "ptp_peers": [
                                {
                                    "link_data": "123.123.60.109",
                                    "link_id": "123.123.24.31",
                                    "metric": "1",
                                },
                                {
                                    "link_data": "123.123.60.201",
                                    "link_id": "123.123.24.5",
                                    "metric": "9000",
                                },
                            ],
                        },
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
diagrams based on OSPF link state database of Huawei devices.

This template parses router-lsa only out of output produced by 
"display ospf lsdb router" command.
 
Produces this structure for each input datum/device output:
'''
[
    [
        {
            "ospf_processes": {
                "123": {
                    "local_rid": "123.123.24.158",
                    "router_lsa": [
                        {
                            "area": "0.0.0.123",
                            "connected_stub": [
                                {
                                    "link_data": "255.255.255.252",
                                    "link_id": "123.123.60.108",
                                    "metric": "1",
                                }
                            ],
                            "originator_rid": "10.123.0.92",
                            "ptp_peers": [
                                {
                                    "link_data": "123.123.60.109",
                                    "link_id": "123.123.24.31",
                                    "metric": "1",
                                },
                                {
                                    "link_data": "123.123.60.201",
                                    "link_id": "123.123.24.5",
                                    "metric": "9000",
                                },
                            ],
                        },
                    ],
                }
            }
        }
    ]
]
'''
</doc>

<group name="ospf_processes.{{ pid }}**">
{{ ignore(" +") }}  OSPF Process {{ pid }} with Router ID {{ local_rid }}

<group name="router_lsa*" functions="record('area') | del('area') | void">          
{{ ignore(" +") }}  Area: {{ area }}         
						  
  <group set="area">
  Type      : Router {{ _start_ }}
  Adv rtr   : {{ originator_rid }}
  
   <group name="{{ link_type }}*" contains="link_type">
   * Link ID: {{ link_id | _start_ }}
     Link ID: {{ link_id | _start_ }}
     Data   : {{ link_data }}
     Link Type: StubNet {{ link_type | set(connected_stub) }}
     Link Type: P-2-P {{ link_type | set(ptp_peers) }}
     Link Type: TransNet  {{ link_type | set(bma_peers) }}
     Metric : {{ metric }}
   </group>

  </group>
</group>
</group>
```
</details>