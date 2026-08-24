Reference path:
```
ttp://platform/cisco_nxos_show_interface.txt
```

---



Template to parse Cisco NX-OS `show interface` output and normalize it for the
`interfaces_status` getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, utilization is a percentage of interface speed, packet rates are
in packets/s, and `rate_interval` is in seconds. Values not reported by NX-OS
are returned as `null`.



---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos_interfaces_status" results="per_template">
<doc>
Template to parse Cisco NX-OS 'show interface' output and normalize it for the
'interfaces_status' getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, utilization is a percentage of interface speed, packet rates are
in packets/s, and 'rate_interval' is in seconds. Values not reported by NX-OS
are returned as 'null'.
</doc>

<input>
commands = [
    "show interface"
]
platform = [
    "cisco_nxos", # scrapli and netmiko
    "nxos", # NAPALM
]
</input>

<macro>
def transform_interfaces_to_status_records(payload):
    from ttp_templates.utils.cisco_nxos_process_show_interface import transform_interfaces_status

    return transform_interfaces_status(payload)
</macro>

<group>
{{ name | _start_ }} is {{ interface_status | ORPHRASE }}, line protocol is {{ protocol_status | ORPHRASE }}
{{ name | _start_ }} is {{ interface_status | ORPHRASE }}
admin state is {{ admin_state | ORPHRASE }},
admin state is {{ admin_state | ORPHRASE }}
  Admin State: {{ admin_state | ORPHRASE }}
  Hardware: {{ hardware | ORPHRASE }}, address: {{ mac_address | mac_eui }} (bia {{ bia | mac_eui }})
  Hardware is {{ hardware | ORPHRASE }}, address is  {{ mac_address | mac_eui }}
  Hardware: {{ hardware | ORPHRASE }}
  Hardware is {{ hardware | ORPHRASE }}
  Description: {{ description | ORPHRASE }}
  Port Description: {{ description | ORPHRASE }}
  MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit, DLY {{ delay | ORPHRASE }},
  MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit, DLY {{ delay | ORPHRASE }}
  MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit , DLY {{ delay | ORPHRASE }}
  MTU {{ mtu | to_int }} bytes,  BW {{ speed_kbps | to_int }} Kbit,, {{ mtu_details | ORPHRASE }}
    MTU {{ mtu | to_int }} bytes, BW {{ speed_kbps | to_int }} Kbit
  MTU {{ mtu | to_int }} bytes
  {{ duplex }}-duplex, {{ displayed_speed | ORPHRASE }}, {{ link_details | ORPHRASE }}
  {{ duplex }}-duplex, {{ displayed_speed | ORPHRASE }}
  Last clearing of "show interface" counters {{ last_cleared | ORPHRASE }}
    Last clearing of "show interface" counters {{ last_cleared | ORPHRASE }}
  {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec, {{ rate_pps_in | to_int }} packets/sec
  {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec, {{ rate_pps_out | to_int }} packets/sec
    {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec, {{ rate_pps_in | to_int }} packets/sec
    {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec, {{ rate_pps_out | to_int }} packets/sec
    {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec
    {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec
    {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec, {{ rate_details_in | ORPHRASE }}
    {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec, {{ rate_details_out | ORPHRASE }}
  {{ rate_interval_in | to_int }} {{ rate_interval_unit_in }} input rate {{ rate_bps_in | to_int }} bits/sec, {{ rate_details_in | ORPHRASE }}
  {{ rate_interval_out | to_int }} {{ rate_interval_unit_out }} output rate {{ rate_bps_out | to_int }} bits/sec, {{ rate_details_out | ORPHRASE }}
    {{ packets_in | to_int }} input packets {{ input_packet_details | ORPHRASE }}
    {{ packets_out | to_int }} output packets {{ output_packet_details | ORPHRASE }}
    {{ packets_in | to_int }} packets input, {{ input_packet_details | ORPHRASE }}
    {{ packets_out | to_int }} packets output, {{ output_packet_details | ORPHRASE }}
    {{ packets_in | to_int }} packets input {{ input_packet_details | ORPHRASE }}
    {{ packets_out | to_int }} packets output {{ output_packet_details | ORPHRASE }}
    input: {{ packets_in | to_int }} pkts, {{ input_packet_details | ORPHRASE }} - output: {{ packets_out | to_int }} pkts, {{ output_packet_details | ORPHRASE }}
    {{ errors_in | to_int }} input error  {{ short_frame | to_int }} short frame  {{ overrun | to_int }} overrun   {{ underrun | to_int }} underrun  {{ ignored | to_int }} ignored
    {{ errors_in | to_int }} input error {{ input_error_details | ORPHRASE }}
    {{ errors_in | to_int }} input errors {{ input_error_details | ORPHRASE }}
    {{ runts | to_int }} runts  {{ giants | to_int }} giants  {{ crc_errors | to_int }} CRC  {{ input_no_buffer | to_int }} no buffer
    {{ runts | to_int }} runts  {{ giants | to_int }} giants  {{ crc_errors | to_int }} CRC/FCS  {{ input_no_buffer | to_int }} no buffer
    {{ crc_errors | to_int }} CRC, {{ crc_details | ORPHRASE }}
        {{ crc_errors | to_int }} CRC,  {{ crc_details | ORPHRASE }}
    {{ errors_out | to_int }} output error  {{ collisions | to_int }} collision  {{ deferred | to_int }} deferred  {{ late_collision | to_int }} late collision
    {{ errors_out | to_int }} output errors  {{ collisions | to_int }} collision  {{ deferred | to_int }} deferred  {{ late_collision | to_int }} late collision
    {{ errors_out | to_int }} output error {{ output_error_details | ORPHRASE }}
    {{ errors_out | to_int }} output errors {{ output_error_details | ORPHRASE }}
    last clearing of "show interface" counters {{ last_cleared | ORPHRASE }}
</group>

<output macro="transform_interfaces_to_status_records"/>

</template>

```
</details>