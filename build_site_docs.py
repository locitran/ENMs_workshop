#!/usr/bin/env python3
"""Build static notebook and API documentation pages for the Jekyll site."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOKS_DIR = ROOT / "notebooks"
NOTEBOOK_HTML_DIR = ROOT / "notebooks-html"
API_DIR = ROOT / "api"
PACKAGE_DIR = ROOT / "yanglab"


def require_command(command: str) -> None:
    """Ensure an external command is available before building docs."""
    if shutil.which(command) is None:
        raise SystemExit(
            f"Missing required command: {command}\n"
            "Install the documentation dependencies first, then run this script again."
        )


def build_notebooks() -> None:
    """Export each Jupyter notebook in notebooks/ to standalone HTML."""
    require_command("jupyter")
    NOTEBOOK_HTML_DIR.mkdir(exist_ok=True)

    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    if not notebooks:
        print("No notebooks found in notebooks/.")
        return

    for notebook in notebooks:
        print(f"Exporting notebook: {notebook.relative_to(ROOT)}")
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "html",
                "--output-dir",
                str(NOTEBOOK_HTML_DIR),
                str(notebook),
            ],
            check=True,
            cwd=ROOT,
        )


def build_api() -> None:
    """Generate static API documentation for the yanglab package with pdoc."""
    subprocess.run(
        [sys.executable, "-m", "pdoc", "-o", str(API_DIR), str(PACKAGE_DIR)],
        check=True,
        cwd=ROOT,
    )


def main() -> None:
    """Build both notebook exports and Python API documentation."""
    print("Building notebook HTML pages...")
    build_notebooks()

    print("Building yanglab API docs...")
    build_api()

    print("Done.")
    print(f"Notebook HTML: {NOTEBOOK_HTML_DIR}")
    print(f"API docs: {API_DIR}")


if __name__ == "__main__":
    main()
