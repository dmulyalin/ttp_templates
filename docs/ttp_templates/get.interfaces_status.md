Reference path:
```
ttp://get/interfaces_status.txt
```

---



Template to parse Arista EOS `show interfaces` output and normalize it for the
`interfaces_status` getter.

Returns a list of dictionaries with interface identity, state, physical
properties, counter-clearing information, error and packet counters, and
averaged input/output rates. `speed_bps`, `rate_bps_in`, and `rate_bps_out`
are in bit/s. `rate_pps_in` and `rate_pps_out` are in packets/s.
`rate_interval` is the rate averaging interval in seconds. Values not reported
for an interface are returned as `null`.



Template to parse Cisco IOS `show interfaces` output and normalize it for the
`interfaces_status` getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, packet rates are in packets/s, and `rate_interval` is in seconds.
Values not reported by IOS are returned as `null`.



Template to parse Cisco IOS-XR `show interfaces` output and normalize it for
the `interfaces_status` getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, packet rates are in packets/s, and `rate_interval` is in seconds.
Values not reported by IOS-XR are returned as `null`.



Template to parse Cisco NX-OS `show interface` output and normalize it for the
`interfaces_status` getter.

Returns a list of dictionaries with interface state, physical properties,
counters, errors, and averaged rates. Interface speed and input/output rates
are in bit/s, packet rates are in packets/s, and `rate_interval` is in seconds.
Values not reported by NX-OS are returned as `null`.



Template to parse Juniper Junos `show interfaces` output and normalize it for
the `interfaces_status` getter.

Returns physical and logical interfaces as a list of dictionaries. Interface
speed and input/output rates are in bit/s, packet rates are in packets/s, and
values not reported by Junos are returned as `null`. `rate_interval` is `null`
because this output does not state the rate averaging interval.



---

<details><summary>Template Content</summary>
```
<template name="interfaces_status" results="per_template">
<doc>
Getter template to parse operational interface status for network devices.

Supported platforms:

- Arista EOS
- Cisco IOS
- Cisco IOS-XR
- Cisco NX-OS
- Juniper Junos

Returns a normalized list of dictionaries with these keys:

- 'name' - interface name
- 'description' - configured description or 'null'
- 'mtu' - MTU in bytes or 'null'
- 'mac_address' - MAC address or 'null'
- 'duplex' - duplex mode or 'null'
- 'status_admin' - administrative state ('up' or 'down')
- 'status_oper' - operational state ('up' or 'down')
- 'speed_bps' - interface speed in bit/s or 'null'
- 'last_cleared' - time since counters were cleared, 'never', or 'null'
- 'transitions' - link state transition count or 'null'
- 'errors_in' / 'errors_out' - input/output error counters or 'null'
- 'crc_errors' - CRC error counter or 'null'
- 'packets_in' / 'packets_out' - cumulative packet counters or 'null'
- 'rate_bps_in' / 'rate_bps_out' - averaged input/output rates in bit/s or 'null'
- 'rate_pps_in' / 'rate_pps_out' - averaged input/output rates in packets/s or 'null'
- 'rate_interval' - rate averaging interval in seconds or 'null'
</doc>

<extend template="ttp://platform/arista_eos_show_interfaces.txt"/>

<extend template="ttp://platform/cisco_ios_show_interfaces.txt"/>

<extend template="ttp://platform/cisco_xr_show_interfaces.txt"/>

<extend template="ttp://platform/cisco_nxos_show_interface.txt"/>

<extend template="ttp://platform/juniper_junos_show_interfaces.txt"/>

</template>

```
</details>