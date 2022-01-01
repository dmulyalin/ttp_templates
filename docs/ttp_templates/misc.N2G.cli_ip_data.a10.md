Reference path:
```
ttp://misc/N2G/cli_ip_data/a10.txt
```

---



Template to parse A10 devices interfaces configuration and IP ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="a10" results="per_template">

<doc>
Template to parse A10 devices interfaces configuration and IP ARP cache.
</doc>

<vars>local_hostname="gethostname"</vars>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | PHRASE | resuball("IfsNormalize") }}
  description {{ port_description | re(".+") }}
  <group name="ip_addresses*" chain="add_network()" method="table">
  ip address {{ ip | IP }} {{ netmask }}
  </group>
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }}  {{ mac | MAC | mac_eui }}  Dynamic  {{ age }}    {{ interface | PHRASE | resuball("IfsNormalize") }}  {{ vlan }} 
</group>

</template>
```
</details>