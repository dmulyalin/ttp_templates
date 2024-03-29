Reference path:
```
ttp://misc/Netbox/parse_cisco_nxos_config.txt
```

---



Template to parse Cisco NXOS configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'show running-config' command.



---

<details><summary>Template Content</summary>
```
<template name="netbox_data" results="per_template">
<doc>
Template to parse Cisco NXOS configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'show running-config' command.
</doc>

<input>
commands = [
    "show running-config"
]
</input>

<macro>
def add_interface_type(data):
    data["interface_type"] = "other"    
    if any(
        i in data["name"].lower() for i in [
            ".", "loopback", "tunnel", "vlan", "nve"
        ]
    ):
        data["interface_type"] = "virtual"
    elif any(
        i in data["name"].lower() for i in [
            "vlan", "nve"
        ]
    ):
        data["interface_type"] = "bridge"
    elif "port-channel" in data["name"].lower():
        data["interface_type"] = "lag"
    return data

def add_parent_interface(data):
    if "lag_id" in data:
        data["parent"] = "Port-Channel{}".format(data["lag_id"])
    elif "." in data["name"]:
        data["parent"] = data["name"].split(".")[0]
    return data
</macro>

## ------------------------------------------------------------------------------------------
## Global Configuration facts
## ------------------------------------------------------------------------------------------
<group name="facts**" method="table">
hostname {{ hostname }}
feature {{ feature | ORPHRASE | split | joinmatches }}
ip domain-name {{ domain_name }}
boot nxos {{ boot_system }}
</group>

## ------------------------------------------------------------------------------------------
## SNMP Configuration
## ------------------------------------------------------------------------------------------
<group name="snmp**" method="table">

</group>

## ------------------------------------------------------------------------------------------
## DNS Servers configuration
## ------------------------------------------------------------------------------------------
<group name="nameservers**.{{ vrf }}" method="table">
ip name-server {{ name_server | ORPHRASE | split(" ") }} use-vrf {{ vrf }}
</group>

## ------------------------------------------------------------------------------------------
## Logging configuration
## ------------------------------------------------------------------------------------------
<group name="logging**" method="table">
logging server {{ host }} 5 use-vrf {{ vrf }} facility syslog
</group>

## ------------------------------------------------------------------------------------------
## Users configuration
## ------------------------------------------------------------------------------------------
<group name="users*">
username {{ username }} password 5 {{ ignore }}  role {{ role }}
</group>

## ------------------------------------------------------------------------------------------
## AAA configuration
## ------------------------------------------------------------------------------------------
<group name="tacacs.servers*">
tacacs-server host {{ server }} key 7 {{ ignore }} timeout 30 
</group>

<group name="tacacs.groups*">
aaa group server tacacs+ {{ name }} 
    <group name="servers*">
    server {{ server | split | joinmatches }}
    use-vrf {{ vrf }}
    source-interface {{ source_interface }}
   </group>
{{ _end_ }}
</group>

<group name="aaa**" method="table">
aaa authentication login default group {{ authentication_login | ORPHRASE }} 
aaa authorization commands default group {{ authorization_exec | ORPHRASE }} 
</group>

## ------------------------------------------------------------------------------------------
## VLANs configuration
## ------------------------------------------------------------------------------------------
<group name="vlans*">
vlan {{ vlan }}
  name {{ name | ORPHRASE }}
  vn-segment {{ vni }}
{{ _end_ }}
</group>   

## ------------------------------------------------------------------------------------------
## VRFs configuration
## ------------------------------------------------------------------------------------------
<group name="vrf*">
vrf context {{ name }}
  description {{ description | re(".+") | default("") }}
  rd {{ rd }}
{{ _end_ }}
</group>

## ------------------------------------------------------------------------------------------
## NTP configuration
## ------------------------------------------------------------------------------------------
<group name="ntp" method="table">
ntp server {{ server }} use-vrf {{ vrf }}
</group>

## ------------------------------------------------------------------------------------------
## Interfaces configuration
## ------------------------------------------------------------------------------------------
<group name="interfaces*" functions="contains('name') | macro('add_interface_type') | macro('add_parent_interface')">
interface {{ name | _start_ }}
  description {{ description | re(".*") | default("") }}
  no shutdown {{ enabled | set(True) | default(False) }}
  shutdown {{ enabled | set(False) }}
  mtu {{ mtu | to_int }}
  vrf member {{ vrf }}
  no switchport {{ is_l3_interface | set(True) }}
  switchport mode trunk {{ mode | set("tagged") }}
  switchport access vlan {{ access_vlan | let("mode", "access") }}
  spanning-tree port type edge trunk {{ stp_portfast_enabled | set(True) }}
  switchport trunk allowed vlan {{ trunk_vlans | unrange(rangechar='-', joinchar=',') | split(",") | joinmatches }}
  switchport trunk allowed vlan add {{ trunk_vlans | unrange(rangechar='-', joinchar=',') | split(",") | joinmatches }}
  channel-group {{ lag_id }} mode {{ lacp_mode }}
  
  <group name="ipv4*" method="table">
  ip address {{ ip | IP }}/{{ mask }}
  ip address {{ ip | IP | let("secondary", True) }}/{{ mask}} secondary
  </group>

  <group name="ipv6*" method="table">
  ipv6 address {{ ip | IP }}/{{ mask }}
  </group>
  
{{ _end_ }}
</group>

## ------------------------------------------------------------------------------------------
## SSH configuration
## ------------------------------------------------------------------------------------------
<group name="ssh_server**" method="table">
    
</group>

## ------------------------------------------------------------------------------------------
## BGP configuration
## ------------------------------------------------------------------------------------------
<group name="bgp">
router bgp {{ asn }}

  <group name="afi.{{ afi }}">
  address-family {{ afi }} {{ safi }}
  </group>
  
  <group name="neighbors**.{{ neighbor_ip }}**" method="table">
  template peer {{ neighbor_ip | let("is_peer_group", True) }}
  neighbor {{ neighbor_ip | let("is_peer_group", False) }}
    remote-as {{ neighbor_asn }}
    inherit peer {{ peer_group }}  
    description {{ description | re(".+") }}
  </group>



  <group name="vrf**.{{ vrf }}">
  vrf {{ vrf }}

    <group name="afi.{{ afi }}">  
    address-family {{ afi }} {{ safi }}
    </group>

    <group name="neighbors**.{{ neighbor_ip }}**" method="table">   
    neighbor {{ neighbor_ip | let("is_peer_group", False) }}
    
      inherit peer {{ peer_group }}  
      remote-as {{ neighbor_asn }}
      description {{ description | re(".+") }}
      
      <group name="afi.{{ afi }}">  
      address-family {{ afi }} {{ safi }}
        route-map {{ rpl_in }} in
        route-map {{ rpl_out }} out
      </group>
        
    </group>
  </group>
</group>      

## ------------------------------------------------------------------------------------------
## Multicast configuration
## ------------------------------------------------------------------------------------------
<group name="multicast">

</group>

<group name="pim_bidir">

</group>

## ------------------------------------------------------------------------------------------
## MC-LAG configuration
## ------------------------------------------------------------------------------------------
<group name="mlag">

</group>
</template>
```
</details>