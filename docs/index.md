
---

**Templates count: 50**

---

[![Downloads](https://pepy.tech/badge/ttp_templates)](https://pepy.tech/project/ttp_templates)
[![PyPI versions](https://img.shields.io/pypi/pyversions/ttp.svg)](https://pypi.python.org/pypi/ttp_templates/)

# Template Text Parser Templates

This repository contains a collection of [TTP](https://github.com/dmulyalin/ttp) templates.

If you solved a problem using TTP and feel that your work can be 
useful to other people, feel free to raise an issue or submit pull request to 
include your template(s) in this repository.

Documentation: [https://dmulyalin.github.io/ttp_templates/](https://dmulyalin.github.io/ttp_templates/)

Repository: [https://github.com/dmulyalin/ttp_templates](https://github.com/dmulyalin/ttp_templates)

TTP: [https://ttp.readthedocs.io/](https://ttp.readthedocs.io/)

## Installation

From PyPi:

`pip install ttp-templates`

or latest from GitHub master branch (need Git installed on the system):

`pip install git+https://github.com/dmulyalin/ttp_templates.git`
 
## Sample usage

This example demonstrates how to parse `Test Platform` output for `show run | sec interface` command using `platform/test_platform_show_run_pipe_sec_interface.txt` template.
<details><summary>Code</summary>

```python
from ttp_templates import parse_output
import pprint

data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
"""

result = parse_output(
    data=data,
    platform="Test Platform",
    command="show run | sec interface"
)

pprint.pprint(result)

# prints:
# [[[{'description': 'Customer #32148',
#     'disabled': True,
#     'dot1q': '251',
#     'interface': 'GigabitEthernet1/3.251',
#     'ip': '172.16.33.10',
#     'mask': '255.255.255.128'},
#    {'description': 'Customer #32148',
#     'disabled': True,
#     'dot1q': '251',
#     'interface': 'GigabitEthernet1/3.251',
#     'ip': '172.16.33.10',
#     'mask': '255.255.255.128'}]]]
```
</details>

Sample code to parse `Cisco IOS` output in a structure compatible with `ietf-interfaces` YANG module.
<details><summary>Code</summary>

```python
from ttp_templates import get_template
from ttp import ttp
import pprint

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
parser = ttp(template=template)

parser.add_input(data1)
parser.add_input(data2)

parser.parse()
res = parser.result()
pprint.pprint(res)

# prints:
# [{'comment': '',
#   'exception': {},
#   'result': [{'ietf-interfaces:interfaces': {'interface': [{'admin-status': 'down',
#                                                             'description': 'Customer '
#                                                                            '#32148',
#                                                             'enabled': False,
#                                                             'ietf-ip:ipv4': {'address': [{'ip': '172.16.33.10',
#                                                                                           'netmask': '255.255.255.128',
#                                                                                           'origin': 'static'}]},
#                                                             'if-index': 1,
#                                                             'link-up-down-trap-enable': 'enabled',
#                                                             'name': 'GigabitEthernet1/3.251',
#                                                             'oper-status': 'unknown',
#                                                             'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
#                                                             'type': 'iana-if-type:ethernetCsmacd'},
#                                                            {'admin-status': 'up',
#                                                             'description': 'vCPEs '
#                                                                            'access '
#                                                                            'control',
#                                                             'enabled': True,
#                                                             'ietf-ip:ipv4': {'address': [{'ip': '172.16.33.10',
#                                                                                           'netmask': '255.255.255.128',
#                                                                                           'origin': 'static'}]},
#                                                             'if-index': 1,
#                                                             'link-up-down-trap-enable': 'enabled',
#                                                             'name': 'GigabitEthernet1/4',
#                                                             'oper-status': 'unknown',
#                                                             'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
#                                                             'type': 'iana-if-type:ethernetCsmacd'}]}},
#              {'ietf-interfaces:interfaces': {'interface': [{'admin-status': 'up',
#                                                             'description': 'Works '
#                                                                            'data',
#                                                             'enabled': True,
#                                                             'ietf-ip:ipv4': {'mtu': 9000},
#                                                             'if-index': 1,
#                                                             'link-up-down-trap-enable': 'enabled',
#                                                             'name': 'GigabitEthernet1/5',
#                                                             'oper-status': 'unknown',
#                                                             'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
#                                                             'type': 'iana-if-type:ethernetCsmacd'},
#                                                            {'admin-status': 'up',
#                                                             'description': 'Works '
#                                                                            'data '
#                                                                            'v6',
#                                                             'enabled': True,
#                                                             'ietf-ip:ipv6': {'address': [{'ip': '2001::1',
#                                                                                           'origin': 'static',
#                                                                                           'prefix-length': 64},
#                                                                                          {'ip': '2001:1::1',
#                                                                                           'origin': 'static',
#                                                                                           'prefix-length': 64}]},
#                                                             'if-index': 1,
#                                                             'link-up-down-trap-enable': 'enabled',
#                                                             'name': 'GigabitEthernet1/7',
#                                                             'oper-status': 'unknown',
#                                                             'statistics': {'discontinuity-time': '1970-01-01T00:00:00+00:00'},
#                                                             'type': 'iana-if-type:ethernetCsmacd'}]}}],
#   'valid': {0: True, 1: True}}]
```
</details>


## How templates collections structured

This repository contains three collections of templates corresponding to folder names:

* `platform` collection - mimics [ntc-templates](https://github.com/networktocode/ntc-templates) API and follows same naming rule
* `yang` collection - contains templates capable of producing YANG compatible structures out of text data
* `misc` collection - miscellaneous templates for various use cases organized in folders

**Platform collection templates files naming rule**

`{{ vendor_os }}_{{ command_with_underscores }}.txt` - lower case only

**YANG collection templates files naming rule**

`{{ YANG module name }}_{{ platform_name }}.txt` - lower case only

**Misc collection templates files naming rule**

`{{ usecase folder }}/{{ template name }}.txt` - upper or lower case

## Additional Template resources

List of resources with TTP templates:

- TTP SrosParser - https://pypi.org/project/ttp-sros-parser/ by [h4ndzdatm0ld](https://github.com/h4ndzdatm0ld)
- Template for parsing "show run" for Cisco IOS - https://github.com/tbotnz/ios-show-run-ttp by [tbotnz](https://github.com/tbotnz)
- Template for Cisco ASA configuration - https://gist.github.com/consentfactory/85872fc83453d1735b15aed3e47a9763 by [consentfactory](https://gist.github.com/consentfactory)