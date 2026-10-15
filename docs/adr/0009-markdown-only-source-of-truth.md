---
title: "0009: Markdown is the only source of truth; checker keeps no index"
tags: [tooling]
code: []
status: accepted
supersedes:
superseded_by:
---

**Context:** Agents and humans edit docs directly. A planned checker CLI (`check`, `qa run`,
`touching`, `tags`, `links`) needs to read them.

**Decision:** The checker parses files on every call. No stored index or cache.
Zero-install (`uvx`), with a `guide` subcommand like aesop tools. No search command: agents use ripgrep.

**Consequences:** Never stale; no sync step. Fine while repo docs are small (hundreds of files).
→ reflected in [architecture](../architecture.md): tooling.

**Alternatives:**
| option | why not |
|---|---|
| stored index (SQLite/JSON) | goes stale on every direct edit |
| docs in a database, rendered to md | agents and git diff work on files |
| built-in search | ripgrep already does it |
