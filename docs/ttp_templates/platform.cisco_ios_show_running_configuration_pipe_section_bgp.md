Reference path:
```
ttp://platform/cisco_ios_show_running_configuration_pipe_section_bgp.txt
```

---



Template to parse Cisco IOS BGP configuration.

Requirements: `TTP >= 0.7.x`

Structure produced by this template does not follow any known convention 
or schema for example openconfig-bgp, but rather was the easiest one to 
produce using TTP built-in features without overwhelming template with
post-processing python code. Resulted structure follows Cisco native 
configuration style and capable of parsing subsets of: 

- BGP global configuration
- BGP global neighbors and peer-groups definition
- AFI configuration including neighbors and networks
- VRF configuration including neighbors, networks and other parameters

Sample device output:
```
router bgp 65001
 !
 bgp router-id 10.5.1.1
 bgp log-neighbor-changes
 neighbor 2001:db8::1 remote-as 65003
 neighbor 2001:db8::1 description Peer1-Global
 neighbor 10.11.0.81 remote-as 65002
 neighbor 10.11.0.81 description Peer2-Global
 neighbor 10.11.0.81 shutdown
 neighbor RR-CLIENTS peer-group
 neighbor RR-CLIENTS remote-as 65001
 neighbor RR-CLIENTS description [ibgp - rr clients]
 neighbor RR-CLIENTS update-source GigabitEthernet1
 neighbor 10.0.0.3 peer-group RR-CLIENTS
 neighbor 10.0.0.5 peer-group RR-CLIENTS
 !
 address-family ipv4
  network 10.255.10.0 mask 255.255.248.0
  network 10.255.10.0 mask 255.255.255.0
  redistribute connected route-map PORTABLE-v4
  neighbor 10.11.0.81 activate
  neighbor 10.11.0.81 description Peer2-IPv4
  neighbor RR-CLIENTS route-reflector-client
  neighbor RR-CLIENTS route-map PASS-IN in
  neighbor RR-CLIENTS route-map PASS-OUT out
  neighbor RR-CLIENTS maximum-prefix 1000 80 restart 15
  neighbor 10.0.0.3 activate
  neighbor 10.0.0.5 activate
 exit-address-family
 !
 address-family ipv6
  redistribute connected
  network 2001:db8::/48
  neighbor 2001:db8::1 activate
  neighbor 2001:db8::1 description Peer1-IPv6
 exit-address-family
 !
 address-family ipv4 multicast
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 3.3.3.3 activate
 exit-address-family 
 !
 address-family ipv4 vrf VoIP
  network 10.255.10.0 mask 255.255.248.0 
  bgp router-id 10.2.1.193
  redistribute connected route-map tospokes
  neighbor 10.2.1.65 remote-as 65001
  neighbor 10.2.1.65 description voip peer 1
  neighbor 10.2.1.65 activate
  neighbor 10.2.1.78 remote-as 65001
  neighbor 10.2.1.78 description voip peer 2
  neighbor 10.2.1.78 shutdown
  neighbor 10.2.1.78 activate
  neighbor 10.2.1.78 next-hop-self
  neighbor 10.2.1.78 prefix-list VoIP-prefixes out
 exit-address-family
!
 address-family ipv4 vrf CUST-2
  bgp router-id 1.1.1.1
  redistribute connected
  neighbor 2.2.2.2 remote-as 65002
  neighbor 2.2.2.2 description peer 12
  neighbor 2.2.2.2 activate
 exit-address-family
!
```
	
After parsing above output, TTP should produce these results:
```
[[{'bgp': {'afis': {'ipv4_multicast': {},
                    'ipv4_unicast': {'config': {'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'},
                                                             {'mask': '255.255.255.0', 'network': '10.255.10.0'}],
                                                'redistribute_connected': True,
                                                'redistribute_connected_rpl': 'PORTABLE-v4'},
                                     'neighbors': {'10.0.0.3': {'activate': True},
                                                   '10.0.0.5': {'activate': True},
                                                   '10.11.0.81': {'activate': True},
                                                   'RR-CLIENTS': {'max_prefix_action': 'restart',
                                                                  'max_prefix_limit': '1000',
                                                                  'max_prefix_restart_interval': '15',
                                                                  'max_prefix_threshold': '80',
                                                                  'rpl_out': 'PASS-OUT',
                                                                  'rr_client': True}}},
                    'ipv6_unicast': {'config': {'networks': [{'mask': '48', 'network': '2001:db8::'}], 'redistribute_connected': True},
                                     'neighbors': {'2001:db8::1': {'activate': True}}},
                    'vpnv4_unicast': {'neighbors': {'3.3.3.3': {'activate': True}}}},
           'asn': '65001',
           'config': {'bgp_rid': '10.5.1.1', 'log_neighbor_changes': True},
           'neighbors': {'10.0.0.3': {'peer_group': 'RR-CLIENTS'},
                         '10.0.0.5': {'peer_group': 'RR-CLIENTS'},
                         '10.11.0.81': {'asn': '65002', 'description': 'Peer2-Global', 'disabled': True},
                         '2001:db8::1': {'asn': '65003', 'description': 'Peer1-Global'},
                         'RR-CLIENTS': {'asn': '65001',
                                        'description': '[ibgp - rr clients]',
                                        'is_peer_group': True,
                                        'update_source': 'GigabitEthernet1'}},
           'vrfs': {'CUST-2': {'afi': 'ipv4',
                               'config': {'bgp_rid': '1.1.1.1', 'redistribute_connected': True},
                               'neighbors': {'2.2.2.2': {'activate': True, 'asn': '65002', 'description': 'peer 12'}}},
                    'VoIP': {'afi': 'ipv4',
                             'config': {'bgp_rid': '10.2.1.193',
                                        'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'}],
                                        'redistribute_connected': True,
                                        'redistribute_connected_rpl': 'tospokes'},
                             'neighbors': {'10.2.1.65': {'activate': True, 'asn': '65001', 'description': 'voip peer 1'},
                                           '10.2.1.78': {'activate': True,
                                                         'asn': '65001',
                                                         'description': 'voip peer 2',
                                                         'disabled': True,
                                                         'next_hop_self': True,
                                                         'pfl_out': 'VoIP-prefixes'}}}}}}]]
```

To use this template with Netmiko (>=3.4.x) run_ttp method:
```
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.bgp.txt")

pprint.pprint(res)
```



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse Cisco IOS BGP configuration.

Requirements: 'TTP >= 0.7.x'

Structure produced by this template does not follow any known convention 
or schema for example openconfig-bgp, but rather was the easiest one to 
produce using TTP built-in features without overwhelming template with
post-processing python code. Resulted structure follows Cisco native 
configuration style and capable of parsing subsets of: 

- BGP global configuration
- BGP global neighbors and peer-groups definition
- AFI configuration including neighbors and networks
- VRF configuration including neighbors, networks and other parameters

Sample device output:
'''
router bgp 65001
 !
 bgp router-id 10.5.1.1
 bgp log-neighbor-changes
 neighbor 2001:db8::1 remote-as 65003
 neighbor 2001:db8::1 description Peer1-Global
 neighbor 10.11.0.81 remote-as 65002
 neighbor 10.11.0.81 description Peer2-Global
 neighbor 10.11.0.81 shutdown
 neighbor RR-CLIENTS peer-group
 neighbor RR-CLIENTS remote-as 65001
 neighbor RR-CLIENTS description [ibgp - rr clients]
 neighbor RR-CLIENTS update-source GigabitEthernet1
 neighbor 10.0.0.3 peer-group RR-CLIENTS
 neighbor 10.0.0.5 peer-group RR-CLIENTS
 !
 address-family ipv4
  network 10.255.10.0 mask 255.255.248.0
  network 10.255.10.0 mask 255.255.255.0
  redistribute connected route-map PORTABLE-v4
  neighbor 10.11.0.81 activate
  neighbor 10.11.0.81 description Peer2-IPv4
  neighbor RR-CLIENTS route-reflector-client
  neighbor RR-CLIENTS route-map PASS-IN in
  neighbor RR-CLIENTS route-map PASS-OUT out
  neighbor RR-CLIENTS maximum-prefix 1000 80 restart 15
  neighbor 10.0.0.3 activate
  neighbor 10.0.0.5 activate
 exit-address-family
 !
 address-family ipv6
  redistribute connected
  network 2001:db8::/48
  neighbor 2001:db8::1 activate
  neighbor 2001:db8::1 description Peer1-IPv6
 exit-address-family
 !
 address-family ipv4 multicast
 exit-address-family
 !
 address-family vpnv4 unicast
  neighbor 3.3.3.3 activate
 exit-address-family 
 !
 address-family ipv4 vrf VoIP
  network 10.255.10.0 mask 255.255.248.0 
  bgp router-id 10.2.1.193
  redistribute connected route-map tospokes
  neighbor 10.2.1.65 remote-as 65001
  neighbor 10.2.1.65 description voip peer 1
  neighbor 10.2.1.65 activate
  neighbor 10.2.1.78 remote-as 65001
  neighbor 10.2.1.78 description voip peer 2
  neighbor 10.2.1.78 shutdown
  neighbor 10.2.1.78 activate
  neighbor 10.2.1.78 next-hop-self
  neighbor 10.2.1.78 prefix-list VoIP-prefixes out
 exit-address-family
!
 address-family ipv4 vrf CUST-2
  bgp router-id 1.1.1.1
  redistribute connected
  neighbor 2.2.2.2 remote-as 65002
  neighbor 2.2.2.2 description peer 12
  neighbor 2.2.2.2 activate
 exit-address-family
!
'''
	
After parsing above output, TTP should produce these results:
'''
[[{'bgp': {'afis': {'ipv4_multicast': {},
                    'ipv4_unicast': {'config': {'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'},
                                                             {'mask': '255.255.255.0', 'network': '10.255.10.0'}],
                                                'redistribute_connected': True,
                                                'redistribute_connected_rpl': 'PORTABLE-v4'},
                                     'neighbors': {'10.0.0.3': {'activate': True},
                                                   '10.0.0.5': {'activate': True},
                                                   '10.11.0.81': {'activate': True},
                                                   'RR-CLIENTS': {'max_prefix_action': 'restart',
                                                                  'max_prefix_limit': '1000',
                                                                  'max_prefix_restart_interval': '15',
                                                                  'max_prefix_threshold': '80',
                                                                  'rpl_out': 'PASS-OUT',
                                                                  'rr_client': True}}},
                    'ipv6_unicast': {'config': {'networks': [{'mask': '48', 'network': '2001:db8::'}], 'redistribute_connected': True},
                                     'neighbors': {'2001:db8::1': {'activate': True}}},
                    'vpnv4_unicast': {'neighbors': {'3.3.3.3': {'activate': True}}}},
           'asn': '65001',
           'config': {'bgp_rid': '10.5.1.1', 'log_neighbor_changes': True},
           'neighbors': {'10.0.0.3': {'peer_group': 'RR-CLIENTS'},
                         '10.0.0.5': {'peer_group': 'RR-CLIENTS'},
                         '10.11.0.81': {'asn': '65002', 'description': 'Peer2-Global', 'disabled': True},
                         '2001:db8::1': {'asn': '65003', 'description': 'Peer1-Global'},
                         'RR-CLIENTS': {'asn': '65001',
                                        'description': '[ibgp - rr clients]',
                                        'is_peer_group': True,
                                        'update_source': 'GigabitEthernet1'}},
           'vrfs': {'CUST-2': {'afi': 'ipv4',
                               'config': {'bgp_rid': '1.1.1.1', 'redistribute_connected': True},
                               'neighbors': {'2.2.2.2': {'activate': True, 'asn': '65002', 'description': 'peer 12'}}},
                    'VoIP': {'afi': 'ipv4',
                             'config': {'bgp_rid': '10.2.1.193',
                                        'networks': [{'mask': '255.255.248.0', 'network': '10.255.10.0'}],
                                        'redistribute_connected': True,
                                        'redistribute_connected_rpl': 'tospokes'},
                             'neighbors': {'10.2.1.65': {'activate': True, 'asn': '65001', 'description': 'voip peer 1'},
                                           '10.2.1.78': {'activate': True,
                                                         'asn': '65001',
                                                         'description': 'voip peer 2',
                                                         'disabled': True,
                                                         'next_hop_self': True,
                                                         'pfl_out': 'VoIP-prefixes'}}}}}}]]
'''

To use this template with Netmiko (>=3.4.x) run_ttp method:
'''
import pprint
from netmiko import ConnectHandler

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="1.2.3.4",
    username="admin",
    password="admin",
)

res = net_connect.run_ttp("ttp://misc/netmiko/cisco.ios.cfg.bgp.txt")

pprint.pprint(res)
'''
</doc>

<vars>
bgp_default = {
    "asn": "",
    "config": {},
    "afis": {},
    "neighbors": {},
    "vrfs": {}
}
</vars>

<group name="bgp" default="bgp_default">
router bgp {{ asn }}

 <group name="config**" method="table">
 bgp router-id {{ bgp_rid }}
 bgp log-neighbor-changes {{ log_neighbor_changes | set(True) }}
 </group>
 
 <group name="neighbors**.{{ neighbor }}**" method="table">
 neighbor {{ neighbor | let("is_peer_group", True) }} peer-group
 neighbor {{ neighbor }} remote-as {{ asn }}
 neighbor {{ neighbor }} description {{ description | re(".+") }}
 neighbor {{ neighbor }} update-source {{ update_source }}
 neighbor {{ neighbor }} peer-group {{ peer_group }}
 neighbor {{ neighbor | let("disabled", True) }} shutdown
 </group>

 <group name="afis**.{{ afi }}_{{ safi }}">
 address-family {{ afi }}
 address-family {{ afi }} {{ safi | default(unicast) | _start_ }}
 
  <group name="config**.networks*" method="table">
  network {{ network | IP }} mask {{ mask }}
  network {{ network | IPV6 }}/{{ mask }}
  </group>
  
  <group name="config**" method="table">
  redistribute connected route-map {{ redistribute_connected_rpl | let("redistribute_connected", True) }}
  redistribute connected {{ redistribute_connected | set(True) }} 
  </group>
  
  <group name="neighbors**.{{ neighbor }}**" method="table">
  neighbor {{ neighbor | let("activate", True) }} activate
  neighbor {{ neighbor | let("next_hop_self", True) }} next-hop-self
  neighbor {{ neighbor | let("rr_client", True) }} route-reflector-client
  neighbor {{ neighbor }} prefix-list {{ pfl_out }} out
  neighbor {{ neighbor }} prefix-list {{ pfl_in }} in
  neighbor {{ neighbor }} route-map {{ rpl_in }} in
  neighbor {{ neighbor }} route-map {{ rpl_out }} out
  neighbor {{ neighbor }} maximum-prefix {{ max_prefix_limit | let("max_prefix_action", "restart") }} {{ max_prefix_threshold }} restart {{ max_prefix_restart_interval }}
  </group>
  
 exit-address-family {{ _end_ }}
 </group>

 <group name="vrfs**.{{ vrf }}">
 address-family {{ afi }} vrf {{ vrf }}

  <group name="config**.networks*" method="table">
  network {{ network | IP }} mask {{ mask }}
  network {{ network | IPV6 }}/{{ mask }}
  </group>
  
  <group name="config**" method="table">
  bgp router-id {{ bgp_rid }}
  redistribute connected route-map {{ redistribute_connected_rpl | let("redistribute_connected", True) }}
  redistribute connected {{ redistribute_connected | set(True) }}
  </group>
 
  <group name="neighbors**.{{ neighbor }}**" method="table">  
  neighbor {{ neighbor }} remote-as {{ asn }}
  neighbor {{ neighbor }} description {{ description | re(".+") }}
  neighbor {{ neighbor | let("activate", True) }} activate
  neighbor {{ neighbor | let("disabled", True) }} shutdown
  neighbor {{ neighbor | let("next_hop_self", True) }} next-hop-self
  neighbor {{ neighbor | let("rr_client", True) }} route-reflector-client
  neighbor {{ neighbor }} prefix-list {{ pfl_out }} out
  neighbor {{ neighbor }} prefix-list {{ pfl_in }} in
  neighbor {{ neighbor }} route-map {{ rpl_in }} in
  neighbor {{ neighbor }} route-map {{ rpl_out }} out
  neighbor {{ neighbor }} maximum-prefix {{ max_prefix_limit | let("max_prefix_action", "restart") }} {{ max_prefix_threshold }} restart {{ max_prefix_restart_interval }}
  </group>
   
 exit-address-family {{ _end_ }}
 </group>
</group>
```
</details>