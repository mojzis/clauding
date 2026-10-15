---
title: "0001: Manifesto lives in its own repo, not in aesop"
tags: [meta, site]
code: [content/]
status: accepted
supersedes:
superseded_by:
---

**Context:** aesop is the toolbox site: tools that enforce. The project-knowledge rules are
conventions agents read, with their own versioning, prompts and scaffold.

**Decision:** Separate repo (`clauding`) and site. aesop links to it.
Moving aesop's principle-style content here is undecided.

**Consequences:** Rules version independently of tool releases. Two sites to keep cross-linked.
→ reflected in [architecture](../architecture.md): purpose.

**Alternatives:**
| option | why not |
|---|---|
| section of aesop | couples conventions to tool releases; aesop's scope is tools |
| docs inside the Python template | template isn't the only consumer; existing repos need a hosted URL |
