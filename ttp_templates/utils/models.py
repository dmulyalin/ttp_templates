from pydantic import (
    BaseModel,
    ConfigDict,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    model_validator,
)
from typing import Union, List


class InterfaceConfigRecord(BaseModel):
    name: StrictStr
    type: StrictStr
    enabled: StrictBool
    parent: Union[None, StrictStr]
    lag: Union[None, StrictStr]
    lag_id: Union[None, StrictInt]
    lag_type: Union[None, StrictStr]
    lacp_mode: Union[None, StrictStr]
    mtu: Union[None, StrictInt]
    mac_address: Union[None, StrictStr]
    speed: Union[None, StrictInt]
    duplex: Union[None, StrictStr]
    description: Union[None, StrictStr]
    mode: Union[None, StrictStr]
    untagged_vlan: Union[None, StrictInt, StrictStr]
    tagged_vlans: List[Union[StrictInt, StrictStr]]
    ipv4_addresses: List[StrictStr]
    ipv6_addresses: List[StrictStr]
    qinq_svlan: Union[None, StrictInt]
    vrf: Union[None, StrictStr]


class InterfaceStatusRecord(BaseModel):
    name: StrictStr
    description: Union[None, StrictStr]
    mtu: Union[None, StrictInt]
    mac_address: Union[None, StrictStr]
    duplex: Union[None, StrictStr]
    status_admin: StrictStr
    status_oper: StrictStr
    speed_bps: Union[None, StrictInt]
    last_cleared: Union[None, StrictStr]
    transitions: Union[None, StrictInt]
    errors_in: Union[None, StrictInt]
    errors_out: Union[None, StrictInt]
    crc_errors: Union[None, StrictInt]
    packets_in: Union[None, StrictInt]
    packets_out: Union[None, StrictInt]
    rate_bps_in: Union[None, StrictInt]
    rate_bps_out: Union[None, StrictInt]
    input_utilization: Union[None, StrictFloat] = None
    output_utilization: Union[None, StrictFloat] = None
    rate_pps_in: Union[None, StrictInt]
    rate_pps_out: Union[None, StrictInt]
    rate_interval: Union[None, StrictInt]

    @staticmethod
    def _calculate_utilization(
        rate_bps: Union[None, StrictInt], speed_bps: Union[None, StrictInt]
    ) -> Union[None, float]:
        if rate_bps is None or speed_bps is None or speed_bps <= 0:
            return None
        return rate_bps * 100 / speed_bps

    @model_validator(mode="after")
    def calculate_utilization(self):
        """Calculate input/output utilization as a percentage of port speed."""
        self.input_utilization = self._calculate_utilization(
            self.rate_bps_in, self.speed_bps
        )
        self.output_utilization = self._calculate_utilization(
            self.rate_bps_out, self.speed_bps
        )
        return self


class LldpNeighborRecord(BaseModel):
    interface: StrictStr
    remote_device: Union[None, StrictStr]
    remote_interface: Union[None, StrictStr]
    remote_system_description: Union[None, StrictStr]
    remote_chassi_id: Union[None, StrictStr]
    remote_interface_description: Union[None, StrictStr]
    remote_device_management_ip: Union[None, StrictStr]


class BgpNeighborRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: StrictStr
    description: Union[None, StrictStr]
    state: Union[None, StrictStr]
    local_address: Union[None, StrictStr]
    local_interface: Union[None, StrictStr]
    remote_address: Union[None, StrictStr]
    local_as: Union[None, StrictInt]
    remote_as: StrictInt
    peer_group: Union[None, StrictStr]
    import_policies: List[StrictStr]
    export_policies: List[StrictStr]
    prefix_list_in: Union[None, StrictStr]
    prefix_list_out: Union[None, StrictStr]
    router_id: Union[None, StrictStr]
    peering_type: Union[None, StrictStr]
    vrf: Union[None, StrictStr]
    hold_time: Union[None, StrictInt]
    keepalive: Union[None, StrictInt]
    uptime_seconds: Union[None, StrictInt]
    max_ttl: Union[None, StrictInt]
    afi: List[StrictStr]
    ipv4_unicast_prefixes_sent: Union[None, StrictInt] = None
    ipv4_unicast_prefixes_received: Union[None, StrictInt] = None
    ipv6_unicast_prefixes_sent: Union[None, StrictInt] = None
    ipv6_unicast_prefixes_received: Union[None, StrictInt] = None
    ipv4_multicast_prefixes_sent: Union[None, StrictInt] = None
    ipv4_multicast_prefixes_received: Union[None, StrictInt] = None
    ipv6_multicast_prefixes_sent: Union[None, StrictInt] = None
    ipv6_multicast_prefixes_received: Union[None, StrictInt] = None
    ipv4_mpls_vpn_prefixes_sent: Union[None, StrictInt] = None
    ipv4_mpls_vpn_prefixes_received: Union[None, StrictInt] = None
    ipv6_mpls_vpn_prefixes_sent: Union[None, StrictInt] = None
    ipv6_mpls_vpn_prefixes_received: Union[None, StrictInt] = None
    ipv4_labeled_unicast_prefixes_sent: Union[None, StrictInt] = None
    ipv4_labeled_unicast_prefixes_received: Union[None, StrictInt] = None
    ipv6_labeled_unicast_prefixes_sent: Union[None, StrictInt] = None
    ipv6_labeled_unicast_prefixes_received: Union[None, StrictInt] = None
    l2vpn_evpn_prefixes_sent: Union[None, StrictInt] = None
    l2vpn_evpn_prefixes_received: Union[None, StrictInt] = None
    l2vpn_vpls_prefixes_sent: Union[None, StrictInt] = None
    l2vpn_vpls_prefixes_received: Union[None, StrictInt] = None
    ipv4_mdt_prefixes_sent: Union[None, StrictInt] = None
    ipv4_mdt_prefixes_received: Union[None, StrictInt] = None
    ipv4_flow_spec_prefixes_sent: Union[None, StrictInt] = None
    ipv4_flow_spec_prefixes_received: Union[None, StrictInt] = None
    ipv6_flow_spec_prefixes_sent: Union[None, StrictInt] = None
    ipv6_flow_spec_prefixes_received: Union[None, StrictInt] = None
    ipv4_sr_te_prefixes_sent: Union[None, StrictInt] = None
    ipv4_sr_te_prefixes_received: Union[None, StrictInt] = None
    ipv6_sr_te_prefixes_sent: Union[None, StrictInt] = None
    ipv6_sr_te_prefixes_received: Union[None, StrictInt] = None
    link_state_prefixes_sent: Union[None, StrictInt] = None
    link_state_prefixes_received: Union[None, StrictInt] = None


class BgpCommunityRecord(BaseModel):
    value: StrictStr
    type: StrictStr
    name: StrictStr


class BgpAsnRecord(BaseModel):
    asn: StrictInt
    description: Union[None, StrictStr]


class InventoryRecord(BaseModel):
    description: StrictStr
    module: StrictStr
    serial: StrictStr
    slot: StrictStr


class VlanRecord(BaseModel):
    vid: StrictInt
    name: StrictStr
    description: Union[None, StrictStr]


class VrfRecord(BaseModel):
    name: StrictStr
    description: Union[None, StrictStr]
    rd: Union[None, StrictStr]
    rt_import: List[StrictStr]
    rt_export: List[StrictStr]
    route_policy_import: Union[None, StrictStr]
    route_policy_export: Union[None, StrictStr]


class ArpRecord(BaseModel):
    ip: StrictStr
    age: Union[StrictInt, StrictStr]
    mac: StrictStr
    interface: Union[None, StrictStr] = None
    protocol: Union[None, StrictStr] = None
    state: Union[None, StrictStr] = None
    type: Union[None, StrictStr] = None
