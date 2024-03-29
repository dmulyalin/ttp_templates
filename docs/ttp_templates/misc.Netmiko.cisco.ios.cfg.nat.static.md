Reference path:
```
ttp://misc/Netmiko/cisco.ios.cfg.nat.static.txt
```

---



Template to parse Cisco IOS `show run | include source static` command output
Using Netmiko run_ttp method.

Extends template: `ttp://platform/cisco_ios_show_running_config_pipe_include_source_static.txt`

Code to invoke this template Netmiko `run_ttp` method:

```
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.nat.static.txt")
```


GitHub Issue: https://github.com/dmulyalin/ttp_templates/issues/1

Author: Denis Mulyalin in cooperation with abhi1693

Template to parse Cisco IOS `show run | include source static` command output.

Template's YANG model (not tested):

```
module nat {

    yang-version 1.1;
    namespace "ttp://platform/cisco_ios_show_running_config_pipe_include_source_static.txt";
    prefix nat;
    revision "2022-May-04" { description "Initial Revision"; }
    description "Template to parse Cisco IOS static NAT configuration";
    
    list static {
        key inside_ip;
        leaf inside_ip {
            type string;
        }
        leaf location { 
            type string;
        }
        leaf global_ip {
            type string;
        }
        leaf interface {
            type string;
        }
        leaf inside_port {
            type uint32;
        }
        leaf global_port {
            type uint32;
        }
        leaf vrf {
            type string;
        }
    }
}
```

Sample data:

```
ip nat inside source static 10.10.10.10 3.3.3.3 extendable
ip nat inside source static tcp 192.168.1.10 443 3.3.4.4 443 vrf VRF1000 extendable
ip nat inside source static 192.168.2.10 3.3.4.5 vrf VRF1002 extendable
ip nat inside source static tcp 192.168.3.10 3389 3.3.5.6 13389 extendable
ip nat inside source static 20.20.20.20 6.6.6.6 extendable
ip nat inside source static tcp 30.30.30.30 443 interface TenGigabitEthernet0/0/0 1443
```

Expected output:

```
[
    {
        "nat": {
            "static": [
                {
                    "global_ip": "3.3.3.3",
                    "inside_ip": "10.10.10.10",
                    "location": "inside"
                },
                {
                    "global_ip": "3.3.4.4",
                    "global_port": 443,
                    "inside_ip": "192.168.1.10",
                    "inside_port": 443,
                    "location": "inside",
                    "protocol": "tcp",
                    "vrf": "VRF1000"
                },
                {
                    "global_ip": "3.3.4.5",
                    "inside_ip": "192.168.2.10",
                    "location": "inside",
                    "vrf": "VRF1002"
                },
                {
                    "global_ip": "3.3.5.6",
                    "global_port": 13389,
                    "inside_ip": "192.168.3.10",
                    "inside_port": 3389,
                    "location": "inside",
                    "protocol": "tcp"
                },
                {
                    "global_ip": "6.6.6.6",
                    "inside_ip": "20.20.20.20",
                    "location": "inside"
                },
                {
                    "global_port": 1443,
                    "inside_ip": "30.30.30.30",
                    "inside_port": 443,
                    "interface": "TenGigabitEthernet0/0/0",
                    "location": "inside",
                    "protocol": "tcp"
                }
            ]
        }
    }
]
```



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse Cisco IOS 'show run | include source static' command output
Using Netmiko run_ttp method.

Extends template: 'ttp://platform/cisco_ios_show_running_config_pipe_include_source_static.txt'

Code to invoke this template Netmiko 'run_ttp' method:

'''
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.nat.static.txt")
'''
</doc>


<input>
commands = [
    "show running-config | include source static"
]
</input>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_include_source_static.txt"/>
```
</details>