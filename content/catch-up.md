---
title: Catch-up prompt
tags: [adoption]
---

Paste into an agent session at the root of an existing repo.

---

Bring this repo in line with the project-knowledge rules at https://mojzis.github.io/clauding/rules/v1/ (rationale: https://mojzis.github.io/clauding/llms.txt).

1. Read the rules. Check `AGENTS.md` / `CLAUDE.md` for a `project-knowledge rules vN` marker.
   - No marker: full adoption (steps 2–8).
   - Older version: apply only what changed between versions, then bump the marker.
2. Add the rules section to `AGENTS.md`. If `CLAUDE.md` exists, have it reference
   `AGENTS.md` rather than duplicate it.
3. Copy the scaffold: `QA.md`, `docs/style.md`, `docs/tags.md`, `docs/adr/`, `docs/papercuts/`.
   Read `docs/style.md` now. It governs everything you write below.
4. **`QA.md`** (one per subproject in a monorepo):
   - Find the commands in CI config, `pyproject.toml`, Makefile/justfile. CI is the reference.
   - **Run every tier you can.** Fill `expect` only from what you observed.
     Never write an expectation you didn't see.
   - A tier that fails or can't run now becomes a papercut. Don't fix it in this pass.
   - Propose oracles from the code and data: invariants, bounds, candidate reference cases.
     All go in as `status: proposed`. List them in the report for a human to confirm.
5. **`docs/architecture.md`:** if missing, write it from the code as it is today.
   This is the baseline. Describe only what you can verify in the code and don't guess at intent.
   Do not write ADRs for past decisions. ADRs start from here.
6. **Existing docs:** split into one-concept files, add frontmatter, add `code:` refs
   you've verified exist, and link related files. Tighten them to the style,
   but keep the facts.
7. **Tags:** derive 10–20 tags from what the docs actually cover.
   Write them into `docs/tags.md`, one line each.
8. Log as papercuts anything that confused you during this pass.
9. Report: files created or split, tiers run and their observed results, proposed oracles,
   tags chosen, papercuts logged, open doubts.

Make it one commit (or a small series), separate from code changes.
