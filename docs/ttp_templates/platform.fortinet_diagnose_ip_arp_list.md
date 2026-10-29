Reference path:
```
ttp://platform/fortinet_diagnose_ip_arp_list.txt
```

---



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



---

<details><summary>Template Content</summary>
```
<template name="fortinet_arp" results="per_template">
<doc>
Template to parse Fortinet FortiOS 'diagnose ip arp list' and
'diagnose ipv6 neighbor-cache list' output and normalize it for the 'arp'
getter.

Returns a list of dictionaries, one per entry, with 'ip', 'mac', 'interface',
'vrf', 'age' and 'state' keys (see the 'arp' getter).

Notes:

- These are the kernel's tables: 'state' comes from its hex NUD flags, and
  'age' from 'confirm' (hundredths of a second), returned in seconds.
  NOARP entries, such as multicast and the VDOM's own, are left out.
- Neither table names the VRF: each entry takes its interface's VRF number
  from 'show system interface' ('set vrf'). Without it 'vrf' is 'null',
  as it is for VRF 0.
</doc>

<input name="ipv4">
commands = ["diagnose ip arp list"]
platform = [
    "fortinet", # netmiko
    "fortinet_fortios", # scrapli community
    "fortios", # NAPALM community driver
]
</input>

<input name="ipv6">
commands = ["diagnose ipv6 neighbor-cache list"]
platform = ["fortinet", "fortinet_fortios", "fortios"]
</input>

<input name="interfaces">
commands = ["show system interface"]
platform = ["fortinet", "fortinet_fortios", "fortios"]
</input>

<macro>
def transform_arp_to_records(payload):
    from ttp_templates.utils.arp import transform_fortinet

    return transform_fortinet(payload)
</macro>

<group name="ipv4*" input="ipv4">
index={{ ignore }} ifname={{ interface | _start_ }} {{ ip }} {{ mac }} state={{ state }} use={{ ignore }} confirm={{ confirm }} update={{ ignore }} ref={{ ignore }}
index={{ ignore }} ifname={{ interface | _start_ }} {{ ip }} state={{ state }} use={{ ignore }} confirm={{ confirm }} update={{ ignore }} ref={{ ignore }}
</group>

<group name="ipv6*" input="ipv6">
ifindex={{ ignore }} ifname={{ interface | _start_ }} {{ ip }} {{ mac }} state={{ state }} use={{ ignore }} confirm={{ confirm }} update={{ ignore }} ref={{ ignore }}
ifindex={{ ignore }} ifname={{ interface | _start_ }} {{ ip }} state={{ state }} use={{ ignore }} confirm={{ confirm }} update={{ ignore }} ref={{ ignore }}
</group>

<group name="interfaces*" input="interfaces">
    edit "{{ interface | _start_ }}"
        set vrf {{ vrf }}
    next {{ _end_ }}
</group>

<output macro="transform_arp_to_records"/>

</template>

```
</details>