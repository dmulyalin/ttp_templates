Reference path:
```
ttp://misc/N2G/cli_ip_data/fortinet.txt
```

---



Template to parse Fortinet fortigate firewalls interfaces configuration and ARP cache.



---

<details><summary>Template Content</summary>
```
<template name="fortinet" results="per_template">

<doc>
Template to parse Fortinet fortigate firewalls interfaces configuration and ARP cache.
</doc>

<input load="python">
commands = [
    "get system config",
    "get system arp",
]
kwargs = {"strip_prompt": False}
method = "send_command"
platform = ["fortinet"]
</input>

<vars>local_hostname="gethostname"</vars>

<!-- Interfaces configuration group -->
<group name="{{ local_hostname }}.interfaces**">
config system interface {{ _start_ }}
    <group name="{{ interface }}">
    edit "{{ interface }}"
        set description "{{ port_description | re(".+") }}"
        set vdom "{{ vrf }}"
        set allowaccess {{ ACL_IN | ORPHRASE }}
        set interface "{{ parent_interface }}"
        set vlanid {{ vid }}
        <group name="ip_addresses*" chain="add_network()" method="table">
        set ip {{ ip | IP }} {{ netmask }}
                set ip {{ ip | IP }} {{ netmask }}
        </group>
    next{{ _end_ }}
    </group>    
end{{ _end_ }}
</group>    

<!-- ARP cache group -->
<group name="{{ local_hostname }}.interfaces.{{ interface }}.arp*" method="table">
{{ ip | IP }}      {{ age }}   {{ mac | MAC | mac_eui }}    {{ interface }}
</group>

</template>
```
</details>