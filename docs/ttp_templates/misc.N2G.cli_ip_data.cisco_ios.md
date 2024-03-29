Reference path:
```
ttp://misc/N2G/cli_ip_data/cisco_ios.txt
```

---



Template to parse Cisco IOS interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="cisco_ios" results="per_template">

<doc>
Template to parse Cisco IOS interfaces configuration and ARP cache.
</doc>

<input load="python">
commands = [
    "show running-config",
    "show ip arp",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["cisco_ios"]
</input>

<vars>local_hostname="gethostname"</vars>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | resuball("IfsNormalize") }}
 description {{ port_description | re(".+") }}
 vrf forwarding {{ vrf }}
 ip vrf forwarding {{ vrf }}
 ip access-group {{ ACL_IN }} in
 ip access-group {{ ACL_OUT }} out
 <group name="ip_addresses*" chain="add_network()" method="table">
 ip address {{ ip | IP }} {{ netmask }}
 ip address {{ ip | IP }} {{ netmask }} secondary
 </group>
 <group name="fhrp*" method="table">
 standby {{ group | let("type", "HSRP") }}  {{ ip | IP }}
 vrrp {{ group | let("type", "VRRP") }} ip {{ ip | IP }}
 </group>
! {{ _end_ }}
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
Internet  {{ ip | IP }}     {{ age }}   {{ mac | MAC | mac_eui }}  {{ type }}   {{ interface | resuball("IfsNormalize") }}
</group>

</template>
```
</details>