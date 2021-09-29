"""
Script to generate documentation for TTP Templates by using <docs>
tag from templates.

This script scans all templates folders, reads all templates, loads
docs tags and creates markdown .md pages for the templates.
"""
import os
from ttp import ttp

for dirpath, dirnames, filenames in os.walk(top="ttp_templates"):
    for filename in filenames:
        if not filename.endswith(".txt"):
            continue
            
        # load doc strings from template
        doc_string = ""
        filepath = os.path.join(dirpath, filename)
        parser = ttp(template=filepath)
        for template in parser._templates:
            doc_string += template.__doc__
        
        # save doc string to .md files
        docs_filename = dirpath.replace("ttp_templates\\", "")
        docs_filename = docs_filename.replace("\\", ".") + "." + filename.replace(".txt", ".md")
        with open(os.path.join("docs", docs_filename), "w") as f:
            f.write(doc_string)
        