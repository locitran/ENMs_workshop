<h1 style="color:#1f4e79; background:#eaf2f8; padding:12px 16px; border-left:6px solid #5b9bd5; border-radius:8px;">Week 1: Introduction to py-rcsb-api</h1>

<p>
  <span style="background:#fff2cc; color:#7f6000; padding:2px 8px; border-radius:999px;"><strong>Topics</strong></span>
</p>

- What `py-rcsb-api` is
- Installation and imports
- Search API basics
- Data API basics
- Simple examples
- Hands-on exercises
- Resources

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">What is `py-rcsb-api`?</h2>

[`py-rcsb-api`](https://github.com/rcsb/py-rcsb-api) is the current Python toolkit for accessing RCSB PDB API services.
According to the official documentation, it provides Python interfaces for:

- the Search API
- the Data API
- the Sequence Coordinates API
- the Model Server API

For beginners, the two most useful parts to start with are:

- `rcsbapi.search` for finding entries
- `rcsbapi.data` for retrieving structured metadata

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Installation</h2>

The official GitHub README says `rcsb-api` requires Python 3.9 or later.

### Install with pip

```bash
pip install rcsb-api
```

### Import the Search API

```python
from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.search import search_attributes as attrs
```

### Import the Data API

```python
from rcsbapi.data import DataQuery
```

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Part 1: Search API</h2>

The Search API is used to find PDB entries that match search conditions.
This is the easiest place to start.

<h3>Text search</h3>

A `TextQuery` works like a keyword search.

```python
from rcsbapi.search import TextQuery

query = TextQuery(value="Hemoglobin")
results = list(query())

print(f"Found {len(results)} entries")
print(results[:10])
```

<h3>Attribute search</h3>

An `AttributeQuery` searches a specific field.

```python
from rcsbapi.search import AttributeQuery

query = AttributeQuery(
    attribute="rcsb_entity_source_organism.scientific_name",
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())

print(results[:10])
```

You can also use the shorter attribute syntax from `search_attributes`.

```python
from rcsbapi.search import search_attributes as attrs

query = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
results = list(query())

print(results[:10])
```

<h3>Combining queries</h3>

Queries can be combined with Python bitwise operators:

- `&` means AND
- `|` means OR
- `~` means NOT

```python
from rcsbapi.search import TextQuery
from rcsbapi.search import search_attributes as attrs

q1 = TextQuery(value="Hemoglobin")
q2 = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"

query = q1 & q2
results = list(query())

print(results[:10])
```

<h3>Another search example</h3>

```python
q_method = attrs.exptl.method == "X-RAY DIFFRACTION"
q_resolution = attrs.rcsb_entry_info.resolution_combined < 2.5

query = q_method & q_resolution
results = list(query())

print(results[:10])
```

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Part 2: Data API</h2>

The Data API is used to retrieve structured information for specific entries.
According to the official documentation, this module builds GraphQL queries for you.

A simple example is to fetch the experimental method for entry `4HHB`.

```python
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=["exptl.method"]
)

result = query.exec()
print(result)
```

This is useful after a search step.
For example, you can:

1. use `rcsbapi.search` to find PDB IDs
2. use `rcsbapi.data` to retrieve metadata for those IDs

<h3>Another Data API example</h3>

```python
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=["rcsb_id", "struct.title"]
)

result = query.exec()
print(result)
```

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">A simple learning workflow</h2>

A good way to learn `py-rcsb-api` is:

1. Start with a `TextQuery`.
2. Try one attribute query.
3. Combine two search queries.
4. Save one or two PDB IDs from the search results.
5. Use `DataQuery` to fetch metadata for those IDs.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Hands-on exercises</h2>

### Exercise 1

Use `TextQuery` to search for `myosin` and print the first 10 PDB IDs.

### Exercise 2

Use `search_attributes` to find entries from `Homo sapiens`.

### Exercise 3

Find entries determined by `ELECTRON MICROSCOPY` with resolution better than `3.5` A.

### Exercise 4

Search for `p53`, then combine that query with a human organism filter.

### Exercise 5

Use `DataQuery` to retrieve `exptl.method` and `struct.title` for entry `4HHB`.

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Resources</h2>

- [Official `rcsb-api` documentation](https://rcsbapi.readthedocs.io/)
- [GitHub repository: `py-rcsb-api`](https://github.com/rcsb/py-rcsb-api)
- [RCSB Search API docs](https://search.rcsb.org/)
- [RCSB Data API docs](https://data.rcsb.org/)
- [Search quickstart notebook](https://github.com/rcsb/py-rcsb-api/blob/master/notebooks/search_quickstart.ipynb)
- [Data quickstart notebook](https://github.com/rcsb/py-rcsb-api/blob/master/notebooks/data_quickstart.ipynb)

<h2 style="color:#c55a11; border-bottom:2px solid #f4b183; padding-bottom:4px;">Take-home message</h2>

`py-rcsb-api` is the current official Python package for accessing RCSB PDB API services.
A practical beginner workflow is to use `rcsbapi.search` to find entries and `rcsbapi.data` to retrieve detailed information about them.
