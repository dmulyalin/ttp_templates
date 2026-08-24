Reference path:
```
ttp://platform/cisco_xr_show_lldp_neighbors_detail.txt
```

---



Normalizes Cisco IOS-XR `show lldp neighbors detail` output to flat list format.

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
<template name="cisco_xr_lldp_neighbors" results="per_template">
<doc>
Normalizes Cisco IOS-XR 'show lldp neighbors detail' output to flat list format.

Returns normalized list of dictionaries, each dictionary has these keys:

- 'interface' - local interface on which the LLDP neighbor was discovered
- 'remote_device' - system name of the remote LLDP neighbor
- 'remote_interface' - port ID of the remote neighbor interface
- 'remote_system_description' - system description string advertised by the remote neighbor
- 'remote_chassi_id' - chassis ID of the remote neighbor
- 'remote_interface_description' - port description advertised by the remote neighbor interface, or 'null' if none
- 'remote_device_management_ip' - first management IP address advertised by the remote neighbor, or 'null' if none

</doc>

<input>
commands = [
    "show lldp neighbors detail"
]
platform = [
    "cisco_xr", # netmiko
    "iosxr", # NAPALM
    "cisco_iosxr", # scrapli
]
</input>

<macro>
def transform_lldp_neighbors_to_records(payload):
    from ttp_templates.utils.cisco_xr_process_show_lldp_neighbors_detail import (
        transform_lldp_neighbors,
    )

    return transform_lldp_neighbors(payload)
</macro>

<group name="neighbors*">
Local Interface: {{ interface | _start_ }}
Chassis id: {{ remote_chassi_id }}
Port id: {{ remote_interface | ORPHRASE }}
Port Description: {{ remote_interface_description | re(".+") }}
System Name: {{ remote_device | re(".+") }}
  IPv4 address: {{ ipv4_address }}
  IPv6 address: {{ ipv6_address }}

<group name="_">
System Description: {{ _start_ }}
{{ remote_system_description | _line_ | strip | joinmatches(" ") }}
Time remaining: {{ ignore }} seconds {{ _end_ }}
</group>

</group>

<output macro="transform_lldp_neighbors_to_records"/>

</template>

```
</details>