# ENMs Workshop

This workshop includes the Week 1 lesson on `py-rcsb-search-api`.

## Files

- `Week1-py-rcsb-search-api.md`: workshop notes
- `Week1-ENMs-Introduction.md`: ENM introduction notes
- `requirements.txt`: Python packages for this workshop
- `check_setup.py`: simple setup test

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Test

```bash
python check_setup.py
```

This test imports `rcsbsearchapi` and runs a small search example.
It needs internet access.

## Git For Students

### Clone the repo

```bash
git clone https://github.com/locitran/ENMs_workshop.git
cd ENMs_workshop
```

### Get the latest changes

```bash
git pull origin main
```

### Check changed files

```bash
git status
```

### Save your own work

```bash
git add .
git commit -m "Update workshop files"
git push origin main
```

## How to publish this repo

This folder is already a git repository.
It is currently on `main` and has no commits yet.

To create the first commit and connect it to GitHub:

```bash
cd /mnt/nas_1/YangLab/project/ENMs_workshop
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/locitran/ENMs_workshop.git
git push -u origin main
```

## Notes

- Recommended Python: 3.10 or 3.11
- `rcsbsearchapi` is deprecated, but it is still fine for this workshop
- For newer projects, consider `rcsb-api`
