---
layout: distill
title: Code Sharing at Scale in Python Monorepos with a Single Version Policy
date: 2026-02-15 10:15:00
description: How structuring internal modules as installable packages in a monorepo enables controlled code reuse across many containers — while keeping images lean and dependency management centralized.
tags: swe
categories: engineering
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-02-15-code-sharing-in-monorepos.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: The Problem - Sharing Code Across Many Containers
  - name: Maintaining Explicit Dependency Boundaries
  - name: Single Version Policy as the Scaling Constraint
  - name: What Changes in Practice
---

In a Python monorepo that produces multiple independently deployed containers, shared modules become a cross-cutting dependency challenge that affects every part of the system. Naïvely copying shared modules into images or accumulating "just-in-case" dependencies in requirements files works for a while, until containers become difficult to audit and builds slow down. Updating a dependency now requires verifying compatibility across all containers that implicitly or explicitly depend on it.

This post argues that scalable code sharing in a monorepo requires two deliberate constraints: internal modules as **installable packages**, and a **Single Version Policy (SVP)** enforced by a shared lockfile.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/python_monorepo_lockfile.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Scaling code reuse through explicit boundaries and global constraints.</b> Internal modules are structured as <b>installable packages</b> to define clear dependency boundaries. A <b>Single Version Policy (SVP)</b> then resolves these requirements into a single, shared lockfile. This allows each container to install only the specific code it needs while guaranteeing that all services across the monorepo share a consistent and audited dependency graph.
</div>

## The Problem: Sharing Code Across Many Containers

In a growing monorepo, the number of containers tends to outpace the number of developers. APIs, workers, training jobs, scheduled tasks, internal tools — all built from the same repository, all sharing some portion of the same code.

The easy solution is to copy shared modules into images or maintain shared requirements files. That works - until it doesn't. Containers include libraries that are not imported by the application code they execute. Dependencies of shared modules are no longer declared at a package boundary but are discovered only through transitive imports. Updating a vulnerable library requires auditing multiple services. Over time, each container drifts into its own slightly different set of dependency versions.

**Code sharing stops being about reuse and becomes a dependency management problem.**

## Maintaining Explicit Dependency Boundaries

The core constraint is simple: **Shared code must declare its own dependencies, and containers must install only what they explicitly depend on**.

In practice, this means turning internal modules into proper installable [Python packages](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), each with its own `pyproject.toml`. A package defines:

- Its runtime dependencies
- Its internal workspace dependencies
- The importable modules that constitute its public API

Containers no longer copy folders. They install packages.

This forces explicit boundaries. If a module imports `pydantic`, it declares it. If a service depends on `ml-core` but not `ml-training`, it installs only the former. The dependency graph becomes explicitly declared rather than inferred from imports across arbitrary directories.

The unit of reuse becomes the package, not the directory.

## Single Version Policy as the Scaling Constraint

Explicit package boundaries are necessary, but not sufficient. Without coordination, each package could pin its own versions, reintroducing divergence at the dependency layer. That is where a Single Version Policy (SVP) enters <d-cite key="google-code-sharing"></d-cite><d-cite key="google-one-version-rule"></d-cite>.

Under SVP:

- All external dependency versions are resolved globally.
- A shared lockfile pins the full transitive graph.
- Internal packages declare what they need, not which version.
- The entire monorepo shares one coherent dependency graph.

This has concrete consequences:

- No [diamond dependency](https://en.wikipedia.org/wiki/Dependency_hell#Diamond_dependency) conflicts between services.
- Security updates are applied once, centrally.
- CI tests a single resolved graph rather than a combinatorial version matrix.

Each container becomes a projection of the same resolved dependency graph, restricted to the subset required by its installed packages.

## What Changes in Practice

This change affects how the system is structured, but the benefits are practical:

- Internal modules become installable packages.
- A shared lockfile governs all external versions.<d-footnote>One practical implementation is using <code>uv</code>, whose <a href="https://docs.astral.sh/uv/concepts/projects/workspaces/">workspace model</a> allows multiple internal packages to share a single resolved dependency graph and lockfile.</d-footnote>
- Containers install only the packages they require.
- CI validates packages independently against the locked graph.

The result is not merely smaller images. The dependency graph becomes inspectable, reproducible, and globally consistent. Dependencies are declared where they originate. Versioning is centralized. Containers become minimal compositions of explicitly declared packages.

This introduces coordination costs: refactoring shared modules into packages, maintaining lockfile stability, and resolving merge conflicts. However, the alternative is unmanaged dependency divergence across services.

At scale, code sharing is not about avoiding duplication. It is about maintaining a coherent dependency graph across many independently deployed artifacts. Installable packages under a Single Version Policy enforce global dependency coherence while preserving atomic change and independent deployment, both of which reduce coordination overhead as the system grows.
