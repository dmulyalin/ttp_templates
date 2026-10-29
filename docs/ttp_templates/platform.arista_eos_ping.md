Reference path:
```
ttp://platform/arista_eos_ping.txt
```

---



Template to parse Arista EOS `ping` output and normalize it for the `ping`
getter.

The command is `ping` followed by the destination and any options, for example
`ping 192.0.2.1` or `ping vrf MGMT 2001:db8::1`. EOS sends 5 echoes by default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
(`null` when no reply was received). Output with no statistics, such as
`ping: connect: Network is unreachable`, returns an empty list.



---

<details><summary>Template Content</summary>
```
<template name="arista_eos_ping" results="per_template">
<doc>
Template to parse Arista EOS 'ping' output and normalize it for the 'ping'
getter.

The command is 'ping' followed by the destination and any options, for example
'ping 192.0.2.1' or 'ping vrf MGMT 2001:db8::1'. EOS sends 5 echoes by default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
('null' when no reply was received). Output with no statistics, such as
'ping: connect: Network is unreachable', returns an empty list.
</doc>

<input>
commands = [
    "ping"
]
platform = [
    "arista_eos", # scrapli and netmiko
    "eos", # NAPALM
]
</input>

<macro>
def transform_ping_to_records(payload):
    from ttp_templates.utils.ping import transform_ping

    return transform_ping(payload)
</macro>

<group>
--- {{ destination | _start_ }} ping statistics ---
{{ sent | to_int }} packets transmitted, {{ received | to_int }} received, {{ ignore(".+") }}
rtt min/avg/max/mdev = {{ rtt }} ms
rtt min/avg/max/mdev = {{ rtt }} ms, ipg/ewma {{ ignore }} ms
</group>

<output macro="transform_ping_to_records"/>

</template>

```
</details>