Reference path:
```
ttp://platform/juniper_junos_show_lldp_neighbors_detail_pipe_display_json.txt
```

---



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
<template name="juniper_junos_lldp_neighbors" results="per_template">
<doc>
Normalizes Juniper JunOS LLDP neighbors JSON to flat list format.

Transforms the nested lldp-neighbors-information/lldp-neighbor-information structure
returned by 'show lldp neighbors detail | display json' into standardized dictionaries with:

- One record per (local_interface, remote_neighbor) pair
- Consistent field naming matching the Arista EOS LLDP neighbor output format

Returns normalized list of dictionaries, each dictionary has these keys:

- 'interface' - local interface on which the LLDP neighbor was discovered
- 'remote_device' - system name of the remote LLDP neighbor
- 'remote_interface' - port ID of the remote neighbor interface
- 'remote_system_description' - system description string advertised by the remote neighbor
- 'remote_chassi_id' - chassis ID of the remote neighbor
- 'remote_interface_description' - port description advertised by the remote neighbor interface, or 'null' if none
- 'remote_device_management_ip' - first management IP address advertised by the remote neighbor, or 'null' if none

</doc>

<macro>
def transform_lldp_neighbors_to_records(json_data):
    from ttp_templates.utils.juniper_junos_process_show_lldp_neighbors_detail_pipe_display_json import transform_lldp_neighbors

    return transform_lldp_neighbors(json_data)
</macro>

<input>
commands = [
    "show lldp neighbors detail | display json"
]
platform = [
    "juniper_junos", # scrapli and netmiko
    "junos", # NAPALM
]
</input>

<group>
{ {{ _start_ }}
{{ data | _line_ | joinmatches }}
} {{ _end_ }}
</group>

<output macro="transform_lldp_neighbors_to_records"/>

</template>

```
</details>