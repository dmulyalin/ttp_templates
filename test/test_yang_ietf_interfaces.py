import sys
import pprint
sys.path.insert(0,'..')

from ttp_templates import get_template
from ttp import ttp


def test_cisco_ios():
    data1 = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/4
 description vCPEs access control
 ip address 172.16.33.10 255.255.255.128
!
    """
    data2 = """
interface GigabitEthernet1/5
 description Works data
 ip mtu 9000
!
interface GigabitEthernet1/7
 description Works data v6
 ipv6 address 2001::1/64
 ipv6 address 2001:1::1/64    
    """
    template = get_template(yang="ietf-interfaces", platform="cisco_ios")
    # print(template)
    parser = ttp(template=template, vars={"validate_with_yangson": True})
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [{'comment': '',
                    'exception': {},
                    'result': [{'ietf-interfaces:interfaces': {'interface': [{'admin-status': 'down',
                                                                              'description': 'Customer '
                                                                                             '#32148',
                                                                              'enabled': False,
                                                                              'ietf-ip:ipv4': {'address': [{'ip': '172.16.33.10',
                                                                                                            'netmask': '255.255.255.128',
                                                                                                            'origin': 'static'}]},
                                                                              'if-index': 1,
                                                                              'link-up-down-trap-enable': 'enabled',
                                                                              'name': 'GigabitEthernet1/3.251',
                                                                              'oper-status': 'unknown',
                                                                              'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
                                                                              'type': 'iana-if-type:ethernetCsmacd'},
                                                                             {'admin-status': 'up',
                                                                              'description': 'vCPEs '
                                                                                             'access '
                                                                                             'control',
                                                                              'enabled': True,
                                                                              'ietf-ip:ipv4': {'address': [{'ip': '172.16.33.10',
                                                                                                            'netmask': '255.255.255.128',
                                                                                                            'origin': 'static'}]},
                                                                              'if-index': 1,
                                                                              'link-up-down-trap-enable': 'enabled',
                                                                              'name': 'GigabitEthernet1/4',
                                                                              'oper-status': 'unknown',
                                                                              'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
                                                                              'type': 'iana-if-type:ethernetCsmacd'}]}},
                               {'ietf-interfaces:interfaces': {'interface': [{'admin-status': 'up',
                                                                              'description': 'Works '
                                                                                             'data',
                                                                              'enabled': True,
                                                                              'ietf-ip:ipv4': {'mtu': 9000},
                                                                              'if-index': 1,
                                                                              'link-up-down-trap-enable': 'enabled',
                                                                              'name': 'GigabitEthernet1/5',
                                                                              'oper-status': 'unknown',
                                                                              'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
                                                                              'type': 'iana-if-type:ethernetCsmacd'},
                                                                             {'admin-status': 'up',
                                                                              'description': 'Works '
                                                                                             'data '
                                                                                             'v6',
                                                                              'enabled': True,
                                                                              'ietf-ip:ipv6': {'address': [{'ip': '2001::1',
                                                                                                            'origin': 'static',
                                                                                                            'prefix-length': 64},
                                                                                                           {'ip': '2001:1::1',
                                                                                                            'origin': 'static',
                                                                                                            'prefix-length': 64}]},
                                                                              'if-index': 1,
                                                                              'link-up-down-trap-enable': 'enabled',
                                                                              'name': 'GigabitEthernet1/7',
                                                                              'oper-status': 'unknown',
                                                                              'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
                                                                              'type': 'iana-if-type:ethernetCsmacd'}]}}],
                    'valid': {0: True, 1: True}}]
    
# test_cisco_ios()