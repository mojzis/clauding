---
title: "Session handoff: next-session.md + sessions/"
tags: [evolving, handoff]
status: trial
---

`docs/next-session.md` says where the work stands and what to pick up. Read it first.
At the end of a session it moves to `docs/sessions/` and a new one is written.

## Why

| without it | failure |
|---|---|
| state lives in the chat | the next session (or another agent) re-derives it from git log and code |
| one ever-growing handoff file | "now" buried under weeks of past; agents read stale lines as current |
| handoff rewritten in place | what a session concluded is gone; git diff is the only trace |

## Shape

```
docs/
  next-session.md                 now only: state + what to pick up, short
  sessions/
    README.md                     the rules below
    2026-10-14-1-mirror-molecules-mended.md
    2026-10-14-2-notes-round-5.md
```

`next-session.md`:

| section | holds |
|---|---|
| `## <date>: <what happened, in a few words>` | this session's outcome: what changed, what's live, what was left as is and why |
| `## Still open from earlier` | unresolved items from past sessions, one line each, linked to the session file |

Session file name: `YYYY-MM-DD-<n>-slug.md`; `<n>` orders several sessions on one day;
the slug names the outcome, not the task.

## Rule

1. **Start:** read `next-session.md`, then the docs it links. It's the entry point, before `docs/README.md`.
2. **End:** `git mv docs/next-session.md docs/sessions/<date>-<n>-<slug>.md`. Move the file;
   don't copy it piece by piece.
3. Write a new `next-session.md`: only where things stand now. Carry unresolved items forward
   as one-liners linking into `sessions/`. Drop resolved ones.
4. Commit with the session's last change.

`sessions/` is history: never edited after the move.

## Boundaries

| file | is about | tense |
|---|---|---|
| [`architecture.md`](../principles/architecture.md) | the system | how it is |
| [ADR](../principles/adr.md) | one decision | why it changed |
| `next-session.md` | the work | where it stands, what's next |
| `sessions/*` | past work | where it stood |
| [papercut](../principles/papercuts.md) | friction | what hurt |

A fact that outlives the session (a decision, an invariant) goes into its own doc;
`next-session.md` links to it.

## Open

- Frontmatter and tags on session files: rules say every doc; cecil's have none.
  This repo gives them `title` + `tags: [handoff]`.
- Who writes it: the agent at "wrap up", or a hook/command. Today: by hand, prompted.
- Subprojects: one `next-session.md` per repo, or per subproject like `QA.md`.
