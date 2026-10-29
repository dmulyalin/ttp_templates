Reference path:
```
ttp://platform/linux_ping.txt
```

---



Template to parse Linux iputils `ping` output and normalize it for the `ping`
getter.

The command is `ping` followed by the destination and options. Linux pings
until interrupted unless given a count, so use `ping -c 5 192.0.2.1` to match
the other platforms' default of 5 echoes.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
(`null` when no reply was received). Output with no statistics, such as
`ping: connect: Network is unreachable`, returns an empty list.



---

<details><summary>Template Content</summary>
```
<template name="linux_ping" results="per_template">
<doc>
Template to parse Linux iputils 'ping' output and normalize it for the 'ping'
getter.

The command is 'ping' followed by the destination and options. Linux pings
until interrupted unless given a count, so use 'ping -c 5 192.0.2.1' to match
the other platforms' default of 5 echoes.

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
    "linux",
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