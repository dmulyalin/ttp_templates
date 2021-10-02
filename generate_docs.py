"""
Script to generate documentation for TTP Templates by using <docs>
tag from templates.

This script scans all templates folders, reads all templates, loads
docs tags and creates markdown .md pages for the templates.
"""
import os
from ttp import ttp
import yaml 
import time

# load and re-make mkdocs.yml nav section
misc = []
misc_dict = {}
platform = []
yang = []
templates_count = 0

page_template = """Reference path:
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

with open("mkdocs.yml", "r") as f:
    mkdocs_yaml = yaml.safe_load(f.read())

for item in mkdocs_yaml["nav"]:
    if "Templates" in item:
        item["Templates"] = [
            {"Misc": misc},
            {"Platform": platform},
            {"YANG": yang},
        ]

# load templates docs and form mkdocs.yml nav section
for dirpath, dirnames, filenames in os.walk(top="ttp_templates"):
    for filename in filenames:
        if not filename.endswith(".txt"):
            continue
            
        # load doc strings from template
        doc_string = ""
        filepath = os.path.join(dirpath, filename)
        parser = ttp(template=filepath)
        for template in parser._templates:
            doc_string += "\n" + template.__doc__
            
        # list templates without docs
        if doc_string.strip() == "":
            print("Template has no docs: {}".format(filepath))
            
        # open template file content
        with open(filepath) as tf:
            template_content = tf.read()
        
        # save doc string to .md files
        splitted_path = dirpath.split(os.sep)
        doc_string = page_template.format(
            path=".".join(splitted_path[1:]) + "." + filename, 
            doc=doc_string if doc_string.strip() else "No `<doc>` tags found",
            template_content=template_content
        )
        docs_filename = ".".join(splitted_path[1:]) + "." + filename.replace(".txt", ".md")
        with open(os.path.join("docs", "ttp_templates", docs_filename), "w") as f:
            f.write(doc_string)
        
        # form nav section of mkdocs.yaml
        if splitted_path[1] == "misc":
            misc_dict.setdefault(splitted_path[2], [])
            misc_dict[splitted_path[2]].append({".".join(docs_filename.split(".")[2:-1]): "ttp_templates/" + docs_filename})
        elif splitted_path[1] == "platform":
            platform.append({".".join(docs_filename.split(".")[1:-1]): "ttp_templates/" + docs_filename})
        elif splitted_path[1] == "yang":
            yang.append({".".join(docs_filename.split(".")[1:-1]): "ttp_templates/" + docs_filename})
        
        templates_count += 1
        
# fill in misc nav
for misc_dir_name, pages in misc_dict.items():
    misc.append({misc_dir_name: pages})

with open("mkdocs.yml", "w") as f:
    f.write(yaml.dump(mkdocs_yaml, default_flow_style=False))

# copy README.md content to index.md
with open("README.md") as readme_file:
    with open("docs/index.md", "w") as index_file:
        index_file.write(readme_file.read())