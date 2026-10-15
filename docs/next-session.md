---
title: Next session
tags: [handoff]
---

Where things stand and what to pick up. History: [sessions/](sessions/README.md).

## 2026-10-15: repo set up, site live, dogfooding started

- Site live at https://mojzis.github.io/clauding (Pages via Actions, deploys on push to `main`).
- Rules v1, five principle pages + QA, catch-up prompt, scaffold; ADRs 0001–0011.
- `CLAUDE.md` is just `@AGENTS.md`; toolbox in [toolbox](toolbox.md). Hook now checks staged markdown.
- New section [evolving practices](../content/evolving/README.md): session handoff, ideas inbox
  (from cecil). This file is the trial run here.
- Site has a light/dark toggle.

## Pick up

- Brief step 3: scaffold + rules section into the Python template (`~/git/python-template`).
- Brief step 4: pilot [catch-up](../content/catch-up.md) on one existing repo; papercuts on this repo.
- Open papercuts: [example tag](papercuts/rules-example-tag-not-in-vocab.md),
  [catch-up vs inline fix](papercuts/catch-up-vs-inline-fix.md). Both are rules v2 candidates.
- Open questions in [brief](brief.md) and on the evolving pages.
- CI warnings: actions on Node 20 (checkout@v4, setup-uv@v5); `ubuntu-latest` → 26 on 2026-10-19.
