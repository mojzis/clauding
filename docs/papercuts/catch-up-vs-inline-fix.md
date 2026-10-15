---
title: "Catch-up says don't fix; rules say fix trivial ones inline"
tags: [adoption, papercuts]
code: [content/catch-up.md, content/rules/v1.md]
status: open
---

**What happened:** rules: "Fix inline only if trivial." Catch-up: failing tiers become papercuts,
"Don't fix it in this pass." Not a contradiction (catch-up is the stricter special case),
but an agent reading both has to reconcile them itself.
**Cost:** a wrong turn per adoption run, if the agent fixes a "trivial" failure mid catch-up.
**Idea for a fix:** one line in catch-up: "This overrides the inline-fix rule for this pass."
