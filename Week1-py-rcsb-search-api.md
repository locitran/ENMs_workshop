<h1 style="color:#1f4e79; background:#eaf2f8; padding:12px 16px; border-left:6px solid #5b9bd5; border-radius:8px;">Week 1: Introduction to py-rcsb-search-api</h1>

<p>
  <span style="background:#fff2cc; color:#7f6000; padding:2px 8px; border-radius:999px;"><strong>Topics</strong></span>
</p>

- What the RCSB PDB is and why we use it in ENM workflows
- What `py-rcsb-search-api` does
- Installation and import
- Basic query types: `TextQuery` and attribute-based queries
- Combining queries with logical operators
- Practical search examples for protein dynamics
- Hands-on exercises
- Resources and next steps

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Why start with the RCSB PDB?</h2>

The [RCSB Protein Data Bank (PDB)](https://www.rcsb.org/) is the main public archive for experimentally determined 3D structures of biological macromolecules.
For ENM-related work, it is usually the first place we go to find a structure that is suitable for:

- Gaussian Network Model (GNM)
- Anisotropic Network Model (ANM)
- normal mode analysis
- comparing different conformational states
- building small benchmark datasets

The PDB gives us more than coordinates. It also gives us metadata that helps us decide whether a structure is useful, such as:

- experimental method
- resolution
- organism
- polymer type
- ligand information
- release date and annotations

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">What is `py-rcsb-search-api`?</h2>

`py-rcsb-search-api` is the Python interface to the RCSB Search API. It lets us search the PDB from code instead of clicking through the website.
That is especially helpful when we want to repeat searches, filter structures systematically, or feed PDB IDs into downstream ENM pipelines.

Typical uses include:

- finding all structures for a protein or protein family
- filtering by organism or experimental method
- collecting entries that match ligand or annotation criteria
- building reproducible structure lists for analysis notebooks

<h3>Package status</h3>

According to the official `rcsbsearchapi` documentation, this package is now marked as deprecated and users are encouraged to migrate to [`rcsb-api`](https://github.com/rcsb/py-rcsb-api) for newer work.
We can still use `rcsbsearchapi` in this workshop because it is simple and very good for learning the query model.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Installation and import</h2>

### Install

```bash
pip install rcsbsearchapi
```

### Import

```python
from rcsbsearchapi import TextQuery
from rcsbsearchapi import rcsb_attributes as attrs
```

`TextQuery` is useful for keyword-style searching.
`attrs` exposes searchable metadata fields in a more readable way.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Basic query type 1: `TextQuery`</h2>

A text query behaves like a keyword search on the RCSB side.
It is a good starting point when you want to explore what is available.

```python
from rcsbsearchapi import TextQuery

query = TextQuery("hemoglobin")
results = list(query())

print(f"Found {len(results)} entries")
print(results[:10])
```

Use `TextQuery` when you want to search terms like:

- protein names
- biological processes
- diseases
- common keywords in annotations

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Basic query type 2: attribute queries</h2>

Attribute queries are more precise. Instead of searching free text, we search a specific field.
For example, we can search by organism, experimental method, or resolution.

```python
from rcsbsearchapi import rcsb_attributes as attrs

query = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
results = list(query())

print(f"Found {len(results)} human entries")
```

Another example: X-ray structures with resolution better than 2.5 A.

```python
q_method = attrs.exptl.method == "X-RAY DIFFRACTION"
q_resolution = attrs.rcsb_entry_info.resolution_combined < 2.5

query = q_method & q_resolution
results = list(query())

print(f"Found {len(results)} high-resolution X-ray entries")
```

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Combining queries</h2>

Queries can be combined with Python bitwise operators:

- `&` means AND
- `|` means OR
- `~` means NOT

This makes it easy to build filters step by step.

### Example: human hemoglobin structures

```python
from rcsbsearchapi import TextQuery
from rcsbsearchapi import rcsb_attributes as attrs

q_text = TextQuery("hemoglobin")
q_species = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"

query = q_text & q_species
results = list(query())

print(f"Found {len(results)} human hemoglobin entries")
print(results[:10])
```

### Example: cryo-EM entries from humans

```python
q_method = attrs.exptl.method == "ELECTRON MICROSCOPY"
q_species = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"

query = q_method & q_species
results = list(query())

print(f"Found {len(results)} human cryo-EM entries")
```

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Examples that are useful for ENM projects</h2>

When preparing structures for ENMs, we usually want entries that are experimentally reliable and biologically relevant.
The exact criteria depend on the project, but these are common patterns.

### 1. Search for a specific target protein

```python
q_target = TextQuery("EGFR")
results = list(q_target())
print(results[:10])
```

This is a quick discovery step. After that, we usually add stricter filters.

### 2. Restrict to human X-ray structures with decent resolution

```python
q_target = TextQuery("EGFR")
q_species = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
q_method = attrs.exptl.method == "X-RAY DIFFRACTION"
q_resolution = attrs.rcsb_entry_info.resolution_combined < 3.0

query = q_target & q_species & q_method & q_resolution
results = list(query())

print(f"Found {len(results)} filtered EGFR entries")
```

### 3. Find membrane proteins from a chosen organism

```python
q_membrane = attrs.rcsb_polymer_entity_annotation.type == "TRANSMEMBRANE"
q_species = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"

query = q_membrane & q_species
results = list(query())

print(f"Found {len(results)} human membrane-protein entries")
```

### 4. Focus on recently released structures

```python
q_recent = attrs.rcsb_accession_info.initial_release_date >= "2020-01-01"
results = list(q_recent())

print(f"Found {len(results)} entries released since 2020")
```

This kind of filter is useful when we want updated structural coverage for a protein family.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">A practical workflow for students</h2>

A simple pattern that works well in workshop notebooks is:

1. Start broad with `TextQuery`.
2. Add one biological filter, such as organism.
3. Add one quality filter, such as method or resolution.
4. Inspect the returned PDB IDs.
5. Select one or more entries for ENM analysis.

This keeps the search process transparent and reproducible.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Hands-on exercises</h2>

### Exercise 1

Search for all entries related to `myosin` and report the first 10 PDB IDs.

### Exercise 2

Find entries determined by `ELECTRON MICROSCOPY` with resolution better than `3.5` A.

### Exercise 3

Find human structures for `p53` and then restrict the result to X-ray structures.

### Exercise 4

Identify structures released on or after `2020-01-01` for a protein family that interests you.

### Exercise 5

Build a query for ENM preparation by combining:

- one target term
- one species filter
- one experimental method filter
- one quality filter

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Resources</h2>

- [Official `rcsbsearchapi` documentation](https://rcsbsearchapi.readthedocs.io/)
- [RCSB Search API](https://search.rcsb.org/)
- [Search attribute reference](https://search.rcsb.org/structure-search-attributes.html)
- [Quickstart notebook](https://github.com/rcsb/py-rcsbsearchapi/blob/master/notebooks/quickstart.ipynb)
- [Successor package: `py-rcsb-api`](https://github.com/rcsb/py-rcsb-api)

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Take-home message</h2>

`py-rcsb-search-api` is a convenient way to move from manual PDB browsing to reproducible, scriptable structure selection.
For ENM work, that matters because choosing the right input structures is often the first step that determines the quality of everything that follows.
