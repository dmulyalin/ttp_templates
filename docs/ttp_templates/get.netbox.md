Reference path:
```
ttp://get/netbox.txt
```

---



Template to parse Arista EOS configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'show running-config' command.



Template to parse Cisco NXOS configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'show running-config' command.



Template to parse Cisco IOS-XR configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of `show running-config` command.



Template to parse Juniper Junos configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'show configuration | display set' command.



Template to parse Opengear configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of `config -g config` command.



---

<details><summary>Template Content</summary>
```
<template name="netbox" results="per_template">
<doc>
Getter template to parse various data from network devices for import into Netbox. 
Designed to work with [Network Automation Fabric](https://docs.norfablabs.com/) 
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/) 
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Cisco IOS-XR
- Cisco NXOS
- Arista EOS
- Juniper Junos
- Opengear

Returns normalized dictionary.

</doc>

<extend template="ttp://misc/Netbox/parse_arista_eos_config.txt"/>

<extend template="ttp://misc/Netbox/parse_cisco_nxos_config.txt"/>

<extend template="ttp://misc/Netbox/parse_cisco_xr_config.txt"/>

<extend template="ttp://misc/Netbox/parse_juniper_junos_config.txt"/>

<extend template="ttp://misc/Netbox/parse_opengear_config.txt"/>

</template>
```
</details>