# Template Guidelines

Use this guide when adding or changing TTP templates. The goal is to keep each
template easy to read, easy to test, and predictable for library users.

## Template File Structure

Platform templates live in `ttp_templates/platform/` and use this filename
format:

```text
<platform>_<command_with_underscores>.txt
```

Use lowercase names. Replace spaces and hyphens with `_`, and replace `|` with
`pipe`. For example:

```text
ttp_templates/platform/cisco_nxos_show_inventory_pipe_json_pretty.txt
```

Keep template files focused on TTP parsing:

1. Add a `<doc>` block that names the platform, command, and expected output.
2. Add an `<input>` block with supported command strings and platform aliases.
3. Add `<group>` blocks that capture raw values from CLI output.
4. Add a small `<macro>` wrapper only when output needs Python processing.
5. Use `<output macro="..."/>` to call the wrapper.

For JSON commands, a common pattern is to capture the full JSON object and pass
it to a utility function:

```text
<group>
{ {{ _start_ }}
{{ data | _line_ | joinmatches }}
} {{ _end_ }}
</group>
```

## Utility Functions

If a template needs more than a few lines of Python, put that logic in
`ttp_templates/utils/`. Prefer one utility file per template. Name it after the
template:

```text
ttp_templates/platform/arista_eos_show_inventory_pipe_json.txt
ttp_templates/utils/arista_eos_process_show_inventory_pipe_json.py
```

The template macro should stay small:

```python
def transform_inventory_to_records(payload):
    from ttp_templates.utils.arista_eos_process_show_inventory_pipe_json import (
        transform_inventory,
    )

    return transform_inventory(payload)
```

Keep utility modules simple and linear:

1. Add a short module docstring explaining the command and output.
2. Export one main function used by the template, such as `transform_inventory`.
3. Use small private helpers only when they make the main function easier to read.
4. Avoid shared helper modules unless several existing templates already use that
   pattern.
5. Use comments for non-obvious parsing decisions, not for every assignment.
6. Return plain Python dictionaries and lists.

For JSON output, load JSON with the standard library:

```python
import json


def _load_json(payload: list) -> dict:
    if not payload:
        return {}
    return json.loads("{" + payload[0]["data"] + "}")
```

## Pydantic Models

Normalized output contracts should be represented in
`ttp_templates/utils/models.py`.

Add one Pydantic model per normalized record type. Use strict types where
possible:

```python
class InventoryRecord(BaseModel):
    description: StrictStr
    module: StrictStr
    serial: StrictStr
    slot: StrictStr
```

Utility functions should validate final records before returning them:

```python
record = {
    "description": description,
    "module": module,
    "serial": serial,
    "slot": slot,
}
records.append(InventoryRecord(**record).model_dump())
```

Keep parsing cleanup in the utility function and schema definition in
`models.py`. Do not hide template-specific behavior inside the model.

## Getter Templates

Getter templates live in `ttp_templates/get/` and combine platform templates
with `<extend>`. They should return normalized, platform-agnostic records.

When adding a platform to a getter:

1. Add or update the platform template.
2. Add a dedicated utility module if transformation is needed.
3. Add or update the Pydantic model for the getter output.
4. Add `<extend template="ttp://platform/<template>.txt"/>` to the getter.
5. Update `docs/getters_support_matrix.md`.
6. Extend the getter test, such as `test/test_get_inventory.py`.

## Tests And Mock Data

Prefer data-driven platform tests under `test/platform/`:

```text
test/platform/<platform>/<command_slug>/<sample>.txt
test/platform/<platform>/<command_slug>/<sample>.yml
```

The command slug uses underscores instead of spaces. For commands with a pipe,
include `pipe` in the folder name:

```text
test/platform/cisco_nxos/show_inventory_pipe_json_pretty/show_inventory_pipe_json_pretty.txt
test/platform/cisco_nxos/show_inventory_pipe_json_pretty/show_inventory_pipe_json_pretty.yml
```

The `.txt` file contains raw device output. The `.yml` file contains the exact
expected parser result, usually a YAML list of dictionaries for `flat_list`
output.

For getter templates, also update the relevant `test/test_get_*.py` file. Getter
tests should verify:

1. The new platform input is registered in `parser.get_input_load()`.
2. The getter parses mock data into the normalized output shape.
3. Invalid or intentionally skipped rows are handled as expected.

Run focused tests before opening a pull request:

```bash
cd test
poetry run pytest -vv test_platform_dynamic.py -k <platform>
poetry run pytest -vv test_get_inventory.py
```

## Documentation

Every template should have a useful `<doc>` block because `generate_docs.py`
builds template reference pages from it.

After adding templates or changing template docs, regenerate docs:

```bash
poetry run python generate_docs.py
```

For static documentation pages such as this one, add the page to `mkdocs.yml`.
The docs generator rewrites the `Templates` navigation section only, so static
top-level pages are preserved.
