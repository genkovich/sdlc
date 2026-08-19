# Fixture: intake / 03-multi-context

## Scenario

Multi-context repo з `CONTEXT-MAP.md`. Очікується що `fix-term` спитає в якому context фіксувати, і пише у відповідний `<ctx>/CONTEXT.md`, не корінь.

## Pre-existing

Place перед запуском:
```
./CONTEXT-MAP.md            (with list of contexts: billing, runtime, admin)
billing/CONTEXT.md          (existing з тлумаченням `tenant — billable org`)
```

## User input

```
/sdlc-intake usage-metrics-export

Feature для export usage metrics — runtime context. Tenant runtime view
(окремо від billing tenant view).

Domain terms у grade: «usage», «tenant» (runtime — це інший view ніж billing
tenant!), «export window». Потрібен brainstorm: pull-based (cron) vs
push-based (event-driven).
```

## Expected behavior

- §A: створює `delivery/usage-metrics-export/idea-brief.md`. Detect multi-context при першому згадуванні «tenant» — спитує: «який context?» options: billing / runtime / admin. User обирає `runtime`.
- §B: викликає `sdlc:fix-term tenant --context runtime`. Skill створює `runtime/CONTEXT.md` (нове) з `tenant — runtime view of billable org (compute/quota state). NOT billing tenant (billing CONTEXT.md), NOT user.` Detects conflict з `billing/CONTEXT.md` і fixes via disambiguation.
- §C: brainstorm — pull vs push vs hybrid (3 finalists).
- §D: MP-check — recommendation «event-driven push», hard-to-reverse=PASS, surprising=PASS, finalists=PASS. ADR pass.
- §E: створює `delivery/usage-metrics-export/adr/0001-event-driven-usage-export.md`.
- §F: commit.

## Expected files

```
delivery/usage-metrics-export/
├── idea-brief.md
├── brainstorm.md
└── adr/
    └── 0001-event-driven-usage-export.md
runtime/CONTEXT.md           # NEW — runtime context, з tenant disambiguation
billing/CONTEXT.md           # UNCHANGED — already existed
```

## Score against rubric.md

D1: critical — `runtime/CONTEXT.md` створено, не корінь `CONTEXT.md`. `billing/CONTEXT.md` unchanged.
D2: fix-term DoD met (multi-context resolve + conflict-with-billing notation).
D3: no overwrite of existing `billing/CONTEXT.md`.
D4: commit має посилання на `runtime/CONTEXT.md`, не root.

## Why this catches a regression

Якщо skill пише у root `CONTEXT.md` → multi-context detection broken; reader через 6 міс плутає billing-tenant з runtime-tenant.
