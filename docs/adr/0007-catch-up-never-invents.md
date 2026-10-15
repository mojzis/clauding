---
title: "0007: Catch-up records only what it observed"
tags: [adoption]
code: [content/catch-up.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Adopting the rules in an existing repo tempts the agent to fill templates with
plausible guesses: expectations it never saw, architecture it inferred.

**Decision:** The catch-up prompt runs every QA tier it can and writes `expect` only from observed runs;
writes `architecture.md` only from verifiable code; logs failing tiers as papercuts without fixing them;
proposes oracles as `proposed`. Separate commit from code changes.

**Consequences:** Baseline is honest, possibly incomplete. Fixes come later as normal work.
→ reflected in [architecture](../architecture.md): adoption.

**Alternatives:**
| option | why not |
|---|---|
| fill templates from intent/README | unverified claims become "docs" |
| fix failures during adoption | mixes knowledge capture with code change; unreviewable |
