---
title: "0011: Practices on trial live in an evolving section, outside the rules"
tags: [evolving, rules]
code: [content/evolving/]
status: accepted
supersedes:
superseded_by:
---

**Context:** New habits come up in real repos (session handoff, ideas inbox in cecil). Rules v1 is
frozen and inlined in every adopter; adding untested practices there would churn every repo.

**Decision:** `content/evolving/`: one page per practice, `status: trial`, with where it's in use and
open questions. This repo trials them itself. Graduating = an ADR + a new rules version.

**Consequences:** Rules stay small and stable; ideas get a public home early.
Adopters must opt in by hand. → reflected in [architecture](../architecture.md): rules.

**Alternatives:**
| option | why not |
|---|---|
| add to rules v2 now | untested beyond one repo; every adopter upgrades for it |
| keep only in cecil | not findable, not reusable, no shared vocabulary |
| `docs/ideas/` here | ideas are unshaped; these practices already have a shape and a trial |
