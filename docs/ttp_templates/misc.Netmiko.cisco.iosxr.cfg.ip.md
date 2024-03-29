Reference path:
```
ttp://misc/Netmiko/cisco.iosxr.cfg.ip.txt
```

---



Template to parse "show running-config interface" output.
This template produces one dictionary item per IP address configured 
on device's interfaces including secondary and VRRP/HSRP IP addresses.

Output is a list of dictionaries. 

Sample data:
```
RP/0/RP0/CPU0:r1#show running-config interface
interface Bundle-Ether1
 description Description of interface
 ipv4 address 10.1.2.54 255.255.255.252
 ipv6 address fd00:1:2::31/126
!
interface Loopback123
 description VRF 123
 vrf VRF-1123
 ipv4 address 10.1.0.10 255.255.255.255
!
RP/0/RP0/CPU0:r1#show running-config router vrrp
router vrrp
 interface GigabitEthernet0/0/0/48
  address-family ipv4
   vrrp 1
    address 1.1.1.1
   !
  !
  address-family ipv6
   vrrp 1
    address global fd::1
!
RP/0/RP0/CPU0:r1#show running-config router hsrp 
router hsrp
 interface GigabitEthernet0/0/0/22
  address-family ipv4
   hsrp 1
    address 3.3.3.3
   !
  !
  address-family ipv6
   hsrp 1
    address global fd::3
```

Sample results, structure="flat_list":
```
[
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.7.89.55",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    },
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.7.89.56",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    }
]
```
 
Template can be invoked using Netmiko `run_ttp` method like this:

```
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.ip.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)
```

How this template works:

1. Parses output from device using group with name="intf_lookup**.{{ interface }}" to 
form interfaces lookup table and record description with VRF
2. Interfaces IP addresses parsed next using group name="intf" adding info about interface 
using intf_lookup lookup table
3. VRRP VIP parsed, adding info about interface using intf_lookup lookup table
4. HSRP VIP parsed, adding info about interface using intf_lookup lookup table

This is sample structure produced after above parsing finishes:
```
[{'intf': [{'interface': 'Bundle-Ether1'}, {'interface': 'Loopback123'}],
  'intf_lookup': {'Bundle-Ether1': {'description': 'Description of interface',
                                    'vrf': 'customer_1'},
                  'Loopback123': {'description': 'VRF 123', 'vrf': 'VRF-1123'}},
  'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '10.1.2.54',
          'mask': '255.255.255.252',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd00:1:2::31',
          'mask': '126',
          'vrf': 'customer_1'},
         {'description': 'VRF 123',
          'hostname': 'r1',
          'interface': 'Loopback123',
          'ipv4': '10.1.0.10',
          'mask': '255.255.255.255',
          'vrf': 'VRF-1123'}]},
 {'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '1.1.1.1',
          'vip': True,
          'vip_type': 'VRRP',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd::1',
          'vip': True,
          'vip_type': 'VRRP',
          'vrf': 'customer_1'}],
  'vrrp': {'vrrp_intf': {'interface': 'Bundle-Ether1'}}},
 {'hsrp': {'hsrp_intf': {'interface': 'Bundle-Ether1'}},
  'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '3.3.3.3',
          'vip': True,
          'vip_type': 'HSRP',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd::3',
          'vip': True,
          'vip_type': 'HSRP',
          'vrf': 'customer_1'}]}]
```
          
Above structure passed through output with "process" macro function to transform results into a list of IP
address dictionaries such as:
```
[{'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '10.1.2.54',
  'mask': '255.255.255.252',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd00:1:2::31',
  'mask': '126',
  'vrf': 'customer_1'},
 {'description': 'VRF 123',
  'hostname': 'r1',
  'interface': 'Loopback123',
  'ipv4': '10.1.0.10',
  'mask': '255.255.255.255',
  'vrf': 'VRF-1123'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '1.1.1.1',
  'vip': True,
  'vip_type': 'VRRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd::1',
  'vip': True,
  'vip_type': 'VRRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '3.3.3.3',
  'vip': True,
  'vip_type': 'HSRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd::3',
  'vip': True,
  'vip_type': 'HSRP',
  'vrf': 'customer_1'}]
```



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "show running-config interface" output.
This template produces one dictionary item per IP address configured 
on device's interfaces including secondary and VRRP/HSRP IP addresses.

Output is a list of dictionaries. 

Sample data:
'''
RP/0/RP0/CPU0:r1#show running-config interface
interface Bundle-Ether1
 description Description of interface
 ipv4 address 10.1.2.54 255.255.255.252
 ipv6 address fd00:1:2::31/126
!
interface Loopback123
 description VRF 123
 vrf VRF-1123
 ipv4 address 10.1.0.10 255.255.255.255
!
RP/0/RP0/CPU0:r1#show running-config router vrrp
router vrrp
 interface GigabitEthernet0/0/0/48
  address-family ipv4
   vrrp 1
    address 1.1.1.1
   !
  !
  address-family ipv6
   vrrp 1
    address global fd::1
!
RP/0/RP0/CPU0:r1#show running-config router hsrp 
router hsrp
 interface GigabitEthernet0/0/0/22
  address-family ipv4
   hsrp 1
    address 3.3.3.3
   !
  !
  address-family ipv6
   hsrp 1
    address global fd::3
'''

Sample results, structure="flat_list":
'''
[
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.7.89.55",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    },
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.7.89.56",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    }
]
'''
 
Template can be invoked using Netmiko 'run_ttp' method like this:

'''
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.ip.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)
'''

How this template works:

1. Parses output from device using group with name="intf_lookup**.{{ interface }}" to 
form interfaces lookup table and record description with VRF
2. Interfaces IP addresses parsed next using group name="intf" adding info about interface 
using intf_lookup lookup table
3. VRRP VIP parsed, adding info about interface using intf_lookup lookup table
4. HSRP VIP parsed, adding info about interface using intf_lookup lookup table

This is sample structure produced after above parsing finishes:
'''
[{'intf': [{'interface': 'Bundle-Ether1'}, {'interface': 'Loopback123'}],
  'intf_lookup': {'Bundle-Ether1': {'description': 'Description of interface',
                                    'vrf': 'customer_1'},
                  'Loopback123': {'description': 'VRF 123', 'vrf': 'VRF-1123'}},
  'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '10.1.2.54',
          'mask': '255.255.255.252',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd00:1:2::31',
          'mask': '126',
          'vrf': 'customer_1'},
         {'description': 'VRF 123',
          'hostname': 'r1',
          'interface': 'Loopback123',
          'ipv4': '10.1.0.10',
          'mask': '255.255.255.255',
          'vrf': 'VRF-1123'}]},
 {'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '1.1.1.1',
          'vip': True,
          'vip_type': 'VRRP',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd::1',
          'vip': True,
          'vip_type': 'VRRP',
          'vrf': 'customer_1'}],
  'vrrp': {'vrrp_intf': {'interface': 'Bundle-Ether1'}}},
 {'hsrp': {'hsrp_intf': {'interface': 'Bundle-Ether1'}},
  'ip': [{'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv4': '3.3.3.3',
          'vip': True,
          'vip_type': 'HSRP',
          'vrf': 'customer_1'},
         {'description': 'Description of interface',
          'hostname': 'r1',
          'interface': 'Bundle-Ether1',
          'ipv6': 'fd::3',
          'vip': True,
          'vip_type': 'HSRP',
          'vrf': 'customer_1'}]}]
'''
          
Above structure passed through output with "process" macro function to transform results into a list of IP
address dictionaries such as:
'''
[{'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '10.1.2.54',
  'mask': '255.255.255.252',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd00:1:2::31',
  'mask': '126',
  'vrf': 'customer_1'},
 {'description': 'VRF 123',
  'hostname': 'r1',
  'interface': 'Loopback123',
  'ipv4': '10.1.0.10',
  'mask': '255.255.255.255',
  'vrf': 'VRF-1123'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '1.1.1.1',
  'vip': True,
  'vip_type': 'VRRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd::1',
  'vip': True,
  'vip_type': 'VRRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv4': '3.3.3.3',
  'vip': True,
  'vip_type': 'HSRP',
  'vrf': 'customer_1'},
 {'description': 'Description of interface',
  'hostname': 'r1',
  'interface': 'Bundle-Ether1',
  'ipv6': 'fd::3',
  'vip': True,
  'vip_type': 'HSRP',
  'vrf': 'customer_1'}]
'''
</doc>



<input>
commands = ["show running-config interface"]
# need to keep prompt for "gethostname" to work
kwargs = {
    "strip_prompt": False,
    "strip_command": False
}
</input>

<input name="vrrp_cfg">
commands = ["show running-config router vrrp"]
</input>

<input name="hsrp_cfg">
commands = ["show running-config router hsrp"]
</input>

<vars>
hostname="gethostname"

set_all = [
    "set(hostname)",
    "set(interface)",
    "lookup(group='intf_lookup', key='interface', update=True)"
]
</vars>

<group name="intf_lookup**.{{ interface }}">
interface {{ interface | resuball("short_interface_names") }}
 description {{ description | re(".+") }}
 vrf {{ vrf | default("default") }}
</group>

<group name="intf" record="interface">
interface {{ interface | resuball("short_interface_names") }}
 <group name="/ip*" chain="set_all" method="table">
 ipv4 address {{ ipv4 | IP | _exact_ }} {{ mask4 }}
 ipv4 address {{ ipv4 | IP | _exact_ | let("secondary", True) }} {{ mask4 }} secondary
 ipv6 address {{ ipv6 | IPV6 | _exact_ }}/{{ mask6 }}
 </group>
! {{ _end_ }}
</group>

<group name="vrrp" input="vrrp_cfg">
router vrrp {{ _start_ }}
 <group name="vrrp_intf" record="interface">
 interface {{ interface | resuball("short_interface_names") }}
    <group name="/ip*" chain="set_all" method="table">
    address {{ ipv4 | IP | let("vip", True) | let("vip_type", "VRRP") }}
    address global {{ ipv6 | IPV6 | let("vip", True) | let("vip_type", "VRRP") }}
    </group>
 </group>
! {{ _end_ }}
</group>

<group name="hsrp" input="hsrp_cfg">
router hsrp {{ _start_ }}
 <group name="hsrp_intf" record="interface">
 interface {{ interface | resuball("short_interface_names") }}
    <group name="/ip*" chain="set_all" method="table">
    address {{ ipv4 | IP | let("vip", True) | let("vip_type", "HSRP") }}
    address global {{ ipv6 | IPV6 | let("vip", True) | let("vip_type", "HSRP") }}
    </group>
 </group>
! {{ _end_ }}
</group>

<output macro="process"/>

<macro>
def process(data):
    ret = []
    for input_res_item in data:
        ret.extend(input_res_item.get("ip", []))
    return ret
</macro>
```
</details>