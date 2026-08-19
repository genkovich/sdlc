---
name: architecture-design
model: opus
effort: high
agents: [explorer, critic]
description: >-
  Use to produce a Software Architecture Document for a feature — Arc42 12 sections + C4 L1/L2
  inline + ADRs spawned on a blast-radius gate — once PRD.md and CONTEXT.md exist. The feature's
  target surface(s) are chosen here (the first §4 decision → SAD frontmatter target_surfaces, read by
  every downstream stage). Drafts §1–§12 in-memory, batch-validates each section Socratically
  (4-state machine), spawns an ADR only when a decision crosses the blast-radius threshold
  (irreversible / multi-module / has legitimate alternatives), writes each resolved section + its
  ADRs atomically, then runs a clean-context critic before finalizing. Brownfield: reads
  docs/architecture-map.md (re-scans only if absent/stale). Triggers on "architecture for {slug}",
  "design architecture for {slug}", "SAD for {slug}", "arc42 for {slug}", "C4 context+container for
  {slug}", "/sdlc-architecture-design {slug}", "спроектуй архітектуру {slug}", "SAD для {slug}",
  "архітектурний документ {slug}". Hard-refuse if docs/features/{slug}/PRD.md is missing.
  Triggers: /sdlc-architecture-design {slug}. Output: docs/features/{slug}/sad.md + adr/NNNN-*.md.
triggers:
  - /sdlc-architecture-design
  - "architecture for"
  - "design architecture for"
  - "SAD for"
  - "arc42 for"
  - "C4 context+container for"
  - "SAD для"
  - "архітектурний документ"
stage: "04-05"
---

# Skill: architecture-design (SDLC stages 04-05 🚪 GATE)

Generator of the **Software Architecture Document** (`docs/features/<slug>/sad.md` — Arc42 12 sections, C4 Context inline in §3 and C4 Container inline in §5) plus supporting ADRs (`docs/features/<slug>/adr/NNNN-*.md`). It drafts all 12 sections in memory, walks them Socratically one section at a time, spawns an ADR only when a decision's *blast radius* (масштаб удару — how painful it is to reverse the decision later) crosses the gate, writes each resolved section and its ADRs as one atomic commit, and runs a clean-context critic over the finished SAD. The document itself is the state — resuming after an interrupt is free. L3 Component / L4 Code are out of scope. This file is the spine; detail lives in `references/`.

The Socratic machine, the critic, the size matrix, and the ask-style are **shared** — this skill keeps only its deltas:
→ [`../_shared/socratic-loop.md`](../_shared/socratic-loop.md) · [`../_shared/critic.md`](../_shared/critic.md) · [`../_shared/size-matrix.md`](../_shared/size-matrix.md) · [`../_shared/ask-style.md`](../_shared/ask-style.md)

Depth governs the per-section question volume + autonomy → [`../_shared/interview-depth.md`](../_shared/interview-depth.md). C4 diagrams are confirmed in prose, never as raw source → [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md). architecture-design is also where the feature's **target surface(s)** are chosen — the first §4 decision, written to `sad.md` frontmatter `target_surfaces` and read (never re-derived) by every downstream stage → [`../_shared/surfaces.md`](../_shared/surfaces.md).

## Як це читати (короткий вступ)

Це інструкція для агента, який запускає skill. У ній **7-крокова процедура** (Protocol нижче) — крок за кроком, як з PRD дістатися до готового `sad.md` з 5-12 ADR.

Якщо вперше відкриваєш файл — почни з: **`## When to use`** + **`## Inputs`** (коли skill застосовний), потім **`## Protocol`** (7 кроків), потім References (деталі на кожен крок), і **`## Definition of Done`** (що має бути виконано до завершення).

**Словничок термінів** (англо-термін → що означає UA одним рядком):

- *target surface* — таргет-сёрфейс: *що саме ми будуємо* (бекенд-сервіс / веб-фронт / мобільний застосунок / CLI / worker / library-sdk). Обирається тут, у §4, і записується у `target_surfaces:` frontmatter SAD → [`../_shared/surfaces.md`](../_shared/surfaces.md).
- *depth dial* — депт-діал: регулятор easy/medium/hard на запуск — скільки skill питає vs вирішує сам → [`../_shared/interview-depth.md`](../_shared/interview-depth.md).
- *blast radius* — масштаб удару: наскільки боляче буде передумати рішення.
- *Socratic loop* — режим діалогу з користувачем питаннями про рішення (одна `AskUserQuestion` за раз).
- *blast-radius gate* — перевірка з 3 критеріями: незворотнє (≥3 днів переробки), зачіпає ≥2 модулі, є чесна альтернатива. **2 з 3 → ADR.**
- *4-state machine* — 4 можливі дії з рішенням: **Прийняти** / **Виправити** / **Винести у відкрите питання** / **Викинути**.
- *Save-as-OQ* — рішення не приймається зараз, переноситься у §11 SAD як відкрите питання з власником і дедлайном.
- *MADR* — формат файлу ADR (markdown з заголовком, контекстом, опціями, наслідками).
- *clean-context critic* — окремий subagent (`sdlc:critic`), який бачить лише фінальний файл (а не діалог), і шукає внутрішні протиріччя.

## Owner

Architect / Tech Lead (drives everything). PM is consulted only on §10 Quality goals and §11 Risk severities.

## When to use

- After `sdlc:write-prd` produced `docs/features/<slug>/PRD.md` (ideally after `sdlc:clarify-prd` tightened it).
- Brownfield repo (existing code the feature changes) OR greenfield with a PRD only.
- `/sdlc-architecture-design <slug>` as explicit invocation.
- Skip if `docs/features/<slug>/sad.md` already has all 12 sections filled (content or `<!-- N/A: reason -->`) AND `adr/` has ≥1 file — suggest review instead.

## Inputs

- `<slug>` — same feature slug used by every earlier stage.
- **Gate (hard-refuse if missing):** `docs/features/<slug>/PRD.md`. If absent → STOP and point: «run `/sdlc-write-prd <slug>` first — architecture-design reads the PRD's goals/NFRs as canonical». `CONTEXT.md` (`## Glossary`) is read when present — it wins over anything that contradicts; absent → derive roles from PRD §4 and note it.
- (Optional) `docs/features/<slug>/.size` — depth hint (MVP vs Full + expected ADR count per the size matrix). Absent → default to M (full set) and say so loudly in the handoff.
- (Optional) `docs/architecture-map.md` — the current-architecture source (produced by `sdlc:map-architecture`). Read it; re-scan only if absent/stale.
- A git repo — so the Step-3 brownfield scan can read code when the map is missing.

## Protocol

1. **Gate + size + set interview depth.** `test -f docs/features/<slug>/PRD.md` → missing = refuse with the pointer above. Read `.size` if present (shapes ADR count + §6 flow count — see the size matrix; absent → default M). **Then set the interview depth (the opening question):** read `interview_depth` from `.claude/sdlc.local.md` if present (else default medium), and — unless a `--depth=easy|medium|hard` arg was passed — ask ONE depth-selection `AskUserQuestion` phrased per [`../_shared/ask-style.md`](../_shared/ask-style.md), with the saved/medium value as the «(Recommended)» first option. The level governs the step-6 per-section question volume (easy: decide convention-defaults itself + an assumptions ledger, ask only blast-radius decisions; medium: walk every real decision; hard: walk every decision, foreground each trade-off) and the C4 diagram confirmation → [`../_shared/interview-depth.md`](../_shared/interview-depth.md). (The blast-radius → ADR gate and the §11 owner+due rule are floors — enforced at every depth.)
2. **Read upstream.** `PRD.md` (§2 Goals, §3 Non-goals, §6 NFR with numeric targets + measurement, §6.1 Security/privacy + abuse cases, §7 KPIs, §8 Open questions, §13 Recommendation, any §1 ¶4 «Decision override» bullets); `CONTEXT.md` `## Glossary` (canonical roles + domain terms — wins over anything that contradicts).
3. **Current architecture — read the map, don't re-scan.** Prefer `docs/architecture-map.md` (produced by `sdlc:map-architecture`): if it exists and is fresh (its `reflects_commit` ≈ current HEAD), read it — that IS the brownfield context (module layout, layering, datastores, conventions, the §Frontend / UI foundation, the C4 of what exists). Re-scan only if the map is **absent or stale**: dispatch the [`explorer`](../../agents/explorer.md) agent — `subagent_type: "sdlc:explorer"` (`model: haiku` + `effort: low`, clean-isolated per [`../_shared/agent-roster.md`](../_shared/agent-roster.md)) — for «primary language + frameworks + versions, module layout, layering/ports conventions, datastores, inter-module comms, the existing design system / component library / tokens (§Frontend), anything that constrains `<slug>`», and suggest the user run `/sdlc-map-architecture` to persist it. Greenfield (no source + no map) → note `<!-- brownfield: N/A — greenfield repo -->` in §3. (Fallback to a `subagent_type: "Explore"` Agent if `sdlc:explorer` is unavailable.)
4. **Bootstrap + read template.** Copy [`./templates/sad-template.md`](./templates/sad-template.md) → `docs/features/<slug>/sad.md`; patch frontmatter (`updated_at`, `ticket`, `feature_size` from `.size`; leave `target_surfaces: []` empty — it's filled when §4's Target-surface decision resolves in step 6). Commit `feat(<slug>): bootstrap sad.md from PRD + architecture-map`. Read the template's `<!-- … -->` comments (the per-section contract) + [`./templates/adr-template.md`](./templates/adr-template.md) (MADR shape). This is the only file write between Step 4 and Step 6 — Step 5 drafts in-memory.
5. **Per-section draft (in-memory).** For each §1 → §12, draft proposed content + the decisions it contains, bundling trivial convention defaults into one question. Per-section sourcing, item-banks, the question budget, and pre-Socratic hygiene → [`./references/draft-generation.md`](./references/draft-generation.md). Do NOT write `sad.md` here.
6. **Socratic walk + blast-radius gate, per-section write.** For each §1 → §12: render the full section + its numbered decisions (big picture), walk one `AskUserQuestion` per decision with the shared 4-state machine (per-section question volume scales with the depth dial — at easy, decide convention-defaults yourself and ladder them into the assumptions ledger, asking only blast-radius decisions), apply transitions in-memory, run the blast-radius gate on each **Approved** decision (spawn an ADR on 2-of-3), then write the resolved section + its spawned ADRs + commit `feat(<slug>): sad §N — <summary>`. Never return to a written section. **§4's first decision is the Target-surface selection** — *what's being built* (a multiSelect over `backend-service` / `web-frontend` / `mobile-app` / `desktop-app` / `cli` / `worker` / `library-sdk`, derived from PRD §1 «for whom» + §4 roles; the PRD itself names no surface), gated by the blast-radius gate (multi-surface is multi-module + irreversible ⇒ usually an ADR). On resolution, **write `target_surfaces: [...]` to the `sad.md` frontmatter** — it draws one §5 C4 container per surface and is read (never re-derived) by `api-forge` / `complete-sequence-diagrams` / `break-tasks` / `plan-tests` / `review-feature`. For each declared **UI surface** (`web-frontend` / `mobile-app` / `desktop-app`), walk the follow-on **UI-architecture decision** (web → SSR/SPA/hybrid; mobile → native/cross-platform; + state/routing if warranted), gated to an ADR like any §4 strategic choice; the UI **reuses** the existing design system / components / tokens from `architecture-map.md` §Frontend → [`../_shared/surfaces.md`](../_shared/surfaces.md). **For the §3 C4Context and §5 C4Container sections, confirm the diagram per [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md)** — write the block into `sad.md`, validate it per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md), then **describe the context / containers in prose** (who talks to what, which systems it depends on) and confirm by prose; **never paste the raw C4 source as the question**. At `easy`, write + a one-line summary and proceed (no per-diagram question). architecture-design delta → [`./references/socratic-loop.md`](./references/socratic-loop.md) (section list, decision-types, the gate); gate scoring → [`./references/blast-radius-heuristic.md`](./references/blast-radius-heuristic.md); C4 syntax for §3/§5 → [`./references/c4-mermaid-syntax.md`](./references/c4-mermaid-syntax.md); cadence → [`./references/socratic-cadence.md`](./references/socratic-cadence.md); question shapes → [`./references/ask-examples.md`](./references/ask-examples.md). Maintain the edits-log + an adjacent ADR-spawns log.
7. **Critic + finalize.** Dispatch the [`critic`](../../agents/critic.md) agent — `subagent_type: "sdlc:critic"` (carries `model: opus` + `effort: high`, clean-isolated per [`../_shared/agent-roster.md`](../_shared/agent-roster.md); fallback `general-purpose` if unavailable) — with the architecture-design delta in [`./references/critic-phase.md`](./references/critic-phase.md) + the agent prompt body in [`./references/critic-prompt.md`](./references/critic-prompt.md) (over [`../_shared/critic.md`](../_shared/critic.md)) on the final `sad.md` + edits-log + ADR-spawns log; resolve each finding via `AskUserQuestion` (Accept revert / Accept amendment / Override-with-rationale → §1 ¶4 bullet). Run the pre-write backstop scans: **validate every Mermaid block in `sad.md` per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md)** (render-parse with `mmdc` if available, else the structural lint — fix any that don't parse, never commit a broken diagram); ADR title in decision-form kebab-case + Status `Accepted`; §9 closed against `adr/`; no `<placeholder>` stubs. On pass, write any amendments + commit `feat(<slug>): sad finalization (critic pass)`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* + *Review* (`sad.md` C4 §3/§5 + `target_surfaces`, `adr/`) + *Run next* (`/clear`, then `/sdlc-complete-sequence-diagrams <slug>`, which writes flows into §6).

## Definition of Done

- `docs/features/<slug>/sad.md` exists with all 12 Arc42 sections filled OR marked `<!-- N/A: <reason> -->`.
- §3 has a real `C4Context` block and §5 a real `C4Container` block — real names from CONTEXT + the map/scan, no `<placeholder>` stubs, no `Container_Bondary` typos. §6 has ≥1 `sequenceDiagram` (the `complete-sequence-diagrams` stage then covers every critical flow / §5 AC — no cap).
- Frontmatter `target_surfaces: [...]` is non-empty (the Target-surface decision was made in §4) and §5 draws **one C4 container per declared surface**; each declared UI surface (`web-frontend` / `mobile-app` / `desktop-app`) carries a UI-architecture decision — an ADR, or an inline §4 note if it didn't cross the gate. → [`../_shared/surfaces.md`](../_shared/surfaces.md).
- §9 ADR table is closed against `adr/` (every file has a row, every row a file). 2–4 ADRs for XS/S, 5–12 for M, 10–15 for L/XL; every ADR Status = `Accepted`, title in decision-form (`0003-sliding-window-with-redis.md` ✓ vs `0003-rate-limiting.md` ✗), no strawman options.
- §10 scenarios are testable (When / Then / How-verify) and cite PRD §6 NFR numbers verbatim (no inventing, no rounding).
- §11 carries a row for every `save_as_oq` decision with both owner AND due (severity literal `Open question`); never N/A.
- §1 Stakeholders + §3 actors match the CONTEXT glossary exactly (no invented `user`/`admin`).
- Step-3 read the map (or the explorer scan ran on a brownfield, or §3 has the greenfield note). Edits-log maintained. The critic ran on the post-Socratic SAD; every finding resolved or overridden.

Full DoD + anti-patterns + N/A logic per section + ADR-count expectations → [`./references/checklist.md`](./references/checklist.md). Any check fails → re-open the relevant `AskUserQuestion`, then re-check.

## Anti-patterns

- **An ADR for every decision** — kills the genre. Only blast-radius decisions become ADRs (5–12 for M, not 25). Conversely, missing an irreversibility under-ADRs the feature.
- **ADR `Status: Proposed` from this skill** — it is synchronous (you decide with the user now), so Status is `Accepted`. Use `sdlc:decide-adr` for an async Proposed → Accepted flow.
- **ADR title in problem-form** (`0003-rate-limiting.md`) or with a **strawman option** (an alternative an existing constraint already excludes) — both dilute the ADR genre and trigger the critic's F6.
- **Inventing §10 numbers** the PRD never agreed to — cite PRD §6 NFR verbatim. **Naming a concrete stack in §2** that contradicts the repo's conventions without an Override note pointing at §11.
- **Re-deriving the surface downstream.** architecture-design declares `target_surfaces` once; `api-forge` / `complete-sequence-diagrams` / `break-tasks` / `plan-tests` / `review-feature` read it. A skill that re-infers the surface when the SAD already declared it is the anti-pattern surfaces.md kills.
- **Skipping the brownfield context** — guessing the layout produces a fictional §5 Container view and invented §2 Constraints. Read `architecture-map.md`; scan with `sdlc:explorer` only if it's missing/stale.
- **Returning to a written section** — each section commits atomically; cross-section drift is the critic's job, not a re-walk. Re-opening §4 after writing §10 means you don't trust the per-section batch.
- **Save-as-OQ without owner+due** — capture both in the follow-up; missing either downgrades to Drop with a warning, never a half-filled §11 row.
- **Resolving critic findings unilaterally** (without `AskUserQuestion`) or **one giant end-of-pass commit** — both defeat the per-section, user-in-the-loop contract.
- **Spilling into C4 L3/L4** — out of scope; suggest a separate diagramming pass.

## References & templates

- [`./references/draft-generation.md`](./references/draft-generation.md) — Step 5: per-section sourcing for §1–§12, item-banks, the question budget, pre-Socratic hygiene.
- [`./references/socratic-loop.md`](./references/socratic-loop.md) — architecture-design's delta over the shared Socratic loop (section list, decision-types incl. Surface + UI-architecture, the blast-radius gate, the §11 OQ table).
- [`./references/socratic-cadence.md`](./references/socratic-cadence.md) — how to avoid question fatigue (mini-recap every 5, Recommended-first, bundle trivial defaults).
- [`./references/blast-radius-heuristic.md`](./references/blast-radius-heuristic.md) — the 3-criteria ADR gate (irreversible / multi-module / legitimate alternatives), scoring, target counts.
- [`./references/critic-phase.md`](./references/critic-phase.md) — Step 7 dispatch + resolution loop + pre-write backstop scans; architecture-design's delta over the shared critic (F5 floor, F6 = NFR-leak + strawman-ADR + §2-vs-repo, F1 = strategic-vector drift).
- [`./references/critic-prompt.md`](./references/critic-prompt.md) — canonical agent prompt body for the Step 7 critic. 6 failure classes adapted for the SAD.
- [`./references/c4-mermaid-syntax.md`](./references/c4-mermaid-syntax.md) — C4Context + C4Container Mermaid cheatsheet for §3/§5.
- [`./references/ask-examples.md`](./references/ask-examples.md) — architecture-design-specific question shapes (Surface, UI-architecture, strategic-with-ADR-spawn, blast-radius gate, Save-as-OQ follow-up, critic-finding resolution).
- [`./references/checklist.md`](./references/checklist.md) — full Definition of Done + anti-patterns + N/A logic + ADR count expectations.
- [`../_shared/interview-depth.md`](../_shared/interview-depth.md) — the easy/medium/hard dial set in step 1 (per-section question volume + autonomy).
- [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md) — how the §3/§5 C4 diagrams are confirmed in prose (write → validate → describe), never as raw source.
- [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md) — validate every C4 block after writing it.
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — the target-surface taxonomy (C4-container-grounded); architecture-design owns the selection (§4 first decision → frontmatter `target_surfaces`), downstream reads it.
- [`./templates/sad-template.md`](./templates/sad-template.md) · [`./templates/adr-template.md`](./templates/adr-template.md) · [`./templates/c4-context.md`](./templates/c4-context.md) · [`./templates/c4-container.md`](./templates/c4-container.md) · [`./templates/deployment.md`](./templates/deployment.md) — output scaffolds; inline comments are the per-section generation contract. (C4 syntax → [`./references/c4-mermaid-syntax.md`](./references/c4-mermaid-syntax.md).)
