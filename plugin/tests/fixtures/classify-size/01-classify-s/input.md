# Fixture: classify-size / 01-classify-s

## Scenario

Feature на межі XS/S: 1 API endpoint + 1 тиждень + internal-only breaking. Очікується класифікація як `S`.

## Pre-existing

```
delivery/rate-limit-headers/idea-brief.md
```

idea-brief має §Rough size = `S` (як hint, not authoritative).

## User input

```
/sdlc-classify-size rate-limit-headers
```

## Expected behavior

1. Skill reads idea-brief.md §Rough size = `S` (starting hint).
2. `.size` файлу не існує → continue.
3. Q1 PR count: user → `2-5 PR`.
4. Q2 time: user → `1 тиждень`.
5. Q3 new module/API/migration: user → `Так, один з трьох` (1 новий header у API).
6. Q4 breaking changes: user → `Так, internal only`.
7. Classify → `S` (matches: 2-5 PR + 1 тиждень + 1 з 3 + internal).
8. Skill confirms: «Класифікую як `S`. Зафіксувати?» User: «Так».
9. Write `delivery/rate-limit-headers/.size` → `S` (single line, no trailing newline issues).
10. PRD.md не існує → skip sync.
11. Commit `size: rate-limit-headers classified as S`.

## Expected files

```
delivery/rate-limit-headers/
├── idea-brief.md   # UNCHANGED
└── .size           # NEW — single line: S
```

## Score against rubric.md

D1: `.size` файл існує, одна літера `S`.
D2: all 4 questions asked; user confirm; not silent write.
D3: `.size` is one-liner (no frontmatter, no comments).
D4: commit prefix `size:`, slug + size відповідні.

## Edge case caught

Якщо skill автомагічно класифікує і пише без AskUserQuestion → catches silent-classify regression.
Якщо skill пише `S\n\n` або multi-line → wrappers grep-логіка фейлить.
