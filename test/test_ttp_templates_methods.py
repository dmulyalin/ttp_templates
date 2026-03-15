import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp_templates import parse_output
from ttp_templates import list_templates


def test_get_template_by_path():
    template = get_template(path="yang/ietf-interfaces_cisco_ios.txt")
    # print(template)
    assert isinstance(template, str)


# test_get_template()


def test_get_template_by_ttp_path_explicit():
    template = get_template(path="ttp://yang/ietf-interfaces_cisco_ios.txt")
    # print(template)
    assert isinstance(template, str)


# test_get_template()


def test_get_template_by_ttp_path_implicit():
    template = get_template("ttp://yang/ietf-interfaces_cisco_ios.txt")
    # print(template)
    assert isinstance(template, str)


# test_get_template_by_ttp_path_implicit()


def test_parse_output_platform():
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    result = parse_output(
        data=data, platform="Test Platform", command="show run | sec interface"
    )
    # pprint.pprint(result)
    assert result == [
        [
            [
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
            ]
        ]
    ]


# test_parse_output()


def test_parse_output_misc():
    data = """
r1# show run | sec interfaces
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.56 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
    """
    result = parse_output(
        data=data, misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt"
    )
    # pprint.pprint(result)
    assert result == [
        [
            {
                "description": "description",
                "hostname": "r1",
                "interface": "GigabitEthernet1",
                "ip": "10.223.89.55",
                "mask": "255.255.255.0",
                "vrf": "MGMT",
            },
            {
                "description": "description",
                "hostname": "r1",
                "interface": "GigabitEthernet1",
                "ip": "10.223.89.56",
                "mask": "255.255.255.0",
                "vrf": "MGMT",
            },
        ]
    ]


# test_parse_output_misc()


def test_parse_output_ttp_path():
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    result = parse_output(
        data=data, path="ttp://platform/test_platform_show_run_pipe_sec_interface.txt"
    )
    # pprint.pprint(result)
    assert result == [
        [
            [
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
            ]
        ]
    ]


# test_parse_output_ttp_path()


def test_parse_output_path():
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    result = parse_output(
        data=data, path="platform/test_platform_show_run_pipe_sec_interface.txt"
    )
    # pprint.pprint(result)
    assert result == [
        [
            [
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
                {
                    "description": "Customer #32148",
                    "disabled": True,
                    "dot1q": "251",
                    "interface": "GigabitEthernet1/3.251",
                    "ip": "172.16.33.10",
                    "mask": "255.255.255.128",
                },
            ]
        ]
    ]


# test_parse_output_path()


def test_get_template_path_traversal_raises():
    """get_template must reject paths that escape the package directory."""
    import pytest

    with pytest.raises(ValueError, match="resolves outside the package directory"):
        get_template(path="../../etc/passwd")


def test_get_template_misc_path_traversal_raises():
    """get_template must reject misc paths that escape the package directory."""
    import pytest

    with pytest.raises(ValueError, match="resolves outside the package directory"):
        get_template(misc="../../etc/shadow")


def test_short_interface_names_2ge_does_not_match_twohundred():
    """2GE patterns must not match TwoHundred* interface names (200GE)."""
    import re
    from ttp_templates.ttp_vars import short_interface_names

    two_ge_patterns = short_interface_names["2GE"]
    two_hundred_names = [
        "TwoHundredGigabitEthernet0/0/0",
        "TwoHundredGigEthernet0/0",
        "TwoHundredGigE0",
        "TwoHundredGig0",
    ]
    for name in two_hundred_names:
        for pattern in two_ge_patterns:
            assert (
                re.search(pattern, name) is None
            ), f"2GE pattern {pattern!r} incorrectly matched {name!r}"


def test_short_interface_names_2ge_does_not_match_twentyfive():
    """2GE patterns must not match TwentyFive* interface names (25GE)."""
    import re
    from ttp_templates.ttp_vars import short_interface_names

    two_ge_patterns = short_interface_names["2GE"]
    twenty_five_names = [
        "TwentyFiveGigabitEthernet0/0/0",
        "TwentyFiveGigEthernet0/0",
        "TwentyFiveGigE0",
        "TwentyFiveGig0",
    ]
    for name in twenty_five_names:
        for pattern in two_ge_patterns:
            assert (
                re.search(pattern, name) is None
            ), f"2GE pattern {pattern!r} incorrectly matched {name!r}"


def test_short_interface_names_2ge_matches_twogig():
    """2GE patterns must still match genuine TwoGigabitEthernet names."""
    import re
    from ttp_templates.ttp_vars import short_interface_names

    two_ge_patterns = short_interface_names["2GE"]
    two_gig_names = ["TwoGigabitEthernet0/0", "TwoGigE0", "Tw0/0"]
    for name in two_gig_names:
        matched = any(re.search(p, name) for p in two_ge_patterns)
        assert matched, f"No 2GE pattern matched genuine 2GE interface {name!r}"


def test_get_template_by_yang_and_platform():
    """get_template with yang+platform resolves the yang/ directory path."""
    template = get_template(yang="ietf-interfaces", platform="cisco_ios")
    assert isinstance(template, str)
    assert len(template) > 0


def test_get_template_yang_and_platform_names_normalised():
    """Spaces in platform and yang names must be normalised to underscores."""
    # "cisco ios" and "ietf interfaces" must resolve to the same file as the
    # canonical lowercase underscore-separated names.
    template_canonical = get_template(yang="ietf-interfaces", platform="cisco_ios")
    template_spaced = get_template(yang="ietf-interfaces", platform="cisco ios")
    assert template_canonical == template_spaced


def test_parse_output_yang_and_platform():
    """parse_output with yang+platform resolves the correct template."""
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    result = parse_output(data=data, yang="ietf-interfaces", platform="cisco_ios")
    assert isinstance(result, list)
    assert len(result) > 0


def test_parse_output_structure_flat_list():
    """parse_output honours the structure='flat_list' argument."""
    data = """
r1# show run | sec interfaces
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.1.1.1 255.255.255.0
interface GigabitEthernet2
 vrf forwarding MGMT
 ip address 10.1.2.1 255.255.255.0
    """
    result = parse_output(
        data=data,
        misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt",
        structure="flat_list",
    )
    assert isinstance(result, list)
    # flat_list collapses nesting – every element must be a dict
    assert all(isinstance(item, dict) for item in result)


def test_parse_output_template_vars_accepted():
    """parse_output must accept and pass template_vars without error."""
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    # Empty dict and a populated dict must both be accepted without raising
    result_empty = parse_output(
        data=data,
        path="platform/test_platform_show_run_pipe_sec_interface.txt",
        template_vars={},
    )
    assert isinstance(result_empty, list)

    result_none = parse_output(
        data=data,
        path="platform/test_platform_show_run_pipe_sec_interface.txt",
        template_vars=None,
    )
    assert isinstance(result_none, list)


def test_get_template_no_args_returns_none():
    """get_template with no arguments must return None, not raise."""
    result = get_template()
    assert result is None


def test_parse_output_no_args_raises_value_error():
    """parse_output with no template-locating argument must raise ValueError."""
    import pytest

    with pytest.raises(ValueError, match="no valid template-locating argument"):
        parse_output(data="some text")


def test_list_templates_misc_root_file_no_crash():
    """list_templates must not crash when a file sits directly inside misc/."""
    import os as _os
    import ttp_templates.ttp_templates as mod
    from unittest.mock import patch

    pkg_dir = _os.path.abspath(_os.path.dirname(mod.__file__))
    misc_dir = _os.path.join(pkg_dir, "misc")
    platform_dir = _os.path.join(pkg_dir, "platform")
    yang_dir = _os.path.join(pkg_dir, "yang")

    def fake_walk(dirname):
        if dirname == misc_dir:
            # misc/ contains both a direct file and a subdirectory with a file
            yield misc_dir, ["SubDir"], ["root_template.txt"]
            yield _os.path.join(misc_dir, "SubDir"), [], ["cisco.txt"]
        elif dirname == platform_dir:
            yield platform_dir, [], []
        elif dirname == yang_dir:
            yield yang_dir, [], []

    with patch.object(mod.os, "walk", side_effect=fake_walk):
        res = list_templates()

    assert isinstance(res["misc"], dict), "misc must remain a dict, not a list"
    assert "SubDir" in res["misc"], "subdirectory entries must still be present"
    # files placed directly in misc/ are stored under the empty-string key
    assert res["misc"][""] == ["root_template.txt"]


def test_list_templates_files_are_sorted():
    """list_templates must return files in sorted (deterministic) order."""
    res = list_templates()
    assert res["platform"] == sorted(res["platform"])
    assert res["yang"] == sorted(res["yang"])
    for subtree in res["misc"].values():
        if isinstance(subtree, list):
            assert subtree == sorted(subtree)
        elif isinstance(subtree, dict):
            for files in subtree.values():
                if isinstance(files, list):
                    assert files == sorted(files)


def test_list_templates_all():
    res = list_templates()
    pprint.pprint(res)
    assert all(k in res for k in ["platform", "yang", "misc"])
    assert isinstance(res["misc"], dict)


# test_list_templates_all()


def test_list_templates_with_filter_match():
    res = list_templates(pattern="*cisco*")
    pprint.pprint(res)
    assert all(k in res for k in ["platform", "yang", "misc"])
    assert isinstance(res["misc"], dict)
    assert all("cisco" in t for t in res["platform"])
    assert all("cisco" in t for t in res["yang"])


# test_list_templates_with_filter_match()


def test_list_templates_with_filter_no_match():
    res = list_templates(pattern="*cisco12345*")
    pprint.pprint(res)
    assert all(k in res for k in ["platform", "yang", "misc"])
    assert isinstance(res["misc"], dict) and res["misc"] != {}
    assert all(res[k] == [] for k in ["platform", "yang"])


# test_list_templates_with_filter_no_match()
