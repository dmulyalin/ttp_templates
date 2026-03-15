"""
test_platform_dynamic.py — data-driven platform template tests.

Each test case is a (.txt, .yml) pair discovered automatically by conftest.py
from the test/platform/ directory tree. No changes to this file are needed
when new sample files are added.

To add a test:
    1. Put raw CLI output in  test/platform/<platform>/<command_slug>/<name>.txt
    2. Put expected result in  test/platform/<platform>/<command_slug>/<name>.yml
       (YAML list of dicts matching TTP flat_list output)
    3. Optionally add a settings.yml in the command folder to override defaults.

Run:
    cd test && poetry run pytest test_platform_dynamic.py -vv
"""

import sys
import yaml

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp


def test_platform_template(platform_test_case):
    """Parse a raw CLI sample and assert the result matches the reference YAML."""
    platform, command, txt_path, yml_path, structure = platform_test_case

    raw_data = txt_path.read_text(encoding="utf-8")

    with yml_path.open(encoding="utf-8") as fh:
        expected = yaml.safe_load(fh)

    template = get_template(platform=platform, command=command)
    assert template is not None, (
        f"No TTP template found for platform={platform!r}, command={command!r}. "
        f"Check that ttp_templates/platform/{platform}_{command.replace(' ', '_')}.txt exists."
    )

    parser = ttp(data=raw_data, template=template)
    parser.parse()
    result = parser.result(structure=structure)

    assert result == expected, (
        f"\n>>> FAILED     : platform={platform!r}, command={command!r}"
        f"\n>>> INPUT FILE : {txt_path}"
        f"\n>>> EXPECTED   : {expected}"
        f"\n>>> GOT        : {result}"
    )
