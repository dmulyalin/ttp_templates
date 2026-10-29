"""Named TTP inputs need explicit routing beyond the dynamic fixture runner."""

import json
from pathlib import Path

import pytest
import yaml
from ttp import ttp

from ttp_templates import get_template
from ttp_templates.utils.arista_eos_process_show_bgp_neighbors_vrf_all_pipe_json import (
    transform_bgp_neighbors,
)


@pytest.mark.parametrize("wrapped", [False, True])
def test_merge_peer_groups_and_multiple_json_captures(wrapped):
    def capture(address):
        return {
            "data": json.dumps(
                {
                    "vrfs": {
                        "default": {
                            "peerList": [
                                {
                                    "peerAddress": address,
                                    "localAsn": 65000,
                                    "asn": 65001,
                                }
                            ]
                        }
                    }
                }
            )[1:-1]
        }

    payload = {
        "ipv4_peers": [capture("192.0.2.1"), capture("192.0.2.2")],
        "ipv6_peers": [capture("2001:db8::1")],
    }
    result = transform_bgp_neighbors([payload] if wrapped else payload)
    assert [peer["remote_address"] for peer in result] == [
        "192.0.2.1",
        "192.0.2.2",
        "2001:db8::1",
    ]


@pytest.mark.parametrize("payload", [{}, [], {"ipv6_peers": []}])
def test_empty_peer_groups(payload):
    assert transform_bgp_neighbors(payload) == []


def test_named_inputs_merge_all_fixture_records():
    folder = (
        Path(__file__).parent
        / "platform/arista_eos/show_ip_bgp_neighbors_vrf_all_pipe_json"
    )
    ipv6_folder = folder.parent / "show_ipv6_bgp_peers_vrf_all_pipe_json"
    samples = [("ipv4", sample) for sample in sorted(folder.glob("*.txt"))]
    samples.extend(("ipv6", sample) for sample in sorted(ipv6_folder.glob("*.txt")))
    parser = ttp(
        template=get_template(
            platform="arista_eos", command="show ip bgp neighbors vrf all | json"
        )
    )
    expected = []
    for input_name, sample in samples:
        parser.add_input(
            sample.read_text(encoding="utf-8"),
            input_name=input_name,
            template_name="arista_eos_bgp_neighbors",
        )
        expected.extend(
            yaml.safe_load(sample.with_suffix(".yml").read_text(encoding="utf-8"))
        )
    parser.parse()
    assert parser.result(structure="flat_list") == expected
