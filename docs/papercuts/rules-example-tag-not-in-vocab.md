---
title: Rules example uses a tag the seed vocabulary lacks
tags: [rules, knowledge]
code: [content/rules/v1.md, scaffold/docs/tags.md]
status: open
---

**What happened:** the frontmatter example in `rules/v1.md` uses `tags: [billing, domain]`;
`billing` isn't in `scaffold/docs/tags.md`. An agent copying the example breaks the vocabulary rule
on its first doc. Principle pages repeat the pattern in their examples.
**Cost:** one wrong tag per adoption, until a checker exists to flag it.
**Idea for a fix:** in v2, add a comment `# billing: added to tags.md in the same change`,
or have `check` skip fenced code blocks so examples stay illustrative.
