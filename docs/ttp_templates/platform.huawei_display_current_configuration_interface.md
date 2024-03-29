Reference path:
```
ttp://platform/huawei_display_current_configuration_interface.txt
```

---



Template to produce list of dictionaries with interface configuration details using 
Huawei "display current-configuration interface" command output.



---

<details><summary>Template Content</summary>
```
<doc>
Template to produce list of dictionaries with interface configuration details using 
Huawei "display current-configuration interface" command output.
</doc>

<group>
interface {{ interface }}
 vlan-type dot1q {{ dot1q }}
 dot1q termination vid {{ dot1q }}
 mtu {{ mtu }}
 description {{ description | re(".*") }}
 ip binding vpn-instance {{ vrf }}
 ip address {{ ipv4 }} {{ mask_v4 }}
 ipv6 address {{ ipv6 }}/{{ mask_v6 }}
 shutdown {{ disabled | set(True) }}
 qos-profile {{ qos_policy_in }} inbound {{ ignore("PHRASE") }}
 qos-profile {{ qos_policy_out }} outbound {{ ignore("PHRASE") }}
# {{ _end_ }}
</group>
```
</details>