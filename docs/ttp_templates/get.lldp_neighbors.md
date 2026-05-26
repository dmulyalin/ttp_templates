Reference path:
```
ttp://get/lldp_neighbors.txt
```

---



Normalizes Arista EOS LLDP neighbors JSON to flat list format.

Transforms nested lldpNeighbors structure into standardized dictionaries with:

- One record per (local_interface, remote_neighbor) pair
- Consistent field naming

Returns normalized list of dictionaries, each dictionary has these keys:

- `interface` - local interface on which the LLDP neighbor was discovered
- `remote_device` - system name of the remote LLDP neighbor
- `remote_interface` - port ID of the remote neighbor interface
- `remote_system_description` - system description string advertised by the remote neighbor
- `remote_chassi_id` - chassis ID of the remote neighbor
- `remote_interface_description` - port description advertised by the remote neighbor interface, or `null` if none
- `remote_device_management_ip` - first management IP address advertised by the remote neighbor, or `null` if none




Normalizes Juniper JunOS LLDP neighbors JSON to flat list format.

Transforms the nested lldp-neighbors-information/lldp-neighbor-information structure
returned by 'show lldp neighbors detail | display json' into standardized dictionaries with:

- One record per (local_interface, remote_neighbor) pair
- Consistent field naming matching the Arista EOS LLDP neighbor output format

Returns normalized list of dictionaries, each dictionary has these keys:

- `interface` - local interface on which the LLDP neighbor was discovered
- `remote_device` - system name of the remote LLDP neighbor
- `remote_interface` - port ID of the remote neighbor interface
- `remote_system_description` - system description string advertised by the remote neighbor
- `remote_chassi_id` - chassis ID of the remote neighbor
- `remote_interface_description` - port description advertised by the remote neighbor interface, or `null` if none
- `remote_device_management_ip` - first management IP address advertised by the remote neighbor, or `null` if none




---

<details><summary>Template Content</summary>
```
<template name="lldp_neighbors" results="per_template">
<doc>
Getter template to parse LLDP neighbors for network devices. Designed to work with 
[Network Automation Fabric](https://docs.norfablabs.com/) 
[Nornir Service](https://docs.norfablabs.com/workers/nornir/services_nornir_service/) 
[parse TTP task](https://docs.norfablabs.com/workers/nornir/services_nornir_service_tasks_parse/)

Supported platforms:

- Arista EOS
- Juniper Junos

Returns normalized list of dictionaries, each dictionary has these keys:

- 'interface' - local interface on which the LLDP neighbor was discovered
- 'remote_device' - system name of the remote LLDP neighbor
- 'remote_interface' - port ID of the remote neighbor interface
- 'remote_system_description' - system description string advertised by the remote neighbor
- 'remote_chassi_id' - chassis ID of the remote neighbor
- 'remote_interface_description' - port description advertised by the remote neighbor interface, or 'null' if none
- 'remote_device_management_ip' - first management IP address advertised by the remote neighbor, or 'null' if none

</doc>

<extend template="ttp://platform/arista_eos_show_lldp_neighbors_detail_pipe_json.txt"/>

<extend template="ttp://platform/juniper_junos_show_lldp_neighbors_detail_pipe_display_json.txt"/>

</template>
```
</details>