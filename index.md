---
layout: default
title: ENMs Workshop
kicker: Elastic Network Models
lead: Course notes, reading material, and hands-on exercises prepared for the ENMs workshop and published as a GitHub Pages site.
description: ENMs workshop homepage with links to lessons and setup material.
---

Welcome to the workshop website for **Elastic Network Models (ENMs)**. This site turns the repository notes into a cleaner teaching format so students can browse the material directly in the browser.

<div class="hero-grid">
  <a class="hero-card" href="{{ '/docs/' | relative_url }}">
    <strong>Docs Guide</strong>
    <span>See the multi-week outline, references, and planned topics.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/outline/' | relative_url }}">
    <strong>Workshop Outline</strong>
    <span>The broader multi-week roadmap with theory, practice, and references.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/week1-enms/' | relative_url }}">
    <strong>Week 1: Introduction to ENMs</strong>
    <span>Concepts, intuition, and the physical basis of ENMs.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/week1-py-rcsb-api/' | relative_url }}">
    <strong>Week 1: py-rcsb-api</strong>
    <span>Search and data API examples for retrieving PDB information.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/week1-bonus/' | relative_url }}">
    <strong>Bonus Notes</strong>
    <span>Optional theory notes on harmonic potentials and oscillators.</span>
  </a>
</div>

## What this site includes

- A browser-friendly homepage for the workshop.
- A sidebar navigation menu for moving between lessons.
- Rendered markdown pages hosted directly from the repository.
- Support for the existing images and math-heavy notes.

## Publishing on GitHub Pages

Push this repository to GitHub, then in the repository settings enable **Pages** and publish from the repository root on your default branch. GitHub will render these markdown files through Jekyll automatically.
