Reference path:
```
ttp://misc/Netmiko/cisco.ios.cfg.ip.txt
```

---



Template to parse "show running-config | section interface" output.
This template produces one dictionary item per IP address configured
on device's interfaces including secondary and VRRP/HSRP IP addresses. 

Output is a list of dictionaries. 

Sample data:

```
r1#show run | sec interface
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.7.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.7.89.56 255.255.255.0
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
  
Template can be invoked using Netmiko run_ttp method like this:

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



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "show running-config | section interface" output.
This template produces one dictionary item per IP address configured
on device's interfaces including secondary and VRRP/HSRP IP addresses. 

Output is a list of dictionaries. 

Sample data:

'''
r1#show run | sec interface
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.7.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.7.89.56 255.255.255.0
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
  
Template can be invoked using Netmiko run_ttp method like this:

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
</doc>

<input>
commands = [
    "show running-config | section interface"
]
# need to keep prompt for "gethostname" to work
kwargs = {
    "strip_prompt": False,
    "strip_command": False
}
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

<group chain="record_all">
interface {{ interface | resuball("short_interface_names") }}
 description {{ description | re(".+") }}
 vrf forwarding {{ vrf | default("default") }}
 <group name="/" chain="set_all" method="table">
 ip address {{ ipv4 | IP }} {{ mask }}
 ip address {{ ipv4 | IP | let("secondary", True) }} {{ mask }} secondary
 ipv6 address {{ ipv6 | IPV6 | _exact_ }}/{{ mask }}
 vrrp 1 ip  {{ ipv4 | IP | let("vip", True) | let("vip_type", "VRRP") }}
 standby 1 ip {{ ipv4 | IP | let("vip", True) | let("vip_type", "HSRP") }}
 </group>
! {{ _end_ }}
</group>
```
</details>