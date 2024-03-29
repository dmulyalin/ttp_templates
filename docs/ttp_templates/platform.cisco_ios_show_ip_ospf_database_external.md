Reference path:
```
ttp://platform/cisco_ios_show_ip_ospf_database_external.txt
```

---



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



---

<details><summary>Template Content</summary>
```
<doc>
This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS devices.

This template parses external-lsa only out of output produced by 
"show ip ospf database external" command.

Caveats:

 - need 'ttp>=0.7.0', 'ttp==0.6.0' will not work due to bugs in it
 
Produces this structure for each input datum/device output:
'''
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
'''
</doc>

<group name="ospf_processes.{{ pid }}**">
            OSPF Router with ID ({{ local_rid }}) (Process ID {{ pid }})
			
<group name="external_lsa*" void="">
                Type-5 AS External Link States {{ _start_ }}
				
  <group>
  LS Type: AS External Link {{ _start_ }}
  Link State ID: {{ subnet }} (External Network Number )
  Advertising Router: {{ originator_rid }}
  Network Mask: /{{ mask }}
        Metric Type: {{ metric_type }} (Larger than any link state path)
        Metric: {{ metric }} 
        External Route Tag: {{ tag }}
{{ _end_ }}
  </group>
</group>
</group>
```
</details>