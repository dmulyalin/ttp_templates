Reference path:
```
ttp://platform/cisco_ios_show_isdn_status.txt
```

---



This Template allows to parse show isdn status on a cisco ios xe



---

<details><summary>Template Content</summary>
```
<doc>
This Template allows to parse show isdn status on a cisco ios xe
</doc>
Global ISDN Switchtype = basic-net3
<group name = "interface">
ISDN {{INTERFACE}} interface
        dsl 2, interface ISDN Switchtype = {{ISDN_SWITCHTYPE}}
    Layer 1 Status:
        {{L1_STATUS}}
    Layer 2 Status:
        TEI = {{TEI_CODE}}, Ces = {{CES}}, SAPI = {{SAPI}}, State = {{TEI_STATE}}
    Layer 3 Status:
        0 Active Layer 3 Call(s)
    Active dsl 2 CCBs = 0
    The Free Channel Mask:  {{FREE_CHANNEL_MASK}}
    Number of L2 Discards = {{L2_DISCARDS}}, L2 Session ID = {{L2_SESSION_ID}}
    Total Allocated ISDN CCBs = 1
</group>


```
</details>