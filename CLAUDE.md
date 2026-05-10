# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal academic website for Christian Henning, hosted at https://chrhenning.com. Built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) template. Deployed via GitHub Actions to `gh-pages` branch on push to `main`.

## Development Commands

**Recommended (Docker):**
```bash
docker compose pull && docker compose up
# Site available at http://localhost:8080
```

**Without Docker (requires Ruby):**
```bash
bundle install
bundle exec jekyll serve
```

**Update Google Scholar citations:**
```bash
python bin/update_scholar_citations.py
```

**Format code:**
```bash
npx prettier --write .
```

## Architecture

| Path | Role |
|------|------|
| `_config.yml` | Main Jekyll config — site metadata, plugins, feature flags |
| `_pages/` | Top-level pages (about, CV, publications, projects, blog) |
| `_posts/` | Blog posts (Markdown, front matter controls layout/tags) |
| `_projects/` | Research/portfolio project pages |
| `_bibliography/papers.bib` | BibTeX source for the publications page |
| `_news/` | Short announcement entries shown on the about page |
| `_layouts/` | Page-level Liquid templates |
| `_includes/` | Reusable Liquid components |
| `_sass/` | SCSS stylesheets |
| `_plugins/` | Custom Ruby plugins (scholar citations, cache busting, BibTeX management) |
| `_data/` | YAML data consumed by templates |
| `assets/` | Images, compiled CSS/JS, PDFs, and other static files |

### Key Conventions

- **Publications** are driven entirely by `_bibliography/papers.bib` — adding/editing a BibTeX entry is sufficient to update the publications page. Citation counts are fetched from Google Scholar via `bin/update_scholar_citations.py` and stored in `_data/`.
- **Blog posts** in `_posts/` support both standard Jekyll Markdown and [Distill](https://distill.pub/)-style layouts (`layout: distill`). MathJax and code highlighting are available in all layouts.
- **Projects** in `_projects/` use front matter fields (`img`, `importance`, `category`) to control display order and grouping on the projects index.
- The site uses `jekyll-scholar` for bibliography rendering and citation cross-linking.
- CSS is purged at build time via `purgecss.config.js` — avoid adding dynamic class names that PurgeCSS can't detect statically.
