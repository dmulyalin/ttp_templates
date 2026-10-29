Reference path:
```
ttp://get/ping.txt
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



Template to parse Cisco ASA `ping` output and normalize it for the `ping`
getter.

The command is `ping` followed by the destination and any options, for example
`ping 192.0.2.1` or `ping inside 2001:db8::1`. The ASA sends 5 echoes by
default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
(`null` when no reply was received). Output with no success rate line, such as
an invalid interface name, returns an empty list.

Notes:

- The ASA reports round-trip times in whole milliseconds.
- With no route to the destination the ASA stops after the first echo and
  reports `0/1`, so `packets_sent` is 1.



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



Template to parse Cisco NX-OS `ping` and `ping6` output and normalize it for
the `ping` getter.

The command is `ping` (or `ping6` for IPv6) followed by the destination and
any options, for example `ping 192.0.2.1 vrf management`. NX-OS sends 5
echoes by default.

Returns a list with one dictionary per ping: destination, packets sent and
received, packet loss in percent, and round-trip min/avg/max in milliseconds
(`null` when no reply was received). Output with no statistics, such as an
invalid VRF, returns an empty list.



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
<template name="ping" results="per_template">
<doc>
Getter template to parse ping results for network devices.

Supported platforms:

- Arista EOS
- Cisco ASA
- Cisco IOS
- Cisco NX-OS
- Linux

Ping needs a destination, so the collected command is 'ping' followed by the
destination and options, for example 'ping 192.0.2.1'. The network platforms
send 5 echoes by default; on Linux use 'ping -c 5 192.0.2.1', as it otherwise
pings until interrupted.

Returns a normalized list of dictionaries, one per ping, with these keys:

- 'destination' - destination as the device printed it, lowercase
- 'packets_sent' - echo requests sent
- 'packets_received' - echo replies received
- 'packet_loss_percent' - packets lost as a percentage of packets sent
- 'rtt_min_ms' / 'rtt_avg_ms' / 'rtt_max_ms' - round-trip times in
  milliseconds, or 'null' when no reply was received

Output without ping statistics, such as an invalid command, VRF or interface,
returns an empty list.
</doc>

<extend template="ttp://platform/arista_eos_ping.txt"/>

<extend template="ttp://platform/cisco_asa_ping.txt"/>

<extend template="ttp://platform/cisco_ios_ping.txt"/>

<extend template="ttp://platform/cisco_nxos_ping.txt"/>

<extend template="ttp://platform/linux_ping.txt"/>

</template>

```
</details>