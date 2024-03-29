Reference path:
```
ttp://misc/ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt
```

---



This template produces one dictionary item per ip address configured on device's interfaces including secondary and VRRP IPs. Output is a list of dictionaries.

Sample data:
```
r1#show run | sec interface
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.56 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
```

Sample results, structure="flat_list":
```
[
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.223.89.55",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    },
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.223.89.56",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    }
]
```

How to use::
```
    from ttp import ttp
	from ttp_templates import get_template
    from pprint import pprint
    
	data = "text output from device"
	
    parser = ttp(
		template=get_template(misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt")
	)
    parser.add_input(data, template_name="interfaces")
    parser.parse()
    pprint(parser.result())
```	



---

<details><summary>Template Content</summary>
```
<template name="interfaces" results="per_template">
<doc>
This template produces one dictionary item per ip address configured on device's interfaces including secondary and VRRP IPs. Output is a list of dictionaries.

Sample data:
'''
r1#show run | sec interface
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.56 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
'''

Sample results, structure="flat_list":
'''
[
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.223.89.55",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    },
    {
        "description": "description",
        "hostname": "r1",
        "interface": "GigabitEthernet1",
        "ip": "10.223.89.56",
        "mask": "255.255.255.0",
        "vrf": "MGMT"
    }
]
'''

How to use::
'''
    from ttp import ttp
	from ttp_templates import get_template
    from pprint import pprint
    
	data = "text output from device"
	
    parser = ttp(
		template=get_template(misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt")
	)
    parser.add_input(data, template_name="interfaces")
    parser.parse()
    pprint(parser.result())
'''	
</doc>

<input>
commands = [
    "show run | sec interface"
]
</input>

<vars>
hostname="gethostname"

record_all = [
    "record(interface)",
    "record(description)",
    "record(vrf)",
    "void()"
]

set_all = [
    "set(interface)",
    "set(description)",
    "set(vrf)",
    "set(hostname)"
]
</vars>

<group name="intf_cfg" chain="record_all">
interface {{ interface }}
 description {{ description | ORPHRASE }}
 vrf forwarding {{ vrf }}
 <group name="/" chain="set_all" method="table">
 ip address {{ ip }} {{ mask }}
 ip address {{ ip | let("secondary", True) }} {{ mask }} secondary
 vrrp 1 ip {{ ip | let("vrrp vip", True) }}
 vrrp 1 ip {{ ip | let("vrrp vip", True) | let("secondary", True) }} secondary
 </group>
</group>
</template>
```
</details>