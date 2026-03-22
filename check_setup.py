from importlib.metadata import PackageNotFoundError, version
from itertools import islice

from rcsbapi.search import TextQuery


def get_package_version() -> str:
    try:
        return version("rcsb-api")
    except PackageNotFoundError:
        return "unknown"


def main() -> None:
    print(f"rcsb-api version: {get_package_version()}")

    query = TextQuery(value="Hemoglobin")
    first_five = list(islice(query(), 5))

    print("First 5 search results for 'Hemoglobin':")
    for pdb_id in first_five:
        print(pdb_id)

    print("Install successfully!")

if __name__ == "__main__":
    main()
