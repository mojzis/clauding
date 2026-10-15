---
title: Architecture
tags: [architecture]
code: [content/, scaffold/, src/clauding/build.py, .github/workflows/pages.yml]
---

**Purpose:** publish the project-knowledge rules (principles, versioned rules text, catch-up prompt,
scaffold) as a small static site agents can read, and apply those rules to this repo itself.

```mermaid
flowchart LR
  content[content/**.md] --> build[src/clauding/build.py]
  docs[docs/**.md] --> build
  scaffold[scaffold/**] --> build
  build --> site[(site/)] --> pages[GitHub Pages]
  pages --> agent[agent in a target repo]
  scaffold -. copied into .-> target[target repo]
  rules[content/rules/vN.md] -. inlined into AGENTS.md .-> target
```

## Rules

| artifact | path | consumer |
|---|---|---|
| rules text | `content/rules/vN.md`, marker on line 1 | pasted verbatim into a target `AGENTS.md` |
| principle pages | `content/principles/*.md` | humans and agents wanting the why |
| catch-up prompt | `content/catch-up.md` | pasted into an agent session in an existing repo |
| scaffold | `scaffold/` | copied as-is into target repos |

A published `vN.md` never changes. A rules change ships as `vN+1.md` ([ADR 0002](adr/0002-rules-inlined-with-version-marker.md)).

## Docs layout

This repo's own knowledge follows the rules: `docs/architecture.md`, `docs/adr/`, `docs/papercuts/`,
`docs/style.md`, `docs/tags.md`, frontmatter on every page. The tag vocabulary covers `docs/` and `content/`.
`docs/brief.md` is the original handoff brief, kept for its open questions.

## QA

[`QA.md`](../QA.md) at the root. Tiers: `fast` (pytest), `site` (build; fails on broken links).

## Adoption

| target | mechanism |
|---|---|
| new repo | scaffold + rules section, shipped in the Python template |
| existing repo | [catch-up prompt](../content/catch-up.md): reads the version marker → full adoption or upgrade |

## Tooling

No checker yet. Planned `check` / `qa run` / `touching` / `tags` / `links`, parsing markdown on every
call, no stored index ([ADR 0009](adr/0009-markdown-only-source-of-truth.md)). Where it lives is open.
Today's automated checks: the build (broken links, bad frontmatter) and `tests/test_build.py` (tags in vocabulary,
scaffold YAML), run by the commit hook on staged markdown and by CI ([toolbox](toolbox.md)).

## Site

`uv run build` → `site/` (gitignored). URL map:

| source | url | raw |
|---|---|---|
| `content/index.md` | `/` | `/index.md` |
| `content/<p>.md` | `/<p>/` | `/<p>/index.md` |
| `docs/README.md` | `/docs/` | `/docs/index.md` |
| `docs/<p>.md` | `/docs/<p>/` | `/docs/<p>/index.md` |
| `scaffold/<f>` | `/scaffold/<f>` | (verbatim) |
| dir without README | `/<dir>/` | generated listing |

Plus `/llms.txt` (index of raw pages) and `/llms-full.txt` (all raw pages concatenated).
Relative `.md` links are rewritten to site URLs; one that doesn't resolve fails the build.
Template files (`_*.md`, `0000-*.md`) are not pages. `BASE_URL` sets the path prefix (default `/clauding`).
Deploy: push to `main` → `.github/workflows/pages.yml`.

**Invariants**
- Every page is published as HTML and as its raw markdown.
- `scaffold/` is published byte-for-byte.
- Markdown is the only source; nothing generated is committed.

**Decisions:** [adr/](adr/)
