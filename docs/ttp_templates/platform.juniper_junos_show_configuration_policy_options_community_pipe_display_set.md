Reference path:
```
ttp://platform/juniper_junos_show_configuration_policy_options_community_pipe_display_set.txt
```

---



Template to parse Juniper Junos BGP community configuration from
`show configuration policy-options community | display set`.

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded. Junos `target`, `origin`, and `large` prefixes
are normalized to `rt`, `soo`, and `large` types respectively.



---

<details><summary>Template Content</summary>
```
<template name="juniper_junos_bgp_communities" results="per_template">
<doc>
Template to parse Juniper Junos BGP community configuration from
'show configuration policy-options community | display set'.

Returns a normalized list of dictionaries with 'value', 'type', and 'name'
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded. Junos 'target', 'origin', and 'large' prefixes
are normalized to 'rt', 'soo', and 'large' types respectively.
</doc>

<input>
commands = [
    "show configuration policy-options community | display set"
]
platform = [
    "juniper_junos",
    "junos",
]
</input>

<macro>
def transform_communities_to_records(data):
    from ttp_templates.utils.juniper_junos_process_show_configuration_policy_options_community_pipe_display_set import transform_community_sets

    return transform_community_sets(data)
</macro>

<group name="community_sets*" method="table">
set policy-options community {{ name }} members {{ values | ORPHRASE }}
</group>

<output macro="transform_communities_to_records"/>

</template>

```
</details>