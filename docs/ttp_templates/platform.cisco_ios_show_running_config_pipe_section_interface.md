Reference path:
```
ttp://platform/cisco_ios_show_running_config_pipe_section_interface.txt
```

---



Template to produce list of dictionaries with interface configuration details using 
Cisco IOSXE "show running-config | section interface" command output.

The exact command is "show running-config" and not "show running-configuration",
as it is changed in later versions of IOSXE.



---

<details><summary>Template Content</summary>
```
<doc>
Template to produce list of dictionaries with interface configuration details using 
Cisco IOSXE "show running-config | section interface" command output.

The exact command is "show running-config" and not "show running-configuration",
as it is changed in later versions of IOSXE.
</doc>

<group>
interface {{ interface }}
 description {{ description | re(".*") }}
 ip address {{ ipv4 }} {{ mask_v4 }}
 ipv6 address {{ ipv6 }}/{{ mask_v6 }}
 shutdown {{ disabled | set(True) }}
 mtu {{ mtu }}
 encapsulation dot1Q {{ dot1q }}
 encapsulation dot1q {{ dot1q }}
 vrf forwarding {{ vrf }}
 ip vrf forwarding {{ vrf }}
 service-policy input {{ qos_policy_in }}
 service-policy output {{ qos_policy_out }}
 ip access-group {{ acl_in }} in
 ip access-group {{ acl_out }} out
! {{ _end_ }}
</group>
```
</details>