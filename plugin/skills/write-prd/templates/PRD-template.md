---
status: Draft
owner: "<feature owner>"
reviewers: ["Tech Lead", "Security Lead"]
updated_at: "<today YYYY-MM-DD>"
feature_size: "<from .size: XS/S/M/L/XL>"
stage: "03"
ticket: "<TBD>"
---

# PRD — <slug>

<!-- Skill instruction: one-line links to inputs used.
> **Inputs (required):** [idea-brief](./idea-brief.md) · [CONTEXT](./CONTEXT.md)
> **Reference module:** `internal/modules/<name>` — code patterns used (error codes, authz, status transitions). If --reference not passed or user declined — write «N/A — green-field mode».
> **External context channels used:** list selected channels from step-4 AskUserQuestion: «MCP-Atlassian: Confluence page "X", Jira ticket Y-123», «Project docs: docs/architecture/auth.md», «architecture-map: docs/architecture-map.md», or «None — only CONTEXT + idea-brief».
Do not mention brainstorm or initiatives artifacts — they are not PRD inputs. -->

## 1. Context

<!-- Skill instruction: 3-4 paragraphs.
¶1 What we're solving — the concrete problem from the interview (idea-brief §2 Problem), for whom (cite user segment from §3 Users).
¶2 Why now — the trigger from idea-brief (incident, contract, deadline, strategic shift).
¶3 The committed approach — 1-2 sentences, from idea-brief §13 Recommendation. For M+/L this is the recommendation from the ideation pass; for XS/S it is the obvious direction from the deep-dive.
¶4 (optional) Traceability context — reference-module patterns or quoted sources (architecture-map §, MCP/doc quotes), AND the slot where critic `Override` resolutions emit «Decision override: <headline> — rationale: <reason>» bullets.
This section is WHAT + WHY, not HOW. Do NOT name a concrete datastore / broker / framework / library here — that belongs to architecture-design. -->

## 2. Goals

<!-- Skill instruction: 2-3 measurable strategic outcomes as a bullet list.
Each is a manifestation of the committed approach (§1 ¶3). Cite idea-brief §13 directly.
No raw numbers here — numbers live in §7 KPIs. Here — strategic outcome.

Example:
- Editor publishes an article in one click, without manual checking whether sections are non-empty (validation on the backend).
- Editor sees all drafts for their team in a single list. -->

## 3. Non-goals

<!-- Skill instruction: 3-4 explicit non-goals, each one sentence + a reason.
Source: idea-brief §6 Out of scope. No references to parked initiatives — source only idea-brief §6.

Example:
- Deleting a published article — deferred to v2 via archiving, because it cannot be safely deleted with active downstream links.
- Cross-team portability — out of scope, each team has isolated articles. -->

## 4. User stories

<!-- Skill instruction: at least 5 user stories, no upper cap. Skill proposes as many as needed to cover all roles from CONTEXT glossary + all goals from §2. Format:

### US-NN: <3-6 word action title>
**As a** <role from CONTEXT glossary>
**I want** <action>
**So that** <observable benefit>

Roles ONLY from the glossary (no invented `user`/`admin`). Title is 3-6 words describing the action, not the entity («Publish a course version», not «Course publishing»).
Each US is covered by at least one AC in §5. -->

### US-01: <title>

**As a** <role>
**I want** <action>
**So that** <benefit>

### US-02: <title>

**As a** <role>
**I want** <action>
**So that** <benefit>

## 5. Acceptance criteria

<!-- Skill instruction: at least one AC of EACH of the 5 coverage types (happy / error / authorization / domain invariant / cross-context), no upper cap. Skill proposes as many as needed so all US are covered by at least one AC. Format:

### AC-NN (US-XX) — <coverage type>
**Given** <business preconditions: actor role, state of their domain objects, prior events>
**When** <business action from the actor's perspective>
**Then** <observable business outcome: actor sees X / system blocks Y and explains Z / system records W>

AC = business-observable outcome from the actor's perspective. NOT how the system does it.

FORBIDDEN in AC text (zero tolerance — critic F6 + pre-write regex):
- HTTP verbs (GET/POST/PUT/PATCH/DELETE)
- URL paths (/courses, /lessons/{id}, /api/v1/...)
- status-code numerics in the body (200/201/400/401/403/404/409/5xx)
- error-code strings matching `[a-z_]+\.[a-z_]+` (e.g. order.not_owner)
- JSON fragments / payload bodies ({field: "value"})
- SQL / DB constructs (UNIQUE, FK, raw INSERT/SELECT/UPDATE, constraint names, driver/ORM error types)
The technical mapping for these lives in `api-forge` + `decide-adr`. Here: only what the actor observes.

Allowed: glossary roles, domain-invariant NAMES as natural-language phrases («no published lessons», «unique sequence per course»), glossary domain objects.

The 5 mandatory coverage types (at least 1 each):
1. happy — actor does the main flow → system records the outcome and confirms.
2. error — actor submits invalid input → system blocks it and explains the reason in plain language.
3. authorization — actor lacks permission → system denies access OR hides existence (rationale in business terms).
4. domain invariant — actor violates a named invariant → system blocks and names the invariant plainly.
5. cross-context — actor's action depends on state in another bounded context → system enforces the cross-context rule.

Tag each AC with its US-NN. Concurrent edge → add as AC-NNb, still in business language. -->

### AC-01 (US-01) — happy path

**Given** an authorized <role> owns a draft <domain-object>
**When** the <role> attempts to publish the <domain-object>
**Then** the system records the <domain-object> as published and confirms to the <role>

### AC-02 (US-01) — domain invariant violation

**Given** an authorized <role> owns a draft <domain-object> with no child <sub-objects>
**When** the <role> attempts to publish the <domain-object>
**Then** the system blocks the publication and tells the <role> that at least one <sub-object> must be published first

## 6. Non-functional requirements

<!-- Skill instruction: table, recommended floor (not a cap). Targets are NUMERIC (≤250ms, ≥30 req/s, 99.9%) — no adjectives («fast», «high»). Measurement = a concrete production metric. Unknown number → TBD with owner+due in §8, never «fast». -->

| Aspect | Target | Measurement |
|---|---|---|
| Latency p95 <write operation> | ≤ <N ms> | <metric source> |
| Latency p95 <read/list operation> | ≤ <N ms> | <metric source> |
| Throughput | ≥ <N req/s> per instance | smoke test in CI |
| Availability | 99.X% | monthly SLO window |
| <Concurrency / Accuracy> | <safety guarantee> | <how enforced> |

## 6.1 Security / privacy

<!-- Skill instruction:
- Data classification: public / internal / confidential / regulated (one word + 1-sentence rationale).
- Personal data touched: none, OR list new fields with type + sensitivity.
- AuthZ/AuthN impact: which capabilities / permission checks are added. Stay surface-neutral — no endpoint/route language; `architecture-design` derives the surfaces.
- Abuse cases (3-5): cross-tenant access, draft/data leak, injection through URL/text fields, spam-create with a rate limit, optional token misuse — each with the business response (deny vs hide-existence; rationale, not status codes).
- Security review verdict: Required (M+ / new authz boundary / new PII) or N/A with a concrete reason. -->

- **Data classification:** <...>
- **Personal data touched:** <...>
- **AuthZ/AuthN impact:** <...>
- **Abuse cases:**
  - <cross-tenant>: <business response>
  - <data-leak>: <how hidden>
  - <spam>: rate limit <N per minute per user>
- **Security review:** <Required / N/A with reason>

## 7. Metrics / KPIs

<!-- Skill instruction: at least 3 KPIs, no upper cap, each baseline → target with a timeframe.
Skill proposes as many as RICE drivers from idea-brief §11 + Recommendation §13.
baseline=0 OK for a new feature. baseline=TBD requires a measurement plan inline.

What to include:
- Adoption rate — share of active users who completed the target action within 30 days.
- Engagement uplift / retention — return-to-feature rate in a cohort with at least N uses.
- Quality / accuracy — error rate, drift, retry count (feature-specific).
- Latency p95 — as in NFR (repeated here as a KPI for post-release tracking). -->

- **<metric 1>** — baseline: <...>, target: <... within ... days>.
- **<metric 2>** — baseline: <...>, target: <...>.
- **<metric 3>** — baseline: <...>, target: <...>.

## 8. Open questions

<!-- Skill instruction: 2-4 open questions from `save_as_oq` resolutions in step 7 + any un-resolved questions from the interview. Format:

`- [ ] <question>? Default now: <X>. — owner: <name/role>, due: <YYYY-MM-DD or stage trigger like "before /sdlc-break-tasks">`

Every question has owner + due — a lone «TBD» without both is an anti-pattern (downgraded to Drop if either is missing). The skill MUST ask for owner + due immediately after the user picks Save-as-OQ. -->

- [ ] <question>? Default now: <...>. — owner: <name/role>, due: <date or stage>
- [ ] <question>? — owner: <name/role>, due: <date or stage>
