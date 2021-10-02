Reference path:
```
ttp://platform.cisco_ios_show_ip_arp.txt
```

---



TTP Template to parse Cisco IOS "show ip arp output".



---

<details><summary>Template Content</summary>
```
<doc>
TTP Template to parse Cisco IOS "show ip arp output".
</doc>

<group method="table" to_int="age">
{{ protocol }} {{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }} {{ type | let("interface", "Uncknown") }}    
{{ protocol }} {{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }} {{ type }} {{ interface | resuball("short_interface_names") }}
</group>
```
</details>