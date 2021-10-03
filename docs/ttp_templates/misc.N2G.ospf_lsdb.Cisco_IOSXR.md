Reference path:
```
ttp://misc.N2G.ospf_lsdb.Cisco_IOSXR.txt
```

---



This template designed for use with N2G library to produce network diagrams based on OSPF 
link state database of Cisco IOS-XR devices. 

Caveats:

 - need `ttp>=0.8.0` for extend to work


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


This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS-XR devices.

This template parses external-lsa only out of output produced by 
"show ospf database external" command.

Caveats:

 - need `ttp>=0.7.0`, `ttp==0.6.0` will not work due to bugs in it
 
Produces this structure for each input datum/device output:
```
[[{'ospf_processes': {'1': {'external_lsa': [{'mask': '0',
                                              'metric': '1',
                                              'metric_type': '2',
                                              'originator_rid': '10.3.22.190',
                                              'subnet': '0.0.0.0',
                                              'tag': '10'},
                                             {'mask': '0',
                                              'metric': '1',
                                              'metric_type': '2',
                                              'originator_rid': '10.3.25.22',
                                              'subnet': '0.0.0.0',
                                              'tag': '10'},
                                             {'mask': '8',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.3.20.95',
                                              'subnet': '10.0.0.0',
                                              'tag': '0'}],
                            'local_rid': '10.1.2.2'}},
   'vars': {'hostname': 'router-1'}}]]
```


This template initially designed for use with N2G library to produce network 
diagrams based on OSPF link state database of Cisco IOS-XR devices.

This template parses external-lsa only out of output produced by 
"show ospf database external" command.

Caveats:

 - need `ttp>=0.7.0`, `ttp==0.6.0` will not work due to bugs in it
 
Produces this structure for each input datum/device output:
```
[[{'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'summary_lsa': [{'area': '0.0.0.0',
                                             'mask': '32',
                                             'metric': '2312',
                                             'originator_rid': '10.0.24.1',
                                             'subnet': '10.1.0.1'},
                                            {'area': '0.0.0.0',
                                             'mask': '32',
                                             'metric': '1806',
                                             'originator_rid': '10.0.24.2',
                                             'subnet': '10.1.0.1'},
                                            {'area': '0.0.0.0',
                                             'mask': '32',
                                             'metric': '1312',
                                             'originator_rid': '10.0.25.192',
                                             'subnet': '10.1.0.1'},
                                            {'area': '0.0.0.0',
                                             'mask': '32',
                                             'metric': '806',
                                             'originator_rid': '10.0.25.193',
                                             'subnet': '10.1.0.1'},
                                            {'area': '0.0.0.32',
                                             'mask': '32',
                                             'metric': '2312',
                                             'originator_rid': '10.0.24.1',
                                             'subnet': '10.1.0.1'}]}},
   'vars': {'hostname': 'router-1'}}]]
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

<input load="python">
# Starting with Netmiko 3.4.0 can use run_ttp method to populate this template with below commands output
commands = [
    "show ospf database router",
    "show ospf database summary",
    "show ospf database external",
]
kwargs = {"strip_prompt": False}
method = "send_command"
</input>

<extend template="ttp://platform/cisco_xr_show_ospf_database_router.txt"/>
<extend template="ttp://platform/cisco_xr_show_ospf_database_external.txt"/>
<extend template="ttp://platform/cisco_xr_show_ospf_database_summary.txt"/>
```
</details>