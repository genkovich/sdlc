# Fixture: intake / 01-rate-limit

## Scenario

Full intake flow на rate-limiting feature. Очікується що skill пройде §A interview → §B inline CONTEXT (для «tenant») → §C brainstorm → §D MP-check (PASS) → §E ADR stub.

## Pre-existing

(Нічого — clean start.)

## User input

```
/sdlc-intake rate-limiting-per-user

Контекст: 3 клієнти за тиждень поскаржилися на 429 від інших користувачів.
Один користувач шле 10k req/min і кладе rate limit на всіх. Клієнти — B2B
на shared infra, contract обіцяє per-tenant SLA.

Розмір: S (один тиждень, 2-5 PRs).

Domain hint: ми оперуємо «tenant» (billable customer org з 1+ users —
NOT user). У brainstorm розглянь: Redis token bucket vs Nginx limit_req_zone
vs Envoy ratelimit (3 finalists). Recommendation очікую — Redis token bucket
(Redis уже є, бібліотека зріла).
```

## Expected behavior

- §A: створює `delivery/rate-limiting-per-user/idea-brief.md` з Problem/Users/Why now/Out of scope/Size (S)/Competitors (Kong, Tyk, AWS API Gateway)/RICE (~240)/Feasibility (3/3).
- §B: під час §A зустрічає «tenant» → проактивно пропонує `sdlc:fix-term tenant`. Skill створює root `CONTEXT.md` з `tenant — billable customer org з 1+ users. NOT user.`
- §C: створює `brainstorm.md` з 5-7 approaches, 3 finalists, recommendation = Redis token bucket.
- §D: MP-check — hard-to-reverse=PASS (≥3 days), surprising=PASS (Nginx alternative), real-trade-off=PASS (3 finalists). User confirms ADR creation.
- §E: створює `adr/0001-token-bucket-with-redis.md` зі Status=Proposed. Backlink у brainstorm.md.
- §F: один commit `01-02: intake for rate-limiting-per-user (idea-brief + brainstorm + ADR-0001 + CONTEXT)`.
- §G: пропонує `sdlc:classify-size`.

## Expected files

```
delivery/rate-limiting-per-user/
├── idea-brief.md        # DoD §1: Problem/Users/Competitors/RICE=240/Feasibility 3/3
├── brainstorm.md        # 3 finalists, recommendation, **Locked in:** [[adr/0001-...]]
└── adr/
    └── 0001-token-bucket-with-redis.md   # Status=Proposed
CONTEXT.md              # ## Glossary: - tenant — ...
```

## Score against rubric.md

D1: 5 files exist, no extras.
D2: usі DoDs intake + fix-term + propose-adr met.
D3: no inline MP-check duplication у intake; ADR title описує рішення, не проблему.
D4: commit message має правильний префікс `01-02:` + повний list файлів.
