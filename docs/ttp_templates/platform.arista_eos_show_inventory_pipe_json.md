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
    import json
    if payload:
        payload = json.loads("{" + payload[0]["data"] + "}")
    else:
        return []

    records = []

    def add_item(item, slot):
        if not isinstance(item, dict):
            return
        serial = str(item.get("serialNum", "")).strip()
        if not serial or serial.upper() == "N/A":
            return
        records.append(
            {
                "module": str(item.get("name") or item.get("modelName") or "").strip(),
                "serial": serial,
                "slot": slot,
                "description": str(item.get("description", "")).strip(),
            }
        )

    add_item(payload.get("systemInformation", {}), "chassis")

    for top_key, top_value in payload.items():
        if not top_key.endswith("Slots") or not isinstance(top_value, dict):
            continue
        slot_prefix = top_key[: -len("Slots")].lower()
        for key, item in top_value.items():
            add_item(item, f"{slot_prefix}-{key}")

    return records
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