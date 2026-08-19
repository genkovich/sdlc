# architecture-design Self-check + Anti-patterns

## TL;DR (короткий вступ українською)

Це **повний чеклист завершення** (англ. *Definition of Done*) — список того, що skill має перевірити перед фінальним комітом.

Як читати розміри функцій (size class):
- **XS** — функція на дні (1-2 інженери, 1 тиждень).
- **S** — на тиждень-два (1-3 інженери, 2-3 тижні).
- **M** — на місяць (2-5 інженерів, 3-5 тижнів). Типова функція курсу.
- **L** — на квартал (4-8 інженерів, 6-12 тижнів).
- **XL** — на квартал+ з 2+ команд.

Очікувана кількість ADR залежить від розміру: XS/S → 2-4, M → 5-12, L/XL → 10-15.

---

Used at the end of Protocol Step 6 (before the Step 7 critic dispatch) and at the end of Step 7 (before the finalization commit). The SKILL.md keeps 6-8 inline non-negotiables; the full DoD + anti-patterns + N/A logic + ADR count expectations live here.

## Definition of Done

- [ ] `docs/features/<slug>/sad.md` exists with all 12 Arc42 sections filled OR marked `<!-- N/A: <one-line reason> -->`. Empty sections without N/A note are not OK.
- [ ] Frontmatter `target_surfaces: [...]` is non-empty (the §4 Target-surface decision was made) and §5 draws **one C4 container per declared surface**. Each declared UI surface (`web-frontend` / `mobile-app` / `desktop-app`) carries a UI-architecture decision — an ADR, or an inline §4 note if it didn't cross the gate. → [`../../_shared/surfaces.md`](../../_shared/surfaces.md).
- [ ] §3 has a `C4Context` Mermaid block with real actors from CONTEXT glossary + real external systems from the architecture-map / scan (no `<placeholder>` template stubs); validated per [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md).
- [ ] §5 has a `C4Container` Mermaid block with real containers / datastores / boundaries (no `<placeholder>`); validated per [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md).
- [ ] §6 has ≥1 `sequenceDiagram` Mermaid block (architecture-design seeds the primary flow(s); `sdlc:complete-sequence-diagrams` then covers every critical flow / §5 AC — no cap).
- [ ] §9 Architecture decisions table references every file in `docs/features/<slug>/adr/` AND every §9 row points to an existing file (no orphans either way).
- [ ] 2-15 ADRs in `docs/features/<slug>/adr/` total. Typical ranges by size: XS/S = 2-4 ADRs; M = 5-12 ADRs; L/XL = 10-15 ADRs. Outside this range → review with anti-patterns below.
- [ ] §10 Quality scenarios are testable (When / Then / How-verify form, no «fast» / «high availability» without numbers). Numbers reference PRD §6 NFR verbatim (no inventing, no rounding).
- [ ] §11 Risks/Open-Decisions table has ≥1 row with severity + mitigation + owner. Severity column literal values: `Low` / `Medium` / `High` for regular risks; `Open question` for Save-as-OQ rows.
- [ ] §11 contains a row for every `save_as_oq`-migrated decision from the Step 6 edits-log with both owner AND due filled (no lone owner, no lone due). Missing either → resolution was downgraded to `drop` with a warning.
- [ ] Step 3 read `docs/architecture-map.md` (or the `sdlc:explorer` scan ran on a brownfield repo, or §3 has the `<!-- brownfield: N/A — greenfield repo -->` note).
- [ ] Step 6 edits-log maintained: every `Edit` / `Drop` / `Save as Open Question` resolution appended one entry with `{decision_id, action: edit|drop|save_as_oq, before, after, user_reason}`. `Approve` decisions intentionally absent (baseline).
- [ ] Step 7 critic sub-agent (`sdlc:critic`) ran on the post-Socratic `sad.md` + edits-log + ADR-spawns log; all findings either resolved via `AskUserQuestion` or overridden with rationale (recorded as a «Decision overrides» bullet in §1 Introduction paragraph 4).
- [ ] Step 7 pre-write backstop scans ran (Mermaid validation per [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md) / ADR title format / §9 orphan) — 0 hits OR all hits explicitly overridden in the resolution loop with recorded rationale.
- [ ] Roles in §1 Stakeholders + §3 actors match CONTEXT glossary exactly (no inventing `user` / `admin` when glossary defines specific roles).
- [ ] Every ADR has Status = `Accepted` (not `Proposed` — this skill is synchronous). Use `sdlc:decide-adr` separately if you need a Proposed → Accepted workflow on something already half-decided in code.
- [ ] Every ADR title is in **decision-form** (imperative kebab-case), not problem-form: `0003-sliding-window-with-redis.md` ✓ vs `0003-rate-limiting.md` ✗.
- [ ] Incremental commits per section: `feat(<slug>): sad §N — <decisions summary>`. Final commit: `feat(<slug>): sad finalization (critic pass)`.
- [ ] PM has been consulted on §10 Quality Goals (the only PM touchpoint in this skill — Architect/Tech Lead drives everything else).

## N/A logic — when a section can be marked N/A

A section may be marked `<!-- N/A: <one-line reason> -->` only when both: (a) there's a concrete reason tied to size class or feature scope; (b) the N/A is consistent with the rest of the SAD (e.g. §7 N/A means §5 Container view does NOT show a new deployment unit).

- **§2 Constraints** — never N/A. Every feature inherits at least Conventions (CLAUDE.md) and Technical (language + framework + datastore versions).
- **§3 Context** — never N/A. Greenfield → still draw C4 Context with the planned actors + external systems.
- **§6 Runtime** — never N/A for M+. architecture-design seeds the primary flow(s) here (≥1 happy-path always); `sdlc:complete-sequence-diagrams` then completes §6 with every critical flow / §5 AC (no cap). If literally no flow is non-trivial (pure CRUD), document a single happy-path CRUD sequence — never N/A the whole section.
- **§7 Deployment** — N/A allowed for XS/S that reuses existing deployment unit with no changes to replicas / scaling thresholds / monitoring. Reason text required: `<!-- N/A: feature reuses existing deployment unit, no replica/scaling/monitoring change -->`.
- **§9 Architecture decisions** — N/A allowed only if no ADRs spawned (typically XS features with only convention-level decisions). Reason text required: `<!-- N/A: no decisions crossed blast-radius threshold this pass -->`. **More common case** is §9 has 2-15 rows, not N/A.
- **§11 Risks** — never N/A. If no Save-as-OQ rows AND no risks identified from PRD §8 / Explore, document at least one risk that brownfield drift might invalidate Step-3 Explore findings before merge.
- **§12 Glossary** — never N/A. Pull from CONTEXT.md + sad.md content; at minimum the domain terms used in sad.md body must be defined here.

Other sections (§1, §4, §5, §8, §10) are mandatory — no N/A.

## Anti-patterns (full list)

In addition to the inline non-negotiables in SKILL.md `## Self-check`:

- **>60 questions in one pass** — fatigue threshold. If approaching, bundle trivial defaults under one «I'm assuming … . Override?» question per [socratic-cadence.md](./socratic-cadence.md) Rule 1. Target total: 8-20 questions per pass; over 25 = fatigue territory.
- **An ADR for every Socratic decision** — kills the ADR genre. Only blast-radius decisions become ADRs (see [blast-radius-heuristic.md](./blast-radius-heuristic.md)). Expect 5-12 for M-class features, NOT 25.
- **Spilling into C4 L3 / L4** — explicitly out of scope. L3 Component + L4 Code are deferred to a separate diagramming pass. Suggest `sdlc:complete-sequence-diagrams` (which covers the runtime flows) if the user asks.
- **Re-asking decided things on resume** — read `sad.md` first; sections with real content are *decided*. Only the Step 7 critic surfaces re-questioning, and only on cross-section drift detection.
- **One giant commit at the end** — incremental commits per section (Step 6e) + finalization commit (Step 7) make resume + review tractable. Single end-of-pass commit loses per-section traceability.
- **«For completeness» empty sections** — every section either has real content or `<!-- N/A: <one-line reason> -->`. An empty section without N/A note is a structural F5 critic finding.
- **Generated ADRs with `Proposed` status** — this skill is synchronous (you are deciding with the user right now). Status is `Accepted`. Use `sdlc:decide-adr` separately for Proposed → Accepted workflow on something already half-decided in code.
- **ADR with strawman options** — ADR `Considered options` excludes alternatives ruled out by existing constraints. Don't include «MongoDB» if CLAUDE.md pins Postgres; don't include «Redis» if there's no Redis in the stack and no §4 strategic seed for a cache tier. Strawmen dilute the ADR genre and trigger F6 critic.
- **ADR title in problem-form** — `0003-rate-limiting.md` describes the problem; `0003-sliding-window-with-redis.md` describes the chosen approach. ADR title must be a decision (imperative), not a topic.
- **Skipping the brownfield context (Step 3)** — guessing the repo layout produces a fictional §5 Container view + invented §2 Constraints. Read `docs/architecture-map.md`; re-scan with `sdlc:explorer` only if it's absent/stale; greenfield skips with the `<!-- brownfield: N/A -->` note.
- **Re-deriving the surface downstream** — architecture-design declares `target_surfaces` once (§4); `api-forge` / `complete-sequence-diagrams` / `break-tasks` / `plan-tests` / `review-feature` read it. Re-inferring it when the SAD already declared it is the anti-pattern surfaces.md kills.
- **Save-as-Open-Question without owner+due** — skill MUST ask follow-up `AskUserQuestion` immediately after the user picks this option. If user leaves either field blank, the migration is downgraded to `Drop` with explicit warning surfaced — never silently shipped with half-filled §11 row.
- **Skip the Step 7 critic** — the Step 6 Socratic loop only catches per-section issues; it cannot see cross-section drift caused by user edits (e.g. §4 outbox-events caps vs §6 happy-path missing outbox emit). Writing the finalization commit without running the critic ships that drift downstream to `sdlc:complete-sequence-diagrams` / `sdlc:api-forge` / `sdlc:decide-adr`.
- **Resolve critic findings unilaterally** (without `AskUserQuestion`). The whole point of Step 7 is to surface contested decisions to the user. Picking «revert» or «amend» without asking re-introduces the silent-edit failure mode.
- **Mermaid template stubs in §3 / §5 left in final draft** — `Person(user, "<User>", "<role + intent>")` is a placeholder. Pre-write regex scan catches this; F5 critic catches this; structural floor is real actors + real names everywhere.
- **§10 scenarios with invented numbers** — F6 critic catches NFR-number leak. §10 cites PRD §6 NFR verbatim (no rounding, no inventing thresholds the PM never agreed to).
- **Returning to a previously-written section** — Step 6e commits each section atomically; Step 6f explicitly forbids reverting to earlier sections. Drift between sections is the critic's job in Step 7. Re-opening §4 after writing §10 means you're not trusting the per-section batch contract.
