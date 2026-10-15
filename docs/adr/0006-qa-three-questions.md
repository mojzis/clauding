---
title: "0006: QA answers three questions: tiers, expect, oracles"
tags: [qa]
code: [scaffold/QA.md, content/principles/qa.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Agents report "done" on green runs that ran the wrong subset, collected nothing,
or produced plausible garbage.

**Decision:** `QA.md` answers:
| question | mechanism |
|---|---|
| did I run the right thing | tiers + selection table |
| did it actually run | `expect` per tier: floors, skip list, warnings max, duration range |
| does it make sense | oracles: reference, invariant, bounds with units, diff vs main, negative control |

Oracles carry `status`: agents add `proposed`, only humans set `confirmed`.
Explicit "not evidence" list. Every task ends with a QA report.

**Consequences:** "Done" becomes checkable; `expect` must move in the same commit as an intended
baseline change. Humans own domain truth.
→ reflected in [architecture](../architecture.md): QA.

**Alternatives:**
| option | why not |
|---|---|
| tests green = done | misses 0 collected, skips, wrong-but-passing output |
| exact counts in `expect` | breaks on every added test; floors catch the real failure |
| agents confirm oracles | agent grades its own homework |
