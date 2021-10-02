Reference path:
```
ttp://platform.cisco_xr_show_arp_vrf_all.txt
```

---



TTP template to parse Cisco IOS XR "show arp vrf all" output. 



---

<details><summary>Template Content</summary>
```
<doc>
TTP template to parse Cisco IOS XR "show arp vrf all" output. 
</doc>

<group method="table" to_int="age">
{{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }}  {{ state | lower }}  {{ type }} {{ interface | resuball("short_interface_names") }}
</group>
```
</details>