---
name: generate-data-model
model: inherit
effort: medium
agents: [explorer]
description: >-
  Use to design the data model AND generate the actual forward + rollback
  migrations in one pass — shippable SQL, not a plan. Greenfield-first: reads
  PRD §4 (entity acceptance criteria) + sad.md §6.4 ER + the sequence diagrams,
  then writes docs/features/{slug}/data-model.md plus paired *.up.sql / *.down.sql
  migrations STAGED under docs/features/{slug}/migrations/ (NOT the live migrations/
  tree — implement-tasks promotes them when the feature is actually built) and an
  audit report. Brownfield delta via --mode brownfield; drift-only via --drift-only.
  Keeps the course's opinionated DB conventions (created_at-only audit, hard delete,
  no CHECK/TRIGGER/business-default, SQL-first, timestamp-named idempotent migrations,
  "DB as dumb storage"). Hard-refuse if PRD.md or sad.md is missing. Triggers on
  "data model for {slug}", "schema for {slug}", "generate migrations for {slug}",
  "DB design + migration", "/sdlc-generate-data-model {slug}", "модель даних для {slug}",
  "схема для {slug}", "згенеруй міграції".
  Triggers: /sdlc-generate-data-model {slug}. Output: docs/features/{slug}/data-model.md
  + staged docs/features/{slug}/migrations/.
triggers:
  - /sdlc-generate-data-model
  - "data model for"
  - "schema for"
  - "generate migrations for"
  - "DB design + migration"
  - "модель даних для"
  - "схема для"
  - "згенеруй міграції"
stage: "07"
---

# Skill: generate-data-model

End-to-end runner for the persistence cut: data model + migrations + drift check in one pass. Greenfield-first by default; brownfield delta as `--mode brownfield`. Output is **shippable** — full `.up.sql` + `.down.sql`, not a plan — but **staged under `docs/features/<slug>/migrations/`, never written into the live `migrations/` tree.** `implement-tasks` **promotes** the staged pair into the repo's live `migrations/` (with the real timestamp / sequence value the convention assigns at promote-time) only when the feature is actually being built. This is deliberate: `generate-data-model` is a design stage several steps before `implement-tasks`, so a stray `migrate up` (a teammate's loop, CI, a deploy) must not be able to apply a half-designed schema to a real database.

## Why this differs from a pure mirror

Unlike the rest of the SDLC toolkit (which mirrors the upstream pipeline's content under course names), `generate-data-model` is a **deliberate partial mirror**. It **keeps the course's opinionated DB defaults** — `created_at`-only audit columns, hard delete, no `CHECK` / `TRIGGER` / business `DEFAULT`, SQL-first migrations, timestamp-prefixed idempotent filenames, "DB as dumb storage" — and does **not** adopt the upstream stack-agnostic "detect-and-follow the repo's DB philosophy" stance. From the upstream pipeline it borrows only **three** mechanisms: (1) **staged migrations** written to the feature folder and promoted later by `implement-tasks`; (2) a **drift-check** that keeps the data model in sync with PRD + SAD; (3) **reading `docs/architecture-map.md`** as the convention source for where persistence + migrations live. (This divergence is also recorded in the toolkit README / CHANGELOG.)

## Owner

Backend Lead.

## When to use

- "data model for <slug>", "schema for <slug>", "generate migrations for <slug>".
- After PRD + sad.md §6.4 (ER stub) + at least the critical sequences exist. Run after `complete-sequence-diagrams` so the skill knows every table the runtime needs.
- `/sdlc-generate-data-model <slug>` — explicit invocation.
- `/sdlc-generate-data-model <slug> --mode brownfield` — analyze existing `migrations/` and propose a delta.
- `/sdlc-generate-data-model <slug> --drift-only` — just compare the domain layer against the current schema; no generation.
- Skip if `data-model.md` exists AND every entity in it has a corresponding pair of staged migration files.

## Inputs

- `<slug>` — same as for PRD / SAD.
- **Gate (hard refuse if missing):**
  - `docs/features/<slug>/PRD.md` — entities live in §4 user-story acceptance criteria.
  - `docs/features/<slug>/sad.md` — §6.4 ER section provides the initial relationships.
  - If either is missing: STOP, suggest `sdlc:write-prd <slug>` or `sdlc:architecture-design <slug>`.
- Optional: the sequence diagrams in `sad.md §6` — each `writes/reads <entity>` note is an index candidate (one index per query, justified).
- Optional: the domain layer (`internal/modules/<...>/domain/*` or stack-equivalent) — drift detection only.
- **Convention source (borrowed mechanism):** `docs/architecture-map.md` (from `sdlc:map-architecture`) — read its §Migrations / persistence section to learn **where** the live `migrations/` tree lives and **which migration tool** the repo uses, instead of re-scanning from scratch. The map gives module layout + migration location; the course's DB defaults below are NOT overridden by it. For **drift detection** specifically, `explorer` still reads the **actual domain layer** (the map gives layout; drift needs the real struct/field source). Re-scan only if the map is absent or stale.

## Defaults (the opinionated, course-owned set — preserved, NOT detected)

These defaults are baked into the skill and into the baseline `.claude/rules/migrations.md` the skill writes on first run. They are **course-opinionated and intentional** — the skill does NOT defer to a repo's differing DB philosophy. It flags any divergence from the repo's existing convention in the report so the team can decide, but the defaults below are the house style this skill applies.

| Topic | Default | Why |
|---|---|---|
| Migration filename | `YYYYMMDDhhmmss_<verb>_<entity>.up.sql` (timestamp-prefixed) | Two parallel feature branches won't collide on `000034_`. |
| Idempotency in DDL | `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, `ON CONFLICT DO NOTHING` for seeds | Re-running a partially-applied migration does not error. |
| Audit columns | `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` only — **no `updated_at`** | Immutable-first: `updated_at` is opt-in per entity, only when the entity is genuinely mutable AND the PRD requires it. Otherwise changes go through an audit table or event log. |
| Delete strategy | Hard delete (+ audit table if business requires history) | No `deleted_at`, no status-column for delete. DB stays simple; history is a separate concern. |
| PK | UUID v7, generated app-side | Cursor pagination, no insert-sequence contention. |
| Naming | `plural snake_case` (`users`, `goal_progress`) | Postgres community standard. |
| Indexes | One per real query (from the sequences). Existing-table → `CREATE INDEX CONCURRENTLY` always. | Each index has a write cost; `CONCURRENTLY` avoids long write locks. |
| Migration authoring | **SQL-first** — raw `.up.sql` / `.down.sql`, no ORM / no migration DSL | The migration is the contract; it reads as plain SQL. |
| Breaking changes | Auto-decompose to 3-step expand → backfill → contract | Zero-downtime by default. |
| New NOT NULL on existing table | Auto-decompose: add nullable → backfill → set NOT NULL | Default zero-downtime path. |
| String columns | `VARCHAR(N)` bounded; `TEXT` only for URLs / long descriptions | Schema-as-documentation; bounds drive validation. |
| JSONB | Only for semantically opaque payload (settings, metadata, polymorphic `block.payload`) | Structured fields → first-class columns. |
| Forbidden | `CHECK`, `TRIGGER`, `DEFAULT '<business value>'`, sequence-as-PK | "DB as dumb storage" — business logic lives in code, only UNIQUE / NOT NULL / FK / indexes / `DEFAULT now()` for timestamps. |
| Multi-DB (replica, sharding) | Out of scope | Single-DB only. |
| Partitioning, materialized views | Out of scope | Perf optimization, not contract. |

## Protocol

1. **Prereq check (hard).** `test -f docs/features/<slug>/PRD.md && test -f docs/features/<slug>/sad.md` → exit ≠ 0 = refuse with a pointer to which prereq is missing.

2. **Rules bootstrap.** If `.claude/rules/migrations.md` is absent in the repo root, copy [`./templates/rules-migrations-baseline.md`](./templates/rules-migrations-baseline.md) → `.claude/rules/migrations.md` and tell the user «I wrote a baseline rules file; edit it if your team disagrees with any default.» Reporting this bootstrap is mandatory.

3. **Read the architecture map for migration location (borrowed mechanism — read-only).** Read `docs/architecture-map.md` (from `sdlc:map-architecture`) **first** — its §Migrations / persistence section tells you **where the live `migrations/` tree lives** and **which migration tool** the repo uses (e.g. golang-migrate's transaction-per-file wrapper). This is a **promote-time hint** for `implement-tasks`, not a license to write into the live tree here. The map also gives module layout, saving a re-scan. **The course DB defaults above are NOT overridden by the map** — if the repo's existing convention differs (e.g. it uses sequential filenames or `updated_at`), apply the course defaults and **flag the divergence in the audit report** so the team can decide. Re-scan with `explorer` only if the map is absent or stale.

4. **Read prereqs in this order:**
   a. PRD §4 — extract entity candidates from acceptance criteria.
   b. sad.md §6.4 — the initial ER stub (often `<!-- TBD: relationships -->`).
   c. `sad.md §6` sequences — each `Note over API, DB: writes <table.column>` becomes a query requirement → an index candidate.
   d. (Optional) the domain layer (`internal/modules/<...>/domain/*` or stack-equivalent) — if present, build a struct-vs-DDL map for drift detection (the `explorer` agent reads the real source).
   e. (Brownfield only) the live `migrations/*.up.sql` — parse the current schema **offline** (no live DB connection).

5. **Aggregate roots.** Ask the user (or infer from PRD acceptance criteria): which aggregate roots own what? Lessons aggregate ContentBlocks; Tenant aggregates QuotaConfig. Without explicit aggregates the FK graph turns into a hairball.

6. **PK strategy.** UUID v7 app-side by default (course default). Confirm with the user only if a PRD acceptance criterion demands a different PK (e.g. a lookup slug as PK).

7. **Columns + constraints** per entity, applying the course defaults:
   - `VARCHAR(N)` for bounded strings (choose N from PRD validation, e.g. `title: maxLength: 200` → `VARCHAR(200)`); `TEXT` only for long descriptions / URLs.
   - `JSONB` only for opaque payloads (one-line justification in the `Notes` column).
   - `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`. **No `updated_at`** unless the entity is genuinely mutable AND the PRD requires it (surface this explicitly — never add `updated_at` silently).
   - **No `CHECK`, no `TRIGGER`, no business `DEFAULT`** — UNIQUE / NOT NULL / FK / `DEFAULT now()` only.
   - `<!-- TBD -->` where honestly undecided.

8. **Indexes per query.** Each sequence note `writes/reads <table.column>` becomes one index candidate; discard candidates with no concrete query; print a "Query it serves" justification column. No "just in case" indexes.

9. **Write `docs/features/<slug>/data-model.md`** from [`./templates/data-model.md`](./templates/data-model.md):
   - ER Mermaid diagram (manual layout — a clean ordered block, not auto-generated).
   - One entity table per aggregate.
   - Indexes table with `Query it serves` filled.
   **Validate the `erDiagram` per [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md)** (render-parse with `mmdc` if available, else the structural lint — valid cardinality glyphs + `type name` attribute lines; fix before continuing — never commit a broken diagram).

10. **Generate migration files — STAGED in the feature folder, never the live tree (borrowed mechanism).** Write the pairs into **`docs/features/<slug>/migrations/`** with a **feature-local timestamp-prefixed** name (`<YYYYMMDDhhmmss>_create_<entity>.up.sql` + matching `.down.sql`) that preserves intra-feature order. The SQL is full and shippable and follows every course default (SQL-first, idempotent, `created_at`-only, hard delete, no `CHECK`/`TRIGGER`); only the **location** differs from a live migration. **Never write into the repo's live `migrations/` tree here.** `implement-tasks` **promotes** these staged pairs into the live `migrations/` (re-stamping the timestamp at promote-time so the live sequence stays correct, in feature-local order) when it runs the migration task. The SQL content rules are unchanged:
    - **Greenfield (default):** one create-`<entity>` `.up.sql` + `.down.sql` per entity (or per small aggregate). `CREATE TABLE IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS` everywhere; `ON CONFLICT DO NOTHING` on seeds.
    - **Brownfield (`--mode brownfield`):** diff vs the parsed existing schema; produce ALTERs only.
    - **Existing-table `CREATE INDEX`:** use `CONCURRENTLY` AND warn that the file must contain only that one statement if your migration tool wraps each file in a transaction (e.g. golang-migrate).
    - **New NOT NULL on existing table / rename / drop:** emit the 3-step expand → backfill → contract sequence (separate timestamp-named files); the user reviews the backfill SQL.

11. **Seeds (3 buckets).**
    - **Bootstrap** (admin user, default org) → first migration `<timestamp>_bootstrap_<thing>.up.sql`, deterministic hardcoded UUID v7 (e.g. `00000000-0000-7000-8000-000000000001`).
    - **Lookup data** (statuses, currencies, rating scales) → separate migration `<timestamp>_seed_<table>.up.sql` with `INSERT ... ON CONFLICT DO NOTHING` (idempotent — re-runs are safe).
    - **Test fixtures** → **NOT** in `migrations/`. Generate them in the form the repo uses (factory functions in `internal/testfixtures/<entity>` or stack-equivalent), documented under "Test fixtures" in `data-model.md`.
    - **PII guard (hard):** no real-looking email / name / phone in any seed — use `admin@example.test`, `user-<uuid>@example.test`, `Test User`.

12. **Drift detection (always; `--drift-only` short-circuits to here) — borrowed mechanism, keeping the model in sync with PRD + SAD.** Two checks:
    - **Schema-vs-source drift:** if the domain layer exists, map each field to a column and report `field-without-column` / `column-without-field` / `type-mismatch` / `nullability-mismatch`; **auto-propose fix migrations** under `docs/features/<slug>/migrations/_drift/` (staged, for the user to review — same staging discipline as the main migrations).
    - **Model-vs-spec drift:** cross-check `data-model.md` against PRD §4 entity acceptance criteria + `sad.md` §6.4 ER — flag any entity/relationship in the PRD/SAD with no table, and any table with no PRD/SAD origin. Record both in the audit report.

13. **Breaking changes — 3-step decomposition.** If a rename / drop / re-type is described:
    - Phase 1: add the new column nullable + dual-write from **app code** (not a DB trigger — DB stays dumb).
    - Phase 2: batched backfill script (ETA + resumability — write a one-page `backfill-<column>.md` companion).
    - Phase 3: drop the old column. Each phase = separate staged migration file = separate PR = separate deploy.

14. **Self-check (4 mandatory, course-owned).** For every staged file:
    - **Naming.** `plural snake_case` tables, `<timestamp>_<verb>_<entity>` filenames.
    - **down.sql reversibility.** Every CREATE has a matching DROP; every ADD COLUMN a DROP COLUMN; every CREATE INDEX a DROP INDEX.
    - **FK indexes.** Every `REFERENCES other_table(id)` has a `CREATE INDEX` on the FK column.
    - **Forbidden features.** Grep for `CHECK (`, `CREATE TRIGGER`, `DEFAULT '` followed by a non-`now()` business literal. Fail with line numbers.
    Any failure → fix or surface to the user (no silent commit).

15. **Audit report** `docs/features/<slug>/_audit/data-model-<date>.md`:
    - **Generated files:** the **staged** migration paths (their `docs/features/<slug>/migrations/<timestamp>_*` paths) + `data-model.md`. State plainly: «migrations are **staged** — not yet in the live `migrations/` tree; `implement-tasks` promotes them (re-stamping the timestamp at promote-time)».
    - **Convention divergences:** where the course defaults differ from the repo's existing convention (e.g. «your repo uses sequential `000003_*` naming; I wrote timestamps per the course default — see the Defaults table» or «repo has `updated_at` elsewhere; this feature is immutable so I omitted it»).
    - **Drift findings:** schema-vs-source (with `_drift/*.sql` proposals) + model-vs-spec.
    - **Breaking changes decomposed:** any 3-step sequence generated.
    - **TBDs:** every `<!-- TBD -->` in `data-model.md` with file:line.

16. **Propose commit + handoff.** Commit `feat(<slug>): data-model.md + staged migrations`. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* (the design doc + the staged migration pairs, plus the staged-not-live note) + *Review* (`docs/features/<slug>/data-model.md`, staged `docs/features/<slug>/migrations/`) + *Run next* (`/clear`, then `/sdlc-api-forge <slug>`).

## Questions for discussion

- Aggregate roots — what owns what?
- Where does the user explicitly want `updated_at` (overriding the immutable-first default)? Surfacing this is mandatory; the skill never adds `updated_at` silently.
- Soft delete or hard delete + audit? Hard delete is the default; the skill needs an explicit override.
- Indexes — any "just in case" the user wants despite no concrete query?
- JSONB usage — confirm each candidate column.
- For breaking changes — does the user accept 3-step decomposition, or is there a maintenance window?

## Definition of Done

- `data-model.md` exists with ER + every entity + every index carrying a query justification; the `erDiagram` parses.
- For every entity/change, a matched `.up.sql` + `.down.sql` pair exists **under `docs/features/<slug>/migrations/`** (staged, timestamp-prefixed names) — **nothing was written into the live `migrations/` tree** (that's `implement-tasks`'s promotion step). The SQL follows the course defaults (SQL-first, idempotent, `created_at`-only, hard delete, no `CHECK`/`TRIGGER`/business-`DEFAULT`).
- All 4 self-checks pass (naming, down reversibility, FK indexes, forbidden features).
- Audit report written (with the staged paths + the promote-time note); drift report (schema-vs-source under `_drift/*.sql`, plus model-vs-spec) if drift was detected.

## Anti-patterns

- **Writing the migration into the live `migrations/` tree at design time.** That drops a half-designed, runnable schema where a stray `migrate up` (CI, a teammate's loop, a deploy) can apply it before the feature is built or reviewed — and grabs a sequence slot early. Stage under `docs/features/<slug>/migrations/`; `implement-tasks` promotes it (re-stamped) when the code that needs it is actually being written.
- **Business defaults in DB** (`DEFAULT 'pending'`). Only `DEFAULT now()` for timestamps; the rest in app code.
- **CHECK constraints on business invariants / triggers / stored procedures.** Business logic lives in code; DB stays dumb.
- **Index "just in case" without a concrete query.** Each index costs write performance.
- **TEXT for everything.** Bounded strings → `VARCHAR(N)`.
- **PK from a DB sequence.** Default UUID v7 from app — no blocking on insert sequence.
- **Adding `updated_at` silently.** Immutable-first; `updated_at` is opt-in per entity, surfaced and justified.
- **One mega-migration with 5 ALTERs.** Rollback becomes all-or-nothing. Split.
- **DROP COLUMN before deploying new code.** Breaks running pods between phases. Always 3-step.
- **Real-looking PII in seeds** (Gmail / .ua emails). Use `example.test`.
- **Sequential migration filenames.** Two parallel feature branches collide on `000034_`. Use timestamps.
- **Switching to an ORM / migration DSL.** SQL-first — the `.up.sql` / `.down.sql` is the contract.
- **Live DB introspection without an offline parse fallback.** CI has no DB credentials; parse the SQL files.
- **Bootstrapping `rules/migrations.md` and forgetting to tell the user.** Report it when it happens.

## Templates

→ [`./templates/data-model.md`](./templates/data-model.md) — output structure for the design doc.
→ [`./templates/rules-migrations-baseline.md`](./templates/rules-migrations-baseline.md) — baseline `.claude/rules/migrations.md` copied at step 2 when missing.
→ [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md) — validate the `erDiagram` after writing it.
→ [`../_shared/handoff.md`](../_shared/handoff.md) — the stage-handoff block emitted at the end (step 16).

## Example invocation

> **User:** "data model for course-lesson-mvp"
>
> **Skill behavior:**
> 1. `test -f docs/features/course-lesson-mvp/PRD.md && test -f docs/features/course-lesson-mvp/sad.md` → OK.
> 2. `.claude/rules/migrations.md` missing → bootstrapped from baseline. Reported to user.
> 3. Reads `docs/architecture-map.md` §Migrations → live tree is `beer-lms-api/migrations/`, tool is golang-migrate (transaction-per-file). Records this as a promote-time hint; does NOT write there.
> 4. Reads PRD §4 (entities: Lesson, ContentBlock, MediaBlob, AuditEvent), sad.md §6.4 (ER stub: Lesson ||--o{ ContentBlock), §6 sequences (5 flows — index on `lessons.course_id` for listLessons; on `content_blocks.lesson_id` for getLesson with blocks).
> 5. Aggregate roots: Lesson aggregates ContentBlock; MediaBlob is referenced (signed URL in `block.payload`).
> 6. PK: UUID v7 app-side.
> 7. Types: `title VARCHAR(200)` (from PRD AC `maxLength: 200`), `slug VARCHAR(120) UNIQUE(course_id, slug)`, `status VARCHAR(32)` (enum-in-app), `block.payload JSONB` (polymorphic — ADR-0001), `published_at TIMESTAMPTZ NULL`, all `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`. No `updated_at`. No `CHECK`/`TRIGGER`.
> 8. Indexes: `idx_lessons_course_id` (listLessons), `idx_blocks_lesson_id` (getLesson), `idx_lessons_published_per_course WHERE status='published'` (partial — listPublishedLessons from US-4).
> 9. Writes `docs/features/course-lesson-mvp/data-model.md` (ER + 3 entity tables + indexes table). `erDiagram` validated per mermaid-check.
> 10. Writes 4 staged migration pairs under `docs/features/course-lesson-mvp/migrations/`: `20260523120000_create_lessons.up.sql`/`.down.sql`, `20260523120001_create_content_blocks.{up,down}.sql`, `20260523120002_create_media_blobs.{up,down}.sql`, `20260523120003_create_audit_events.{up,down}.sql`. All idempotent. **Nothing written into `beer-lms-api/migrations/`** — `implement-tasks` promotes these later.
> 11. Seeds: none required. Test fixtures: writes `beer-lms-api/internal/testfixtures/lesson.go` with `NewLesson`, `NewContentBlock` factories. PII guard satisfied.
> 12. Drift: domain structs not yet written → schema-vs-source skipped; model-vs-spec → all 4 PRD entities have a table, no orphan tables.
> 13. No breaking changes (greenfield).
> 14. Self-check: 4/4 pass — naming OK, every `.down` reverses its `.up`, FK indexes present (`idx_blocks_lesson_id`), no forbidden features.
> 15. Audit report `_audit/data-model-2026-05-23.md`: lists the **staged** migration paths; notes «staged, not live — `implement-tasks` promotes»; flags «timestamp naming differs from the repo's existing sequential `000003_seed_admin.up.sql` — course default, see Defaults table»; no drift; 1 TBD (`block.payload` marked `<!-- TBD: lock with ADR-0001 -->`).
> 16. Commit `feat(course-lesson-mvp): data-model.md + staged migrations`; emits the stage-handoff block → next `/sdlc-api-forge course-lesson-mvp`.
