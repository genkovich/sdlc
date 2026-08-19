---
name: api-forge
description: >
  Use to derive the API contract for a feature — an OpenAPI 3.1 document at
  docs/features/{slug}/contracts/openapi.yaml plus a drift/sync report, and the
  right contract artifact per surface (events.md for async, cli.md for CLI,
  public-api.md for library/SDK). Triggers on "api for {slug}", "openapi for {slug}",
  "API contract for {slug}", "lock the interface for {slug}", "events for {slug}",
  "/sdlc-api-forge {slug}", "контракт API для {slug}", "OpenAPI для {slug}", "опиши ендпоінти".
  The contract is never hand-written: it is a derived function of data-model.md (typed
  fields + constraints), sad.md §6 sequence diagrams (error branches, async actors), and
  PRD.md acceptance criteria.
  Hard gate: docs/features/{slug}/PRD.md. data-model.md is recommended but optional —
  without it the skill runs in scenario B (PRD + sequences only) and fills
  unresolved_origins in the sync report.
  Renamed from define-api in v3.3.0; the legacy name is kept as a deprecation wrapper.
triggers:
  - /sdlc-api-forge
stage: "10"
---

# Skill: api-forge

Projects the upstream artifacts into one **interface contract**. By default that's an HTTP/OpenAPI contract; this skill is **interface-kind aware** — and the kind comes from the surface(s) `architecture-design` declared in `sad.md` frontmatter `target_surfaces`, **read here, not re-derived** (→ [`../_shared/surfaces.md`](../_shared/surfaces.md)). For a non-HTTP project it produces the matching contract form:

- **HTTP / REST** (default) → `contracts/openapi.yaml` (OpenAPI 3.1) + `api-sync-report.md`.
- **gRPC / RPC** → a `.proto` (or the repo's IDL) with the same derive-and-drift discipline.
- **CLI** → `contracts/cli.md` — the command/flag/exit-code surface derived from the AC.
- **Library / SDK** → `contracts/public-api.md` — the public signatures/types the feature exposes.
- **Event-only / worker** → just `contracts/events.md` (no request/response surface).
- **No external interface** (pure internal logic) → **skip** with a one-line note in the report; go straight to `break-tasks`.

Whatever the form, the contract is **derived from `data-model.md` + the sad.md §6 sequences + the PRD's AC, never typed by hand** — generation that diverges from the model or the sequences is the bug this skill exists to catch. The rest of this file details the HTTP path (the common case); the same derive → drift-check → reconcile loop applies to the other forms with the form-appropriate artifact.

This skill keeps only its own machinery. Depth (events doc only when async; one resource vs full surface) follows the **size matrix** → [`../_shared/size-matrix.md`](../_shared/size-matrix.md).

## Owner

Backend Lead (drives the interface). The PM confirms each endpoint maps to a real user story; a frontend / consumer engineer is the first reader — the contract is locked before they start integration.

## Inputs

- `<slug>` — same feature slug used by every earlier stage.
- **Gate (hard-refuse if missing):** `docs/features/<slug>/PRD.md`. It is the source of user stories and acceptance criteria; without it the endpoint list would be invented. If absent → STOP and point: «run `/sdlc-write-prd <slug>` first».
- **Recommended (presence determines scenario A vs B):**
  - `docs/features/<slug>/data-model.md` — strongest source of typed fields and constraints. Presence triggers scenario A (typed contract). Absence triggers scenario B (PRD/sequence-derived contract with `unresolved_origins` block).
  - `docs/features/<slug>/sad.md` §6 — the Mermaid `sequenceDiagram` blocks. Their `alt`/`else` branches become error `responses`; an async participant (`<message-bus>` / `<external-system>`) on a mutating flow marks its endpoint `Idempotency-Key`-required and seeds `events.md`. Absent → note the gap and still generate.
- **Optional (auto-detected, enrich when present):**
  - `docs/features/<slug>/adr/*.md` — architecture decisions that override defaults (versioning, error format, auth scheme).
  - `docs/features/<slug>/CONTEXT.md` — glossary terms become schema names verbatim.
  - **Existing `contracts/openapi.yaml`** — if present, diff and update in place, never overwrite whole-cloth.
  - `docs/features/<slug>/.size` — depth hint. Absent → default to M (full surface).

If any recommended/optional input is missing, the skill still generates a usable contract. The `api-sync-report.md` flags which enrichment was skipped and why it would have helped.

## Scenarios A vs B

The skill detects scenario from inputs and tells the user which one it is running.

### Scenario A — data-model.md exists (preferred)

Contract is **derived** from the model. Every field has an `origin` in a typed entity. Constraints (`maxLength`, `pattern`, `enum`) trace back to DDL (`varchar(N)`, `CHECK`, ENUM type). Error codes derive from constraints (`UNIQUE (a, b)` → `<entity>.duplicate_<field>`). `unresolved_origins` is **empty**.

Drift check verifies field-by-field alignment. Drift in scenario A means model and contract disagree on form — human resolves which artifact is right.

### Scenario B — data-model.md missing (fallback)

Contract is **inferred** from PRD §4 acceptance criteria + sequence diagrams + SAD §6 namespacing. Types are less precise (`string` without `maxLength`, no enum patterns yet). Error codes derive from `alt`-blocks in sequences, not from constraints.

`unresolved_origins` lists every field whose origin is "inferred from PRD/sequence, needs confirmation when data-model.md arrives". This is **not an error** — it is **declared incompleteness**, visible to the team.

### Reconcile (`--reconcile` flag)

When `data-model.md` arrives after a scenario-B run, re-run with `--reconcile`. It:

1. Re-reads all inputs.
2. Switches scenario B → A.
3. Tightens types: `string` becomes `string` + `maxLength` where DDL exists.
4. Promotes low-confidence origins to high.
5. Empties `unresolved_origins`.
6. Surfaces any field that **had** an inferred origin but **now disagrees** with the model — that is real drift, not stale incompleteness.

`info.version` is never bumped silently; the user bumps semver explicitly with a CHANGELOG line.

## Defaults

Fixed minimum, not invented per feature; an `adr/*.md` overrides any of them and the report records "deviation by ADR-NNNN".

| Topic | Default | Rationale |
|---|---|---|
| OpenAPI version | `3.1.0` | JSON Schema 2020-12 reused by JSON validators; native webhooks; `nullable` via `type: [string, null]`. |
| Error response shape | `{code, message, details?}` snake_case | Homogeneous FE handling; `code` gives machine rule "retry vs change request". |
| Error `code` namespacing | `<module>.<error_name>` | `lesson.duplicate_slug`, `lesson.module_not_found` — domain-readable, neutral convention. |
| Pagination for list endpoints | Cursor (UUID v7), not offset | Stable pages under concurrent writes; stable context for AI consumer. |
| URL versioning | `/api/v1/...` | Simpler than header versioning; cacheable; version is visible in the path. |
| Authentication | `BearerAuth` global | Global default; public endpoints declare explicit `security: []`. |
| Schema reuse | `$ref` mandatory; inline schemas forbidden | Single source of truth per type — less drift between endpoints. |
| Forbidden | `nullable: true` (3.0 style), real PII in `example`, `additionalProperties: true` on response shapes, `?v=2` query versioning, offset pagination | Well-known anti-patterns. |

## Protocol

1. **Gate + interface kind + read.** `test -f docs/features/<slug>/PRD.md` → fail = refuse with the pointer above. **Determine the interface kind — read `sad.md` frontmatter `target_surfaces` FIRST** (architecture-design already declared it; the surface picks the contract form per [`../_shared/surfaces.md`](../_shared/surfaces.md): `backend-service` → OpenAPI / gRPC / events per its sub-kind; `cli` → `contracts/cli.md`; `worker` → `contracts/events.md`; `library-sdk` → `contracts/public-api.md`; a UI surface — `web-frontend` / `mobile-app` / `desktop-app` — *consumes* the backend contract, it does not author one). **Fall back to deriving the kind** from `docs/architecture-map.md` + the PRD's capabilities **only if the SAD or the field is absent** (a greenfield run where `architecture-design` was skipped). HTTP/REST → the OpenAPI path below (default); gRPC/CLI/library/event-only → produce the matching contract form with this same derive→drift→reconcile loop; **no external interface** (pure internal logic) → skip to `break-tasks` with a one-line note in the report. Then detect scenario (A if `data-model.md` exists, B otherwise). Surface a one-line "found / missing" note for sad.md and data-model.md.

2. **Copy the template.** [`./templates/openapi.yaml`](./templates/openapi.yaml) → `docs/features/<slug>/contracts/openapi.yaml`. If async flows exist, also [`./templates/events.md`](./templates/events.md) → `contracts/events.md`. If CLI surface, [`./templates/cli.md`](./templates/cli.md) → `contracts/cli.md`. If library-sdk surface, [`./templates/public-api.md`](./templates/public-api.md) → `contracts/public-api.md`. Fill `info.description` from PRD §1 (why this API exists).

3. **Derive endpoints + schemas.** One endpoint (or more) per PRD §4 user story. In scenario A, every request/response field traces to a `data-model.md` entity column — copy its constraints across (`maxLength`/`pattern`/`enum` from the model's bounded types). In scenario B, schemas are derived from PRD field names + sequence message names; `unresolved_origins` is populated. **Never invent a field with no origin in any input** — ask the user where it comes from. `$ref` every shared schema; no inline duplication. Lists paginate by cursor (`?after=&before=&limit=`), wrapped in `{items, has_next, has_prev, next_cursor}`.

4. **Derive error responses from the sequences.** Each endpoint covered by a §6 flow: turn every `alt … else … end` branch into a `responses` entry. The error body is the unified envelope **`{code, message, details?}`**; `code` follows the **neutral** convention `module.error_name` (snake_case, e.g. `lesson.not_owned`, `lesson.invalid_state`). Map status by class (4xx client / 5xx server). This closes the PRD's usual blind spot — PRD lists the happy path + a couple of errors; the sequences enumerate the authorization and concurrent-state branches the PRD omits.

5. **Async + idempotency.** A mutating endpoint whose §6 flow shows a retry note or an async actor is marked `Idempotency-Key`-required (state the TTL). For each async message, fill an `events.md` entry: event name `module.action.vN`, payload schema, producer, consumers, retry / dead-letter behaviour.

6. **Examples + placeholder data.** Every operation carries a request example + a success example + an error example, using placeholder values only (`<...>@example.test`, `+380 00 000 00 00`, `Test User`) — never real PII.

7. **Inline DRIFT CHECK (bidirectional) + write the report.** Compare the generated contract against the read artifacts and write `docs/features/<slug>/contracts/api-sync-report.md` — see [`./references/drift-check.md`](./references/drift-check.md). It has a field-origins table (one row per `operation.field`: `path | origin | confidence`) and a checklist. The check runs **both directions**:
   - **forward** (contract derived correctly): endpoint↔model, error-code↔repo, validation↔constraint, OpenAPI↔sequence.
   - **back-feed (coverage cross-check)**: every PRD §5 AC maps to ≥1 operation/response; every operation maps to a §4 user story + ≥1 AC; every `sad.md` §6 `alt`-branch has a response, and any error/authorization response the contract needs but no §6 flow shows is a **sequence gap**. A gap here is not an api bug — it's a hole upstream: surface it and offer **Fix-the-source-first**, which re-opens `write-prd` (add the missing AC) or `complete-sequence-diagrams` (draw the missing branch) before the contract is finalized.
   A **core** finding failing (or ≥3 flags total) pauses the run — resolve each via the 4-state actions: Accept-as-is / Fix-the-contract / Save-as-OQ / Fix-the-source-first. Never silently edit the sources — surface the mismatch and let the human pick the right artifact (the contract, the PRD's AC, or the sequence).

8. **Lint + write + commit.** Suggest `spectral lint contracts/openapi.yaml` (add it to the project's check target if not yet wired). On a clean check, the files are written; propose commit `api: <slug> contract`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* + *Review* (`contracts/openapi.yaml`, `api-sync-report.md`, + `events.md` if async, + `cli.md` if CLI, + `public-api.md` if library) + *Run next* (`/clear`, then `/sdlc-break-tasks <slug>`).

### Reconcile mode

`/sdlc-api-forge <slug> --reconcile`. Re-derives after an upstream artifact changed (typically `data-model.md` arrived or was tightened after a thinner first pass). It re-reads inputs, tightens loose types where the model now has a constraint, refreshes the field-origins confidence column, and — the load-bearing part — surfaces any field that **had** an inferred origin but **now disagrees** with the model. That disagreement is real drift, not stale incompleteness.

## Definition of Done

- `docs/features/<slug>/contracts/openapi.yaml` written: OpenAPI 3.1, `BearerAuth` global with public endpoints declaring explicit `security: []`, every error response the `{code, message, details?}` envelope, every operation with examples, all shared types via `$ref`.
- `api-sync-report.md` written alongside: field-origins table + the 4-point drift checklist, scenario recorded, every core finding ✓ or explicitly resolved, `unresolved_origins` empty (A) or listed (B).
- Every endpoint maps to a PRD §4 user story; every field traces to a `data-model.md` column (scenario A) or has an explicit inferred origin noted (scenario B); every error `code` exists in the repo's error definitions.
- `contracts/events.md` present iff the feature has async flows; each event has a payload schema, producer, consumers, retry / DLQ note.
- `contracts/cli.md` present iff the surface is `cli`; `contracts/public-api.md` present iff the surface is `library-sdk`.

## Conflicts — human in the loop

| Conflict | Skill action |
|---|---|
| Field in `data-model.md` with no story in PRD covering it | Add it to the schema with a `# unused-in-prd` note in the report; ask the user. |
| A §6 sequence references a flow that maps to no endpoint | Flag `# orphan-sequence` in the report; ask (forgotten endpoint? internal job?). |
| PRD §5 constraint contradicts a `data-model.md` constraint | Take the stricter value; flag both; the human resolves which artifact is wrong. |
| Existing `openapi.yaml` has a field absent from every source | Keep it with a `# manual-addition` note; flag in the report. |
| A field disappeared from `data-model.md` | Keep it in the YAML with a `# stale` note; surface it — the human removes from the contract or restores in the model. |

If ≥3 flags appear in one run, pause, list them, and ask whether to continue or fix the sources first.

## Anti-patterns

- **Contract written by hand**, then the model/sequences bent to fit it. The arrow is one-way: model + sequences + PRD → contract.
- **Skipping the drift check** because "it was just generated, of course it matches". Generation can match the PRD-as-read while diverging from the model or the sequences — different files, different authors. A clean 4/4 ✓ is cheap; a silent ✗ in prod is not.
- **Error responses from the PRD only.** PRD lists happy + a couple of errors; the §6 sequences hold the authorization and concurrent-state branches. Skipping them leaves blind spots.
- **Inventing a field** with no origin in any input, or **silently dropping** one that left `data-model.md` (keep it with a `# stale` note and surface it — the human decides).
- **Stack-specific schema or error names.** Schemas use the domain language from `data-model.md`; error codes are the neutral `module.error_name` convention — not a Go/TS/Python idiom and not tied to any driver's error type.
- **Free-text errors** (`{"error": "failed"}`), `?v=2` query versioning, `nullable: true` (3.0 style — use `type: [string, null]`), offset pagination, or real PII in examples.
- **Re-deriving the interface kind when `architecture-design` already declared it.** `target_surfaces` in `sad.md` is the primary signal — read it; the architecture-map derivation is the **fallback only** when the SAD/field is absent. Silently re-inferring HTTP-vs-events on every run is the double-derivation this skill's surface-awareness removes.
- **Hiding scenario B as if it were complete.** Scenario B is a valid state, not a half-baked one. `unresolved_origins` must be visible. Pretending the contract is fully typed when it isn't sets the team up for silent drift when the model arrives.

## Sources of best practices

- **Microsoft REST API Guidelines** — https://github.com/microsoft/api-guidelines. Error shape with machine-readable `code`, URL versioning, `BearerAuth` default.
- **Google AIP (API Improvement Proposals)** — https://google.aip.dev/. Resource-oriented paths, snake_case field names, domain-namespaced error codes.
- **Zalando RESTful API Guidelines** — https://opensource.zalando.com/restful-api-guidelines/. Cursor pagination via next-link, JSON-only responses, snake_case JSON.
- **OpenAPI 3.1 specification** — https://spec.openapis.org/oas/v3.1.0. Full JSON Schema 2020-12 compatibility.

## References & templates

- [`../_shared/surfaces.md`](../_shared/surfaces.md) — the declared `target_surfaces` (read from `sad.md`) pick the contract form; this skill reads, never re-derives.
- [`../_shared/size-matrix.md`](../_shared/size-matrix.md) — MVP (one resource, events only if async) vs Full surface depth.
- [`../_shared/handoff.md`](../_shared/handoff.md) — stage-handoff block format.
- [`./references/drift-check.md`](./references/drift-check.md) — the field-origins table + 4-point drift checklist, reconcile semantics, conflict table.
- [`./templates/openapi.yaml`](./templates/openapi.yaml) — OpenAPI 3.1 scaffold: `BearerAuth`, cursor page wrapper, `{code, message, details?}` Error schema.
- [`./templates/events.md`](./templates/events.md) — async event-contract scaffold (producer / consumers / payload / retry / DLQ).
- [`./templates/cli.md`](./templates/cli.md) — CLI surface contract scaffold (commands / flags / exit codes).
- [`./templates/public-api.md`](./templates/public-api.md) — library/SDK public-API contract scaffold (public signatures / types).
