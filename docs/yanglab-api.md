---
layout: default
title: yanglab API
kicker: Resources
lead: Auto-generated API documentation for the local `yanglab` teaching package.
description: API docs for the yanglab package used in the ENMs workshop.
permalink: /yanglab-api/
---
The `yanglab` package is documented as static HTML so it can be browsed on GitHub Pages.

Entry points:

- [yanglab package index]({{ '/api/yanglab.html' | relative_url }})
- [yanglab.UniProt]({{ '/api/yanglab/UniProt.html' | relative_url }})
- [yanglab.RCSB]({{ '/api/yanglab/RCSB.html' | relative_url }})

Source code in this repository:

- [yanglab/](https://github.com/locitran/ENMs_workshop/tree/main/yanglab)

To regenerate the API documentation locally, run:

```bash
python build_site_docs.py
```

That command rebuilds the static API files under `api/`.
