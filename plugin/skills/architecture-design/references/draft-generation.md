# Draft generation — per-section contract for architecture-design Protocol step 5

## TL;DR (короткий вступ українською)

Це крок 5 у Protocol — як skill робить **чорновик у памʼяті** перед тим, як питати користувача (крок 6) і писати на диск (крок 6e).

На кожну з 12 секцій Arc42 skill:

1. Бере джерела у пріоритеті: CONTEXT.md → PRD.md → architecture-map.md (або scan через `sdlc:explorer`) → попередні рішення.
2. Тягне з **item-bank** (бібліотеки готових варіантів) — наприклад, для §4 це «sync HTTP / async via outbox / sync через спільну БД».
3. Прогоняє **pre-Socratic hygiene** (попередні перевірки чистоти): чи актори з CONTEXT, чи числа з PRD §6 NFR, чи всі Mermaid-блоки використовують реальні імена.

Глосарій:
- *item-bank* — бібліотека типових варіантів для секції (skill підказує, які опції найчастіше зустрічаються).
- *pre-Socratic hygiene* — фінальні перевірки до того, як питати користувача: щоб не питати про те, що вже зафіксовано у CONTEXT/CLAUDE.md.

---

How the skill turns required inputs (PRD + CONTEXT + the architecture-map / Explore report) + earlier-section decisions + template instructions into an in-memory draft for each of the 12 Arc42 sections. The authoritative format/structure source is the inline comment in [../templates/sad-template.md](../templates/sad-template.md) for that section. This file is the operational glue: where the content comes from per section + the item-banks the skill draws from + pre-Socratic hygiene checks.

The draft is held in memory only — the on-disk `sad.md` is **not** touched between Step 4 (bootstrap copy) and Step 6e (per-section file write). The skill ends Step 5 with all 12 sections proposed in-memory + each section's decision list ready for the Step 6 batch loop.

## Inputs in priority order

1. **`CONTEXT.md` `## Glossary`** — canonical for role names + domain terms. If anything contradicts it (PRD, the map/scan, reference code), glossary wins.
2. **`docs/features/<slug>/PRD.md`** — Goals (§2), Non-goals (§3), NFR (§6 incl. numeric targets + measurement sources), §6.1 Security/privacy + abuse cases, KPIs (§7), Open questions (§8), §13 Recommendation, §1 Context overrides (¶4 bullets emitted by the `sdlc:clarify-prd` / `sdlc:write-prd` critic).
3. **The current-architecture source** (Step 3) — `docs/architecture-map.md` if present + fresh, else the `sdlc:explorer` scan: primary language + framework + versions; top-level module layout; ports/adapters/layering conventions; data stores; inter-module communication style; the existing design system / component library / tokens (§Frontend / UI foundation); repo-pinned constraints relevant to `<slug>`. Greenfield → null (skill notes `<!-- brownfield: N/A — greenfield repo -->` in §3 and skips repo-pattern citations).
4. **Earlier-section in-memory decisions** — §4 surface + strategic choices constrain §5/§6/§7/§8; §5 module boundaries constrain §6 flows; §10 quality scenarios reference §1 quality goals. The skill must read its own in-memory draft when drafting later sections (no re-reading the file).

## Per-section sources + item-banks

The item-banks below are guidance — the skill picks how many items to draft based on size class (`.size`) and PRD signal. No upper cap on items per section; lower bounds noted where they exist.

- **§1 Introduction and goals.**
  - Intent (1 paragraph): from PRD §2 Goals + §1 Context.
  - **Top-3 quality goals (1-liners; ≥3, typically 3, occasionally 4)** — from PRD §6 NFR ranked by NFR criticality + PRD §13 Recommendation. Each goal is 1 line; full scenarios live in §10.
  - Stakeholders table: from PRD §4 User-story roles + CONTEXT glossary (Tech Lead row added, Sign-off owner = Yes).

- **§2 Constraints.**
  - **Technical**: the map/scan-reported language + framework + datastore versions + architecture convention. If PRD §6 NFR includes a pin override → that wins.
  - **Organisational**: PRD §2 deadline + effort budget if quoted; otherwise leave `<TBD by PM>` and add an entry to §11 Risks.
  - **Conventions**: link to the repo's convention file (CLAUDE.md / equivalent) + reference any module-level patterns from the map/scan.
  - **Regulatory**: PRD §6.1 Security/privacy verdict + abuse-cases — copy applicable controls. Never N/A.

- **§3 Context and scope.**
  - 2-3 sentences business context: from PRD §1 ¶1 + §1 ¶3 Recommendation vector.
  - External systems table: from PRD §6.1 Security cross-context entries + the map/scan «inter-module communication» + «data stores» rows.
  - **C4 Context (L1) Mermaid block**: actors from CONTEXT glossary roles + PRD §4 US, external systems from the map/scan. 5-10 elements max. Syntax → see [c4-mermaid-syntax.md](./c4-mermaid-syntax.md). Confirm prose-first → [`../../_shared/diagram-presentation.md`](../../_shared/diagram-presentation.md); validate → [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md). Never N/A.

- **§4 Solution strategy.**
  - **Target surface(s) FIRST** — `backend-service` / `web-frontend` / `mobile-app` / `desktop-app` / `cli` / `worker` / `library-sdk`, derived from PRD §1 «for whom» + §4 roles (the PRD names no surface). Written to frontmatter `target_surfaces`, gates §5 + every downstream stage → [`../../_shared/surfaces.md`](../../_shared/surfaces.md). Multi-surface ⇒ usually an ADR.
  - **Top-3 strategic choices (≥3, typically 3, sometimes 4)** — the seeds for ADRs. Each: 2-3 sentences rationale referencing relevant Quality Goals + Constraints.
  - **Decision-bank (typical strategic decisions per choice)**:
    - Module-to-module integration: async via outbox events / sync HTTP / sync via shared DB.
    - Persistence strategy: single store / per-module store / read-write split.
    - **UI-architecture, one per declared UI surface** (web → server-rendered / SPA / hybrid; mobile → native / cross-platform; + state-management + routing if warranted) — this **replaces** the old single "dashboard / read-side delivery" item, lifting it to a per-surface decision. The UI **reuses** the repo's existing design system / components / tokens from `architecture-map.md` §Frontend → [`../../_shared/surfaces.md`](../../_shared/surfaces.md).
    - Concurrency model: optimistic locking / pessimistic locking / event sourcing.
    - Caching tier: none / in-process / shared (e.g. Redis).
  - **ADR-gate kicks in almost always** for §4 decisions because they're strategic-level. Plan ≥2 ADRs from §4 alone.

- **§5 Building block view.**
  - 1 paragraph: layered / hexagonal / clean / event-driven + why.
  - **Decision-bank**:
    - Extend existing module vs new module (boundary heuristic from the map/scan).
    - Layered vs hexagonal vs clean (default = follow the repo's convention; only ask if PRD signals divergence).
    - Internal sub-package layout (`domain/`, `app/`, `infra/`, `ports/` or project equivalent).
  - **C4 Container (L2) Mermaid block**: **one `Container` per declared `target_surface`** (a fullstack `[backend-service, web-frontend]` draws both the backend-API container and the web/SPA container; a `[backend-service, mobile-app]` draws the API + the mobile app), plus the feature's other modules/services as `Container`, datastores as `ContainerDb`. Syntax → see [c4-mermaid-syntax.md](./c4-mermaid-syntax.md). Confirm prose-first → [`../../_shared/diagram-presentation.md`](../../_shared/diagram-presentation.md); validate → [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md).

- **§6 Runtime view.**
  - Seed the **primary critical flow(s)** here — happy-path always; a failure-mode flow if §4 picked async or has an external dependency; an event-propagation flow if §4 picked events. For a declared UI surface, seed a UI-driven flow (`<user>` → `<ui>` → `<service>` → `<data-store>`). architecture-design **seeds**; the `complete-sequence-diagrams` stage then covers **every §5 AC** (no cap). XS/S keeps ≥1 happy-path flow; never N/A for M+.
  - Mermaid `sequenceDiagram` block per flow with actors + ≥2 participants + ≥3 message arrows. Reference §5 containers by name (no inventing new ones). Messages are semantic — no HTTP verbs / paths / status codes (those arrive at the `api-forge` stage). Validate → [`../../_shared/mermaid-check.md`](../../_shared/mermaid-check.md).
  - **Decision-bank**: which failure modes are critical enough to diagram (downstream-down, timeout, partial-failure, idempotency reset).

- **§7 Deployment view.**
  - Topology in 2-3 sentences: where it runs + replicas + scaling thresholds.
  - Monitoring rows: metrics + alerts + tracing — sourced from the repo's observability conventions + PRD NFR latency targets.
  - **For XS/S that doesn't change deployment** → `<!-- N/A: feature reuses existing deployment unit -->` is allowed (still draft a 1-sentence justification). Scaffold → [../templates/deployment.md](../templates/deployment.md).

- **§8 Crosscutting concepts.**
  - Table rows: logging / auth / errors / ID strategy / i18n / observability / events / rate-limiting (if applicable).
  - **Default = «inherit the repo's conventions»** — bundled as one `AskUserQuestion` per [socratic-cadence.md](./socratic-cadence.md) Rule 1: "I'm assuming the repo's defaults. Override?" with 2 options (`Keep defaults` / `Custom for §X`).
  - Per-feature override only if PRD §6 NFR or §6.1 Security signals it.

- **§9 Architecture decisions.**
  - Table auto-populated as ADRs spawn in §4-§8. No drafting in Step 5 — section starts empty, filled during the Step 6 ADR-gates.

- **§10 Quality requirements.**
  - **≥3 scenarios (one per Quality Goal from §1)** — full When/Then/How-verify form.
  - Numbers from PRD §6 NFR **verbatim** — no inventing, no rounding. If PRD says «p95 ≤ 250ms», SAD says «p95 ≤ 250ms». Forbidden: «fast», «scalable», «high availability» without a number.
  - **How-verify**: concrete test name / chaos drill / load-test command / Prometheus metric — not «integration test».

- **§11 Risks and technical debt.**
  - Auto-generated at end of Step 6 from edits-log + PRD §8 Open Questions + the map/scan-reported brownfield gotchas.
  - **Decision-bank**: outbox/queue lag during an outage; schema-versioning debt; brownfield drift; security debt accepted in v1; accepted-debt rows.
  - **Open-architectural-decision rows** (from Step 6 `Save as Open Question` resolutions): see [socratic-loop.md](./socratic-loop.md) §«Open-Questions table».
  - **Severity column** accepts literal `Open question` value for OQ rows (in addition to Low/Medium/High for regular risks). Never N/A.

- **§12 Glossary.**
  - Auto-extract from CONTEXT.md glossary terms that appear in sad.md body + add domain terms surfaced during the Step 6 Socratic that aren't in CONTEXT (flag those for a `sdlc:fix-term` follow-up after the pass).

## Cadence (size-aware) — architecture-design's question budget

The 4-state machine, the mini-recap-every-5, and the soft per-section budget all come from [`../../_shared/socratic-loop.md`](../../_shared/socratic-loop.md) + [socratic-cadence.md](./socratic-cadence.md). architecture-design's per-section targets:

| Section | Typical Qs | Note |
|---|---|---|
| §1 Intro & goals | 0-1 | Usually pulled from the PRD. Ask if the top-3 quality goals are unclear. |
| §2 Constraints | 1-2 | One bundled «any stack/version overrides?» |
| §3 Context | 0-1 | Mostly drawn from PRD + the map/scan. |
| §4 Solution strategy | 2-4 | The dense one — surface-first, then strategic choices; expect ADRs. |
| §5 Building blocks | 1-3 | Module boundaries, layering style. |
| §6 Runtime | 1-2 | Which failure modes get a diagram. |
| §7 Deployment | 0-2 | Often `<!-- N/A -->` for a feature inside an existing unit. |
| §8 Crosscutting | 1 bundled | «Repo defaults + overrides?» |
| §9 ADR index | 0 | Auto-populated. |
| §10 Quality reqs | 1-2 | Numbers from PRD NFR + verify method. |
| §11 Risks | 1-2 | «Top-3 risks?» then refine. |
| §12 Glossary | 0 | Auto-extracted. |

**Total target: 8-20 questions across the whole pass.** Above 25 is fatigue territory — bundle harder (one question per *uncertainty*, not per *parameter*). The depth dial scales this further (easy asks fewer; hard walks every decision) → [`../../_shared/interview-depth.md`](../../_shared/interview-depth.md).

## Pre-Socratic hygiene

Before handing the in-memory draft to the Step 6 batch loop, the skill must self-check (the critic is the second backstop):

- §1 Stakeholders + §3 actors use CONTEXT glossary roles verbatim (no inventing `user`/`admin` if glossary defines specific roles).
- §2 Constraints reflect the map/scan (no contradicting the repo's conventions without an explicit Override note pointing at §11).
- §3 + §5 Mermaid blocks declare all elements before `Rel` lines (no dangling references; no `Container_Bondary` typos).
- §10 numeric targets cite PRD §6 NFR row exactly (no inventing numbers; no rounding `≤ 250ms` to `≤ 300ms`).
- §6 sequence diagrams reference participants from §5 Container view by name.
- §11 includes at least one row sourced from the map/scan-reported brownfield gotchas (or `<!-- N/A: greenfield -->` if applicable).

A hygiene failure regenerates the offending section in-memory before Step 6. The Step-7 critic (see [critic-phase.md](./critic-phase.md)) is the second backstop — pre-Socratic hygiene is the first.
