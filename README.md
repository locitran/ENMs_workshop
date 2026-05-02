# ENMs Workshop

This workshop includes the Week 1 lesson on `ENMs` and `py-rcsb-api`.

## Website

This repository includes a GitHub Pages site in the repository root built from markdown files with Jekyll.

After pushing to GitHub, enable **Settings -> Pages** and publish from:

- Branch: your default branch
- Folder: `/ (root)`

The site homepage will be served at: https://locitran.github.io/ENMs_workshop/

This website presents the workshop materials in a browser-friendly format, including the introduction to elastic network models, the `py-rcsb-api` lesson, additional theory notes, and the overall workshop outline.

GitHub Pages will render the markdown pages in the repository root automatically through Jekyll.

## Website Tree

- Home: https://locitran.github.io/ENMs_workshop/
- Workshop Outline: https://locitran.github.io/ENMs_workshop/outline/
- Week 1 Introduction: https://locitran.github.io/ENMs_workshop/intro-enms/
- Week 1 py-rcsb-api: https://locitran.github.io/ENMs_workshop/py-rcsb-api/
- Two-particle motion: https://locitran.github.io/ENMs_workshop/two-particle-motion/

## Files

- `docs/Week1-py-rcsb-api.md`: workshop notes for `py-rcsb-api`
- `docs/Week1-ENMs-Introduction.md`: ENM introduction notes
- `notebooks/`: source Jupyter notebooks
- `notebooks-html/`: exported HTML versions of the notebooks
- `_layouts/`, `_config.yml`, `index.md`, `docs/`: Jekyll site for GitHub Pages
- `requirements.txt`: Python packages for this workshop
- `check_setup.py`: simple setup test

## Getting Started

### 1. Log in to A100
```bash
ssh -l <your_login_name> 140.114.97.192
```

Use your assigned login name and password.

### 2. Download the workshop from GitHub
Go to the directory where you want to place the repository, then run:
```bash
git clone https://github.com/locitran/ENMs_workshop.git
cd ENMs_workshop
```

### 3. Run Jupiter notebook in A100
Refer to this hackMD https://hackmd.io/Y9HZatmrSnqtHcC7X6tc-Q

### 4. Export notebooks to HTML
To generate HTML versions of all notebooks and store them in `notebooks-html`,
run:

```bash
jupyter nbconvert --to html --output-dir=notebooks-html notebooks/*.ipynb
```

Notes:

- This keeps the source notebooks in `notebooks/`.
- The exported HTML files are written to `notebooks-html/`.
- Example: `notebooks/uniprot.ipynb` becomes `notebooks-html/uniprot.html`.
- If a notebook has saved cell outputs, figures, or tables, they will be included in the HTML export.


## Setup With Conda
Please use conda for this workshop.

If you do not have Miniconda yet, follow the Miniconda section in this HackMD first:
https://hackmd.io/JTdM-ho2Siqx3F01vDdkow?view#Miniconda

Then create and activate an environment:
```bash
conda create --name <your_env_name> python=<python_version>
conda activate <your_env_name>
```

Example:
```bash
conda create --name enm_workshop python=3.11
conda activate enm_workshop
```

After that, install the package requirements:
```bash
pip install -r requirements.txt
```

## Install `yanglab` As A Package

The `yanglab` code under `ENMs_workshop/yanglab` can now be installed as a
local Python package because this project includes a
[`pyproject.toml`](/mnt/nas_1/YangLab/project/ENMs_workshop/pyproject.toml).

From the `ENMs_workshop` directory:

```bash
cd ENMs_workshop
pip install -e . --no-build-isolation
```

If you also want the notebook and plotting dependencies used in the workshop:

```bash
pip install -e ".[workshop]" --no-build-isolation
```

You can then import the package with:

```python
import yanglab
print(yanglab.__version__)
```

## Test
This test should import `rcsbapi` and run a small example. It needs internet access.
```bash
python check_setup.py
```
