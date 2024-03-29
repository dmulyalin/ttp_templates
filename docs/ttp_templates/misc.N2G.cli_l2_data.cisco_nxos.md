Reference path:
```
ttp://misc/N2G/cli_l2_data/cisco_nxos.txt
```

---



This template designed to parse Cisco NXOS configuration and CDP and LLDP neighbors.



---

<details><summary>Template Content</summary>
```
<template name="cisco_nxos" results="per_template">

<doc>
This template designed to parse Cisco NXOS configuration and CDP and LLDP neighbors.
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
platform = ["nxos_ssh", "cisco_nxos"]
</input>

<vars>local_hostname="gethostname"</vars>

<macro>
def process_vlans(data):
    return {data["vid"]: data["name"]}
    
def check_is_physical_port(data):
    for item in _ttp_["vars"]["physical_ports"]:
        if data.startswith(item) and not "." in data:
            return data, {"is_physical_port": True}
    return data
</macro>

<macro>
def check_lldp_peer_name(data):
    undef_names = ["not advertised", "null"]
    if data.get("target.id", "").lower() in undef_names:
        data["target.id"] = data["data.chassis_id"]
    return data
</macro>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**">
interface {{ interface | resuball(IfsNormalize) }}
  description {{ description | re(".+") }}
  switchport {{ is_l2 | set(True) }}
  switchport access vlan {{ access_vlan }}
  switchport mode {{ l2_mode }}
  switchport trunk allowed vlan {{ trunk_vlans | unrange("-", ",") | joinmatches(",") }}
  switchport trunk allowed vlan add {{ trunk_vlans | unrange("-", ",") | joinmatches(",") }}
  channel-group {{ lag_id | DIGIT }} mode {{ lag_mode }}
  vpc {{ mlag_id | DIGIT }}
  mtu {{ mtu }}
  vrf member {{ vrf }}
  ip address {{ ip | joinmatches(",") }} 
  ip address {{ ip | joinmatches(",") }} secondary 
</group>

<group name="{{ local_hostname }}.interfaces**.{{ interface }}**.state">
{{ interface | _start_ | resuball(IfsNormalize) | macro("check_is_physical_port") }} is {{ admin | ORPHRASE }}, line protocol is {{ line }}, autostate enabled
{{ interface | _start_ | resuball(IfsNormalize) | macro("check_is_physical_port") }} is {{ line | ORPHRASE }}
admin state is {{ admin | ORPHRASE }},{{ ignore(".*") }}
admin state is {{ admin }}
  Belongs to {{ parent_lag }}
  Description: {{ description | re(".+") }} 
  Hardware: {{ hardware | ORPHRASE }}, address: {{ mac }} (bia {{ bia }})
  Hardware is {{ hardware }}, address is  {{ mac }}
  MTU {{ mtu }} bytes, BW {{ bw_kbits }} Kbit, DLY 10 usec
  Port mode is {{ mode }}
  {{ duplex }}-duplex, {{ link_speed | PHRASE }}, media type is {{ media_type }}
  {{ duplex }}-duplex, {{ link_speed | PHRASE | exclude(",media") }}
  Members in this channel: {{ lag_members | ORPHRASE }}
</group>

<!-- node_facts VLANs group -->
<group name="{{ local_hostname }}.node_facts.vlans**" macro="process_vlans">
vlan {{ vid | exclude(",") }}
  name {{ name | ORPHRASE | default("no name") }}
</group>

<!-- LLDP peers group -->
<group name="{{ local_hostname }}.lldp_peers*" chain="macro('check_lldp_peer_name') | expand()">
Chassis id: {{ data.chassis_id }}
Port id: {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
Local Port id: {{ src_label | resuball(IfsNormalize) }}
Port Description: {{ data.peer_port_description | re(".+") }}
System Name: {{ target.id | ORPHRASE | split(".") | item(0) | split("(") | item(0) }}
System Description: {{ data.peer_system | ORPHRASE}}
System Capabilities: {{ data.peer_capabilities | ORPHRASE }}
Management Address: {{ target.top_label }}
{{ source | set("local_hostname") }}
</group>

<!-- CDP peers group -->
<group name="{{ local_hostname }}.cdp_peers*" expand="">
Device ID:{{ target.id | split(".") | item(0) | split("(") | item(0) }}
    IPv4 Address: {{ target.top_label }}
Platform: {{ target.bottom_label | ORPHRASE }}, Capabilities: {{ data.peer_capabilities | ORPHRASE }}
Interface: {{ src_label | resuball(IfsNormalize) }}, Port ID (outgoing port): {{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
MTU: {{ data.peer_mtu }}
Physical Location: {{ data.peer_location | ORPHRASE }}
{{ source | set("local_hostname") }}
</group>
</template>
```
</details>