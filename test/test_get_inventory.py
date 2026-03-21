import sys
import pprint


from ttp_templates import get_template
from ttp import ttp

def test_get_inventory():
    template = get_template(get="inventory")

    with open("./platform/cisco_xr/show_inventory/cisco_xr_show_inventory.txt", "r") as f:
        cisco_xr_data = f.read()

    parser = ttp(template=template)
    template_inputs = parser.get_input_load()
    print("\ntemplate_inputs:")
    pprint.pprint(template_inputs)

    assert all(
        k in template_inputs for k in [
            "arista_eos_inventory",
            "cisco_nxos_inventory",
            "cisco_xr_inventory",
            "juniper_junos_inventory",
        ]
    ), "Template inputs are wrong"

    parser.add_input(template_name="cisco_xr_inventory", data=cisco_xr_data)
    parser.parse()
    result = parser.result(structure="dictionary")

    print("\nParsing results:")
    pprint.pprint(result)
    assert result["cisco_xr_inventory"] and len(result["cisco_xr_inventory"]) > 0, "cisco_xr_inventory parsing results are wrong"