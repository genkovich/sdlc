---
name: clarify-prd
model: opus
effort: high
agents: [devils-advocate]
description: >-
  Use to run an ambiguity sweep over a written PRD.md and close every under-specified
  point before glossary or architecture proceeds — so two engineers can't reasonably build
  different things from the same PRD. Triggers on "/sdlc-clarify-prd {slug}",
  "clarify {slug}", "find ambiguities in {slug}", "is the PRD ready",
  "sharpen the PRD", "прояснити PRD", "знайди неоднозначності {slug}", "чи готова специфікація".
  Re-reads the PRD, dispatches a clean-context devil's-advocate subagent to list where the
  PRD forks, then for each ambiguity runs AskUserQuestion to RESOLVE it (tighten §1/§5/§6
  in place) or DEFER it (→ §8 Open questions with owner+due). Output: an updated
  docs/features/{slug}/PRD.md with every ambiguity resolved or deferred — none dangling.
  Hard-refuse if PRD.md is missing.
triggers:
  - /sdlc-clarify-prd
  - "clarify"
  - "find ambiguities in"
  - "is the PRD ready"
  - "sharpen the PRD"
stage: "03"
---

# Skill: clarify-prd (SDLC stage 03 — PRD ambiguity sweep)

Ambiguity sweep over a written `PRD.md`. It hunts the PRD for under-specified points — vague terms, unmeasured NFRs, AC missing error/authz/edge behavior, unstated assumptions, conflicting requirements, undefined domain terms, missing actors, scope creep — then dispatches a **clean-context devil's-advocate subagent** that re-reads the PRD fresh and answers one question: *where would two engineers reasonably build different things from this?* Each ambiguity it surfaces is closed with the user: either **resolved** (the PRD is tightened in place) or **deferred** (a §8 Open-Questions row with owner + due). It exists so `fix-term` / `architecture-design` never proceed on an ambiguous PRD.

This is a sweep, not a full authoring stage — it does **not** run the shared Socratic loop or the coherence critic. Its shared dependencies:
→ [`../_shared/ask-style.md`](../_shared/ask-style.md) (resolve/defer question phrasing) · [`../_shared/interview-depth.md`](../_shared/interview-depth.md) (sweep aggressiveness + per-finding question volume) · [`../_shared/agent-roster.md`](../_shared/agent-roster.md) (dispatch discipline).

Depth governs how aggressively the sweep hunts + the per-finding question volume. (Every surfaced ambiguity is still Resolved or Deferred at every level — that's a floor, not a dial.)

## Owner

PM + Tech Lead (the PRD's co-authors resolve their own ambiguities). PM owns vague-term / scope / missing-actor calls; Tech Lead owns unmeasured-NFR / under-specified-AC / conflicting-requirement calls.

## Inputs

- `<slug>` — same feature slug used by `write-prd`.
- **Gate (hard-refuse if missing):** `docs/features/<slug>/PRD.md`. Absent → STOP and point: «run `/sdlc-write-prd <slug>` first — clarify-prd sharpens an existing PRD, it does not write one».
- (Optional) `docs/features/<slug>/CONTEXT.md` — if present, its `## Glossary` is canonical; an "undefined-term" finding for a word already glossed there is a false positive (drop it).

## Protocol

1. **Gate + set interview depth.** `test -f docs/features/<slug>/PRD.md` → missing = refuse with the pointer above. Read the PRD (and `CONTEXT.md` `## Glossary` if present, to suppress false "undefined-term" hits). **Then set the interview depth (the opening question):** read `interview_depth` from `.claude/sdlc.local.md` if present (else default medium), and — unless a `--depth=easy|medium|hard` arg was passed — ask ONE depth-selection `AskUserQuestion` phrased per [`../_shared/ask-style.md`](../_shared/ask-style.md), with the saved/medium value as the «(Recommended)» first option. The level tunes how adversarially the sweep + subagent hunt (easy: only build-divergence that changes behavior, with assumptions stated; medium: balanced; hard: adversarial, every fork surfaced) and the per-finding question volume → [`../_shared/interview-depth.md`](../_shared/interview-depth.md).

2. **First-pass self-sweep.** Walk the PRD against the eight ambiguity classes in [`./references/ambiguity-checks.md`](./references/ambiguity-checks.md) (vague-term / unmeasured-NFR / under-specified-AC / unstated-assumption / conflicting-requirement / undefined-term / missing-actor / scope-creep). Note candidate findings with a `§ref` each — do not edit yet.

3. **Devil's-advocate subagent (the core mechanic).** Dispatch the `devils-advocate` agent — `subagent_type: "sdlc:devils-advocate"` (carries its own `model: opus` + `effort: high`; clean context — it never saw this conversation). Pass only the slug + the PRD path; it Reads `PRD.md` (and `CONTEXT.md`) itself — inline nothing — and returns "two engineers would diverge here" findings. The dispatch follows the contract in [`../_shared/agent-roster.md`](../_shared/agent-roster.md) (clean-isolated context, cited findings, `NO_AMBIGUITIES` if none). If `sdlc:devils-advocate` is unavailable at runtime, fall back to a `general-purpose` Agent with the prompt body in [`./references/ambiguity-checks.md`](./references/ambiguity-checks.md).

4. **Merge + dedupe.** Union the self-sweep (step 2) with the subagent findings (step 3); collapse duplicates (same `§ref` + same class). Keep the highest-impact first (conflicting-requirement > under-specified-AC > unmeasured-NFR > undefined-term > missing-actor > scope-creep > vague-term > unstated-assumption). If the merged set is empty → report «PRD is unambiguous», stamp nothing, suggest `fix-term` / `architecture-design`.

5. **Resolve or defer, per finding.** For each finding, one `AskUserQuestion` phrased per [`../_shared/ask-style.md`](../_shared/ask-style.md), offering: **Resolve now** (user picks/dictates the tightening) · **Defer to §8** (→ Open-Questions row, owner + due captured in a follow-up; missing either = stays unresolved, re-ask once) · **Not an ambiguity** (false positive — drop it, e.g. a term already in CONTEXT). Every finding ends Resolved or Deferred — none dangling. **Depth tunes the question volume, not the floor:** at `easy`, the skill resolves the unambiguous, low-stakes findings itself with sensible tightenings and lists them in a stated-assumptions ledger for a batch veto, asking only the behavioral/high-stakes forks; at `hard`, it asks every finding. The «zero dangling» rule holds at every level.

6. **Write resolutions back.** Apply Resolve edits in the PRD's native section (tighten the §5 AC into business-observable form, replace a §6 adjective with a numeric target + measurement, fix a §1 term, add a missing §4 actor/US, cut a §3 scope-creep line). Append every Defer as a §8 checkbox row `- [ ] <question>? Default now: <X>. — owner: <name/role>, due: <date or stage>`. Keep a short edits-log (one line per finding: `class · §ref · resolved|deferred · before→after`).
   - **Undefined-term findings reconcile the glossary in-flow (a hard rule, at every depth).** When an `undefined-term` finding is Resolved, immediately invoke `/sdlc-fix-term <slug>` for that term — compare it against `CONTEXT.md` and add/update the definition **now**, not as a deferred note. clarify-prd never resolves a term by inventing a meaning inline; the canonical definition lands in `CONTEXT.md` so `architecture-design` / downstream stages read one source.

7. **Stamp + commit.** Set `updated_at: <today>` in the frontmatter. Re-respect `write-prd`'s invariants when tightening (§5 AC stays free of HTTP/status/error-code/SQL tokens; §6 numbers carry a measurement; §4 roles only from the glossary). Propose `clarify-prd: <slug> — N resolved, M deferred`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* + *Review* (tightened `PRD.md`) + *Run next* (`/clear`, then `/sdlc-fix-term <slug>`, or `/sdlc-architecture-design <slug>` to skip the glossary).

## Definition of Done

- Every ambiguity from the self-sweep + the subagent is **Resolved** (PRD tightened in its native section) or **Deferred** (a §8 row with both owner AND due) — zero dangling.
- Resolve edits preserve `write-prd`'s contracts: §5 AC carry no HTTP/status/error-code/SQL tokens, §6 NFR rows carry a numeric target + measurement (no adjectives), §4 roles match the CONTEXT glossary.
- The devil's-advocate subagent actually ran (clean context, Read the PRD itself) — not skipped, not paraphrased into the main thread.
- `updated_at` reflects today; edits-log kept; commit proposed.

## Anti-patterns

- **Skipping the subagent** and sweeping only in-thread. The clean-context fork-finder is the core mechanic — the self-sweep is shaped by the conversation that wrote the PRD and misses its own blind spots.
- **Resolving an ambiguity unilaterally** (no `AskUserQuestion`). clarify-prd proposes; the author decides — the same user-in-the-loop contract as every SDLC stage.
- **Defer without owner+due** — a §8 row missing either is not a real defer; re-ask once, else it stays unresolved.
- **Re-running the coherence critic here.** That F1–F6 cross-section drift check belongs to `write-prd` / `architecture-design`; clarify-prd's subagent hunts *ambiguity* (build-divergence), a different target.
- **Leaking implementation into a Resolve edit** — tightening a §5 AC by adding a status code / endpoint / SQL detail. Stay business-observable; the technical mapping lives in `api-forge` / `generate-data-model`.
- **Inventing answers to fill findings.** A genuinely open point is *deferred* with an owner, not guessed — better an honest §8 row than a fabricated AC.
- **Authoring new scope.** clarify-prd sharpens what the PRD already says; a brand-new requirement goes back through `write-prd`, not in under cover of a "clarification".

## References

- [`./references/ambiguity-checks.md`](./references/ambiguity-checks.md) — the eight ambiguity classes (how to spot / how to resolve each) + the clean-context devil's-advocate subagent prompt body.
- [`../_shared/ask-style.md`](../_shared/ask-style.md) — phrasing for the resolve/defer/false-positive question.
- [`../_shared/interview-depth.md`](../_shared/interview-depth.md) — the easy/medium/hard dial set in step 1 (sweep aggressiveness + per-finding question volume).
- [`../_shared/agent-roster.md`](../_shared/agent-roster.md) — model/effort policy + the shared agent dispatch contract.
- [`../_shared/handoff.md`](../_shared/handoff.md) — the stage-handoff block format emitted at step 7.
