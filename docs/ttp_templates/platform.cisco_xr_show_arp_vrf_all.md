Reference path:
```
ttp://platform/cisco_xr_show_arp_vrf_all.txt
```

---



Template to parse Cisco IOS XR `show arp`, `show arp vrf all` and
`show ipv6 neighbors` output and normalize it for the `arp` getter.

Returns a list of dictionaries, one per entry, with `ip`, `mac`, `interface`,
`vrf`, `age` and `state` keys (see the `arp` getter).

Notes:

- `show arp vrf all` leaves out the default table (XRd 26.2.1), so the IPv4
  input takes `show arp` too; an entry in both outputs is returned once.
  `show ipv6 neighbors` lists every VRF's entries.
- Neither table names the VRF: each entry takes its interface's VRF from
  `show ipv4 vrf all interface brief` and `show ipv6 vrf all interface brief`.
  Without them `vrf` is `null`.
- `show ipv6 neighbors` abbreviates interface names (`Mg0/RP0/CPU0/0`); they
  are expanded against the interface brief output (`MgmtEth0/RP0/CPU0/0`).
- ARP ages (`hh:mm:ss`) are returned in seconds. IPv6 entries have no age.
- Unresolved entries (`Deleted`, no MAC address) are returned as
  `incomplete`. A configured IPv6 neighbor is printed as `REACH` and returned
  as `reachable`.
- The router's own addresses (`Interface`) and multicast adjacencies are left
  out.



---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_arp" results="per_template">
<doc>
Template to parse Cisco IOS XR 'show arp', 'show arp vrf all' and
'show ipv6 neighbors' output and normalize it for the 'arp' getter.

Returns a list of dictionaries, one per entry, with 'ip', 'mac', 'interface',
'vrf', 'age' and 'state' keys (see the 'arp' getter).

Notes:

- 'show arp vrf all' leaves out the default table (XRd 26.2.1), so the IPv4
  input takes 'show arp' too; an entry in both outputs is returned once.
  'show ipv6 neighbors' lists every VRF's entries.
- Neither table names the VRF: each entry takes its interface's VRF from
  'show ipv4 vrf all interface brief' and 'show ipv6 vrf all interface brief'.
  Without them 'vrf' is 'null'.
- 'show ipv6 neighbors' abbreviates interface names ('Mg0/RP0/CPU0/0'); they
  are expanded against the interface brief output ('MgmtEth0/RP0/CPU0/0').
- ARP ages ('hh:mm:ss') are returned in seconds. IPv6 entries have no age.
- Unresolved entries ('Deleted', no MAC address) are returned as
  'incomplete'. A configured IPv6 neighbor is printed as 'REACH' and returned
  as 'reachable'.
- The router's own addresses ('Interface') and multicast adjacencies are left
  out.
</doc>

<input name="ipv4">
commands = ["show arp", "show arp vrf all"]
platform = [
    "cisco_xr",    # netmiko
    "iosxr",       # napalm
    "cisco_iosxr", # scrapli
]
</input>

<input name="ipv6">
commands = ["show ipv6 neighbors"]
platform = ["cisco_xr", "iosxr", "cisco_iosxr"]
</input>

<input name="ipv4_interfaces">
commands = ["show ipv4 vrf all interface brief"]
platform = ["cisco_xr", "iosxr", "cisco_iosxr"]
</input>

<input name="ipv6_interfaces">
commands = ["show ipv6 vrf all interface brief"]
platform = ["cisco_xr", "iosxr", "cisco_iosxr"]
</input>

<macro>
def transform_arp_to_records(payload):
    from ttp_templates.utils.arp import transform_cisco_xr

    return transform_cisco_xr(payload)
</macro>

<!-- not bound to an input, so show arp vrf all output parses on its own -->
<group name="ipv4*">
{{ ip | IP | _start_ }} {{ age }} {{ mac }} {{ state }} {{ ignore }} {{ interface }}
</group>

<group name="ipv6*" input="ipv6">
{{ ip | _start_ }} {{ age }} {{ mac }} {{ state }} {{ interface }} {{ ignore }}
</group>

<group name="ipv4_interfaces*" input="ipv4_interfaces">
{{ interface | _start_ }} {{ ignore }} {{ ignore }} {{ ignore }} {{ vrf }}
</group>

<group name="ipv6_interfaces*" input="ipv6_interfaces">
{{ interface | _start_ }} {{ ignore }} Vrf-Name: {{ vrf }}
</group>

<output macro="transform_arp_to_records"/>

</template>

```
</details>