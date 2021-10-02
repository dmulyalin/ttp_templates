Reference path:
```
ttp://misc.N2G.isis_lsdb.Cisco_IOSXR.txt
```

---



This template designed for use with N2G library to produce network diagrams based on ISIS 
link state database of Cisco IOS-XR devices. 

Caveats:
 - need ttp>=0.8.0 for extend to work


Template to parse ISIS LSDP of Cisco IOS-XR devices as produced
by "show isis database verbose" command.

This template produces this structure:

[[{'isis_processes': {'100': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '9',
                                                  'local_ip': '10.123.0.17',
                                                  'metric': '16777214',
                                                  'peer_intf_id': '50',
                                                  'peer_ip': '10.123.0.18',
                                                  'peer_name': 'R1-X2'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.1/32'}],
                                       'rid': '10.111.1.1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '48',
                                                  'local_ip': '10.123.0.33',
                                                  'metric': '456',
                                                  'peer_intf_id': '53',
                                                  'peer_ip': '10.123.0.34',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.2/32'}],
                                       'rid': '10.111.1.2'}]},
                      '200': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '57',
                                                  'peer_name': 'R2-X1'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': 'fddd:2:c101::1/128'},,
                                       'rid': 'fddd:2:c101::1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '60',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': 'fdff::/36'}],
                                       'rid': 'fddd:2:c101::2'}]}}}]]



---

<details><summary>Template Content</summary>
```
<doc>
This template designed for use with N2G library to produce network diagrams based on ISIS 
link state database of Cisco IOS-XR devices. 

Caveats:
 - need ttp>=0.8.0 for extend to work
</doc>

<input load="python">
# Starting with Netmiko 3.4.0 can use run_ttp method to populate this template with below commands output
commands = [
    "show isis database verbose",
]
</input>

<extend template="ttp://platform/cisco_xr_show_isis_database_verbose.txt"/>
```
</details>