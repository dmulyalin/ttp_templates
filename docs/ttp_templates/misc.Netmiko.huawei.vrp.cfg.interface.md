Reference path:
```
ttp://misc/Netmiko/huawei.vrp.cfg.interface.txt
```

---



Template to parse "display current-configuration interface" output for Huawei devices.


Template to produce list of dictionaries with interface configuration details using 
Huawei "display current-configuration interface" command output.



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse "display current-configuration interface" output for Huawei devices.
</doc>

<input>
commands = ["display current-configuration interface"]
</input>

<extend template="ttp://platform/huawei_display_current_configuration_interface.txt"/>
```
</details>