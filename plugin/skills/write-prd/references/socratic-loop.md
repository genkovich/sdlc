# write-prd — delta over the shared Socratic loop

Read [`../../_shared/socratic-loop.md`](../../_shared/socratic-loop.md) for the canonical 4-state machine, edits-log, and disk-write discipline. write-prd supplies only the deltas below.

## Sections walked (in order)

§4 User stories → §5 Acceptance criteria → §6 NFR → §7 KPIs. §1–§3 are drafted and shown but not per-item walked (they have no decision set — the user edits them inline if needed).

## Decision-types

- **User story** (§4) — Approve / Edit / Drop / Save-as-OQ. Dropping a US that owned the only AC of a coverage type triggers the §5 coverage gate (a). Dropping the **entire** US is a legitimate de-scope and does not fire the use-case floor (b) — only a retained US losing its last AC does.
- **Acceptance criterion** (§5) — the 4-state machine **plus a 5th option «Add another AC»** (user dictates a new AC; skill drafts it in business form and runs a one-question mini-batch on it). Dropping / OQ-migrating the **last AC of a retained §4 user story** fires the use-case floor below (regenerate an AC for that US).
- **NFR row** (§6) — Approve / Edit (change the number or measurement) / Save-as-OQ (number is TBD, owner+due mandatory). A bare adjective («fast») is never Approvable — force a number or an OQ.
- **KPI** (§7) — Approve / Edit / Drop. baseline=TBD forces an inline measurement plan or an OQ.

## Per-skill gate — §5 coverage floors (two, both re-checked after every resolution)

After every §5 resolution, re-check **both** floors below (OQ-migrated AC do NOT count toward either — they live in §8 now). Both hold at every interview depth.

1. **Coverage-type floor.** At least one AC of each of the 5 coverage types (happy / error / authorization / domain invariant / cross-context) still stands after drops + OQ-migrations. If a type is empty, regenerate a replacement AC of that type and run a one-question mini-batch.

2. **Use-case floor (§4 US → at least one §5 AC).** **Every *retained* §4 user story still has at least one acceptance criterion.** If a Drop / OQ-migration leaves a retained US with no AC, regenerate (or use the «Add another AC» option) an AC for that US and run a one-question mini-batch — a user story with no AC is incomplete and silently breaks the downstream `complete-sequence-diagrams` use-case coverage and `review-feature` end-to-end trace. (Dropping the **whole** US is a legitimate de-scope and does not fire this floor — only a retained US losing its last AC does.) This also applies at **draft time**: if the initial §5 draft gave some §4 US no AC, add one before the walk begins.

## Open-Questions table

`save_as_oq` rows land in **§8 Open questions** as a checkbox line:
```
- [ ] <headline>? Default now: <default-if-known>. — owner: <name/role>, due: <YYYY-MM-DD or stage trigger like "before /sdlc-break-tasks">
```
Owner + due are **mandatory** — skill issues a follow-up `AskUserQuestion` immediately after the user picks `Save-as-OQ` to capture both. Missing either downgrades to `Drop` with an explicit warning.

## Edits-log schema (write-prd specifics)

```
{item_id:    "US-06" | "AC-04" | "NFR-row-2" | "KPI-01",
 action:     "edit" | "drop" | "add" | "save_as_oq",
 before:     "<verbatim text of the item before user action, or null for add>",
 after:      "<verbatim text after — for save_as_oq this is the §8 entry incl. owner+due; null for drop>",
 user_reason:"<the rationale the user provided, verbatim>"}
```

`Approve` items do **not** go into the log — they are the baseline. The log is the **sole** signal the clean-context critic uses to detect upstream-coherence drift.

## Contract

Per-section batch, not per-item-across-sections. For each section in order:

1. **7a. Render the full proposed section** in one message — body text + numbered list of decisions. The user sees the whole shape before any per-decision commitment.
2. **7b. Walk per-item resolutions** — one `AskUserQuestion` per item (4-state machine; 5-state for §5 AC).
3. **7c. Apply transitions** to the in-memory draft as each resolution arrives.
4. **7d. Run the coverage gate** (§5 only) — after all resolutions, verify both floors. If either is broken, regenerate a replacement AC and run a mini-batch. Loop until both floors hold or user `Save-as-OQ`-s the regenerated AC (critic handles it downstream).
5. **7e. Repeat for the next section.** The skill never returns to a previous section — cross-section drift is the critic's job.

On-disk artifacts are not touched until a section is resolved. Then write to disk + commit one bundled commit per section.

## Exit condition

Step 7 completes when:

- All 4 sections (§4 US, §5 AC, §6 NFR, §7 KPI) have been batch-rendered (7a) and walked (7b) with one resolution per item.
- The in-memory draft reflects every `Edit`/`Drop`/`Add`/`Save as OQ` resolution; `Save as OQ` items appear in §8 with owner+due.
- Both §5 coverage floors (7d) are closed.
- The edits-log has no pending entries.

Then proceed to step 8 (see [`critic.md`](./critic.md)).

For concrete question wording and option descriptions, see [`ask-examples.md`](./ask-examples.md) (junior-friendly Ukrainian shape).
