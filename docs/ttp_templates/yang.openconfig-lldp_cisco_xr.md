Reference path:
```
ttp://yang/openconfig-lldp_cisco_xr.txt
```

---



Required devices' commands output:

 - show lldp neighbors detail
 
Device output should contain device prompt, otherwise device hostname will not be extracted.

Returns result compatible with this subset of `openconfig-lldp`
YANG model:
```
module: openconfig-lldp
  +--rw lldp
     +--rw config
     |  +--rw system-name?                  string
     +--rw interfaces
        +--rw interface* [name]
           +--rw name         
           +--ro neighbors
              +--ro neighbor* [id]
                 +--ro id              
                 +--ro state
                 |  +--ro system-name?               string
                 |  +--ro system-description?        string
                 |  +--ro chassis-id?                string
                 |  +--ro chassis-id-type?           oc-lldp-types:chassis-id-type
                 |  +--ro id?                        string
                 |  +--ro port-id?                   string
                 |  +--ro port-id-type?              oc-lldp-types:port-id-type
                 |  +--ro port-description?          string
                 |  +--ro management-address?        string
                 +--ro capabilities
                    +--ro capability* [name]
                       +--ro name        
```					   



---

<details><summary>Template Content</summary>
```
<doc>
Required devices' commands output:

 - show lldp neighbors detail
 
Device output should contain device prompt, otherwise device hostname will not be extracted.

Returns result compatible with this subset of 'openconfig-lldp'
YANG model:
'''
module: openconfig-lldp
  +--rw lldp
     +--rw config
     |  +--rw system-name?                  string
     +--rw interfaces
        +--rw interface* [name]
           +--rw name         
           +--ro neighbors
              +--ro neighbor* [id]
                 +--ro id              
                 +--ro state
                 |  +--ro system-name?               string
                 |  +--ro system-description?        string
                 |  +--ro chassis-id?                string
                 |  +--ro chassis-id-type?           oc-lldp-types:chassis-id-type
                 |  +--ro id?                        string
                 |  +--ro port-id?                   string
                 |  +--ro port-id-type?              oc-lldp-types:port-id-type
                 |  +--ro port-description?          string
                 |  +--ro management-address?        string
                 +--ro capabilities
                    +--ro capability* [name]
                       +--ro name        
'''					   
</doc>



<macro>
def process(data):
    """
    Function to process parsing results in a structure
    compatible with openconfig-lldp YANG module.
    
    Parsing results are a dictionary keyed by interface name, that 
    is done to combine multiple neighbors in a list under the 
    interface, while in opencofnig-lldp model structure under 
    "lldp.interfaces.inderface" must be a list.
    
    Moreover, neighbors must contain "id" key and use "state" key to
    store information about neighbor details.
    """
    ret = []

    for res_item in data:
        # transform dictionary of interfaces into a list
        ret_template = {
                "opencondig-lldp": {
                    "lldp": {
                        "interfaces": {"interface": []},
                        "config": {
                            "system-name": res_item.get("system_name", {}).get("hostname")
                        }
                    }
                }
        }
        interfaces = res_item.get("lldp", {}).get("interfaces", {}).get("inderface", {})
        for interface_name, interface_data in interfaces.items():
    
            # set neighbors IDs and form structure with "state" key
            neighbors = interface_data["neighbors"]["neighbor"]
            interface_data["neighbors"]["neighbor"] = []
            for id, neigbour in enumerate(neighbors, 1):
                interface_data["neighbors"]["neighbor"].append(
                    {
                        "id": id,
                        "state": {"id": id, **neigbour}
                    }            
                )
    
            # form final interface structure
            ret_template["opencondig-lldp"]["lldp"]["interfaces"]["interface"].append(
                {
                    "name": interface_name,
                    **interface_data
                }
            )
        ret.append(ret_template)
            
    return ret
    
def map_capabilities(data):
    """
    Function to map capabilities
    """
    ret = []
    
    mapper = {
        "B": {"name": "MAC_BRIDGE"},
        "R": {"name": "ROUTER"}
    }
    
    for code in data.get("codes", []):
        if code in mapper:
            ret.append(mapper[code])
    
    return {"capability": ret}
</macro>

<vars>
ifmap = {
    'ATM': ['^ATM', '^AT'],
    'BDI': ['^Bd', '^Bdi'],
    'EOBC': ['^EOBC', '^EO'],
    'Eth': ['^Ethernet', '^Eth', '^eth', r'^Et(?=\d)', r'^et(?=\d)'],
    'FE': ['^FastEthernet', '^FastEth', '^FastE', '^Fast', '^Fas', '^FE', '^Fa', '^fa'],
    'Fddi': ['^Fddi', '^FD'],
    '50GE': ['^FiftyGigabitEthernet', '^FiftyGigEthernet', '^FiftyGigEth', '^FiftyGigE', '^FI', '^Fi', '^fi'],
    '40GE': ['^FortyGigabitEthernet', '^FortyGigEthernet', '^FortyGigEth', '^FortyGigE', '^FortyGig', '^FGE', '^FO', '^Fo'],
    '400GE': ['^FourHundredGigabitEthernet', '^FourHundredGigEthernet', '^FourHundredGigEth', '^FourHundredGigE', '^FourHundredGig', '^F', '^f'],
    'GE': ['^GigabitEthernet', '^GigEthernet', '^GigEth', '^GigE', '^Gig', '^GE', '^Ge', '^ge', '^Gi', '^gi'],
    '100GE': ['^HundredGigabitEthernet', '^HundredGigEthernet', '^HundredGigEth', '^HundredGigE', '^HundredGig', '^Hu'],
    'Lo': ['^Loopback', '^loopback', '^Lo', '^lo'],
    'MFR': ['^MFR'], 
    'Ma': ['^Management_short'],
    'MGMT': ['^Management', '^Mgmt', '^mgmt', '^Ma'],
    'Multilink': ['^Multilink', '^Mu'],
    'POS': ['^POS', '^PO'],
    'LAG': ['^PortChannel', '^Port-channel', '^Port-Channel', '^port-channel', '^po', '^Po', "^Bundle-Ether", "^BE"],
    'Serial': ['^Serial', '^Se', '^S'],
    '10GE': ['^TenGigabitEthernet', '^TenGigEthernet', '^TenGigEth', '^TenGigE', '^TenGig', '^TeGig', '^Ten', '^Te', '^te'],
    'Tunnel': ['^Tunnel', '^Tun', '^Tu'],
    '25GE': ['^TwentyFiveGigabitEthernet', '^TwentyFiveGigEthernet', '^TwentyFiveGigEth', '^TwentyFiveGigE', '^TwentyFiveGig', '^Twe', '^TF', '^Tf', '^tf'],
    '2GE': ['^Tw', '^Two'],
    '200GE': ['^TwoHundredGigabitEthernet', '^TwoHundredGigEthernet', '^TwoHundredGigEth', '^TwoHundredGigE', '^TwoHundredGig', '^TH', '^Th', '^th'],
    'VLAN': ['^VLAN', '^V', '^Vl'],
    'Virtual-Access': ['^Virtual-Access', '^Vi'],
    'Virtual-Template': ['^Virtual-Template', '^Vt'],
    'WLAN': ['^Wlan-GigabitEthernet'],
    'nve': ['^n', '^nv', '^nve']
}
</vars>

<vars name="system_name">
hostname="gethostname"
</vars>

<group name="lldp.interfaces.inderface**.{{ name }}**">
##
##  Parses "show lldp neighbors detail" output
##
Local Interface: {{ name | resuball(ifmap) }}

<group name="neighbors.neighbor*">
Chassis id: {{ chassis-id | mac_eui }}
Port id: {{ port-id | resuball(ifmap) }}
Port Description: {{ port-description | re(".+") | default(None) }}
System Name: {{ system-name }}
  IPv4 address: {{ management-address | default(None) }}
  
<group name="_">
System Description: {{ _start_ }}
{{ system-description | _line_ | strip | joinmatches(" ") }}
Time remaining: {{ ignore }} seconds {{ _end_ }}
</group>

<group name="capabilities" macro="map_capabilities">
System Capabilities: {{ codes | split(",") }}
</group>

{{ port-id-type | set("INTERFACE_NAME") }}
{{ chassis-id-type | set("MAC_ADDRESS") }}
</group>
</group>

<output macro="process"/>
```
</details>