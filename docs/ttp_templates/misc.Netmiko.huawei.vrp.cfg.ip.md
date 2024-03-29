Reference path:
```
ttp://misc/Netmiko/huawei.vrp.cfg.ip.txt
```

---



Template to parse "display current-configuration interface" output.
This template produces one dictionary item per IP address configured 
on device's interfaces including secondary and VRRP IP addresses. 

Output is a list of dictionaries. 

Sample data:
```
Huawei-box-1-dis cur interface
interface Eth-Trunk1.100
 vlan-type dot1q 100
 mtu 9600
 description Link description  here
 ip address 10.1.130.2 255.255.255.252
 ip binding vpn-instance VRF1
 vrrp6 vrid 1 virtual-ip 2001:db8::100
#
```
   
Sample results, structure="flat_list":
```
[
    {
        "description": "description",
        "hostname": "Huawei-box-1",
        "interface": "Eth-Trunk1.100",
        "ip": "10.1.130.2",
        "mask": "255.255.255.252",
        "vrf": "VRF1"
    }
]
```
  
Template supports Netmiko run_ttp method:
```
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="huawei",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/huawei.vrp.cfg.ip.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)

# prints something along the lines of:
# 
```



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "display current-configuration interface" output.
This template produces one dictionary item per IP address configured 
on device's interfaces including secondary and VRRP IP addresses. 

Output is a list of dictionaries. 

Sample data:
'''
Huawei-box-1-dis cur interface
interface Eth-Trunk1.100
 vlan-type dot1q 100
 mtu 9600
 description Link description  here
 ip address 10.1.130.2 255.255.255.252
 ip binding vpn-instance VRF1
 vrrp6 vrid 1 virtual-ip 2001:db8::100
#
'''
   
Sample results, structure="flat_list":
'''
[
    {
        "description": "description",
        "hostname": "Huawei-box-1",
        "interface": "Eth-Trunk1.100",
        "ip": "10.1.130.2",
        "mask": "255.255.255.252",
        "vrf": "VRF1"
    }
]
'''
  
Template supports Netmiko run_ttp method:
'''
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="huawei",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/huawei.vrp.cfg.ip.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)

# prints something along the lines of:
# 
'''
</doc>



<input>
commands = [
    "display current-configuration interface"
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
 ip binding vpn-instance {{ vrf | default("default") }}
 <group name="/" chain="set_all" method="table">
 ip address {{ ipv4 | IP }} {{ mask }}
 ip address {{ ipv4 | IP | let("secondary", True) }} {{ mask }} sub
 ipv6 address {{ ipv6 | IPV6 | _exact_ }}/{{ mask }}
 vrrp vrid 1 virtual-ip {{ ipv4 | IP | let("vip", True) | let("vip_type", "VRRP") }}
 vrrp6 vrid 1 virtual-ip {{ ipv6 | IPV6 | let("vip", True) | let("vip_type", "VRRP") | _exact_ }}
 </group>
# {{ _end_ }}
</group>

```
</details>