---
title: "0004: Docs point at code, never the reverse"
tags: [freshness, knowledge]
code: [scaffold/docs/README.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Docs rot when code changes. Need a checkable link between the two.

**Decision:** Frontmatter `code:` lists `path` or `path::Symbol`. One direction only.
Changing or moving anything listed → update the doc in the same commit.

**Consequences:** A checker can resolve every ref and find docs touching a diff (`touching`).
Code stays free of doc pointers.
→ reflected in [architecture](../architecture.md): docs layout.

**Alternatives:**
| option | why not |
|---|---|
| code comments link to docs | two directions to maintain; clutters code |
| bidirectional links | doubles the drift surface |
| no explicit links, rely on search | not checkable; misses renames |
