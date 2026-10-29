Reference path:
```
ttp://platform/cisco_asa_show_arp.txt
```

---



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



---

<details><summary>Template Content</summary>
```
<template name="cisco_asa_arp" results="per_template">
<doc>
Template to parse Cisco ASA 'show arp' and 'show ipv6 neighbor' output and
normalize it for the 'arp' getter.

Returns a list of dictionaries, one per entry, with 'ip', 'mac', 'interface',
'vrf', 'age' and 'state' keys (see the 'arp' getter).

Notes:

- Both tables name the interface by its nameif; with 'show nameif' output
  the interface's name is returned instead ('GigabitEthernet0/1.977' for
  'inside'), without it the nameif.
- The ASA has no VRFs, so 'vrf' is 'null'.
- 'show arp' prints ages in seconds, 'show ipv6 neighbor' in minutes; both
  are returned in seconds. A '-' for the age marks a configured entry
  ('static', no age).
- Entries 'show arp' marks 'alias', the ASA's own proxy ARP addresses, are
  left out.
</doc>

<input name="ipv4">
commands = ["show arp"]
platform = [
    "cisco_asa", # scrapli community and netmiko
    "asa", # NAPALM community driver
]
</input>

<input name="ipv6">
commands = ["show ipv6 neighbor"]
platform = ["cisco_asa", "asa"]
</input>

<input name="nameif">
commands = ["show nameif"]
platform = ["cisco_asa", "asa"]
</input>

<macro>
def transform_arp_to_records(payload):
    from ttp_templates.utils.arp import transform_cisco_asa

    return transform_cisco_asa(payload)
</macro>

<group name="ipv4*" input="ipv4">
{{ ignore("\\s+") }}{{ interface | _start_ }} {{ ip | IP }} {{ mac }} {{ age }}
{{ interface | _start_ }} {{ ip | IP }} {{ mac }} {{ age }}
</group>

<group name="ipv6*" input="ipv6">
{{ ip | _start_ }} {{ age }} {{ mac }} {{ state }} {{ interface }}
</group>

<group name="nameif*" input="nameif">
{{ interface | _start_ }} {{ name }} {{ security | DIGIT }}
</group>

<output macro="transform_arp_to_records"/>

</template>

```
</details>