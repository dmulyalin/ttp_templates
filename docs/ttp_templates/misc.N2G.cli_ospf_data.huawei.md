Reference path:
```
ttp://misc/N2G/cli_ospf_data/huawei.txt
```

---



Template to parse Huawei devices OSPF database content.


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
Template to parse Huawei devices OSPF database content.
</doc>

<input load="python">
commands = [
    "display ospf lsdb router",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["huawei", "huawei_vrpv8"]
</input>

<extend template="ttp://platform/huawei_display_ospf_lsdb_router.txt"/>
```
</details>