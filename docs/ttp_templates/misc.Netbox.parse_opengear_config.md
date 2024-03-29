Reference path:
```
ttp://misc/Netbox/parse_opengear_config.txt
```

---



Template to parse Opengear configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of `config -g config` command.



---

<details><summary>Template Content</summary>
```
<template name="netbox_data" results="per_template">
<doc>
Template to parse Opengear configuration and produce data structure
that is easy to work with to import data into the Netbox.

This template requires output of 'config -g config' command.
</doc>

<input>
commands = [
    "config -g config"
]
</input>

<macro>
def process_interface(data):

    if not data.get("name"):
        return False
        
    data["description"] = ""
    
    if data["disabled"] == "on":
        data.pop("disabled")
        data["enabled"] = False
    else:
        data.pop("disabled")
        data["enabled"] = True
            
    if data["name"] == "wan":
        data["name"] = "eth0"
        data["label"] = "wan"
        data["interface_type"] = "bridge" 
    elif data["name"] == "lan":
        data["name"] = "eth1"
        data["label"] = "lan"
        data["interface_type"] = "bridge" 
    else:
        return False
        
    return data
    
def process_output(data):
    
    # transform interfaces dictionary into a list
    interfaces = []
    for intf_name, intf_data in data.get("interfaces", {}).items():
    
        # transform ipv4 addresses to list
        if intf_data.get("ipv4") and intf_data.get("maskv4"):
            intf_data["ipv4"] = [{"ip": intf_data.pop("ipv4"), "mask": intf_data.pop("maskv4")}]
        
        interfaces.append(intf_data)
        interfaces[-1]["name"] = intf_name
    data["interfaces"] = interfaces
    
    return data
</macro>

## ------------------------------------------------------------------------------------------
## Global Configuration facts
## ------------------------------------------------------------------------------------------
<group name="facts**" method="table">
config.name {{ hostname }}
config.system.name {{ hostname }}
</group>

## ------------------------------------------------------------------------------------------
## DNS Servers configuration
## ------------------------------------------------------------------------------------------
<group name="nameservers*" method="table">
config.interfaces.lan.dns1 {{ name_server }}
</group>

## ------------------------------------------------------------------------------------------
## Logging configuration
## ------------------------------------------------------------------------------------------
<group name="logging**.{{ server }}" method="table">
config.syslog.servers.{{ server }}.address {{ host }}
</group>

## ------------------------------------------------------------------------------------------
## Users configuration
## ------------------------------------------------------------------------------------------
<group name="users*">
config.users.user1.username {{ username | joinmatches }}
</group>

## ------------------------------------------------------------------------------------------
## AAA configuration
## ------------------------------------------------------------------------------------------
<group name="aaa**" method="table">
config.auth.tacacs.auth_server {{ tacacs_servers | split(",") }}
config.auth.type {{ authentication_login }}
</group>

## ------------------------------------------------------------------------------------------
## NTP configuration
## ------------------------------------------------------------------------------------------
<group name="ntp">
config.ntp.servers.server1.address {{ server | joinmatches }}
</group>

## ------------------------------------------------------------------------------------------
## Interfaces configuration
## ------------------------------------------------------------------------------------------
<group name="interfaces**.{{ name }}**" functions="macro('process_interface')" method="table">
config.interfaces.{{ name }}.address {{ ipv4 }}
config.interfaces.{{ name }}.netmask {{ maskv4 }}
config.interfaces.{{ name }}.failover.address1 {{ failover_ip }}
config.interfaces.{{ name }}.failover.interface {{ failover_interface }}
config.interfaces.{{ name }}.gateway {{ gateway }}
config.interfaces.{{ name }}.mtu {{ mtu | to_int }}
config.interfaces.{{ name }}.disabled {{ disabled | default("off") }}
</group>

## ------------------------------------------------------------------------------------------
## Console Server Ports Configuration
## ------------------------------------------------------------------------------------------
<group name="console_server_ports**.{{ name }}**" method="table">
config.ports.{{ name }}.charsize {{ charsize }}
config.ports.{{ name }}.flowcontrol {{ flowcontrol }}
config.ports.{{ name }}.label {{ description | re(".+") }}
config.ports.{{ name }}.parity {{ parity }}
config.ports.{{ name }}.pinout {{ pinout }}
config.ports.{{ name }}.speed {{ speed }}
config.ports.{{ name }}.stop {{ stop_bits }}
</group>

## ------------------------------------------------------------------------------------------
## DHCP configuration
## ------------------------------------------------------------------------------------------
<group name="dhcprelay**" method="table">
config.services.dhcprelay.enabled {{ dhcprelay_enabled }}
config.services.dhcprelay.lowers.lower1.circuit_id {{ circuit_id }}
config.services.dhcprelay.lowers.lower1.role {{ client_ports }}
config.services.dhcprelay.servers.server1 {{ dhcp_server }}
<group name="uplink_ports*">
config.services.dhcprelay.uppers.upper1.interface {{ port | joinmatches }}
</group>
</group>

<output macro="process_output"/>

</template>
```
</details>