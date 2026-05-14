from pydantic import BaseModel, StrictInt, StrictStr, StrictBool
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
    untagged_vlan: Union[None, StrictInt]
    tagged_vlans: List[StrictInt]
    ipv4_addresses: List[StrictStr]
    ipv6_addresses: List[StrictStr]
    qinq_svlan: Union[None, StrictInt]
    vrf: Union[None, StrictStr]


class LldpNeighborRecord(BaseModel):
    interface: StrictStr
    remote_device: Union[None, StrictStr]
    remote_interface: Union[None, StrictStr]
    remote_system_description: Union[None, StrictStr]
    remote_chassi_id: Union[None, StrictStr]
    remote_interface_description: Union[None, StrictStr]
    remote_device_management_ip: Union[None, StrictStr]
