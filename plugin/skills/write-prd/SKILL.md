---
name: write-prd
model: opus
effort: high
agents: [critic]
description: >
  Use to turn a raw feature idea into a reviewed PRD.md — a lightweight Socratic interview
  front (capture the idea, deep-dive the problem) merged with a full product spec (context,
  goals, user stories, acceptance criteria, NFRs, KPIs). Triggers on "/sdlc-write-prd {slug}",
  "write PRD for {slug}", "draft PRD for {slug}", "PRD для {slug}", "write spec for {slug}",
  "product requirements for {slug}", "напиши PRD {slug}", "опиши вимоги", "зафіксуй ідею".
  Opens by setting the interview-depth dial (easy/medium/hard), drafts from templates/PRD-template.md,
  validates each acceptance criterion Socratically, runs a clean-context critic (sdlc:critic),
  then writes docs/features/{slug}/PRD.md. Hard refuse if idea-brief.md or CONTEXT.md missing.
triggers:
  - /sdlc-write-prd
  - "write PRD for"
  - "draft PRD for"
  - "PRD для"
  - "write spec for"
  - "product requirements for"
stage: "03"
---

# Skill: write-prd (SDLC stage 03 — PRD drafter)

Turns a one-line idea into a reviewed `PRD.md`: a lightweight interview captures and stress-tests the idea, then the skill drafts a product spec (context → goals → user stories → acceptance criteria → NFRs → KPIs), validates it Socratically, and runs a clean-context critic before writing. Less typing, more reviewing. This file is the spine; detail lives in `references/`.

The Socratic machine, the critic, and the ask-style are **shared** — this skill keeps only its deltas:
→ [`../_shared/socratic-loop.md`](../_shared/socratic-loop.md) · [`../_shared/critic.md`](../_shared/critic.md) · [`../_shared/ask-style.md`](../_shared/ask-style.md)

Depth governs question volume + autonomy → [`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

PM + Tech Lead (co-authors). PM drives goals / non-goals / KPIs; Tech Lead drives context patterns and the acceptance-criteria coverage.

## Inputs

**Hard required** (skill stops without them):

- `<slug>` — kebab-case feature slug.
- `docs/features/<slug>/idea-brief.md` — problem, RICE, Recommendation (§13), Out of scope (§6). Missing → «run `/sdlc-interview <slug>` first».
- `docs/features/<slug>/CONTEXT.md` — canonical glossary (role names, domain terms). Missing → «run `/sdlc-fix-term <slug>` first». No silent fallback.

**Optional**:
- `docs/features/<slug>/.size` — depth hint (MVP vs Full per the size matrix). Read if present; **established here if absent** (step 1 classifies + writes it), so downstream stages never silently default to M.
- `--reference <path-to-module>` — passed at invocation; pre-selects the «Reference module code» channel in step 3.

## Protocol

1. **Prereq check + read context + set interview depth.** `test -f` both required inputs and stop with the appropriate error if either is missing. Then: if `CONTEXT.md` exists, load its `## Glossary` as session state (canonical roles + terms). If `.size` exists, read it to size the PRD's depth; **if absent, establish it now** — classify the feature via the 4 signals in [`../_shared/size-matrix.md`](../_shared/size-matrix.md) (PR count / time-to-merge / new module·API·migration / breaking changes), confirm in one bundled `AskUserQuestion` (at `easy` depth, take the matrix default and record it in the assumptions ledger), and write `docs/features/<slug>/.size` — so every later stage reads a real size instead of silently defaulting to M. `classify-size` stays the utility to re-classify when scope changes. If `docs/architecture-map.md` exists (from `map-architecture`), read it so the PRD is **architecture-aware** — it informs §1 Context, §2 Constraints, and §3 Non-goals (what the existing system already does / can't do). Absent → suggest running `/sdlc-map-architecture` first, but proceed (the PRD is product-level and can be captured without it). **Do not leak the map's tech into §5 AC** — AC stay business-observable; the map shapes constraints, not acceptance criteria. **Then set the interview depth (the opening question):** **if `.claude/sdlc.local.md` is absent, auto-create it** with the documented default frontmatter (every key + its allowed values explained inline) and patch `.gitignore`; then read `interview_depth` from it (else default medium), and — unless a `--depth=easy|medium|hard` arg was passed (which skips the question) — ask ONE depth-selection `AskUserQuestion` phrased per [`../_shared/ask-style.md`](../_shared/ask-style.md), with the saved/medium value as the «(Recommended)» first option, overridable per run. The chosen level governs the step-2 deep-dive volume and the step-7 Socratic volume → [`../_shared/interview-depth.md`](../_shared/interview-depth.md). (Completeness — §5's 5-type AC floor **and** §4→§5 use-case floor — is unaffected by depth.)

2. **Capture the idea (interview front).** One `AskUserQuestion` for the raw idea in 1–3 sentences (persist verbatim as the baseline). Then a Socratic deep-dive across problem clarity / success criteria / constraints / strategic fit, delivered in batches of 2–3 — its volume scales with the depth dial (easy: only the few un-inferable ones, then a stated-assumptions ledger; medium: 3–5; hard: walk every angle, foreground each trade-off). Phrase every question per [`../_shared/ask-style.md`](../_shared/ask-style.md).

3. **Reconcile the glossary in-flow (a hard rule, at every depth).** On every new or unknown domain term that surfaces in the interview or the draft, invoke `/sdlc-fix-term <slug>` for it **immediately** — compare it against `CONTEXT.md` and add/update the definition before continuing. By the time the PRD is written, every §4 role and §5 domain term is already glossary-canonical; the glossary is never a deferred batch.

4. **Ask which extra channels to read** (multi-select `AskUserQuestion`): reference module code / project docs / MCP-Atlassian (Confluence) / MCP-Atlassian (Jira) / knowledge-base / none. For each picked channel ask the **specific** path/query — no silent broad scans. If `--reference` was passed, pre-select `Reference module code`.

5. **Read selected channels.** Reference module → extract entity types, error sentinels, status constants, authz checks. MCP-Atlassian → `mcp__atlassian__search` for specified pages/tickets. Docs / RAG → only the paths/topics the user named.

6. **Read the template + draft §1–§8.** Read [`./templates/PRD-template.md`](./templates/PRD-template.md) (its `<!-- Skill instruction: ... -->` comments are the per-section contract). Draft per [`./references/draft-generation.md`](./references/draft-generation.md): per-section sources, the **5 AC coverage types** (happy / error / authorization / domain invariant / cross-context), and the **stack-agnostic forbidden-token** rule for acceptance criteria. Ensure **every §4 user story has ≥1 AC in §5 at draft time** (the use-case floor applies before the Socratic walk begins).

7. **Socratic validation.** Walk §4 US → §5 AC → §6 NFR → §7 KPI with the shared 4-state machine (per-decision question volume scales with the depth dial — at easy, the un-asked decisions land in the assumptions ledger for a batch veto). write-prd delta → [`./references/socratic-loop.md`](./references/socratic-loop.md): AC has a 5th option «Add another AC»; the §5 coverage gate enforces **two floors** after drops/OQ-migrations — (a) ≥1 AC of each of the 5 coverage types, and (b) **≥1 AC per retained §4 user story** (regenerate/add a replacement if a type *or* a user story is left empty). **Both are floors, not dials — enforced at every depth;** only the question volume scales. The (b) floor closes the §4→§5 link so the downstream `complete-sequence-diagrams` use-case coverage + `review-feature` trace can't be undermined by a user story that lost its only AC. Maintain the edits-log.

8. **Critic + write + commit.** Dispatch the [`critic`](../../agents/critic.md) agent — `subagent_type: "sdlc:critic"` (carries `model: opus` + `effort: high`, clean-isolated context per [`../_shared/agent-roster.md`](../_shared/agent-roster.md)) — with the write-prd delta in [`./references/critic.md`](./references/critic.md) (over [`../_shared/critic.md`](../_shared/critic.md)) — inline the draft + edits-log, it Reads `CONTEXT.md` + `idea-brief.md`. Resolve findings via `AskUserQuestion` (Accept revert / Accept amendment / Override-with-rationale → §1 ¶4 bullet). Run the forbidden-token regex scan as the F6 backstop. On pass, write `docs/features/<slug>/PRD.md` (glossary already reconciled in-flow per step 3) and propose commit `03: PRD for <slug>`. **Register on the roadmap:** add/promote this feature to **Now** in `docs/roadmap.md` (via `/sdlc-roadmap`) — an outcome one-liner + a link to this feature folder + status; if it existed as a Next candidate, move it up. (If there's no roadmap yet, skip — it's optional.) Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* + *Review* (`PRD.md`, `.size`) + *Run next* (`/clear`, then `/sdlc-clarify-prd <slug>`). (If `sdlc:critic` is unavailable, fall back to a `general-purpose` Agent with the same delta.)

## Definition of Done

- `docs/features/<slug>/PRD.md` written; all sections filled (or `<!-- N/A: reason -->`).
- `docs/features/<slug>/.size` exists after this stage (read if it was present, else classified + written here).
- §5 holds ≥1 AC of each of the 5 coverage types after drops/OQ-migrations, **every §4 user story has ≥1 AC** (the use-case floor — no retained US left with zero ACs), and **0 forbidden tokens** (HTTP verbs / URL paths / status-code numerics / `module.error_name` strings / JSON fragments / SQL constructs).
- §4 roles match the `CONTEXT.md` glossary exactly (no invented `user`/`admin`).
- §8 Open Questions each carry owner + due (no lone «TBD»).
- Edits-log maintained; critic (`sdlc:critic`) ran on the post-Socratic draft; every finding resolved or overridden.

## Anti-patterns

- **Skipping the interview front** and reconstructing the idea from the model's guess. Capture + deep-dive must actually fire `AskUserQuestion`.
- **Naming concrete technologies in §1–§3** (a specific datastore, broker, framework, or library). The PRD is WHAT + WHY; technology choices belong to `architecture-design`.
- **Implementation leak in AC** — HTTP/status/error-code/SQL detail. That mapping lives in `api-forge` and `decide-adr`.
- **Dispatching `general-purpose` instead of `sdlc:critic`** without first checking availability. The namespaced critic carries the correct model/effort and clean context; fall back only on confirmed unavailability.
- **Treating brainstorm or initiatives artifacts as PRD inputs.** PRD draws only from CONTEXT + idea-brief (required) plus user-selected additional channels.
- **Inventing role names or domain terms** not in CONTEXT glossary. The glossary is canonical; the PRD never introduces new role names.

## References & template

- [`../_shared/interview-depth.md`](../_shared/interview-depth.md) — the easy/medium/hard dial set in step 1 (question volume, autonomy).
- [`./references/draft-generation.md`](./references/draft-generation.md) — per-section sources, 5 AC coverage types, stack-agnostic forbidden tokens.
- [`./references/socratic-loop.md`](./references/socratic-loop.md) — write-prd's delta over the shared Socratic loop (sections walked, use-case floor, decision-types).
- [`./references/critic.md`](./references/critic.md) — write-prd's delta over the shared critic (F5 structural floor + F6 forbidden-token specialization).
- [`./references/ask-examples.md`](./references/ask-examples.md) — explanatory `AskUserQuestion` shape for US / AC / NFR / KPI + critic-finding examples (junior-friendly Ukrainian).
- [`./references/checklist.md`](./references/checklist.md) — Definition of Done + full anti-patterns.
- [`./templates/PRD-template.md`](./templates/PRD-template.md) — output scaffold; inline `<!-- Skill instruction: ... -->` comments are the per-section generation contract.
