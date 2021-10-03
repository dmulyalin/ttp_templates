Reference path:
```
ttp://misc.ttp_templates_tests.netmiko_cisco_ios_interfaces.txt
```

---



This template used in to test Netmiko `run_ttp` method



---

<details><summary>Template Content</summary>
```
<template name="interfaces" results="per_template">

<doc>
This template used in to test Netmiko `run_ttp` method
</doc>


<input>
commands = [
    "show run | sec interface"
]
</input>

<group name="intf_cfg">
interface {{ interface }}
 description {{ description | ORPHRASE }}
 ip address {{ ip }} {{ mask }}
</group>
</template>
```
</details>