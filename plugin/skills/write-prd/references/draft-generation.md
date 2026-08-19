# Draft generation — per-section contract for write-prd Protocol step 6

The authoritative format for each section is the `<!-- Skill instruction: ... -->` comment in [`../templates/PRD-template.md`](../templates/PRD-template.md). This file is the operational glue: where content comes from and what is forbidden.

## Inputs in priority order

1. **`CONTEXT.md` `## Glossary`** — canonical for role names + domain terms. If anything contradicts it, the glossary wins.
2. **`idea-brief.md`** — sections §2 Problem, §3 Users, §6 Out of scope, §11 RICE, §13 Recommendation.
3. **`docs/architecture-map.md`** (if present, from `map-architecture`) — informs §1 Context, §2 constraints, and §3 Non-goals (what the existing system already handles / structurally can't do). Do **not** leak map tech into §5 AC — AC stay business-observable.
4. **Channel outputs from step 5** — reference-module patterns (entity types, error sentinels, status constants, authz checks), MCP-Atlassian quotes, project docs, RAG hits → §1 ¶4 traceability only.

## Per-section sources

- **§1 Context** — 3-4 paragraphs. ¶1 from idea-brief §2 Problem. ¶2 from idea-brief «Why now» / triggers. ¶3 from idea-brief §13 Recommendation (cite directly — 1-2 sentences, the committed approach). ¶4 (optional) reference patterns + MCP/docs/RAG quotes as **traceability context** — and the slot where critic `Override` resolutions emit «Decision override: <headline> — rationale: <reason>» bullets. This section is WHAT + WHY, not HOW. Do NOT name a concrete datastore / broker / framework / library here — those belong to `architecture-design`.
- **§2 Goals** — 2-3 measurable strategic outcomes as a bullet list. Each is a manifestation of the committed approach (§1 ¶3). No raw numbers here — numbers live in §7 KPIs.
- **§3 Non-goals** — 3-4 explicit non-goals, each one sentence + a reason. Source: idea-brief §6 Out of scope. Keeps scope honest.
- **§4 User stories** — ≥5 US (no upper cap) in `As a <role> / I want / So that` form. Skill proposes as many as needed to cover all roles from CONTEXT glossary + all goals from §2. Roles **only** from CONTEXT glossary (no `user`/`admin` invented if the glossary defines specific roles).
- **§5 Acceptance criteria** — see the §5 AC contract below.
- **§6 NFR table** — recommended-list rows with numeric targets. No «fast»/«reliable»/«high». Measurement = concrete production metric name. TBD allowed only with owner + due tied to a row in §8.
- **§6.1 Security / privacy** — data classification, personal data touched, authZ/authN impact (surface-neutral — no endpoint/route language; `architecture-design` derives the surfaces), **3-5 abuse cases** (cross-tenant access, draft-leak, injection through URL/text fields, spam-create with rate limit, optional token misuse — each with the business response), security review verdict.
- **§7 Metrics / KPIs** — ≥3 metrics (no upper cap), baseline → target with timeframe. baseline=0 OK for new feature; baseline=TBD requires a measurement plan inline.
- **§8 Open questions** — 2-4 entries, each with owner + due (date or stage trigger). Format: `- [ ] <question>? Default now: <X>. — owner: <name/role>, due: <date or stage>`.

## §5 acceptance-criteria contract

AC describes a **business-observable outcome from the actor's perspective**, in Given/When/Then. **No upper cap** — propose as many as needed so **every §4 user story has at least one AC** and all five coverage types appear. If a `Drop` / `Save as Open Question` during Socratic leaves a coverage type empty **or a retained §4 user story with no AC**, regenerate a replacement AC and run a mini-batch on it (the two coverage floors — see [`socratic-loop.md`](./socratic-loop.md)). The «every US has at least one AC» rule is a **re-checked floor**, not only a draft-time target — it is verified after every §5 resolution, so `complete-sequence-diagrams` and `review-feature` downstream can rely on each use-case having a testable criterion.

Five coverage types, at least one each:

1. **happy** — actor does the main flow → system records the outcome and confirms.
2. **error** — actor submits invalid input → system blocks it and explains the reason (phrase as «system shows the actor that <field> must be <constraint>»; no HTTP code, no error-code string).
3. **authorization** — actor lacks permission (cross-tenant / cross-role / not-owner) → system denies access or hides existence; rationale in business terms (no `403`/`404`).
4. **domain invariant** — actor violates a named invariant → system blocks the action and names the invariant in plain language (no error-code-string, no `409`).
5. **cross-context** — actor's action depends on state in another bounded context → system enforces the cross-context rule.

## Forbidden tokens in §5 AC (stack-agnostic, zero tolerance)

Checked by the critic's F6 and the pre-write regex scan:

- **HTTP verbs**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- **URL paths**: anything starting with `/` then a lowercase identifier (`/orders`, `/items/{id}`, `/api/v1/...`).
- **status-code numerics** in the AC body: `200`, `201`, `400`, `401`, `403`, `404`, `409`, `5xx`, `500`, `503`.
- **error-code strings** matching `[a-z_]+\.[a-z_]+` (e.g. `order.not_owner`, `validation.title_too_long`).
- **JSON fragments / payload bodies**: `{title, description}`, `{id, status: "draft"}`.
- **SQL / DB constructs**: `UNIQUE(...)`, `FK`, raw `INSERT`/`SELECT`/`UPDATE`, constraint names — and any **driver/ORM-specific error type** (e.g. `pq.*`, `sqlalchemy.*`).

The technical mapping for all of these lives in `api-forge` (HTTP method/path/status, error-code strings, payload schemas) and `generate-data-model` / `decide-adr` (DB constructs). The PRD's AC is WHAT a user can observe, not HOW the system encodes it.

## Stack-agnostic hygiene for §1-§3

The product-level sections must not name a **concrete technology** — a specific datastore, message broker, framework, or library. Flag any proper-noun product/library name in the WHAT/WHY sections and move it to the `architecture-design` stage.

## Pre-write hygiene (before Socratic)

- §4 US roles use CONTEXT glossary terms verbatim.
- §3 Non-goals each carry a reason (no inventing).
- §1 ¶3 cites idea-brief §13 Recommendation verbatim or paraphrases without losing the vector.
- **§5 has at least one of each coverage type, at least one AC per §4 US, and 0 forbidden tokens** (self-scan; the critic + regex are the backstop).
