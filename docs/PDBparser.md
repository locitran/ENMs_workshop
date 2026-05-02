---
layout: default
title: "Week 4: PDB Parsing with MDAnalysis and ProDy"
kicker: "Coding Lesson"
lead: "Learn how to read structure and trajectory files, select atom groups, and perform trajectory-based mode analysis with MDAnalysis and ProDy."
description: "Teaching material for PDB parsing and trajectory analysis with MDAnalysis and ProDy."
permalink: /pdbparser/
---

# Week 4: PDB Parsing with MDAnalysis and ProDy

<p><span style="background:#fff2cc; color:#7f6000; padding:2px 8px; border-radius:999px;"><strong>Topics</strong></span></p>

- What a topology file and a coordinate file are
- Reading PDB and trajectory data with `MDAnalysis` and `ProDy`
- Selecting atom groups
- Selecting atom groups within a distance range
- Trajectory-based mode analysis
- Practice questions

## Why These Packages?

`MDAnalysis` and `ProDy` solve related but slightly different problems:

- `MDAnalysis` is excellent for reading many structure and trajectory formats and for making flexible atom selections.
- `ProDy` is especially convenient for structural dynamics analysis, including ENM-based normal modes and trajectory-based principal component analysis (PCA) / essential dynamics analysis (EDA).

In practice, it is common to:

1. read and select atoms with `MDAnalysis`
2. pass coordinates to `ProDy` for dynamics analysis

## Topology File vs Coordinate File

A molecular simulation usually separates **what the system is** from **where the atoms are**.

- A **topology file** stores atom identities and connectivity information.
- A **coordinate file** stores atom positions.

Examples of topology-like files:

- `PDB`
- `PSF`
- `PRMTOP`
- `TOP`

Examples of coordinate / trajectory files:

- `DCD`
- `XTC`
- `TRR`
- `RST` / AMBER restart
- single coordinate snapshots in `PDB` or `GRO`

> **Question for students:** What is the topology file and coordinate file? How are they different?

### A useful rule of thumb

- If you want to select atoms by names such as `protein`, `backbone`, `resid 50`, or `name CA`, you usually need a topology file with atom metadata.
- A trajectory file alone often does **not** contain enough metadata for rich atom selections.

## Reading Structure and Trajectory Files

### MDAnalysis

The basic object in `MDAnalysis` is a `Universe`.

```python
import MDAnalysis as mda

# Example 1: a PDB file only
u = mda.Universe("protein.pdb")

# Example 2: topology + trajectory
u = mda.Universe("topology.psf", "trajectory.dcd")

# Example 3: AMBER topology + trajectory
u = mda.Universe("system.prmtop", "traj.dcd")
```

Useful checks:

```python
print(u)
print("Number of atoms:", len(u.atoms))
print("Number of residues:", len(u.residues))
print("Number of frames:", len(u.trajectory))
```

### ProDy

For structure files:

```python
from prody import parsePDB

atoms = parsePDB("protein.pdb")
print(atoms)
```

For a DCD trajectory:

```python
from prody import DCDFile

dcd = DCDFile("trajectory.dcd")
print("Number of atoms:", dcd.numAtoms())
print("Number of frames:", dcd.numFrames())
```

`ProDy` also works well with atom groups parsed from PDB files:

```python
ca = atoms.select("protein and name CA")
print(ca)
```

## Selecting Atom Groups

This is one of the most important practical skills for students.

### 1.1 How to select certain atom group

### MDAnalysis examples

```python
protein = u.select_atoms("protein")
backbone = u.select_atoms("backbone")
ca = u.select_atoms("name CA")
chainA = u.select_atoms("segid A")
res50 = u.select_atoms("resid 50")
ala = u.select_atoms("resname ALA")
heavy = u.select_atoms("not name H*")
```

### ProDy examples

```python
protein = atoms.select("protein")
backbone = atoms.select("backbone")
ca = atoms.select("name CA")
chainA = atoms.select("chain A")
res50 = atoms.select("resnum 50")
ala = atoms.select("resname ALA")
heavy = atoms.select("not hydrogen")
```

### 1.2 How to select certain atom group within a range, and variants

Selections by distance are especially useful for binding sites, contacts, and local motions.

### MDAnalysis distance-based selections

```python
# Atoms within 5 A of residue 50
near_res50 = u.select_atoms("around 5 resid 50")

# Protein atoms within 4 A of ligand
binding_site = u.select_atoms("protein and around 4 resname ATP")

# Residues whose atoms are within 6 A of chain A
near_chainA = u.select_atoms("byres around 6 segid A")
```

Other useful variants in `MDAnalysis`:

- `around d selection`: atoms within distance `d`
- `byres ...`: expand atom selection to full residues
- `same residue as ...`: select complete residues related to another selection
- `point x y z d`: select atoms around a point in space

Examples:

```python
whole_residues = u.select_atoms("same residue as around 5 resname ATP")
sphere = u.select_atoms("point 10.0 12.0 15.0 6.0")
```

### ProDy distance-based selections

```python
# Atoms within 5 A of residue 50
near_res50 = atoms.select("within 5 of resnum 50")

# Protein atoms within 4 A of a ligand
binding_site = atoms.select("protein and within 4 of resname ATP")

# CA atoms within 8 A of chain A
ca_near_chainA = atoms.select("name CA and within 8 of chain A")
```

Useful variants in `ProDy`:

- `within d of ...`
- `exwithin d of ...` to exclude the reference selection itself
- combinations with `and`, `or`, `not`

Example:

```python
neighbors_only = atoms.select("protein and exwithin 5 of resnum 50")
```

> **Question for students:** If you want all residues within 5 A of a ligand, should you select atoms only, or should you expand the selection to complete residues?

## Topology + Coordinate in the Current Workshop Files

For the current workshop example:

- `data/md_NPT.dcd` is a trajectory file with many frames
- `data/md_NPT.rst` is an AMBER restart-style coordinate file containing one coordinate set and box information

These files are enough to demonstrate trajectory-based coordinate analysis, but they are **not** as rich as a full topology such as `PDB`, `PSF`, or `PRMTOP` for atom-name-based selections.

So:

- for teaching selection syntax, it is better to use a PDB/topology-rich example
- for teaching trajectory-based mode analysis, these files are still useful

## How to Perform Normal Mode Analysis

There are two related but different workflows students should know.

### A. ENM-based normal mode analysis from a structure

This is what `ProDy` is classically known for.

```python
from prody import parsePDB, ANM

atoms = parsePDB("protein.pdb").select("protein and name CA")

anm = ANM("protein ANM")
anm.buildHessian(atoms, cutoff=15.0, gamma=1.0)
anm.calcModes(n_modes=20)

print(anm)
print("Number of modes:", anm.numModes())
```

Typical next steps:

- inspect eigenvalues
- animate a low-frequency mode
- compare modes with experimental motions

### B. Trajectory-based mode analysis from MD

When we use an MD trajectory, we usually perform **PCA** or **EDA** rather than ENM normal mode analysis.

The idea is:

1. align the trajectory
2. compute the covariance matrix of coordinate fluctuations
3. diagonalize the covariance matrix
4. interpret the first few eigenvectors as collective modes

This is often called:

- PCA
- principal modes
- essential dynamics analysis
- quasi-harmonic analysis

## Example Workflow for a Trajectory

Below is a teaching-oriented workflow using the workshop files.

### 1. Load the reference coordinates and trajectory

```python
from scipy.io import netcdf_file
from prody import DCDFile

f = netcdf_file("data/md_NPT.rst", "r", mmap=False)
ref = f.variables["coordinates"].data.copy()
f.close()

dcd = DCDFile("data/md_NPT.dcd")
print("Reference shape:", ref.shape)
print("Trajectory frames:", dcd.numFrames())
print("Atoms per frame:", dcd.numAtoms())
```

### 2. Choose a subset of atoms for analysis

Because the trajectory has many atoms, the first teaching example should use a reduced subset.

```python
import numpy as np

# Example: every 100th atom, then keep the first 500 selected atoms
sel = np.arange(0, ref.shape[0], 100)[:500]
ref_sel = ref[sel]
```

If a rich topology were available, this is where we would instead choose `CA` atoms or backbone atoms.

### 3. Remove rigid-body motion

```python
from prody import calcTransformation

ref_cent = ref_sel - ref_sel.mean(axis=0)
```

Then loop over frames:

```python
frames = []
for i, frame in enumerate(dcd):
    if i >= 200:   # keep the first 200 frames for a small classroom example
        break
    coords = frame.getCoords()[sel]
    coords_cent = coords - coords.mean(axis=0)
    trans = calcTransformation(coords_cent, ref_cent)
    aligned = trans.apply(coords_cent.copy())
    frames.append(aligned.reshape(-1))
```

### 4. Compute PCA / essential dynamics

```python
import numpy as np
from sklearn.decomposition import PCA

X = np.vstack(frames)
print("Data matrix shape:", X.shape)  # (n_frames, 3*n_selected_atoms)

pca = PCA(n_components=5)
pca.fit(X)

print("Explained variance ratio:", pca.explained_variance_ratio_)
```

### 5. Project frames onto the first two modes

```python
proj = pca.transform(X)
pc1 = proj[:, 0]
pc2 = proj[:, 1]
```

This lets students see whether the trajectory samples one basin or multiple basins in conformational space.

### 6. Estimate fluctuation size from the covariance

```python
cov = np.cov(X, rowvar=False)
eigvals, eigvecs = np.linalg.eigh(cov)
eigvals = eigvals[::-1]
eigvecs = eigvecs[:, ::-1]

print("Largest eigenvalues:", eigvals[:5])
```

The largest eigenvalues correspond to the softest, largest-amplitude collective motions sampled by the trajectory.

## Suggested Student Questions

> **Question for students:** What is the topology file and coordinate file? How are they different?

> **Question for students:** Why do we align the trajectory before computing PCA?

> **Question for students:** What happens if we include overall translation and rotation in the covariance matrix?

> **Question for students:** Why might we choose `CA` atoms instead of all atoms for a first normal mode / PCA analysis?

> **Question for students:** In an MD trajectory, are the first principal components exactly the same as ENM normal modes? Why or why not?

## Summary

- `MDAnalysis` is excellent for reading trajectories and making atom selections.
- `ProDy` is excellent for structural dynamics and ENM-based mode analysis.
- A topology file tells us **what atoms exist** and how to name/select them.
- A coordinate or trajectory file tells us **where those atoms are**.
- For MD trajectories, the practical “normal mode” workflow is usually PCA / essential dynamics rather than ENM mode calculation.

## Minimal Installation Note

For this lesson, students will typically need:

```bash
pip install MDAnalysis ProDy scikit-learn scipy matplotlib
```

