Reference path:
```
ttp://platform/juniper_junos_show_chassis_hardware_pipe_json.txt
```

---



Template to parse Juniper inventory.

This template requires output of 'show inventory' command.



---

<details><summary>Template Content</summary>
```
<template name="juniper_junos_inventory" results="per_template">
<doc>
Template to parse Juniper inventory.

This template requires output of 'show inventory' command.
</doc>

<macro>
def load_json(result):
    import json
    try:
        return json.loads("{" + result[0]["data"] + "}")
    except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError):
        return {}
</macro>

<macro>
def transform_inventory_to_records(payload):
    def pick(node, key):
        value = node.get(key)
        if not isinstance(value, list):
            return None
        for item in value:
            if isinstance(item, dict):
                data = item.get("data")
                if isinstance(data, str) and data.strip():
                    return data.strip()
        return None

    records = []
    stack = [payload]

    while stack:
        node = stack.pop()
        if isinstance(node, list):
            stack.extend(node)
            continue
        if not isinstance(node, dict):
            continue

        serial = pick(node, "serial-number")
        if serial and serial.upper() != "BUILTIN":
            description = pick(node, "description") or ""
            records.append(
                {
                    "module": description or (pick(node, "part-number") or ""),
                    "serial": serial,
                    "slot": pick(node, "name") or "",
                    "description": description,
                }
            )

        for value in node.values():
            stack.append(value)

    return records
</macro>

<input>
commands = [
    "show chassis hardware | display json"
]
platform = [
    "juniper_junos", # netmiko sand scrapli
    "junos", # napalm
]
</input>

<group>
{ {{ _start_ }}
{{ data | _line_ | joinmatches }}
} {{ _end_ }}
</group>

<output macro="load_json"/>
<output macro="transform_inventory_to_records"/>

</template>
```
</details>