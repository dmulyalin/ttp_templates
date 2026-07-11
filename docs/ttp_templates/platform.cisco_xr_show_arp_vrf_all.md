Reference path:
```
ttp://platform/cisco_xr_show_arp_vrf_all.txt
```

---



TTP template to parse Cisco IOS XR "show arp vrf all" output. 



---

<details><summary>Template Content</summary>
```
<doc>
TTP template to parse Cisco IOS XR "show arp vrf all" output. 
</doc>

<macro>
def validate_arp_records(data):
    from ttp_templates.utils.models import ArpRecord

    def validate_item(item):
        if isinstance(item, dict):
            return ArpRecord(**item).model_dump(exclude_unset=True)
        if isinstance(item, list):
            return [validate_item(child) for child in item]
        return item

    return validate_item(data)
</macro>

<group method="table" to_int="age">
{{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }}  {{ state | lower }}  {{ type }} {{ interface | resuball("short_interface_names") }}
</group>

<output macro="validate_arp_records"/>

```
</details>