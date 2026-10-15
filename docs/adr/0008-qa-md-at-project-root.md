---
title: "0008: QA.md lives at the project root"
tags: [qa]
code: [scaffold/QA.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** QA is operational: what to run before claiming done. Monorepos have several projects.

**Decision:** `QA.md` at each project root, beside `README.md`, not in `docs/`.
Monorepo: one per subproject; the root one lists subprojects and cross-cutting runs.

**Consequences:** Found by agents next to the code they run. Still follows doc frontmatter rules.
→ reflected in [architecture](../architecture.md): QA.

**Alternatives:**
| option | why not |
|---|---|
| `docs/qa.md` | buried with reference docs; less likely read before "done" |
| in `AGENTS.md` | per-project commands bloat the shared rules section |
