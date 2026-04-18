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
    get: Optional[str] = None,
) -> Optional[str]:
    """Locate a template file and return its content.

    ``path`` argument is always preferred over other arguments.

    Valid combinations of template location arguments:

    * ``path="./misc/foo/bar.txt"``
    * ``platform="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``
    * ``get="foo_folder/bar_template.txt"``

    Args:
        path: OS path or ``ttp://`` URI to the template file to load.
        platform: Platform name to load the template for, e.g. ``cisco_ios``.
        command: CLI command to load the template for, e.g. ``show ip arp``.
        yang: YANG module name to load the template for, e.g. ``ietf-interfaces``.
        misc: Path to the template relative to the repository ``misc`` folder.
        get: Name of the getter template e.g. "inventory"

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
    elif get:
        path = (
            "get/{}".format(get) if get.endswith(".txt") else "get/{}.txt".format(get)
        )
        log.debug("get_template: resolved get path '%s'", path)
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
            "get_template: no valid argument combination provided, " "returning None"
        )
        return None

    template_dir = os.path.abspath(os.path.dirname(__file__))
    # Resolve symlinks and ".." segments so the containment check is reliable
    template_filename = os.path.realpath(os.path.join(template_dir, path))

    # Ensure the resolved path stays inside the package directory to prevent
    # path-traversal attacks (e.g. path="../../etc/passwd").
    if not template_filename.startswith(template_dir + os.sep):
        raise ValueError(
            f"Template path '{path}' resolves outside the package directory."
        )

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
    get: Optional[str] = None,
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
    * ``get="inventory", platform="cisco_xr"``

    Args:
        data: Raw text data to parse.
        path: OS path or ``ttp://`` URI to the template file to load.
        platform: Platform name to load the template for, e.g. ``cisco_ios``.
            **Required** when ``get`` is used — it selects the platform-specific
            input inside the getter template (e.g. ``"cisco_xr"``, ``"arista_eos"``).
        command: CLI command to load the template for, e.g. ``show ip arp``.
        yang: YANG module name to load the template for, e.g. ``ietf-interfaces``.
        misc: Path to the template relative to the repository ``misc`` folder.
        get: Name of the getter template, e.g. ``"inventory"``. Works similarly to
            NAPALM getters — a single getter bundles platform-specific parsing logic
            and returns a normalized, platform-agnostic structure. ``platform`` must
            also be supplied so the correct input section is selected.
        structure: Output structure format - ``list``, ``dictionary``, or
            ``flat_list``.
        template_vars: Additional variables to pass into the TTP template object.

    Returns:
        Parsed results as a dict or list, depending on the ``structure`` argument.

    Raises:
        ValueError: If no valid template-locating argument combination is provided,
            or if ``get`` is used without ``platform``.
        RuntimeError: If ``get`` is used and none of the getter's inputs support
            the specified ``platform``.
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
        platform=platform, command=command, path=path, yang=yang, misc=misc, get=get
    )

    if template is None:
        raise ValueError(
            "parse_output: no valid template-locating argument combination was "
            "provided; supply one of: path, platform+command, yang+platform, or misc."
        )

    log.debug("parse_output: creating TTP parser, structure=%r", structure)

    # handle getter if platform is given
    if get:
        if not platform:
            raise ValueError(
                f"'{get}' getter need platform name to parse provided data"
            )
        parser = ttp(template=template, vars=template_vars)
        # sort input data across inputs
        input_found = False
        for template_name, inputs in parser.get_input_load().items():
            for input_name, params in inputs.items():
                if platform in params.get("platform", []):
                    parser.add_input(
                        template_name=template_name, input_name=input_name, data=data
                    )
                    input_found = True
                    break
            if input_found:
                break
        else:
            raise RuntimeError(
                f"None of the '{get}' getter inputs support platform '{platform}'"
            )
        # parse the data and return result only for template with matched input
        parser.parse(one=True)
        results = parser.result(structure="dictionary")
        results = results[template_name]
    else:
        # parse the data
        parser = ttp(data=data, template=template, vars=template_vars)
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
        "get": [],
    }
    # filenames to exclude regardless of the caller's pattern
    skip_files = ["readme.md"]
    paths = ["platform", "yang", "misc", "get"]
    ttp_templates_dir = os.path.abspath(os.path.dirname(__file__))

    log.debug(
        "list_templates: scanning '%s' with pattern '%s'", ttp_templates_dir, pattern
    )

    for path in paths:
        dirname = os.path.join(ttp_templates_dir, path)
        for dirpath, dirnames, filenames in os.walk(dirname):
            # build a list of folder names relative to the package root
            # e.g. "/platform" → ["platform"], "/misc/N2G/cli_ip_data" → ["misc", "N2G", "cli_ip_data"]
            dirpath_items = dirpath.replace(ttp_templates_dir, "").split(os.sep)[1:]

            # skip directories that contain no files
            if not filenames:
                continue

            # keep only files that match the caller's glob pattern and are not in the skip list;
            # sort the result so the output is deterministic regardless of filesystem ordering
            files = sorted(
                filename
                for filename in filenames
                if (
                    fnmatchcase(filename, pattern)
                    and filename.lower() not in skip_files
                )
            )

            # traverse the result dict to the correct nesting level and store the file list
            ref = res
            for index, item in enumerate(dirpath_items):
                if index + 1 == len(dirpath_items):
                    # Reached the leaf directory: store the matching files list.
                    # Guard against overwriting an existing sub-dict, which would
                    # happen if a template file sits directly inside misc/ alongside
                    # subdirectories (e.g. misc/my_template.txt).  In that case we
                    # store the files under the empty-string key so the dict
                    # structure is preserved and subsequent iterations don't crash.
                    if isinstance(ref.get(item), dict):
                        ref[item][""] = files
                    else:
                        ref[item] = files
                else:
                    # descend one level deeper, creating intermediate dicts as needed
                    ref = ref.setdefault(item, {})

    log.debug("list_templates: scan complete")
    return res


def list_templates_refs(pattern: str = "*") -> list:
    """Return a flat list of ``ttp://`` references for all matching templates.

    Each entry uses the ``ttp://`` URI scheme understood by :func:`get_template`  e.g.:

    * ``ttp://platform/cisco_ios_show_ip_arp.txt``
    * ``ttp://misc/N2G/cli_ip_data/cisco_ios.txt``

    Args:
        pattern: Glob pattern used to filter template filenames.

    Returns:
        Sorted list of ``ttp://`` URI strings for all matching templates.
    """
    skip_files = ["readme.md"]
    paths = ["platform", "yang", "misc", "get"]
    ttp_templates_dir = os.path.abspath(os.path.dirname(__file__))
    refs: list = []

    for path in paths:
        dirname = os.path.join(ttp_templates_dir, path)
        for dirpath, _dirnames, filenames in os.walk(dirname):
            # path relative to the package root, using forward slashes for the URI
            rel_dir = os.path.relpath(dirpath, ttp_templates_dir).replace(os.sep, "/")
            for filename in filenames:
                if (
                    fnmatchcase(filename, pattern)
                    and filename.lower() not in skip_files
                ):
                    refs.append("ttp://{}/{}".format(rel_dir, filename))

    log.debug("list_templates_refs: found %d refs", len(refs))
    return sorted(refs)
