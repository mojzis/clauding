---
title: "QA: <project>"
tags: [qa]
code: [tests/]
tiers:
  - name: fast
    cmd: uv run pytest -m "not slow" -q
    when: every change
    expect: {collected_min: 0, skips: [], warnings_max: 0, seconds: [0, 60]}
  - name: full
    cmd: uv run pytest -q
    when: before merge; changes to data shapes or public interfaces
    expect: {collected_min: 0, skips: [], warnings_max: 0, seconds: [0, 600]}
---

<!-- Principles: https://mojzis.github.io/clauding/principles/qa/. Tiers live in frontmatter only. -->

**Prerequisites:** env vars, services, data. How to get each.

**Selection**
| change | run |
|---|---|
| docs only | nothing |
| anything in `src/` | fast |
| schema, IO, public API | full + diff vs main |

**Oracles**
| name | kind | check | status |
|---|---|---|---|
| | reference / invariant / bounds / diff | command or query | confirmed / proposed |

**Diff vs main:** command that runs the reference input through a given ref, and where the outputs land.

**Project-specific non-evidence:** e.g. "`--offline` mode passes trivially".

**Known flaky:** links to papercuts.
