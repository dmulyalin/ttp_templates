Reference path:
```
ttp://platform/cisco_xr_show_interfaces.txt
```

---



Template to parse Cisco IOS-XR `show interfaces` output and normalize it for
the `interfaces_status` getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, packet rates are in packets/s, and `rate_interval` is in seconds.
Values not reported by IOS-XR are returned as `null`.



---

<details><summary>Template Content</summary>
```
<template name="cisco_xr_interfaces_status" results="per_template">
<doc>
Template to parse Cisco IOS-XR 'show interfaces' output and normalize it for
the 'interfaces_status' getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, packet rates are in packets/s, and 'rate_interval' is in seconds.
Values not reported by IOS-XR are returned as 'null'.
</doc>

<input>
commands = [
    "show interfaces"
]
platform = [
    "cisco_xr", # scrapli and netmiko
    "iosxr", # NAPALM
]
</input>

<macro>
def transform_interfaces_to_status_records(payload):
    from ttp_templates.utils.cisco_xr_process_show_interfaces import transform_interfaces_status

    return transform_interfaces_status(payload)
</macro>

<group>
{{ name | _start_ }} is {{ interface_status | ORPHRASE }}, line protocol is {{ protocol_status | ORPHRASE }}
  Interface state transitions: {{ transitions | to_int }}
  Hardware is {{ hardware | ORPHRASE }}, address is {{ mac_address | mac_eui }} (bia {{ bia | mac_eui }})
  Hardware is {{ hardware | ORPHRASE }}, address is {{ mac_address | mac_eui }}
  Hardware is {{ hardware | ORPHRASE }}
  Description: {{ description | ORPHRASE }}
  MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit (Max: {{ max_speed_kbps | to_int }} Kbit)
  MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit
  {{ duplex }}-duplex, {{ displayed_speed }}, {{ link_details | ORPHRASE }}
  {{ duplex }}-duplex, {{ displayed_speed }}
  Duplex {{ duplex }}, {{ displayed_speed }}, {{ link_details | ORPHRASE }}
  Last clearing of "show interface" counters {{ last_cleared | ORPHRASE }}
  {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec, {{ rate_pps_in | to_int }} packets/sec
  {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec, {{ rate_pps_out | to_int }} packets/sec
     {{ packets_in | to_int }} packets input, {{ bytes_in | to_int }} bytes, {{ input_drops | to_int }} total input drops
     {{ errors_in | to_int }} input errors, {{ crc_errors | to_int }} CRC, {{ input_error_details | ORPHRASE }}
     {{ packets_out | to_int }} packets output, {{ bytes_out | to_int }} bytes, {{ output_drops | to_int }} total output drops
     {{ errors_out | to_int }} output errors, {{ output_error_details | ORPHRASE }}
</group>

<output macro="transform_interfaces_to_status_records"/>

</template>

```
</details>