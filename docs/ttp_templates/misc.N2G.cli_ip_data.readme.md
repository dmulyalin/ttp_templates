# cli_ip_data Templates

cli_ip_data templates designed to parse show commands output from networking devices into a
structured data for the use of N2G application to produce diagrams.

Parsing results example:

```
{'cisco_ios': {'switch_1': {'interfaces': {'SVI123': {'arp': [{'age': '-',
                                                               'ip': '10.123.111.1',
                                                               'mac': 'd094.6643.1111',
                                                               'type': 'ARPA'}],
                                                      'ip_addresses': [{'ip': '10.123.111.1',
                                                                        'netmask': '24',
                                                                        'network': '10.123.111.0/24'},
                                                                       {'ip': '10.123.222.1',
                                                                        'netmask': '24',
                                                                        'network': '10.123.222.0/24'}],
                                                      'port_description': 'Workstations Vlan',
                                                      'vrf': 'CORP'}}},
               'switch_2': {'interfaces': {'SVI11': {'ip_addresses': [{'ip': '10.11.11.1',
                                                                       'netmask': '24',
                                                                       'network': '10.11.11.0/24'}],
                                                     'port_description': 'Workstations Vlan'},
                                           'SVI22': {'arp': [{'age': '-',
                                                              'ip': '10.22.22.1',
                                                              'mac': 'd094.7890.1111',
                                                              'type': 'ARPA'},
                                                             {'age': '106',
                                                              'ip': '10.22.22.4',
                                                              'mac': 'd867.7890.1444',
                                                              'type': 'ARPA'}],
                                                     'ip_addresses': [{'ip': '10.22.22.1',
                                                                       'netmask': '24',
                                                                       'network': '10.22.22.0/24'}],
                                                     'port_description': 'Workstations Vlan'},
                                           'Te1/1/71': {'arp': [{'age': '5',
                                                                 'ip': '10.1.234.1',
                                                                 'mac': 'd867.d9b7.1111',
                                                                 'type': 'ARPA'}],
                                                        'fhrp': [{'hsrp_group': '1',
                                                                 'vip': '10.1.234.1.99',
                                                                 'type': 'hsrp'}],
                                                        'ip_addresses': [{'ip': '10.1.234.2',
                                                                          'netmask': '24',
                                                                          'network': '10.1.234.0/24'}],
                                                        'port_description': 'to SWITCH_2 shared '
                                                                            'subnet'}}}}}
```

Parsing results schema:

TBD