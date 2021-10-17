Reference path:
```
ttp://misc/Netmiko/cisco.ios.arp.txt
```

---



TTP template to parse Cisco IOS "show ip arp" output.

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

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.arp.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)

# prints something along the lines of:
# [{'age': 8,
#   'ip': '172.29.50.1',
#   'mac': '84:b8:02:76:ac:0e',
#   'protocol': 'Internet',
#   'type': 'ARPA'},
#  {'age': 221,
#   'interface': 'Vlan20',
#   'ip': '172.29.50.2',
#   'mac': '00:19:07:25:34:4a',
#   'protocol': 'Internet',
#   'type': 'ARPA'},
#  {'age': -1,
#   'interface': 'Vlan21',
#   'ip': '172.29.50.3',
#   'mac': '00:24:f7:dd:77:41',
#   'protocol': 'Internet',
#   'type': 'ARPA'}]
```


TTP Template to parse Cisco IOS "show ip arp output".

This template produces list of dictionaries results where each
dictionary item compatible to this model:
```
module arp-table {

yang-version 1.1;

namespace
  "ttp://platform/cisco_ios_show_ip_arp";
  
list entry {
        config false;
        key "ip";
        
        leaf protocol {
            type string;
        }
        
        leaf ip {
            type string;
            mandatory true;
            description
                "IP address";
        }

        leaf age {
            type uint32;
            description
                "IP address";
        }

        leaf mac {
            type string;
            mandatory "true";
            description
                "MAC address";
        }    

        leaf type {
            type string;
        }

        leaf interface {
            type string;
            default "Uncknown";
			mandatory false;
            description
                "Interface name";
        }        
    }
}
```

Sample instance data:
```
TBD
```



---

<details><summary>Template Content</summary>
```
<doc>
TTP template to parse Cisco IOS "show ip arp" output.

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

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.arp.txt", res_kwargs={"structure": "flat_list"})

pprint.pprint(res)

# prints something along the lines of:
# [{'age': 8,
#   'ip': '172.29.50.1',
#   'mac': '84:b8:02:76:ac:0e',
#   'protocol': 'Internet',
#   'type': 'ARPA'},
#  {'age': 221,
#   'interface': 'Vlan20',
#   'ip': '172.29.50.2',
#   'mac': '00:19:07:25:34:4a',
#   'protocol': 'Internet',
#   'type': 'ARPA'},
#  {'age': -1,
#   'interface': 'Vlan21',
#   'ip': '172.29.50.3',
#   'mac': '00:24:f7:dd:77:41',
#   'protocol': 'Internet',
#   'type': 'ARPA'}]
'''
</doc>


<input>
commands = [
    "show ip arp"
]
</input>

<extend template="ttp://platform/cisco_ios_show_ip_arp.txt"/>
```
</details>