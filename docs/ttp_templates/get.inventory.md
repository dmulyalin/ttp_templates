Reference path:
```
ttp://get/inventory.txt
```

---



Template to parse Cisco IOS XR inventory.

This template requires output of 'show inventory' command.



Template to parse Arista inventory.

This template requires output of 'show inventory' command.



Template to parse Cisco NX-OS inventory.

This template requires output of 'show inventory' command.



Template to parse Juniper inventory.

This template requires output of 'show inventory' command.



---

<details><summary>Template Content</summary>
```
<template name="inventory" results="per_template">
<doc>
Getter template to parse inventory for network devices. Designed to work with 
[Network Automation Fabric](https://docs.norfablabs.com/) 
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/) 
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Cisco IOS-XR
- Cisco NXOS
- Arista EOS
- Juniper Junos

Returns normalized list of dictionaries, each dictionary has these keys:

- 'description' - description of module/inventory item
- 'module' - PID of the module/inventory item
- 'serial' - serial number of the module/inventory item
- 'slot' - name of the parent slot housing module/inventory item

Example data returned by template (YAML):

'''yaml
- description: "ASR9K Route Switch Processor with 440G/slot Fabric and 6GB"
  slot: "module 0/RSP0/CPU0"
  module: "A9K-RSP440-TR"
  serial: "M9YXCZV9QF"
- description: "ASR-9006 Fan Tray V2"
  slot: "fantray 0/FT0/SP"
  module: "ASR-9006-FAN-V2"
  serial: "PDANV9GYV8H"
- description: "ASR9K Generic Fan"
  slot: "fan0 0/FT0/SP"
  module: "N/A"
  serial: ""
'''

</doc>

<extend template="ttp://platform/cisco_xr_show_inventory.txt"/>

<extend template="ttp://platform/arista_eos_show_inventory_pipe_json.txt"/>

<extend template="ttp://platform/cisco_nxos_show_inventory_pipe_json_pretty.txt"/>

<extend template="ttp://platform/juniper_junos_show_chassis_hardware_pipe_json.txt"/>

</template>
```
</details>