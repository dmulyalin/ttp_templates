import sys
import pprint
import logging

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp

logging.basicConfig(level=logging.INFO)

def test_show_hostname():
    with open(
        "./mock_data/arista_eos_show_hostname.txt", "r"
    ) as f:
        data = f.read()
    template = get_template(
        platform="arista_eos", command="show hostname"
    )
    pprint.pprint(template)
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    pprint.pprint(res)
    assert res == [[[{'fqdn': 'ceos1', 'hostname': 'ceos1'}]]]