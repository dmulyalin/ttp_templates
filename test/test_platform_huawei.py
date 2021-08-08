import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


def test_huwei_display_ospf_lsdb_router():
    with open("./mock_data/huawei_display_ospf_lsdb_router.txt", "r") as f:
        data = f.read()
    template = get_template(platform="huawei", command="display ospf lsdb router")
    # print(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    # pprint.pprint(res)
    assert res == [
        [
            {
                "ospf_processes": {
                    "123": {
                        "local_rid": "123.123.24.158",
                        "router_lsa": [
                            {
                                "area": "0.0.0.123",
                                "originator_rid": "10.123.0.91",
                                "ptp_peers": [
                                    {
                                        "link_data": "123.123.60.206",
                                        "link_id": "123.123.24.6",
                                        "metric": "9000",
                                    },
                                    {
                                        "link_data": "123.123.1.220",
                                        "link_id": "10.123.2.7",
                                        "metric": "3000",
                                    },
                                ],
                            },
                            {
                                "area": "0.0.0.123",
                                "connected_stub": [
                                    {
                                        "link_data": "255.255.255.252",
                                        "link_id": "123.123.60.108",
                                        "metric": "1",
                                    }
                                ],
                                "originator_rid": "10.123.0.92",
                                "ptp_peers": [
                                    {
                                        "link_data": "123.123.60.109",
                                        "link_id": "123.123.24.31",
                                        "metric": "1",
                                    },
                                    {
                                        "link_data": "123.123.60.201",
                                        "link_id": "123.123.24.5",
                                        "metric": "9000",
                                    },
                                ],
                            },
                        ],
                    }
                }
            }
        ]
    ]


# test_huwei_display_ospf_lsdb_router()
