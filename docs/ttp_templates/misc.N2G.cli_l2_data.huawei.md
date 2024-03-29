Reference path:
```
ttp://misc/N2G/cli_l2_data/huawei.txt
```

---



This template designed to parse Huawei configuration and LLDP neighbors.



---

<details><summary>Template Content</summary>
```
<template name="huawei" results="per_template">

<doc>
This template designed to parse Huawei configuration and LLDP neighbors.
</doc>

<input load="python">
commands = [
    "display lldp neighbor details",
    "display current-configuration interface",
    "display interface",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["huawei", "huawei_vrpv8"]
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
    undef_names = ["not advertised", "null", "--"]
    if data.get("target.id", "").lower() in undef_names:
        data["target.id"] = data["data.chassis_id"]
    return data
    
def lldp_choose_bottom_label(data):
    if "target.bottom_label_2" in data:
        data["target.bottom_label"] = data.pop("target.bottom_label_2")
    elif "target.bottom_label" in data:
        data["data.peer_system"] = str(data["target.bottom_label"])
        data["target.bottom_label"] = "{}..".format(data["target.bottom_label"][:18])
    return data
</macro>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**">
interface {{ interface | resuball(IfsNormalize) }}
 description {{ description | re(".+") }}
 port link-type {{ l2_mode }}
 dot1q termination vid {{ dot1q_vid }}
 port trunk allow-pass vlan {{ trunk_vlans | unrange("to", " ") | replace(' ', ',') | joinmatches(",") }}
 port trunk allow-pass vlan all {{ trunk_vlans | set("ALL") }}
 dfs-group 1 m-lag {{ mlag_id | DIGIT }}
 eth-trunk {{ lag_id | DIGIT }}
 mode {{ lag_mode }}
 port trunk pvid vlan {{ access_vlan }}
 ip address {{ ip | PHRASE | joinmatches(",") }}
 ip binding vpn-instance {{ vrf }}
 peer-link 1 {{ peer_link | set(True) }}
</group>

<!-- Interfaces state group
<group name="{{ local_hostname }}.interfaces**.{{ interface }}**.state">

</group>
 -->

<!-- node_facts VLANs group -->
<group name="{{ local_hostname }}.node_facts.vlans**" macro="process_vlans">
vlan {{ vid | exclude(",") }}
 name {{ name | ORPHRASE | default("no name") }}
</group>

<!-- LLDP peers group -->
<group name="{{ local_hostname }}.lldp_peers*" chain="macro('check_lldp_peer_name') | macro(lldp_choose_bottom_label) | expand()">
{{ src_label | resuball(IfsNormalize) }}  has 1 neighbor(s):
Port ID                            :{{ trgt_label | ORPHRASE | resuball(IfsNormalize) }}
Chassis ID                         :{{ data.chassis_id }}
System name                        :{{ target.id | split(".") | item(0) | split("(") | item(0) }}
HUAWEI {{ target.bottom_label_2 }}
System description                 :{{ target.bottom_label | ORPHRASE }}
Port description                   :{{ data.peer_port_description | re(".+") | notequal("--") }}
System capabilities supported      :{{ data.peer_capabilities | ORPHRASE | notequal("--") }}
Maximum frame Size                 :{{ data.peer_mtu | notequal("--") }}
Management address                 :{{ target.top_label }}
{{ source | set("local_hostname") }}
</group>
</template>
```
</details>