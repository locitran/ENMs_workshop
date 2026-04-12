---
layout: default
title: UniProt API Lesson
kicker: Week 1
lead: Learn how to think about websites as data sources, then use UniProt as a concrete example for fetching and parsing biological information in Python.
description: A teaching lesson on fetching and parsing information from UniProt.
permalink: /uniprot/
---
In general, there are three steps

1. Fetch the raw data from the website
2. Choose the parser that matches the data format
3. Convert the web data into Python structure

UniProt website is just an example.

We usually browse websites using Chrome or Edge, and most websites are written in HTML/CSS. Of course, we can still extract data from these pages, but a website API is often more convenient because the information is already organized in a structured form.

Several UniProt APIs are documented at https://www.uniprot.org/api-documentation/uniprotkb. However, in this material we will work with `https://rest.uniprot.org/uniprotkb/<UNIPROT ACC>`.

Here is an example "https://rest.uniprot.org/uniprotkb/P04439".

# Fetch the raw data

```python
def queryUniprot(accession, timeout=20):
    """Fetch one UniProtKB REST record as a raw JSON dictionary."""
    if not isinstance(accession, str):
        raise TypeError("accession should be a string")

    accession = accession.strip()
    if not accession:
        raise ValueError("accession should not be empty")

    url = REST_UNIPROT.format(accession)
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"No UniProt record found for accession {accession}") from exc
    return response.json()
```

Try

```python
accession = 'P04439'
raw = queryUniprot(accession)
type(raw), raw['primaryAccession']
```

# Write a parser

```python
class UniprotRecord(object):
    """Wrap one UniProt REST record and expose parsed biological annotations."""

    def __init__(self, data):
        self._rawdata = data

    def getOrganism(self):
        """Parse organism names, taxonomy id, and lineage."""
        organism = self._rawdata.get("organism", {})
        return {
            "scientific_name": organism.get("scientificName"),
            "common_name": organism.get("commonName"),
            "taxonomy_id": organism.get("taxonId"),
            "lineage": organism.get("lineage", []),
        }
```

# Combine fetching and parsing functions

```python
def searchUniprot(accession, timeout=20, n_attempts=3, dt=1):
    """Fetch one UniProt record and wrap it as a :class:`UniprotRecord`."""
    last_error = None
    for attempt in range(n_attempts):
        try:
            data = queryUniprot(accession, timeout=timeout)
            return UniprotRecord(data)
        except Exception as exc:
            last_error = exc
            LOGGER.info(f"Attempt {attempt} to contact UniProt failed")
            if attempt < n_attempts - 1:
                time.sleep((attempt + 1) * dt)
    raise last_error

record = searchUniprot(accession)
record.getOrganism()
# Output 
{'scientific_name': 'Homo sapiens',
 'common_name': 'Human',
 'taxonomy_id': 9606,
 'lineage': ['Eukaryota',
  'Metazoa',
  'Chordata',
  'Craniata',
  'Vertebrata',
  'Euteleostomi',
  'Mammalia',
  'Eutheria',
  'Euarchontoglires',
  'Primates',
  'Haplorrhini',
  'Catarrhini',
  'Hominidae',
  'Homo']}
```

# Exercise

Given a UniProt ID, please do as follow
1. Collect all PDB IDs
2. Write a function to rank PDB IDs based on coverage, resolution, and alphabet. 