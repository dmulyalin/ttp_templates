import logging
import os
from fnmatch import fnmatchcase
from typing import Dict, List, Optional, Union

from ttp import ttp

log = logging.getLogger(__name__)


def get_template(
    path: Optional[str] = None,
    platform: Optional[str] = None,
    command: Optional[str] = None,
    yang: Optional[str] = None,
    misc: Optional[str] = None,
) -> Optional[str]:
    """Locate a template file and return its content.

    ``path`` argument is always preferred over other arguments.

    Valid combinations of template location arguments:

    * ``path="./misc/foo/bar.txt"``
    * ``platform="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``

    Args:
        path: OS path or ``ttp://`` URI to the template file to load.
        platform: Platform name to load the template for, e.g. ``cisco_ios``.
        command: CLI command to load the template for, e.g. ``show ip arp``.
        yang: YANG module name to load the template for, e.g. ``ietf-interfaces``.
        misc: Path to the template relative to the repository ``misc`` folder.

    Returns:
        Template file content as a string, or ``None`` if no valid argument
        combination was provided.
    """
    # resolve the relative path to the template file based on provided arguments
    if path:
        # strip the optional "ttp://" scheme prefix used by TTP library
        if path.strip().startswith("ttp://"):
            path = path.strip()[6:]
        log.debug("get_template: using explicit path '%s'", path)
    elif platform and command:
        platform = platform.lower()
        command = command.lower()
        # replace pipe symbol with the word "pipe" to form a valid filename
        command = command.replace("|", "pipe")
        for symbol in [" ", "-"]:
            platform = platform.replace(symbol, "_")
            command = command.replace(symbol, "_")
        path = "platform/{}_{}.txt".format(platform, command)
        log.debug("get_template: resolved platform+command path '%s'", path)
    elif platform and yang:
        platform = platform.lower()
        yang = yang.lower()
        for symbol in [" "]:
            platform = platform.replace(symbol, "_")
            yang = yang.replace(symbol, "_")
        path = "yang/{}_{}.txt".format(yang, platform)
        log.debug("get_template: resolved yang+platform path '%s'", path)
    elif misc:
        path = "misc/{}".format(misc)
        log.debug("get_template: resolved misc path '%s'", path)
    else:
        log.warning(
            "get_template: no valid argument combination provided, "
            "returning None"
        )
        return None

    template_dir = os.path.abspath(os.path.dirname(__file__))
    template_filename = os.path.join(template_dir, path)

    log.debug("get_template: loading template file '%s'", template_filename)

    # read and return the template file content
    with open(template_filename, mode="r", encoding="utf-8") as f:
        content = f.read()

    log.debug(
        "get_template: loaded template '%s', %d characters",
        template_filename,
        len(content),
    )
    return content


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
    """Load a template and parse the provided data string with TTP.

    ``path`` argument is always preferred over other arguments.

    Valid combinations of template location arguments:

    * ``path="./misc/foo/bar.txt"``
    * ``platform="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``

    Args:
        data: Raw text data to parse.
        path: OS path or ``ttp://`` URI to the template file to load.
        platform: Platform name to load the template for, e.g. ``cisco_ios``.
        command: CLI command to load the template for, e.g. ``show ip arp``.
        yang: YANG module name to load the template for, e.g. ``ietf-interfaces``.
        misc: Path to the template relative to the repository ``misc`` folder.
        structure: Output structure format - ``list``, ``dictionary``, or
            ``flat_list``.
        template_vars: Additional variables to pass into the TTP template object.

    Returns:
        Parsed results as a dict or list, depending on the ``structure`` argument.
    """
    template_vars = template_vars or {}

    log.debug(
        "parse_output: loading template (platform=%r, command=%r, "
        "path=%r, yang=%r, misc=%r)",
        platform,
        command,
        path,
        yang,
        misc,
    )

    # retrieve the template text using the provided locator arguments
    template = get_template(
        platform=platform, command=command, path=path, yang=yang, misc=misc
    )

    log.debug("parse_output: creating TTP parser, structure=%r", structure)

    # instantiate the TTP parser with the data and template
    parser = ttp(data=data, template=template, vars=template_vars)

    # run the parse pass and collect results
    parser.parse(one=True)
    results = parser.result(structure=structure)

    log.debug("parse_output: parsing complete")
    return results


def list_templates(pattern: str = "*") -> Dict:
    """List available templates whose filenames match the given glob pattern.

    The primary use case for this function is to simplify integration with
    other applications by providing a programmatic API to enumerate all
    available TTP templates.

    Args:
        pattern: Glob pattern used to filter template filenames. Defaults to
            ``"*"`` which matches all templates.

    Returns:
        Dictionary with three top-level keys:

        * ``platform`` - list of matching platform template filenames.
        * ``yang`` - list of matching YANG template filenames.
        * ``misc`` - nested dict mirroring the ``misc/`` directory hierarchy,
          with leaf values being lists of matching filenames.
    """
    res: Dict = {
        "platform": [],
        "yang": [],
        "misc": {},
    }
    # filenames to exclude regardless of the caller's pattern
    skip_files = ["readme.md"]
    paths = ["platform", "yang", "misc"]
    ttp_templates_dir = os.path.abspath(os.path.dirname(__file__))

    log.debug("list_templates: scanning '%s' with pattern '%s'", ttp_templates_dir, pattern)

    for path in paths:
        dirname = os.path.join(ttp_templates_dir, path)
        for dirpath, dirnames, filenames in os.walk(dirname):
            # build a list of folder names relative to the package root
            # e.g. "/platform" → ["platform"], "/misc/N2G/cli_ip_data" → ["misc", "N2G", "cli_ip_data"]
            dirpath_items = dirpath.replace(ttp_templates_dir, "").split(os.sep)[1:]

            # skip directories that contain no files
            if not filenames:
                continue

            # keep only files that match the caller's glob pattern and are not in the skip list
            files = [
                filename
                for filename in filenames
                if (
                    fnmatchcase(filename, pattern)
                    and filename.lower() not in skip_files
                )
            ]

            log.debug(
                "list_templates: dir '%s' → %d/%d files match pattern",
                dirpath,
                len(files),
                len(filenames),
            )

            # traverse the result dict to the correct nesting level and store the file list
            ref = res
            for index, item in enumerate(dirpath_items):
                if index + 1 == len(dirpath_items):
                    # we have reached the leaf directory: store the files list here
                    ref[item] = files
                else:
                    # descend one level deeper, creating intermediate dicts as needed
                    ref = ref.setdefault(item, {})

    log.debug("list_templates: scan complete")
    return res
