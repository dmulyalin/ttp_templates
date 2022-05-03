Reference path:
```
ttp://misc/Netmiko/cisco.ios.cfg.interface.txt
```

---



Template to parse "show running-config | section interface" output for Cisco IOS.


Template to produce list of dictionaries with interface configuration details using 
Cisco IOSXE "show running-config | section interface" command output.

The exact command is "show running-config" and not "show running-configuration",
as it is changed in later versions of IOSXE.



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "show running-config | section interface" output for Cisco IOS.
</doc>

<input>
commands = ["show running-config | section interface"]
</input>

<extend template="ttp://platform/cisco_ios_show_running_config_pipe_section_interface.txt"/>
```
</details>