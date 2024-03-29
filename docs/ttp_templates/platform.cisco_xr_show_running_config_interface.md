Reference path:
```
ttp://platform/cisco_xr_show_running_config_interface.txt
```

---



Template to produce list of dictionaries with interface 
configuration details using Cisco IOS-XR "show run interface"
command output.



---

<details><summary>Template Content</summary>
```
<doc>
Template to produce list of dictionaries with interface 
configuration details using Cisco IOS-XR "show run interface"
command output.
</doc>

<group>
interface {{ interface | _start_ }}
interface {{ interface | _start_ }} l2transport
 description {{ description | re(".*") }}
 mtu {{ mtu }}
 service-policy input {{ qos_policy_in }}
 service-policy output {{ qos_policy_out }}
 ipv4 address {{ ipv4 }} {{ mask_v4 }}
 ipv6 address {{ ipv6 }}/{{ mask_v6 }}
 encapsulation dot1q {{ dot1q }}
 vrf {{ vrf }}
 bundle id {{ lag_id }} mode {{ ignore }}
 shutdown {{ disabled | set(True) }}
! {{ _end_ }}
</group>
```
</details>