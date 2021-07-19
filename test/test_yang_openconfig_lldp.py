import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


def test_openconfig_lldp_cisco_ios():
    data1 = """
switch1# show lldp nei details
------------------------------------------------
Local Intf: Te2/1/23
Chassis id: 1111.2222.3333
Port id: Te1/2
Port Description: TenGigabitEthernet1/2
System Name: r1.lab.local

System Description: 
Cisco IOS Software, Catalyst 1234 L3 Switch Software (cat1234e-ENTSERVICESK9-M), Version 1534.1(1)SG, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2012 by Cisco Systems, Inc.
Compiled Sun 15-Apr-12 02:35 by p

Time remaining: 92 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses:
    IP: 1.1.1.1
Auto Negotiation - supported, enabled
Physical media capabilities:
    Other/unknown
Media Attachment Unit type: 35
Vlan ID: - not advertised

------------------------------------------------
Local Intf: Te1/1/9
Chassis id: 4444.5555.6666
Port id: Gi1/1
Port Description: GigabitEthernet1/1
System Name: r5.lab.local

System Description: 
Cisco IOS Software, C4321 Software (C4321-IPBASEK9-M), Version 143.0(2)SE7, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Thu 23-Oct-14 13:43 by prod_rel_team

Time remaining: 103 seconds
System Capabilities: B,R
Enabled Capabilities: B
Management Addresses:
    IP: 2.2.2.5
Auto Negotiation - not supported
Physical media capabilities:
    1000baseX(FD)
Media Attachment Unit type: 24
Vlan ID: - not advertised
    """
    data2 = """
switch333# show lldp nei details
------------------------------------------------
Local Intf: Te2/1/121
Chassis id: 7777.aaaa.bbbb
Port id: Te1/2
Port Description: TenGigabitEthernet1/2
System Name: sw31.lab.local

System Description: 
Cisco IOS Software, Catalyst 569 L3 Switch Software (cat569e-ENTSERVICESK9-M), Version 125.1(1)SG, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2012 by Cisco Systems, Inc.
Compiled Sun 15-Apr-12 02:35 by p

Time remaining: 92 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses:
    IP: 31.1.1.1
Auto Negotiation - supported, enabled
Physical media capabilities:
    Other/unknown
Media Attachment Unit type: 35
Vlan ID: - not advertised

------------------------------------------------
Local Intf: Te1/1/9
Chassis id: 8888.bbbb.aaaa
Port id: Gi1/1
Port Description: GigabitEthernet1/1
System Name: rcore-1234

System Description: 
Cisco IOS Software, C567E Software (C567E-IPBASEK9-M), Version 178.0(2)SE7, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Thu 23-Oct-14 13:43 by prod_rel_team

Time remaining: 103 seconds
System Capabilities: B,R
Enabled Capabilities: B
Management Addresses:
    IP: 123.4.4.44
Auto Negotiation - not supported
Physical media capabilities:
    1000baseLX(FD)
Media Attachment Unit type: 24
Vlan ID: - not advertised   
    """
    template = get_template(yang="openconfig-lldp", platform="cisco_ios")
    # print(template)
    parser = ttp(template=template, vars={"validate_with_yangson": False})
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result(structure="flat_list")
    # pprint.pprint(res, width=200)
    assert res == [
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "switch1"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "10GE2/1/23",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "11:11:22:22:33:33",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "1.1.1.1",
                                                "port-description": "TenGigabitEthernet1/2",
                                                "port-id": "10GE1/2",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco IOS Software, Catalyst 1234 L3 Switch Software "
                                                "(cat1234e-ENTSERVICESK9-M), Version 1534.1(1)SG, RELEASE SOFTWARE (fc3) "
                                                "Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2012 "
                                                "by Cisco Systems, Inc. Compiled Sun 15-Apr-12 02:35 by p",
                                                "system-name": "r1.lab.local",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "10GE1/1/9",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "44:44:55:55:66:66",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "2.2.2.5",
                                                "port-description": "GigabitEthernet1/1",
                                                "port-id": "GE1/1",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco IOS Software, C4321 Software (C4321-IPBASEK9-M), Version 143.0(2)SE7, "
                                                "RELEASE SOFTWARE (fc1) Technical Support: http://www.cisco.com/techsupport "
                                                "Copyright (c) 1986-2014 by Cisco Systems, Inc. Compiled Thu 23-Oct-14 13:43 "
                                                "by prod_rel_team",
                                                "system-name": "r5.lab.local",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "switch333"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "10GE2/1/121",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "77:77:aa:aa:bb:bb",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "31.1.1.1",
                                                "port-description": "TenGigabitEthernet1/2",
                                                "port-id": "10GE1/2",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco IOS Software, Catalyst 569 L3 Switch Software "
                                                "(cat569e-ENTSERVICESK9-M), Version 125.1(1)SG, RELEASE SOFTWARE (fc3) "
                                                "Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2012 "
                                                "by Cisco Systems, Inc. Compiled Sun 15-Apr-12 02:35 by p",
                                                "system-name": "sw31.lab.local",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "10GE1/1/9",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "88:88:bb:bb:aa:aa",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "123.4.4.44",
                                                "port-description": "GigabitEthernet1/1",
                                                "port-id": "GE1/1",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco IOS Software, C567E Software (C567E-IPBASEK9-M), Version 178.0(2)SE7, "
                                                "RELEASE SOFTWARE (fc1) Technical Support: http://www.cisco.com/techsupport "
                                                "Copyright (c) 1986-2014 by Cisco Systems, Inc. Compiled Thu 23-Oct-14 13:43 "
                                                "by prod_rel_team",
                                                "system-name": "rcore-1234",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
    ]


# test_openconfig_lldp_cisco_ios()


def test_openconfig_lldp_cisco_ios_xr():
    data1 = """
xr-route-1# show lldp nei det
------------------------------------------------
Local Interface: TenGigE0/0/0/0
Parent Interface: Bundle-Ether5
Chassis id: 1234.1234.1234
Port id: GigabitEthernet2/1/2
Port Description: some direct fibre patching
System Name: core-route-1

System Description: 

Huawei Versatile Routing Platform Software
VRP (R) software, Version 251.1 (CX632 V12345678)
Copyright (C) 2000-2099 Huawei Technologies Co., Ltd.
CX61-X29


Time remaining: 106 seconds
Hold Time: 120 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses:
  IPv4 address: 1.1.1.11

Peer MAC Address: 66:33:88:65:11:22


------------------------------------------------
Local Interface: HundredGigE0/0/2/0
Parent Interface: Bundle-Ether1
Chassis id: 4321.4321.4321
Port id: HundredGigE0/0/2/0
Port Description: to edge  router 1
System Name: edge-route-1

System Description: 
 3.4.2, NCS-1234

Time remaining: 100 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 2.2.2.2

Peer MAC Address: 66:33:88:65:11:11
    """
    data2 = """
xr-route-0# show lldp nei det
------------------------------------------------
Local Interface: TenGigE0/0/0/1
Parent Interface: Bundle-Ether5
Chassis id: 1234.1234.1234
Port id: GigabitEthernet2/1/2
Port Description: some direct fibre patching
System Name: core-route-21

System Description: 

Huawei Versatile Routing Platform Software
VRP (R) software, Version 251.1 (CX632 V12345678)
Copyright (C) 2000-2099 Huawei Technologies Co., Ltd.
CX61-X29


Time remaining: 106 seconds
Hold Time: 120 seconds
System Capabilities: B,R
Enabled Capabilities: B,R
Management Addresses:
  IPv4 address: 4.4.4.4

Peer MAC Address: 66:33:88:65:11:33


------------------------------------------------
Local Interface: HundredGigE0/0/2/1
Parent Interface: Bundle-Ether3
Chassis id: 4321.4321.4321
Port id: HundredGigE0/0/2/1
Port Description: to edge  router 1
System Name: edge-route-1

System Description: 
 3.4.2, NCS-1234

Time remaining: 100 seconds
Hold Time: 120 seconds
System Capabilities: R
Enabled Capabilities: R
Management Addresses:
  IPv4 address: 3.3.3.3

Peer MAC Address: 66:33:88:65:11:44
    """
    template = get_template(yang="openconfig-lldp", platform="cisco_xr")
    # print(template)
    parser = ttp(template=template)
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result(structure="flat_list")
    # pprint.pprint(res, width=200)
    assert res == [
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "xr-route-1"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "10GE0/0/0/0",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "12:34:12:34:12:34",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "1.1.1.11",
                                                "port-description": "some direct fibre patching",
                                                "port-id": "GE2/1/2",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Huawei Versatile Routing Platform Software VRP (R) software, Version 251.1 "
                                                "(CX632 V12345678) Copyright (C) 2000-2099 Huawei Technologies Co., Ltd. "
                                                "CX61-X29",
                                                "system-name": "core-route-1",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "100GE0/0/2/0",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [{"name": "ROUTER"}]
                                                },
                                                "chassis-id": "43:21:43:21:43:21",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "2.2.2.2",
                                                "port-description": "to edge  router 1",
                                                "port-id": "100GE0/0/2/0",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "3.4.2, NCS-1234",
                                                "system-name": "edge-route-1",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "xr-route-0"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "10GE0/0/0/1",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "12:34:12:34:12:34",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "4.4.4.4",
                                                "port-description": "some direct fibre patching",
                                                "port-id": "GE2/1/2",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Huawei Versatile Routing Platform Software VRP (R) software, Version 251.1 "
                                                "(CX632 V12345678) Copyright (C) 2000-2099 Huawei Technologies Co., Ltd. "
                                                "CX61-X29",
                                                "system-name": "core-route-21",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "100GE0/0/2/1",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [{"name": "ROUTER"}]
                                                },
                                                "chassis-id": "43:21:43:21:43:21",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "3.3.3.3",
                                                "port-description": "to edge  router 1",
                                                "port-id": "100GE0/0/2/1",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "3.4.2, NCS-1234",
                                                "system-name": "edge-route-1",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
    ]


# test_openconfig_lldp_cisco_ios_xr()


def test_openconfig_lldp_cisco_nxos():
    data1 = """
switch-nxos-core-1# show lldp eni det
Chassis id: 1234.1234.1234
Port id: Eth1/1
Local Port id: mgmt0
Port Description: switch-1:mgmt0 oob
System Name: switch-1
System Description: Cisco Nexus Operating System (NX-OS) Software 2.1(1)U1(1)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2014, Cisco Systems, Inc. All rights reserved.
Time remaining: 108 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 1.1.1.1
Management Address IPV6: not advertised
Vlan ID: 111


Chassis id: 4321.4321.4321
Port id: 1234.4444.3333
Local Port id: Eth1/21
Port Description: null
System Name: null
System Description: null
Time remaining: 117 seconds
System Capabilities: not advertised
Enabled Capabilities: not advertised
Management Address: not advertised
Management Address IPV6: not advertised
Vlan ID: not advertised
    """
    data2 = """
switch24-edge-1# show lldp nei det
Chassis id: 5555.5555.5555
Port id: Eth1/23
Local Port id: Eth5/3
Port Description: abc-switch-1 some port some   description
System Name: abc-switch-1
System Description: Cisco NX-OS(tm) n1100, Software (n7100-s6-dk9), Version 21.32(1), RELEASE SOFTWARE Copyright (c) 2002-2017 by Cisco Systems, Inc. Compiled 6/36/2099 01:00
:00
Time remaining: 118 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 2.2.2.2
Vlan ID: not advertised


Chassis id: 6666.6666.6666
Port id: Ethernet1/25/4
Local Port id: Eth1/234
Port Description: system42 interface 1234
System Name: system42
System Description: Cisco Nexus Operating System (NX-OS) Software 123.1(4)I4(4)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2091, Cisco Systems, Inc. All rights reserved.
Time remaining: 112 seconds
System Capabilities: B, R
Enabled Capabilities: B, R
Management Address: 25.25.25.25
Management Address IPV6: 1234.1234.1234
Vlan ID: not advertised
    """
    template = get_template(yang="openconfig-lldp", platform="cisco_nxos")
    # print(template)
    parser = ttp(template=template, vars={"validate_with_yangson": False})
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result(structure="flat_list")
    # pprint.pprint(res, width=200)
    assert res == [
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "switch-nxos-core-1"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "MGMT0",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "12:34:12:34:12:34",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "1.1.1.1",
                                                "port-description": "switch-1:mgmt0 oob",
                                                "port-id": "Eth1/1",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco Nexus Operating System (NX-OS) Software 2.1(1)U1(1) TAC support: "
                                                "http://www.cisco.com/tac Copyright (c) 2002-2014, Cisco Systems, Inc. All "
                                                "rights reserved.",
                                                "system-name": "switch-1",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "Eth1/21",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {"capability": []},
                                                "chassis-id": "43:21:43:21:43:21",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": None,
                                                "port-description": "null",
                                                "port-id": "1234.4444.3333",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "null",
                                                "system-name": "null",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
        {
            "opencondig-lldp": {
                "lldp": {
                    "config": {"system-name": "switch24-edge-1"},
                    "interfaces": {
                        "interface": [
                            {
                                "name": "Eth5/3",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "55:55:55:55:55:55",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "2.2.2.2",
                                                "port-description": "abc-switch-1 some port some   description",
                                                "port-id": "Eth1/23",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco NX-OS(tm) n1100, Software (n7100-s6-dk9), Version 21.32(1), RELEASE "
                                                "SOFTWARE Copyright (c) 2002-2017 by Cisco Systems, Inc. Compiled 6/36/2099 "
                                                "01:00 :00",
                                                "system-name": "abc-switch-1",
                                            },
                                        }
                                    ]
                                },
                            },
                            {
                                "name": "Eth1/234",
                                "neighbors": {
                                    "neighbor": [
                                        {
                                            "id": 1,
                                            "state": {
                                                "capabilities": {
                                                    "capability": [
                                                        {"name": "MAC_BRIDGE"},
                                                        {"name": "ROUTER"},
                                                    ]
                                                },
                                                "chassis-id": "66:66:66:66:66:66",
                                                "chassis-id-type": "MAC_ADDRESS",
                                                "id": 1,
                                                "management-address": "25.25.25.25",
                                                "port-description": "system42 interface 1234",
                                                "port-id": "Eth1/25/4",
                                                "port-id-type": "INTERFACE_NAME",
                                                "system-description": "Cisco Nexus Operating System (NX-OS) Software 123.1(4)I4(4) TAC support: "
                                                "http://www.cisco.com/tac Copyright (c) 2002-2091, Cisco Systems, Inc. All "
                                                "rights reserved.",
                                                "system-name": "system42",
                                            },
                                        }
                                    ]
                                },
                            },
                        ]
                    },
                }
            }
        },
    ]


# test_openconfig_lldp_cisco_nxos()
