---
layout: default
title: Learning Notebooks
kicker: Resources
lead: Export Jupyter notebooks as static HTML pages so they can be viewed from the workshop website.
description: Notebook pages for the ENMs workshop.
permalink: /learning-notebooks/
---
This site cannot render raw `.ipynb` notebooks directly on GitHub Pages, so the notebooks are exported as static HTML.

Current notebook pages:

- [UniProt notebook]({{ '/notebooks-html/uniprot.html' | relative_url }})
- [Week 1 notebook]({{ '/notebooks-html/week1.html' | relative_url }})

Source notebooks in this repository:

- [notebooks/uniprot.ipynb](https://github.com/locitran/ENMs_workshop/blob/main/notebooks/uniprot.ipynb)
- [notebooks/week1.ipynb](https://github.com/locitran/ENMs_workshop/blob/main/notebooks/week1.ipynb)

To refresh the exported notebook pages locally, run:

```bash
python build_site_docs.py
```

That command regenerates the static HTML under `notebooks-html/`.
