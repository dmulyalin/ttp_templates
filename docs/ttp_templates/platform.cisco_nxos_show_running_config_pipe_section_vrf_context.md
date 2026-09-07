Reference path:
```
ttp://platform/cisco_nxos_show_running_config_pipe_section_vrf_context.txt
```

---



Template to parse Cisco NX-OS VRF configuration and normalize it to a flat
list of VRF dictionaries.

This template requires output of
'show running-config | section "vrf context"'.

Returns normalized list of dictionaries, each dictionary has these keys:

- `name` - VRF name string
- `instance_type` - always `vrf`
- `description` - VRF description string or `null` when not configured
- `rd` - route distinguisher string or `null` when not configured
- `rt_import` - list of import route-target strings
- `rt_export` - list of export route-target strings
- `route_policy_import` - import route policy string or `null` when not configured
- `route_policy_export` - export route policy string or `null` when not configured




---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_vrfs" results="per_template">
<doc>
Template to parse Cisco NX-OS VRF configuration and normalize it to a flat
list of VRF dictionaries.

This template requires output of
'show running-config | section "vrf context"'.

Returns normalized list of dictionaries, each dictionary has these keys:

- 'name' - VRF name string
- 'instance_type' - always 'vrf'
- 'description' - VRF description string or 'null' when not configured
- 'rd' - route distinguisher string or 'null' when not configured
- 'rt_import' - list of import route-target strings
- 'rt_export' - list of export route-target strings
- 'route_policy_import' - import route policy string or 'null' when not configured
- 'route_policy_export' - export route policy string or 'null' when not configured

</doc>

<input>
commands = [
    'show running-config | section "vrf context"'
]
platform = [
    "cisco_nxos",
    "nxos",
]
</input>

<macro>
def transform_vrfs_to_records(data):
    from ttp_templates.utils.cisco_nxos_process_show_running_config_pipe_section_vrf_context import transform_vrfs_config

    return transform_vrfs_config(data)
</macro>

<group name="vrfs**.{{ name }}**">
vrf context {{ name | _start_ }}
  description {{ description | re(".+") }}
  rd {{ rd }}

  <group name="address_families**.{{ afi }}_{{ safi }}**">
  address-family {{ afi }} {{ safi | _start_ }}
    route-target import {{ rt_import | re(".+") | to_list | joinmatches }}
    route-target export {{ rt_export | re(".+") | to_list | joinmatches }}
    route-target both {{ rt_both | re(".+") | to_list | joinmatches }}
    import map {{ route_policy_import }}
    export map {{ route_policy_export }}
  </group>
</group>

<output macro="transform_vrfs_to_records"/>

</template>

```
</details>