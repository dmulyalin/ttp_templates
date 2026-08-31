"""Regression checks for generated MkDocs navigation."""

from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).parents[1]
DOCS_DIR = ROOT / "docs"


def _iter_nav_paths(node: Any) -> Iterable[str]:
    """Yield documentation paths from a nested MkDocs nav structure."""
    if isinstance(node, str):
        if node.endswith(".md"):
            yield node
    elif isinstance(node, list):
        for item in node:
            yield from _iter_nav_paths(item)
    elif isinstance(node, dict):
        for value in node.values():
            yield from _iter_nav_paths(value)


def test_generated_template_docs_match_navigation():
    """Generated template pages and nav entries must match exactly."""
    with (ROOT / "mkdocs.yml").open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    nav_paths = set(_iter_nav_paths(config["nav"]))
    missing = sorted(path for path in nav_paths if not (DOCS_DIR / path).is_file())
    assert not missing, f"MkDocs nav references missing pages: {missing}"

    generated_paths = {
        page.relative_to(DOCS_DIR).as_posix()
        for page in (DOCS_DIR / "ttp_templates").glob("*.md")
    }
    orphaned = sorted(generated_paths - nav_paths)
    assert not orphaned, f"Generated pages are absent from MkDocs nav: {orphaned}"
