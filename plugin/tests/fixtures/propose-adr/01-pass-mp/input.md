# Fixture: propose-adr / 01-pass-mp

## Scenario

Recommendation що проходить усі 3 MP checks (PASS). Очікується ADR stub зі Status=Proposed + backlink.

## Pre-existing

```
delivery/rate-limit-test/brainstorm.md
```

Зміст `brainstorm.md` (фрагмент):

```markdown
# Brainstorm — rate-limit-test

## Context
Per-tenant rate limit для B2B platform.

## Options

### Redis token bucket
Pros: Redis existing, INCR+EXPIRE простий.
Cons: SPOF якщо Redis down.

### Nginx limit_req_zone
Pros: nginx existing.
Cons: zone-key — не tenant.

### Envoy ratelimit
Pros: dedicated service.
Cons: ще один компонент.

## Recommendation
Redis token bucket — Redis уже є, найдешевший integration.
```

## User input

```
/sdlc-propose-adr rate-limit-test

Recommendation з brainstorm — Redis token bucket. Хочу зафіксувати ADR.
```

## Expected behavior

1. Skill reads brainstorm.md, extracts recommendation і options.
2. Q1 hard-to-reverse: `≥ 3 days` (зміна сховища). PASS.
3. Q2 surprising in 6 months: `Так — non-obvious, nginx existing` (PASS).
4. Q3 real trade-off: програмний check finds ≥3 finalists (Redis / Nginx / Envoy). PASS.
5. Threshold gate: 3/3 PASS → confirm.
6. User confirms creation.
7. Compute NNNN=0001, title=`token-bucket-with-redis`.
8. Copy template → `delivery/rate-limit-test/adr/0001-token-bucket-with-redis.md`. Pre-fill.
9. Add `**Locked in:** [[adr/0001-token-bucket-with-redis]] (status=Proposed)` after §Recommendation in brainstorm.md.
10. Commit `11-proposed: ADR 0001 token-bucket-with-redis for rate-limit-test (Proposed)`.

## Expected files

```
delivery/rate-limit-test/
├── brainstorm.md                      # MODIFIED — adds **Locked in:** line
└── adr/
    └── 0001-token-bucket-with-redis.md   # NEW — Status: Proposed
```

## Score against rubric.md

D1: ADR file existstwith expected name; brainstorm.md modified (`**Locked in:**` line added).
D2: propose-adr DoD met — all 3 MP-checks PASS, Status=Proposed, backlink in brainstorm.
D3: title описує рішення (`token-bucket-with-redis`), не проблему (`rate-limiting`).
D4: commit prefix `11-proposed:`, ADR number 0001, title kebab-case.
