import sys
import pprint

sys.path.insert(0, "..")

from netmiko import ConnectHandler
from ttp_templates import get_template
from ttp_templates import ttp_vars


def mock_output_cisco_ios(command_string, *args, **kwargs):
    outputs = {
        "show ip arp": """
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  172.29.50.1             8   84b8.0276.ac0e  ARPA   
Internet  172.29.50.2           221   0019.0725.344a  ARPA   Vlan20
Internet  172.29.50.3             -   0024.f7dd.7741  ARPA   Vlan21       
        """,
        "show running-configuration | section interface": """
router-1# show running-config | section interface
interface Vlan1234
 description Some  description
 ip address 10.1.251.170 255.255.255.0
 ip address 10.1.251.171 255.255.255.0 secondary
 standby 1234 ip 172.20.128.3
 ipv6 address AAAA::1/64
 ipv6 address BBBB::1/64
!
interface GigabitEthernet1
 description Workstations subnet 1
 vrf forwarding OFFICE
 ip address 10.2.251.170 255.255.255.0 
 vrrp 123 ip  10.2.251.1
!
        """,
        "show running-configuration | section bgp": """
router bgp 65001
 !
 bgp router-id 10.5.1.1
 bgp log-neighbor-changes
 neighbor 2001:db8::1 remote-as 65003
 neighbor 2001:db8::1 description Peer1-Global
 neighbor 10.11.0.81 remote-as 65002
 neighbor 10.11.0.81 description Peer2-Global
 neighbor 10.11.0.81 shutdown
 neighbor RR-CLIENTS peer-group
 neighbor RR-CLIENTS remote-as 65001
 neighbor RR-CLIENTS description [ibgp - rr clients]
 neighbor RR-CLIENTS update-source GigabitEthernet1
 neighbor 10.0.0.3 peer-group RR-CLIENTS
 neighbor 10.0.0.5 peer-group RR-CLIENTS
 !
 address-family ipv4
  network 10.255.10.0 mask 255.255.248.0
  network 10.255.10.0 mask 255.255.255.0
  redistribute connected route-map PORTABLE-v4
  neighbor 10.11.0.81 activate
  neighbor 10.11.0.81 description Peer2-IPv4
  neighbor RR-CLIENTS route-reflector-client
  neighbor RR-CLIENTS route-map PASS-IN in
  neighbor RR-CLIENTS route-map PASS-OUT out
  neighbor RR-CLIENTS maximum-prefix 1000 80 restart 15
  neighbor 10.0.0.3 activate
  neighbor 10.0.0.5 activate
 exit-address-family
 !
 address-family ipv6
  redistribute connected
  network 2001:db8::/48
  neighbor 2001:db8::1 activate
  neighbor 2001:db8::1 description Peer1-IPv6
 exit-address-family
 !
 address-family ipv4 multicast
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 3.3.3.3 activate
 exit-address-family 
 !
 address-family ipv4 vrf VoIP
  network 10.255.10.0 mask 255.255.248.0 
  bgp router-id 10.2.1.193
  redistribute connected route-map tospokes
  neighbor 10.2.1.65 remote-as 65001
  neighbor 10.2.1.65 description voip peer 1
  neighbor 10.2.1.65 activate
  neighbor 10.2.1.78 remote-as 65001
  neighbor 10.2.1.78 description voip peer 2
  neighbor 10.2.1.78 shutdown
  neighbor 10.2.1.78 activate
  neighbor 10.2.1.78 next-hop-self
  neighbor 10.2.1.78 prefix-list VoIP-prefixes out
 exit-address-family
!
 address-family ipv4 vrf CUST-2
  bgp router-id 1.1.1.1
  redistribute connected
  neighbor 2.2.2.2 remote-as 65002
  neighbor 2.2.2.2 description peer 12
  neighbor 2.2.2.2 activate
 exit-address-family
!
    """
    }
    return outputs[command_string]


def mock_output_cisco_ios_xr(command_string, *args, **kwargs):
    outputs = {
        "show arp vrf all": """
-------------------------------------------------------------------------------
0/0/CPU0
-------------------------------------------------------------------------------
Address         Age        Hardware Addr   State      Type  Interface
10.1.2.3  -          1234.7698.d416  Interface  ARPA  GigabitEthernet0/0/0/22
10.1.2.4  00:35:34   1234.c686.c9c0  Dynamic    ARPA  GigabitEthernet0/0/0/22

-------------------------------------------------------------------------------
0/RP0/CPU0
-------------------------------------------------------------------------------
Address         Age        Hardware Addr   State      Type  Interface
10.2.3.33     00:10:50   1234.dd60.1f88  Dynamic    ARPA  MgmtEth0/RP0/CPU0/0
10.5.3.34     -          7cad.4fe6.a49a  Interface  ARPA  MgmtEth0/RP0/CPU0/0
        """,
        "show running-config interface": """
RP/0/RP0/CPU0:r1#show running-config interface
interface Bundle-Ether1
 description Description of interface
 ipv4 address 10.1.2.54 255.255.255.252
 ipv6 address fd00:1:2::31/126
!
interface Loopback123
 description VRF 123
 vrf VRF-1123
 ipv4 address 10.1.0.10 255.255.255.255
!
        """,
        "show running-config router vrrp": """
RP/0/RP0/CPU0:r1#show running-config router vrrp
router vrrp
 interface Bundle-Ether1
  address-family ipv4
   vrrp 1
    address 1.1.1.1
   !
  !
  address-family ipv6
   vrrp 1
    address global fd::1
!
        """,
        "show running-config router hsrp": """
RP/0/RP0/CPU0:r1#show running-config router hsrp
router hsrp
 interface Bundle-Ether1
  address-family ipv4
   hsrp 1
    address 3.3.3.3
   !
  !
  address-family ipv6
   hsrp 1
    address global fd::3
!
        """
    }
    return outputs[command_string]


def mock_output_huawei_vrp(command_string, *args, **kwargs):
    outputs = {
        "display current-configuration interface": """
<router_23>display current-configuration interface
interface Eth-Trunk1.100
 description Link description  here
 ip address 10.1.130.2 255.255.255.252
 ip address 10.1.130.3 255.255.255.252 sub 
 ip binding vpn-instance VRF2 
#
interface vlanif10
 description Link description  here 2
 ip binding vpn-instance VRF2 
 ip address 10.2.130.2 255.255.255.252
 vrrp vrid 1 virtual-ip 10.1.1.2
 ipv6 address fc00:1::2/64
 vrrp6 vrid 1 virtual-ip 2001:DB8::100 
#
        """
    }
    return outputs[command_string]
    
    
lab_cisco_ios = {
    "device_type": "cisco_ios",
    "host": "1.2.3.4",
    "username": "cisco",
    "password": "cisco",
    "auto_connect": False,  # stop Netmiko trying connect to device
}
connection_cisco_ios = ConnectHandler(**lab_cisco_ios)
# override send command method to return mock data
setattr(connection_cisco_ios, "send_command", mock_output_cisco_ios)

lab_cisco_ios_xr = {
    "device_type": "cisco_xr",
    "host": "1.2.3.4",
    "username": "cisco",
    "password": "cisco",
    "auto_connect": False,  # stop Netmiko trying connect to device
}
connection_cisco_ios_xr = ConnectHandler(**lab_cisco_ios_xr)
setattr(connection_cisco_ios_xr, "send_command", mock_output_cisco_ios_xr)


lab_huawei_vrp = {
    "device_type": "huawei",
    "host": "1.2.3.4",
    "username": "huawei",
    "password": "huawei",
    "auto_connect": False,  # stop Netmiko trying connect to device
}
connection_huawei_vrp = ConnectHandler(**lab_huawei_vrp)
setattr(connection_huawei_vrp, "send_command", mock_output_huawei_vrp)


def test_cisco_ios_arp_original_intf_names():
    res = connection_cisco_ios.run_ttp(
        "ttp://misc/netmiko/cisco.ios.arp.txt", res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res)
    assert res == [
        {
            "age": 8,
            "interface": "Uncknown",
            "ip": "172.29.50.1",
            "mac": "84:b8:02:76:ac:0e",
            "protocol": "Internet",
            "type": "ARPA",
        },
        {
            "age": 221,
            "interface": "Vlan20",
            "ip": "172.29.50.2",
            "mac": "00:19:07:25:34:4a",
            "protocol": "Internet",
            "type": "ARPA",
        },
        {
            "age": -1,
            "interface": "Vlan21",
            "ip": "172.29.50.3",
            "mac": "00:24:f7:dd:77:41",
            "protocol": "Internet",
            "type": "ARPA",
        },
    ]


# test_cisco_ios_arp_original_intf_names()


def test_cisco_ios_cfg_ip_original_intf_names():
    res = connection_cisco_ios.run_ttp(
        "ttp://misc/netmiko/cisco.ios.cfg.ip.txt", res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res)
    assert res == [
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.170",
            "mask": "255.255.255.0",
            'vrf': 'default',
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.171",
            "mask": "255.255.255.0",
            "secondary": True,
            'vrf': 'default',
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "172.20.128.3",
            "vip": True,
            "vip_type": "HSRP",
            'vrf': 'default',
        },
        {
            "mask": "64",
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "AAAA::1",
            'vrf': 'default',
        },
        {
            "mask": "64",
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "BBBB::1",
            'vrf': 'default',
        },
        {
            "description": "Workstations subnet 1",
            "hostname": "router-1",
            "interface": "GigabitEthernet1",
            "ipv4": "10.2.251.170",
            "mask": "255.255.255.0",
            "vrf": "OFFICE",
        },
        {
            "description": "Workstations subnet 1",
            "hostname": "router-1",
            "interface": "GigabitEthernet1",
            "ipv4": "10.2.251.1",
            "vip": True,
            "vip_type": "VRRP",
            "vrf": "OFFICE",
        },
    ]


# test_cisco_ios_cfg_ip_original_intf_names()


def test_cisco_ios_cfg_ip_short_intf_names():
    res = connection_cisco_ios.run_ttp(
        "ttp://misc/netmiko/cisco.ios.cfg.ip.txt",
        res_kwargs={"structure": "flat_list"},
        vars=ttp_vars.all_vars,
    )
    # pprint.pprint(res)
    assert res == [
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.170",
            "mask": "255.255.255.0",
            'vrf': 'default',
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.171",
            "mask": "255.255.255.0",
            "secondary": True,
            'vrf': 'default',
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "172.20.128.3",
            "vip": True,
            "vip_type": "HSRP",
            'vrf': 'default',
        },
        {
            "mask": "64",
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "AAAA::1",
            'vrf': 'default',
        },
        {
            "mask": "64",
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "BBBB::1",
            'vrf': 'default',
        },
        {
            "description": "Workstations subnet 1",
            "hostname": "router-1",
            "interface": "GE1",
            "ipv4": "10.2.251.170",
            "mask": "255.255.255.0",
            "vrf": "OFFICE",
        },
        {
            "description": "Workstations subnet 1",
            "hostname": "router-1",
            "interface": "GE1",
            "ipv4": "10.2.251.1",
            "vip": True,
            "vip_type": "VRRP",
            "vrf": "OFFICE",
        },
    ]


# test_cisco_ios_cfg_ip_short_intf_names()


def test_cisco_ios_xr_arp_short_intf_names():
    res = connection_cisco_ios_xr.run_ttp(
        "ttp://misc/netmiko/cisco.iosxr.arp.txt",
        res_kwargs={"structure": "flat_list"},
        vars={"short_interface_names": ttp_vars.short_interface_names},
    )
    # pprint.pprint(res)
    assert res == [
        {
            "age": -1,
            "interface": "GE0/0/0/22",
            "ip": "10.1.2.3",
            "mac": "12:34:76:98:d4:16",
            "state": "interface",
            "type": "ARPA",
        },
        {
            "age": "00:35:34",
            "interface": "GE0/0/0/22",
            "ip": "10.1.2.4",
            "mac": "12:34:c6:86:c9:c0",
            "state": "dynamic",
            "type": "ARPA",
        },
        {
            "age": "00:10:50",
            "interface": "MGMTEth0/RP0/CPU0/0",
            "ip": "10.2.3.33",
            "mac": "12:34:dd:60:1f:88",
            "state": "dynamic",
            "type": "ARPA",
        },
        {
            "age": -1,
            "interface": "MGMTEth0/RP0/CPU0/0",
            "ip": "10.5.3.34",
            "mac": "7c:ad:4f:e6:a4:9a",
            "state": "interface",
            "type": "ARPA",
        },
    ]


# test_cisco_ios_xr_arp_short_intf_names()


def test_cisco_ios_xr_arp_original_intf_names():
    res = connection_cisco_ios_xr.run_ttp(
        "ttp://misc/netmiko/cisco.iosxr.arp.txt", res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res)
    assert res == [
        {
            "age": -1,
            "interface": "GigabitEthernet0/0/0/22",
            "ip": "10.1.2.3",
            "mac": "12:34:76:98:d4:16",
            "state": "interface",
            "type": "ARPA",
        },
        {
            "age": "00:35:34",
            "interface": "GigabitEthernet0/0/0/22",
            "ip": "10.1.2.4",
            "mac": "12:34:c6:86:c9:c0",
            "state": "dynamic",
            "type": "ARPA",
        },
        {
            "age": "00:10:50",
            "interface": "MgmtEth0/RP0/CPU0/0",
            "ip": "10.2.3.33",
            "mac": "12:34:dd:60:1f:88",
            "state": "dynamic",
            "type": "ARPA",
        },
        {
            "age": -1,
            "interface": "MgmtEth0/RP0/CPU0/0",
            "ip": "10.5.3.34",
            "mac": "7c:ad:4f:e6:a4:9a",
            "state": "interface",
            "type": "ARPA",
        },
    ]


# test_cisco_ios_xr_arp_original_intf_names()


def test_huawei_vrp_cfg_ip_original_intf_names():
    res = connection_huawei_vrp.run_ttp(
        "ttp://misc/netmiko/huawei.vrp.cfg.ip.txt", res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res)
    assert res == [{'description': 'Link description  here',
                    'hostname': 'router_23',
                    'interface': 'Eth-Trunk1.100',
                    'ipv4': '10.1.130.2',
                    'mask': '255.255.255.252',
                    'vrf': 'default'},
                   {'description': 'Link description  here',
                    'hostname': 'router_23',
                    'interface': 'Eth-Trunk1.100',
                    'ipv4': '10.1.130.3',
                    'mask': '255.255.255.252',
                    'secondary': True,
                    'vrf': 'default'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'vlanif10',
                    'ipv4': '10.2.130.2',
                    'mask': '255.255.255.252',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'vlanif10',
                    'ipv4': '10.1.1.2',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'vlanif10',
                    'ipv6': 'fc00:1::2',
                    'mask': '64',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'vlanif10',
                    'ipv6': '2001:DB8::100',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'VRF2'}]
  
# test_huawei_vrp_cfg_ip_original_intf_names()


def test_huawei_vrp_cfg_ip_short_intf_names():
    res = connection_huawei_vrp.run_ttp(
        "ttp://misc/netmiko/huawei.vrp.cfg.ip.txt", 
        res_kwargs={"structure": "flat_list"},
        vars=ttp_vars.all_vars
    )
    # pprint.pprint(res)
    assert res == [{'description': 'Link description  here',
                    'hostname': 'router_23',
                    'interface': 'LAG1.100',
                    'ipv4': '10.1.130.2',
                    'mask': '255.255.255.252',
                    'vrf': 'default'},
                   {'description': 'Link description  here',
                    'hostname': 'router_23',
                    'interface': 'LAG1.100',
                    'ipv4': '10.1.130.3',
                    'mask': '255.255.255.252',
                    'secondary': True,
                    'vrf': 'default'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'VLAN10',
                    'ipv4': '10.2.130.2',
                    'mask': '255.255.255.252',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'VLAN10',
                    'ipv4': '10.1.1.2',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'VLAN10',
                    'ipv6': 'fc00:1::2',
                    'mask': '64',
                    'vrf': 'VRF2'},
                   {'description': 'Link description  here 2',
                    'hostname': 'router_23',
                    'interface': 'VLAN10',
                    'ipv6': '2001:DB8::100',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'VRF2'}]
  
# test_huawei_vrp_cfg_ip_short_intf_names()


def test_cisco_iosxr_cfg_ip_original_intf_names():
    res = connection_cisco_ios_xr.run_ttp(
        "ttp://misc/netmiko/cisco.iosxr.cfg.ip.txt", 
        res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res)
    assert res == [{'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv4': '10.1.2.54',
                    'mask': '255.255.255.252',
                    'vrf': 'default'},
                    {'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv6': 'fd00:1:2::31',
                    'mask': '126',
                    'vrf': 'default'},
                    {'description': 'VRF 123',
                    'hostname': 'r1',
                    'interface': 'Loopback123',
                    'ipv4': '10.1.0.10',
                    'mask': '255.255.255.255',
                    'vrf': 'VRF-1123'},
                    {'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv4': '1.1.1.1',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'default'},
                    {'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv6': 'fd::1',
                    'vip': True,
                    'vip_type': 'VRRP',
                    'vrf': 'default'},
                    {'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv4': '3.3.3.3',
                    'vip': True,
                    'vip_type': 'HSRP',
                    'vrf': 'default'},
                    {'description': 'Description of interface',
                    'hostname': 'r1',
                    'interface': 'Bundle-Ether1',
                    'ipv6': 'fd::3',
                    'vip': True,
                    'vip_type': 'HSRP',
                    'vrf': 'default'}]
  
# test_cisco_iosxr_cfg_ip_original_intf_names()


def test_cisco_ios_cfg_bgp():
    res = connection_cisco_ios.run_ttp(
        "ttp://misc/netmiko/cisco.ios.cfg.bgp.txt", 
        # res_kwargs={"structure": "flat_list"}
    )
    # pprint.pprint(res, width=150) 
    assert res == [[{'bgp': {'afis': {'ipv4_multicast': {},
                    'ipv4_unicast': {'config': {'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'},
                                                             {'mask': '255.255.255.0', 'network': '10.255.10.0'}],
                                                'redistribute_connected': True,
                                                'redistribute_connected_rpl': 'PORTABLE-v4'},
                                     'neighbors': {'10.0.0.3': {'activate': True},
                                                   '10.0.0.5': {'activate': True},
                                                   '10.11.0.81': {'activate': True},
                                                   'RR-CLIENTS': {'max_prefix_action': 'restart',
                                                                  'max_prefix_limit': '1000',
                                                                  'max_prefix_restart_interval': '15',
                                                                  'max_prefix_threshold': '80',
                                                                  'rpl_out': 'PASS-OUT',
                                                                  'rr_client': True}}},
                    'ipv6_unicast': {'config': {'networks': [{'mask': '48', 'network': '2001:db8::'}], 'redistribute_connected': True},
                                     'neighbors': {'2001:db8::1': {'activate': True}}},
                    'vpnv4_unicast': {'neighbors': {'3.3.3.3': {'activate': True}}}},
           'asn': '65001',
           'config': {'bgp_rid': '10.5.1.1', 'log_neighbor_changes': True},
           'neighbors': {'10.0.0.3': {'peer_group': 'RR-CLIENTS'},
                         '10.0.0.5': {'peer_group': 'RR-CLIENTS'},
                         '10.11.0.81': {'asn': '65002', 'description': 'Peer2-Global', 'disabled': True},
                         '2001:db8::1': {'asn': '65003', 'description': 'Peer1-Global'},
                         'RR-CLIENTS': {'asn': '65001',
                                        'description': '[ibgp - rr clients]',
                                        'is_peer_group': True,
                                        'update_source': 'GigabitEthernet1'}},
           'vrfs': {'CUST-2': {'afi': 'ipv4',
                               'config': {'bgp_rid': '1.1.1.1', 'redistribute_connected': True},
                               'neighbors': {'2.2.2.2': {'activate': True, 'asn': '65002', 'description': 'peer 12'}}},
                    'VoIP': {'afi': 'ipv4',
                             'config': {'bgp_rid': '10.2.1.193',
                                        'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'}],
                                        'redistribute_connected': True,
                                        'redistribute_connected_rpl': 'tospokes'},
                             'neighbors': {'10.2.1.65': {'activate': True, 'asn': '65001', 'description': 'voip peer 1'},
                                           '10.2.1.78': {'activate': True,
                                                         'asn': '65001',
                                                         'description': 'voip peer 2',
                                                         'disabled': True,
                                                         'next_hop_self': True,
                                                         'pfl_out': 'VoIP-prefixes'}}}}}}]]
    
# test_cisco_ios_cfg_bgp()