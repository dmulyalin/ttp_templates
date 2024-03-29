Reference path:
```
ttp://platform/cisco_ios_show_ip_ospf_database_summary.txt
```

---



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
This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses summary-lsa only out of output produced by 
"show ip ospf database summary" command.

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
'''
</doc>

<group name="ospf_processes.{{ pid }}**">
            OSPF Router with ID ({{ local_rid }}) (Process ID {{ pid }})
			
<group name="summary_lsa*" functions="record('area') | del('area') | void">
                Summary Net Link States (Area {{ area }})

  <group set="area">
  LS Type: Summary Links(Network) {{ _start_ }}
  Link State ID: {{ subnet }} (summary Network Number)
  Advertising Router: {{ originator_rid }}
  Network Mask: /{{ mask }}
        MTID: 0         Metric: {{ metric }} 
{{ _end_ }}        
  </group>
</group>
		
</group>
```
</details>