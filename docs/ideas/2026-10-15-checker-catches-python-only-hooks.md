---
title: Checker flags adopter repos whose hook skips markdown
tags: [ideas, tooling]
---

> same gap applies to any adopter repo whose hook is Python-only

Context: found while fixing [docs-only commits passing unchecked](../papercuts/docs-commits-unchecked.md) here.

- catch-up or `check` could warn when the commit hook never sees `.md` files.
