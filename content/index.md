---
title: Project-knowledge rules
tags: [meta]
---

Short rules that keep a repo's knowledge agent-usable and its "done" provable.
Strong models follow short rules well: text gets most of the way, a small checker covers the rest.

| rule | lives in | principle |
|---|---|---|
| QA | `QA.md` at the project root | [evidence, not a green checkmark](principles/qa.md) |
| current architecture | `docs/architecture.md` | [architecture](principles/architecture.md) |
| decisions | `docs/adr/NNNN-slug.md` | [ADRs](principles/adr.md) |
| papercuts | `docs/papercuts/slug.md` | [papercuts](principles/papercuts.md) |
| writing style | `docs/style.md` | [style](../scaffold/docs/style.md) |
| small linked tagged docs | `docs/**` + `docs/tags.md` | [knowledge](principles/knowledge.md) |
| freshness | frontmatter `code:` refs | [freshness](principles/freshness.md) |

## Use it

| situation | do |
|---|---|
| new repo | copy the [scaffold](#scaffold), paste the [rules](rules/v1.md) into `AGENTS.md` |
| existing repo | paste the [catch-up prompt](catch-up.md) into an agent session at the repo root |
| repo on an older version | same prompt: it reads the `project-knowledge rules vN` marker and upgrades |
| agent reading this site | start at [`llms.txt`](https://mojzis.github.io/clauding/llms.txt) |

## Evolving

Practices on trial, not in the rules yet: [session handoff](evolving/session-handoff.md),
[ideas inbox](evolving/ideas-inbox.md). [All](evolving/README.md).

## Scaffold

Copied into target repos as-is:

- [`QA.md`](../scaffold/QA.md): tiers + `expect` in frontmatter, oracles table
- [`docs/README.md`](../scaffold/docs/README.md): index
- [`docs/architecture.md`](../scaffold/docs/architecture.md): diagram, component table, invariants
- [`docs/style.md`](../scaffold/docs/style.md): writing rules
- [`docs/tags.md`](../scaffold/docs/tags.md): seed vocabulary
- [`docs/adr/0000-template.md`](../scaffold/docs/adr/0000-template.md)
- [`docs/papercuts/_template.md`](../scaffold/docs/papercuts/_template.md)

## This site follows its own rules

Its [architecture](../docs/architecture.md), [decisions](../docs/adr/) and [papercuts](../docs/papercuts/)
are published alongside. Source: [github.com/mojzis/clauding](https://github.com/mojzis/clauding).
