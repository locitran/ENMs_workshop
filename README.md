# ENMs Workshop

This workshop includes the Week 1 lesson on `ENMs` and `py-rcsb-api`.

## Files

- `workshop/Week1-py-rcsb-api.md`: workshop notes for `py-rcsb-api`
- `workshop/Week1-ENMs-Introduction.md`: ENM introduction notes
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

## Test
This test should import `rcsbapi` and run a small example. It needs internet access.
```bash
python check_setup.py
```

