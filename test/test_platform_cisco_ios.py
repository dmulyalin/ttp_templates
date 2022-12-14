import sys
import pprint
import logging

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp

logging.basicConfig(level=logging.INFO)

def test_cisco_ios_show_isdn_status():
    with open(
        "./mock_data/cisco_ios_show_isdn_status.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="cisco_ios", command="show isdn status"
    )
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [[
            {
                "interface": [
                    {
                        "CES": "1",
                        "FREE_CHANNEL_MASK": "0x80000003",
                        "INTERFACE": "Serial0/3/0:23",
                        "ISDN_SWITCHTYPE": "primary-ni",
                        "L1_STATUS": "ACTIVE",
                        "L2_DISCARDS": "0",
                        "L2_SESSION_ID": "1",
                        "SAPI": "0",
                        "TEI_CODE": "0",
                        "TEI_STATE": "MULTIPLE_FRAME_ESTABLISHED"
                    },
                    {
                        "CES": "1",
                        "FREE_CHANNEL_MASK": "0x80000003",
                        "INTERFACE": "BRI0/1/0",
                        "ISDN_SWITCHTYPE": "basic-net3",
                        "L1_STATUS": "ACTIVE",
                        "SAPI": "0",
                        "TEI_CODE": "0",
                        "TEI_STATE": "MULTIPLE_FRAME_ESTABLISHED"
                    },
                    {
                        "CES": "1",
                        "FREE_CHANNEL_MASK": "0x80000003",
                        "INTERFACE": "BRI0/1/1",
                        "ISDN_SWITCHTYPE": "basic-net3",
                        "L1_STATUS": "ACTIVE",
                        "SAPI": "0",
                        "TEI_CODE": "0",
                        "TEI_STATE": "MULTIPLE_FRAME_ESTABLISHED"
                    },
                    {
                        "CES": "1",
                        "FREE_CHANNEL_MASK": "0x80000003",
                        "INTERFACE": "BRI0/2/0",
                        "ISDN_SWITCHTYPE": "basic-net3",
                        "L1_STATUS": "DEACTIVATED",
                        "SAPI": "0",
                        "TEI_CODE": "0",
                        "TEI_STATE": "MULTIPLE_FRAME_ESTABLISHED"
                    },
                    {
                        "CES": "1",
                        "FREE_CHANNEL_MASK": "0x80000003",
                        "INTERFACE": "BRI0/2/1",
                        "ISDN_SWITCHTYPE": "basic-net3",
                        "L1_STATUS": "ACTIVE",
                        "SAPI": "0",
                        "TEI_CODE": "0",
                        "TEI_STATE": "MULTIPLE_FRAME_ESTABLISHED"
                    }
                ]
            }
        ]]


def test_cisco_ios_show_ip_ospf_database_router():
    with open(
        "./mock_data/cisco_ios_show_ip_ospf_database_router_IOL4_ABR.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="cisco_ios", command="show ip ospf database router"
    )
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [
        [
            {
                "ospf_processes": {
                    "1": {
                        "local_rid": "10.0.0.4",
                        "router_lsa": [
                            {
                                "area": "0",
                                "asbr": False,
                                "bma_peers": [
                                    {
                                        "link_data": "10.1.117.3",
                                        "link_id": "10.1.117.7",
                                        "metric": "10",
                                    }
                                ],
                                "originator_rid": "10.0.0.3",
                            },
                            {
                                "area": "0",
                                "asbr": False,
                                "bma_peers": [
                                    {
                                        "link_data": "10.1.117.4",
                                        "link_id": "10.1.117.7",
                                        "metric": "10",
                                    }
                                ],
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.128",
                                        "link_id": "10.1.14.0",
                                        "metric": "10",
                                    }
                                ],
                                "originator_rid": "10.0.0.4",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.1.14.4",
                                        "link_id": "10.0.0.10",
                                        "metric": "10",
                                    }
                                ],
                            },
                            {
                                "area": "0",
                                "asbr": False,
                                "bma_peers": [
                                    {
                                        "link_data": "10.1.117.7",
                                        "link_id": "10.1.117.7",
                                        "metric": "10",
                                    }
                                ],
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.255",
                                        "link_id": "10.0.0.7",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.1.107.0",
                                        "metric": "10",
                                    },
                                    {
                                        "link_data": "255.255.255.0",
                                        "link_id": "10.1.37.0",
                                        "metric": "10",
                                    },
                                ],
                                "originator_rid": "10.0.0.7",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.1.107.2",
                                        "link_id": "10.0.0.10",
                                        "metric": "10",
                                    }
                                ],
                            },
                            {
                                "area": "0",
                                "asbr": True,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.255",
                                        "link_id": "10.0.0.10",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "10.1.107.0",
                                        "metric": "10",
                                    },
                                    {
                                        "link_data": "255.255.255.128",
                                        "link_id": "10.1.14.0",
                                        "metric": "10",
                                    },
                                ],
                                "originator_rid": "10.0.0.10",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.1.107.1",
                                        "link_id": "10.0.0.7",
                                        "metric": "10",
                                    },
                                    {
                                        "link_data": "10.1.14.1",
                                        "link_id": "10.0.0.4",
                                        "metric": "10",
                                    },
                                ],
                            },
                            {
                                "area": "100",
                                "asbr": False,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.254",
                                        "link_id": "10.1.45.2",
                                        "metric": "10",
                                    }
                                ],
                                "originator_rid": "10.0.0.4",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.1.45.2",
                                        "link_id": "10.0.5.101",
                                        "metric": "10",
                                    }
                                ],
                            },
                            {
                                "area": "100",
                                "asbr": True,
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.254",
                                        "link_id": "10.1.45.2",
                                        "metric": "10",
                                    }
                                ],
                                "originator_rid": "10.0.5.101",
                                "ptp_peers": [
                                    {
                                        "link_data": "10.1.45.3",
                                        "link_id": "10.0.0.4",
                                        "metric": "10",
                                    }
                                ],
                            },
                        ],
                    }
                }
            }
        ]
    ]


# test_cisco_ios_show_ip_ospf_database_router()


def test_cisco_ios_show_ip_ospf_database_external():
    with open(
        "./mock_data/cisco_ios_show_ip_ospf_database_external_IOL4_ABR.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="cisco_ios", command="show ip ospf database external"
    )
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [
        [
            {
                "ospf_processes": {
                    "1": {
                        "external_lsa": [
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.0.10",
                                "subnet": "10.0.0.100",
                                "tag": "0",
                            },
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.0.10",
                                "subnet": "10.0.0.101",
                                "tag": "0",
                            },
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.0.10",
                                "subnet": "10.0.0.102",
                                "tag": "0",
                            },
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.0.10",
                                "subnet": "10.0.0.103",
                                "tag": "0",
                            },
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.5.101",
                                "subnet": "10.0.5.100",
                                "tag": "0",
                            },
                            {
                                "mask": "32",
                                "metric": "20",
                                "metric_type": "2",
                                "originator_rid": "10.0.5.101",
                                "subnet": "10.0.5.101",
                                "tag": "0",
                            },
                        ],
                        "local_rid": "10.0.0.4",
                    }
                }
            }
        ]
    ]


# test_cisco_ios_show_ip_ospf_database_external()


def test_cisco_ios_show_ip_ospf_database_summary():
    with open(
        "./mock_data/cisco_ios_show_ip_ospf_database_summary_IOL4_ABR.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="cisco_ios", command="show ip ospf database summary"
    )
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [
        [
            {
                "ospf_processes": {
                    "1": {
                        "local_rid": "10.0.0.4",
                        "summary_lsa": [
                            {
                                "area": "0",
                                "mask": "31",
                                "metric": "10",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.1.45.2",
                            },
                            {
                                "area": "100",
                                "mask": "32",
                                "metric": "11",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.0.0.7",
                            },
                            {
                                "area": "100",
                                "mask": "32",
                                "metric": "11",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.0.0.10",
                            },
                            {
                                "area": "100",
                                "mask": "25",
                                "metric": "10",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.1.14.0",
                            },
                            {
                                "area": "100",
                                "mask": "24",
                                "metric": "20",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.1.37.0",
                            },
                            {
                                "area": "100",
                                "mask": "30",
                                "metric": "20",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.1.107.0",
                            },
                            {
                                "area": "100",
                                "mask": "24",
                                "metric": "10",
                                "originator_rid": "10.0.0.4",
                                "subnet": "10.1.117.0",
                            },
                        ],
                    }
                }
            }
        ]
    ]


# test_cisco_ios_show_ip_ospf_database_summary()

def test_cisco_ios_cisco_ios_show_running_config_pipe_include_source_static():
    data = """
ip nat inside source static 10.10.10.10 3.3.3.3 extendable
ip nat inside source static tcp 192.168.1.10 443 3.3.4.4 443 vrf VRF1000 extendable
ip nat inside source static 192.168.2.10 3.3.4.5 vrf VRF1002 extendable
ip nat inside source static tcp 192.168.3.10 3389 3.3.5.6 13389 extendable
ip nat inside source static 20.20.20.20 6.6.6.6 extendable
ip nat inside source static tcp 30.30.30.30 443 interface TenGigabitEthernet0/0/0 1443
    """
    template = get_template(
        platform="cisco_ios", command="show running-config | include source static"
    )
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [[{'nat': {'static': [{'global_ip': '3.3.3.3',
                                         'inside_ip': '10.10.10.10',
                                         'location': 'inside'},
                                        {'global_ip': '3.3.4.4',
                                         'global_port': 443,
                                         'inside_ip': '192.168.1.10',
                                         'inside_port': 443,
                                         'location': 'inside',
                                         'protocol': 'tcp',
                                         'vrf': 'VRF1000'},
                                        {'global_ip': '3.3.4.5',
                                         'inside_ip': '192.168.2.10',
                                         'location': 'inside',
                                         'vrf': 'VRF1002'},
                                        {'global_ip': '3.3.5.6',
                                         'global_port': 13389,
                                         'inside_ip': '192.168.3.10',
                                         'inside_port': 3389,
                                         'location': 'inside',
                                         'protocol': 'tcp'},
                                        {'global_ip': '6.6.6.6',
                                         'inside_ip': '20.20.20.20',
                                         'location': 'inside'},
                                        {'global_port': 1443,
                                         'inside_ip': '30.30.30.30',
                                         'inside_port': 443,
                                         'interface': 'TenGigabitEthernet0/0/0',
                                         'location': 'inside',
                                         'protocol': 'tcp'}]}}]]

# test_cisco_ios_cisco_ios_show_running_config_pipe_include_source_static()
