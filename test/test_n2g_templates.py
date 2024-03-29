import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp
from ttp_templates.ttp_vars import all_vars

# Custom TTP functions to use in templates:
def add_network(data):
    if "netmask" in data:
        ip_obj, _ = _ttp_["match"]["to_ip"]("{}/{}".format(data["ip"], data["netmask"]))
    else:
        ip_obj, _ = _ttp_["match"]["to_ip"](data["ip"])
    data["network"] = str(ip_obj.network)
    data["netmask"] = str(ip_obj.network.prefixlen)
    return data, None
    
def test_N2G_ospf_lsdb_Cisco_IOSXR():
    with open("./mock_data/cisco_xr_show_ip_ospf_database_router_external_summary_router-1.txt", "r") as f:
        data1 = f.read()
    with open("./mock_data/cisco_xr_show_ip_ospf_database_router_external_summary_router-2.txt", "r") as f:
        data2 = f.read()
    template = get_template(path="misc/N2G/cli_ospf_data/cisco_xr.txt")
    # print(template)
    parser = ttp(template=template)
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [[{'ospf_processes': {'1': {'external_lsa': [{'mask': '0',
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
                                              'tag': '0'},
                                             {'mask': '24',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.3.22.83',
                                              'subnet': '10.0.2.0',
                                              'tag': '0'}],
                            'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'bma_peers': [{'link_data': '10.3.162.14',
                                                           'link_id': '10.3.162.13',
                                                           'metric': '1'},
                                                          {'link_data': '10.3.162.10',
                                                           'link_id': '10.3.162.9',
                                                           'metric': '1'}],
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.0',
                                                                'metric': '9100'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.61.1',
                                                           'link_id': '10.1.1.251',
                                                           'metric': '9100'},
                                                          {'link_data': '10.0.61.94',
                                                           'link_id': '10.1.2.6',
                                                           'metric': '65535'},
                                                          {'link_data': '0.0.1.220',
                                                           'link_id': '10.1.2.7',
                                                           'metric': '3000'}]},
                                           {'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.61.96',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.92',
                                            'ptp_peers': [{'link_data': '0.0.2.5',
                                                           'link_id': '10.1.2.6',
                                                           'metric': '1100'},
                                                          {'link_data': '0.0.2.67',
                                                           'link_id': '10.1.2.8',
                                                           'metric': '3000'},
                                                          {'link_data': '0.0.2.69',
                                                           'link_id': '10.1.2.7',
                                                           'metric': '3000'}]}],
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
                                             'subnet': '10.1.0.1'}]}}},
  {'ospf_processes': {'1': {'local_rid': '10.1.2.2',
                            'router_lsa': [{'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.204',
                                                                'metric': '9000'},
                                                               {'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.196',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'},
                                                          {'link_data': '10.0.60.197',
                                                           'link_id': '10.1.0.92',
                                                           'metric': '9000'}]},
                                           {'area': '0.0.0.0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.108',
                                                                'metric': '1'},
                                                               {'link_data': '255.255.255.252',
                                                                'link_id': '10.0.60.200',
                                                                'metric': '9000'}],
                                            'originator_rid': '10.1.0.92',
                                            'ptp_peers': [{'link_data': '10.0.60.109',
                                                           'link_id': '10.0.24.31',
                                                           'metric': '1'},
                                                          {'link_data': '10.0.60.201',
                                                           'link_id': '10.0.24.5',
                                                           'metric': '9000'}]},
                                           {'area': '0.0.0.1',
                                            'asbr': True,
                                            'originator_rid': '10.1.0.91',
                                            'ptp_peers': [{'link_data': '10.0.60.206',
                                                           'link_id': '10.0.24.6',
                                                           'metric': '9000'}]}],
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
                                             'subnet': '10.1.0.1'}]},
                      '10': {'external_lsa': [{'mask': '0',
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
                                               'tag': '0'},
                                              {'mask': '24',
                                               'metric': '20',
                                               'metric_type': '2',
                                               'originator_rid': '10.3.22.83',
                                               'subnet': '10.0.2.0',
                                               'tag': '0'}],
                             'local_rid': '10.3.22.75'}}}]]

# test_N2G_ospf_lsdb_Cisco_IOSXR()

def test_N2G_ospf_lsdb_Cisco_IOS():
    with open("./mock_data/cisco_ios_show_ip_ospf_database_router_external_summary_IOL4_ABR.txt", "r") as f:
        data = f.read()
    template = get_template(path="misc/N2G/cli_ospf_data/Cisco_IOS.txt")
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)    
    assert res == [[{'ospf_processes': {'1': {'external_lsa': [{'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.0.10',
                                              'subnet': '10.0.0.100',
                                              'tag': '0'},
                                             {'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.0.10',
                                              'subnet': '10.0.0.101',
                                              'tag': '0'},
                                             {'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.0.10',
                                              'subnet': '10.0.0.102',
                                              'tag': '0'},
                                             {'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.0.10',
                                              'subnet': '10.0.0.103',
                                              'tag': '0'},
                                             {'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.5.101',
                                              'subnet': '10.0.5.100',
                                              'tag': '0'},
                                             {'mask': '32',
                                              'metric': '20',
                                              'metric_type': '2',
                                              'originator_rid': '10.0.5.101',
                                              'subnet': '10.0.5.101',
                                              'tag': '0'}],
                            'local_rid': '10.0.0.4',
                            'router_lsa': [{'area': '0',
                                            'asbr': False,
                                            'bma_peers': [{'link_data': '10.1.117.3',
                                                           'link_id': '10.1.117.7',
                                                           'metric': '10'}],
                                            'originator_rid': '10.0.0.3'},
                                           {'area': '0',
                                            'asbr': False,
                                            'bma_peers': [{'link_data': '10.1.117.4',
                                                           'link_id': '10.1.117.7',
                                                           'metric': '10'}],
                                            'connected_stub': [{'link_data': '255.255.255.128',
                                                                'link_id': '10.1.14.0',
                                                                'metric': '10'}],
                                            'originator_rid': '10.0.0.4',
                                            'ptp_peers': [{'link_data': '10.1.14.4',
                                                           'link_id': '10.0.0.10',
                                                           'metric': '10'}]},
                                           {'area': '0',
                                            'asbr': False,
                                            'bma_peers': [{'link_data': '10.1.117.7',
                                                           'link_id': '10.1.117.7',
                                                           'metric': '10'}],
                                            'connected_stub': [{'link_data': '255.255.255.255',
                                                                'link_id': '10.0.0.7',
                                                                'metric': '1'},
                                                               {'link_data': '255.255.255.252',
                                                                'link_id': '10.1.107.0',
                                                                'metric': '10'},
                                                               {'link_data': '255.255.255.0',
                                                                'link_id': '10.1.37.0',
                                                                'metric': '10'}],
                                            'originator_rid': '10.0.0.7',
                                            'ptp_peers': [{'link_data': '10.1.107.2',
                                                           'link_id': '10.0.0.10',
                                                           'metric': '10'}]},
                                           {'area': '0',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.255',
                                                                'link_id': '10.0.0.10',
                                                                'metric': '1'},
                                                               {'link_data': '255.255.255.252',
                                                                'link_id': '10.1.107.0',
                                                                'metric': '10'},
                                                               {'link_data': '255.255.255.128',
                                                                'link_id': '10.1.14.0',
                                                                'metric': '10'}],
                                            'originator_rid': '10.0.0.10',
                                            'ptp_peers': [{'link_data': '10.1.107.1',
                                                           'link_id': '10.0.0.7',
                                                           'metric': '10'},
                                                          {'link_data': '10.1.14.1',
                                                           'link_id': '10.0.0.4',
                                                           'metric': '10'}]},
                                           {'area': '100',
                                            'asbr': False,
                                            'connected_stub': [{'link_data': '255.255.255.254',
                                                                'link_id': '10.1.45.2',
                                                                'metric': '10'}],
                                            'originator_rid': '10.0.0.4',
                                            'ptp_peers': [{'link_data': '10.1.45.2',
                                                           'link_id': '10.0.5.101',
                                                           'metric': '10'}]},
                                           {'area': '100',
                                            'asbr': True,
                                            'connected_stub': [{'link_data': '255.255.255.254',
                                                                'link_id': '10.1.45.2',
                                                                'metric': '10'}],
                                            'originator_rid': '10.0.5.101',
                                            'ptp_peers': [{'link_data': '10.1.45.3',
                                                           'link_id': '10.0.0.4',
                                                           'metric': '10'}]}],
                            'summary_lsa': [{'area': '0',
                                             'mask': '31',
                                             'metric': '10',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.1.45.2'},
                                            {'area': '100',
                                             'mask': '32',
                                             'metric': '11',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.0.0.7'},
                                            {'area': '100',
                                             'mask': '32',
                                             'metric': '11',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.0.0.10'},
                                            {'area': '100',
                                             'mask': '25',
                                             'metric': '10',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.1.14.0'},
                                            {'area': '100',
                                             'mask': '24',
                                             'metric': '20',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.1.37.0'},
                                            {'area': '100',
                                             'mask': '30',
                                             'metric': '20',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.1.107.0'},
                                            {'area': '100',
                                             'mask': '24',
                                             'metric': '10',
                                             'originator_rid': '10.0.0.4',
                                             'subnet': '10.1.117.0'}]}}}]]
   
# test_N2G_ospf_lsdb_Cisco_IOS()


def test_N2G_ospf_lsdb_huawei():
    with open("./mock_data/huawei_display_ospf_lsdb_router.txt", "r") as f:
        data = f.read()
    template = get_template(path="misc/N2G/cli_ospf_data/Huawei.txt")
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)    
    assert res == [[{'ospf_processes': {'123': {'local_rid': '123.123.24.158',
                              'router_lsa': [{'area': '0.0.0.123',
                                              'originator_rid': '10.123.0.91',
                                              'ptp_peers': [{'link_data': '123.123.60.206',
                                                             'link_id': '123.123.24.6',
                                                             'metric': '9000'},
                                                            {'link_data': '123.123.1.220',
                                                             'link_id': '10.123.2.7',
                                                             'metric': '3000'}]},
                                             {'area': '0.0.0.123',
                                              'connected_stub': [{'link_data': '255.255.255.252',
                                                                  'link_id': '123.123.60.108',
                                                                  'metric': '1'}],
                                              'originator_rid': '10.123.0.92',
                                              'ptp_peers': [{'link_data': '123.123.60.109',
                                                             'link_id': '123.123.24.31',
                                                             'metric': '1'},
                                                            {'link_data': '123.123.60.201',
                                                             'link_id': '123.123.24.5',
                                                             'metric': '9000'}]}]}}}]]
                                                             
# test_N2G_ospf_lsdb_huawei()

def test_N2G_isis_lsdb_juniper():
    with open("./mock_data/juniper_show_isis_database_verbose_pipe_no_more.txt", "r") as f:
        data = f.read()
    template = get_template(path="misc/N2G/cli_isis_data/juniper.txt")
    print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)    
    assert res == [[{'isis_processes': {'ISIS': {'R1-X1': [{'isis_area': '49.0001',
                                          'level': '2',
                                          'links': [{'bw_gbit': '10',
                                                     'local_intf_id': '332',
                                                     'local_ip': '10.123.111.238',
                                                     'metric': '20',
                                                     'peer_intf_id': '461',
                                                     'peer_ip': '10.123.111.237',
                                                     'peer_name': 'R1-X2'}],
                                          'networks': [{'metric': '0',
                                                        'network': '10.123.123.31/32'},
                                                       {'metric': '0',
                                                        'network': '10.123.123.41/32'},
                                                       {'metric': '20',
                                                        'network': '::ffff:10.123.111.236/126'}],
                                          'rid': '10.123.123.31',
                                          'rid_v6': '2001::10:123:123:31'}]}}}]]
                                          
# test_N2G_isis_lsdb_juniper()

def test_N2G_cli_l2_data_juniper():
    with open("./mock_data/test_N2G_cli_l2_data_juniper.txt", "r") as f:
        data = f.read()
    template = get_template(path="misc/N2G/cli_l2_data/juniper.txt")
    print(template)
    parser = ttp(data=data, template=template, vars={"IfsNormalize": all_vars["short_interface_names"], "physical_ports": all_vars["physical_ports"]})
    parser.parse()
    res = parser.result()
    pprint.pprint(res)       
    assert res == [{'switch-1.net.acme1.lab': {'interfaces': {'GE0/0/0': {'description': 'useful '
                                                                       'staff',
                                                        'lag_id': '31',
                                                        'lag_mode': 'active',
                                                        'mtu': '9234',
                                                        'state': {'admin': 'Enabled',
                                                                  'description': 'useful '
                                                                                 'staff',
                                                                  'is_physical_port': True,
                                                                  'line': 'Up',
                                                                  'mac': '84:03:28:15:11:13'}}},
                             'interfaces_id': [{'description': 'em0',
                                                'id': '17',
                                                'interface': 'em0',
                                                'parent': '-',
                                                'status': 'Up'},
                                               {'description': '-',
                                                'id': '521',
                                                'interface': '100GE0/0/31',
                                                'parent': '-',
                                                'status': 'Down'},
                                               {'description': 'CID-BN-P-env4207-env4208-0004 '
                                                               '| BACKHAUL',
                                                'id': '612',
                                                'interface': '100GE0/0/32',
                                                'parent': '-',
                                                'status': 'Up'},
                                               {'description': '-',
                                                'id': '522',
                                                'interface': '100GE0/0/33',
                                                'parent': '-',
                                                'status': 'Down'},
                                               {'description': 'BACKHAUL',
                                                'id': '615',
                                                'interface': '100GE0/0/34',
                                                'parent': '-',
                                                'status': 'Up'},
                                               {'description': '-',
                                                'id': '602',
                                                'interface': '100GE0/0/35',
                                                'parent': '-',
                                                'status': 'Down'}],
                             'lldp_peers': [{'data': {'chassis_id': '04:3f:72:cf:43:21',
                                                      'parent_interface': '-',
                                                      'peer_port_description': '04:3f:72:cf:12:34'},
                                             'source': 'switch-1.net.acme1.lab',
                                             'src_label': '100GE0/0/12',
                                             'target': {'id': '04:3f:72:cf:43:21'},
                                             'trgt_label': ''},
                                            {'data': {'chassis_id': '11:22:33:1b:7a:80',
                                                      'parent_interface': '-',
                                                      'peer_port_description': 'Eth0'},
                                             'source': 'switch-1.net.acme1.lab',
                                             'src_label': '100GE0/0/13',
                                             'target': {'id': 'CSW31'},
                                             'trgt_label': ''},
                                            {'data': {'chassis_id': '9c:e1:76:9d:11:23',
                                                      'parent_interface': '-',
                                                      'peer_port_description': 'HundredGigE0/0/1/0.12'},
                                             'source': 'switch-1.net.acme1.lab',
                                             'src_label': '100GE0/0/14',
                                             'target': {'id': 'nsw02-env1.env4208.net.acme1.lab'},
                                             'trgt_label': '100GE0/0/1/0.12'},
                                            {'data': {'chassis_id': '9c:e1:76:9d:11:23',
                                                      'parent_interface': '-',
                                                      'peer_port_description': 'HundredGigE0/0/1/0.34'},
                                             'source': 'switch-1.net.acme1.lab',
                                             'src_label': '100GE0/0/15',
                                             'target': {'id': 'nsw02-env1.env4208.net.acme1.lab'},
                                             'trgt_label': '100GE0/0/1/0.34'}],
                             'node_facts': {'system': {'chassis_id': '84:03:28:15:12:34',
                                                       'description': 'Juniper '
                                                                      'Networks, '
                                                                      'Inc. '
                                                                      'ssm5123-64c '
                                                                      'Ethernet '
                                                                      'Switch, '
                                                                      'kernel '
                                                                      'JUNOS '
                                                                      '12.2R3-S1.3, '
                                                                      'Build '
                                                                      'date: '
                                                                      '2011-05-12 '
                                                                      '12:34:56 '
                                                                      'UTC '
                                                                      'Copyright '
                                                                      '(c) '
                                                                      '1996-2021 '
                                                                      'Juniper '
                                                                      'Networks, '
                                                                      'Inc.'}}}}]
                                                                      
# test_N2G_cli_l2_data_juniper()


def test_N2G_cli_ip_data_arista_eos():
    with open("./mock_data/test_N2G_cli_ip_data_arista_eos.txt", "r") as f:
        data = f.read()
    template = get_template(path="misc/N2G/cli_ip_data/arista_eos.txt")
    # print(template)
    parser = ttp(vars={"IfsNormalize": all_vars["short_interface_names"], "physical_ports": all_vars["physical_ports"]})
    parser.add_function(add_network, scope="group", name="add_network", add_ttp=True)
    parser.add_template(template=template)
    parser.add_input(data, template_name="arista_eos")
    parser.parse()
    res = parser.result()
    pprint.pprint(res)   
    assert res == [{'ceos1': {'interfaces': {'Eth1': {'arp': [{'age': '0:00:16',
                                                               'ip': '10.0.1.3',
                                                               'mac': '02:42:0a:00:01:03'}],
                                                      'ip_addresses': [{'ip': '10.0.1.4',
                                                                        'netmask': '24',
                                                                        'network': '10.0.1.0/24'}],
                                                      'port_description': 'Configured by '
                                                                          'NETCONF'},
                                             'Lo1': {'ip_addresses': [{'ip': '1.1.1.1',
                                                                       'netmask': '24',
                                                                       'network': '1.1.1.0/24'}]},
                                             'Lo1000': {},
                                             'Lo2': {'ip_addresses': [{'ip': '2.2.2.2',
                                                                       'netmask': '24',
                                                                       'network': '2.2.2.0/24'}],
                                                     'port_description': 'Lopback2 for Customer '
                                                                         '27123'},
                                             'Lo3': {'ip_addresses': [{'ip': '1.2.3.4',
                                                                       'netmask': '24',
                                                                       'network': '1.2.3.0/24'}],
                                                     'port_description': 'Customer #56924 '
                                                                         'service'}}}}]
                                                       
# test_N2G_cli_ip_data_arista_eos()