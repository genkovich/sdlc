# Critic phase — Protocol Step 7 for architecture-design

Read [`../../_shared/critic.md`](../../_shared/critic.md) for the canonical dispatch + the F1–F6 skeleton. architecture-design supplies only the dispatch contract, the resolution loop, the pre-write backstop scans, and the F5/F6/F1 specialization below; the agent prompt body lives in [critic-prompt.md](./critic-prompt.md).

## TL;DR (короткий вступ українською)

Крок 7 — окремий **subagent зі свіжими очима** (англ. *clean-context critic*: він НЕ бачив діалогу з користувачем). Дивиться фінальний `sad.md` і шукає **6 класів проблем**:

| Клас | Що шукає | Простіше |
|---|---|---|
| **F1 Strategic-vector drift** | §4 каже одне, а §6 показує інше | «стратегічна нитка зривається» |
| **F2 Size-class creep** | M-функція виросла у L | «обсяг розповз» |
| **F3 Defer vs PRD vector** | Відкладене рішення зачіпає PRD-критичний параметр | «відклали те, що PRD назвав ключовим» |
| **F4 Silent edits** | Текст у sad.md ≠ те, що користувач підтвердив | «тихі правки після Socratic» |
| **F5 Coverage regression** | Mermaid-блоки лишилися як шаблон, секції порожні, ADR-сироти | «структурні дірки» |
| **F6 Constraint/Quality leak** | §10 використовує число, якого нема у PRD; ADR має фейкову альтернативу | «протиріччя зі стеком або PRD-числами» |

Після критика — окрема перевірка регулярками (синтаксис Mermaid, формат назв ADR, §9 без сиріт).

---

Runs between the Socratic batch loop (Step 6 — already wrote 12 sections + ADRs to disk in incremental commits) and the finalization commit (Step 7 close). Catches **cross-section drift** caused by user edits during Step 6 (which a per-section loop cannot see — the skill never returns to a previous section after writing it), **ADR coherence problems**, **Mermaid syntax issues**, **NFR-number leaks**, and **strategic-vector contradictions**.

The actual prompt body for the sub-agent lives in [critic-prompt.md](./critic-prompt.md). This file is the dispatch contract + resolution loop + pre-write backstop scans around it.

## Dispatch

Single `Agent` tool call — `subagent_type: "sdlc:critic"` (carries `model: opus` + `effort: high`, clean-isolated per [`../../_shared/agent-roster.md`](../../_shared/agent-roster.md); fallback `general-purpose` if the namespaced agent is unavailable), **clean context** — the sub-agent has not seen the Socratic conversation, has not seen the map/scan output, has not seen any earlier skill state.

**What to inline into the prompt** (substituted into the `{{SAD_DRAFT}}` / `{{EDITS_LOG}}` / `{{ADR_SPAWNS_LOG}}` / `{{PRD_PATH}}` / `{{CONTEXT_PATH}}` / `{{ADR_DIR_PATH}}` placeholders in `critic-prompt.md`):

1. The final post-Socratic `sad.md` contents (the full text of the file just written to disk in Step 6e — all 12 sections).
2. The Step-6 edits-log (the array of entries from [socratic-loop.md](./socratic-loop.md)).
3. The Step-6 ADR-spawns log (in-memory array: `{adr_id, title, section, triggered_by}` per spawn).
4. The paths to `docs/features/<slug>/PRD.md`, `CONTEXT.md`, and `docs/features/<slug>/adr/` — **paths only, not bodies**. The critic reads PRD/CONTEXT and inspects `adr/` files itself in clean context to avoid paraphrase-poisoning.

## Output contract

The critic returns a markdown report ≤300 words. Either:

- Literal `NO_CONTESTED_DECISIONS` → proceed straight to Pre-write regex scan + Self-check + finalization commit.
- Or 0-7 findings, one bullet per finding, citing sad-§ + PRD-§ / CONTEXT line + suggested resolution.

Failure classes the critic probes (full definitions in [critic-prompt.md](./critic-prompt.md)):

- **F1 — Strategic-vector drift.** After Socratic edits, §4 Solution Strategy or §1 Quality Goals contradicts a later section's content (e.g. §4 caps async-via-outbox but §6 happy-path shows synchronous call without outbox emit; §1 QG-1=availability dominant but §10 scenarios all measure performance).
- **F2 — Size-class creep.** Socratic edits expanded scope beyond `feature_size` (e.g. M-class feature now has 8 modules in §5 building-block view, which is L-territory; or the §5 Container count / declared surfaces grew past the size class). (§6 flow count is **not** a creep signal — architecture-design only seeds the primary flow(s); `complete-sequence-diagrams` adds the rest.)
- **F3 — Defer vs PRD vector.** A `save_as_oq`-migrated decision touched a feature PRD §6 NFR / §7 KPI / §13 Recommendation / §11 RICE named as load-bearing. **Differentiate** in finding text: «decision dropped» (hard removal) vs «decision deferred to §11 OD-table» (softer — alive in §11 with owner+due). Both can break the vector, but the deferred form is recoverable if OQ resolves before downstream stages.
- **F4 — Silent edits.** Final `sad.md` text differs from `after` field of an `edit` entry (author silently re-edited after Socratic, bypassing the contract).
- **F5 — Coverage regression.** 12 sections all filled (or `<!-- N/A: <reason> -->`)? Frontmatter `target_surfaces` non-empty AND §5 draws one C4 container per declared surface? §3 has a C4 Context Mermaid block (not template stub)? §5 has a C4 Container Mermaid block (not template stub)? §6 has ≥1 `sequenceDiagram` (architecture-design seeds the primary flow(s); `complete-sequence-diagrams` covers the rest — no cap)? §9 ADR table references every file in `adr/` (no orphans, no missing rows)? §11 contains a row for every `save_as_oq` decision in the edits-log with owner + due?
- **F6 — Constraint / Quality leak.** §10 scenarios reference numbers NOT present in PRD §6 NFR (invented targets); ADR `Considered options` lists a strawman (an alternative excluded by an existing constraint, e.g. «MongoDB» when the repo's convention file / §2 pins Postgres as the only store); §2 Constraints contradicts the repo's conventions (as reported by the architecture-map / Step-3 scan) without an Override note pointing at §11.

If the critic returns `CRITIC_BLOCKED: <reason>` (cannot Read PRD/CONTEXT/adr-dir) — STOP and report to the user. Do **not** silent-write the finalization commit.

## Resolution loop

For each finding, surface it to the user via `AskUserQuestion`. Per finding, options:

- **`Accept revert / amendment as suggested`** — apply the critic's suggested edit verbatim.
- **`Accept amendment (different wording)`** — user types alternative wording; skill applies that.
- **`Override (rationale)`** — keep `sad.md` as-is, user provides the rationale.

Constraints:

- **≤2 `AskUserQuestion` batches**, max 4 questions per batch. The user's **second** answer per finding is final (single-iteration cap, mirrors Step 6).
- **`Override` resolutions emit a bullet** into `sad.md` §1 Introduction paragraph 4 (Decision overrides), exactly: «<finding-headline> — overridden by author, rationale: <user-rationale>». This makes the deliberate choice visible to downstream skills (`sdlc:complete-sequence-diagrams`, `sdlc:api-forge`, `sdlc:decide-adr`).

After all findings resolved, re-run the SKILL.md Self-check inline non-negotiables. If any still fail — re-open the relevant `AskUserQuestion` once, then proceed.

## Pre-write backstop scans (Mermaid + ADR title + §9 orphan)

Independent of the critic, before the finalization commit run three structural scans over the post-resolution `sad.md` + `adr/`:

### Mermaid validation

Validate **every** Mermaid block in `sad.md` (§3 C4Context, §5 C4Container, §6 sequenceDiagram) per [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md) — render-parse with `mmdc` if available, else the structural lint there. A diagram that doesn't parse must never be committed (it renders as a red error box). The lint catches: matched fences (no truncation); every element (`Person`/`Container`/`ContainerDb`/`System*`/`SystemDb`/sequence actors) declared **before** any `Rel(...)` / `->>` that references it; no `Container_Bondary` / `ContainerBoundary` typos (Mermaid silently renders an empty block); no `<placeholder>` template stubs (e.g. `Person(user, "<User>", "<role + intent>")` or `Rel(svc, db, "<reads/writes>")`).

Hit → fix the syntax and re-validate (loop up to 3×). If it still won't parse, re-open `AskUserQuestion` on the offending block with options `Regenerate from CONTEXT + PRD` / `Override (rationale)`.

### ADR title format scan

For each `docs/features/<slug>/adr/NNNN-*.md`:

- Filename matches `NNNN-<kebab-case>.md` where NNNN is 4-digit zero-padded.
- Title (filename minus number) reads as a **decision** in imperative form, not a problem. Heuristics for problem-form: starts with a domain term + no verb (`0003-rate-limiting.md` ✗ — describes the problem; `0003-sliding-window-with-redis.md` ✓ — describes the chosen approach).
- File has Status = `Accepted` (not `Proposed` — this skill is synchronous).

Hit → re-open `AskUserQuestion` on the ADR with options `Rename to decision-form (suggested: <kebab>)` / `Keep as-is (rationale)`.

### §9 orphan scan

- Every file in `docs/features/<slug>/adr/` has a row in `sad.md` §9 table.
- Every §9 row references a file that exists in `adr/`.

Hit → re-open `AskUserQuestion` to fix the mismatch (add missing row / remove ghost row / locate missing file).

These three scans are the safety net if the critic missed something (e.g. truncated output, or critic prioritised F1-F4 over F5 due to ≤7 findings cap).

## Failure modes

- **Critic timeout / error** → STOP, report to user. Never fall back to silent finalization commit.
- **Critic returns malformed output** (no bullets, no `NO_CONTESTED_DECISIONS`, no `CRITIC_BLOCKED`) → re-dispatch once with «Your previous output did not match the required format» appended; if still malformed → STOP and ask the user how to proceed.
- **User picks `Override` for every finding** → allowed (SAD authorship is the user's call), but every override emits a §1 ¶4 bullet so the override trail is auditable.
- **Regex scan hits 5+ times** → likely indicates the Step-5 draft generation hygiene check failed (see [draft-generation.md](./draft-generation.md) §«Pre-Socratic hygiene»). Report to user as a process anomaly + ask whether to re-run the section's batch (single section re-do is OK; full Step-6 redo is not — too much churn).
