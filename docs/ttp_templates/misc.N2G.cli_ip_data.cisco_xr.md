Reference path:
```
ttp://misc/N2G/cli_ip_data/cisco_xr.txt
```

---



Template to parse Cisco IOSXR interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="cisco_xr" results="per_template">

<doc>
Template to parse Cisco IOSXR interfaces configuration and ARP cache.
</doc>

<vars>local_hostname="gethostname"</vars>

<group record="local_hostname" void="">
hostname {{ local_hostname }}
</group>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | resuball("IfsNormalize") }}
 description {{ port_description | re(".+") }}
 vrf {{ vrf }}
 <group name="ip_addresses*" chain="add_network()" method="table">
 ipv4 address {{ ip | IP }} {{ netmask }}
 ipv4 address {{ ip | IP }} {{ netmask }} secondary
 </group>
! {{ _end_ }}
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | MAC| mac_eui }}  {{ ignore }}  {{ ignore }} {{ interface | resuball("IfsNormalize") }}
</group>

</template>
```
</details>