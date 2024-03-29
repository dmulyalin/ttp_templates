Reference path:
```
ttp://platform/cisco_ios_show_ip_arp.txt
```

---



TTP Template to parse Cisco IOS "show ip arp output".

This template produces list of dictionaries results where each
dictionary item compatible to this model:
```
module arp-table {

yang-version 1.1;

namespace
  "ttp://platform/cisco_ios_show_ip_arp";
  
list entry {
        config false;
        key "ip";
        
        leaf protocol {
            type string;
        }
        
        leaf ip {
            type string;
            mandatory true;
            description
                "IP address";
        }

        leaf age {
            type uint32;
            description
                "IP address";
        }

        leaf mac {
            type string;
            mandatory "true";
            description
                "MAC address";
        }    

        leaf type {
            type string;
        }

        leaf interface {
            type string;
            default "Uncknown";
			mandatory false;
            description
                "Interface name";
        }        
    }
}
```

Sample instance data:
```
TBD
```



---

<details><summary>Template Content</summary>
```
<doc>
TTP Template to parse Cisco IOS "show ip arp output".

This template produces list of dictionaries results where each
dictionary item compatible to this model:
'''
module arp-table {

yang-version 1.1;

namespace
  "ttp://platform/cisco_ios_show_ip_arp";
  
list entry {
        config false;
        key "ip";
        
        leaf protocol {
            type string;
        }
        
        leaf ip {
            type string;
            mandatory true;
            description
                "IP address";
        }

        leaf age {
            type uint32;
            description
                "IP address";
        }

        leaf mac {
            type string;
            mandatory "true";
            description
                "MAC address";
        }    

        leaf type {
            type string;
        }

        leaf interface {
            type string;
            default "Uncknown";
			mandatory false;
            description
                "Interface name";
        }        
    }
}
'''

Sample instance data:
'''
TBD
'''
</doc>

<group method="table" to_int="age">
{{ protocol }} {{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }} {{ type | let("interface", "Uncknown") }}    
{{ protocol }} {{ ip | IP }} {{ age | replace("-", "-1") }} {{ mac | mac_eui }} {{ type }} {{ interface | resuball("short_interface_names") }}
</group>
```
</details>