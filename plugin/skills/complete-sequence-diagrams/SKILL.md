---
name: complete-sequence-diagrams
description: >-
  Use to add Mermaid sequenceDiagram blocks to the SAD's runtime view
  (sad.md §6) — one per critical flow, showing how a request moves between
  generic participants with happy + error paths.
  Triggers on "complete sequences for {slug}", "sequence diagram for {slug}",
  "draw the runtime flow", "add a sequence to the SAD",
  "/sdlc:complete-sequence-diagrams {slug}", "діаграми послідовності {slug}",
  "sequence для {slug}", "намалюй потік {slug}". Reads sad.md §5 for
  participants, drafts each flow from templates/seq-flow.md with generic
  participants, walks them Socratically one flow at a time, writes
  confirmed blocks into sad.md §6 — they inform data-model indexes downstream —
  and closes with the US/AC → flow coverage table written as the last block
  of §6 (`### Coverage: US/AC → flows`).
  Hard-refuse if sad.md is missing → run /sdlc:architecture-design first.
  Single-flow mode: /sdlc:complete-sequence-diagrams {slug} --flow {name}.
triggers:
  - /sdlc:complete-sequence-diagrams
stage: "05"
---

# Skill: complete-sequence-diagrams

Draws the **runtime view** of an already-designed feature: for each critical flow it produces a Mermaid `sequenceDiagram` block — generic participants, happy path plus the error branches the PRD demands — and writes them into `docs/features/<slug>/sad.md §6`. One flow at a time, user confirms each. The diagrams are the bridge between the static design (§5 building blocks) and the data layer: every persist/read step you draw becomes a hint for the indexes `generate-data-model` will need.

This skill keeps only its own machinery. **Flow count is driven by the PRD, not a cap** — every §4 user story / §5 acceptance criterion is covered (size may collapse *detail*, never *coverage*), and the proof of that coverage is **persisted, not chatted**: the US/AC → flow table is written into `sad.md §6` as its last block (step 7), where `review-feature`'s end-to-end trace and `api-forge`'s coverage cross-check read it. Each diagram is **confirmed in prose, never as raw Mermaid** → [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md); the per-flow confirm-vs-proceed behaviour follows the interview-depth setting → [`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

Tech Lead (drives the runtime decomposition). The PM confirms that each drawn flow matches a real user story; a backend engineer flags persist steps that imply a new index.

## Inputs

- `<slug>` — same feature slug used by every earlier stage.
- **Gate (hard-refuse if missing):** `docs/features/<slug>/sad.md`. The §5 building-block view names the participants; §6 is where flows are written. If `sad.md` is absent → STOP and point: «run `/sdlc:architecture-design <slug>` first — sequences are written into its §6».
- **Strongly expected:** `docs/features/<slug>/PRD.md` — §4 user stories tell you *which* flows exist; §5 acceptance criteria are the **coverage floor** — every AC must be shown by a flow, a branch, or an explicit non-runtime N/A (the step-7 coverage check). Present by this stage in the normal pipeline; if genuinely absent, fall back to §6/§5 of `sad.md` for the flow list and note that AC-coverage can't be verified.
- (Optional) `docs/features/<slug>/.size` — depth hint for *detail* (XS/S may collapse a flow's internal steps), never for *coverage*. Absent → default to M.
- (Optional) `.claude/sdlc.local.md` `interview_depth` (else medium) — governs only the diagram-confirmation UX (per-diagram prose+ask vs. write+summarize-and-proceed); this skill does **not** open its own depth question (it honors the setting, or a `--depth=` arg if passed).

## Protocol

1. **Gate.** `test -f docs/features/<slug>/sad.md` → fail = refuse with the pointer above. Then read §5 (participants) and §6 (any flows already drawn — this skill is additive, never rewrite an existing block).

2. **Pick the flows — PRD-driven, no cap.** List the flows from `PRD.md` **§4 user stories + §5 acceptance criteria** (absent the PRD, from §6 itself): **one flow per critical user story / distinct runtime path**. There is **no fixed cap** — draw as many flows as the user stories and ACs need. Then **plan AC coverage**: map every §5 AC to where it will be shown — a **dedicated flow**, an **`alt`/`else` branch** inside the relevant flow, or **explicitly non-runtime** (e.g. a middleware-enforced authorization check, a build-time validation) with a one-line reason. Size only collapses *detail* (XS/S may show fewer internal steps per flow), never *coverage*. Confirm the flow list **and the AC→flow map** with one `AskUserQuestion` before drawing.

3. **Map participants — generic only.** For each flow, draw participants from a fixed generic vocabulary: `<client>`, `<ui>`, `<service>`, `<data-store>`, `<external-system>`, `<message-bus>`. Do **not** invent concrete service or technology names — those are `architecture-design` / `generate-data-model` decisions, not runtime-view ones. **When `sad.md` frontmatter `target_surfaces` declares a UI surface** (`web-frontend` / `mobile-app` / `desktop-app`), draw the flows it touches as **UI-driven** — `<user>` (actor) → `<ui>` → `<service>` → `<data-store>` — so the user-visible step is shown, not just the service call (→ [`../_shared/surfaces.md`](../_shared/surfaces.md)). A backend-only / `cli` / `worker` feature keeps the service-level vocabulary (no `<ui>`). `<ui>` stays generic like every other participant — never a framework or component name. If a flow needs a participant §5 never declared, note it («flow needs `<message-bus>`, not in §5 — flag for architecture-design») and still draw it.

4. **Sync vs async.** If the PRD describes a webhook, scheduled job, queued/event-driven step, or any third-party callback → async: add an idempotency-key check as the handler's first step, a retry note (`Note over <service>,<external-system>: retry N times with backoff`), and a dead-letter branch in an `alt` after N failures. Otherwise → sync (request → response).

5. **Draft each flow** from [`./templates/seq-flow.md`](./templates/seq-flow.md): a precondition note, the happy-path messages, an `alt`/`else` for the error branches the PRD acceptance criteria require, and a postcondition note. Mark every write as a generic persist note — `Note over <service>,<data-store>: persists <entity>` — so `generate-data-model` sees what to index. Keep messages verb-first and free of HTTP verbs / status numbers / SQL.

6. **Present + confirm each flow, one at a time — in prose, never raw Mermaid.** Per [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md): for each drafted flow, **write the block into §6** under a `### <flow name>` heading (so Obsidian renders it), **validate** it parses per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md), then **describe it in prose** — the happy path plus every `alt`/`else` branch in plain words. **Never paste the raw `sequenceDiagram` source as the question.** Confirm by prose, governed by the interview-depth setting: at **medium/hard**, one `AskUserQuestion` per flow with the 4-state actions (Accept / Fix / Save-as-OQ / Drop) — on **Fix**, regenerate + overwrite that one block, re-validate, re-describe (one round, second answer final); on **Drop**, remove the block again. At **easy**, write + a one-line prose summary into the assumptions ledger and proceed (no per-flow question). Never touch a flow already present in §6. Maintain a short edits-log.

7. **Use-case + AC → flow coverage table — written into `sad.md §6` (before finalizing).** Two passes, one table, one fixed home. The table is a **file artifact, not a chat message**: it is written into `docs/features/<slug>/sad.md` as the **last block of §6**, under the fixed heading **`### Coverage: US/AC → flows`** (after every `### <flow name>` block, before `## 7`), from [`./templates/seq-coverage.md`](./templates/seq-coverage.md). Build it in two passes:
   - **Use-case pass (§4).** One row per **§4 user story**, in §4 order: the `### <flow name>` heading(s) that realize it. Every retained user story maps to **≥1 flow** (a US with no flow is a gap — draft + confirm one, or de-scope it back through `/sdlc:write-prd`/`/sdlc:clarify-prd`, never silently skip).
   - **AC pass (§5).** One row per **§5 AC**, in §5 order: where it is now shown — a **dedicated flow** (`flow`), an **`alt`/`else` branch** (`branch` + the branch label in *Note*), or an **explicit non-runtime N/A** (`N/A` + its one-line reason in *Note*, e.g. «authorization check in middleware, not a runtime flow»).

   Columns are fixed: `| ID | Realized by (§6 heading) | How | Note |` — `ID` = `US-NN` / `AC-NN` exactly as the PRD spells it; `Realized by` = the §6 heading text(s), `—` for N/A; `How` ∈ `flow` / `branch` / `N/A`; `Note` = branch label, N/A reason, or empty. Close the block with one summary line: `Coverage: <n>/<n> user stories · <m>/<m> ACs — <k> non-runtime N/A.` No `GAP` may remain in the written table: if a `Drop`/`Save-as-OQ` during step 6 left a user story or an AC uncovered, draft + confirm the missing flow or branch first, or record the explicit N/A with the user. **No §4 user story and no §5 AC may be silently uncovered.**

   **Confirm the N/A rows, not the table.** At medium/hard, one `AskUserQuestion` lists the N/A rows (and nothing else — the mapping rows are mechanical); at easy, write the table and add the N/A rows to the assumptions ledger. **This step runs at every depth and size** (easy/XS included) and the table is written even when every row is trivially `flow` — a §6 without the block is an unfinished run. **Idempotent:** on a re-run, if `### Coverage: US/AC → flows` already exists in §6, **replace the whole block** (heading to the summary line) with the regenerated one — never append a second table, never leave a stale one. Print only the summary line in chat; the table itself lives in the file.

8. **Finalize: order, validate, propose commit.** Order the §6 flow blocks to match §4, keeping `### Coverage: US/AC → flows` as the **last** block of §6. **Re-validate every `sequenceDiagram` block per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md)** as the backstop (balanced `alt`/`else`/`end`, declared participants; fix any that don't parse before committing). Append any flagged items (new participants, decisions worth an ADR) as a `**Flags:**` bullet list directly under the coverage table's summary line — flag only, never auto-write an ADR. Propose commit `sequences: <slug> runtime flows + coverage`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* (flows written + the coverage summary line) + *Review* (`sad.md` §6 — the flow blocks, and `### Coverage: US/AC → flows` for the N/A rows) + *Run next* (`/clear`, then `/sdlc:generate-data-model <slug>`, which uses the persist notes to choose indexes).

## Single-flow mode

`/sdlc:complete-sequence-diagrams <slug> --flow <name>` — draws one sequence on demand. Skips the full inventory (step 2) and goes straight to step 4 (classify → participants → draft → validate → confirm). Writes inline into `sad.md §6` under `### <name>`, **above** the `### Coverage: US/AC → flows` block if one exists. It does **not** build a new coverage table; it **patches the existing one**: for every US/AC the new flow realizes, update that row (`Realized by` + `How`, replacing a `N/A` or an outdated entry) and refresh the summary line. If §6 has no coverage block yet, say so in the handoff («no coverage table in §6 — run the full `/sdlc:complete-sequence-diagrams <slug>` to generate it») and do not invent a partial one. Still uses generic participants and validates per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md).

## Definition of Done

- `sad.md §6` holds a Mermaid `sequenceDiagram` for **every** critical user story / distinct runtime path — **no fixed cap**; size may collapse a flow's internal detail, never its coverage.
- **Every §4 user story maps to ≥1 flow, and every §5 AC maps to a flow, an `alt`/`else` branch, or an explicit non-runtime N/A** — the step-7 coverage check passed on both passes; nothing is silently uncovered (holds at every depth + size).
- **The coverage table is in the file:** `sad.md §6` ends with exactly one `### Coverage: US/AC → flows` block — fixed columns `ID | Realized by (§6 heading) | How | Note`, one row per §4 US and per §5 AC in PRD order, no `GAP` rows, a `Coverage: n/n user stories · m/m ACs — k non-runtime N/A.` summary line. A table shown only in chat, or a second stale table left after a re-run, fails this item.
- Each flow was **confirmed in prose** (medium/hard) or **written + summarized** (easy) — never by pasting raw `sequenceDiagram` source as the question.
- Every block uses **only** generic participants (`<client>` / `<ui>` / `<service>` / `<data-store>` / `<external-system>` / `<message-bus>`) — no concrete technology or service names. A declared UI surface uses `<ui>` in a UI-driven flow (`<user>` → `<ui>` → `<service>` → `<data-store>`); a backend-only feature omits it.
- Each flow shows the error branches its PRD acceptance criteria require, not happy-path only; every mutating step carries a generic persist note for `generate-data-model`.
- Every async flow has an idempotency-key step, a retry note, and a dead-letter branch.
- Pre-existing §6 blocks are untouched; new participants / ADR-worthy decisions are flagged, not silently added.

## Anti-patterns

- **Concrete participants.** Naming a specific database, service, or broker — the legacy trap. Participants stay generic; naming the technology is the job of `architecture-design` / `generate-data-model`.
- **Capping the flow count** and silently under-covering. Flow count is driven by §4/§5 — every AC is shown by a flow, a branch, or an explicit N/A.
- **Coverage table in chat only.** Printing the US/AC → flow table in the terminal and moving on leaves nothing for `review-feature` / `api-forge` (or a reviewer) to open. The table is written into `sad.md §6` under `### Coverage: US/AC → flows`; chat gets the one-line summary.
- **Pasting raw Mermaid as the confirmation.** `sequenceDiagram` source in the terminal is unreadable — the user approves blind. Confirm in prose; let Obsidian render the written block (per [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md)).
- **Happy path only** when the PRD lists explicit error acceptance criteria. Each flow gets happy + the demanded error branches.
- **One mega-diagram** for the whole feature. Split per flow; a cross-cutting flow gets its own `### Cross-cutting: <name>` heading.
- **Auto-writing ADRs.** This skill only flags decisions (idempotency strategy, retry shape, sync-vs-async); ADRs come from `/sdlc:decide-adr` or a human.
- **Rewriting an existing §6 block.** Additive only — editing a drawn flow is a deliberate manual diff.
- **Inventing a participant §5 never declared without flagging it.** §5 is the source of truth; the flag lets `architecture-design` reconcile it.

## References & template

- [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md) — how each flow is confirmed (write → validate → prose-describe → confirm/proceed); never raw Mermaid as the question.
- [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md) — parse-validation run on each block at step 6 and again as the step-8 backstop.
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — a declared UI surface adds `<ui>` to the vocabulary and draws UI-driven flows; read from `sad.md` `target_surfaces`.
- [`../_shared/handoff.md`](../_shared/handoff.md) — stage-handoff block format emitted at step 8.
- [`./templates/seq-flow.md`](./templates/seq-flow.md) — generic-participant `sequenceDiagram` scaffold (sync + async), embedded inline in `sad.md §6`.
- [`./templates/seq-coverage.md`](./templates/seq-coverage.md) — the `### Coverage: US/AC → flows` block (fixed columns + summary line), written as the last block of `sad.md §6` at step 7.
