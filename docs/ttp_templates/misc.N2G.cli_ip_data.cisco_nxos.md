Reference path:
```
ttp://misc/N2G/cli_ip_data/cisco_nxos.txt
```

---



Template to parse Cisco NXOS interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos" results="per_template">

<doc>
Template to parse Cisco NXOS interfaces configuration and ARP cache.
</doc>

<input load="python">
commands = [
    "show running-config",
    "show ip arp",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["nxos_ssh", "cisco_nxos"]
</input>

<vars>local_hostname="gethostname"</vars>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}">
interface {{ interface | resuball("IfsNormalize") }}
  description {{ port_description | re(".+") }}
  vrf member {{ vrf }}
  ip access-group {{ ACL_IN }} in
  ip access-group {{ ACL_OUT }} out
 <group name="ip_addresses*" chain="add_network()" method="table">
  ip address {{ ip | IP }}/{{ netmask }}
  ip address {{ ip | IP }}/{{ netmask }} secondary
 </group>
 <group name="fhrp*" method="table">
  <group>
  hsrp {{ group | let("type", "HSRP") }}  
    ip {{ ip | IP }}
  </group>
  <group>
  vrrpv3 {{ group | let("type", "VRRP") }} address-family ipv4
    address {{ ip | IP }} primary
  </group>
 </group>
! {{ _end_ }}
</group>

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }}    {{ age }}  {{ mac | MAC | mac_eui }}  {{ interface | resuball("IfsNormalize") }}
{{ ip | IP }}    {{ age }}  {{ mac | MAC | mac_eui }}  {{ interface | resuball("IfsNormalize") }}  *
</group>

</template>
```
</details>