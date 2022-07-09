# cli_l2_data Templates

cli_l2_data templates designed to parse show commands output from networking devices into a
structured data for the use of N2G application to produce diagrams.

Results structure example:

```
{'cisco_ios': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                           'src_label': 'Ge4/6',
                                           'target': {'bottom_label': 'cisco WS-C6509',
                                                      'id': 'switch-2',
                                                      'top_label': '10.2.2.2'},
                                           'trgt_label': 'Ge1/5'},
                                          {'source': 'switch-1',
                                           'src_label': 'Ge4/7',
                                           'target': {'bottom_label': 'cisco WS-C6509',
                                                      'id': 'switch-2',
                                                      'top_label': '10.2.2.2'},
                                           'trgt_label': 'Ge1/6'}],
                            'interfaces': {'Ge1/1': {'description': 'switch-3:Gi0/1',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'lag_id': '11',
                                                     'lag_mode': 'active',
                                                     'mtu': '9216',
                                                     'state': {'admin': 'up',
                                                               'bw_kbits': '10000000',
                                                               'description': 'switch-3:Gi0/1',
                                                               'duplex': 'Full',
                                                               'hardware': 'Ten Gigabit Ethernet '
                                                                           'Port',
                                                               'is_physical_port': True,
                                                               'line': 'up',
                                                               'line_status': 'connected',
                                                               'link_speed': '10Gb/s',
                                                               'link_type': 'auto',
                                                               'mac': 'a89d.2163.1111',
                                                               'media_type': '10GBase-LR',
                                                               'mtu': '9216'},
                                                     'trunk_vlans': '101'}
                                           'Ge4/6': {'description': 'switch-2: trunk',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'lag_id': '3',
                                                     'lag_mode': 'active',
                                                     'trunk_vlans': '200,201,202,203,204,205'}
                                           'LAG11': {'description': 'switch-3: trunk LAG',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'trunk_vlans': '101'},
                                           'LAG3': {'description': 'switch-2: trunk LAG',
                                                    'is_l2': True,
                                                    'l2_mode': 'trunk',
                                                    'state': {'admin': 'up',
                                                              'bw_kbits': '20000000',
                                                              'description': 'switch-2: trunk LAG',
                                                              'duplex': 'Full',
                                                              'hardware': 'EtherChannel',
                                                              'lag_members': 'Ge4/6 Ge4/7',
                                                              'line': 'up',
                                                              'line_status': 'connected',
                                                              'link_type': '10Gb/s',
                                                              'mac': 'a89d.2163.3333',
                                                              'media_type': 'N/A',
                                                              'mtu': '1500'},
                            'node_facts': {'vlans': {'101': 'test_vlan', '200': 'ProdVMS'}}},
               'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                           'src_label': 'Ge1/5',
                                           'target': {'bottom_label': 'cisco WS-C6509',
                                                      'id': 'switch-1',
                                                      'top_label': '10.1.1.1'},
                                           'trgt_label': 'Ge4/6'},
                                          {'source': 'switch-2',
                                           'src_label': 'Ge1/6',
                                           'target': {'bottom_label': 'cisco WS-C6509',
                                                      'id': 'switch-1',
                                                      'top_label': '10.1.1.1'},
                                           'trgt_label': 'Ge4/7'}],
                            'interfaces': {'Ge1/5': {'description': 'switch-1: trunk',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'lag_id': '3',
                                                     'lag_mode': 'active',
                                                     'trunk_vlans': '200,201,202,203,204,205'}
                            'node_facts': {'vlans': {'101': 'test_vlan', '200': 'ProdVMS'}}}}}
```