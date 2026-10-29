Reference path:
```
ttp://get/arp.txt
```

---



Template to parse Arista EOS `show ip arp vrf all | json` and
`show ipv6 neighbors vrf all | json` output and normalize it for the `arp`
getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- IPv4 ages are in seconds. The IPv6 table's `age` isn't (a lab switch gave
  one larger than its uptime), so IPv6 entries have no age.
- The IPv6 table abbreviates interface names (`Ma0`); the EOS abbreviations
  are expanded (`Management0`).
- An entry learned on an SVI names the VLAN interface and the port
  (`Vlan10, Ethernet1`); the VLAN interface is returned.
- EOS gives no state, so `state` is `null`.



Template to parse Cisco ASA `show arp` and `show ipv6 neighbor` output and
normalize it for the `arp` getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- Both tables name the interface by its nameif; with `show nameif` output
  the interface's name is returned instead (`GigabitEthernet0/1.977` for
  `inside`), without it the nameif.
- The ASA has no VRFs, so `vrf` is `null`.
- `show arp` prints ages in seconds, `show ipv6 neighbor` in minutes; both
  are returned in seconds. A `-` for the age marks a configured entry
  (`static`, no age).
- Entries `show arp` marks `alias`, the ASA's own proxy ARP addresses, are
  left out.



Template to parse Cisco IOS and IOS-XE `show ip arp` and `show ipv6 neighbors`
output and normalize it for the `arp` getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- These commands list the global table only, so `vrf` is `null`. IOS has no
  command listing every VRF's table, and `show ip arp vrf NAME` doesn't name
  the VRF in its output.
- Ages are printed in minutes and returned in seconds.
- A `-` for the age marks a configured entry or one of the router's own
  addresses; both are returned as `static`, with no age.
- `show ipv6 neighbors` abbreviates interface names (`Gi1`); the common
  abbreviations are expanded (`GigabitEthernet1`), others are returned as
  printed.
- `show ip arp` output on its own, parsed with
  `parse_output(platform="cisco_ios", command="show ip arp")`, gives the IPv4
  entries.



Template to parse Cisco NX-OS `show ip arp detail vrf all | json` and
`show ipv6 neighbor vrf all | json` output and normalize it for the `arp`
getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- These forms name each entry's VRF (`adj-vrf-name`); `show ip arp vrf all`
  without `detail` doesn't.
- Ages are returned in seconds (NX-OS prints `PT11M23S` for IPv4 and
  `00:11:23` for IPv6).
- NX-OS gives no state; an entry with no MAC address is `incomplete`,
  others `null`.



Template to parse Cisco IOS XR `show arp vrf all` and `show ipv6 neighbors`
output and normalize it for the `arp` getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- Neither table names the VRF: each entry takes its interface's VRF from
  `show ipv4 vrf all interface brief` and `show ipv6 vrf all interface brief`.
  Without them `vrf` is `null`.
- `show ipv6 neighbors` abbreviates interface names (`Mg0/RP0/CPU0/0`); they
  are expanded against the interface brief output (`MgmtEth0/RP0/CPU0/0`).
- ARP ages (`hh:mm:ss`) are returned in seconds. IPv6 entries have no age.
- The router's own addresses (`Interface`) and multicast adjacencies are left
  out.
- `show arp` output has the same layout and parses the same way.



Template to parse Fortinet FortiOS `diagnose ip arp list` and
`diagnose ipv6 neighbor-cache list` output and normalize it for the `arp`
getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- These are the kernel's tables: `state` comes from its hex NUD flags, and
  `age` from `confirm` (hundredths of a second), returned in seconds.
  NOARP entries, such as multicast and the VDOM's own, are left out.
- Neither table names the VRF: each entry takes its interface's VRF number
  from `show system interface` (`set vrf`). Without it `vrf` is `null`,
  as it is for VRF 0.



Template to parse Juniper Junos `show arp no-resolve | display json` and
`show ipv6 neighbors | display json` output and normalize it for the `arp`
getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- Neither table names the routing instance: each entry takes its unit's
  instance from `show route instance detail | display json`. Without it
  `vrf` is `null`.
- Entries on units in Junos's own instances (`__juniper_private1__`, such as
  `em1.0`) are left out when the instances are given.
- Junos gives no ARP age, and the IPv6 table's `expire` is a countdown, not
  an age, so `age` is `null`.
- ARP entries have no state but `static` (flag `permanent`).



Template to parse Linux `ip -j -s neigh show` output and normalize it for the
`arp` getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- The one command lists IPv4 and IPv6 neighbors together.
- Each entry takes its link's VRF, the link's master where that is a VRF,
  from `ip -j -d link show`. Without it `vrf` is `null`.
- `age` is the kernel's `confirmed` timer, in seconds: the time since the
  neighbor was last confirmed reachable.
- NOARP entries (multicast, point-to-point links) are left out.



---

<details><summary>Template Content</summary>
```
<template name="arp" results="per_template">
<doc>
Getter template to parse the IPv4 ARP table and the IPv6 neighbor cache of
network devices.

Supported platforms:

- Arista EOS
- Cisco ASA
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Fortinet FortiOS
- Juniper Junos
- Linux

Each platform template collects its IPv4 and IPv6 tables, and where those
don't name the VRF, a command mapping interfaces to VRFs (see the support
matrix for the commands).

Returns a normalized list of dictionaries, one per entry, with these keys:

- 'ip' - neighbor IPv4 or IPv6 address, IPv6 in its compressed lowercase form
- 'mac' - MAC address, lowercase and colon-separated, or 'null' while
  unresolved
- 'interface' - interface the entry was learned on, full name, or 'null'
  where the device prints none
- 'vrf' - VRF the entry belongs to, or 'null' for the default/global/master
  table
- 'age' - seconds since the entry was learned or refreshed, or 'null' for
  static entries and where the platform gives no age
- 'state' - one of 'incomplete', 'reachable', 'stale', 'delay', 'probe',
  'failed', 'static', or 'null' where the platform gives none for a
  resolved entry

Multicast entries, the devices' own entries where the platform marks them,
and NOARP entries are left out. Per platform limits are noted in each
platform template.
</doc>

<extend template="ttp://platform/arista_eos_show_ip_arp_vrf_all_pipe_json.txt"/>

<extend template="ttp://platform/cisco_asa_show_arp.txt"/>

<extend template="ttp://platform/cisco_ios_show_ip_arp.txt"/>

<extend template="ttp://platform/cisco_nxos_show_ip_arp_detail_vrf_all_pipe_json.txt"/>

<extend template="ttp://platform/cisco_xr_show_arp_vrf_all.txt"/>

<extend template="ttp://platform/fortinet_diagnose_ip_arp_list.txt"/>

<extend template="ttp://platform/juniper_junos_show_arp_no_resolve_pipe_display_json.txt"/>

<extend template="ttp://platform/linux_ip_neigh_show.txt"/>

</template>

```
</details>