Reference path:
```
ttp://platform/cisco_nxos_show_running_config_rpm.txt
```

---



Template to parse Cisco NX-OS BGP community-list configuration from
`show running-config rpm`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and expanded entries are excluded. Standard, extended, and
large community lists with optional sequence numbers are supported.



---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_bgp_communities" results="per_template">
<doc>
Template to parse Cisco NX-OS BGP community-list configuration from
'show running-config rpm'.

Returns a normalized list of dictionaries with 'value', 'type', and 'name'
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and expanded entries are excluded. Standard, extended, and
large community lists with optional sequence numbers are supported.
</doc>

<input>
commands = [
    "show running-config rpm"
]
platform = [
    "cisco_nxos",
    "nxos",
]
</input>

<macro>
def transform_communities_to_records(data):
    from ttp_templates.utils.cisco_nxos_process_show_running_config_rpm import transform_community_lists

    return transform_community_lists(data)
</macro>

<group name="standard_lists*" method="table">
ip community-list standard {{ name }} seq {{ sequence }} permit {{ values | ORPHRASE }}
ip community-list standard {{ name }} permit {{ values | ORPHRASE }}
</group>

<group name="extended_lists*" method="table">
ip extcommunity-list standard {{ name }} seq {{ sequence }} permit {{ values | ORPHRASE }}
ip extcommunity-list standard {{ name }} permit {{ values | ORPHRASE }}
</group>

<group name="large_lists*" method="table">
ip large-community-list standard {{ name }} seq {{ sequence }} permit {{ values | ORPHRASE }}
ip large-community-list standard {{ name }} permit {{ values | ORPHRASE }}
</group>

<output macro="transform_communities_to_records"/>

</template>

```
</details>