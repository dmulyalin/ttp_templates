Reference path:
```
ttp://misc/N2G/cli_ip_data/huawei.txt
```

---



Template to parse Huawei interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="huawei" results="per_template">

<doc>
Template to parse Huawei interfaces configuration and ARP cache.
</doc>

<input load="python">
commands = [
    "display current-configuration interface",
    "display arp all",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["huawei", "huawei_vrpv8"]
</input>

<vars>local_hostname="gethostname"</vars>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | resuball("IfsNormalize") }}
 description {{ port_description | re(".+") }}
 ip binding vpn-instance {{ vrf }}
 <group name="ip_addresses*" chain="add_network()" method="table">
 ip address {{ ip | IP }} {{ netmask }}
 ip address {{ ip | IP }} {{ netmask }} sub
 ipv6 address {{ ip | IPV6 }}/{{ netmask }}
 ipv6 address {{ ip | IPV6 }}/{{ netmask }} sub
 </group>
 <group name="fhrp*" method="table">
 vrrp vrid {{ group | let("type", "VRRP") }} virtual-ip {{ ip | IP }}
 </group>
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }}   {{ mac | MAC | mac_eui }}  {{ expire | re("\\d+") }}  {{ type | notdigit }}  {{ interface | resuball("IfsNormalize") }}   {{ vrf }}
{{ ip | IP }}   {{ mac | MAC | mac_eui }}                             {{ type | notdigit }}  {{ interface | resuball("IfsNormalize") }}   {{ vrf }}
{{ ip | IP }}   {{ mac | MAC | mac_eui }}  {{ expire | re("\\d+") }}  {{ type | notdigit }}  {{ interface | resuball("IfsNormalize") }}
{{ ip | IP }}   {{ mac | MAC | mac_eui }}                             {{ type | notdigit }}  {{ interface | resuball("IfsNormalize") }}
</group>

</template>
```
</details>