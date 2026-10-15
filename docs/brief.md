---
title: 'Brief: project-knowledge rules ("agentic engineering manifesto")'
tags: [meta]
---

The handoff doc for building this. Read it first, then the files it points to.

## Goal

Every project, repo or subproject, follows one set of rules that keeps its knowledge
agent-usable and its "done" provable:

| rule | lives in | purpose |
|---|---|---|
| QA | `QA.md` at the project root | how to run checks; how to tell the result makes sense |
| current architecture | `docs/architecture.md` | how the system is *now* |
| decisions | `docs/adr/NNNN-slug.md` | changes from the architecture baseline onward |
| papercuts | `docs/papercuts/slug.md` | friction hit by agent or human |
| writing style | `docs/style.md` | dense; diagrams and schemas over prose |
| small linked tagged docs | `docs/**` + `docs/tags.md` | one concept per file, controlled tag vocabulary |
| freshness | frontmatter `code:` refs | docs point at code; change code → update doc in the same commit |

Premise: strong models follow short rules well. Text gets most of the way;
a small checker covers the rest.

## Deliverables

1. **Manifesto repo/site** (new, not part of aesop). A garden of small pages, not a blog.
   Published like aesop (GitHub Pages + `llms.txt`). Dogfoods its own rules:
   small tagged files, its own ADRs and papercuts.
   Holds: one principle page per rule, the catch-up prompt, the scaffold, a versioned rules text.
2. **Python template:** ships the `AGENTS.md` rules section + scaffold.
3. **Existing repos:** a hosted catch-up prompt, pasted into an agent session.
   It reads the version marker → full adoption or upgrade.
4. **Checker tool** (later): see Tooling.

## Files in this bundle

```
AGENTS-section.md        rules text, inlined into each repo's AGENTS.md (version marker on line 1)
catch-up-prompt.md       adoption/upgrade prompt for existing repos
manifesto/
  qa-principles.md       principle page: QA (the only page written so far)
scaffold/                copied into target repos as-is
  QA.md                  template; tiers + expect live in frontmatter
  docs/README.md         index
  docs/architecture.md   template: diagram, component table, invariants
  docs/style.md          writing rules
  docs/tags.md           seed vocabulary
  docs/adr/0000-template.md
  docs/papercuts/_template.md
```

Moved since: `manifesto/qa-principles.md` → `content/principles/qa.md`, `AGENTS-section.md` → `content/rules/v1.md`,
`catch-up-prompt.md` → `content/catch-up.md`, `scaffold/` → `scaffold/`. Current layout: [architecture](architecture.md).

`<MANIFESTO_URL>` was a placeholder; it is now `https://mojzis.github.io/clauding` ([ADR 0010](adr/0010-static-site-python-build.md)).

## Decisions made

- **Separate repo from aesop.** aesop = tools that enforce; manifesto = conventions agents read.
  aesop links to the manifesto. aesop's principle-style content may move over (undecided).
- **Rules are inlined in each repo** (they're short) with a version marker and a link
  for the rationale. Copy plus marker beats fetching at runtime.
- **No backfilled ADRs.** Missing `architecture.md` → write it from the code as the baseline;
  ADRs start from there. Accepting an ADR means updating `architecture.md` in the same change.
- **Docs → code links only**, as `path::Symbol` in frontmatter `code:`. One direction, checkable.
- **Controlled tag vocabulary** in `docs/tags.md` (the braindump idea: show existing tags when adding).
- **QA has three questions:** did I run the right thing (tiers), did it actually run
  (`expect`: floors, skip lists, duration range), does it make sense (oracles).
  Oracles: reference cases, invariants, bounds with units, diff vs main (explain every diff),
  negative control. Agents propose oracles (`proposed`); only humans confirm.
  An explicit "not evidence" list. Every task ends with a QA report.
- **Catch-up never invents:** it runs QA tiers and records only what it observed,
  writes architecture only from verifiable code, and logs failures as papercuts without fixing them.
- **`QA.md` sits at the project root**, not in `docs/`. It's operational, like the README.

## Tooling

Markdown is the only source of truth. The tool is a disposable view over it.
- **No stored index.** Parse on every call; repo docs are small. Agents and humans edit files
  directly, so any index would go stale.
- Zero-install CLI (`uvx`), with a `guide` subcommand, same pattern as aesop tools.

| command | does | priority |
|---|---|---|
| `check` | `code:` refs resolve (path + symbol); relative links resolve; tags in vocabulary; frontmatter present; size limit; accepted ADR ⇒ architecture.md touched in the same commit | 1 |
| `qa run <tier>` | run the tier from `QA.md` frontmatter, parse the summary, compare to `expect` | 1 |
| `touching <paths>` | docs whose `code:` covers the given paths; for the staged diff in a commit hook | 2 |
| `tags` | vocabulary with usage counts | 2 |
| `links` / `orphans` | backlinks; unlinked files | 3 |
| search | **don't build**; agents use ripgrep | — |

## Open questions

- Repo and site name. Whether the checker lives in aesop or next to the manifesto.
- Large repos: `architecture.md` will exceed ~150 lines and should become an index plus per-component files.
  Write that as an ADR once it actually happens.
- Data pipelines: reference cases need small, realistic, commit-safe fixtures.
  Do they exist, or is producing them part of adoption?
- Exact `QA.md` frontmatter schema (keys, units) before the tool depends on it.
- Papercuts: keep fixed ones (current default) or delete them.

## Suggested build order

1. Manifesto repo: move `manifesto/` + `scaffold/` + rules + prompt in. Write the remaining principle
   pages in `docs/style.md` style (architecture, adr, papercuts, docs & tags, freshness).
   Add an `llms.txt` and publish.
2. Write the repo's own first ADRs for the decisions above. These are real ones, made now.
3. Put the scaffold + rules section into the Python template.
4. Pilot the catch-up prompt on one existing repo. Log what went wrong as papercuts
   on the manifesto and revise the prompt.
5. Checker: `check` + `qa run`, then `touching` in a commit hook.
