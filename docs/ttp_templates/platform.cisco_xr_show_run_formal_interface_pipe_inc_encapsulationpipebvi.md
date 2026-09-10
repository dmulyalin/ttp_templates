Reference path:
```
ttp://platform/cisco_xr_show_run_formal_interface_pipe_inc_encapsulationpipebvi.txt
```

---



Template to derive Cisco IOS-XR VLANs and interface membership from formal
interface configuration.

This template requires output of
`show run formal interface | inc "encapsulation|BVI"`.

Every VLAN referenced by a dot1q or untagged subinterface encapsulation, or by
a BVI interface name, is returned, including VLANs that do not have a separate
global VLAN definition. Parsed interface mode uses the existing normalized
values `tagged` and `access`; BVI interfaces are untagged members.

Returns normalized list of dictionaries with these keys:

- `vid` - VLAN ID as integer
- `name` - defaults to `VLAN<vid>`
- `description` - always `null`
- `tagged_interfaces` - interface names carrying the VLAN tagged
- `untagged_interfaces` - interface names carrying the VLAN untagged




---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_vlans" results="per_template">
<doc>
Template to derive Cisco IOS-XR VLANs and interface membership from formal
interface configuration.

This template requires output of
'show run formal interface | inc "encapsulation|BVI"'.

Every VLAN referenced by a dot1q or untagged subinterface encapsulation, or by
a BVI interface name, is returned, including VLANs that do not have a separate
global VLAN definition. Parsed interface mode uses the existing normalized
values 'tagged' and 'access'; BVI interfaces are untagged members.

Returns normalized list of dictionaries with these keys:

- 'vid' - VLAN ID as integer
- 'name' - defaults to 'VLAN&lt;vid&gt;'
- 'description' - always 'null'
- 'tagged_interfaces' - interface names carrying the VLAN tagged
- 'untagged_interfaces' - interface names carrying the VLAN untagged

</doc>

<input>
commands = [
    "show run formal interface | inc \"encapsulation|BVI\""
]
platform = [
    "cisco_xr",
    "iosxr",
]
</input>

<macro>
def transform_vlans_to_records(data):
    from ttp_templates.utils.cisco_xr_process_show_run_formal_interface_pipe_inc_encapsulationpipebvi import transform_vlans_config

    return transform_vlans_config(data)
</macro>

<group name="interfaces**.{{ name }}**" method="table">
interface {{ name }} encapsulation dot1q {{ vlan | to_int }}
interface {{ name }} l2transport encapsulation dot1q {{ vlan | to_int }}
interface {{ name | let("mode", "access") }} encapsulation untagged
interface {{ name | let("mode", "access") }} l2transport encapsulation untagged
</group>

<group name="bvi_interfaces*" method="table">
interface BVI{{ vid | DIGIT | to_int }}
</group>

<output macro="transform_vlans_to_records"/>

</template>

```
</details>