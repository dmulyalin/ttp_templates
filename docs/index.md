
---

**Templates count: 67**

---

[![Downloads](https://pepy.tech/badge/ttp_templates)](https://pepy.tech/project/ttp_templates)
[![PyPI versions](https://img.shields.io/pypi/pyversions/ttp.svg)](https://pypi.python.org/pypi/ttp_templates/)

# Template Text Parser Templates

This repository contains a collection of [TTP](https://github.com/dmulyalin/ttp) templates.

If you solved a problem using TTP and feel that your work can be useful to other people, feel
free to raise an issue or submit pull request to include your template(s) in this repository.
Refer to [Contribute Guide](https://dmulyalin.github.io/ttp_templates/contribute/) for details.

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

This repository contains four collections of templates corresponding to folder names:

* `platform` collection - mimics [ntc-templates](https://github.com/networktocode/ntc-templates) API and follows same naming rule
* `yang` collection - contains templates capable of producing YANG compatible structures out of text data
* `misc` collection - miscellaneous templates for various use cases organized in folders
* `get` collection - getter templates that return normalised, platform-agnostic output, similar in purpose to [NAPALM getters](https://napalm.readthedocs.io/en/latest/base.html)

Sample code to retrieve normalised inventory using the `inventory` getter. Getters work like
NAPALM getters: one template bundles platform-specific parsing logic and returns a unified
structure regardless of vendor. The `platform` argument is **required** when using a getter —
it selects the correct platform-specific input inside the getter template.
<details><summary>Code</summary>

```python
from ttp_templates import parse_output
import pprint

# Cisco IOS-XR "show inventory" raw CLI output
data = """
NAME: "Chassis", DESCR: "Cisco ASR 9006 4-slot Line Card Chassis"
PID: ASR-9006-SYS    , VID: V07, SN: FOX1234ABCD

NAME: "0/RSP0/CPU0", DESCR: "Route Switch Processor"
PID: A9K-RSP440-TR   , VID: V04, SN: FOX5678EFGH
"""

# platform routes data to the "cisco_xr" input inside inventory.txt;
# the getter normalises results from all supported platforms into the same structure.
result = parse_output(data=data, get="inventory", platform="cisco_xr")

pprint.pprint(result)
# prints:
# [[{'description': 'Cisco ASR 9006 4-slot Line Card Chassis',
#    'module': 'ASR-9006-SYS',
#    'serial': 'FOX1234ABCD',
#    'slot': 'Chassis'},
#   {'description': 'Route Switch Processor',
#    'module': 'A9K-RSP440-TR',
#    'serial': 'FOX5678EFGH',
#    'slot': '0/RSP0/CPU0'}]]
```
</details>

### Platform collection templates files naming rule

`{{ vendor_os }}_{{ command_with_underscores }}.txt` - lower case only.

Naming rules details:

* All space symbols `' '` replaced with underscores.
* Pipe symbol `|` replaced with `pipe` in template name. For example,
  template to parse Cisco IOS `show run | section interface` command output
  must be named `cisco_ios_show_running_config_pipe_section_interface.txt`
* Dash symbols `-` replaced with underscores. For example, template to parse
  Huawei `display current-configuration interface` command output  must be
  named `huawei_display_current_configuration_interface.txt`

### YANG collection templates files naming rule

`{{ YANG module name }}_{{ platform_name }}.txt` - lower case only

Naming rules details:

* All space symbols `' '` replaced with underscore.
* Dash symbol `-` **does not** replaced with underscore. For example, template
  to produce output compatible with openconfig-lldp YANG model for Cisco IOS
  must be named `openconfig-lldp_cisco_xr.txt`

### Misc collection templates files naming rule

`{{ usecase folder }}/{{ template name }}.txt` - upper or lower case

Naming rules details:

* Nothing replaced with anything, provided template name used as is.

### Get collection templates files naming rule

`{{ getter_name }}.txt` - lower case only, one file per logical getter.

Naming rules details:

* Each file name describes a single getter function, e.g. `inventory.txt`, `interfaces.txt`, `facts.txt`.
* A getter template uses TTP `<extend>` directives to compose platform-specific `platform/` templates
  and expose their results under a unified, platform-agnostic structure.
* Each platform-specific input inside the getter must declare a `platform` list in its `<input>` block
  so `parse_output` can route data to the correct input.
* Getter templates are loaded with `get_template(get="inventory")` or
  `parse_output(data=..., get="inventory", platform="cisco_xr")` — the `.txt` extension is optional.
  `platform` is mandatory for `parse_output` so the getter can route data to the correct input.

## Additional Templates Resources

List of resources with TTP templates:

- TTP SrosParser - https://pypi.org/project/ttp-sros-parser/ by [h4ndzdatm0ld](https://github.com/h4ndzdatm0ld)
- Template for parsing "show run" for Cisco IOS - https://github.com/tbotnz/ios-show-run-ttp by [tbotnz](https://github.com/tbotnz)
- Template for Cisco ASA configuration - https://github.com/consentfactory/ttp-cisco-asa-template by [consentfactory](https://gist.github.com/consentfactory)
  - (gist for historical purposes) https://gist.github.com/consentfactory/85872fc83453d1735b15aed3e47a9763
