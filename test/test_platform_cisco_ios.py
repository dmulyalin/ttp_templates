import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


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
