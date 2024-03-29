Reference path:
```
ttp://misc/Netmiko/cisco.iosxr.arp.txt
```

---



TTP template to parse Cisco IOS XR "show arp vrf all" output with Netmiko. 

Template can be invoked using Netmiko run_ttp method like this:
```
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
	device_type="cisco_xr",
	host="1.2.3.4",
	username="admin",
	password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.iosxr.arp.txt", res_kwargs={"structure": "flat_list"})

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
#  {'age': '-',
#   'interface': 'Vlan21',
#   'ip': '172.29.50.3',
#   'mac': '00:24:f7:dd:77:41',
#   'protocol': 'Internet',
#   'type': 'ARPA'}]
```


TTP template to parse Cisco IOS XR "show arp vrf all" output. 



---

<details><summary>Template Content</summary>
```
<doc>
TTP template to parse Cisco IOS XR "show arp vrf all" output with Netmiko. 

Template can be invoked using Netmiko run_ttp method like this:
'''
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
	device_type="cisco_xr",
	host="1.2.3.4",
	username="admin",
	password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.iosxr.arp.txt", res_kwargs={"structure": "flat_list"})

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
#  {'age': '-',
#   'interface': 'Vlan21',
#   'ip': '172.29.50.3',
#   'mac': '00:24:f7:dd:77:41',
#   'protocol': 'Internet',
#   'type': 'ARPA'}]
'''
</doc>


<input>
commands = [
    "show arp vrf all"
]
</input>

<extend template="ttp://platform/cisco_xr_show_arp_vrf_all.txt"/>
```
</details>