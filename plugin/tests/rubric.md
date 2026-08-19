# Eval rubric

4 quality dimensions per fixture. Pass = всі 4. Fail на будь-якому = regression caught.

## D1 — Output artefacts exist

Skill створив очікувані файли у правильних місцях.

Check:
```bash
diff -r docs/features/<slug>/ fixtures/<skill>/<scenario>/expected/
```

- Pass: усі expected files присутні з очікуваним вмістом (allow whitespace diff).
- Fail: missing file OR extra file OR major content divergence.

## D2 — DoD criteria met

Skill пройшов власну `## Definition of Done` секцію.

Check (per skill):

### intake
- [ ] `idea-brief.md` з Problem/Users/Out-of-scope/Competitors/RICE/Feasibility.
- [ ] `brainstorm.md` з ≥3 approaches, risks (prob × impact), recommendation.
- [ ] (Якщо domain terms) `CONTEXT.md` з `## Glossary`, без empty H2.
- [ ] (Якщо MP-pass) `adr/NNNN-*.md` зі Status=Proposed + backlink у brainstorm.

### propose-adr
- [ ] Усі 3 MP-check questions запитані.
- [ ] PASS path → ADR stub Status=Proposed + backlink.
- [ ] FAIL path → no ADR, refusal з reason (which criterion failed).

### classify-size
- [ ] `docs/features/<slug>/.size` створено з одним з: XS/S/M/L/XL.
- [ ] User confirmed класифікацію (не silent write).
- [ ] (Якщо PRD існує) sync з frontmatter `feature_size:`.

### prep-review
- [ ] `review-checklist.md` ≤25 пунктів.
- [ ] Кожен пункт має WHERE-context (на який файл/функцію вказує).
- [ ] Domain-relevant items (не лише "no typos").

## D3 — No anti-patterns

Skill не порушив `## Anti-patterns` секцію.

Per-skill spot-checks:

### intake
- [ ] Не дублює MP-check inline (delegує до propose-adr).
- [ ] Не дублює CONTEXT bootstrap (delegує до fix-term).
- [ ] Single commit per phase (не 3-4 окремих).

### propose-adr
- [ ] Не пропонує ADR на rejected approach.
- [ ] Status=Proposed, не Accepted (Accepted — через decide-adr).
- [ ] Title описує decision, не problem.

### classify-size
- [ ] Не silent (asks confirm).
- [ ] `.size` файл — one-liner, без frontmatter.

### prep-review
- [ ] ≤25 actionable items (не 50+).
- [ ] Domain items (не лише generic «no typos / build passes»).

## D4 — Commit message correct

Skill пропонує commit з правильним форматом.

Check:
- intake → `01-02: intake for <slug> (idea-brief + brainstorm[ + ADR-NNNN + CONTEXT])`
- propose-adr → `11-proposed: ADR NNNN <title> for <slug> (Proposed)`
- classify-size → `size: <slug> classified as <X>` (або як частина intake commit)
- prep-review → `16: review-checklist for <slug>`

Pass: format matches (allow minor punctuation drift).
Fail: wrong stage prefix, missing slug, або skill пропонує git push (anti-pattern — лише propose, не execute).

## Aggregate score

| D1 | D2 | D3 | D4 | Result |
|:--:|:--:|:--:|:--:|--------|
| ✅ | ✅ | ✅ | ✅ | PASS — fixture green |
| any | ✅ | any | any | PARTIAL — investigate |
| any | ❌ | any | any | FAIL — regression caught |

D2 is the most important: DoD criteria define correctness. D1 catches missing files; D3 catches subjective drift; D4 catches integration breakage.

## Logging

Manual run results — у git commit message при додаванні fixture або у Issue, якщо caught regression. Не зберігай результати в repo (vary per session).
