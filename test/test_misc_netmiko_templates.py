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
        "show running-config | section interface": """
router-1# show running-config | section interface
interface Vlan1234
 description Some  description
 vrf forwarding VRF1
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
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.171",
            "mask": "255.255.255.0",
            "secondary": True,
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "172.20.128.3",
            "vip": True,
            "vip_type": "HSRP",
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "AAAA::1/64",
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "BBBB::1/64",
            "vrf": "VRF1",
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
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "10.1.251.171",
            "mask": "255.255.255.0",
            "secondary": True,
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv4": "172.20.128.3",
            "vip": True,
            "vip_type": "HSRP",
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "AAAA::1/64",
            "vrf": "VRF1",
        },
        {
            "description": "Some  description",
            "hostname": "router-1",
            "interface": "Vlan1234",
            "ipv6": "BBBB::1/64",
            "vrf": "VRF1",
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
