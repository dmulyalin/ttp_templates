Reference path:
```
ttp://misc/N2G/cli_ip_data/arista_eos.txt
```

---



Template to parse Arista EOS interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="arista_eos" results="per_template">

<doc>
Template to parse Arista EOS interfaces configuration and ARP cache.
</doc>

<input load="python">
commands = [
    "show running-config",
    "show ip arp vrf all",
]
method = "send_command"
platform = ["arista_eos"]
</input>

<!-- Extract Device Hostname -->
<group name="nill" void="">
hostname {{ local_hostname | record("local_hostname") }}
</group>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | resuball("IfsNormalize") }}
   description {{ port_description | re(".+") }}
   vrf {{ vrf }}
   <group name="ip_addresses*" chain="add_network()" method="table">
   ip address {{ ip | IP }}/{{ netmask }}
   ip address {{ ip | IP }}/{{ netmask }} secondary
   </group>
! {{ _end_ }}
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }}   {{ age }}   {{ mac | MAC | mac_eui }}   {{ interface | resuball("IfsNormalize") }}
</group>

</template>
```
</details>