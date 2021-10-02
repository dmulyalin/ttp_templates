Reference path:
```
ttp://platform.cisco_xr_show_isis_database_verbose.txt
```

---



Template to parse ISIS LSDP of Cisco IOS-XR devices as produced
by "show isis database verbose" command.

This template produces this structure:

[[{'isis_processes': {'100': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '9',
                                                  'local_ip': '10.123.0.17',
                                                  'metric': '16777214',
                                                  'peer_intf_id': '50',
                                                  'peer_ip': '10.123.0.18',
                                                  'peer_name': 'R1-X2'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.1/32'}],
                                       'rid': '10.111.1.1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '48',
                                                  'local_ip': '10.123.0.33',
                                                  'metric': '456',
                                                  'peer_intf_id': '53',
                                                  'peer_ip': '10.123.0.34',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.2/32'}],
                                       'rid': '10.111.1.2'}]},
                      '200': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '57',
                                                  'peer_name': 'R2-X1'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': 'fddd:2:c101::1/128'},,
                                       'rid': 'fddd:2:c101::1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '60',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': 'fdff::/36'}],
                                       'rid': 'fddd:2:c101::2'}]}}}]]



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse ISIS LSDP of Cisco IOS-XR devices as produced
by "show isis database verbose" command.

This template produces this structure:

[[{'isis_processes': {'100': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '9',
                                                  'local_ip': '10.123.0.17',
                                                  'metric': '16777214',
                                                  'peer_intf_id': '50',
                                                  'peer_ip': '10.123.0.18',
                                                  'peer_name': 'R1-X2'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.1/32'}],
                                       'rid': '10.111.1.1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'affinity': '0x00000000',
                                                  'bw_kbit': '10000000',
                                                  'local_intf_id': '48',
                                                  'local_ip': '10.123.0.33',
                                                  'metric': '456',
                                                  'peer_intf_id': '53',
                                                  'peer_ip': '10.123.0.34',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': '10.111.1.2/32'}],
                                       'rid': '10.111.1.2'}]},
                      '200': {'LSP': [{'hostname': 'R1-X1',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '57',
                                                  'peer_name': 'R2-X1'}],
                                       'lsp_id': 'R1-X1',
                                       'networks': [{'metric': '0',
                                                     'network': 'fddd:2:c101::1/128'},,
                                       'rid': 'fddd:2:c101::1'},
                                      {'hostname': 'R1-X2',
                                       'isis_area': '49.0001',
                                       'level': 'Level-2',
                                       'links': [{'bw_kbit': '10000000',
                                                  'delay_avg_us': '1',
                                                  'delay_max_us': '1',
                                                  'delay_min_us': '1',
                                                  'delay_variation_us': '0',
                                                  'local_intf_id': '68',
                                                  'metric': '10',
                                                  'peer_intf_id': '60',
                                                  'peer_name': 'R2-X2'}],
                                       'lsp_id': 'R1-X2',
                                       'networks': [{'metric': '0',
                                                     'network': 'fdff::/36'}],
                                       'rid': 'fddd:2:c101::2'}]}}}]]
</doc>

<group name="isis_processes.{{ pid }}**" functions="record('level') | del('level')">
IS-IS {{ pid }} ({{ level }}) Link State Database

<group name="LSP*" set="level">
{{ lsp_id | _start_ }}.00-00 * {{ ignore }} {{ ignore }} 65487/*      0/0/0
{{ lsp_id | _start_ }}.00-00   {{ ignore }} {{ ignore }} 64768/65535  0/0/0
{{ lsp_id | _start_ }}.00-00*  {{ ignore }} {{ ignore }} 65487/*      0/0/0
  Auth:           {{ auth }}, Length: 17
  Area Address:   {{ isis_area }}
  Router ID:      {{ rid }}
  Hostname:       {{ hostname }}
  IPv6 Address:   {{ rid }}
    IPv6 Router ID: {{ rid }}
	
  <group name="networks*">
  Metric: {{ metric | _start_ }}     IP-Extended {{ network }}
  Metric: {{ metric | _start_ }}     MT (IPv6 Unicast) IPv6 {{ network | _exact_ }}
  Metric: {{ metric | _start_ }}     MT (IPv6 Unicast) IPv6-Ext-InAr {{ network | _exact_ }}
  </group>
  
  <group name="links*">
  Metric: {{ metric | _start_ }}   IS-Extended {{ peer_name }}.00
  Metric: {{ metric | _start_ }}   MT (IPv6 Unicast) IS-Extended {{ peer_name }}.00
    Local Interface ID: {{ local_intf_id }}, Remote Interface ID: {{ peer_intf_id }}
    Interface IP Address: {{ local_ip }}
    Neighbor IP Address: {{ peer_ip }}
    Affinity: {{ affinity }}
    Physical BW: {{ bw_kbit }} kbits/sec
    Link Average Delay: {{ delay_avg_us }} us
    Link Min/Max Delay: {{ delay_min_us }}/{{ delay_max_us }} us
    Link Delay Variation: {{ delay_variation_us }} us
    <group name="srv6_endx_sid*">
    END.X SID: {{ sid | IPV6}} B:0 S:0 P:0 uA (PSP/USD) Alg:{{ algo }}
        Block Length: {{ block_length }}, Node-ID Length: {{ node_id_length }}, Func-Length: {{ func_length }}, Args-Length: {{ args_length }}
	</group>
  </group>
  
  <group name="srv6_locators*">
  SRv6 Locator:   MT (IPv6 Unicast) {{ locator | IPV6 }}/{{ mask }} D:0 Metric: 0 Algorithm: {{ algo }}
  </group>
  
</group>
</group>
```
</details>