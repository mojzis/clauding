---
title: "0005: Controlled tag vocabulary in docs/tags.md"
tags: [knowledge]
code: [scaffold/docs/tags.md]
status: accepted
supersedes:
superseded_by:
---

**Context:** Free tags fragment (`test`, `tests`, `testing`) and stop being useful for lookup.

**Decision:** Tags only from `docs/tags.md`, one line each with meaning.
A new tag is added there in the same change. Tools show existing tags when adding.

**Consequences:** Tag lookup is reliable; vocabulary is checkable. Small friction to add a tag.
→ reflected in [architecture](../architecture.md): docs layout.

**Alternatives:**
| option | why not |
|---|---|
| free-form tags | synonyms and typos; lookup fails |
| directory hierarchy only | one file belongs to several topics |
| no tags | agents can't find related docs without reading all |
