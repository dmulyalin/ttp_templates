import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


def test_juniper_juniper_show_isis_database_verbose_pipe_no_more():
    with open(
        "./mock_data/juniper_show_isis_database_verbose_pipe_no_more.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="juniper", command="show isis database verbose | no-more"
    )
    # print(template)
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
                                          
# test_juniper_juniper_show_isis_database_verbose_pipe_no_more()