Reference path:
```
ttp://platform/cisco_xr_show_rpl_community_set.txt
```

---



Template to parse Cisco IOS-XR BGP community sets from these commands:

- `show rpl community-set`
- `show rpl extcommunity-set`
- `show rpl large-community-set`

Returns a normalized list of dictionaries with `value`, `type`, and `name`
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded.



---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_bgp_communities" results="per_template">
<doc>
Template to parse Cisco IOS-XR BGP community sets from these commands:

- 'show rpl community-set'
- 'show rpl extcommunity-set'
- 'show rpl large-community-set'

Returns a normalized list of dictionaries with 'value', 'type', and 'name'
keys. Each concrete community value is returned as a separate dictionary;
pattern entries are excluded.
</doc>

<input>
commands = [
    "show rpl community-set",
    "show rpl extcommunity-set",
    "show rpl large-community-set",
]
platform = [
    "cisco_xr",
    "iosxr",
    "cisco_iosxr",
]
</input>

<macro>
def transform_communities_to_records(data):
    from ttp_templates.utils.cisco_xr_process_show_rpl_community_set import transform_community_sets

    return transform_community_sets(data)
</macro>

<group name="standard_sets*">
community-set {{ name | _start_ }}
 {{ values | _line_ | joinmatches }}
end-set {{ _end_ }}
</group>

<group name="extended_sets*">
extcommunity-set {{ type }} {{ name | _start_ }}
 {{ values | _line_ | joinmatches }}
end-set {{ _end_ }}
</group>

<group name="large_sets*">
large-community-set {{ name | _start_ }}
 {{ values | _line_ | joinmatches }}
end-set {{ _end_ }}
</group>

<output macro="transform_communities_to_records"/>

</template>

```
</details>