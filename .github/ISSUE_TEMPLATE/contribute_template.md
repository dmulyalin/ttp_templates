---
name: Contribute Template
about: Use this template for contributing new TTP Templates.
title: ''
labels: new template
assignees: ''

---

It is great to see that you would like to contribute new template(s) to TTP Templates repository, thank you.

Several pieces of information required for each template:

* Template Category and Template Name
* Template Content
* Sample Data
* Expected Output

*Sample Data* and *Expected Output* used to make up template test.

*Template Content* placed in one of *Template Category* below using *Template Name* as a filename:

* `platform` template - mimics [ntc-templates](https://github.com/networktocode/ntc-templates) 
  API and follows same naming rule - `{{ vendor_os }}_{{ command_with_underscores }}.txt` - lower case only
* `yang` template - contains templates capable of producing YANG compatible structures out of text data,
  and uses naming rule - `{{ YANG module name }}_{{ platform_name }}.txt` - lower case only
* `misc` template - miscellaneous templates for various use cases organized in folders, naming
  rule is - `{{ usecase folder }}/{{ template name }}.txt` - upper or lower case

If you are in doubt choosing template name and category, feel free to leave them blank.

# Template Category and Template Name

Template name: `template name here`
Template category: `platform, misc or yang`

# Template Content

```
Template content here
```

# Sample Data

```
Sample data here
```

# Expected Output

Expected output is output produced by parsing provided sample data with the template.

```
Expected output here
```
