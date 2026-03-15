"""
conftest.py — auto-discovers platform template test cases.

Layout expected under test/platform/:

    test/platform/
        <platform>/               e.g. cisco_xr
            <command_slug>/       e.g. show_inventory  (underscores = spaces in CLI command)
                <sample>.txt      raw CLI output
                <sample>.yml      expected TTP result (flat_list by default)
                settings.yml      (optional) per-command overrides, e.g. structure: list

Adding a new .txt/.yml pair is enough to create a new test — no code changes needed.
"""

import yaml
import pytest
from pathlib import Path

_PLATFORM_DIR = Path(__file__).parent / "platform"


def _collect_platform_cases():
    """Walk test/platform/ and return a list of pytest.param objects."""
    cases = []

    if not _PLATFORM_DIR.is_dir():
        return cases

    for platform_dir in sorted(_PLATFORM_DIR.iterdir()):
        if not platform_dir.is_dir():
            continue
        platform = platform_dir.name

        for command_dir in sorted(platform_dir.iterdir()):
            if not command_dir.is_dir():
                continue

            command_slug = command_dir.name
            # Folder name uses underscores; CLI command uses spaces.
            # e.g. show_inventory -> "show inventory"
            command = command_slug.replace("_", " ")

            # Optional per-command settings file.
            settings_file = command_dir / "settings.yml"
            settings: dict = {}
            if settings_file.exists():
                with settings_file.open(encoding="utf-8") as fh:
                    settings = yaml.safe_load(fh) or {}

            structure = settings.get("structure", "flat_list")

            # Pair every .txt file with a same-stem .yml file.
            for txt_file in sorted(command_dir.glob("*.txt")):
                yml_file = txt_file.with_suffix(".yml")
                if not yml_file.exists():
                    continue

                test_id = f"{platform}__{command_slug}__{txt_file.stem}"
                cases.append(
                    pytest.param(
                        # Wrapped as a single tuple so the fixture receives one value.
                        (platform, command, txt_file, yml_file, structure),
                        id=test_id,
                    )
                )

    return cases


def pytest_generate_tests(metafunc):
    """Parametrize any test that declares a ``platform_test_case`` fixture."""
    if "platform_test_case" in metafunc.fixturenames:
        cases = _collect_platform_cases()
        metafunc.parametrize("platform_test_case", cases)
