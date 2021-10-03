Reference path:
```
ttp://misc.N2G.ospf_lsdb.Cisco_IOS.txt
```

---



This template designed for use with N2G library to produce network diagrams based on OSPF 
link state database of Cisco IOS-XR devices. 

Caveats:

 - need `ttp>=0.8.0` for extend to work


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


This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses external-lsa only out of output produced by 
"show ip ospf database external" command.

Caveats:

 - need `ttp>=0.7.0`, `ttp==0.6.0` will not work due to bugs in it
 
Produces this structure for each input datum/device output:
```
[
    [
        {
            "ospf_processes": {
                "1": {
                    "external_lsa": [
                        {
                            "mask": "32",
                            "metric": "20",
                            "metric_type": "2",
                            "originator_rid": "10.0.0.10",
                            "subnet": "10.0.0.100",
                            "tag": "0",
                        }
                    ],
                    "local_rid": "10.0.0.4",
                }
            }
        }
    ]
]
```


This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses summary-lsa only out of output produced by 
"show ip ospf database summary" command.

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
                    "summary_lsa": [
                        {
                            "area": "0",
                            "mask": "31",
                            "metric": "10",
                            "originator_rid": "10.0.0.4",
                            "subnet": "10.1.45.2",
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
This template designed for use with N2G library to produce network diagrams based on OSPF 
link state database of Cisco IOS-XR devices. 

Caveats:

 - need 'ttp>=0.8.0' for extend to work
</doc>

<extend template="ttp://platform/cisco_ios_show_ip_ospf_database_router.txt"/>
<extend template="ttp://platform/cisco_ios_show_ip_ospf_database_external.txt"/>
<extend template="ttp://platform/cisco_ios_show_ip_ospf_database_summary.txt"/>
```
</details>