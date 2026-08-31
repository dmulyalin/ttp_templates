Reference path:
```
ttp://platform/a10_show_lldp_neighbors.txt
```

---



Template to parse A10 ACOS `show lldp neighbors` output and normalize it for
the `lldp_neighbors` getter.

Returns one dictionary per neighbor with the local interface, remote system
name, remote port ID and description, remote system description, chassis ID,
and management IP address. Missing advertised values are returned as `null`.



---

<details><summary>Template Content</summary>
```
<template name="a10_lldp_neighbors" results="per_template">
<doc>
Template to parse A10 ACOS 'show lldp neighbors' output and normalize it for
the 'lldp_neighbors' getter.

Returns one dictionary per neighbor with the local interface, remote system
name, remote port ID and description, remote system description, chassis ID,
and management IP address. Missing advertised values are returned as 'null'.
</doc>

<input>
commands = [
    "show lldp neighbors"
]
platform = [
    "a10",
    "a10_ssh",
]
</input>

<macro>
def transform_lldp_neighbors_to_records(payload):
    from ttp_templates.utils.a10_process_show_lldp_neighbors import transform_lldp_neighbors

    return transform_lldp_neighbors(payload)
</macro>

<group name="neighbors*">
interface {{ interface | ORPHRASE | _start_ }}:
chassis: {{ remote_chassi_id_raw | ORPHRASE }}
port: {{ remote_interface | ORPHRASE }}
port description: {{ remote_interface_description | ORPHRASE }}
system name: {{ remote_device | ORPHRASE }}
system description: {{ remote_system_description | ORPHRASE }}
management address: {{ remote_device_management_ip | ORPHRASE }}
</group>

<output macro="transform_lldp_neighbors_to_records"/>

</template>

```
</details>