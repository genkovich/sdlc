# Fixture: propose-adr / 02-fail-mp

## Scenario

Recommendation що **fail** MP-check (легко-reversible вибір між двома HTTP-клієнтами з ідентичним API). Очікується REFUSAL з прозорою причиною, без створення ADR.

## Pre-existing

```
delivery/http-client-pick/brainstorm.md
```

Зміст (фрагмент):

```markdown
# Brainstorm — http-client-pick

## Options

### `requests` Python library
Pros: industry standard, добре документований.
Cons: blocking.

### `httpx` Python library
Pros: async + sync API, modern.
Cons: трохи новіший.

## Recommendation
`httpx` — async-ready на майбутнє.
```

## User input

```
/sdlc-propose-adr http-client-pick

Recommendation — httpx. Чи варто ADR?
```

## Expected behavior

1. Skill reads brainstorm.md.
2. Q1 hard-to-reverse: `< 1 day` (бібліотека swap з ідентичним API). FAIL.
3. Threshold gate: ≥1 FAIL → STOP.
4. Skill explanation: «Recommendation `httpx` зафіксований у brainstorm.md. ADR не потрібен — легко переграти (бібліотека з ідентичним API, < 1 day rework).»
5. NO ADR створено. NO backlink у brainstorm.

## Expected files

```
delivery/http-client-pick/
└── brainstorm.md   # UNCHANGED
```

NO `adr/` directory created.

## Score against rubric.md

D1: жодних нових файлів. brainstorm unchanged.
D2: skill correctly identified FAIL і REFUSED з причиною (which criterion).
D3: skill did NOT create ADR на reversible вибір. MP-threshold protection working.
D4: NO commit пропозиція (нічого не змінено).

## Why this catches a regression

Якщо skill створив ADR — MP-threshold deflated, ADR стає шумом. Catch на ранній стадії.
