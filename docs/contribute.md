# Contribute

There are several ways to help the TTP Templates project:

* Spread the word about TTP and TTP Templates
* Suggest features and ideas
* Report bugs
* Fix typos in code, templates and documentation
* Write documentation
* Contribute new templates
* Improve existing templates

## Contribute by Issue

Open a [GitHub issue](https://github.com/dmulyalin/ttp_templates/issues/new/choose)
using the `Contribute Template` type and include:

* Platform and command
* Raw sample output
* Expected structured result
* Notes about supported software versions, if known

## Contribute by Pull Request

The project uses [Poetry](https://python-poetry.org/) for dependency
management:

```bash
poetry install
```

Before opening a pull request, run focused tests for the files you changed and
include sample data plus expected output for every new parser.

## Template Categories

Place template content in the right category:

| Category | Location | Naming rule |
|---|---|---|
| Platform | `ttp_templates/platform/` | `<vendor_os>_<command_with_underscores>.txt` |
| Getter | `ttp_templates/get/` | `<getter_name>.txt`, for example `inventory.txt` |
| YANG | `ttp_templates/yang/` | `<yang_module>_<platform_name>.txt` |
| Misc | `ttp_templates/misc/<usecase>/` | Free-form template name under a use-case folder |

Use lowercase names for platform, getter and YANG templates. Replace spaces and
hyphens with `_`, and replace `|` with `pipe`.

Examples:

```text
ttp_templates/platform/cisco_nxos_show_inventory_pipe_json_pretty.txt
ttp_templates/platform/linux_ip_address_show.txt
ttp_templates/get/interfaces.txt
```

## Template Contribution Workflow for AI Agents

Use this step-by-step workflow when adding or changing templates. It is written
so an AI coding assistant can follow it without inventing project structure.

### 1. Read Existing Context

First inspect the closest existing examples:

1. Read `CLAUDE.md`.
2. Read this file.
3. Read the target getter template if the new template belongs to a getter, for
   example `ttp_templates/get/inventory.txt`.
4. Read similar platform templates under `ttp_templates/platform/`.
5. Read matching utility files under `ttp_templates/utils/`.
6. Read existing mock data under `test/platform/<platform>/`.

Do not start by creating new abstractions. Follow the local naming, output
shape and utility style already present in the repository.

### 2. Decide the Output Shape

Before writing the template, write down the final data structure:

1. For a standalone platform template, match the nearest existing platform
   output style.
2. For a getter template, return the normalized getter record shape.
3. For normalized records, validate final dictionaries with a Pydantic model in
   `ttp_templates/utils/models.py`.
4. Keep field names, null handling and list handling consistent with existing
   templates for the same getter.

### 3. Create or Update the Platform Template

Platform templates live in `ttp_templates/platform/`.

Keep the template file focused on TTP parsing:

1. Add a `<template name="...">` wrapper.
2. Add a `<doc>` block that names the platform, command and output.
3. Add an `<input>` block with the command and platform aliases.
4. Add `<group>` blocks that capture raw values.
5. Add a small `<macro>` wrapper only when Python processing is needed.
6. Add `<output macro="..."/>` when using a macro.

Example macro wrapper:

```python
def transform_inventory_to_records(payload):
    from ttp_templates.utils.arista_eos_process_show_inventory_pipe_json import (
        transform_inventory,
    )

    return transform_inventory(payload)
```

For JSON commands, prefer capturing the JSON blob and parsing it in a utility
function:

```text
<group>
{ {{ _start_ }}
{{ data | _line_ | joinmatches }}
} {{ _end_ }}
</group>
```

Avoid complex Python inside TTP `<macro>` blocks. Put non-trivial processing in
`ttp_templates/utils/`.

### 4. Create a Utility Function Only When Needed

If processing is more than a few simple lines, create one utility file per
template:

```text
ttp_templates/platform/arista_eos_show_inventory_pipe_json.txt
ttp_templates/utils/arista_eos_process_show_inventory_pipe_json.py
```

Utility module rules:

1. Add a module docstring that explains what command is normalized.
2. Add a `Used by:` note listing the template path.
3. Export one main function used by the template.
4. Keep code linear and readable.
5. Use private helpers only when they make the main function easier to read.
6. Return plain dictionaries and lists.
7. Validate final normalized records before returning them.

Do not make a reusable shared module unless several existing templates already
use that pattern.

### 5. Add or Update Pydantic Models

Normalized output contracts belong in `ttp_templates/utils/models.py`.

Add one model per normalized record type and use strict types where practical:

```python
class InventoryRecord(BaseModel):
    description: StrictStr
    module: StrictStr
    serial: StrictStr
    slot: StrictStr
```

Validate final records in the utility function:

```python
record = {
    "description": description,
    "module": module,
    "serial": serial,
    "slot": slot,
}
records.append(InventoryRecord(**record).model_dump())
```

Keep schema definitions in `models.py`. Keep template-specific cleanup in the
template utility.

### 6. Add Mock Data and Expected Results

Prefer data-driven platform tests under `test/platform/`:

```text
test/platform/<platform>/<command_slug>/<sample>.txt
test/platform/<platform>/<command_slug>/<sample>.yml
```

The command slug uses underscores instead of spaces. For commands with a pipe,
include `pipe`:

```text
test/platform/cisco_nxos/show_inventory_pipe_json_pretty/show_inventory_pipe_json_pretty.txt
test/platform/cisco_nxos/show_inventory_pipe_json_pretty/show_inventory_pipe_json_pretty.yml
```

Rules for fixtures:

1. The `.txt` file contains raw device output only.
2. The `.yml` file contains the exact expected parser result.
3. Use the same stem for `.txt` and `.yml`.
4. Add more than one sample when the command has meaningful output variants.
5. Prefer `flat_list` expected output unless an existing `settings.yml` says
   otherwise.

The dynamic test collector automatically discovers matching `.txt` and `.yml`
pairs under `test/platform/`.

### 7. Update Getter Templates

Getter templates live in `ttp_templates/get/` and combine platform templates
with `<extend>`.

When adding support for a platform to a getter:

1. Add or update the platform template.
2. Add a utility module if transformation is needed.
3. Validate normalized records with the getter model.
4. Add `<extend template="ttp://platform/<template>.txt"/>` to the getter.
5. Update `docs/getters_support_matrix.md`.
6. Add or update `test/test_get_*.py` only when data-driven platform tests do
   not cover the getter behavior.

### 8. Update Documentation

Every template should have a useful `<doc>` block. Generated template reference
pages are built from those docstrings.

Do not manually create or edit generated template reference pages under
`docs/ttp_templates/`, and do not manually add template pages to the `Templates`
navigation in `mkdocs.yml`. The docs generator rewrites those files and nav
entries.

After changing templates or template docs, regenerate docs:

```bash
poetry run python generate_docs.py
```

For static documentation pages such as this guide, add the page to `mkdocs.yml`.
The docs generator rewrites the `Templates` navigation section only, so static
top-level pages are preserved.

### 9. Run Focused Tests

Run the smallest useful test set first:

```bash
cd test
poetry run pytest -vv test_platform_dynamic.py -k <platform>
```

For getter-specific behavior, also run the getter test:

```bash
cd test
poetry run pytest -vv test_get_inventory.py
```

Then run broader tests if the change touches shared models, shared utility
logic, or public API behavior.

### 10. Final Checklist

Before submitting:

1. Template name follows project naming rules.
2. Template has a clear `<doc>` block.
3. Template has an `<input>` block with command and platform aliases.
4. Complex processing lives in `ttp_templates/utils/`.
5. Utility module has a `Used by:` note.
6. Normalized records are validated with a Pydantic model.
7. Mock `.txt` and expected `.yml` files have matching names.
8. Getter support matrix is updated when getter support changes.
9. Generated template docs are not hand-edited.
10. Focused tests pass.
