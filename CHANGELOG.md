# Changelog

All notable changes to the `sdlc/` toolkit and `sdlc` Claude Code plugin.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [4.5.1] — 2026-08-19

### Changed — scaffold: єдина env-пара `api/.env.example` → `api/.env`

- base-tpl (a0ce095) схлопнув дві env-пари в одну: docker-специфіка (POSTGRES_*, PGDATA-пін,
  DATABASE_URL з хостом `postgres`) переїхала інлайном у `docker-compose.yml`, а `api/.env`
  тепер читають і локальний `make -C api run`, і compose (`env_file` + `environment`-override).
- Що зробити після оновлення: у своїх проєктах-нащадках нічого — конвенція набирає чинності
  для нових скафолдів; згадки `api/.env.docker` у скілі виправлені на `api/.env`.

## [4.2.0] — 2026-06-01

### Added — `verify-ui` skill (the live browser feedback channel)

- New cross-cutting utility skill `verify-ui` (`/sdlc-verify-ui {slug-or-story}`): verifies a UI
  surface's acceptance criteria through a **live browser run** — opens the running app, drives the
  Given/When/Then scenario, reads the **real page state** (DOM via `snapshot`, computed styles via
  `eval`, persistence via `localstorage-get`, survives `reload`), and returns a per-AC pass/fail
  with a screenshot artefact. Catches what compiles and "passes the logic" but is visually or
  behaviourally broken — the class of bug deterministic gates can't see.
- **CLI-first.** Drives `playwright-cli` in bash (token-efficient, the vendor-recommended default
  for coding-agent loops/CI). Playwright MCP stays available for live stateful debugging only.
  Install: `npm install -g @playwright/cli@latest` → `npx playwright install chromium` →
  `playwright-cli install --skills`.
- **Surface-gated** to UI `target_surfaces` (reads `sad.md`); for backend-only features the
  browser channel gives no signal and the skill says so. Verdict is **evidence-before-assertion**:
  every FAIL carries expected vs actual read from the live page, never "looks right".
- Design→code input via **Figma Dev Mode MCP** named as the *input* channel (read the design's
  structure, not a flat picture) — it complements, never replaces, result-verification in the browser.
- Plugin skill count 17 → 18 (5 cross-cutting utilities). Backs Lecture 7.6 screencast #2
  ("розробка через Playwright"); the synthetic demo carries a self-contained `verify-ui` mirror.

## [Unreleased]

### Added — `scaffold` skill + greenfield `interview` (v4.5.0, 2026-08-19)

**What you get.** A complete new-project flow that starts in an empty folder:
`mkdir my-app` → `/sdlc-interview` (greenfield mode writes a project-level
`docs/idea-brief.md`) → `/sdlc-scaffold` (materializes the project from the public
[base-tpl](https://github.com/genkovich/base-tpl) template) → `/init`.

- **New skill `scaffold`** (`/sdlc-scaffold`): asks stack questions (backend language /
  architecture / frontend / auth) and battery questions (deploy, CI, Prometheus+Grafana
  monitoring, freshness pin bump), then runs base-tpl's tested `scaffold.sh`. Batteries are
  **subtractive**: an unselected battery is physically absent from the result (folders, compose
  services, CI jobs, README lines). "Yes to everything" reproduces the template byte-for-byte.
  Unfilled paths (PHP/Python/TS backends, microservices, flat React, non-Google auth) refuse
  honestly instead of generating stubs. Freshness bumps infrastructure pins via context7
  (WebSearch/registry fallback) behind a `make check` gate with automatic rollback.
- **`interview` greenfield mode**: in an empty folder (no `.git`, no `docs/`) the skill now
  writes a **project-level** `docs/idea-brief.md` (same 15-section template; slug = product
  name) and hands off to `/sdlc-scaffold` instead of `write-prd`. Feature mode in an existing
  repo is unchanged.
- **`interview` depth regulator**: first checkpoint now asks easy / medium / hard.
  `easy` = 3-4 checkpoints (idea, one Socratic batch, one combined RICE+recommendation
  confirm) with no sub-agent fan-out — for quick passes; `medium` = the existing 14-phase
  protocol (default); `hard` = medium plus an extra Socratic batch and a wider competitive
  table. Recorded in the brief frontmatter as `depth:`.
- **Distribution**: the repo now carries `.claude-plugin/marketplace.json`, so the plugin
  installs user-scoped from the marketplace and the skills are visible in any folder —
  including the empty folder a greenfield project starts in.

**Migration.** No breaking changes. Existing feature-mode `interview` runs behave exactly as
before (the depth question defaults to medium = the previous protocol). The idea-brief template
gained one frontmatter line (`depth:`); existing briefs stay valid.


### Added — `user-documentation` skill (2026-07-30)

- New cross-cutting utility `/sdlc-user-documentation <target-dir>` generates **end-user
  documentation from a live web application**: flow inventory (repo scan + live nav snapshot,
  user-confirmed and frozen) → per-flow browser walks with a JSONL action journal and state
  screenshots → one clean-context `sdlc:doc-flow` agent per flow writes the doc **strictly from
  the journal** → a thin linked `<Product> - User Guide.md` index. Style codified from the
  Beer-LMS reference corpus (Flow-docs, exact-780px full views or element crops, `> **Note:**`
  callouts, applicable-only tail tables).
- **Deterministic by construction**: flows classified `mutates: true/false` at inventory —
  read-only flows fan out in parallel, mutating flows run strictly sequentially (concurrent
  mutators corrupt each other's screenshots); all created data carries a `Docgen:` prefix;
  state-reference docs may only document OBSERVED states (create-through-UI or honest FAIL).
- **Optional screencasts** (`--video`): `replay-screencast.sh` re-executes the journal through
  `playwright-cli run-code` (closed action dictionary == replay contract, Playwright auto-wait
  for free) into a chaptered `.webm`.
- **Mechanical gate** `validate-docs.py` (zero-dep, PNG width via IHDR): H1/frontmatter/`---`
  frame, gapless Step/State numbering, embeds resolve + no orphan PNGs, width ≤ 780, one embed
  syntax per target (vault wikilinks vs repo markdown, auto-detected via `.obsidian/` walk-up),
  index links every flow. Calibrated green on the reference corpus.
- New agent `sdlc:doc-flow` (sonnet, cyan) — walks ONE flow and writes ONE doc, sentinel
  `DOCFLOW_OK`/`DOCFLOW_FAIL` contract, ephemeral-state (toast) inversion rule, OAuth
  special-case for `doc_type: auth`.
- Live eval on beer-lms: 3/3 flows OK with zero retries (task-flow 11 steps vs reference 11,
  auth special-case, state-reference with UI-seeded states), validator 0 errors / 0 warnings,
  40s+ replayed screencast with 0 failed steps, both vault-wikilink and repo-markdown targets.
- Plugin skill count 19 → 20 (7 cross-cutting utilities). Agents 10 → 11 (`sdlc:doc-flow`).

### Added — `prepare-design-spec` skill (2026-07-15)

- New design-entry utility `/sdlc-prepare-design-spec <slug>` closes the gap between product
  discovery and Figma/Pencil authoring. It inspects the real repository, separates Confirmed,
  Observed, and Proposed statements, and writes one `docs/features/<slug>/design-spec.md` that
  contains the specification and an embedded, traced Definition of Done.
- Added self-contained specification and DoD templates with requirement-to-evidence traceability. The
  workflow ends in deterministic repository gates plus live `verify-ui` evidence; an agent success
  report or screenshot alone cannot satisfy completion.
- Plugin skill count 18 → 19 (6 cross-cutting utilities).

### Changed (template ownership refactor, 2026-05-25)

- Single-owner artefact templates relocated from `sdlc/document-templates/` into the `templates/` subfolder of their owner skill: `interview/`, `fix-term/`, `write-prd/`, `architecture-design/` (gains `c4-context.md`, `c4-container.md`, `deployment.md` alongside existing `sad-template.md`, `adr-template.md`), `complete-sequence-diagrams/`, `generate-data-model/`, `api-forge/`, `plan-tests/`. Skill folders are now self-contained — copying a skill brings its template along.
- `write-prd/PRD-template.md` moved into `write-prd/templates/PRD-template.md` for consistency (all skills now keep templates in a `templates/` subfolder).
- `decide-adr` SKILL drops the legacy fallback to `document-templates/adr/NNNN-title.md`; the canonical ADR shape stays at `architecture-design/templates/adr-template.md`, referenced cross-skill.
- All 9 affected SKILL.md files updated to read templates from `./templates/X.md` instead of `../../../document-templates/X.md`.
- `document-templates/` keeps only cross-feature / manual / legacy snippets (`CHANGELOG.md`, `CONTEXT-MAP.md`, `claude-context.md`, `review-checklist.md`, `rollback-plan.md`, `migration-plan.md`, `task-breakdown.md`, `SPEC.md`, `arc42.md`, `architecture-brief.md`, `adr/NNNN-title.md`, `diagrams/c4-component.md`). Skills do not copy from this folder during their protocol — these are snippets pulled by hand when needed.
- Empty `document-templates/api/` directory removed.
- Docs rewritten: `plugin/README.md` (skill-anatomy + key-files-per-skill table + dedicated section on what stays in `document-templates/`); point-edits in `sdlc/README.md`, `sdlc/CLAUDE.md`, `sdlc/00-overview/file-structure.md` to reflect the new layout.

### Removed (M1-M6 cleanup, 2026-05-25)

Aggressive trim — toolkit now serves the Claude Course Modules 1-6 lecture set. Skills/templates/examples not referenced by any lecture deleted. Snapshot tag: `pre-m6-cleanup-2026-05-25` (rollback point).

**Skills (24 → 11):**
- Removed 7 atomic skills with zero lecture refs: `impl-prep`, `prep-context`, `prep-review`, `ship`, `sync-kb`, `write-changelog`, `help`.
- Removed 4 deprecated stubs: `define-api` (renamed to `api-forge` in v3.3.0), `design-db` (merged into `generate-data-model`), `plan-migration` (merged into `generate-data-model`), `draw-sequence` (superseded by `complete-sequence-diagrams`; single-flow case via `--flow`).
- Removed 2 composite wrappers: `design` (03-06), `detail` (07-09). Atomic invocation is now the only entry-point — wrappers added orchestration overhead that no lecture relied on.
- Kept (after Phase C validation): `break-tasks` — Lecture 6.7 LMS lesson actively invokes `/sdlc-break-tasks`.

**Templates (3 removed):**
- `kb-note.md` (sync-kb related, no longer needed)
- `feature-rollout-plan.md` (no lecture references)
- `security-review.md` (no lecture references)

**Examples (34 → 33+1):**
- Kept `examples/rate-limiting/` (Lecture 6.1 and 6.2 Sources.md reference it as the end-to-end filled brief sample).
- Kept `examples/goals-tracking/arc42.md` (referenced in Lecture 6.4 as filled-in Arc42 sample).
- Removed rest of `examples/goals-tracking/` (idea-brief.md, SPEC.md, data-model.md, migration-plan.md, rollback-plan.md, task-breakdown.md, implementation-pack.md, README.md, adr/, api/, diagrams/, all .sql).

**Backups (.bak files):**
- Removed 12 `*.bak-2026-05-23-pre-simplify` files left over from architecture-design simplification — pre-simplify content recoverable from git history.

**Docs synced to reflect post-cleanup state:**
- `plugin.json` description trimmed to the 11 remaining skills.
- `README.md` stage table replaced with 9-stage pipeline; both `rate-limiting` and `goals-tracking/arc42.md` examples linked.
- `plugin/README.md` quickstart rewritten without composite wrappers; atomic skill table updated.
- `CLAUDE.md` GATE table updated (`write-prd`/`architecture-design`/`decide-adr`); composite-wrapper section removed; cross-cutting list trimmed.
- `00-overview/file-structure.md` removed deleted template entries.

### Removed (earlier)

- **Stage 12 (`implementation-pack`) dropped 2026-05-25** — the impl-pack aggregator (former hard pipeline gate) is gone. Downstream stages (`break-tasks`, `prep-context`, `prep-review`, `ship`, `write-changelog`) read PRD / SAD / data-model / openapi / sequences / ADR DIRECTLY (now those downstream skills are also removed in the M1-M6 cleanup above).
- Removed `plugin/skills/pack-impl/` (skill + tests).
- Removed `plugin/tests/fixtures/pack-impl/` fixtures.
- Removed `document-templates/implementation-pack.md`.
- `scripts/sdlc_lint.py` no longer requires `implementation-pack.md`.

### Added
- `complete-sequence-diagrams` skill — auditor + completer for SAD §6: reads PRD §4, cross-checks SAD §6 by US-N heading match, iteratively (per UC, user-confirmed) generates Mermaid `sequenceDiagram` blocks for missing UCs, validates with `mmdc --parse-only`, flags new actors and ADR-potential decisions, adds async patterns (idempotency, retry, DLQ) to non-`localhost` flows. Supports `--flow <name>` for single-flow ad-hoc mode (replacement for `draw-sequence`).
- `generate-data-model` skill — end-to-end persistence runner: reads PRD + SAD §6.4 + sequences (+ optional Go domain structs), produces `delivery/<slug>/data-model.md` AND live `.up.sql` + `.down.sql` pairs AND an audit report in one invocation. Opinionated defaults: timestamp filenames, `IF NOT EXISTS` everywhere, only `created_at` (no `updated_at`, immutable-first), hard delete + audit table, `CREATE INDEX CONCURRENTLY` for existing tables, auto 3-step expand→backfill→contract for breaking changes. PII guard in seeds. Includes inline drift detection (`--drift-only`) against domain structs.
- `sdlc/document-templates/rules-migrations-baseline.md` — baseline `.claude/rules/migrations.md` that `generate-data-model` writes on first run if the repo has none.

### Deprecated
- `draw-sequence` — superseded by `complete-sequence-diagrams` (single-flow case covered via `--flow <name>`).
- `design-db` — superseded by `generate-data-model` (data-model.md is one of its outputs).
- `plan-migration` — superseded by `generate-data-model` (produces actual SQL files instead of just a plan; migration-plan content folded into the audit report).

Deprecated skills kept for backward compatibility; will be removed in a future cleanup.

### BREAKING
- Removed `intake` skill — `/sdlc-interview` is now the single entry-point for ideation phase
- Removed `brainstorm` skill — its responsibilities (strategic approaches, multi-perspective, devil's advocate) merged into expanded `interview` skill
- Removed `brainstorm.md` and `initiatives.md` templates — consolidated into expanded `idea-brief.md` (15 sections)
- `propose-adr` moved from gate 1 to gate 3 (prereq: architecture-brief.md §Trade-offs)
- `interview` rewritten as 14-phase autonomous protocol with Claude-driven RICE/Feasibility (was user-input only)

## [4.0.0] — 2026-05-30

Full-cycle upgrade. The toolkit now covers the complete `map-architecture → ship` pipeline (was `interview → break-tasks`). Mirrors the upstream [sdd](https://github.com/genkovich/sdd) pipeline under course-specific skill names.

### Added

**New backbone skills (close the cycle):**
- `map-architecture` — scans the codebase once, writes `docs/architecture-map.md` (repo-root, persisted). Every later stage reads it instead of re-scanning. Carries a §Frontend/UI foundation section so design work reuses the existing design system. On a greenfield repo, also scaffolds `tasks.json`.
- `clarify-prd` — ambiguity sweep over an existing `PRD.md`: surfaces contradictions, missing acceptance criteria, and scope gaps; tightens the PRD in place before design work begins.
- `roadmap` — `/sdlc-roadmap` utility that maintains `docs/roadmap.md` (Now / Next / Later / Shipped tables); `ship-feature` moves features to Shipped automatically.
- `implement-tasks` — TDD engine: SELECT → RED → GREEN → REFACTOR → GATE → COMMIT. Three modes: **sequential** (default), **agent-team** (via `TeamCreate`), **dynamic Workflow**. Stack-agnostic command detection; promotes staged migrations from `docs/features/<slug>/migrations/` into the repo's live migrations tree (re-stamping timestamps). Adds `SDLC-Task` / `SDLC-AC` trailers to every commit. Per-project overrides in `.claude/sdlc.local.md` (auto-created, gitignored).
- `review-feature` — clean-context `sdlc:reviewer`; stage-1 traces every AC end-to-end (PRD → sequences → data-model → api → tasks → code, gated on `target_surfaces`), stage-2 covers quality and non-functional concerns. Loops back to `implement-tasks` on CHANGES REQUESTED (no `/clear`). Emits `_review/review-<date>.md` (PASS / CHANGES REQUESTED).
- `ship-feature` — run-the-feature check, changelog entry, PR body (AC + ADR links + `SDLC-Task` history), forge detection (gh / glab), moves feature to `docs/roadmap.md §Shipped`, terminal handoff block.

**New mechanisms:**
- `target_surfaces` — declared in `sad.md` frontmatter by `architecture-design`; downstream skills (`complete-sequence-diagrams`, `api-forge`, `break-tasks`, `plan-tests`, `review-feature`) gate on it instead of re-deriving the surface taxonomy each time.
- `tasks.json` — machine-readable task DAG (`id`, `title`, `layer`, `deps`, `acs`, `dod`, `files_hint`) at `docs/features/<slug>/tasks/tasks.json`; emitted by `break-tasks`, consumed by `implement-tasks`. This artefact closes the previously broken design-to-implementation cycle.
- Staged migrations — `generate-data-model` now writes migration files to `docs/features/<slug>/migrations/`; `implement-tasks` promotes them into the live migrations tree.
- Depth-dial (`_shared/interview-depth.md`) — per-stage effort control across the backbone.
- Copy-ready stage-handoff blocks (`_shared/handoff.md`) — every skill ends with a formatted block the user can paste to start the next stage.
- Mermaid-check validation (`_shared/mermaid-check.md`) — called by architecture-design and complete-sequence-diagrams before any diagram is committed.

**9 plugin-namespaced agents** (dispatched as `sdlc:<name>`): `explorer` (haiku, codebase scan), `researcher` (sonnet), `strategist` (opus), `analyst` (opus), `devils-advocate` (opus), `critic` (opus), `test-author` (sonnet), `implementer` (sonnet), `reviewer` (opus). Model / effort policy in `_shared/agent-roster.md`.

**10 shared references** in `plugin/skills/_shared/`: `agent-roster`, `ask-style`, `critic`, `diagram-presentation`, `handoff`, `interview-depth`, `mermaid-check`, `size-matrix`, `socratic-loop`, `surfaces`.

### Changed

- **Existing backbone skills rewritten** to mirror the upstream sdd pipeline content under course names:
  - `write-prd` — now code-aware (reads `architecture-map.md`), Socratic, depth-dialed; output moved to `docs/features/<slug>/PRD.md`.
  - `architecture-design` — produces SAD (Arc42 + C4 L1/L2) and declares `target_surfaces` in frontmatter; also emits `adr/NNNN-*.md` stubs.
  - `complete-sequence-diagrams` — generic participants; surface-gated UI legs (only drawn when `ui` is in `target_surfaces`).
  - `api-forge` — surface-read (contract type driven by `target_surfaces`); drift-check enforces fix-the-source-first; scenario A (typed) vs B (PRD-derived).
  - `break-tasks` — now emits `tasks.json` (machine DAG) in addition to the human tracker and task files.
  - `plan-tests` — stack-agnostic (no hardcoded tool names); surface-gated tiers.
  - `classify-size` — updated decision matrix from `_shared/size-matrix.md`.
  - `fix-term` — multi-context `CONTEXT-MAP.md` support added.
  - `decide-adr` — blast-radius worthiness gate; lifecycle Proposed → Accepted explicit.
- **Per-feature artefact path** changed from `delivery/<slug>/` to `docs/features/<slug>/`. Repo-root artefacts (`architecture-map.md`, `roadmap.md`) live under `docs/`.
- **Commit trailers** renamed `SDD-Task` / `SDD-AC` → `SDLC-Task` / `SDLC-AC`.
- `plugin.json`, `README.md`, `CLAUDE.md`, `00-overview/` updated to reflect 17-skill, 9-agent, 10-shared-ref counts and the new full-cycle description.

### Note — `generate-data-model` is a deliberate partial mirror

`generate-data-model` **intentionally does NOT adopt** the upstream sdd stance of deriving DB conventions from the target repo. It keeps the course's opinionated DB defaults: `created_at`-only audit (immutable-first, no `updated_at`), hard delete, no CHECK constraints / triggers / business-level DEFAULTs (DB as dumb storage), SQL-first migrations, timestamp-prefixed idempotent filenames. From the upstream pipeline it borrows **only** staged migrations, drift-check, and reading `architecture-map.md` as a convention source. Future maintainers: do not "fix" this toward the stack-agnostic upstream stance — the deviation is course pedagogy, not an oversight.

---

## [3.0.1] — 2026-05-19

OSS-readiness pass — translate all docs / skills / templates / overview / scripts to English and remove project- and course-specific framing so the toolkit drops into any team unchanged.

### Changed

- All 27 `plugin/skills/<name>/SKILL.md` bodies translated to English (frontmatter triggers, `## Questions for discussion`, `## Template`, anti-patterns prose). Section structure and opinionated tone preserved verbatim.
- All `document-templates/*.md` + `adr/` + `api/` + `diagrams/` skeletons translated (placeholders, `<!-- Why: ... -->` guidance, table headers, Mermaid node labels).
- `00-overview/*.md` (process-map, DoR, DoD, mvp-vs-full, rollout-plan, process-metrics, file-structure) translated end-to-end; Mermaid labels rendered in English.
- `scripts/generate-gates.sh` and `scripts/sdlc_lint.py` — comments and user-facing strings translated.
- Top-level `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `plugin/README.md`, `Makefile` translated.
- `plugin/plugin.json` `description` rewritten in clean English.

### Removed

- Course-, project-, and team-specific framing in prose (community-chat link, internal team and repo names, personal name and email in non-attribution prose). OSS attribution stays in `LICENSE` (MIT Copyright) and `plugin.json` `author` block per OSS norm.

### Not changed

- `examples/` (rate-limiting, goals-tracking) — case-study scope, intentionally left in Ukrainian and out of this pass.
- `LICENSE` — untouched (MIT Copyright preserved).
- `plugin.json` `author`, `repository`, `homepage` — untouched.
- `plugin/tests/` fixtures and rubric — out of scope for this pass.

## [3.0.0] — 2026-05-18

OSS-ready release. **Breaking** — `sdlc/01-stages/` removed; skills are now the single source of truth.

### Added

- **5 phase wrappers:** `sdlc:design` (03-07), `sdlc:detail` (08-10), `sdlc:impl-prep` (11-14), `sdlc:ship` (15-18). Each delegates to atomic skills with size-aware skip-logic per `00-overview/mvp-vs-full.md`. Single commit per phase.
- **3 cross-cutting atomic skills:**
  - `sdlc:propose-adr` — MP-threshold check (3 AskUserQuestion: hard-to-reverse / surprising / real trade-off) → ADR stub with `Status: Proposed` + bidirectional `**Locked in:**` backlink in `brainstorm.md`.
  - `sdlc:fix-term` — lazy `CONTEXT.md` glossary bootstrap (single- or multi-context via `CONTEXT-MAP.md`), canonical definition + NOT cross-reference, generic-tech-term filter, conflict check.
  - `sdlc:classify-size` — 4 AskUserQuestion (PR count / time / new module-API-migration / breaking changes) → `delivery/<slug>/.size` one-liner (XS/S/M/L/XL).
- `plugin.json` full OSS metadata: author, license, homepage, repository, keywords.
- `sdlc/LICENSE` — MIT.
- `sdlc/plugin/README.md` — install, quickstart, skill index, conventions.
- `sdlc/CONTRIBUTING.md` — how to add atomic / wrapper / template; PR checklist.
- `sdlc/CHANGELOG.md` (this file).

### Changed

- **Skill files now contain full protocol + DoD + anti-patterns** (previously skills did `Read sdlc/01-stages/NN-*.md` for protocol). Edit one place per stage, not two.
- `sdlc:intake` refactored to delegate to `sdlc:fix-term` (was inline §B CONTEXT bootstrap) and `sdlc:propose-adr` (was inline §D/§E MP-check + ADR stub). 176 → ~150 lines, no duplicated logic.
- `sdlc:intake` §G — recommends `sdlc:classify-size` as next step before design phase.
- `document-templates/*.md` HTML-comment headers updated to point at `plugin/skills/<name>/SKILL.md` (was `01-stages/NN-*.md`).
- `examples/goals-tracking/{idea-brief,SPEC}.md` HTML-comment headers updated.
- `sdlc/README.md` — stage table now points at skills, not removed stage files.
- `sdlc/CLAUDE.md` — "How to work with artefacts" rewritten to reference skills.

### Removed

- `sdlc/01-stages/01-raw-idea-intake.md` ... `18-obsidian-kb-sync.md` (18 files). Content merged into corresponding `plugin/skills/<name>/SKILL.md`. Backup tag `pre-phase-1-stages-merge` preserves prior state for diff.

## [2.1.0] — 2026-05-17

### Added

- `sdlc:intake` composite wrapper (stages 01-02 + MP-threshold ADR-propose + lazy `CONTEXT.md` glossary with inline term-resolution).
- Bidirectional `**Locked in:** [[adr/NNNN-...]]` backlink in `brainstorm.md` after ADR stub creation.

## [2.0.0] — 2026-05-15

### Added

- 16 atomic skills for stages 03-18 (`write-spec`, `draft-architecture`, `write-arc42`, `draw-c4`, `draw-sequence`, `design-db`, `plan-migration`, `define-api`, `decide-adr`, `pack-impl`, `break-tasks`, `prep-context`, `plan-tests`, `prep-review`, `write-changelog`, `sync-kb`).

### Removed

- `sdlc-stage-runner` (consolidated 18-stage runner; superseded by atomic skills with hard-prereq gates).

## [1.0.0] — 2026-05-12

### Added

- Initial Claude Code plugin scaffold with `sdlc:interview` (stage 01) and `sdlc:brainstorm` (stage 02).
- `document-templates/` for all 18 stage artefacts.
- `00-overview/` — process map, definition-of-ready, definition-of-done, MVP-vs-full matrix.
- `examples/rate-limiting/` — synthetic end-to-end example.
- `Makefile` with `sdlc-check` and `sdlc-metrics` targets.

[Unreleased]: https://github.com/genkovich/agentic-engineering-course/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/genkovich/agentic-engineering-course/compare/v3.0.1...v4.0.0
[3.0.1]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v3.0.1
[3.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v3.0.0
[2.1.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v2.1.0
[2.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v2.0.0
[1.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v1.0.0
