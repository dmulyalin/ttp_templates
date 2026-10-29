Reference path:
```
ttp://platform/arista_eos_show_ip_arp_vrf_all_pipe_json.txt
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



---

<details><summary>Template Content</summary>
```
<template name="arista_eos_arp" results="per_template">
<doc>
Template to parse Arista EOS 'show ip arp vrf all | json' and
'show ipv6 neighbors vrf all | json' output and normalize it for the 'arp'
getter.

Returns a list of dictionaries, one per entry, with 'ip', 'mac', 'interface',
'vrf', 'age' and 'state' keys (see the 'arp' getter).

Notes:

- IPv4 ages are in seconds. The IPv6 table's 'age' isn't (a lab switch gave
  one larger than its uptime), so IPv6 entries have no age.
- The IPv6 table abbreviates interface names ('Ma0'); the EOS abbreviations
  are expanded ('Management0').
- An entry learned on an SVI names the VLAN interface and the port
  ('Vlan10, Ethernet1'); the VLAN interface is returned.
- EOS gives no state, so 'state' is 'null'.
</doc>

<input name="ipv4">
commands = ["show ip arp vrf all | json"]
platform = [
    "arista_eos", # scrapli and netmiko
    "eos", # NAPALM
]
</input>

<input name="ipv6">
commands = ["show ipv6 neighbors vrf all | json"]
platform = ["arista_eos", "eos"]
</input>

<macro>
def transform_arp_to_records(payload):
    from ttp_templates.utils.arp import transform_arista_eos

    return transform_arista_eos(payload)
</macro>

<group name="ipv4*" input="ipv4">
{{ data | _line_ }}
</group>

<group name="ipv6*" input="ipv6">
{{ data | _line_ }}
</group>

<output macro="transform_arp_to_records"/>

</template>

```
</details>