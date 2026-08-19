# sdlc — Claude Code plugin

20 skills + 11 plugin-namespaced agents for a full ideation → ship pipeline with Claude.

- **12-stage backbone** — covers the entire cycle from codebase scan to merge & changelog.
- **7 cross-cutting utilities** — called ad-hoc at any stage (classify-size, fix-term, decide-adr, roadmap, prepare-design-spec, verify-ui, user-documentation).
- **1 ideation skill** — interview (runs researcher / strategist / analyst / devils-advocate agents).
- **11 agents** — dispatched as `sdlc:<name>` from inside skills; model/effort policy in `skills/_shared/agent-roster.md`.
- **10 shared references** — `skills/_shared/` files consumed by multiple skills (surfaces, handoff, mermaid-check, depth-dial, …).

Each skill is a self-contained folder under `skills/<name>/` — `SKILL.md` (protocol + DoD + anti-patterns), optional `templates/` (skeletons the skill copies into `docs/features/<slug>/`), optional `references/` (mini-guides the skill reads at specific protocol steps).

## Install

```bash
# Option A — symlink (recommended for hacking)
ln -s "$(pwd)/sdlc/plugin" ~/.claude/local-plugins/sdlc

# Option B — Claude Code installer
claude /plugin install ./sdlc/plugin
```

Verify: `claude /plugin list` shows `sdlc`; `/sdlc-interview` (or any other slash-trigger below) appears in the slash menu.

## Skill order — full backbone (12 stages)

> Each stage reads the previous stage's artefacts. The `map-architecture` scan happens **once** at the start; later stages read `docs/architecture-map.md` instead of re-scanning. Cross-cutting utilities (`fix-term`, `classify-size`, `decide-adr`, `roadmap`, `prepare-design-spec`, `verify-ui`) are called ad-hoc, not in sequence.

| Stage | Skill | Command | Output |
|------:|-------|---------|--------|
| 00 | [`map-architecture`](skills/map-architecture/SKILL.md) | `/sdlc-map-architecture` | `docs/architecture-map.md` (repo-root); greenfield → scaffold `tasks.json` |
| 03 | [`write-prd`](skills/write-prd/SKILL.md) 🚪 | `/sdlc-write-prd` | `docs/features/<slug>/PRD.md` |
| 03 | [`clarify-prd`](skills/clarify-prd/SKILL.md) | `/sdlc-clarify-prd` | tightens `PRD.md` in place (ambiguity sweep) |
| 04–05 | [`architecture-design`](skills/architecture-design/SKILL.md) 🚪 | `/sdlc-architecture-design` | `docs/features/<slug>/sad.md` (Arc42 + C4 L1/L2 + `target_surfaces` frontmatter) + `adr/NNNN-*.md` |
| 05 | [`complete-sequence-diagrams`](skills/complete-sequence-diagrams/SKILL.md) | `/sdlc-complete-sequence-diagrams` | `sad.md §6` flows (generic participants, surface-gated UI legs) |
| 07 | [`generate-data-model`](skills/generate-data-model/SKILL.md) | `/sdlc-generate-data-model` | `docs/features/<slug>/data-model.md` + **staged** `docs/features/<slug>/migrations/` (promoted by implement-tasks) |
| 10 | [`api-forge`](skills/api-forge/SKILL.md) | `/sdlc-api-forge` | `docs/features/<slug>/contracts/openapi.yaml` (+ events.md / cli.md / public-api.md per surface) + `api-sync-report.md` |
| 13 | [`break-tasks`](skills/break-tasks/SKILL.md) | `/sdlc-break-tasks` | `docs/features/<slug>/tasks/_epic.md` + `tracker.md` + `<task>.md` + **`tasks/tasks.json`** (machine DAG) |
| 15 | [`plan-tests`](skills/plan-tests/SKILL.md) | `/sdlc-plan-tests` | `docs/features/<slug>/test-plan.md` (surface-gated tiers; generic, no hardcoded tools) |
| 17 | [`implement-tasks`](skills/implement-tasks/SKILL.md) | `/sdlc-implement-tasks` | committed TDD code + tests + updated `tracker.md`; promotes staged migrations |
| 17 | [`review-feature`](skills/review-feature/SKILL.md) 🚪 | `/sdlc-review-feature` | `docs/features/<slug>/_review/review-<date>.md` (PASS / CHANGES REQUESTED) |
| 18 | [`ship-feature`](skills/ship-feature/SKILL.md) 🚪 | `/sdlc-ship-feature` | `CHANGELOG.md` + PR body; moves feature to `docs/roadmap.md` Shipped |

🚪 = hard refuse if prereq is missing.

## Cross-cutting utilities (ad-hoc, no fixed stage)

| Skill | Command | Output |
|-------|---------|--------|
| [`interview`](skills/interview/SKILL.md) | `/sdlc-interview` | `docs/features/<slug>/idea-brief.md` (ideation suite — researcher / strategist / analyst / devils-advocate) |
| [`classify-size`](skills/classify-size/SKILL.md) | `/sdlc-classify-size` | `docs/features/<slug>/.size` (XS/S/M/L/XL; matrix in `_shared/size-matrix.md`) |
| [`fix-term`](skills/fix-term/SKILL.md) | `/sdlc-fix-term` | `CONTEXT.md` glossary (+ multi-context `CONTEXT-MAP.md`) |
| [`decide-adr`](skills/decide-adr/SKILL.md) 🚪 | `/sdlc-decide-adr` | standalone `adr/NNNN-*.md` (blast-radius worthiness gate, Proposed → Accepted) |
| [`roadmap`](skills/roadmap/SKILL.md) | `/sdlc-roadmap` | `docs/roadmap.md` (Now / Next / Later / Shipped tables) |
| [`prepare-design-spec`](skills/prepare-design-spec/SKILL.md) | `/sdlc-prepare-design-spec` | `docs/features/<slug>/design-spec.md` |
| [`verify-ui`](skills/verify-ui/SKILL.md) | `/sdlc-verify-ui` | per-AC live browser verdict + screenshot evidence |
| [`user-documentation`](skills/user-documentation/SKILL.md) | `/sdlc-user-documentation` | end-user flow docs + linked User Guide index from a live app (screenshots, optional screencasts) |

## Agents

11 agents are dispatched as `sdlc:<name>` from inside skills — never called directly by the user. Model/effort policy for each agent lives in [`skills/_shared/agent-roster.md`](skills/_shared/agent-roster.md).

| Agent | Role | Dispatched from |
|-------|------|----------------|
| `sdlc:explorer` | Fast codebase scan (haiku) | map-architecture |
| `sdlc:researcher` | Source research (sonnet) | interview |
| `sdlc:strategist` | Strategic framing (opus) | interview |
| `sdlc:analyst` | Trade-off analysis (opus) | interview |
| `sdlc:devils-advocate` | Adversarial stress-test (opus) | interview |
| `sdlc:critic` | Clean-context quality review (opus) | write-prd, architecture-design, review-feature |
| `sdlc:test-author` | Test plan generation (sonnet) | plan-tests |
| `sdlc:implementer` | GREEN — make the red test pass (sonnet) | implement-tasks |
| `sdlc:refactor` | REFACTOR — tidy while green, isolated (sonnet) | implement-tasks |
| `sdlc:reviewer` | Final feature review (opus) | review-feature |
| `sdlc:doc-flow` | Per-flow user-doc walk + write (sonnet) | user-documentation |

## Shared mechanisms

`skills/_shared/` contains 10 reference files consumed by multiple skills:

| File | Purpose |
|------|---------|
| `agent-roster.md` | Model/effort/agents policy for all 11 agents |
| `ask-style.md` | AskUserQuestion formatting conventions |
| `critic.md` | Critic-phase protocol (clean-context adversarial review) |
| `diagram-presentation.md` | Mermaid diagram rendering and presentation rules |
| `handoff.md` | Stage-handoff block template (every skill ends with one) |
| `interview-depth.md` | Depth-dial (1–5) for the ideation interview |
| `mermaid-check.md` | Mermaid syntax validation checklist |
| `size-matrix.md` | XS/S/M/L/XL classification matrix |
| `socratic-loop.md` | Socratic Q&A loop protocol shared by multiple skills |
| `surfaces.md` | `target_surfaces` taxonomy (web / mobile / api / cli / event / background) |

**Cross-cutting mechanisms:**

- **`target_surfaces`** — declared in `sad.md` frontmatter by `architecture-design`; downstream skills (sequences, api, tasks, plan-tests, review) gate on it instead of re-deriving.
- **`architecture-map.md`** — `map-architecture` scans the codebase once; later stages read it. Carries a §Frontend/UI foundation section so UI work reuses the existing design system.
- **`tasks.json`** — machine-readable DAG (`id, title, layer, deps, acs, dod, files_hint`) at `docs/features/<slug>/tasks/tasks.json`; `implement-tasks` reads it to close the cycle.
- **Staged migrations** — `generate-data-model` writes to `docs/features/<slug>/migrations/`; `implement-tasks` promotes them into the repo's live migrations tree (re-stamping timestamps).
- **TDD engine** — `implement-tasks` runs SELECT → RED → GREEN → REFACTOR → GATE → COMMIT; supports sequential / agent-team / dynamic Workflow modes; commit trailers `SDLC-Task` / `SDLC-AC`.
- **Stage-handoff blocks** — every skill ends with a handoff block (from `_shared/handoff.md`) naming the next skill and what to pass forward.
- **Socratic loop** — shared Q&A cadence across write-prd, architecture-design, clarify-prd.
- **Critic phase** — clean-context `sdlc:critic` / `sdlc:reviewer` used in PRD, architecture, and final review to surface blind spots.

## What's inside each skill

Every skill folder has the same anatomy:

- `SKILL.md` — frontmatter (`name`, `description`, `triggers`, `stage`) + the protocol the skill executes + Self-check + anti-patterns. Single source of truth.
- `templates/` *(if the skill copies a skeleton)* — the artefact starter that the skill writes into `docs/features/<slug>/`. Owned by this skill: no other skill copies it.
- `references/` *(if the protocol is long)* — mini-guides loaded at specific protocol steps.

Per-skill specifics (templates + key references):

| Skill | Key files |
|-------|-----------|
| `map-architecture` | no templates — writes `docs/architecture-map.md` directly from codebase scan |
| `interview` | `templates/idea-brief.md` (15 sections); dispatches researcher/strategist/analyst/devils-advocate |
| `write-prd` | `templates/PRD-template.md`; `references/{draft-generation,socratic-loop,critic-phase,critic-prompt,ask-examples,checklist}.md` |
| `clarify-prd` | `references/ambiguity-sweep.md` (tightens PRD in place, no new file) |
| `architecture-design` | `templates/{sad-template,adr-template,c4-context,c4-container,deployment}.md`; `references/{draft-generation,socratic-loop,blast-radius-heuristic,socratic-cadence,c4-mermaid-syntax,…}.md` |
| `complete-sequence-diagrams` | `templates/seq-flow.md` (single-flow shape, embedded inline in SAD §6) |
| `generate-data-model` | `templates/{data-model,rules-migrations-baseline}.md`; staged migrations to `docs/features/<slug>/migrations/`; reads `docs/architecture-map.md` for convention source |
| `api-forge` | `templates/{openapi.yaml,events.md}`; `references/{cli.md,public-api.md,drift-check.md}` (per-surface contracts + drift detection) |
| `break-tasks` | `templates/{_epic,tracker,task}.md`; produces `tasks/tasks.json` machine DAG |
| `plan-tests` | `templates/test-plan.md` |
| `implement-tasks` | reads `tasks/tasks.json`; `references/{tdd-engine,commit-format,sdlc-local,…}.md` (×8); promotes staged migrations |
| `review-feature` | `templates/review-template.md`; `references/review-dimensions.md` (AC trace + quality dimensions) |
| `ship-feature` | `templates/{changelog-entry,pr-body}.md`; forge-detect (gh/glab); updates `docs/roadmap.md` |
| `decide-adr` | no own templates — pulls canonical `../architecture-design/templates/adr-template.md` cross-skill |
| `fix-term` | `templates/CONTEXT.md` (lazy bootstrap for the per-feature glossary) |
| `classify-size` | no template — writes a 1-line `.size` file |
| `roadmap` | `templates/roadmap.md` (Now/Next/Later/Shipped tables) |
| `prepare-design-spec` | `templates/design-spec.md`; repository-aware design-entry contract |
| `user-documentation` | `templates/{flow-doc,user-guide-index}.md`; `references/{style-guide,determinism,flow-inventory}.md`; `scripts/{validate-docs.py,replay-screencast.sh}`; dispatches `sdlc:doc-flow` per flow |

## DB exception

`generate-data-model` is a **deliberate partial mirror** of the upstream sdd pipeline. It keeps the course's opinionated DB defaults — audit = `created_at` only (immutable-first); hard delete; no CHECK / TRIGGER / business DEFAULT (DB as "dumb storage"); SQL-first migrations; timestamp-prefixed idempotent filenames. It does **not** adopt sdd's stack-agnostic "detect-the-repo's-DB-philosophy" stance. From the upstream pipeline it borrows only: staged migrations, drift-check, and reading `docs/architecture-map.md` as a convention source.

## Shared templates

`sdlc/document-templates/` keeps templates that don't belong to any single skill:

- **Cross-feature / manual** — `CHANGELOG.md`, `CONTEXT-MAP.md` (multi-context glossary map), `claude-context.md` (coding-session bootstrap), `review-checklist.md`, `rollback-plan.md`, `migration-plan.md`, `task-breakdown.md` (legacy alias for `break-tasks` outputs), `diagrams/c4-component.md` (L3, out of scope for SAD).
- **Legacy** — `SPEC.md`, `arc42.md`, `architecture-brief.md`, `adr/NNNN-title.md` — superseded artefacts kept for repos that haven't migrated.

Skills do **not** copy from this folder during their protocol. These are snippets a human pulls in by hand when the feature needs them.

## Conventions

- **Skill = source of truth.** Edit `skills/<name>/SKILL.md` to change skill behaviour; the protocol there is what gets executed.
- **Templates colocated with their owner skill** — single ownership; copying a skill folder gives you a working skill.
- **Mermaid only** for diagrams (C4, sequence, ER, deployment). No PlantUML, no draw.io.
- **One ADR = one decision.** Spawned inline through the blast-radius gate in `architecture-design`; standalone via `decide-adr` for post-hoc cases.
- **Texts in repo, not Confluence.**
- **Feature artifacts at `docs/features/<slug>/`** — repo-root artifacts at `docs/` (architecture-map.md, roadmap.md).

## Customizing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to add a new skill.

## License

MIT. See [LICENSE](../LICENSE).
