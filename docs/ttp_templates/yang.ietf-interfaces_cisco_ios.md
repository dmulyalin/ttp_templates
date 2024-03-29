Reference path:
```
ttp://yang/ietf-interfaces_cisco_ios.txt
```

---



This templates produces structured data compatible with ietf-interfaces YANG module
out of Cisco IOS `show run` configuration output.

YANG ietf-interfaces module tree:
```
+--rw ietf-interfaces:interfaces
|  +--rw interface* [name]
|     +--ro admin-status {enumeration}
|     +--rw description? {string}
|     +--rw enabled? {boolean}
|     +--ro higher-layer-if* {interface-ref(leafref)}
|     +--ro if-index {int32}
|     +--rw ietf-ip:ipv4!
|     |  +--rw address* [ip]
|     |  |  +--rw ip {ipv4-address-no-zone(string)}
|     |  |  +--ro origin? {ip-address-origin(enumeration)}
|     |  |  +--rw (subnet)
|     |  |     +--:(netmask)
|     |  |     |  +--rw netmask? {dotted-quad(string)}
|     |  |     +--:(prefix-length)
|     |  |        +--rw prefix-length? {uint8}
|     |  +--rw enabled? {boolean}
|     |  +--rw forwarding? {boolean}
|     |  +--rw mtu? {uint16}
|     |  +--rw neighbor* [ip]
|     |     +--rw ip {ipv4-address-no-zone(string)}
|     |     +--rw link-layer-address {phys-address(string)}
|     |     +--ro origin? {neighbor-origin(enumeration)}
|     +--rw ietf-ip:ipv6!
|     |  +--rw address* [ip]
|     |  |  +--rw ip {ipv6-address-no-zone(string)}
|     |  |  +--ro origin? {ip-address-origin(enumeration)}
|     |  |  +--rw prefix-length {uint8}
|     |  |  +--ro status? {enumeration}
|     |  +--rw autoconf
|     |  |  +--rw create-global-addresses? {boolean}
|     |  |  +--rw create-temporary-addresses? {boolean}
|     |  |  +--rw temporary-preferred-lifetime? {uint32}
|     |  |  +--rw temporary-valid-lifetime? {uint32}
|     |  +--rw dup-addr-detect-transmits? {uint32}
|     |  +--rw enabled? {boolean}
|     |  +--rw forwarding? {boolean}
|     |  +--rw mtu? {uint32}
|     |  +--rw neighbor* [ip]
|     |     +--rw ip {ipv6-address-no-zone(string)}
|     |     +--ro is-router? {empty}
|     |     +--rw link-layer-address {phys-address(string)}
|     |     +--ro origin? {neighbor-origin(enumeration)}
|     |     +--ro state? {enumeration}
|     +--ro last-change? {date-and-time(string)}
|     +--rw link-up-down-trap-enable? {enumeration}
|     +--ro lower-layer-if* {interface-ref(leafref)}
|     +--rw name {string}
|     +--ro oper-status {enumeration}
|     +--ro phys-address? {phys-address(string)}
|     +--ro speed? {gauge64(uint64)}
|     +--ro statistics
|     |  +--ro discontinuity-time {date-and-time(string)}
|     |  +--ro in-broadcast-pkts? {counter64(uint64)}
|     |  +--ro in-discards? {counter32(uint32)}
|     |  +--ro in-errors? {counter32(uint32)}
|     |  +--ro in-multicast-pkts? {counter64(uint64)}
|     |  +--ro in-octets? {counter64(uint64)}
|     |  +--ro in-unicast-pkts? {counter64(uint64)}
|     |  +--ro in-unknown-protos? {counter32(uint32)}
|     |  +--ro out-broadcast-pkts? {counter64(uint64)}
|     |  +--ro out-discards? {counter32(uint32)}
|     |  +--ro out-errors? {counter32(uint32)}
|     |  +--ro out-multicast-pkts? {counter64(uint64)}
|     |  +--ro out-octets? {counter64(uint64)}
|     |  +--ro out-unicast-pkts? {counter64(uint64)}
|     +--rw type {identityref}
+--ro ietf-interfaces:interfaces-state
   +--ro interface* [name]
      +--ro admin-status {enumeration}
      +--ro higher-layer-if* {interface-state-ref(leafref)}
      +--ro if-index {int32}
      +--ro ietf-ip:ipv4!
      |  +--ro address* [ip]
      |  |  +--ro ip {ipv4-address-no-zone(string)}
      |  |  +--ro origin? {ip-address-origin(enumeration)}
      |  |  +--ro (subnet)?
      |  |     +--:(netmask)
      |  |     |  +--ro netmask? {dotted-quad(string)}
      |  |     +--:(prefix-length)
      |  |        +--ro prefix-length? {uint8}
      |  +--ro forwarding? {boolean}
      |  +--ro mtu? {uint16}
      |  +--ro neighbor* [ip]
      |     +--ro ip {ipv4-address-no-zone(string)}
      |     +--ro link-layer-address? {phys-address(string)}
      |     +--ro origin? {neighbor-origin(enumeration)}
      +--ro ietf-ip:ipv6!
      |  +--ro address* [ip]
      |  |  +--ro ip {ipv6-address-no-zone(string)}
      |  |  +--ro origin? {ip-address-origin(enumeration)}
      |  |  +--ro prefix-length {uint8}
      |  |  +--ro status? {enumeration}
      |  +--ro forwarding? {boolean}
      |  +--ro mtu? {uint32}
      |  +--ro neighbor* [ip]
      |     +--ro ip {ipv6-address-no-zone(string)}
      |     +--ro is-router? {empty}
      |     +--ro link-layer-address? {phys-address(string)}
      |     +--ro origin? {neighbor-origin(enumeration)}
      |     +--ro state? {enumeration}
      +--ro last-change? {date-and-time(string)}
      +--ro lower-layer-if* {interface-state-ref(leafref)}
      +--ro name {string}
      +--ro oper-status {enumeration}
      +--ro phys-address? {phys-address(string)}
      +--ro speed? {gauge64(uint64)}
      +--ro statistics
      |  +--ro discontinuity-time {date-and-time(string)}
      |  +--ro in-broadcast-pkts? {counter64(uint64)}
      |  +--ro in-discards? {counter32(uint32)}
      |  +--ro in-errors? {counter32(uint32)}
      |  +--ro in-multicast-pkts? {counter64(uint64)}
      |  +--ro in-octets? {counter64(uint64)}
      |  +--ro in-unicast-pkts? {counter64(uint64)}
      |  +--ro in-unknown-protos? {counter32(uint32)}
      |  +--ro out-broadcast-pkts? {counter64(uint64)}
      |  +--ro out-discards? {counter32(uint32)}
      |  +--ro out-errors? {counter32(uint32)}
      |  +--ro out-multicast-pkts? {counter64(uint64)}
      |  +--ro out-octets? {counter64(uint64)}
      |  +--ro out-unicast-pkts? {counter64(uint64)}
      +--ro type {identityref}
```

Sample data:
```
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/4
 description vCPEs access control
 ip address 172.16.33.10 255.255.255.128
! 
```

Sample results:
```
{
    "ietf-interfaces:interfaces": {
        "interface": [
            {
                "admin-status": "down",
                "description": "Customer " "#32148",
                "enabled": False,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "172.16.33.10",
                            "netmask": "255.255.255.128",
                            "origin": "static",
                        }
                    ]
                },
                "if-index": 1,
                "link-up-down-trap-enable": "enabled",
                "name": "GigabitEthernet1/3.251",
                "oper-status": "unknown",
                "statistics": {
                    "discontinuity-time": "1970-01-01T00:00:00+00:00"
                },
                "type": "iana-if-type:ethernetCsmacd",
            },
            {
                "admin-status": "up",
                "description": "vCPEs " "access " "control",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "172.16.33.10",
                            "netmask": "255.255.255.128",
                            "origin": "static",
                        }
                    ]
                },
                "if-index": 1,
                "link-up-down-trap-enable": "enabled",
                "name": "GigabitEthernet1/4",
                "oper-status": "unknown",
                "statistics": {
                    "discontinuity-time": "1970-01-01T00:00:00+00:00"
                },
                "type": "iana-if-type:ethernetCsmacd",
            },
        ]
    }
}
```


# ----------------------------------------------------------------------------
# Cisco IOS interfaces groups and inputs
# ----------------------------------------------------------------------------



---

<details><summary>Template Content</summary>
```
<doc>
This templates produces structured data compatible with ietf-interfaces YANG module
out of Cisco IOS 'show run' configuration output.

YANG ietf-interfaces module tree:
'''
+--rw ietf-interfaces:interfaces
|  +--rw interface* [name]
|     +--ro admin-status {enumeration}
|     +--rw description? {string}
|     +--rw enabled? {boolean}
|     +--ro higher-layer-if* {interface-ref(leafref)}
|     +--ro if-index {int32}
|     +--rw ietf-ip:ipv4!
|     |  +--rw address* [ip]
|     |  |  +--rw ip {ipv4-address-no-zone(string)}
|     |  |  +--ro origin? {ip-address-origin(enumeration)}
|     |  |  +--rw (subnet)
|     |  |     +--:(netmask)
|     |  |     |  +--rw netmask? {dotted-quad(string)}
|     |  |     +--:(prefix-length)
|     |  |        +--rw prefix-length? {uint8}
|     |  +--rw enabled? {boolean}
|     |  +--rw forwarding? {boolean}
|     |  +--rw mtu? {uint16}
|     |  +--rw neighbor* [ip]
|     |     +--rw ip {ipv4-address-no-zone(string)}
|     |     +--rw link-layer-address {phys-address(string)}
|     |     +--ro origin? {neighbor-origin(enumeration)}
|     +--rw ietf-ip:ipv6!
|     |  +--rw address* [ip]
|     |  |  +--rw ip {ipv6-address-no-zone(string)}
|     |  |  +--ro origin? {ip-address-origin(enumeration)}
|     |  |  +--rw prefix-length {uint8}
|     |  |  +--ro status? {enumeration}
|     |  +--rw autoconf
|     |  |  +--rw create-global-addresses? {boolean}
|     |  |  +--rw create-temporary-addresses? {boolean}
|     |  |  +--rw temporary-preferred-lifetime? {uint32}
|     |  |  +--rw temporary-valid-lifetime? {uint32}
|     |  +--rw dup-addr-detect-transmits? {uint32}
|     |  +--rw enabled? {boolean}
|     |  +--rw forwarding? {boolean}
|     |  +--rw mtu? {uint32}
|     |  +--rw neighbor* [ip]
|     |     +--rw ip {ipv6-address-no-zone(string)}
|     |     +--ro is-router? {empty}
|     |     +--rw link-layer-address {phys-address(string)}
|     |     +--ro origin? {neighbor-origin(enumeration)}
|     |     +--ro state? {enumeration}
|     +--ro last-change? {date-and-time(string)}
|     +--rw link-up-down-trap-enable? {enumeration}
|     +--ro lower-layer-if* {interface-ref(leafref)}
|     +--rw name {string}
|     +--ro oper-status {enumeration}
|     +--ro phys-address? {phys-address(string)}
|     +--ro speed? {gauge64(uint64)}
|     +--ro statistics
|     |  +--ro discontinuity-time {date-and-time(string)}
|     |  +--ro in-broadcast-pkts? {counter64(uint64)}
|     |  +--ro in-discards? {counter32(uint32)}
|     |  +--ro in-errors? {counter32(uint32)}
|     |  +--ro in-multicast-pkts? {counter64(uint64)}
|     |  +--ro in-octets? {counter64(uint64)}
|     |  +--ro in-unicast-pkts? {counter64(uint64)}
|     |  +--ro in-unknown-protos? {counter32(uint32)}
|     |  +--ro out-broadcast-pkts? {counter64(uint64)}
|     |  +--ro out-discards? {counter32(uint32)}
|     |  +--ro out-errors? {counter32(uint32)}
|     |  +--ro out-multicast-pkts? {counter64(uint64)}
|     |  +--ro out-octets? {counter64(uint64)}
|     |  +--ro out-unicast-pkts? {counter64(uint64)}
|     +--rw type {identityref}
+--ro ietf-interfaces:interfaces-state
   +--ro interface* [name]
      +--ro admin-status {enumeration}
      +--ro higher-layer-if* {interface-state-ref(leafref)}
      +--ro if-index {int32}
      +--ro ietf-ip:ipv4!
      |  +--ro address* [ip]
      |  |  +--ro ip {ipv4-address-no-zone(string)}
      |  |  +--ro origin? {ip-address-origin(enumeration)}
      |  |  +--ro (subnet)?
      |  |     +--:(netmask)
      |  |     |  +--ro netmask? {dotted-quad(string)}
      |  |     +--:(prefix-length)
      |  |        +--ro prefix-length? {uint8}
      |  +--ro forwarding? {boolean}
      |  +--ro mtu? {uint16}
      |  +--ro neighbor* [ip]
      |     +--ro ip {ipv4-address-no-zone(string)}
      |     +--ro link-layer-address? {phys-address(string)}
      |     +--ro origin? {neighbor-origin(enumeration)}
      +--ro ietf-ip:ipv6!
      |  +--ro address* [ip]
      |  |  +--ro ip {ipv6-address-no-zone(string)}
      |  |  +--ro origin? {ip-address-origin(enumeration)}
      |  |  +--ro prefix-length {uint8}
      |  |  +--ro status? {enumeration}
      |  +--ro forwarding? {boolean}
      |  +--ro mtu? {uint32}
      |  +--ro neighbor* [ip]
      |     +--ro ip {ipv6-address-no-zone(string)}
      |     +--ro is-router? {empty}
      |     +--ro link-layer-address? {phys-address(string)}
      |     +--ro origin? {neighbor-origin(enumeration)}
      |     +--ro state? {enumeration}
      +--ro last-change? {date-and-time(string)}
      +--ro lower-layer-if* {interface-state-ref(leafref)}
      +--ro name {string}
      +--ro oper-status {enumeration}
      +--ro phys-address? {phys-address(string)}
      +--ro speed? {gauge64(uint64)}
      +--ro statistics
      |  +--ro discontinuity-time {date-and-time(string)}
      |  +--ro in-broadcast-pkts? {counter64(uint64)}
      |  +--ro in-discards? {counter32(uint32)}
      |  +--ro in-errors? {counter32(uint32)}
      |  +--ro in-multicast-pkts? {counter64(uint64)}
      |  +--ro in-octets? {counter64(uint64)}
      |  +--ro in-unicast-pkts? {counter64(uint64)}
      |  +--ro in-unknown-protos? {counter32(uint32)}
      |  +--ro out-broadcast-pkts? {counter64(uint64)}
      |  +--ro out-discards? {counter32(uint32)}
      |  +--ro out-errors? {counter32(uint32)}
      |  +--ro out-multicast-pkts? {counter64(uint64)}
      |  +--ro out-octets? {counter64(uint64)}
      |  +--ro out-unicast-pkts? {counter64(uint64)}
      +--ro type {identityref}
'''

Sample data:
'''
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/4
 description vCPEs access control
 ip address 172.16.33.10 255.255.255.128
! 
'''

Sample results:
'''
{
    "ietf-interfaces:interfaces": {
        "interface": [
            {
                "admin-status": "down",
                "description": "Customer " "#32148",
                "enabled": False,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "172.16.33.10",
                            "netmask": "255.255.255.128",
                            "origin": "static",
                        }
                    ]
                },
                "if-index": 1,
                "link-up-down-trap-enable": "enabled",
                "name": "GigabitEthernet1/3.251",
                "oper-status": "unknown",
                "statistics": {
                    "discontinuity-time": "1970-01-01T00:00:00+00:00"
                },
                "type": "iana-if-type:ethernetCsmacd",
            },
            {
                "admin-status": "up",
                "description": "vCPEs " "access " "control",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "172.16.33.10",
                            "netmask": "255.255.255.128",
                            "origin": "static",
                        }
                    ]
                },
                "if-index": 1,
                "link-up-down-trap-enable": "enabled",
                "name": "GigabitEthernet1/4",
                "oper-status": "unknown",
                "statistics": {
                    "discontinuity-time": "1970-01-01T00:00:00+00:00"
                },
                "type": "iana-if-type:ethernetCsmacd",
            },
        ]
    }
}
'''
</doc>


<macro>
def add_iftype(data):
    if "eth" in data.lower():
        return data, {"type": "iana-if-type:ethernetCsmacd"}
    return data, {"type": None}
</macro>


<doc>
# ----------------------------------------------------------------------------
# Cisco IOS interfaces groups and inputs
# ----------------------------------------------------------------------------
</doc>

<input>
commands = [
    "show running-config | section interface",
    "show interface"
]
</input>

<group name="ietf-interfaces:interfaces.interface*">
## ----------------------------------------------------------------------------
## ietf-interface section
## ----------------------------------------------------------------------------
interface {{ name | macro(add_iftype) }}
 description {{ description | re(".+") }}
 shutdown {{ enabled | set(False) | let("admin-status", "down") }}
 {{ link-up-down-trap-enable | set(enabled) }}
 {{ admin-status | set(up) }}
 {{ enabled | set(True) }}
 {{ if-index | set(1) }}
 {{ statistics | set({"discontinuity-time": "1970-01-01T00:00:00+00:00"}) }}
 {{ oper-status | set(unknown) }}
 
## ----------------------------------------------------------------------------
## ietf-ip section
## ----------------------------------------------------------------------------
 <group name="ietf-ip:ipv4">
 ip mtu {{ mtu | to_int }} 
 </group>
 
 <group name="ietf-ip:ipv4.address*">
 ip address {{ ip | _start_ }} {{ netmask }}
 ip address {{ ip | _start_ }} {{ netmask }} secondary
 {{ origin | set(static) }}  
 </group>

 <group name="ietf-ip:ipv6.address*">
 ipv6 address {{ ip | _start_ }}/{{ prefix-length | to_int }}
 {{ origin | set(static) }}  
 </group>
 
</group>

<output condition="validate_with_yangson, True">
validate_yangson="'./yang-modules/ietf/'"
</output>
```
</details>