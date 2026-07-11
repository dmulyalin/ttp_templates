Reference path:
```
ttp://platform/arista_eos_show_inventory_pipe_json.txt
```

---



Template to parse Arista inventory.

This template requires output of 'show inventory' command.



---

<details><summary>Template Content</summary>
```
<template name="arista_eos_inventory" results="per_template">
<doc>
Template to parse Arista inventory.

This template requires output of 'show inventory' command.
</doc>

<macro>
def transform_inventory_to_records(payload):
    from ttp_templates.utils.arista_eos_process_show_inventory_pipe_json import (
        transform_inventory,
    )

    return transform_inventory(payload)
</macro>

<input>
commands = [
    "show inventory | json"
]
platform = [
    "arista_eos", # scrapli and netmiko
    "eos", # NAPALM
]
</input>

<group>
{ {{ _start_ }}
{{ data | _line_ | joinmatches }}
} {{ _end_ }}
</group>

<output macro="transform_inventory_to_records"/>

</template>
```
</details>
