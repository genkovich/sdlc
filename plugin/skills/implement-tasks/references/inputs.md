# Inputs + preconditions (step 1)

## Hard gate

`docs/features/<slug>/tasks/tasks.json` must exist and parse as JSON. Missing or malformed → refuse: «run `/sdlc-break-tasks <slug>` first (it emits tasks.json)». Do not try to reconstruct tasks from the markdown — `docs/features/<slug>/tasks/tasks.json` is the contract.

## Validate the contract

The loaded `tasks.json` must satisfy the shape from the `break-tasks` skill:

- top-level `{ slug, tasks: [...] }`.
- each task: `id` (unique), `title`, `layer` (`migration|domain|infra|app|ports|ui|tests|wiring|docs`), `deps` (array of existing ids), `acs` (array of PRD §5 AC ids), `dod` (one testable sentence), `files_hint` (array of paths/dirs).
- `deps` forms a DAG (no cycles) — verified in step 4. A cycle is a hard error: report the cycle and stop (it is a `break-tasks` bug, not an `implement-tasks` one).

## Scaffold task sets (from `map-architecture` greenfield)

A `tasks.json` with `slug: "_scaffold"` and `layer: scaffold` tasks comes from `map-architecture`'s greenfield foundation (not from `break-tasks`). These tasks have **no feature `acs`** — they create the project skeleton (structure, baseline module, test harness, migration tooling, CI, conventions doc). Handle them specially:

- **The skeleton smoke test is the red→green anchor**, not a feature AC: RED = «the project does not build / boot / the tooling doesn't run»; GREEN = «build + boot + the empty test suite + the migration tool all succeed». Write that smoke test as part of the scaffold (task S2 in the foundation contract) and drive the skeleton to make it pass — no per-folder TDD theatre.
- Read `docs/architecture-map.md` (`mode: greenfield-bootstrap`) for the exact stack + conventions to scaffold to.
- After the scaffold is green the repo is real, and the normal per-feature flow (`write-prd → … → implement-tasks`) builds into it with real feature TDD.

## Context the agents read directly

The engine does **not** paste these into prompts — each agent (or the sequential runner) reads them itself, so there's no paraphrase drift:

- `docs/features/<slug>/PRD.md` — §5 acceptance criteria (the source of truth for what each test asserts).
- `docs/features/<slug>/test-plan.md` — the AC→test map, if `plan-tests` ran.
- `docs/features/<slug>/data-model.md` + the **staged** migration files under `docs/features/<slug>/migrations/` — the schema the code targets (a `layer: migration` task promotes them into the live migrations tree; see «Staged migrations → promote» below).
- `docs/features/<slug>/contracts/openapi.yaml` — the API contract handlers must match.
- `docs/features/<slug>/sad.md` + Accepted `adr/` — the architecture and the locked decisions.
- `docs/architecture-map.md` (from `map-architecture`, if present) — the existing system's conventions the new code must match (module wiring, error handling, IDs, tests, migrations; **for a `ui` surface, §Frontend / UI foundation — the design system / components / tokens / styling to reuse**) + the closest precedent to copy (including the **closest UI precedent** for a new screen). Saves the agents re-discovering the patterns.

## Staged migrations → promote before running

`generate-data-model` stages each migration as `docs/features/<slug>/migrations/<NN>_<verb>_<entity>.up.sql` + `.down.sql` (feature-local ordinal) — **not** in the live migrations tree, so a design-stage schema can't be applied to a real DB before the feature is built. The `layer: migration` task(s) own **promotion** — this is the wiring `generate-data-model` set up:

1. **Promote in ordinal order.** For each staged `<NN>_*` pair (ascending), copy it into the repo's live migrations directory under the repo's detected convention — sequential → the **next free number** (`000023_*`); timestamped → a fresh timestamp re-stamped **at promote-time** — preserving the intra-feature order. The number/timestamp is assigned **now, at promote-time**, so two features building around the same time never collide and the live sequence stays correct. The SQL body is copied **verbatim** — never rewritten during promotion. After promotion the live file is canonical; the staged copy is the frozen design record (git keeps it; don't hand-edit it).
2. **Then apply + verify.** Run the migration with the repo's tool against the (ephemeral, testcontainers) DB; the task's DoD «migration applies and reverts cleanly» is checked on the promoted file. The feature's integration tests run against the promoted schema.
3. **Commit** the promoted live file(s) with the migration task (the staged pair under `docs/features/<slug>/migrations/` was already committed by `generate-data-model`).

A `layer: migration` task with **no** staged file under the feature's `migrations/` is a `break-tasks`/`generate-data-model` mismatch — surface it, do not invent SQL.

## `ui`-layer tasks

A `layer: ui` task (present only when `sad.md` frontmatter `target_surfaces` declares a UI surface — `web-frontend` / `mobile-app` / `desktop-app`) runs through the **same TDD cycle** as any other task; it just follows the **repo's frontend test convention** — component / e2e-through-UI runners detected from `package.json` scripts (Playwright / Storybook / a visual-diff tool / etc.) — **not** a backend assumption. No engine change: command-detection already picks up frontend scripts in its cascade.

**Reuse the UI foundation (don't reinvent).** A `ui` task **composes the existing design system** from `architecture-map.md` §Frontend — reuse the existing components / shared primitives, pull design tokens (colors / spacing / typography) from the repo's token source, and build in the repo's **one** styling approach. Find the **closest existing screen/component** (the §Frontend UI precedent) and extend/compose it; write a **new** component only when no existing primitive fits, in the repo's styling approach — never a second one. This is the frontend echo of "match the repo + copy the closest precedent" → [`../../_shared/surfaces.md`](../../_shared/surfaces.md).

## Repo state

- Note the current branch. If `branch_strategy: feature` and the repo is on its default branch, create/switch to a feature branch before any commit (see [`settings.md`](./settings.md)).
- Do not touch unrelated dirty changes — work only the files each task's `files_hint` names.
