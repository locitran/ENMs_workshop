# Week 1: Introduction to py-rcsb-api

<p><span style="background:#fff2cc; color:#7f6000; padding:2px 8px; border-radius:999px;"><strong>Topics</strong></span></p>

- What `py-rcsb-api` is
- Installation and imports
- Search API basics
- Data API basics
- Simple examples
- Hands-on exercises
- Resources

## What is `py-rcsb-api`?

[`py-rcsb-api`](https://github.com/rcsb/py-rcsb-api) is the current Python toolkit for accessing RCSB PDB API services.
According to the official documentation, it provides Python interfaces for:

- the Search API
- the Data API
- the Sequence Coordinates API (not included in this workshop)
- the Model Server API (not included in this workshop)

For more information, visit:
- [Official `rcsb-api` documentation](https://rcsbapi.readthedocs.io/)
- [GitHub repository: `py-rcsb-api`](https://github.com/rcsb/py-rcsb-api)

## Part 1: Search API

The **Search API** is used to find PDB entries that match search conditions.
This is the easiest place to start.

### Text search

A `TextQuery` works like a keyword search.

```python
from rcsbapi.search import TextQuery
query = TextQuery(value="Hemoglobin")
results = list(query())
print(f"Found {len(results)} entries")
print(results[:10])
```

![alt text](<../images/week 1 - Text search.png>)

### Attribute search

An `AttributeQuery` searches a specific field.

```python
from rcsbapi.search import AttributeQuery
query = AttributeQuery(
    attribute="rcsb_entity_source_organism.scientific_name",
    operator="exact_match",
    value="Homo sapiens"
)
results = list(query())
print(f"Found {len(results)} entries")
print(results[:10])
```

![alt text](<../images/week 1 - Attribute search.png>)

You can also use the shorter attribute syntax from `search_attributes`.

```python
from rcsbapi.search import search_attributes as attrs
query = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
results = list(query())
print(f"Found {len(results)} entries")
print(results[:10])
```

### Combining queries

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

![alt text](<../images/week 1 - Combining queries.png>)

### Another search example

```python
q_method = attrs.exptl.method == "X-RAY DIFFRACTION"
q_resolution = attrs.rcsb_entry_info.resolution_combined < 2.5

query = q_method & q_resolution
results = list(query())

print(results[:10])
```

### Useful references
- [Search API quickstart](https://rcsbapi.readthedocs.io/en/latest/search_api/quickstart.html)
- [Search API Attributes](https://search.rcsb.org/structure-search-attributes.html)
- [Search API docs](https://search.rcsb.org/)

## Part 2: Data API

The **Data API** is used to retrieve structured information for specific IDs such as PDB entries.
If the Search API answers the question "which structures match my conditions?", the Data API answers the question "what details do these structures have?"

The official `py-rcsb-api` documentation explains that the Data API uses **GraphQL** under the hood.
In practice, this means:

- you start from an input object such as `entries`
- you provide one or more IDs, such as `4HHB`
- you request the exact fields you want back, such as `exptl.method` or `struct.title`

`DataQuery` helps us build this GraphQL request in Python, so we do not have to write the GraphQL query by hand.

### Basic pattern

A Data API query usually has three main parts:

1. `input_type`
   This says what kind of object you are querying, for example `entries`.
2. `input_ids`
   This is the list of IDs you want to look up.
3. `return_data_list`
   This is the list of fields you want to retrieve.

### Example 1: get the experimental method for one structure

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

This asks for entry `4HHB` and returns the value stored under `exptl.method`.

### Example output
A simplified example of the returned result may look like this:
```python
{
    'data': {
        'entries': [
            {
                'exptl': [
                    {'method': 'X-RAY DIFFRACTION'}
                ]
            }
        ]
    }
}
```
You usually need to inspect the result step by step to find the field you want.

### Example 2: retrieve more than one field
```python
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=["rcsb_id", "struct.title", "exptl.method"]
)

result = query.exec()
print(result)
```

### Example 3: request data for multiple entries
This is useful when you already have a short list of PDB IDs from a search result.
```python
from rcsbapi.data import DataQuery

query = DataQuery(
    input_type="entries",
    input_ids=["4HHB", "1CRN"],
    return_data_list=["rcsb_id", "struct.title"]
)

result = query.exec()
print(result)
```

### How the Data API relates to GraphQL

The RCSB Data API itself is based on **GraphQL**.
GraphQL organizes data into:

- **types**: structured objects such as an entry
- **fields**: properties under those objects
- **scalars**: final values such as strings, numbers, or booleans

The `py-rcsb-api` package reads the schema and helps generate GraphQL automatically.
So instead of writing raw GraphQL like this:

```graphql
{
  entries(entry_ids: ["4HHB"]) {
    exptl {
      method
    }
  }
}
```

we can write the equivalent Python query:
```python
from rcsbapi.data import DataQuery
query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=["exptl.method"]
)
```

This is one of the main benefits of `DataQuery`.
It gives us a simpler Python interface, while still using the GraphQL Data API underneath.

### Useful references
- [Data API quickstart](https://rcsbapi.readthedocs.io/en/latest/data_api/quickstart.html)
- [Data API Attributes](https://data.rcsb.org/data-attributes.html)
- [Data API docs](https://data.rcsb.org/)

## Hands-on exercises

### Exercise 1
Use `TextQuery` to search for `insulin` and print the first 10 PDB IDs.

### Exercise 2
Use `search_attributes` to find entries from `Mus musculus` and print the first 10 PDB IDs.

### Exercise 3
Find entries determined by `X-RAY DIFFRACTION` with resolution better than `2.0` A.

### Exercise 4
Search for `kinase`, then combine that query with a human organism filter.
Print the first 10 matching PDB IDs.

### Exercise 5
Use 10 PDB IDs from `Exercise 4` to find 
- (1) number of biological assembly structures (bas),
- (2) number of chains in each structure,
- (3) corresponding UniProt ID.
- (4) Finally, please arrange the results in a dictionary as follow:
```python
resulting_dictionary = {
    'pdbID 1': {
        'bas_1': {
            'chain A': 'Uniprot ID 1',
            'chain B': 'Uniprot ID 2',
            ...
        },
        'bas_2': {...
        }
    },
    'pdbID 2': {...
    },
    ...
}
```