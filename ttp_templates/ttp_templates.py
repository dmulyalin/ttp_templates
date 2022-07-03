import os
from ttp import ttp
from typing import Optional, List, Dict, Union
from fnmatch import fnmatchcase


def get_template(
    path: Optional[str] = None,
    platform: Optional[str] = None,
    command: Optional[str] = None,
    yang: Optional[str] = None,
    misc: Optional[str] = None,
) -> str:
    """
    Function to locate template file and return it's content

    **Valid combinations of template location**

    ``path`` attribute is always more preferred

    * ``path="./misc/foo/bar.txt"``
    * ``platform="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``

    :param path: OS path to template to load
    :param platform: name of the platform to load template for
    :param command: command to load template for
    :param yang: name of YANG module to load template for
    :param misc: OS path to template within repository misc folder
    """
    # form path to template file
    if path:
        if path.strip().startswith("ttp://"):
            path = path.strip()[6:]
    elif platform and command:
        platform = platform.lower()
        command = command.lower()
        command = command.replace("|", "pipe")
        for symbol in [" ", "-"]:
            platform = platform.replace(symbol, "_")
            command = command.replace(symbol, "_")
        path = "platform/{}_{}.txt".format(platform, command)
    elif platform and yang:
        platform = platform.lower()
        yang = yang.lower()
        for symbol in [" "]:
            platform = platform.replace(symbol, "_")
            yang = yang.replace(symbol, "_")
        path = "yang/{}_{}.txt".format(yang, platform)
    elif misc:
        path = "misc/{}".format(misc)
    else:
        return None

    template_dir = os.path.abspath(os.path.dirname(__file__))
    template_filename = os.path.join(template_dir, path)

    # open template file and return content
    with open(template_filename, mode="r", encoding="utf-8") as f:
        return f.read()


def parse_output(
    data: str,
    platform: Optional[str] = None,
    command: Optional[str] = None,
    path: Optional[str] = None,
    yang: Optional[str] = None,
    misc: Optional[str] = None,
    structure: Optional[str] = "list",
    template_vars: Optional[Dict] = None,
) -> Union[Dict, List]:
    """
    Function to load template text and parse data provided

    **Valid combinations of template location**

    ``path`` attribute is always more preferred

    * ``path="./misc/foo/bar.txt"``
    * ``platform="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``

    :param data: data to parse
    :param path: OS path to template to load
    :param platform: name of the platform to load template for
    :param command: command to load template for
    :param yang: name of YANG module to load template for
    :param misc: OS path to template within repository misc folder
    :param structure: results structure list, dictionary or flat_list
    :param template_vars: variables to load in template object
    """
    template_vars = template_vars or {}
    # get template text
    template = get_template(
        platform=platform, command=command, path=path, yang=yang, misc=misc
    )

    # create parser object
    parser = ttp(data=data, template=template, vars=template_vars)

    # parse and return results
    parser.parse(one=True)
    return parser.result(structure=structure)


def list_templates(pattern: str = "*") -> dict:
    """
    Function to list available templates matching given pattern.

    Primary usecase for this function is to simplify integration with
    other applications by providing API interface to list available
    TTP templates.

    :param pattern: glob pattern to filter templates by name
    :param return: dictionary with platform, yang and misc keys
    """
    res = {
        "platform": [],
        "yang": [],
        "misc": {},
    }
    skip_files = ["readme.md"]
    paths = ["platform", "yang", "misc"]
    ttp_templates_dir = os.path.abspath(os.path.dirname(__file__))

    for path in paths:
        dirname = os.path.join(ttp_templates_dir, path)
        for dirpath, dirnames, filenames in os.walk(dirname):
            # get a list of parent folders names for current folder
            dirpath_items = dirpath.replace(ttp_templates_dir, "").split(os.sep)[1:]
            # skip if no files in folder
            if not filenames:
                continue
            # filter files
            files = [
                filename
                for filename in filenames
                if (
                    fnmatchcase(filename, pattern)
                    and filename.lower() not in skip_files
                )
            ]
            # descend down dirpath_items in res and save files list
            ref = res
            for index, item in enumerate(dirpath_items):
                # check if last item and save files list
                if index + 1 == len(dirpath_items):
                    ref[item] = files
                # create item key in res and obtain reference to its value
                else:
                    ref = ref.setdefault(item, {})
    return res
