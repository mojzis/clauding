---
title: Dev toolbox
tags: [dev]
code: [pyproject.toml, hooks/pre-commit]
---

Checks and their tiers: [QA.md](../QA.md). This page: the tools behind them and their gotchas.
Every tool explains itself: `uv run <tool> guide`, and `guide tune` before changing a threshold.
Source: [aesop toolbox](https://mojzis.github.io/aesop/llms.txt).

**Fresh clone**
```
uv sync
uv run madoqua install && git checkout hooks/pre-commit   # core.hooksPath is local config; install overwrites our shim
```

**Commit hook** (`hooks/pre-commit`)

| staged | runs | blocks on |
|---|---|---|
| `.py` / `.pyi` | madoqua fix: `ruff check --fix`, `ruff format` (re-staged) | — |
| `.py` / `.pyi` | madoqua check: `ruff check`, `ty check` (staged only), `biston`, `zorilla`, `gerenuk run` | any failure |
| `.md` under `content/`, `docs/`, `scaffold/`, or root `*.md` | `build` (links, frontmatter) + tag/scaffold tests | broken link, bad YAML, unknown tag |

~0.3 s each. Never `--no-verify` / `MADOQUA_SKIP` past a check that's telling the truth.
Security lint is ruff `S` (no bandit); `tests/**` ignores S101/S105/S106.

**Other commands**

| command | for |
|---|---|
| `uv run poe fix` | format + autofix everything |
| `uv run poe check-all` | everything incl. dead code (vulture), unused deps (deptry) |
| `BASE_URL= uv run build && python -m http.server -d site` | local preview, root-relative links |
| `uv run tyf find/refs/list/calls <sym>` | symbol lookup; **use instead of grep** for definitions/references |
| `uv run gerenuk audit <file>` | symbols nothing references |
| `uv run gerenuk impacted-tests` | which tests the diff reaches, and why |
| `uv run pycoati . --format pretty` | test-suite suspicion audit before a cleanup; never in hook/CI (runs suite 3×) |

**Refresh the toolbox**
```
uv lock --refresh --upgrade-package madoqua --upgrade-package gerenuk --upgrade-package biston --upgrade-package zorilla --upgrade-package pycoati --upgrade-package ty-find && uv sync
```
`--refresh` matters: without it uv may serve a stale index.

**Gotchas**
- ty is beta: prefer `# ty: ignore[rule]` over blanket suppression. `uv run poe typecheck` is repo-wide; the hook isn't.
- gerenuk diffs the **working tree** vs `origin/main`: unstaged edits count; touching `pyproject.toml`/`uv.lock` runs the full suite. `--base HEAD` scopes to the commit.
- ty-find index goes stale after the hook's `ruff format`. Tell: `tyf refs` lists only the definition, or gerenuk `selected` is empty. Fix: `uv run tyf daemon restart`.
- `ruff format` can wrap a line and move a trailing `# zorilla: ignore` off the flagged line.
