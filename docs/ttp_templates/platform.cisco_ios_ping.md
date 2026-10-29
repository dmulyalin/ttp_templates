Reference path:
```
ttp://platform/cisco_ios_ping.txt
```

---



Template to parse Cisco IOS and IOS-XE `ping` output and normalize it for the
`ping` getter.

The command is `ping` followed by the destination and any options, for example
`ping 192.0.2.1` or `ping vrf MGMT 2001:db8::1`. IOS sends 5 echoes by default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
(`null` when no reply was received). Output with no success rate line, such as
an invalid command or VRF, returns an empty list.

Notes:

- IOS reports round-trip times in whole milliseconds.
- With no route to the destination IOS stops after the first echo and reports
  `0/1`, so `packets_sent` is 1.



---

<details><summary>Template Content</summary>
```
<template name="cisco_ios_ping" results="per_template">
<doc>
Template to parse Cisco IOS and IOS-XE 'ping' output and normalize it for the
'ping' getter.

The command is 'ping' followed by the destination and any options, for example
'ping 192.0.2.1' or 'ping vrf MGMT 2001:db8::1'. IOS sends 5 echoes by default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
('null' when no reply was received). Output with no success rate line, such as
an invalid command or VRF, returns an empty list.

Notes:

- IOS reports round-trip times in whole milliseconds.
- With no route to the destination IOS stops after the first echo and reports
  '0/1', so 'packets_sent' is 1.
</doc>

<input>
commands = [
    "ping"
]
platform = [
    "cisco_ios", # scrapli and netmiko
    "ios", # NAPALM
]
</input>

<macro>
def transform_ping_to_records(payload):
    from ttp_templates.utils.ping import transform_ping

    return transform_ping(payload)
</macro>

<group>
Sending {{ ignore }}, {{ ignore }} ICMP Echos to {{ destination | _start_ }}, timeout is {{ ignore }} seconds:
Success rate is {{ ignore }} percent ({{ received | to_int }}/{{ sent | to_int }}), round-trip min/avg/max = {{ rtt }} ms
Success rate is {{ ignore }} percent ({{ received | to_int }}/{{ sent | to_int }})
</group>

<output macro="transform_ping_to_records"/>

</template>

```
</details>