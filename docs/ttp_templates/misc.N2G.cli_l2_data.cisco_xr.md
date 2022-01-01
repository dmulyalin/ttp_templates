Reference path:
```
ttp://misc/N2G/cli_l2_data/cisco_xr.txt
```

---



This template designed to parse Cisco IOSXR configuration and CDP and LLDP neighbors.




---

<details><summary>Template Content</summary>
```
<template name="cisco_xr" results="per_template">

<doc>
This template designed to parse Cisco IOSXR configuration and CDP and LLDP neighbors.

</doc>

<vars>local_hostname="gethostname"</vars>

<macro>
def check_is_physical_port(data):
    for item in _ttp_["vars"]["physical_ports"]:
        if data.startswith(item) and not "." in item:
            return data, {"is_physical_port": True}
    return data
</macro>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**">
interface {{ interface | resuball(IfsNormalize) }}
 mtu {{ mtu }}
 vrf {{ vrf }}
 description {{ description | re(".+") }}
 ipv4 address {{ ip | PHRASE | joinmatches(",") }}
 ipv4 address {{ ip | PHRASE | joinmatches(",") }} secondary
 ipv6 address {{ ip | joinmatches(",") }}
 bundle id {{ lag_id | DIGIT }} mode {{ lag_mode }}
</group>

<!-- Interfaces state group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**.state">
{{ interface | _start_ | resuball(IfsNormalize) | macro("check_is_physical_port") }} is {{ admin | ORPHRASE }}, line protocol is {{ line | ORPHRASE }}
  Hardware is {{ hardware }} interface(s)
  Hardware is {{ hardware }} interface
  Hardware is {{ hardware | ORPHRASE }} interface(s), address is {{ mac }}
  Hardware is {{ hardware | ORPHRASE }}, address is {{ mac }} (bia {{ ignore }})
  Description: {{ description | re(".+") }}
  Internet address is {{ ip }}
  MTU {{ mtu }} bytes, BW {{ bw_kbits }} Kbit (Max: 1000000 Kbit)
  MTU {{ mtu }} bytes, BW {{ bw_kbits }} Kbit
  {{ duplex }}-duplex, {{ link_speed }}
  {{ duplex }}-duplex, {{ link_speed }}, link type is {{ link_type }}
  {{ duplex }}-duplex, {{ link_speed }}, {{ media_type }}, link type is {{ link_type }}
      {{ lag_members | joinmatches(" ") }}  {{ ignore }}-duplex  {{ ignore }} {{ ignore }}
</group>

<!-- LLDP peers group -->
<group name="{{ local_hostname }}.lldp_peers*" expand="">
Local Interface: {{ src_label | resuball(IfsNormalize) }}
Chassis id: {{ data.chassis_id }}
Port id: {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
Port Description: {{ data.peer_port_description | re(".+") }}
System Name: {{ target.id | split(".") | item(0) | split("(") | item(0) }}
System Capabilities: {{ data.peer_capabilities | ORPHRASE }}
  IPv4 address: {{ target.top_label }}
{{ source | set("local_hostname") }}
</group>


<!-- CDP peers group -->
<group name="{{ local_hostname }}.cdp_peers*" expand="">
Device ID: {{ target.id | split(".") | item(0) | split("(") | item(0) }}
  IPv4 address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }},  Capabilities: {{ data.peer_capabilities | ORPHRASE }}
Interface: {{ src_label | resuball(IfsNormalize) }}
Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
{{ source | set("local_hostname") }}
</group>
</template>
```
</details>