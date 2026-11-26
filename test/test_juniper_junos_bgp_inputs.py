import json
from pathlib import Path

import pytest
from ttp import ttp

from ttp_templates import get_template, parse_output


@pytest.mark.parametrize("named_inputs", [True, False])
def test_junos_bgp_peer_ranges(named_inputs):
    def operational_peer(address, group, vrf, remote_as):
        fields = {
            "peer-address": f"{address}+179",
            "peer-group": group,
            "local-as": "65000",
            "peer-as": remote_as,
        }
        if vrf is not None:
            fields["peer-cfg-rti"] = vrf
        return {key: [{"data": value}] for key, value in fields.items()}

    peers = [
        operational_peer("10.2.2.7", "grp-2", "master", "4321"),
        operational_peer("10.1.2.3", "grp-2", "vrf-1", "1234"),
        operational_peer("10.1.2.4", "grp-2", "vrf-1", "1234"),
        operational_peer("10.1.2.5", "grp-2", "master", "1234"),
        operational_peer("10.2.2.8", "other-group", None, "4321"),
    ]
    operational = json.dumps({"bgp-information": [{"bgp-peer": peers}]}, indent=2)
    config_path = (
        Path(__file__).parent
        / "platform/juniper_junos/show_bgp_dynamic_peer_configuration/dynamic_peers.txt"
    )
    configuration = config_path.read_text(encoding="utf-8")

    if named_inputs:
        parser = ttp(template=get_template(get="bgp_neighbors"))
        for input_name, data in (
            ("operational", operational),
            ("configuration", configuration),
        ):
            parser.add_input(
                data,
                input_name=input_name,
                template_name="junper_junos_bgp_neighbors",
            )
        parser.parse(one=True)
        records = parser.result(structure="dictionary")["junper_junos_bgp_neighbors"]
    else:
        records = parse_output(
            data=f"{operational}\n{configuration}",
            get="bgp_neighbors",
            platform="juniper_junos",
        )

    assert {record["name"]: record["vrf"] for record in records} == {
        "default_10.2.2.7": "default",
        "vrf-1_10.1.2.3": "vrf-1",
        "vrf-1_10.1.2.4": "vrf-1",
        "default_10.1.2.5": "default",
        "default_10.2.2.8": "default",
        "default_10.2.2.0/24": "default",
        "vrf-1_10.1.2.0/24": "vrf-1",
    }
    assert {record["name"]: record["remote_address_range"] for record in records} == {
        "default_10.2.2.7": "10.2.2.0/24",
        "vrf-1_10.1.2.3": "10.1.2.0/24",
        "vrf-1_10.1.2.4": "10.1.2.0/24",
        "default_10.1.2.5": None,
        "default_10.2.2.8": None,
        "default_10.2.2.0/24": "10.2.2.0/24",
        "vrf-1_10.1.2.0/24": "10.1.2.0/24",
    }
