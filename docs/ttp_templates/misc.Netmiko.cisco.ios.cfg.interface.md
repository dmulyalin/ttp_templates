Reference path:
```
ttp://misc/Netmiko/cisco.ios.cfg.interface.txt
```

---



*Authored by Codex GPT-5.*

Template to parse Cisco IOS interfaces configuration and normalize it to a
flat list of dictionaries suitable for Netbox import.

This template requires output of 'show running-config | section interface'.

The transform macro returns a list of dictionaries where each dictionary
contains the following keys (missing values are set to `null` / `None`):

- `name`: interface name string (e.g. GigabitEthernet0/1, Vlan100)
- `type`: ``other`` by default; ``bridge`` if "vlan" or "bvi" in name;
    ``lag`` if "port-channel" in name; ``virtual`` if "loopback", "tunnel",
    or if the interface name contains a dot (`.`)
- `enabled`: boolean; interfaces are `True` by default unless explicitly
    shutdown in the config
- `parent`: parent interface name or `null` (if the interface name contains
    a dot the parent is the part before the dot)
- `lag_id`: lag identifier integer (channel-group number) or `null`
- `lag_type`: ``lag`` for standard port channels or `null`
- `lacp_mode`: LACP mode string (e.g. ``active``, ``passive``) or `null`
- `lag`: Name of parent LAG interface e.g. `Port-channel10` or `null`
- `mtu`: integer MTU or `null`
- `mac_address`: string in MAC EUI format or `null`
- `speed`: integer speed in kbit/s or `null`
- `duplex`: string duplex setting or `null`
- `description`: string (empty string when not set)
- `mode`: ``tagged`` / ``access`` or `null`
- `untagged_vlan`: integer or `null`
- `tagged_vlans`: list of integers (empty list when none)
- `qinq_svlan`: integer inner VLAN from `second-dot1q` or `null`
- `vrf`: string or `null`
- `ipv4_addresses`: list of strings with IP/prefix (e.g. 10.0.0.1/24)
- `ipv6_addresses`: list of strings with IP/prefix (e.g. 2001:db8::1/64)

Example normalized output (YAML):

```yaml
- description: Users SVI
  duplex: null
  enabled: true
  ipv4_addresses:
  - 192.0.2.1/24
  ipv6_addresses: []
  lacp_mode: null
  lag: null
  lag_id: null
  lag_type: null
  mac_address: null
  mode: access
  mtu: 1500
  name: Vlan100
  parent: null
  qinq_svlan: null
  speed: null
  tagged_vlans: []
  type: bridge
  untagged_vlan: 100
  vrf: USERS
```




---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "show running-config | section interface" output for Cisco IOS.
</doc>

<input>
commands = ["show running-config | section interface"]
</input>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_interface.txt"/>
```
</details>