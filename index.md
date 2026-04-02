---
layout: default
title: ENMs Workshop
kicker: Elastic Network Models
lead: Course notes, reading material, and hands-on exercises prepared for the ENMs workshop and published as a GitHub Pages site.
description: ENMs workshop homepage with links to lessons and setup material.
---

Welcome to the workshop website for **Elastic Network Models (ENMs)**. This site turns the repository notes into a cleaner teaching format so students can browse the material directly in the browser.

<div class="hero-grid">
  <a class="hero-card" href="{{ '/docs/week1-enms/' | relative_url }}">
    <strong>Week 1: Introduction</strong>
    <span>Concepts, intuition, and the physical basis of elastic network models.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/week1-py-rcsb-api/' | relative_url }}">
    <strong>Week 1: py-rcsb-api</strong>
    <span>Search and data API examples for retrieving PDB information.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/week1-bonus/' | relative_url }}">
    <strong>Bonus Notes</strong>
    <span>Optional theory notes on harmonic potentials and oscillators.</span>
  </a>
  <a class="hero-card" href="{{ '/docs/outline/' | relative_url }}">
    <strong>Workshop Outline</strong>
    <span>The broader multi-week roadmap with theory, practice, and references.</span>
  </a>
</div>

## Site Tree

- [Home]({{ '/' | relative_url }})
- [Week 1: Introduction]({{ '/docs/week1-enms/' | relative_url }})
- [Week 1: py-rcsb-api]({{ '/docs/week1-py-rcsb-api/' | relative_url }})
- [Bonus Notes]({{ '/docs/week1-bonus/' | relative_url }})
- [Workshop Outline]({{ '/docs/outline/' | relative_url }})

## What this site includes

- A browser-friendly homepage for the workshop.
- A sidebar navigation menu for moving between lessons.
- Rendered markdown pages hosted directly from the repository.
- Support for the existing images and math-heavy notes.

## Publishing on GitHub Pages

Push this repository to GitHub, then in the repository settings enable **Pages** and publish from the repository root on your default branch. GitHub will render these markdown files through Jekyll automatically.
