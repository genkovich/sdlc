# sdlc plugin tests

Manual test fixtures для high-blast-radius skills. Без automated runner для v3.0 — кожен fixture запускається вручну і diff-иться з очікуваним output. CI-runner — backlog.

## Structure

```
tests/
├── README.md               # цей файл
├── rubric.md               # eval criteria (DoD checks per skill)
└── fixtures/
    ├── intake/
    │   ├── 01-rate-limit/   # full intake flow з ADR + CONTEXT
    │   ├── 02-typo-fix/     # XS feature — мінімальний brief
    │   └── 03-multi-context/  # multi-context repo з CONTEXT-MAP.md
    ├── propose-adr/
    │   ├── 01-pass-mp/      # 3/3 PASS → ADR stub
    │   └── 02-fail-mp/      # MP fail → refuse з reason
    ├── classify-size/
    │   └── 01-classify-s/   # M-сценарій рухається до S
    └── prep-review/
        └── 01-review-25/    # ≤25 actionable items з WHERE-context
```

Кожна fixture директорія має:
- `input.md` — user message + (опц.) pre-existing artefacts.
- `expected/` — directory з очікуваними створеними/зміненими файлами.
- `notes.md` — (опц.) ключові edge cases, що skill повинен спіймати.

## Running a fixture manually

```bash
# 1. Підготовка — copy pre-existing artefacts (якщо є)
SLUG=rate-limit-test
mkdir -p delivery/$SLUG
cp -r plugin/tests/fixtures/intake/01-rate-limit/pre-existing/* delivery/$SLUG/ 2>/dev/null

# 2. Read input.md і запусти skill
cat plugin/tests/fixtures/intake/01-rate-limit/input.md
# Open Claude Code, paste input as user message, observe behavior.

# 3. Diff output проти expected
diff -r delivery/$SLUG/ plugin/tests/fixtures/intake/01-rate-limit/expected/

# 4. Score за rubric.md
```

## Scoring per fixture

Use `rubric.md` to score:
- ✅ Output exists у `docs/features/<slug>/`.
- ✅ DoD checked (per skill's `## Definition of Done`).
- ✅ No anti-patterns triggered.
- ✅ Commit proposed correctly (right message format).

Pass = всі 4. Fail на будь-якому — fixture caught a regression.

## Adding a new fixture

1. Pick critical skill (intake / propose-adr / classify-size / prep-review).
2. Define scenario name (kebab-case, descriptive): `04-conflict-term-resolution`, `02-fail-mp-no-finalists`.
3. Create `fixtures/<skill>/<scenario>/`:
   - `input.md` — user message + (опц.) pre-existing artefacts list.
   - `expected/` — copy from manual run that you trust.
   - `notes.md` — what edge case this catches.
4. Update this README's structure tree.

## Why not automate?

Skills використовують AskUserQuestion і LLM-generation, які не deterministic. Snapshot testing вимагає mock LLM або record-replay. Backlog: explore `claude --eval` mode коли стане доступним; meanwhile manual diff достатньо для регресій критичних flow.

## Coverage

| Skill | Fixtures | High-blast-radius reason |
|-------|---------:|---------------------------|
| intake | 3 | Composite — bug у §A впливає на §B, §C, §D, §E |
| propose-adr | 2 | MP-threshold subjective → false PASS може спамити ADR-ами |
| classify-size | 1 | Wrong size → wrong skip-matrix у 4 wrappers |
| prep-review | 1 | GATE 16 — без checklist review нерівномірний |
