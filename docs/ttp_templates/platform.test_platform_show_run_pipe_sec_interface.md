Reference path:
```
ttp://platform.test_platform_show_run_pipe_sec_interface.txt
```

---



Template to help with testing ttp_templates api



---

<details><summary>Template Content</summary>
```
<doc>
Template to help with testing ttp_templates api
</doc>

<group>
interface {{ interface }}
 description {{ description | re(".+") }}
 encapsulation dot1q {{ dot1q }}
 ip address {{ ip }} {{ mask }}
 shutdown {{ disabled | set(True) }}
</group>
```
</details>