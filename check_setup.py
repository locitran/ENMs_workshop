from itertools import islice

import rcsbsearchapi
from rcsbsearchapi import TextQuery


def main() -> None:
    print(f"rcsbsearchapi version: {rcsbsearchapi.__version__}")

    query = TextQuery("hemoglobin")
    first_five = list(islice(query(), 5))

    print("First 5 search results for 'hemoglobin':")
    for pdb_id in first_five:
        print(pdb_id)


if __name__ == "__main__":
    main()
