---
title: "Knowledge: small, linked, tagged files"
tags: [principle, knowledge]
---

Project knowledge lives in `docs/` as small, dense, linked, tagged markdown files.
Markdown is the only source of truth.

## Why

| without it | failure |
|---|---|
| one long doc | agent loads 2,000 lines to use 20 |
| free-form tags | `billing`, `invoices`, `invoicing`: nothing findable |
| unlinked files | dead knowledge nobody reaches |
| no frontmatter | no way to find docs for an area without reading them all |

## Small files

- One concept per file, ~<150 lines. Split rather than grow.
- Link related files relatively. A file nothing links to is a smell.
- If a section needs a heading to be findable, it probably wants its own file.

## Frontmatter on every doc

```yaml
---
title: Invoice computation               # str, required
tags: [billing, domain]                  # list[str], only from docs/tags.md
code: [src/pkg/billing.py::compute_invoice, src/pkg/io/]   # path or path::Symbol
---
```

`code:` is covered by [freshness](freshness.md). ADRs and papercuts add `status` ([ADRs](adr.md), [papercuts](papercuts.md)).

## Controlled tag vocabulary

`docs/tags.md`: one tag per line with a one-line meaning.

- Tags only from `docs/tags.md`.
- If none fits, add one there **in the same change**.
- When adding a tag, look at the existing ones first.

Seed vocabulary: [`scaffold/docs/tags.md`](../../scaffold/docs/tags.md):
`meta`, `domain`, `architecture`, `ops`, `dev`, `qa`.
The catch-up prompt derives 10–20 tags from what the docs actually cover.

## Layout

```
QA.md                  operational, at the project root (see QA)
docs/
  README.md            index
  style.md             writing rules
  tags.md              vocabulary
  architecture.md      current state
  adr/NNNN-slug.md     decisions
  papercuts/slug.md    friction
  <concept>.md         everything else, one concept each
```

Scaffold index: [`scaffold/docs/README.md`](../../scaffold/docs/README.md).
Writing rules: [`scaffold/docs/style.md`](../../scaffold/docs/style.md): read before writing any doc.

## Search

None built. Agents use ripgrep over frontmatter and text.
No stored index either: files are edited directly, so an index would go stale.

## Interplay

| rule | link |
|---|---|
| [freshness](freshness.md) | `code:` is how docs are found from code |
| [architecture](architecture.md) | the hub most files link back to |
| [papercuts](papercuts.md) | a misleading or unfindable doc is a papercut |

## Tooling

| check | command |
|---|---|
| frontmatter present; tags in vocabulary; relative links resolve; size limit | `check` |
| vocabulary with usage counts | `tags` |
| backlinks; unlinked files | `links` / `orphans` |
