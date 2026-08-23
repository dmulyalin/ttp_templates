Reference path:
```
ttp://platform/juniper_junos_show_interfaces.txt
```

---



Template to parse Juniper Junos `show interfaces` output and normalize it for
the `interfaces_status` getter.

Returns physical and logical interfaces as a list of dictionaries. Interface
speed and input/output rates are in bit/s, packet rates are in packets/s, and
values not reported by Junos are returned as `null`. `rate_interval` is `null`
because this output does not state the rate averaging interval.



---

<details><summary>Template Content</summary>
```
<template name="juniper_junos_interfaces_status" results="per_template">
<doc>
Template to parse Juniper Junos 'show interfaces' output and normalize it for
the 'interfaces_status' getter.

Returns physical and logical interfaces as a list of dictionaries. Interface
speed and input/output rates are in bit/s, packet rates are in packets/s, and
values not reported by Junos are returned as 'null'. 'rate_interval' is 'null'
because this output does not state the rate averaging interval.
</doc>

<input>
commands = [
    "show interfaces"
]
platform = [
    "juniper_junos", # scrapli and netmiko
    "junos", # NAPALM
]
</input>

<macro>
def transform_interfaces_to_status_records(payload):
    from ttp_templates.utils.juniper_junos_process_show_interfaces import transform_interfaces_status

    return transform_interfaces_status(payload)
</macro>

<group>
Physical interface: {{ name | _start_ }}, {{ status_admin_raw }}, Physical link is {{ status_oper_raw }}
  Logical interface {{ name | _start_ }} (Index {{ index }}) (SNMP ifIndex {{ snmp_index | let("status_admin_raw", "Enabled") }})
  Description: {{ description | ORPHRASE }}
  Link-level type: {{ hardware }}, MTU: {{ mtu_raw }}, MRU: {{ mru }}, LAN-PHY mode, Speed: {{ displayed_speed }}, {{ link_details | ORPHRASE }}
  Link-level type: {{ hardware }}, MTU: {{ mtu_raw }}, {{ link_details | ORPHRASE }}
  Link-level type: {{ hardware }}, MTU: {{ mtu_raw }}
  Type: {{ interface_type }}, Link-level type: {{ hardware }}, MTU: {{ mtu_raw }}, Speed: {{ displayed_speed }}
  Link-mode: {{ duplex }}-duplex, Speed: {{ displayed_speed }}, {{ link_mode_details | ORPHRASE }}
  Current address: {{ mac_address | mac_eui }}, Hardware address: {{ hardware_address | mac_eui }}
  Input rate     : {{ rate_bps_in | to_int }} bps ({{ rate_pps_in | to_int }} pps)
  Output rate    : {{ rate_bps_out | to_int }} bps ({{ rate_pps_out | to_int }} pps)
    Flags: {{ status_oper_raw }} {{ logical_flags | _line_ }}
    Input packets : {{ packets_in | to_int }}
    Output packets: {{ packets_out | to_int }}
    Protocol inet, MTU: {{ mtu_raw }}
</group>

<output macro="transform_interfaces_to_status_records"/>

</template>

```
</details>