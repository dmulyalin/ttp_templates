Reference path:
```
ttp://misc/N2G/cli_isis_data/cisco_xr.txt
```

---



Template to parse Cisco IOSXR "show isis database verbose" output.


Template to parse ISIS LSDB of Cisco IOS-XR devices out of 
"show isis database verbose" command output.

This template produces this structure:
```
[[{'isis_processes': {'100': {'R1-X1': [{'isis_area': '49.0001',
                                         'level': 'Level-2',
                                         'links': [{'affinity': '0x00000000',
                                                    'bw_kbit': '10000000',
                                                    'isis_pid': '100',
                                                    'local_intf_id': '9',
                                                    'local_ip': '10.123.0.17',
                                                    'metric': '16777214',
                                                    'peer_intf_id': '50',
                                                    'peer_ip': '10.123.0.18',
                                                    'peer_name': 'R1-X2'},
                                                   {'affinity': '0x00000000',
                                                    'bw_kbit': '10000000',
                                                    'isis_pid': '100',
                                                    'local_intf_id': '7',
                                                    'local_ip': '10.123.0.25',
                                                    'metric': '123',
                                                    'peer_intf_id': '53',
                                                    'peer_ip': '10.123.0.26',
                                                    'peer_name': 'R2-X1'}],
                                         'networks': [{'isis_pid': '100',
                                                       'metric': '0',
                                                       'network': '10.111.1.1/32'}],
                                         'rid': '10.111.1.1'}]}}}]]
```



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse Cisco IOSXR "show isis database verbose" output.
</doc>

<input load="python">
# Starting with Netmiko 3.4.0 can use run_ttp method to populate this template with below commands output
commands = [
    "show isis database verbose",
]
platform = ["cisco_xr"]
</input>

<extend template="ttp://platform/cisco_xr_show_isis_database_verbose.txt"/>
```
</details>