# Creating Getter Parsers

Getter parsers provide normalized, platform-independent output for a logical
data type such as inventory, interfaces, LLDP neighbors, BGP neighbors, or
VLANs. A getter is a wrapper under `ttp_templates/get/` that extends one or
more platform templates under `ttp_templates/platform/`.

## Files Involved

For a new getter or a new platform implementation of an existing getter, expect
to touch these files:

| File or folder | Purpose |
|---|---|
| `ttp_templates/get/<getter>.txt` | Getter wrapper with `<extend>` entries |
| `ttp_templates/platform/<platform>_<command>.txt` | Platform command parser |
| `ttp_templates/utils/<platform>_process_<command>.py` | Optional normalizer utility |
| `ttp_templates/utils/models.py` | Pydantic model for normalized records |
| `test/platform/<platform>/<command_slug>/` | Raw mock output and expected YAML |
| `docs/getters_support_matrix.md` | Getter platform support matrix |

Do not manually create or edit generated reference pages under
`docs/ttp_templates/`. Those pages are generated from template `<doc>` blocks.

## Output Contract

Define the normalized record shape before writing the parser. Getter output
should be a list of dictionaries with stable keys and predictable types.

For example, the `vlans` getter returns:

```yaml
- vid: 100
  name: USERS
  description: null
  tagged_interfaces:
  - Ethernet1
  untagged_interfaces:
  - Ethernet2
```

Add a Pydantic model in `ttp_templates/utils/models.py` for each normalized
record type:

```python
class VlanRecord(BaseModel):
    vid: StrictInt
    name: StrictStr
    description: Union[None, StrictStr]
    tagged_interfaces: List[StrictStr]
    untagged_interfaces: List[StrictStr]
```

Validate final records in the utility before returning them:

```python
records.append(VlanRecord(**record).model_dump())
```

## Platform Template

Platform templates live under `ttp_templates/platform/` and use this naming
rule:

```text
<platform>_<command_with_underscores>.txt
```

Replace spaces and hyphens with `_`, and replace `|` with `pipe`.

Examples:

```text
ttp_templates/platform/cisco_ios_show_running_config_pipe_section_vlan.txt
ttp_templates/platform/juniper_junos_show_configuration_vlans_pipe_display_set.txt
```

Each platform template should include:

1. A `<template name="...">` wrapper.
2. A `<doc>` block that names the command and output shape.
3. An `<input>` block with command and platform aliases.
4. TTP `<group>` statements to capture raw values.
5. A small `<macro>` wrapper when Python normalization is needed.
6. An `<output macro="..."/>` tag when a macro is used.

Keep Python inside `<macro>` minimal. Put parsing cleanup, range expansion,
JSON walking, default values, and validation in `ttp_templates/utils/`.

## Utility Function

Create a utility module when the template needs normalization beyond simple
TTP captures. Use one utility file per platform template unless an established
shared helper already exists.

Utility module checklist:

1. Module docstring explains the command being normalized.
2. `Used by:` note lists the platform template.
3. One public transform function is called by the template macro.
4. Private helpers are used only for real cleanup, such as VLAN range expansion.
5. Final records are validated with the getter Pydantic model.
6. The function returns plain Python lists and dictionaries.

Getter utilities should tolerate the TTP macro payload shape used by
`results="per_template"`. In practice this often means accepting both a bare
dictionary and a list of dictionaries:

```python
items = [payload] if isinstance(payload, dict) else payload
```

## Getter Wrapper

Getter templates live under `ttp_templates/get/`.

Add a platform implementation to the getter with an `<extend>` entry:

```xml
<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_vlan.txt"/>
```

Also update the getter `<doc>` block so supported platforms and returned keys
stay accurate.

## Mock Data And Expected YAML

Use the data-driven platform test layout:

```text
test/platform/<platform>/<command_slug>/<sample>.txt
test/platform/<platform>/<command_slug>/<sample>.yml
```

The `.txt` file contains raw command output. The `.yml` file contains the exact
expected normalized result. Use the same filename stem for both files.

The dynamic test collector automatically discovers these pairs, so do not add a
dedicated `test_get_<getter>.py` file unless the platform fixtures cannot cover
the behavior.

For commands with important syntax variants, include those variants in mock
data. For example, VLAN parsers should cover single IDs and range/list syntax
when the platform supports it:

```text
vlan 2,100-105
```

## Support Matrix

When adding or removing getter platform support, update
`docs/getters_support_matrix.md`.

Add the getter row or platform checkmark and list the collection command in the
notes section:

```markdown
### vlans

Collected commands by platform:

- Cisco IOS: `show running-config | section vlan`
```

## Documentation

Write useful `<doc>` blocks in templates. The generated template reference docs
and template navigation are produced from those blocks by:

```bash
poetry run inv docs
```

Static documentation under `docs/`, including this guide, is edited manually
and should be listed in `mkdocs.yml`.

## Validation

Run the dynamic platform tests after adding mock data:

```bash
python -m pytest test/test_platform_dynamic.py -q
```

For a direct getter smoke test:

```python
from pathlib import Path
from ttp_templates import parse_output

data = Path("test/platform/cisco_ios/show_running_config_pipe_section_vlan/show_running_config_pipe_section_vlan.txt").read_text()
result = parse_output(data=data, get="vlans", platform="cisco_ios")
```

Before finishing, run:

```bash
git diff --check
```

## Checklist

1. Getter output shape is documented and stable.
2. Pydantic model exists for normalized records.
3. Platform template name matches `get_template()` command resolution.
4. `<input>` command and platform aliases are present.
5. Utility function validates final records.
6. Getter wrapper extends the new platform template.
7. Mock `.txt` and expected `.yml` files are present.
8. Getter support matrix is updated.
9. Generated template docs are not hand-edited.
10. Focused tests pass.
