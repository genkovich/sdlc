---
name: decide-adr
description: >-
  Triggers: "ADR for {decision}", "adr for {slug}", "document the decision on
  {topic}", "lock in the decision about {X}", "MADR for {topic}",
  "/sdlc-decide-adr {slug} {title}", "create ADR for a decision", "document
  the decision", "ADR on {topic}". Use to record a post-hoc or asynchronous
  architecture decision as a MADR ADR when it was NOT captured during the
  synchronous architecture-design pass — a choice made in code, in a chat, on
  a whiteboard, or one a break-tasks / review gate flagged as missing. Confirms
  the decision is ADR-worthy via the blast-radius gate, picks the next 4-digit
  number, copies architecture-design's MADR template, and fills context /
  drivers / considered options / outcome / honest consequences. Supports a
  Proposed → Accepted review flow. Output:
  docs/features/{slug}/adr/NNNN-{title}.md. For decisions made live with the
  user, use sdlc:architecture-design — it spawns ADRs inline (Accepted).
triggers:
  - /sdlc-decide-adr
---

# Skill: decide-adr

The **post-hoc / asynchronous ADR path**. `architecture-design` spawns ADRs synchronously and marks them `Accepted` while walking the decision Socratically; `decide-adr` records a decision that *missed* that pass — already in code, agreed in a chat, sketched on a whiteboard, or flagged by a `break-tasks` / review gate as a contract with no ADR behind it. It can also run a `Proposed → Accepted` review flow when the decision still needs a reviewer's sign-off. One file = one decision; it reuses `architecture-design`'s MADR template, so there is **no second ADR format here**.

It is a recording utility, not a Socratic design stage — it does **not** run the shared Socratic loop or critic. The two shared dependencies are question phrasing and the worthiness gate:
→ [`../_shared/ask-style.md`](../_shared/ask-style.md) · [`../architecture-design/references/blast-radius-heuristic.md`](../architecture-design/references/blast-radius-heuristic.md)

## Owner

Decision author (usually the Architect or Tech Lead). A reviewer (Tech Lead, plus Security when relevant) signs off the `Proposed → Accepted` transition.

## Inputs

- `<slug>` — the feature slug, same as every earlier stage.
- `<title>` — kebab-case, describes the **decision**, not the problem (`time-sortable-ids`, not `id-strategy`).
- The decision itself + its alternatives — pulled from `sad.md` §4 Solution strategy / §9 ADR index / §11 Risks, or supplied by the user.
- **Input gate (soft).** Expects `docs/features/<slug>/` to exist, ideally with `sad.md` (decide-adr reads its §4/§9/§11 for context and drivers). If the decision is genuinely standalone — no feature folder yet — allow it, but **note the missing design context** in the ADR's Context section and warn the user, rather than refusing.

## Protocol

1. **Locate the feature.** `test -d docs/features/<slug>`. Missing → ask whether to proceed standalone (phrasing per [`../_shared/ask-style.md`](../_shared/ask-style.md)). On «yes», create `docs/features/<slug>/adr/` and flag that design context is absent. `sad.md` present → read its §4 (strategy), §9 (existing ADR index), §11 (risks); absent → note it and source context from the user.
2. **Worthiness check.** Score the decision against the **blast-radius gate** — [`../architecture-design/references/blast-radius-heuristic.md`](../architecture-design/references/blast-radius-heuristic.md) (irreversible / multi-module / has legitimate alternatives). 2-of-3 → proceed. Below the bar → tell the user it is likely inline-in-`sad.md` material, not an ADR, and confirm before writing one anyway.
3. **Dedup.** `ls docs/features/<slug>/adr/*.md 2>/dev/null`. An Accepted ADR on the same topic exists → don't duplicate: propose either editing it or a new ADR that marks the old one `Superseded by NNNN` (and stamps the old one's `status` + `updated_at`).
4. **Pick the number.** `NNNN` = (count of existing `adr/*.md`) + 1, zero-padded to 4 digits (`0001`, `0002`, …). Never reuse a number.
5. **Copy the template.** Copy [`../architecture-design/templates/adr-template.md`](../architecture-design/templates/adr-template.md) → `docs/features/<slug>/adr/NNNN-<title>.md`. This is the canonical MADR shape, owned by `architecture-design` and referenced here — do not invent a variant. Patch frontmatter: `owner`, `updated_at: <today>`, `feature_size` (from `.size` if present), `ticket`.
6. **Context.** 2–4 sentences: what forced this decision (an NFR, an incident, a constraint), and — if `sad.md` is absent — an explicit note that there is no design document, so the context is reconstructed from the author.
7. **Decision drivers.** Bullets — the quality goals / constraints that pushed the choice, each traceable to a real source (PRD §NFR, `sad.md` §2 Constraints, a §1 top-3 quality goal). Don't invent drivers; they filter out pet decisions.
8. **Considered options.** List **all** serious options (≥2 — one option is a declaration, not a decision), one line each with its trade-off. No strawman (an option an existing constraint already rules out).
9. **Decision outcome.** «Chosen: <option>» + 1–2 sentences on why it won, citing the drivers above.
10. **Consequences.** Positive **and** Negative **and** Neutral — cons included, or it's rationalisation, not a record. Name what changes in the codebase, ops, monitoring, onboarding. `<!-- TBD -->` only where a number honestly needs a spike.
11. **Status.** `Proposed` while a reviewer still has to sign off; `Accepted` once final. Run the review flow when needed: write `Proposed`, fill `reviewers`, and on sign-off flip to `Accepted` and bump `updated_at`. A reader six months on must be able to tell a live plan from a settled fact.
12. **Close the loop.** Add a row to `sad.md` §9 ADR index (and link from `tasks/_epic.md` if the ADR scopes a specific task). The ADR's own `## Links` must point up to the PRD + the relevant `sad.md` §N — no orphans.
13. **Propose commit + handoff.** `adr: <slug> NNNN <title>`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) (utility variant) — *What I did* + *Review* (`adr/NNNN-<title>.md`) + *Run next*: resume the gate that needed it (`/sdlc-break-tasks <slug>` or `/sdlc-plan-tests <slug>`); `/clear` optional.

## Definition of Done

- `docs/features/<slug>/adr/NNNN-<title>.md` exists in architecture-design's MADR format (frontmatter + Context + Decision drivers + Considered options + Decision outcome + Consequences + Links).
- `NNNN` is correct (existing count + 1, 4-digit) and the title is in **decision-form** (`0007-time-sortable-ids.md` ✓ vs `0007-id-strategy.md` ✗).
- `status` is explicit — `Accepted` (final) or `Proposed` (reviewer pending, `reviewers` filled).
- ≥2 considered options, no strawman; Consequences carry real Negatives, not only Positives.
- Linked both ways: a row in `sad.md` §9 (when `sad.md` exists) and the ADR's `## Links` point up to PRD + sad §N. A genuinely standalone ADR notes the missing design context instead.
- Dedup ran; a same-topic prior decision is `Superseded by NNNN`, never silently duplicated.

## Anti-patterns

- **Using this for a live decision.** A choice made *now* with the user belongs in `architecture-design` (spawned inline, `Accepted`); `decide-adr` is for what missed that pass.
- **ADR without options.** «We chose X» with no alternatives is a declaration. List ≥2 serious options; no strawman.
- **ADR as a changelog.** «Tried it, didn't work» is a news feed, not a decision record.
- **ADR as a PRD.** Acceptance criteria / NFRs don't live here — an ADR is trade-off and reasoning. That detail is in `PRD.md` / `data-model.md` / contracts.
- **No status.** A reader six months on can't tell a current plan from an old decision.
- **Problem-form title** (`0007-id-strategy.md`) — in the §9 index it's unclear which decision exists. Use the decision (`0007-time-sortable-ids.md`).
- **All-positive consequences** — an honest ADR names its Negatives and Neutrals too.
- **Reinventing the template.** Reuse [`../architecture-design/templates/adr-template.md`](../architecture-design/templates/adr-template.md); a second ADR format fragments the genre.
- **Orphan ADR.** Written but not in §9 and with no `## Links` up to PRD/sad — six-month archaeology can't find it.

## References & template

- [`../architecture-design/templates/adr-template.md`](../architecture-design/templates/adr-template.md) — the canonical MADR scaffold this skill copies and fills (owned by `architecture-design`; **do not** duplicate it here).
- [`../architecture-design/references/blast-radius-heuristic.md`](../architecture-design/references/blast-radius-heuristic.md) — the 3-criteria worthiness gate (irreversible / multi-module / legitimate alternatives); same gate `architecture-design` runs, applied here to confirm the decision earns an ADR.
- [`../_shared/ask-style.md`](../_shared/ask-style.md) — phrasing for the standalone-confirm, worthiness-borderline, and Superseded questions.

## Example invocation

> **User:** «ADR for time-sortable-ids on checkout-discounts — `break-tasks` flagged a missing ADR for the id-generation choice»
> **Skill:** `docs/features/checkout-discounts/` exists with `sad.md` → reads §4/§9/§11. Blast-radius: id strategy is irreversible (a switch later needs a backfill across every row) + multi-module (other modules read the ids) → 2-of-3, proceed. `ls adr/` → `0001`, `0002` exist → `NNNN = 0003`. Title `0003-time-sortable-ids.md` (decision-form). Copies `../architecture-design/templates/adr-template.md`. Context: the §11 risk on hot-row contention forced an explicit id choice. Drivers: PRD NFR (predictable ordering) + the existing capability in the stack. Options: (a) time-sortable ids generated in the app; (b) database auto-increment; (c) random ids. Outcome: «Chosen: (a)» — keeps natural ordering without a central sequence; (b) couples to one writer, (c) loses ordering. Consequences: + ordered without coordination; − slightly larger ids than auto-increment; neutral: switching later needs a backfill. Status `Accepted`. Adds a §9 row, fills `## Links`. Commit `adr: checkout-discounts 0003 time-sortable-ids`.
