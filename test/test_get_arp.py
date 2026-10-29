"""The arp getter with each platform's inputs together, including the
commands that map interfaces to VRFs."""

from pathlib import Path

import pytest
import yaml
from ttp import ttp

from ttp_templates import get_template, parse_output
from ttp_templates.utils.arp import record, transform_cisco_ios

TEST_DIR = Path(__file__).parent
PLATFORM = TEST_DIR / "platform"
EXPECTED = TEST_DIR / "mock_data/get_arp"

# template name: {input name: fixture}
INPUTS = {
    "arista_eos_arp": {
        "ipv4": "arista_eos/show_ip_arp_vrf_all_pipe_json/show_ip_arp_vrf_all_pipe_json.txt",
        "ipv6": "arista_eos/show_ipv6_neighbors_vrf_all_pipe_json/show_ipv6_neighbors_vrf_all_pipe_json.txt",
    },
    "cisco_asa_arp": {
        "ipv4": "cisco_asa/show_arp/show_arp.txt",
        "ipv6": "cisco_asa/show_ipv6_neighbor/show_ipv6_neighbor.txt",
        "nameif": "cisco_asa/show_nameif/show_nameif.txt",
    },
    "cisco_ios_arp": {
        "ipv4": "cisco_ios/show_ip_arp/show_ip_arp.txt",
        "ipv6": "cisco_ios/show_ipv6_neighbors/show_ipv6_neighbors.txt",
    },
    "cisco_nxos_arp": {
        "ipv4": "cisco_nxos/show_ip_arp_detail_vrf_all_pipe_json/show_ip_arp_detail_vrf_all_pipe_json.txt",
        "ipv6": "cisco_nxos/show_ipv6_neighbor_vrf_all_pipe_json/show_ipv6_neighbor_vrf_all_pipe_json.txt",
    },
    "cisco_xr_arp": {
        "ipv4": "cisco_xr/show_arp_vrf_all/show_arp.txt",
        "ipv6": "cisco_xr/show_ipv6_neighbors/show_ipv6_neighbors.txt",
        "ipv4_interfaces": "cisco_xr/show_ipv4_vrf_all_interface_brief/show_ipv4_vrf_all_interface_brief.txt",
        "ipv6_interfaces": "cisco_xr/show_ipv6_vrf_all_interface_brief/show_ipv6_vrf_all_interface_brief.txt",
    },
    "fortinet_arp": {
        "ipv4": "fortinet/diagnose_ip_arp_list/diagnose_ip_arp_list.txt",
        "ipv6": "fortinet/diagnose_ipv6_neighbor_cache_list/diagnose_ipv6_neighbor_cache_list.txt",
        "interfaces": "fortinet/show_system_interface/show_system_interface.txt",
    },
    "juniper_junos_arp": {
        "ipv4": "juniper_junos/show_arp_no_resolve_pipe_display_json/show_arp_no_resolve_pipe_display_json.txt",
        "ipv6": "juniper_junos/show_ipv6_neighbors_pipe_display_json/show_ipv6_neighbors_pipe_display_json.txt",
        "instances": "juniper_junos/show_route_instance_detail_pipe_display_json/show_route_instance_detail_pipe_display_json.txt",
    },
    "linux_arp": {
        "neighbors": "linux/ip_neigh_show/ip_j_s_neigh_show.txt",
        "links": "linux/ip_link_show/ip_j_d_link_show.txt",
    },
}


def test_get_arp_inputs():
    parser = ttp(template=get_template(get="arp"))
    loaded = parser.get_input_load()
    assert set(INPUTS) <= set(loaded)


@pytest.mark.parametrize("template_name", sorted(INPUTS))
def test_get_arp(template_name):
    parser = ttp(template=get_template(get="arp"))
    for input_name, fixture in INPUTS[template_name].items():
        parser.add_input(
            (PLATFORM / fixture).read_text(encoding="utf-8"),
            input_name=input_name,
            template_name=template_name,
        )
    parser.parse()
    result = parser.result(structure="dictionary")
    expected = yaml.safe_load(
        (EXPECTED / f"{template_name}.yml").read_text(encoding="utf-8")
    )
    assert result[template_name] == expected


def test_get_arp_cisco_ios_vrf():
    # IOS doesn't name the VRF: the caller passes the one it read
    parser = ttp(template=get_template(get="arp"), vars={"vrf": "TTP-A"})
    for input_name, fixture in (
        ("ipv4", "cisco_ios/show_ip_arp/show_ip_arp_vrf.txt"),
        ("ipv6", "cisco_ios/show_ipv6_neighbors/show_ipv6_neighbors_vrf.txt"),
    ):
        parser.add_input(
            (PLATFORM / fixture).read_text(encoding="utf-8"),
            input_name=input_name,
            template_name="cisco_ios_arp",
        )
    parser.parse()
    result = parser.result(structure="dictionary")
    expected = yaml.safe_load(
        (EXPECTED / "cisco_ios_arp_vrf.yml").read_text(encoding="utf-8")
    )
    assert result["cisco_ios_arp"] == expected


@pytest.mark.parametrize(
    "template_vars, vrf", [({"vrf": "TTP-A"}, "TTP-A"), ({}, None)]
)
def test_parse_output_cisco_ios_vrf(template_vars, vrf):
    data = (PLATFORM / "cisco_ios/show_ip_arp/show_ip_arp_vrf.txt").read_text(
        encoding="utf-8"
    )
    result = parse_output(
        data, get="arp", platform="cisco_ios", template_vars=template_vars
    )
    assert len(result) == 4
    assert {r["vrf"] for r in result} == {vrf}


def test_incomplete_and_static_entries():
    # IOS-XE show ip arp lines: an unresolved entry and a configured one
    payload = {
        "ipv4": [
            {"ip": "192.0.2.99", "age": "0", "mac": "Incomplete"},
            {"ip": "192.0.2.77", "age": "-", "mac": "0011.2233.4455"},
        ]
    }
    assert transform_cisco_ios(payload) == [
        {
            "ip": "192.0.2.99",
            "mac": None,
            "interface": None,
            "vrf": None,
            "age": 0,
            "state": "incomplete",
        },
        {
            "ip": "192.0.2.77",
            "mac": "00:11:22:33:44:55",
            "interface": None,
            "vrf": None,
            "age": None,
            "state": "static",
        },
    ]


@pytest.mark.parametrize("address", ["ff02::16", "224.0.0.22", "0.0.0.0", "[Mcast"])
def test_not_neighbors(address):
    assert record(address, "33:33:00:00:00:16") is None
