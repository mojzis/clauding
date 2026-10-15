---
title: "0003: Architecture baseline; no backfilled ADRs"
tags: [adr, architecture, adoption]
code: [scaffold/docs/architecture.md, scaffold/docs/adr/0000-template.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Existing repos have years of undocumented decisions. Reconstructing them means guessing intent.

**Decision:** Missing `architecture.md` → write it from the code as it is: the baseline.
ADRs record changes from the baseline onward. Accepting an ADR means updating
`architecture.md` in the same change.

**Consequences:** Adoption is bounded and verifiable. Past "why" is lost unless a human writes it.
`architecture.md` is always current; ADRs carry history.
→ reflected in [architecture](../architecture.md): docs layout.

**Alternatives:**
| option | why not |
|---|---|
| backfill ADRs from git history | agent invents rationale; unverifiable |
| ADRs only, no current-state doc | reader must replay history to learn the present |
| architecture doc only | loses the why of each change |
