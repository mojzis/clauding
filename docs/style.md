---
title: Writing style for docs
tags: [meta]
code: []
---

Readers are agents and busy humans. Every word costs context.

**Density**
- Lead with the point. No intros, no "this document describes", no summaries of what follows.
- Fragments are fine. Cut every word that carries no information.
- One fact, one place. Link instead of restating.
- Don't paraphrase code. Point at it with `code:` and add only what the code can't say:
  why, invariants, gotchas.

**Shape over prose**
| content | use |
|---|---|
| flow, sequence, dependencies | mermaid `flowchart` / `sequenceDiagram` |
| lifecycle, statuses | mermaid `stateDiagram-v2` |
| data shapes, contracts | schema block (typed fields, units, nullability) |
| comparisons, options, mappings | table |
| steps | numbered list, one action each |
| reasoning, trade-offs | short prose, the only place for it |

**Precision**
- Concrete names: real modules, tables, fields, commands. No "the service", "various components".
- Units and ranges on every number. Say what's guaranteed and what's merely usual.
- A short example beats a long explanation.

**Hygiene**
- No dates or "recently" in current-state docs. Git has the history; ADRs have the why.
- No TODOs in docs. Log a papercut instead.
- If a section needs a heading to be findable, it probably wants its own file.
