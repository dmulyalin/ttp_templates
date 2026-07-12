import sys
import pprint
from pathlib import Path


from ttp_templates import get_template
from ttp import ttp


TEST_DIR = Path(__file__).parent


def test_get_inventory():
    template = get_template(get="inventory")

    cisco_xr_data = (
        TEST_DIR / "platform/cisco_xr/show_inventory/cisco_xr_show_inventory.txt"
    ).read_text(encoding="utf-8")
    cisco_nxos_data = (
        TEST_DIR
        / "platform/cisco_nxos/show_inventory_pipe_json_pretty/show_inventory_pipe_json_pretty.txt"
    ).read_text(encoding="utf-8")
    cisco_ios_data = (
        TEST_DIR / "platform/cisco_ios/show_inventory/show_inventory.txt"
    ).read_text(encoding="utf-8")
    a10_data = (TEST_DIR / "platform/a10/show_hardware/show_hardware.txt").read_text(
        encoding="utf-8"
    )

    parser = ttp(template=template)
    template_inputs = parser.get_input_load()
    print("\ntemplate_inputs:")
    pprint.pprint(template_inputs)

    assert all(
        k in template_inputs for k in [
            "arista_eos_inventory",
            "a10_show_hardware",
            "cisco_ios_inventory",
            "cisco_nxos_inventory",
            "cisco_xr_inventory",
            "juniper_junos_inventory",
        ]
    ), "Template inputs are wrong"

    parser.add_input(template_name="cisco_xr_inventory", data=cisco_xr_data)
    parser.add_input(template_name="cisco_ios_inventory", data=cisco_ios_data)
    parser.add_input(template_name="cisco_nxos_inventory", data=cisco_nxos_data)
    parser.add_input(template_name="a10_show_hardware", data=a10_data)
    parser.parse()
    result = parser.result(structure="dictionary")

    print("\nParsing results:")
    pprint.pprint(result)
    assert result["cisco_xr_inventory"] and len(result["cisco_xr_inventory"]) > 0, (
        "cisco_xr_inventory parsing results are wrong"
    )
    assert result["cisco_nxos_inventory"] == [
        {
            "description": "Nexus 31108TCV Chassis",
            "module": "N3K-C31108TC-V",
            "serial": "12424121414124",
            "slot": "Chassis",
        },
        {
            "description": "48x1/10G-T 6x40/100G QSFP28 Ethernet Module",
            "module": "N3K-C31108TC-V",
            "serial": "12424121414124",
            "slot": "Slot 1",
        },
        {
            "description": "Nexus 31108TCV Chassis Power Supply",
            "module": "NXA-PAC-650W-PE",
            "serial": "rggrgrwgrgwrgr",
            "slot": "Power Supply 1",
        },
        {
            "description": "Nexus 31108TCV Chassis Power Supply",
            "module": "NXA-PAC-650W-PE",
            "serial": "45gereryt3",
            "slot": "Power Supply 2",
        },
    ], "cisco_nxos_inventory parsing results are wrong"
    assert result["cisco_ios_inventory"] == [
        {
            "description": "3640 chassis",
            "module": "",
            "serial": "FF1045C5",
            "slot": "3640 chassis",
        },
        {
            "description": "One port Fastethernet TX",
            "module": "NM-1FE-TX=",
            "serial": "7720321",
            "slot": "One port Fastethernet TX",
        },
        {
            "description": "One port Fastethernet TX",
            "module": "NM-1FE-TX=",
            "serial": "7720321",
            "slot": "One port Fastethernet TX",
        },
        {
            "description": "One port Fastethernet TX",
            "module": "NM-1FE-TX=",
            "serial": "7720321",
            "slot": "One port Fastethernet TX",
        },
    ], "cisco_ios_inventory parsing results are wrong"
    assert result["a10_show_hardware"] == [
        {
            "description": "Thunder Series Unified Application Service Gateway",
            "module": "TH1234",
            "serial": "gfnggfndngdfgf",
            "slot": "chassis",
        }
    ], "a10_show_hardware parsing results are wrong"
