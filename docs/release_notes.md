# Release Notes

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

## v0.3.2

### Templates

- Added `misc/Netbox` folder with templates for Junos, IOS-XR, and Arista devices configuration.

## v0.3.1

### Templates

- Added `ttp://misc/N2G/cli_ip_data/arista_eos.txt` template to parse Arista EOS IP details for N2G L3 diagrams.

## v0.3.0

### Features

- Added `list_templates` method to list available templates.

### Bugs

- Fixed Cisco IOS `show running-configuration` to correct command: `show running-config`.
- Updated N2G IOS-XR `cli_ip_data` template to match `ipv4 address 1.1.1.1/32` style config.

### Templates

- Updated all N2G templates to have default input with required commands and platform attributes.

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

## v0.1.3

### Bugs

- Fixed TTP Templates docs example path formation: the correct path is `ttp://misc/Netmiko/cisco.ios.arp.txt`, not `ttp://misc.Netmiko.cisco.ios.arp.txt`.

### New Templates

- Added N2G templates.

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