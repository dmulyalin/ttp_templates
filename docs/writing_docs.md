# Writing docs for TTP Templates

TTP Templates have `<doc>` tag that can be used to embed documentation strings into the templates.

Templates `<doc>` tags content supports markdown.

TTP Templates Collection comes with `generate_docs.py` script, this script iterates over all
folders within `ttp_templates` repository, loads templates and extracts `<doc>` tags content
to form `.md` files and construct navigation tree.