Reference path:
```
ttp://platform/arista_eos_show_running_config_pipe_include_community_list.txt
```

---



Template to parse Arista EOS BGP community-list configuration from
`show running-config | include community-list`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and regexp entries are excluded. Standard, extended (`rt`,
`soo`, and `lbw`), and large community lists are supported.



---

<details><summary>Template Content</summary>
```
<template name="arista_eos_bgp_communities" results="per_template">
<doc>
Template to parse Arista EOS BGP community-list configuration from
'show running-config | include community-list'.

Returns a normalized list of dictionaries with 'value', 'type', and 'name'
keys. Each permitted concrete community value is returned as a separate
dictionary; deny and regexp entries are excluded. Standard, extended ('rt',
'soo', and 'lbw'), and large community lists are supported.
</doc>

<input>
commands = [
    "show running-config | include community-list"
]
platform = [
    "arista_eos",
    "eos",
]
</input>

<macro>
def transform_communities_to_records(data):
    from ttp_templates.utils.arista_eos_process_show_running_config_pipe_include_community_list import transform_community_lists

    return transform_community_lists(data)
</macro>

<group name="standard_lists*" method="table">
ip community-list {{ name }} permit {{ values | ORPHRASE }}
</group>

<group name="extended_lists*" method="table">
ip extcommunity-list {{ name }} permit {{ values | ORPHRASE }}
</group>

<group name="large_lists*" method="table">
ip large-community-list {{ name }} permit {{ values | ORPHRASE }}
</group>

<output macro="transform_communities_to_records"/>

</template>

```
</details>