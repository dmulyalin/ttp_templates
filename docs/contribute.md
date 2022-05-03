# Contribute

There are several things you can do to help TTP Templates project.

* Spread the word about TTP and TTP Templates
* Suggest great features and ideas
* Report bugs
* Fix typos in code, templates and documentation
* Write documentation
* Contribute new templates
* Improve existing templates

## Contribute Templates by Opening GitHub Issue

Open [GitHub issue](https://github.com/dmulyalin/ttp_templates/issues) using 
`Contribute Template` type and fill in required details.

## Contribute Templates by Pull Request

Before you start, make sure to think of for each template:

* Template Category and Template Name
* Template Content
* Sample Data
* Expected Output

*Sample Data* and *Expected Output* used to compose template test.

*Template Content* placed in one of *Template Category* folder below using *Template Name* as a filename:

* `platform` category - mimics [ntc-templates](https://github.com/networktocode/ntc-templates) 
  API and follows same naming rule - `{{ vendor_os }}_{{ command_with_underscores }}.txt` - lower case only
* `yang` category - contains templates capable of producing YANG compatible structures out of text data,
  and uses naming rule - `{{ YANG module name }}_{{ platform_name }}.txt` - lower case only
* `misc` category - miscellaneous templates for various use cases organized in folders, naming
  rule is - `{{ usecase folder }}/{{ template name }}.txt` - upper or lower case

To prepare your working environment might need to install required packages using requirements 
files located in TTP Templates repository e.g.:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pip install -r requirements-docs.txt
```

To add new template or multiple templates follow these steps:

1. Fork [TTP Templates](https://github.com/dmulyalin/ttp_templates) repository to your GitHub account
2. Git clone forked TTP Templates repository to your local machine
3. Add new TTP template file to `ttp_templates/platform/`, `ttp_templates/misc/<usecase>/` or 
   `ttp_templates/yang/` folder
4. Add [PyTest](https://pypi.org/project/pytest/) tests under `test` folder inside one of the existing 
   files or create new file, might be good to look at existing tests for ideas on how to test the template
5. Generate documentation using [Writing Docs guide](writing_docs.md), omitting `gh-deploy` portion
6. Commit changes and push them to GitHub
7. Raise GitHub pull request to merge your changes into TTP Templates repository

## Writing TTP Templates Tests

TTP templates use [PyTest](https://pypi.org/project/pytest/) for testing.

Composing tests is fairly straightforward once you figured out TTP template content, sample data
and expected output. 

Assuming template category is `platform`, platform name `cisco_ios`, template filename is 
`ttp_templates/platform/cisco_ios_show_running_config_pipe_section_interface.txt` and template 
content is:

```
<doc>
Author: Author Name
Contact: Contact Details
Version: 0.1.0

Template to produce list of dictionaries with interface configuration details using 
Cisco IOSXE "show running-config | section interface" command output.

The exact command is "show running-config" and not "show running-configuration",
as it is changed in later versions of IOSXE.
</doc>

<group>
interface {{ interface }}
 description {{ description | ORPHRASE }}
 ip address {{ ip }} {{ mask }}
! {{ _end_ }}
</group>
```

test to validate above template might look like this:

```python
import sys
import pprint

sys.path.insert(0, "..")

from ttp_templates import get_template
from ttp import ttp

def test_cisco_ios_show_run_pipe_section_interface():
    data = """
interface Loopback0
 description RID loopback
 ip address 192.168.31.44 255.255.255.255
!
    """
    expected_output = [
        [
            {
                "description": "RID loopback",
                "interface": "Loopback0",
                "ip": "192.168.31.44",
                "mask": "255.255.255.255"
            }
        ]
    ]
    template = get_template(platform="cisco_ios", command="show running-config | section interface")
    parser = ttp(data=data, template=template)
    parser.parse()
    res = parser.result()
    assert res == expected_output
```

That test can be placed inside `test_platform_cisco_ios.py` file and run using command:

```bash
pytest -vv test_platform_cisco_ios::test_cisco_ios_show_run_pipe_section_interface
```
