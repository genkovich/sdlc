# Socratic loop — architecture-design's delta over the shared loop (Protocol step 6)

Read [`../../_shared/socratic-loop.md`](../../_shared/socratic-loop.md) for the canonical 4-state machine (Approve / Edit / Save-as-OQ / Drop), the edits-log schema, the cadence, and the disk-write discipline (in-memory until the section is written). architecture-design supplies only the deltas below.

## TL;DR (короткий вступ українською)

Це крок 6 у Protocol — діалог з користувачем по кожній секції SAD. Логіка:

1. Skill **малює всю секцію відразу** + нумерує рішення всередині.
2. Питає **по одному рішенню** через `AskUserQuestion`.
3. Користувач обирає одну з **4 дій з рішенням** (англ. *4-state machine*): **Прийняти** / **Виправити** / **Винести у відкрите питання** (`Save as OQ`) / **Викинути** (`Drop`).
4. Для кожного **Прийнятого** рішення skill прогоняє **3 питання масштабу удару** (англ. *blast-radius gate*). Якщо хоч 2 з 3 спрацьовують — створюється файл ADR з форматом **MADR** (markdown з заголовком, контекстом, опціями, наслідками).
5. Skill **пише секцію + ADR-файли + комітить** одним комітом. Більше до цієї секції не повертається — внутрішні протиріччя ловить окремий критик на кроці 7.

§4 **відкривається рішенням Target-surface** (що саме будуємо) — воно гейтить §5-контейнери і всі наступні стадії, тому вирішується першим. На кожну оголошену UI-поверхню йде follow-on UI-architecture рішення.

---

Goes between the in-memory draft (Step 5) and the Step-7 critic. Per-section batch validation via `AskUserQuestion` over the in-memory draft; per Approved decision a blast-radius gate; per ADR-gated decision an ADR spawn; **then** the section is written to `sad.md` + incremental commit. Section file-writes are atomic — the skill never returns to a previous section after writing it (cross-section drift caught by the Step-7 critic).

For concrete question wording + option `description` fields, see [ask-examples.md](./ask-examples.md). Cadence (mini-recap every 5, question budget per section) → [socratic-cadence.md](./socratic-cadence.md). ADR-gate scoring → [blast-radius-heuristic.md](./blast-radius-heuristic.md). Diagram confirms (§3/§5 C4) go prose-first → [`../../_shared/diagram-presentation.md`](../../_shared/diagram-presentation.md); validate each block → [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md).

## Sections walked (in order)

The 12 Arc42 sections of `sad.md`, in order:

§1 Introduction & goals → §2 Constraints → §3 Context & scope (C4 Context inline) → §4 Solution strategy → §5 Building blocks (C4 Container inline) → §6 Runtime → §7 Deployment → §8 Crosscutting → §9 Architecture decisions → §10 Quality requirements → §11 Risks → §12 Glossary.

§4 opens with the **Target-surface** decision (it gates §5's containers + every downstream stage, so it's resolved before any other §4 choice — see the decision-types catalog below). One bundled commit per section (`sad.md` edits + any ADR files the gate spawned). The skill never returns to a written section — cross-section drift is the Step-7 critic's job. Section depth follows the size matrix; even XS/S walks all 12 (more `<!-- N/A: reason -->`, see [`../../_shared/size-matrix.md`](../../_shared/size-matrix.md)).

## Contract

**Per-section batch, not per-decision-across-sections.** For each of §1 → §12 in order, the skill:

1. **6a. Renders the full proposed section** in one message — proposed body text + numbered list of decisions the section contains. This gives the user the big picture before any resolution is requested (they spot duplicates / gaps / drop-the-whole-section problems before per-decision commitment).
2. **6b. Walks per-decision resolutions** — one `AskUserQuestion` per decision, using the 4-state machine below. Per-section question volume scales with the depth dial → [`../../_shared/interview-depth.md`](../../_shared/interview-depth.md) (easy: decide convention-defaults yourself + an assumptions ledger, ask only blast-radius decisions; hard: walk every decision, foreground each trade-off).
3. **6c. Applies transitions** to the in-memory section as each resolution arrives.
4. **6d. Runs the blast-radius gate** on every Approved decision (NOT on Edit/Drop/Save-as-OQ — those don't become ADRs). If it scores 2-of-3, spawn an ADR; on a 1-of-3 borderline, ask explicitly — see [blast-radius-heuristic.md](./blast-radius-heuristic.md).
5. **6e. Writes the resolved section to `sad.md`** (with all in-memory transitions applied) + writes any ADR files spawned in 6d + commits `feat(<slug>): sad §N — <decisions summary>`. Single commit per section that bundles sad.md + adr/. For §3 C4Context and §5 C4Container: write the block, validate it per [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md), then confirm by prose per [`../../_shared/diagram-presentation.md`](../../_shared/diagram-presentation.md) — never paste the raw C4 source as the question.
6. **6f. Moves to the next section** — repeats 6a-6e. The skill **never returns** to a previously-written section. Cross-section drift (e.g. §4 strategy contradicts §6 happy-path flow) is the Step-7 critic's job.

## Decision-types catalog

Each section holds a mix of these; the same 4-state machine applies to all — the `description` field of each option (see [ask-examples.md](./ask-examples.md)) names the next mechanical step the skill takes.

- **Surface decision** (§4, walked **first**) — *what's being built*: a multiSelect over the C4-grounded taxonomy (`backend-service` / `web-frontend` / `mobile-app` / `desktop-app` / `cli` / `worker` / `library-sdk`), Recommended-set derived from PRD §1 «for whom» + §4 roles. It gates §5 (one container per surface) and every downstream stage, so it's resolved before any other §4 decision. The blast-radius gate fires whenever **>1 surface** is picked (multi-module + irreversible). On resolution, write `target_surfaces: [...]` to the `sad.md` frontmatter → [`../../_shared/surfaces.md`](../../_shared/surfaces.md).
- **UI-architecture decision** (§4, one per declared UI surface) — the follow-on to a `web-frontend` / `mobile-app` / `desktop-app` pick: web → SSR/SPA/hybrid; mobile → native/cross-platform; + state-management + routing only if complexity warrants. Option-set of 2-3, Recommended-first; the gate fires often (irreversible delivery choice). This **evolves** the old §4 "read-side delivery (SSR / SPA / API-only)" item up into a per-surface decision. Kept light (no component-tree / token / screen artifact). It **references the existing design system / component library** from `architecture-map.md` §Frontend — the UI **reuses** that foundation (components, tokens, styling), it doesn't design greenfield → [`../../_shared/surfaces.md`](../../_shared/surfaces.md).
- **Strategic decision** — predominantly §4 Solution strategy, occasionally §7 Deployment. Option-set of 2-4 with «Recommended first + 1-line WHY». **ADR-gate kicks in almost always** (irreversible + multi-module). Plan ≥2 ADRs from §4 alone.
- **Building-block decision** — predominantly §5 Building blocks. Module boundary (extend vs new), layered-vs-hexagonal-vs-clean (only ask if PRD signals divergence from the repo's convention), internal sub-package layout. ADR-gate often fires (multi-module).
- **Crosscutting bundle** — §8 Crosscutting. Option-set of 2: «Keep repo defaults» / «Custom for §X». ADR-gate rarely fires (decisions are convention-level, not blast-radius).
- **Quality scenario** — §10 Quality requirements. Option-set is rarely useful (numbers come from PRD NFR). Typical resolution = `Approve` / `Edit` (refine verification method) / `Save as Open Question` (defer scenario till after the Step-7 critic — usually because verification method is TBD by an owner).
- **Risk entry** — §11 Risks. Auto-generated from edits-log + PRD §8 Open Questions + the Step-3 brownfield scan/map gotchas. User Approves verbatim or `Edit`-s severity/mitigation/owner.
- **Open-architectural-decision row** (special case of Risk entry) — created automatically from any `Save as Open Question` resolution in earlier sections. Skill writes the §11 row at the moment of the OQ resolution; user does NOT see a separate question for it (already approved when they picked `Save as Open Question`). Severity column carries the literal `Open question`.

## 4 дії з рішенням — 4-state machine (uniform across all decision-types)

> **UA-перифраза.** «4-state machine» — це 4 можливі дії з кожним рішенням: **Прийняти** (Approve) / **Виправити** (Edit) / **Винести у відкрите питання** (Save as OQ) / **Викинути** (Drop). `Cancel` і `Reject` — синоніми Drop. Кожна дія має чітку механіку нижче.


- **`Approve`** → keep decision verbatim. No edits-log entry. **Run blast-radius gate** (Step 6d). If it scores 2-of-3, spawn an ADR (see SKILL.md and [blast-radius-heuristic.md](./blast-radius-heuristic.md)). Move to next decision.

- **`Edit`** → user types new option / new wording / new severity etc. in one go; skill regenerates the decision with the new constraint and asks **once more** on the new version (single-iteration cap — the second answer is final). Log entry with `action: "edit"`.

- **`Save as Open Question`** → decision is removed from its native section AND a row is appended to §11 Risks/Open-Decisions table in this exact shape:

  ```
  | Open architectural decision: <headline> | Open question | Resolve before <stage trigger or YYYY-MM-DD>; <inline rationale from user> | <owner> |
  ```

  Owner + due (date OR stage trigger like «before `/sdlc-break-tasks`») are **mandatory** — skill issues a follow-up `AskUserQuestion` immediately after the user picks this option to capture both. If the user leaves owner OR due blank, the resolution is **downgraded to `Drop`** with an explicit warning surfaced.

  Severity column accepts literal `Open question` value (not Low/Medium/High) — that's the marker that distinguishes OQ rows from regular risks (used by the Step-7 critic F3 + checklist).

  Log entry with `action: "save_as_oq"`. **No ADR spawn** — `Save as OQ` is a defer, not a decision; ADRs are for accepted decisions only.

- **`Drop`** → decision is removed from the section. Two sub-paths:
  - **If decision was mandatory** (e.g. §5 module boundary — every feature has one) → skill re-asks with a **reframed** option set (e.g. if user dropped «extend existing» and «new module», skill asks «extend existing with new sub-package» / «move to shared package»). Single re-ask only; if user drops again → escalate to `Save as Open Question` with skill-suggested owner = Architect + due = «before next pass» and a warning.
  - **If decision was optional** (e.g. §6 extra failure-mode flow beyond happy-path) → leave it out, no replacement.
  - Log entry with `action: "drop"`.

Each option label must be paired with a `description` explaining the next mechanical step the skill will take after that choice — see [ask-examples.md](./ask-examples.md) for canonical wording.

`Cancel` and `Reject` are synonyms for `Drop` — same transition, same edits-log action.

Persist edits into the in-memory section after each resolution. The on-disk `sad.md` is **not** touched until step 6e (after all decisions in the current section resolved + blast-radius gate run + ADRs spawned).

## ADR spawn within Step 6d

When the blast-radius gate fires on an Approved decision:

1. Compute NNNN: `ls docs/features/<slug>/adr/*.md 2>/dev/null | wc -l` + 1, zero-padded to 4 digits.
2. Compute kebab-case title from the **decision** (not the problem): `0003-sliding-window-with-redis.md` ✓ vs `0003-rate-limiting.md` ✗.
3. Copy `./templates/adr-template.md` → `docs/features/<slug>/adr/NNNN-<title>.md`. Fill: Status = `Accepted`; Context (2-4 sentences from the section); Decision drivers (relevant Quality Goals + Constraints); Considered options (from the AskUserQuestion options including rejected ones); Decision outcome (chosen option + 1-2 sentences rationale); Consequences (Positive / Negative / Neutral); Links (PRD path, sad.md §N, related ADRs).
4. Add a row to §9 ADR table in-memory: `| NNNN | <imperative title> | Accepted | §N |`.
5. **No separate commit** — the ADR file goes into the section commit in Step 6e together with sad.md edits.
6. Append to ADR-spawns log (in-memory only, not persisted):
   ```
   {adr_id: "NNNN", title: "<imperative kebab>", section: "§N", triggered_by: "DEC-§N-<decision-id>"}
   ```
   The Step-7 critic reads `docs/features/<slug>/adr/` directly — the spawns log is for in-memory traceability, NOT a persisted artifact.

Expected ADR count by size: XS/S → 2-4, M → 5-12, L/XL → 10-15.

## Edits-log (mandatory)

Maintain an edits-log throughout step 6. After each `Edit` / `Drop` / `Save as Open Question` resolution (NOT for `Approve`), append one entry:

```
{decision_id: "DEC-§N-<short-id>"  (e.g. "DEC-§4-modulesIntegration", "DEC-§5-moduleBoundary",
                                    "DEC-§10-QG1-verification"),
 action:      "edit" | "drop" | "save_as_oq",
 before:      "<verbatim option / wording / severity before user action>",
 after:       "<verbatim option / wording / severity after — for save_as_oq this is the §11 row text
                incl. owner+due; for drop this is null>",
 user_reason: "<the rationale the user provided, verbatim>"}
```

`Approve` decisions do **not** go into the log — they are the baseline. The log is the **sole** signal the Step-7 critic uses to detect upstream-coherence drift caused by user edits during Socratic. Without it, the critic has no input for F1/F2/F3/F4.

If the user provides no reason on `Drop` or `Save as Open Question` — re-prompt once for it. Verbatim user wording matters: the critic uses it to judge whether a defer silently re-introduces a vector that PRD §6 NFR / §7 KPI / §13 Recommendation named as load-bearing.

The ADR-spawns log lives **adjacent** to the edits-log (not folded in) because they're different signals: edits-log = upstream-coherence (what user changed); ADR-spawns log = downstream artifact (what new file was created). Critic reads `adr/` directly; spawns log is in-memory only.

## Open-Questions table

`save_as_oq` rows land in **§11 Risks** in this exact shape, with the literal `Open question` in the severity column:

```
| Open architectural decision: <headline> | Open question | Resolve before <stage trigger or YYYY-MM-DD>; <inline rationale> | <owner> |
```

Owner + due (a date OR a stage trigger like «before `/sdlc-break-tasks`») are mandatory — capture both in the follow-up `AskUserQuestion`. Missing either downgrades to Drop with a warning. No gate — a defer is not an accepted decision.

## Exit condition

Step 6 completes when:

- All 12 sections have been batch-rendered (6a) + walked (6b) with one resolution per decision.
- Each section's resolved content + any ADR files spawned in 6d are **already written to disk** in 6e (incremental commits per section).
- The §9 ADR table is closed (no orphans — every file in `adr/` has a §9 row, every §9 row has a file).
- §11 Risks contains every `save_as_oq`-migrated row from Step 6 with owner+due filled (no lone owner, no lone due).
- The edits-log is closed (no pending entries).
- Frontmatter `target_surfaces: [...]` is non-empty (§4 Target-surface decision resolved) and §5 drew one container per declared surface.

Then proceed to Step 7 (see [critic-phase.md](./critic-phase.md)).
