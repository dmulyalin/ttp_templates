import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


def test_N2G_ospf_Cisco_IOSXR():
    data1 = """
RP/0/RP0/CPU0:router-1#show ospf database router 

            OSPF Router with ID (10.1.2.2) (Process ID 1)

                Router Link States (Area 0.0.0.0)

  Routing Bit Set on this LSA
  LS age: 787
  Options: (No TOS-capability, No DC)
  LS Type: Router Links
  Link State ID: 10.1.0.91
  Advertising Router: 10.1.0.91
  LS Seq Number: 80006666
  Checksum: 0x210d
  Length: 288
  Area Border Router
   Number of Links: 22

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.1.251
     (Link Data) Router Interface address: 10.0.61.1
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.61.0
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.6
     (Link Data) Router Interface address: 10.0.61.94
      Number of TOS metrics: 0
       TOS 0 Metrics: 65535

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.7
     (Link Data) Router Interface address: 0.0.1.220
      Number of TOS metrics: 0
       TOS 0 Metrics: 3000

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.3.162.13
     (Link Data) Router Interface address: 10.3.162.14
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Transit Network
     (Link ID) Designated Router address: 10.3.162.9
     (Link Data) Router Interface address: 10.3.162.10
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

  Routing Bit Set on this LSA
  LS age: 787
  Options: (No TOS-capability, No DC)
  LS Type: Router Links
  Link State ID: 10.1.0.92
  Advertising Router: 10.1.0.92
  LS Seq Number: 8000cbda
  Checksum: 0x3e2f
  Length: 312
  Area Border Router
   Number of Links: 24

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.61.96
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.6
     (Link Data) Router Interface address: 0.0.2.5
      Number of TOS metrics: 0
       TOS 0 Metrics: 1100

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.8
     (Link Data) Router Interface address: 0.0.2.67
      Number of TOS metrics: 0
       TOS 0 Metrics: 3000

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.2.7
     (Link Data) Router Interface address: 0.0.2.69
      Number of TOS metrics: 0
       TOS 0 Metrics: 3000
       
RP/0/RP0/CPU0:router-1#show ospf database summary 

            OSPF Router with ID (10.1.2.2) (Process ID 1)

                Summary Net Link States (Area 0.0.0.0)

  LS age: 1639
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.1
  LS Seq Number: 800030eb
  Checksum: 0x899d
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 2312 

  LS age: 427
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.2
  LS Seq Number: 800030eb
  Checksum: 0xad74
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1806 

  LS age: 1695
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.192
  LS Seq Number: 800030eb
  Checksum: 0xd081
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1312 

  Routing Bit Set on this LSA
  LS age: 581
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.193
  LS Seq Number: 800030eb
  Checksum: 0xf458
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 806 

                Summary Net Link States (Area 0.0.0.32)

  LS age: 1639
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.1
  LS Seq Number: 800030eb
  Checksum: 0x899d
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 2312 
        
RP/0/RSP0/CPU0:router-1#show ospf database external 

            OSPF Router with ID (10.3.22.75) (Process ID 1)

                Type-5 AS External Link States

  Routing Bit Set on this LSA
  LS age: 1009
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.3.22.190
  LS Seq Number: 80000519
  Checksum: 0x9009
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  LS age: 520
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.3.25.22
  LS Seq Number: 80001b96
  Checksum: 0x3279
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  Routing Bit Set on this LSA
  LS age: 90
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.0.0 (External Network Number)
  Advertising Router: 10.3.20.95
  LS Seq Number: 8003494f
  Checksum: 0x1d4d
  Length: 36
  Network Mask: /8
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 0.0.0.0
        External Route Tag: 0

  Routing Bit Set on this LSA
  LS age: 1251
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.2.0 (External Network Number)
  Advertising Router: 10.3.22.83
  LS Seq Number: 800079c3
  Checksum: 0x5d2e
  Length: 36
  Network Mask: /24
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 10.4.209.161
        External Route Tag: 0
    """
    data2 = """
RP/0/RP0/CPU0:router-1#show ospf database router 

            OSPF Router with ID (10.1.2.2) (Process ID 1)

                Router Link States (Area 0.0.0.0)

  Routing Bit Set on this LSA
  LS age: 787
  Options: (No TOS-capability, No DC)
  LS Type: Router Links
  Link State ID: 10.1.0.91
  Advertising Router: 10.1.0.91
  LS Seq Number: 80006666
  Checksum: 0x210d
  Length: 288
  Area Border Router
   Number of Links: 22

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.24.6
     (Link Data) Router Interface address: 10.0.60.206
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.60.204
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.1.0.92
     (Link Data) Router Interface address: 10.0.60.197
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.60.196
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

  Routing Bit Set on this LSA
  LS age: 787
  Options: (No TOS-capability, No DC)
  LS Type: Router Links
  Link State ID: 10.1.0.92
  Advertising Router: 10.1.0.92
  LS Seq Number: 8000cbda
  Checksum: 0x3e2f
  Length: 312
  Area Border Router
   Number of Links: 24

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.24.31
     (Link Data) Router Interface address: 10.0.60.109
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.60.108
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 1

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.24.5
     (Link Data) Router Interface address: 10.0.60.201
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000
          
    Link connected to: a Stub Network
     (Link ID) Network/subnet number: 10.0.60.200
     (Link Data) Network Mask: 255.255.255.252
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000

                Router Link States (Area 0.0.0.1)

  Routing Bit Set on this LSA
  LS age: 787
  Options: (No TOS-capability, No DC)
  LS Type: Router Links
  Link State ID: 10.1.0.91
  Advertising Router: 10.1.0.91
  LS Seq Number: 80006666
  Checksum: 0x210d
  Length: 288
  Area Border Router
   Number of Links: 22

    Link connected to: another Router (point-to-point)
     (Link ID) Neighboring Router ID: 10.0.24.6
     (Link Data) Router Interface address: 10.0.60.206
      Number of TOS metrics: 0
       TOS 0 Metrics: 9000
       
RP/0/RP0/CPU0:router-1#show ospf database summary 

            OSPF Router with ID (10.1.2.2) (Process ID 1)

                Summary Net Link States (Area 0.0.0.0)

  LS age: 1639
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.1
  LS Seq Number: 800030eb
  Checksum: 0x899d
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 2312 

  LS age: 427
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.24.2
  LS Seq Number: 800030eb
  Checksum: 0xad74
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1806 

  LS age: 1695
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.192
  LS Seq Number: 800030eb
  Checksum: 0xd081
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 1312 

  Routing Bit Set on this LSA
  LS age: 581
  Options: (No TOS-capability, No DC)
  LS Type: Summary Links (Network)
  Link State ID: 10.1.0.1 (Summary Network Number)
  Advertising Router: 10.0.25.193
  LS Seq Number: 800030eb
  Checksum: 0xf458
  Length: 28
  Network Mask: /32
        TOS: 0  Metric: 806 
        
RP/0/RSP0/CPU0:router-1#show ospf database external 

            OSPF Router with ID (10.3.22.75) (Process ID 10)

                Type-5 AS External Link States

  Routing Bit Set on this LSA
  LS age: 1009
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.3.22.190
  LS Seq Number: 80000519
  Checksum: 0x9009
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  LS age: 520
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 0.0.0.0 (External Network Number)
  Advertising Router: 10.3.25.22
  LS Seq Number: 80001b96
  Checksum: 0x3279
  Length: 36
  Network Mask: /0
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 1 
        Forward Address: 0.0.0.0
        External Route Tag: 10

  Routing Bit Set on this LSA
  LS age: 90
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.0.0 (External Network Number)
  Advertising Router: 10.3.20.95
  LS Seq Number: 8003494f
  Checksum: 0x1d4d
  Length: 36
  Network Mask: /8
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 0.0.0.0
        External Route Tag: 0

  Routing Bit Set on this LSA
  LS age: 1251
  Options: (No TOS-capability, DC)
  LS Type: AS External Link
  Link State ID: 10.0.2.0 (External Network Number)
  Advertising Router: 10.3.22.83
  LS Seq Number: 800079c3
  Checksum: 0x5d2e
  Length: 36
  Network Mask: /24
        Metric Type: 2 (Larger than any link state path)
        TOS: 0 
        Metric: 20 
        Forward Address: 10.4.209.161
        External Route Tag: 0
    """
    template = get_template(path="misc/N2G/ospf_lsdb/Cisco_IOSXR.txt")
    # print(template)
    parser = ttp(template=template)
    parser.add_input(data1)
    parser.add_input(data2)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [
        [
            {
                "OSPF_PROCESSES": {
                    "1": {
                        "external_lsa": [
                            {
                                "mask": "0",
                                "metric": "1",
                                "metric_type": "2",
                                "originator_rid": "10.3.22.190",
                                "subnet": "0.0.0.0",
                                "tag": "10",
                            },
                            {
                                "mask": "0",
                                "metric": "1",
                                "metric_type": "2",
                                "originator_rid": "10.3.25.22",
                                "subnet": "0.0.0.0",
                                "tag": "10",
                            },
                            {
                                "mask": "8",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.3.20.95",
                                "subnet": "10.0.0.0",
                                "tag": "0",
                            },
                            {
                                "mask": "24",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.3.22.83",
                                "subnet": "10.0.2.0",
                                "tag": "0",
                            },
                        ],
                        "local_rid": "10.1.2.2",
                        "router_lsa": [
                            {
                                "area": "0.0.0.0",
                                "asbr": True,
                                "bma_peers": [
                                    {
                                        "link_data": "10.3.162.14",
                                        "link_id": "10.3.162.13",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "10.3.162.10",
                                        "link_id": "10.3.162.9",
                                        "metric": "1",
                                    },
                                ],
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.61.0",
                                        "metric": "9100",
                                    }
                                ],
                                "originator_rid": "10.1.0.91",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.0.61.1",
                                        "link_id": "10.1.1.251",
                                        "metric": "9100",
                                    },
                                    {
                                        "link_data": "10.0.61.94",
                                        "link_id": "10.1.2.6",
                                        "metric": "65535",
                                    },
                                    {
                                        "link_data": "0.0.1.220",
                                        "link_id": "10.1.2.7",
                                        "metric": "3000",
                                    },
                                ],
                            },
                            {
                                "area": "0.0.0.0",
                                "asbr": True,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.61.96",
                                        "metric": "9000",
                                    }
                                ],
                                "originator_rid": "10.1.0.92",
                                "ptp_peers": [
                                    {
                                        "link_data": "0.0.2.5",
                                        "link_id": "10.1.2.6",
                                        "metric": "1100",
                                    },
                                    {
                                        "link_data": "0.0.2.67",
                                        "link_id": "10.1.2.8",
                                        "metric": "3000",
                                    },
                                    {
                                        "link_data": "0.0.2.69",
                                        "link_id": "10.1.2.7",
                                        "metric": "3000",
                                    },
                                ],
                            },
                        ],
                        "summary_lsa": [
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "2312",
                                "originator_rid": "10.0.24.1",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "1806",
                                "originator_rid": "10.0.24.2",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "1312",
                                "originator_rid": "10.0.25.192",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "806",
                                "originator_rid": "10.0.25.193",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.32",
                                "mask": "32",
                                "metric": "2312",
                                "originator_rid": "10.0.24.1",
                                "subnet": "10.1.0.1",
                            },
                        ],
                    }
                },
                "vars": {"hostname": "router-1"},
            },
            {
                "OSPF_PROCESSES": {
                    "1": {
                        "local_rid": "10.1.2.2",
                        "router_lsa": [
                            {
                                "area": "0.0.0.0",
                                "asbr": True,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.60.204",
                                        "metric": "9000",
                                    },
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.60.196",
                                        "metric": "9000",
                                    },
                                ],
                                "originator_rid": "10.1.0.91",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.0.60.206",
                                        "link_id": "10.0.24.6",
                                        "metric": "9000",
                                    },
                                    {
                                        "link_data": "10.0.60.197",
                                        "link_id": "10.1.0.92",
                                        "metric": "9000",
                                    },
                                ],
                            },
                            {
                                "area": "0.0.0.0",
                                "asbr": True,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.60.108",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.0.60.200",
                                        "metric": "9000",
                                    },
                                ],
                                "originator_rid": "10.1.0.92",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.0.60.109",
                                        "link_id": "10.0.24.31",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "10.0.60.201",
                                        "link_id": "10.0.24.5",
                                        "metric": "9000",
                                    },
                                ],
                            },
                            {
                                "area": "0.0.0.1",
                                "asbr": True,
                                "originator_rid": "10.1.0.91",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.0.60.206",
                                        "link_id": "10.0.24.6",
                                        "metric": "9000",
                                    }
                                ],
                            },
                        ],
                        "summary_lsa": [
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "2312",
                                "originator_rid": "10.0.24.1",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "1806",
                                "originator_rid": "10.0.24.2",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "1312",
                                "originator_rid": "10.0.25.192",
                                "subnet": "10.1.0.1",
                            },
                            {
                                "area": "0.0.0.0",
                                "mask": "32",
                                "metric": "806",
                                "originator_rid": "10.0.25.193",
                                "subnet": "10.1.0.1",
                            },
                        ],
                    },
                    "10": {
                        "external_lsa": [
                            {
                                "mask": "0",
                                "metric": "1",
                                "metric_type": "2",
                                "originator_rid": "10.3.22.190",
                                "subnet": "0.0.0.0",
                                "tag": "10",
                            },
                            {
                                "mask": "0",
                                "metric": "1",
                                "metric_type": "2",
                                "originator_rid": "10.3.25.22",
                                "subnet": "0.0.0.0",
                                "tag": "10",
                            },
                            {
                                "mask": "8",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.3.20.95",
                                "subnet": "10.0.0.0",
                                "tag": "0",
                            },
                            {
                                "mask": "24",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.3.22.83",
                                "subnet": "10.0.2.0",
                                "tag": "0",
                            },
                        ],
                        "local_rid": "10.3.22.75",
                    },
                },
                "vars": {"hostname": "router-1"},
            },
        ]
    ]


# test_N2G_ospf_Cisco_IOSXR()
