---
title: "QA: clauding"
tags: [qa]
code: [tests/, src/clauding/build.py]
tiers:
  - name: fast
    cmd: uv run pytest -q -o addopts=
    when: every change
    expect: {collected_min: 12, skips: [], warnings_max: 0, seconds: [0.05, 10]}
  - name: site
    cmd: BASE_URL= uv run build
    when: any change to content/, docs/, scaffold/ or the build
    expect: {pages_min: 30, seconds: [0.05, 10]}
  - name: full
    cmd: uv run poe check
    when: before push
    expect: {collected_min: 12, skips: [], seconds: [1, 120]}
---

<!-- Principles: https://mojzis.github.io/clauding/principles/qa/. Tiers live in frontmatter only. -->

**Prerequisites:** `uv sync`. No services, no env vars.

**Selection**
| change | run |
|---|---|
| `content/`, `docs/`, `scaffold/` | site + fast (`fast` builds the real site and checks tags) |
| `src/clauding/build.py` | fast + site + diff vs main |
| `pyproject.toml`, `uv.lock`, CI | full |

**Oracles**
| name | kind | check | status |
|---|---|---|---|
| links resolve | invariant | `site` tier exits 0; any broken relative link fails it | proposed |
| tags in vocabulary | invariant | `tests/test_build.py::test_real_tags_are_in_vocabulary` | proposed |
| raw twin | invariant | every `site/**/index.html` has an `index.md` sibling | proposed |
| scaffold verbatim | invariant | `diff -r scaffold site/scaffold` is empty | proposed |
| page count | bounds | pages built = md files in `content/` + `docs/` − templates + generated dir listings | proposed |

**Diff vs main:** `git worktree add /tmp/main main && (cd /tmp/main && BASE_URL= uv run build)`,
then `diff -r /tmp/main/site site`. Every diff must be explained by the change.

**Project-specific non-evidence:** "the page renders" in a browser without checking links;
`site/` existing from an earlier build.

**Known flaky:** none.
