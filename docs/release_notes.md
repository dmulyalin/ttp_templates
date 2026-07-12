# Release Notes

## 0.5.9

### TEMPLATES

1. Added Cisco NX-OS inventory parsing support using
   `ttp://platform/cisco_nxos_show_inventory_pipe_json_pretty.txt` for
   `show inventory | json-pretty` command output.
2. Updated `ttp://get/inventory.txt` to use the Cisco NX-OS
   `show inventory | json-pretty` platform template.
3. Added A10 hardware parsing support using
   `ttp://platform/a10_show_hardware.txt` for `show hardware` command output.
4. Updated `ttp://get/inventory.txt` to include A10 inventory parsing through
   the `show hardware` platform template.
5. Added Linux interface parsing support using
   `ttp://platform/linux_ip_address_show.txt` for `ip address show` command
   output.
6. Updated `ttp://get/interfaces.txt` to include Linux interface parsing.
7. Added Cisco NX-OS interface parsing support using
   `ttp://platform/cisco_nxos_show_running_config_interface.txt` for
   `show running-config interface` command output.
8. Updated `ttp://get/interfaces.txt` to include Cisco NX-OS interface parsing.
9. Added Cisco IOS inventory parsing support using
   `ttp://platform/cisco_ios_show_inventory.txt` for `show inventory` command
   output.
10. Updated `ttp://get/inventory.txt` to include Cisco IOS inventory parsing.

### CHANGES

1. Added `InventoryRecord` Pydantic model in `ttp_templates/utils/models.py` to
   validate normalized inventory records.
2. Moved inventory transformation logic out of TTP template macros and into
   dedicated utility modules:
   - `ttp_templates/utils/arista_eos_process_show_inventory_pipe_json.py`
   - `ttp_templates/utils/cisco_ios_process_show_inventory.py`
   - `ttp_templates/utils/cisco_nxos_process_show_inventory_pipe_json_pretty.py`
   - `ttp_templates/utils/cisco_xr_process_show_inventory.py`
   - `ttp_templates/utils/juniper_junos_process_show_chassis_hardware_pipe_json.py`
3. Updated Arista EOS, Cisco IOS, Cisco NX-OS, Cisco IOS-XR and Juniper Junos
   inventory templates to import their processing functions from
   `ttp_templates/utils/` and return validated normalized records.
4. Added `BgpNeighborRecord` Pydantic model and updated Arista EOS, Cisco IOS-XR
   and Juniper Junos BGP neighbor utility functions to validate normalized
   neighbor records before returning them.
5. Updated Arista EOS and Juniper Junos LLDP neighbor utility functions to use
   the existing `LldpNeighborRecord` model for normalized LLDP records.
6. Added `ArpRecord` Pydantic model and updated Cisco IOS and Cisco IOS-XR ARP
   platform templates to validate parsed ARP entries while preserving TTP result
   structure.
7. Updated A10 `show hardware` parsing to validate normalized inventory records
   with the existing `InventoryRecord` model using
   `ttp_templates/utils/a10_process_show_hardware.py`.
8. Added `ttp_templates/utils/linux_process_ip_address_show.py` to normalize
   Linux operational interface output and validate it with
   `InterfaceConfigRecord`.
9. Added `ttp_templates/utils/cisco_nxos_process_show_running_config_interface.py`
   to normalize Cisco NX-OS interface configuration output and validate it with
   `InterfaceConfigRecord`.

### TESTS

1. Added Cisco NX-OS inventory mock data and expected output under
   `test/platform/cisco_nxos/show_inventory_pipe_json_pretty/`.
2. Extended `test/test_get_inventory.py` to validate Cisco NX-OS inventory
   parsing through the `get/inventory` getter.
3. Added A10 `show hardware` mock data and expected output under
   `test/platform/a10/show_hardware/`.
4. Extended `test/test_get_inventory.py` to validate A10 inventory parsing
   through the `get/inventory` getter.
5. Added Linux `ip address show` mock data and expected output under
   `test/platform/linux/ip_address_show/`.
6. Added Cisco NX-OS `show running-config interface` mock data and expected
   output under `test/platform/cisco_nxos/show_running_config_interface/`.
7. Added Cisco IOS `show inventory` mock data samples and expected output under
   `test/platform/cisco_ios/show_inventory/`.

### DOCS

1. Merged template guidelines into `docs/contribute.md` and rewrote the
   guidance as an AI-friendly step-by-step workflow for adding templates.
2. Updated `CLAUDE.md`, `mkdocs.yml` and generated template reference pages to
   document the new template workflow.
3. Updated `docs/getters_support_matrix.md` to note Cisco NX-OS inventory
   getter support with `show inventory | json-pretty`.
4. Added generated template reference docs and mkdocs navigation entry for
   `ttp://platform/a10_show_hardware.txt`.
5. Updated getter support matrix and generated inventory getter reference docs
   to include A10 inventory support.
6. Updated getter support matrix to include Linux interface getter support.
7. Updated getter support matrix to include Cisco NX-OS interface getter
   support.
8. Updated getter support matrix to include Cisco IOS inventory getter support.



---

## 0.5.8

### BUGS

1. Fixing `juniper_junos_process_show_configuration_interfaces_pipe_display_set` untagged_vlan vlan handling for juniper subinterfaces - set mode to access and populate untagged_vlan correctly
2. Fixing `juniper_junos_process_show_configuration_interfaces_pipe_display_set` to not assing parent for any logical interface like `gr` or `lt` or `lo0`

---

## 0.5.7

### BUGS

1. Fixing `cisco_xr_show_bgp_neighbors.txt` template dynamic BGP peers ASN parsing
2. Fixing `juniper_junos_process_show_configuration_interfaces_pipe_display_set` extraction of ips for interfaces with virtual gateways
3. Fixing `juniper_junos_process_show_configuration_interfaces_pipe_display_set` parent assignment logic - skip it for irb and lo0 interfaces
4. Fixing `juniper_junos_process_show_configuration_interfaces_pipe_display_set` to check if bridge port has sub-interface when trying to derive untagged vlan

---

## 0.5.6

### CHANGES

1. Changing `get/interfaces` `lag` to be a parent lag name and adding `lag_id` attribute
2. `get/interfaces` for Arista adding interfaces speeds map
3. Enhancing `get/interfaces` for Arista to calculate access VLAN id for SVI interfaces
4. Changing `vrf` to be `None` for get bgp peerings, if BGP peering belongs to global/default/master VRF

### TEMPLATES

1. Added `platform/cisco_xr_show_running_config_interface.txt` refactoring to alight with interfaces getter data
2. Added `platform/juniper_junos_show_configuration_interfaces_pipe_display_set.txt` template
3. Added `platform/arista_eos_show_lldp_neighbors_detail_pipe_json.txt` template
4. Added `get/lldp_neighbors.txt` getter template supporting Arista EOS
5. Added `platform/juniper_junos_show_lldp_neighbors_detail_pipe_display_json.txt` template

---

## 0.5.5

### CHANGES

1. Changing Arista EOS bgp neighbor template to use "show ip bgp .." command instead of "show bgp .." command

---

## 0.5.4

### BUGS

1. Fixing VRF handling for `platform/cisco_xr_show_bgp_neighbors.txt` template.
2. Fixing BGP peer local ip handling for `platform/cisco_xr_show_bgp_neighbors.txt` template for newer IOS XR syntax
3. Fixing bgp peer group extraction for `platform/arista_eos_show_bgp_neighbors_vrf_all_pipe_json.txt` template for newer JSON format

---

## 0.5.3

### TEMPLATES

1. platform/arista_eos_show_running_config_section_interface
2. get/interfaces.txt

### CHANGES

1. bgp neighbors templates now return local_as and remote_as as integers not strings.
2. Removed filtering of built-in modules for Junos inventory in get_inventory getter.

---

## 0.5.2

### TEMPLATES

1. platform/arista_eos_show_bgp_neighbors_vrf_all_pipe_json.txt
2. get/bgp_neighbors.txt
3. platform/juniper_junos_show_bgp_neighbor_pipe_display_json.txt
4. platform/cisco_xr_show_bgp_neighbors.txt

---

## 0.5.1

### CHANGES

1. Enhancing `get` results return to return only parsing result for matched template

---

## 0.5.0

### Features

- **`get` template collection** – new `ttp_templates/get/` directory holds getter templates
  modelled after [NAPALM getters](https://napalm.readthedocs.io/en/latest/base.html). Each
  getter bundles platform-specific `<extend>` references and returns a normalised,
  platform-agnostic structure regardless of which vendor's output is supplied.

- **`inventory` getter template** – first getter: `get/inventory.txt` supports
  Cisco IOS-XR (`cisco_xr`), Cisco NXOS (`cisco_nxos`, `nxos`), Arista EOS
  (`arista_eos`, `eos`), and Juniper Junos (`juniper_junos`, `junos`).
  Returns a list of dicts with keys `slot`, `description`, `module`, `serial`.

- **`get_template(get=...)` argument** – `get_template` now accepts a `get` keyword
  argument to load a getter template by name (e.g. `get_template(get="inventory")`).
  The `.txt` extension is optional.

- **`parse_output(get=..., platform=...)` routing** – `parse_output` updated to
  handle getter templates: when `get` is supplied the `platform` argument is
  **required** and is used to select the correct platform-specific input section
  inside the getter template. Raises `ValueError` when `platform` is omitted and
  `RuntimeError` when no input in the getter supports the given platform.

- **`list_templates()` includes `"get"` key** – the dict returned by `list_templates`
  now has a `"get"` top-level key listing all getter template filenames.

- **`list_templates_refs()` new function** – returns a flat, sorted list of
  `ttp://` URI strings for every template across all collections (`platform`,
  `yang`, `misc`, `get`). Every URI is directly loadable via
  `get_template(path=ref)`. Supports the same `pattern` glob filter as
  `list_templates`.

### Templates

- Added `ttp://get/inventory.txt` – multi-platform inventory getter template.
- Updated `ttp://platform/cisco_xr_show_inventory.txt` – added `platform` list
  to the input block for getter routing compatibility.
- Updated `ttp://platform/arista_eos_show_inventory_pipe_json.txt` – added
  `platform` list with `arista_eos` and `eos` entries.
- Updated `ttp://platform/cisco_nxos_show_inventory_pipe_json_pretty.txt` – added
  `platform` list with `cisco_nxos` and `nxos` entries.
- Updated `ttp://platform/juniper_junos_show_chassis_hardware_pipe_json.txt` – added
  `platform` list with `juniper_junos` and `junos` entries.

---

## v0.4.0

### Bugs

- **Bug 1** – `parse_output` now raises `ValueError` with a descriptive message
  when called without any valid template-locating argument (previously the
  `None` returned by `get_template` was silently forwarded to the TTP
  constructor, causing confusing downstream errors).
- **Bug 2** – Fixed path-traversal vulnerability (OWASP A01) in `get_template`.
  The resolved template filename is now verified with `os.path.realpath` to
  confirm it falls inside the package directory before the file is opened;
  crafted paths such as `path="../../etc/passwd"` now raise `ValueError`.
- **Bug 3** – Fixed `list_templates` crashing with `AttributeError` when a
  template file is placed directly inside the `misc/` root directory (rather
  than in a subdirectory). The leaf-assignment logic now checks whether the
  target key already holds a dict; if it does, the files are stored under the
  empty-string sub-key instead of overwriting the dict with a list.
- **Bug 4** – `list_templates` now returns file lists in sorted alphabetical
  order. Previously `os.walk` / `os.listdir` produced non-deterministic
  ordering across operating systems and filesystems, making the output
  unreliable for callers and difficult to test reliably.
- **Bug 5** – Fixed prefix-ambiguity in `short_interface_names` (`ttp_vars.py`).
  The `2GE` patterns `'^Tw'` and `'^Two'` were broad enough to also match
  `TwoHundredGigabitEthernet*` (200GE) names because `2GE` appeared before
  `200GE` in the dict. Negative look-ahead anchors
  (`r'^Tw(?!entyFive|oHundred)'` and `r'^Two(?!Hundred)'`) were added so
  only genuine 2GE interface names are matched.

### Changes

- Python minimum version bumped to 3.10.
- Improved logging throughout all public API functions.
- Improved type hint annotations and converted docstrings to Google format.
- Improved inline comments for clarity.
- Enhancing tests suite

---

## v0.3.2

### Templates

- Added `misc/Netbox` folder with templates for Junos, IOS-XR, and Arista devices configuration.

---

## v0.3.1

### Templates

- Added `ttp://misc/N2G/cli_ip_data/arista_eos.txt` template to parse Arista EOS IP details for N2G L3 diagrams.

---

## v0.3.0

### Features

- Added `list_templates` method to list available templates.

### Bugs

- Fixed Cisco IOS `show running-configuration` to correct command: `show running-config`.
- Updated N2G IOS-XR `cli_ip_data` template to match `ipv4 address 1.1.1.1/32` style config.

### Templates

- Updated all N2G templates to have default input with required commands and platform attributes.

---

## v0.2.0

### Changes

- Moved to Poetry for dependency management.

### Templates

Added templates:

- `ttp://platform/juniper_junos_show_isis_database_verbose_pipe_no_more.txt`
- `ttp://misc/N2G/cli_l2_data/juniper.txt`
- `ttp://misc/N2G/cli_isis_data/juniper.txt`
- `ttp://platform/arista_eos_show_hostname.txt`

Modified templates:

- `ttp://platform/cisco_xr_show_isis_database_verbose.txt` – updated produced data structure to key LSPs by hostname.

---

## v0.1.3

### Bugs

- Fixed TTP Templates docs example path formation: the correct path is `ttp://misc/Netmiko/cisco.ios.arp.txt`, not `ttp://misc.Netmiko.cisco.ios.arp.txt`.

### New Templates

- Added N2G templates.

---

## v0.1.2

### Minor Features

- Added support for `get_template` to source a template by path using the `ttp://` URI scheme.
- Added `ttp_vars.py` to repository to store common TTP variables.
- Added `short_interface_names` dictionary in `ttp_vars.py` for use with `resuball` to normalize interface names to shorter abbreviations.

### New Templates

- `misc/Netmiko/cisco.ios.arp.txt`
- `misc/Netmiko/cisco.ios.cfg.ip.txt`
- `misc/Netmiko/cisco.iosxr.arp.txt`
- `misc/Netmiko/huawei.vrp.cfg.ip.txt`
- `yang/openconfig-lldp_cisco_ios.txt`
- `yang/openconfig-lldp_cisco_nxos.txt`
- `yang/openconfig-lldp_cisco_xr.txt`
- `misc/Netmiko/cisco.iosxr.cfg.ip.txt`
- `platform/arista_eos_show_hostname.txt`
