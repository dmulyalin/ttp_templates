Reference path:
```
ttp://misc/N2G/cli_isis_data/juniper.txt
```

---



Template to parse Juniper JunOS "show isis database extensive | no-more" output.


Template to parse ISIS LSDB of Juniper JunOS devices out of 
"show isis database extensive | no-more" command output.

For this sample data:
```
IS-IS level 2 link-state database:

R1-X1.00-00 Sequence: 0x22425, Checksum: 0x8904, Lifetime: 463 secs
   IS neighbor: R1-X2.00                       Metric:       20
     Two-way fragment: R1-X2.00-00, Two-way first fragment: R1-X2.00-00
   IP prefix: 10.123.123.31/32                 Metric:        0 Internal Up
   IP prefix: 10.123.123.41/32                 Metric:        0 Internal Up
   V6 prefix: ::ffff:10.123.111.236/126        Metric:       20 Internal Up

  Header: LSP ID: R1-X1.00-00, Length: 233 bytes
    Allocated length: 284 bytes, Router ID: 10.123.123.31
    Remaining lifetime: 463 secs, Level: 2, Interface: 80
    Estimated free bytes: 51, Actual free bytes: 51
    Aging timer expires in: 463 secs
    Protocols: IP, IPv6

  Packet: LSP ID: R1-X1.00-00, Length: 233 bytes, Lifetime : 1194 secs
    Checksum: 0x8904, Sequence: 0x22425, Attributes: 0x3 L1 L2
    NLPID: 0x83, Fixed length: 27 bytes, Version: 1, Sysid length: 0 bytes
    Packet type: 20, Packet version: 1, Max area: 0

  TLVs:
    Area address: 49.0001 (3)
    LSP Buffer Size: 1492
    Speaks: IP
    Speaks: IPV6
    IP router id: 10.123.123.31
    IP address: 10.123.123.31
    IPv6 TE Router ID: 2001::10:123:123:31
    Hostname: R1-X1
    Extended IS Reachability TLV, Type: 22, Length: 85
    IS extended neighbor: R1-X2.00, Metric: default 20 SubTLV len: 74
      IP address: 10.123.111.238
      Neighbor's IP address: 10.123.111.237
      Local interface index: 332, Remote interface index: 461
      Current reservable bandwidth:
        Priority 0 : 7Gbps
        Priority 1 : 7Gbps
        Priority 2 : 7Gbps
        Priority 3 : 7Gbps
        Priority 4 : 7Gbps
        Priority 5 : 7Gbps
        Priority 6 : 6.7Gbps
        Priority 7 : 6.7Gbps
      Maximum reservable bandwidth: 7Gbps
      Maximum bandwidth: 10Gbps
      Administrative groups:  0 none
    IPv6 prefix: ::ffff:10.123.111.236/126 Metric 20 Up
    IP extended prefix: 10.123.123.31/32 metric 0 up
    IP extended prefix: 10.123.123.41/32 metric 0 up
    IP extended prefix: 10.123.111.236/30 metric 20 up
    IP address: 10.123.123.41
    Authentication data: 17 bytes
  No queued transmissions
```

This template produces this result:
```
[[{'isis_processes': {'ISIS': {'R1-X1': [{'isis_area': '49.0001',
                                          'level': '2',
                                          'links': [{'bw_gbit': '10',
                                                     'local_intf_id': '332',
                                                     'local_ip': '10.123.111.238',
                                                     'metric': '20',
                                                     'peer_intf_id': '461',
                                                     'peer_ip': '10.123.111.237',
                                                     'peer_name': 'R1-X2'}],
                                          'networks': [{'metric': '0',
                                                        'network': '10.123.123.31/32'},
                                                       {'metric': '0',
                                                        'network': '10.123.123.41/32'},
                                                       {'metric': '20',
                                                        'network': '::ffff:10.123.111.236/126'}],
                                          'rid': '10.123.123.31',
                                          'rid_v6': '2001::10:123:123:31'}]}}}]]
```

Notes:

- Process ID (PID) always set to `ISIS` value as PID does not present in 
  "show isis database extensive | no-more" command output on Juniper devices.



---

<details><summary>Template Content</summary>
```
<doc>
Template to parse Juniper JunOS "show isis database extensive | no-more" output.
</doc>

<input load="python">
commands = [
    "show isis database extensive | no-more",
]
platform = ["juniper", "juniper_junos"]
</input>

<extend template="ttp://platform/juniper_show_isis_database_verbose_pipe_no_more.txt"/>
```
</details>