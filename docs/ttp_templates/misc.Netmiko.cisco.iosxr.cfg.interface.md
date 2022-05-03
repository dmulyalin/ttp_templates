Reference path:
```
ttp://misc/Netmiko/cisco.iosxr.cfg.interface.txt
```

---



Template to parse "show running-config interface" output for Cisco IOSXR.


Template to produce list of dictionaries with interface 
configuration details using Cisco IOS-XR "show run interface"
command output.



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "show running-config interface" output for Cisco IOSXR.
</doc>

<input>
commands = ["show running-config interface"]
</input>

<extend template="ttp://platform/cisco_xr_show_running_config_interface.txt"/>
```
</details>