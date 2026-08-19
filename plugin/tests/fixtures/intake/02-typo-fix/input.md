# Fixture: intake / 02-typo-fix

## Scenario

XS feature (typo fix у error message). Очікується що skill **не** дублює MP-check, **не** створює ADR, **не** створює CONTEXT (немає domain terms).

## Pre-existing

(Нічого.)

## User input

```
/sdlc-intake fix-typo-in-429-message

Typo у error message: «Too Many Reqests» → «Too Many Requests». 1 PR, до 1 дня.
Без міграцій, без новий API, без breaking changes.
```

## Expected behavior

- §A: створює `idea-brief.md` зі Problem (typo), Users (всі), Out-of-scope (всі інші error messages), Size=XS, Competitors=N/A (internal), RICE (low), Feasibility 3/3.
- §B: **skip** — немає domain terms. Зустрічає тільки «typo», «error message» — generic.
- §C: створює `brainstorm.md` з мінімальним set (3 approaches: hotfix / wait next release / batch з іншими typo fixes). Recommendation = hotfix.
- §D: MP-check — hard-to-reverse=FAIL (1-line PR, ревертом). Skill **не пропонує ADR**, прозоро повідомляє: «recommendation у brainstorm, ADR не потрібен — легко переграти (1-line change)».
- §E: **skip** (D failed).
- §F: один commit `01-02: intake for fix-typo-in-429-message (idea-brief + brainstorm)`.
- §G: пропонує `sdlc:classify-size` (буде XS).

## Expected files

```
delivery/fix-typo-in-429-message/
├── idea-brief.md        # XS, RICE low, Feasibility 3/3
└── brainstorm.md        # 3 approaches, recommendation = hotfix, no **Locked in:** line
```

NO `CONTEXT.md`, NO `adr/` directory.

## Score against rubric.md

D1: only 2 files. No CONTEXT.md, no adr/. ✅ якщо expected diff clean.
D2: intake DoD met; propose-adr correctly REFUSED з reason.
D3: skill not creating ADR на тривіальне (anti-pattern avoided).
D4: commit без ADR-NNNN/CONTEXT bracketed parts.

## Why this catches a regression

Якщо skill створив ADR на typo fix → MP-threshold broken. Catch заранo.
