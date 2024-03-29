Reference path:
```
ttp://misc/N2G/cli_l2_data/cisco_ios.txt
```

---



This template designed to parse Cisco IOS configuration and CDP and LLDP neighbors.



---

<details><summary>Template Content</summary>
```
<template name="cisco_ios" results="per_template">

<doc>
This template designed to parse Cisco IOS configuration and CDP and LLDP neighbors.
</doc>

<input load="python">
commands = [
    "show cdp neighbor details",
    "show lldp neighbor details",
    "show running-config",
    "show interface",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["cisco_ios"]
</input>

<vars>local_hostname="gethostname"</vars>

<macro>
def process_vlans(data):
    return {data["vid"]: data["name"]}
    
def check_is_physical_port(data):
    for item in _ttp_["vars"]["physical_ports"]:
        if data.startswith(item) and not "." in item:
            return data, {"is_physical_port": True}
    return data
</macro>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**">
interface {{ interface | resuball(IfsNormalize) }}
 description {{ description | re(".+") }}
 switchport {{ is_l2 | set(True) }}
 switchport access vlan {{ access_vlan }}
 switchport mode {{ l2_mode }}
 vrf forwarding {{ vrf }}
 ip address {{ ip | PHRASE | joinmatches(",") }}
 ip address {{ ip | PHRASE | joinmatches(",") }} secondary
 switchport trunk allowed vlan {{ trunk_vlans | unrange("-", ",") | joinmatches(",") }}
 channel-group {{ lag_id | DIGIT }} mode {{ lag_mode }}
 mtu {{ mtu }}
</group>

<!-- Interfaces state group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**.state">
{{ interface | _start_ | resuball(IfsNormalize) | macro("check_is_physical_port") }} is {{ admin | ORPHRASE }}, line protocol is {{ line }}
{{ interface | _start_ | resuball(IfsNormalize) | macro("check_is_physical_port") }} is {{ admin | ORPHRASE }}, line protocol is {{ line }} ({{ line_status }})
  Description: {{ description | re(".+") }} 
  Hardware is {{ hardware | ORPHRASE }}, address is {{ mac }} (bia {{ ignore }})
  MTU {{ mtu }} bytes, BW {{ bw_kbits }} Kbit/sec, DLY 1000 usec, 
  {{ duplex }}-duplex, {{ link_type }}, media type is {{ media_type }}
  {{ duplex }}-duplex, {{ link_speed }}-speed, link type is {{ link_type }}, media type is {{ media_type | ORPHRASE }}
  {{ duplex }}-duplex, {{ link_speed }}, link type is {{ link_type }}, media type is {{ media_type | ORPHRASE }}
  Members in this channel: {{ lag_members | ORPHRASE }}
</group>

<!-- node_facts VLANs group -->
<group name="{{ local_hostname }}.node_facts.vlans**" macro="process_vlans">
vlan {{ vid }}
 name {{ name | ORPHRASE | default("no name") }}
</group>

<!-- LLDP peers group -->
<group name="{{ local_hostname }}.lldp_peers*" expand="">
Local Intf: {{ src_label | resuball(IfsNormalize) }}
Port id: {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
System Name: {{ target.id | split(".") | item(0) | split("(") | item(0) }}
System Capabilities: {{ ignore(ORPHRASE) }}
    IP: {{ target.top_label }}
{{ source | set("local_hostname") }}
</group>

<!-- CDP peers group -->
<group name="{{ local_hostname }}.cdp_peers*" expand="">
Device ID: {{ target.id | split(".") | item(0) | split("(") | item(0) }}
  IP address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }},  Capabilities: {{ ignore(ORPHRASE) }}
Interface: {{ src_label | resuball(IfsNormalize) }},  Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
{{ source | set("local_hostname") }}
</group>
</template>
```
</details>