---
title: "0002: Rules are inlined in each repo, with a version marker"
tags: [rules, adoption]
code: [content/rules/v1.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Agents must follow the rules on every task, offline, without a fetch step.
The rules are short (~50 lines).

**Decision:** Each repo copies the rules section into `AGENTS.md`. Line 1 is
`<!-- project-knowledge rules vN — canonical: <url> -->`. The rationale stays on the site, linked.
Published versions (`content/rules/vN.md`) are immutable; changes ship as a new version.

**Consequences:** Rules are always in context. Drift is detectable by the marker;
the catch-up prompt upgrades from vN to vM.
→ reflected in [architecture](../architecture.md): rules.

**Alternatives:**
| option | why not |
|---|---|
| link only, agent fetches at runtime | network dependency; agents skip the fetch; content changes under you |
| git submodule / package | heavy for 50 lines; agents don't read vendored dirs |
| inline without marker | can't tell which version a repo follows |
