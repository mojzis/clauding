---
title: Docs-only commits passed the hook unchecked
tags: [dev, papercuts]
code: [hooks/pre-commit]
status: fixed
---

**What happened:** madoqua acts on staged `.py` only; a docs-only commit was a silent no-op.
In a repo that is mostly markdown, broken links and unknown tags surfaced only in CI, after push.
**Cost:** every docs commit unverified; the site deploy would fail instead of the commit.
**Fix:** `hooks/pre-commit` runs the build + tag/scaffold tests when markdown is staged, then madoqua
([toolbox](../toolbox.md)). Same gap applies to any adopter repo whose hook is Python-only: a hint for the `check` tool.
