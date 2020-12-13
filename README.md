# Template Text Parser Templates

This repository contains a collection of [TTP](https://github.com/dmulyalin/ttp) templates.

Templates developed by community. If you come across problem that 
you was able to solve using TTP and feel that your work can be 
useful to other people, do not hesitate to raise an issue or submit 
pull request to include your template in this repository.


## Sample usage

A couple of examples.

<details><summary>This example demonstrates how to parse `Test Platform` output for `show run | sec interface` command using `platform/test_platform_show_run_pipe_sec_interface.txt` template.</summary>

```python
from ttp import ttp
from ttp_templates import parse_output

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

<details><summary>Sample code to parse `Cisco IOS` output in a structure compatible with `ietf-interfaces` YANG module</summary>

```python
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


# How templates collections structured

This repository contains three collections corresponding to folder names:

* platform - mimics [ntc-templates](https://github.com/networktocode/ntc-templates) API and follows same naming rule - `{{ vendor_os }}_{{ command_with_underscores }}.txt` - lower case only
* yang - contains templates capable of producing YANG compatible structures out of text data, naming `{{ YANG module name}}_{{ platform_name}}.txt` - lower case only
* misc - miscellaneous templates for various usecases organized in folders, naming - `{{ usecase folder }}/{{ template name }}.txt` - upper or lower case

# API reference

Function `ttp_templates.parse_output`:
```
Function to load template text and parse data provided

**Attributes**

* data (str) - data to parse
* path (str) - OS path to template to load
* platform (str) - name of the platform to load template for
* command (str) - command to load template for
* yang (str) - name of YANG module to load template for
* misc (str) - OS path to template within repository misc folder    
* structure (str) - results structure list, dictionary or flat_list
* template_vars (dict) - variables to load in template object

**Valid combinations of template location**

``path`` attribute is always more preferred

* ``path="./misc/foo/bar.txt"`` 
* ``platfrom="cisco_ios", command="show version"``
* ``yang="ietf-interfaces", platform="cisco_ios"``
* ``misc="foo_folder/bar_template.txt"`` 
```

Function `ttp_templates.get_template`:
```
Function to locate template file and return it's content

**Attributes**

* path (str) - OS path to template to load
* platform (str) - name of the platform to load template for
* command (str) - command to load template for
* yang (str) - name of YANG module to load template for
* misc (str) - OS path to template within repository misc folder    

**Valid combinations of template location**

``path`` attribute is always more preferred

* ``path="./misc/foo/bar.txt"`` 
* ``platfrom="cisco_ios", command="show version"``
* ``yang="ietf-interfaces", platform="cisco_ios"``
* ``misc="foo_folder/bar_template.txt"`` 
```	
	
# Contributions
Feel free to submit an issue, report a bug or ask a question, feature requests are welcomed.

It is always good idea to document as much as you can and give context on the problem you was 
trying to solve. TTP templates have ``<doc>`` tag exactly for that.