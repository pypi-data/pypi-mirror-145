# Markdown Manuscript Filters
Intended to work with: 
- a markdown preview plugin for Atom or VSCode 
  - I use [markdown-preview-enhanced]()
- an intallation of LaTeX + pandoc 
- [markdown-manuscript-template]()

# Installation 
locally, from git repo:
`pip install -e .`

🚧 
from PyPi - [pypi page](https://pypi.org/project/markdown-manuscript-filters/)
`pip install markdown-manuscript-filters`


# Usage 
```
usage: compile_markdown.py [-h] [--dir DIR] [--aux AUX] [--out OUT] [-p] [-v] [-e] src_file

Converts markdown with @import statements to all-in-one markdown file 
- then filters out common annotation 
- then converts to pdf with pandoc

positional arguments:
  src_file    source markdown file (with @imports)

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   starting directory
  --aux AUX   directory for auxiliary files
  --out OUT   directory for outputs (i.e. pdf)
  -p          open (p)df after successful compile
  -v          (v)erbose
  -e          halt (e)xecution if a step errors
```

for example:
```
python -m compile_markdown -pve manuscript_v1  --aux publish/aux/ --out publish/output
```
<details><summary>↪example terminal output</summary>

```
.. compiling @imports ..
importing: 1_introduction.md
importing: 2_methods.md
importing: 3_results.md
writing compiled file to : tests/publish/aux/mv1_out.md
.. re-adding yaml ..
.. re-adding yaml, again ..
.. undoing line wrap ..
☼☼ PDF export complete ☼☼
☼☼ available at tests/publish/output/manuscript_v1.pdf ☼☼
```
</details>

---
# Image Attribution:

<img src="tests/Pan_flute.svg" height=50></img>
By johnny_automatic - Open Clip Art Library image's page, CC0, https://commons.wikimedia.org/w/index.php?curid=11066062
