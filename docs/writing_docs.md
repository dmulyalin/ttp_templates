# Writing docs for TTP Templates

TTP Templates have `<doc>` tag that can be used to embed documentation strings into the templates.

Templates `<doc>` tags content is just a text, but TTP Templates documentation assumes markdown
syntaxes used to populate docs.

TTP Templates use [mkdocs](https://www.mkdocs.org) with [material theme](https://squidfunk.github.io/mkdocs-material/) 
to produce documentation. 

TTP Templates Collection comes with `generate_docs.py` script, this script iterates over all
folders within `ttp_templates` repository, loads templates and extracts `<doc>` tags content
to form `.md` files, saves `.md` files in `docs/ttp_templates` folder and construct navigation tree 
within `mkdocs.yml` file.

## Generating Documentation

First, need to write docs within the templates.

Next, generate `.md` doc files out of TTP templates:

```
python3 generate_docs.py
```

Finally, use `mkdocs` to serve, build or deploy docs using commands:

* `mkdocs serve` - serve docs locally to view docs content via browser
* `mkdocs build` - build docs
* `mkdocs gh-deploy` - deploy docs to GitHub