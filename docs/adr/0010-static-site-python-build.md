---
title: "0010: Site built by a small Python script, published with raw markdown"
tags: [site]
code: [src/clauding/build.py, content/]
status: accepted
supersedes:
superseded_by:
---

**Context:** The manifesto is read by agents and humans. Pages must be fetchable as plain markdown.

**Decision:** `src/clauding/build.py` (Python-Markdown + PyYAML, no Jinja) renders `content/**` and `docs/**`
to `site/`. Every HTML page has a raw `.md` sibling; site emits `llms.txt` and `llms-full.txt`;
`scaffold/` published raw. Deployed by GitHub Actions to https://mojzis.github.io/clauding.

**Consequences:** One dependency-light script, same pattern as aesop. No theme or plugin ecosystem.
→ reflected in [architecture](../architecture.md): site.

**Alternatives:**
| option | why not |
|---|---|
| MkDocs / Zensical | heavy config; raw-md siblings and `llms.txt` need plugins |
| Jinja2 templates like aesop | one page shape; f-string template suffices |
| GitHub-rendered markdown only | no `llms.txt`, no stable site URL |
