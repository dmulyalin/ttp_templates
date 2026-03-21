# CLAUDE.md

## Project overview

`ttp_templates` is a Python package that ships a curated collection of
[TTP (Template Text Parser)](https://ttp.readthedocs.io/) templates together
with a small Python API for resolving, loading, and using them.  Templates are
plain-text regex skeletons that TTP interprets to extract structured data from
raw CLI/config output produced by network devices (Cisco IOS/XR/NXOS, Arista
EOS, Huawei VRP, Juniper JunOS, etc.).

PyPI: `ttp-templates`  
Docs: <https://dmulyalin.github.io/ttp_templates/>  
Repo: <https://github.com/dmulyalin/ttp_templates>

---

## Repository layout

```
ttp_templates/          # installable package
    __init__.py         # re-exports get_template, parse_output, list_templates
    ttp_templates.py    # all public API functions
    ttp_vars.py         # reusable TTP variables (short_interface_names, …)
    platform/           # one .txt template per (platform, command) pair
    yang/               # one .txt template per (YANG module, platform) pair
    get/                # one .txt getter template per logical function (inventory, interfaces, …)
    misc/               # free-form hierarchy of specialised templates
        N2G/            # templates consumed by the N2G topology library
        Netbox/         # templates for extracting Netbox-style data
        Netmiko/        # templates for use with the Netmiko SSH library
        ttp_templates_tests/  # templates used only by the test suite

test/                   # pytest test suite
    test_ttp_templates_methods.py   # unit tests for the three public API functions
    test_platform_*.py              # regression/integration tests per platform
    test_n2g_templates.py           # N2G-specific template tests
    test_misc_netmiko_templates.py  # Netmiko template tests
    test_yang_*.py                  # YANG template tests
    mock_data/                      # raw CLI output fixtures used by tests
    yang-modules/                   # YANG schema files for yangson validation

private/                # internal notes, not part of the package
docs/                   # MkDocs source (published to GitHub Pages)
```

---

## Public API (`ttp_templates`)

### `get_template(**kwargs) -> Optional[str]`

Resolves a template file from one of four addressing schemes and returns its
raw text content, or `None` when no valid combination of arguments is supplied.

| Arguments | Description |
|---|---|
| `path="platform/cisco_ios_show_ip_arp.txt"` | Explicit relative or `ttp://`-prefixed path |
| `platform="cisco_ios", command="show ip arp"` | Resolved to `platform/<platform>_<command>.txt` |
| `yang="ietf-interfaces", platform="cisco_ios"` | Resolved to `yang/<yang>_<platform>.txt` |
| `misc="N2G/cli_ip_data/cisco_ios.txt"` | Resolved relative to the `misc/` directory |
| `get="inventory"` | Resolved to `get/inventory.txt`; `.txt` suffix is optional |

Spaces and hyphens in `platform`/`command` are normalised to underscores;
`|` in `command` is replaced with `pipe`.
For `get`, the `.txt` extension is appended automatically when absent.

### `parse_output(data, **kwargs) -> Union[Dict, List]`

Thin wrapper: calls `get_template` with the same kwargs, instantiates a `ttp`
parser with the template and the provided `data` string, runs the parse pass,
and returns `parser.result(structure=structure)`.

Accepted extra kwargs:  
- `structure` (`"list"` | `"dictionary"` | `"flat_list"`, default `"list"`)  
- `template_vars` – dict of variables injected into the TTP template at parse time.

### `list_templates(pattern="*") -> Dict`

Walks the `platform/`, `yang/`, and `misc/` directories and returns a
dictionary whose structure mirrors the directory tree. Filenames are filtered
by the caller's `fnmatch` glob `pattern`. `readme.md` files are always
excluded.

Return shape:
```python
{
    "platform": ["cisco_ios_show_ip_arp.txt", ...],
    "yang": ["ietf-interfaces_cisco_ios.txt", ...],
    "misc": {
        "N2G": {
            "cli_ip_data": ["cisco_ios.txt", ...],
            ...
        },
        ...
    },
}
```

---

## Template variables (`ttp_templates.ttp_vars`)

| Name | Type | Purpose |
|---|---|---|
| `short_interface_names` | `dict` | Regex pattern lists for TTP `resuball` to normalise long interface names to short abbreviations (e.g. `GigabitEthernet` → `GE`) |
| `physical_ports` | `list` | Subset of `short_interface_names` keys that represent physical (non-logical) ports; used by the N2G L2 drawer |
| `all_vars` | `dict` | Convenience bundle of all of the above for passing as `template_vars` |

---

## Template naming conventions

| Category | File location | Naming scheme |
|---|---|---|
| Platform | `platform/` | `<platform>_<command>.txt` – spaces/hyphens → `_`, `\|` → `pipe` |
| YANG | `yang/` | `<yang_module>_<platform>.txt` |
| Misc | `misc/<SubDir>/` | Freeform, usually lowercase with underscores |

---

## Development environment

The project uses [Poetry](https://python-poetry.org/) for dependency and
build management.

```bash
# install all dependencies (including dev group)
poetry install

# run the full test suite
cd test
poetry run pytest -vv

# run a specific test file
cd test
poetry run pytest test_ttp_templates_methods.py -vv

# build docs locally
poetry run mkdocs serve
```

### Key dev dependencies

| Tool | Purpose |
|---|---|
| `pytest` | Test runner |
| `cerberus` | Schema validation in N2G tests |
| `deepdiff` | Deep equality assertions |
| `yangson` | YANG schema validation for yang template tests |
| `netmiko` | Integration tests against real/mock devices |
| `black` | Code formatting |
| `flake8` / `pylint` | Linting |
| `bandit` | Security scanning |

---

## Logging

All three API functions emit `logging.debug` messages using a module-level
logger obtained with `logging.getLogger(__name__)` (logger name:
`ttp_templates.ttp_templates`). No handlers are attached by the library;
callers are responsible for configuring logging if they need output.

Example to enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Known bugs / issues

See [private/bug_report.md](private/bug_report.md) for a full list. Summary:

1. **Path-traversal vulnerability** – `get_template` does not sanitise the
   `path` / `misc` arguments; crafted `..` sequences can read files outside the
   package.
2. **`get_template` returns `None` silently** – `parse_output` passes that
   `None` straight to the TTP constructor with no guard, which may cause
   confusing errors.
3. **`list_templates` dict/list collision** – placing a template file directly
   in `misc/` (not a subdirectory) would corrupt the result dict and raise
   `AttributeError`.
4. **Non-deterministic file ordering** – `os.walk` / `os.listdir` do not sort
   filenames.
5. **No template caching** – every call re-reads from disk and creates a new
   `ttp` parser instance.
6. **`short_interface_names` prefix ambiguity** – `2GE` patterns (`^Tw`, `^Two`)
   are strict prefixes of `TwentyFive*` / `TwoHundred*` names; insertion order
   may cause mis-classification depending on TTP's `resuball` implementation.
