Reference path:
```
ttp://platform/cisco_nxos_show_inventory_pipe_json_pretty.txt
```

---



Template to parse Cisco NX-OS inventory.

This template requires output of 'show inventory' command.



---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_inventory" results="per_template">
<doc>
Template to parse Cisco NX-OS inventory.

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
    rows = payload.get("TABLE_inv", {}).get("ROW_inv", [])
    if isinstance(rows, dict):
        rows = [rows]
    records = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        serial = str(r.get("serialnum", "")).strip()
        if not serial or serial.upper() == "N/A":
            continue
        records.append(
            {
                "module": str(r.get("productid", "")).strip(),
                "serial": serial,
                "slot": str(r.get("name", "")).replace('"', "").strip(),
                "description": str(r.get("desc", "")).replace('"', "").strip(),
            }
        )
    return records
</macro>

<input>
commands = [
    "show inventory | json-pretty"
]
platform = [
    "nxos", # NAPALM
    "cisco_nxos", # Netmiko and Scrapli
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