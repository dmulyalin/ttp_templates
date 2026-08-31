"""Invoke tasks for local development and CI-style checks."""

import os
import shlex
from pathlib import Path

import yaml
from invoke import Exit, task
from ttp import ttp

ROOT = Path(__file__).parent.resolve()
PYTHON_VERSIONS = ("3.10", "3.11", "3.12", "3.13", "3.14")
DOCKER_SERVICES = {
    version: f"py{version.replace('.', '')}" for version in PYTHON_VERSIONS
}
PAGE_TEMPLATE = """Reference path:
```
ttp://{path}
```

---

{doc}

---

<details><summary>Template Content</summary>
```
{template_content}
```
</details>"""


def _quote(value):
    value = str(value)
    if os.name == "nt":
        return '"' + value.replace('"', '\\"') + '"'
    return shlex.quote(value)


def _run(c, command, **kwargs):
    kwargs.setdefault("pty", os.name != "nt")
    return c.run(command, **kwargs)


def _ensure_docker(c):
    result = c.run("docker info", hide=True, warn=True)
    if result.ok:
        return

    raise Exit(
        "Docker is not running or is not reachable.\n"
        "Start Docker Desktop, wait until the Linux engine is ready, "
        "then run the Invoke Docker test task again.",
        code=1,
    )


def _pytest_args(extra):
    parts = ["-vv"]
    if extra:
        parts.append(extra)
    return " ".join(parts)


def _selected_versions(versions):
    selected = tuple(item.strip() for item in versions.split(",") if item.strip())
    return selected or PYTHON_VERSIONS


def _docker_service(version):
    try:
        return DOCKER_SERVICES[version]
    except KeyError as exc:
        supported = ", ".join(PYTHON_VERSIONS)
        raise Exit(
            f"Unsupported Python version {version!r}. Use one of: {supported}", code=1
        ) from exc


def _run_docker_tests(c, version, extra="", build=True):
    service = _docker_service(version)
    build_flag = "--build --quiet-build " if build else ""
    pytest_command = f"pytest {_pytest_args(extra)}"
    _run(
        c,
        f"docker compose run --rm {build_flag}{service} sh -lc {_quote(pytest_command)}",
    )


def _write(path, content, encoding="utf-8"):
    with open(path, "w", encoding=encoding) as handle:
        handle.write(content)


def _generate_docs():
    """Generate docs pages and refresh the Templates nav section."""
    misc = []
    misc_dict = {}
    platform = []
    yang = []
    get = [{"Getters Support Matrix": "getters_support_matrix.md"}]
    generated_docs = set()
    templates_count = 0

    with open("mkdocs.yml", "r", encoding="utf-8") as handle:
        mkdocs_yaml = yaml.safe_load(handle.read())

    for item in mkdocs_yaml["nav"]:
        if "Templates" in item:
            item["Templates"] = [
                {"Misc": misc},
                {"Platform": platform},
                {"YANG": yang},
                {"Getters": get},
            ]

    for dirpath, dirnames, filenames in os.walk(top="ttp_templates"):
        dirnames.sort()
        for filename in sorted(filenames):
            if filename == "readme.md":
                templates_count += 1
                generated_docs.add(_process_readme(dirpath, filename, misc_dict))
            elif filename.endswith(".txt"):
                templates_count += 1
                generated_docs.add(
                    _process_template(
                        dirpath, filename, misc_dict, platform, yang, get
                    )
                )

    # This directory contains generated pages only. Remove pages whose source
    # template was renamed or deleted after all current pages were generated.
    docs_dir = Path("docs") / "ttp_templates"
    for existing_page in docs_dir.glob("*.md"):
        if existing_page.name not in generated_docs:
            existing_page.unlink()

    for misc_dir_name, pages in misc_dict.items():
        misc.append({misc_dir_name: pages})

    _write("mkdocs.yml", yaml.dump(mkdocs_yaml, default_flow_style=False))
    _write_index(templates_count)


def _process_readme(dirpath, filename, misc_dict):
    filepath = Path(dirpath) / filename
    with open(filepath, encoding="utf-8") as handle:
        doc_string = handle.read()

    splitted_path = Path(dirpath).parts
    display_filename = ".".join(splitted_path[1:]) + "." + filename
    docs_filename = ".".join(splitted_path[1:]) + "." + filename.lower()
    _write(Path("docs") / "ttp_templates" / docs_filename, doc_string)

    if splitted_path[1] == "misc":
        misc_dict.setdefault(splitted_path[2], [])
        misc_dict[splitted_path[2]].append(
            {
                display_filename.split(".")[2] + ".readme": "ttp_templates/"
                + docs_filename
            }
        )

    return docs_filename


def _process_template(dirpath, filename, misc_dict, platform, yang, get):
    doc_string = ""
    filepath = Path(dirpath) / filename
    print(filepath)
    parser = ttp(template=str(filepath))
    for template in parser._templates:
        doc_string += "\n" + template.__doc__

    if doc_string.strip() == "":
        print("Template has no docs: {}".format(filepath))

    with open(filepath, encoding="utf-8") as handle:
        template_content = handle.read()

    splitted_path = Path(dirpath).parts
    display_filename = ".".join(splitted_path[1:]) + "." + filename.replace(
        ".txt", ".md"
    )
    docs_filename = ".".join(splitted_path[1:]) + "." + filename.lower().replace(
        ".txt", ".md"
    )
    doc_string = PAGE_TEMPLATE.format(
        path="/".join(splitted_path[1:]) + "/" + filename,
        doc=doc_string if doc_string.strip() else "No `<doc>` tags found",
        template_content=template_content.replace("`", "'"),
    )
    _write(Path("docs") / "ttp_templates" / docs_filename, doc_string)

    if splitted_path[1] == "misc":
        misc_dict.setdefault(splitted_path[2], [])
        misc_dict[splitted_path[2]].append(
            {
                ".".join(display_filename.split(".")[2:-1]): "ttp_templates/"
                + docs_filename
            }
        )
    elif splitted_path[1] == "platform":
        platform.append(
            {
                ".".join(display_filename.split(".")[1:-1]): "ttp_templates/"
                + docs_filename
            }
        )
    elif splitted_path[1] == "yang":
        yang.append(
            {
                ".".join(display_filename.split(".")[1:-1]): "ttp_templates/"
                + docs_filename
            }
        )
    elif splitted_path[1] == "get":
        get.append(
            {
                ".".join(display_filename.split(".")[1:-1]): "ttp_templates/"
                + docs_filename
            }
        )

    return docs_filename


def _write_index(templates_count):
    with open("README.md", encoding="utf-8") as readme_file:
        _write(
            "docs/index.md",
            """
---

**Templates count: {}**

---

{}""".format(
                templates_count,
                readme_file.read(),
            ),
        )


@task(
    help={
        "extra": "Additional pytest arguments, for example '-k inventory'.",
    }
)
def test(c, extra=""):
    """Run the test suite in the local Poetry environment."""
    with c.cd("test"):
        _run(c, f"poetry run pytest {_pytest_args(extra)}")


@task(
    help={
        "versions": "Comma-separated Python versions. Defaults to all supported versions.",
        "pull": "Pull newer base images while building.",
    }
)
def docker_build(c, versions="", pull=False):
    """Build cached Docker test images."""
    _ensure_docker(c)
    services = " ".join(
        _docker_service(version) for version in _selected_versions(versions)
    )
    pull_flag = "--pull " if pull else ""
    _run(c, f"docker compose build {pull_flag}{services}")


@task(
    help={
        "version": "Python Docker image version, for example 3.12.",
        "extra": "Additional pytest arguments passed inside the container.",
    }
)
def test_docker(c, version="3.12", extra=""):
    """Run tests in a single Python Docker Compose service."""
    _ensure_docker(c)
    _run_docker_tests(c, version=version, extra=extra)


@task(
    help={
        "versions": "Comma-separated Python versions. Defaults to all supported versions.",
        "extra": "Additional pytest arguments passed inside each container.",
    }
)
def test_docker_all(c, versions="", extra=""):
    """Run tests across all configured Python Docker Compose services."""
    _ensure_docker(c)
    selected_versions = _selected_versions(versions)
    docker_build(c, versions=",".join(selected_versions))
    for version in selected_versions:
        _run_docker_tests(c, version=version, extra=extra, build=False)


@task
def ruff(c):
    """Run Ruff lint and format checks."""
    _run(c, "poetry run ruff check .")
    _run(c, "poetry run ruff format --check tasks.py")


@task
def lint(c):
    """Run Python linting checks."""
    _run(
        c,
        "poetry run flake8 ttp_templates tasks.py --ignore=E501,E203,E402,F401,W503",
    )


@task
def vulture(c):
    """Run Vulture dead-code checks."""
    _run(c, "poetry run vulture")


@task
def docs(c):
    """Generate template documentation."""
    _generate_docs()


@task(pre=[ruff, lint, vulture, test])
def check(c):
    """Run local checks before pushing."""
    pass
