---
name: break-tasks
description: >
  Use to break a designed feature into atomic, ≤1-day tasks with a dependency graph, a
  per-task Definition of Done, and a machine-readable tasks.json that the implement-tasks engine
  consumes. Triggers on "task breakdown for {slug}", "break down tasks for {slug}",
  "tasks for {slug}", "plan the work for {slug}", "sprint plan for {feature}", "stage 13 for {slug}",
  "/sdlc-break-tasks {slug}". Reads PRD.md + sad.md + Accepted ADRs (+ data-model + openapi if present),
  writes docs/features/{slug}/tasks/{_epic,tracker,<task>}.md AND docs/features/{slug}/tasks/tasks.json.
  Tracker export to any issue tracker is optional and tool-neutral. Hard-refuses if PRD.md or sad.md
  or an Accepted ADR is missing. Stories LINK to upstream artefacts (PRD AC §, SAD §6, data-model,
  openapi), they do not duplicate them.
triggers:
  - /sdlc-break-tasks
  - "task breakdown for"
  - "break down tasks for"
  - "tasks for"
  - "plan the work for"
stage: "13"
---

# Skill: break-tasks (SDLC stage 13)

Task-breakdown generator: atomic tasks ≤1 day, each a separately reviewable change (≤~500 LOC preferred), with a visible dependency graph and a Definition of Done per task. One task = one focused Claude session = one PR. "Build the feature" is not a task — break it down.

Task files **link** to upstream artefacts (`PRD.md §AC-N`, `sad.md §6 UC-N`, `data-model.md`, `contracts/openapi.yaml`, `adr/NNNN-*.md`) — they do not duplicate them. Alongside the human-facing markdown, this skill emits **`tasks.json`**, the contract the `implement-tasks` engine reads to build its dependency DAG.

This is the **stage 13 runner** and the keystone that closes the cycle: the markdown is for humans, the `tasks.json` is the machine handoff to `implement-tasks`.

## Owner

Tech Lead.

## When to use

- "task breakdown for <slug>", "break down tasks for <feature>", "sprint plan for <feature>", "run stage 13".
- User has PRD + sad.md + Accepted ADRs and is about to start implementation (or create tickets in Jira / Linear / Issues).
- `/sdlc-break-tasks <slug>` as explicit invocation.
- Skip if the task-breakdown already exists and `implement-tasks` is mid-run.

## Inputs

- `<slug>` — feature slug.
- **Gate (hard refuse):** `docs/features/<slug>/PRD.md` + `docs/features/<slug>/sad.md` + ≥1 Accepted ADR in `adr/`. Missing → STOP and point at the producing skill (`write-prd` / `architecture-design` / `decide-adr`).
- Read directly (not via an index): PRD §5 AC + §6 NFR, sad §5 module boundaries + §6 runtime + §9 ADR index, each Accepted ADR, and — if present — `data-model.md` and `contracts/openapi.yaml`.

## Protocol

1. **Prereq check (hard).** `test -f docs/features/<slug>/PRD.md && test -f docs/features/<slug>/sad.md && ls docs/features/<slug>/adr/*.md` → exit ≠ 0 = refuse with the missing artefact named.
2. **Read upstream directly.** PRD §5 AC + §6 NFR (what to deliver), sad.md §5 module boundaries (task scope) + §6 runtime flows + §9 ADR index, each Accepted ADR (constraints), data-model.md (invariants if DB), openapi.yaml (contract). No intermediate index — each task links back to the section it derives from.
3. **Scaffold output.** `mkdir -p docs/features/<slug>/tasks/` → create `tasks/_epic.md` (summary + links + the DAG `flowchart`), `tasks/tracker.md` (status table), one `tasks/<task-slug>.md` per task. Templates → [`./templates/_epic.md`](./templates/_epic.md), [`./templates/tracker.md`](./templates/tracker.md), [`./templates/task.md`](./templates/task.md). **Validate the `_epic.md` `flowchart` per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md)** (render-parse with `mmdc` if available, else the structural lint; fix before committing).
4. **Identify work-items by layer.** Generic, stack-agnostic layers: `migration` (DB) · `domain` (entities/invariants) · `infra` (repo/persistence) · `app` (service/use-case) · `ports` (handler/API) · `ui` (UI components / screens / view-state — only when a UI surface is declared) · `tests` · `wiring` (composition/DI) · `docs`. **`sad.md` frontmatter `target_surfaces` gates which layers appear** (→ [`../_shared/surfaces.md`](../_shared/surfaces.md)): a `web-frontend` / `mobile-app` / `desktop-app` surface adds `ui` tasks; a backend-only feature emits domain/infra/app/ports (no `ui`); a `cli` feature app/ports; a `worker` domain/infra. Each `ui` task **names the existing components / tokens / styling it reuses** (from `architecture-map.md` §Frontend) — a *new* component is listed only when no existing primitive fits. List 8–20 items by size (see [`../_shared/size-matrix.md`](../_shared/size-matrix.md)).
5. **Atomic check.** Each task ≤1 working day. More → split. A change >~500 LOC is a smell that the task is too wide.
6. **Dependency graph.** For each task, `deps: [...]`. Identify parallel branches (e.g. the migration and a pure-domain task can start together). This graph IS the DAG `implement-tasks` will topologically sort into phases.
7. **Per-task DoD.** Each task is testable: «unit tests for the new validation pass», «migration applies and reverts cleanly», «handler returns the PRD'd outcome for AC-03». No subjective «done when I say so».
8. **AC refs + files hint.** Each task lists the `acs` it satisfies (PRD §5 IDs) and a `files_hint` — the directories/files it will touch. `files_hint` lets `implement-tasks` serialize tasks whose file sets overlap, and `layer: migration` is always serialized (ordered migration sequence); `layer: ui` is **not** auto-serialized — UI tasks parallelize unless their `files_hint` overlaps. A migration task's `files_hint` is the **staged** pair `docs/features/<slug>/migrations/<NN>_*` (which `implement-tasks` promotes into the live `migrations/` when it runs the task) — not a live `migrations/` path.
9. **Estimate + owner.** S/M/L or hours; a named owner (or `<TBD lead>`). Adapt to the team's sizing if any (S = 2h, M = half-day, L = day, otherwise split).
10. **Emit `tasks.json`** (step contract below) — the same model the markdown reflects, in machine form, at `docs/features/<slug>/tasks/tasks.json`.
11. **Optional tracker export.** If an issue-tracker MCP is connected (Jira / Linear / GitHub Issues / Redmine — whichever the repo uses), offer to create tickets from `_epic.md` + the task files. Otherwise provide copy-paste-ready bodies. Never hard-bind to one tracker.
12. **Self-check.** Every task ≤1 day; DAG acyclic with ≥1 parallel branch where the work allows; DoD per task; `acs` cover every PRD §5 AC; `tasks.json` validates against the contract.
13. **Propose commit + handoff.** `13: task-breakdown for <slug> (breakdown + tasks.json)`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* + *Review* (`tasks/`, `tasks/tasks.json`) + *Run next* (`/clear`, then `/sdlc-plan-tests <slug>`, then `/sdlc-implement-tasks <slug>`).

## `tasks.json` contract (read by `implement-tasks`)

```json
{
  "slug": "<slug>",
  "tasks": [
    {
      "id": "T1",
      "title": "imperative, specific",
      "layer": "migration|domain|infra|app|ports|ui|tests|wiring|docs",
      "deps": ["T0"],
      "acs": ["AC-01", "AC-02"],
      "dod": "one testable sentence",
      "files_hint": ["path/or/dir/the/task/touches"]
    }
  ]
}
```

- The markdown task files and `tasks.json` use the **same field names** (`deps`, `acs`) — this skill emits both from one model, so there's no translation layer to drift.
- `deps` must form a **DAG** (no cycles) and reference only ids present in the file. The DAG edges are the `deps` arrows; the `_epic.md` `flowchart` renders the same edges.
- **Serialization lanes** (how `implement-tasks` reads the DAG): `layer: migration` tasks are serialized into the ordered migration sequence; `layer: ui` is **not** auto-serialized (UI tasks parallelize); tasks with overlapping `files_hint` are serialized into the same lane regardless of layer. Everything else with no shared lane and satisfied `deps` runs in parallel within a phase.
- Which layers are present is gated by `sad.md` frontmatter `target_surfaces` (a UI surface adds `ui`; a backend-only feature has none) → [`../_shared/surfaces.md`](../_shared/surfaces.md).

## Questions for discussion

- Dependencies between tasks (the DAG)?
- What parallelizes — which branches start together?
- DoD per task?
- Who is the owner?
- Estimate (S/M/L or hours)?

## Definition of Done

- `tasks/_epic.md` + `tasks/tracker.md` + one `tasks/<task>.md` per task exist, linking (not duplicating) upstream.
- `tasks/tasks.json` exists and validates: acyclic `deps`, every `acs` entry is a real PRD §5 AC, every task has a `dod` and a `files_hint`.
- Every task ≤1 day with an owner; the DAG shows ≥1 parallel branch where the work allows.
- Every PRD §5 AC is covered by ≥1 task's `acs`.
- Each task = reviewable PR (≤~500 LOC preferred).

## Anti-patterns

- **«Build the feature»** as one task. Break into ≥8 atomic ones.
- **5-day monster tasks** → unreviewable. Split.
- **No dependencies** → parallel starts that block each other the next day.
- **No per-task DoD** → «done when I decide».
- **No owner** → nobody starts, or everyone assumes the other will.
- **Sizing without reference (S/M/L).** If the team has no calibration — S = 2h, M = half-day, L = day, otherwise split.
- **Hard-binding to one tracker** (Jira-only language). Export is optional and tool-neutral.
- **Task body duplicates PRD AC / sad §6 / data-model verbatim** — link, don't paste.
- **`tasks.json` out of sync with the markdown** — they must reflect the same model.
- **A task that violates a Hard Rule** from PRD §6 NFR / sad §11 (e.g. «edit another module» when the architecture forbids it).
- **A `ui` task that recreates an existing primitive** (Button/Card/modal) or introduces a second styling system instead of composing `architecture-map.md` §Frontend.

## References & template

- [`./templates/_epic.md`](./templates/_epic.md) · [`./templates/tracker.md`](./templates/tracker.md) · [`./templates/task.md`](./templates/task.md)
- [`../_shared/size-matrix.md`](../_shared/size-matrix.md) — how many tasks for the feature size.
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — `target_surfaces` (read from `sad.md`) gates which layers appear; a UI surface adds the `ui` layer (not auto-serialized).
- [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md) — validate the `_epic.md` DAG `flowchart` before committing.
- [`../_shared/handoff.md`](../_shared/handoff.md) — the stage-handoff block emitted as the final output.

## Example invocation

> **User:** `/sdlc-break-tasks rate-limiting-per-user`
>
> **Skill behavior:**
> 1. `test -f` PRD + sad.md + ADR-0001 → OK.
> 2. Reads PRD §5 AC, sad.md §5 (module `middleware/rate-limit/*`, `internal/quota-config/*`), `target_surfaces: [backend-service]` (no `ui` layer), data-model (staged migration `<NN>_quota_config`), ADR-0001.
> 3. `mkdir -p docs/features/rate-limiting-per-user/tasks/` → writes `_epic.md` (with the DAG `flowchart`, validated per `mermaid-check.md`), `tracker.md`, 10 `<task-slug>.md` stories that LINK to PRD §AC-3 / sad.md §6 UC-1 / ADR-0001 instead of duplicating their content, and `tasks.json`.
> 4. Tasks: (T1) staged migration `<NN>_quota_config` + down; (T2) entity `RateLimitTier` + `QuotaConfig` domain; (T3) repo for quota-config; (T4) service `QuotaConfigService`; (T5) handler `POST /v1/quota-configs` + tests; (T6) handler `GET/PATCH/DELETE` + tests; (T7) middleware (token-bucket); (T8) wiring in composition root; (T9) metrics + event `rate_limit.exceeded.v1`; (T10) E2E test on happy + 429.
> 5. Each ≤1 day. T5/T6 split because together >500 LOC.
> 6. Deps: T2→T3→T4→T5→T6; T1 parallel with T2; T4→T7→T8; T9→T8; T8→T10. `layer: migration` (T1) serialized; T5/T6 share a `files_hint` lane → serialized.
> 7. DoD: T1 — staged migration promoted to live then applies + reverts cleanly; T5 — handler tests pass + openapi example valid for AC-03; T10 — E2E green.
> 8. Estimate: T1=S, T2=M, T7=L, … total ~9 person-days.
> 9. Owners: T1–T4 — @alice; T5–T8 — @bob; T9–T10 — @charlie.
> 10. Self-check → atomic ✅, DAG acyclic with ≥1 parallel branch ✅, DoD per task ✅, every PRD §5 AC covered by ≥1 `acs` ✅, `tasks.json` validates ✅.
> 11. Commit: `13: task-breakdown for rate-limiting-per-user (breakdown + tasks.json)`.
> 12. Handoff block → *Run next* `/clear` → `/sdlc-plan-tests rate-limiting-per-user` → `/sdlc-implement-tasks rate-limiting-per-user`.
