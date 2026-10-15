---
title: "QA: evidence, not a green checkmark"
tags: [qa, principle]
---

An agent saying "done" is a claim. `QA.md` is what turns it into evidence.

## Three questions

Every `QA.md` must let an agent answer all three, without asking a human.

| question | failure it prevents | answered by |
|---|---|---|
| Did I run the right thing? | fast subset where the change needed full; wrong package | tiers + selection table |
| Did it actually run? | 0 collected, swallowed import error, everything skipped, early exit, stale cache | `expect` baseline per tier |
| Does the result make sense? | green tests, wrong output: empty, doubled, off by 1000× | oracles |

## 1. Tiers: what to run

Named tiers with a command and a trigger, for example `fast` for every change, `full` before merge,
and `slow`/`e2e` when a boundary changes. There's also a selection table mapping kinds of change to a tier.
Commands must match CI. A mismatch between the two is a papercut.

## 2. Expect: proof it ran

A baseline per tier, stated as **floors and lists**, not exact numbers:

```yaml
expect:
  collected_min: 400        # a sudden drop means collection broke
  skips: [test_s3_live]     # any other skip is a failure
  warnings_max: 5
  seconds: [20, 90]         # too fast is as suspicious as too slow
```

If a change moves the baseline on purpose, update `expect` in the same commit.
This is the same freshness rule as for docs.

## 3. Oracles: does it make sense

Ordered from strongest to weakest:

| kind | example | catches |
|---|---|---|
| reference case | `fixtures/inv-2024-03` → known totals | wrong logic |
| invariant | Σ in = Σ out; rows after left join = rows left; key unique | lost or duplicated data |
| bounds with units | spot price −500…5000 EUR/MWh; daily volume 10–40 GWh | unit and scale errors |
| diff vs main | same input through both versions; **every diff must be explained by the change** | unintended side effects |
| negative control | a new check is seen failing once before it passes | checks that can't fail |

**Provenance:** `confirmed` means a human vouched for it. `proposed` means an agent derived it from code or data.
Agents may propose oracles. They never promote them to confirmed. Domain truth comes from humans.

## Not evidence

- reasoning about the code ("this should work")
- tests edited in the same change until they pass, meaning assertions got weakened
- a mock replacing the unit under test
- new `skip` / `xfail` added to get green
- "output exists", because non-empty doesn't mean correct
- a run against a different commit, a dirty cache, or a partial selection reported as full

## QA report

Every task ends with this. A missing line reads as "not done".

```
qa:      fast ✓ 412 passed, 1 skipped (expect ≥400, skip listed) 41s
oracles: ref inv-2024-03 ✓ · conservation ✓ · diff vs main: 2 rows, explained: rounding fix (adr/0007)
not run: e2e (needs VPN), human to run before merge
```

## Layout

- `QA.md` at each project root, and in each subproject of a monorepo.
- The root `QA.md` lists the subprojects and says what to run for cross-cutting changes.

## Tooling

The `tiers` in frontmatter are machine-readable on purpose.
- *Did it run?* A tool can fully automate this: run the tier, parse the summary, compare it to `expect`.
- *Does it make sense?* Partially: executable oracles run, and the diff vs main can be produced;
  explaining the diff stays with the agent.
