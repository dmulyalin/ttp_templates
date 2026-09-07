Reference path:
```
ttp://platform/arista_eos_show_running_config_section_vrf.txt
```

---



Template to parse Arista EOS VRF configuration and normalize it to a flat list
of VRF dictionaries.

This template requires output of 'show running-config section vrf'.

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
<template name="arista_eos_vrfs" results="per_template">
<doc>
Template to parse Arista EOS VRF configuration and normalize it to a flat list
of VRF dictionaries.

This template requires output of 'show running-config section vrf'.

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
    "show running-config section vrf"
]
platform = [
    "arista_eos", # scrapli and netmiko
    "eos", # NAPALM
]
</input>

<macro>
def transform_vrfs_to_records(data):
    from ttp_templates.utils.arista_eos_process_show_running_config_section_vrf import transform_vrfs_config

    return transform_vrfs_config(data)
</macro>

<group name="vrfs**.{{ name }}**">
vrf instance {{ name | _start_ }}
   description {{ description | re(".+") }}
   rd {{ rd }}
!{{ _end_ }}
</group>

<group>
router bgp {{ asn | _start_ }}
   <group name="vrfs**.{{ name }}**">
   vrf {{ name | _start_ }}
      rd {{ rd }}
      route-target import {{ rt_import | contains(":") | to_list | joinmatches }}
      route-target export {{ rt_export | contains(":") | to_list | joinmatches }}
      route-target import {{ ignore }} {{ rt_import | contains(":") | to_list | joinmatches }}
      route-target export {{ ignore }} {{ rt_export | contains(":") | to_list | joinmatches }}
      route-target both {{ rt_both | contains(":") | to_list | joinmatches }}
      route-target both {{ ignore }} {{ rt_both | contains(":") | to_list | joinmatches }}
      import map {{ route_policy_import }}
      export map {{ route_policy_export }}
   !{{ _end_ }}
   </group>
!{{ _end_ }}
</group>

<output macro="transform_vrfs_to_records"/>

</template>

```
</details>