# api-forge — drift check, report shape, reconcile, conflicts

The contract is a **derived** artifact: `data-model.md` (typed shape) + `sad.md` §6 sequences
(error branches, async actors) + `PRD.md` §4/§5 (endpoint list, observable outcomes) → OpenAPI.
This file is the operational detail for step 7 of the spine — what the report holds and what
each drift point compares. The spine ([`../SKILL.md`](../SKILL.md)) is the source of truth for
when this runs.

## `api-sync-report.md` shape

Written to `docs/features/<slug>/contracts/api-sync-report.md` next to the YAML. Three sections.

### Section A — field-origins table

One row per `(operation, schema_field)` pair, so every field in the contract is traceable:

```
| schema_path                | origin                                  | confidence |
|----------------------------|-----------------------------------------|------------|
| createLesson.title         | data-model.md → lesson.title (≤200)     | high       |
| createLesson.module_id     | data-model.md → lesson.module_id (FK)   | high       |
| listLessons.next_cursor    | derived (cursor wrapper convention)     | high       |
| publishLesson.published_at | inferred from PRD §5 AC-4, no column    | low        |
```

- **high** — field maps to a `data-model.md` column with a matching type/constraint.
- **medium** — field derived from a PRD field name with no column yet (e.g. a computed/response-only field).
- **low** — field inferred from a sequence message name only; flag it for confirmation.

A `low` row is **declared incompleteness**, not an error — it tells the team what `--reconcile`
will tighten when the model gains that column. Never hide it.

### Section B — drift findings (4-point checklist)

Each point is ✓ or ✗ with a one-line diagnostic on ✗.

1. **Endpoint ↔ data-model** *(core)* — every endpoint reads/writes ≥1 entity in `data-model.md`
   (e.g. `POST /lessons/{id}/publish` mutates `lesson.status`). In scenario B (data-model absent),
   fall back to: every endpoint maps to a PRD §4 user story.
2. **Error code ↔ repo error definition** *(core)* — every `code` in an `Error` response exists in
   the repo's error definitions, **checked in the form the repo uses**. Detect that form first —
   a constants/enum file, an error registry, a sentinel module, a generated table — and match
   against it; do **not** assume any one language or a Go-style `domain/errors.go`. If the repo
   has no central error list yet, record "no error registry found — codes are the contract's
   proposal; reconcile when the repo defines them" rather than failing the point.
3. **Validation ↔ constraint** *(core)* — `maxLength` / `pattern` / `enum` in the contract align
   with the bounded types and uniqueness/format constraints in `data-model.md`. Scenario B:
   record "deferred to reconcile — no data-model.md yet". On a conflict, take the **stricter**
   value and flag both — the human resolves which artifact is wrong.
4. **OpenAPI ↔ sequence** *(supporting)* — the methods, paths, and outcome branches the §6
   sequences imply match the contract. Mismatch usually means a sequence was drawn before the
   contract was finalized and never updated. Because §6 participants are generic
   (`<client>`/`<service>`/`<data-store>`), match on the **flow and its `alt`-branches**, not on
   participant names — a branch like `alt not owner` must have a corresponding error response.

A **core** point (1–3) failing — or **≥3 flags** of any kind in one run — pauses the run and is
surfaced to the user before writing. **Supporting** point (4) failing becomes a follow-up note in
the report. Resolve each finding via the 4-state actions:

- **Accept as is** — record the mismatch as accepted (e.g. an intentionally internal entity with
  no endpoint), move on.
- **Fix the contract** — regenerate the affected operation/schema to match the source.
- **Save as Open Question** — park it with owner + due; the field/endpoint stays with a
  `# unresolved` note until answered.
- **Fix the source first** — STOP; the contract waits for the user to correct `data-model.md` /
  the sequence / the PRD (this skill never edits sources).

### Section C — unresolved_origins

Empty in scenario A. In scenario B — list of fields whose origin is "inferred from PRD/sequence,
needs confirmation when data-model.md arrives". Each entry: `schema_path | current origin | what
reconcile would tighten`.

## Back-feed coverage cross-check

The drift check runs **both directions**. Beyond the 4 forward points above, check:

- Every PRD §5 AC maps to ≥1 operation/response in the contract.
- Every operation maps to a PRD §4 user story + ≥1 AC.
- Every `sad.md` §6 `alt`-branch has a corresponding response in the contract.
- Any error/authorization response the contract needs but no §6 flow shows → flag as a
  **sequence gap** (not a contract bug — a hole upstream). Offer **Fix-the-source-first**:
  re-open `/sdlc-complete-sequence-diagrams <slug>` (draw the missing branch) or
  `/sdlc-write-prd <slug>` (add the missing AC) before finalizing.

## Reconcile semantics (`--reconcile`)

Run after an upstream artifact changed — most often `data-model.md` arrived (or was tightened)
after a thinner first pass. The reconcile pass:

1. Re-reads all inputs.
2. Tightens loose types where the model now carries a constraint (a bare `string` becomes
   `string` + `maxLength`; a free field becomes an `enum`).
3. Refreshes the Section A confidence column (`low`/`medium` → `high` where a column now backs the field).
4. **Surfaces real drift** — any field that *had* an inferred origin but *now disagrees* with the
   model. This is the load-bearing output: stale incompleteness becomes either resolved or a
   genuine conflict, and the two never get confused.

`info.version` is never bumped here — the user bumps semver explicitly with a CHANGELOG line.

## Conflict table — human in the loop

| Conflict | Skill action |
|---|---|
| Field in `data-model.md` with no story in PRD covering it | Add it to the schema with a `# unused-in-prd` note in the report; ask the user. |
| A §6 sequence references a flow that maps to no endpoint | Flag `# orphan-sequence` in the report; ask (forgotten endpoint? internal job?). |
| PRD §5 constraint contradicts a `data-model.md` constraint | Take the stricter value; flag both; the human resolves which artifact is wrong. |
| Existing `openapi.yaml` has a field absent from every source | Keep it with a `# manual-addition` note; flag in the report. |
| A field disappeared from `data-model.md` | Keep it in the YAML with a `# stale` note; surface it — the human removes from the contract or restores in the model. |

If ≥3 flags appear in one run, pause, list them, and ask whether to continue or fix the sources first.

## Defaults (deviation by ADR only)

A fixed minimum, not invented per feature; an `adr/*.md` overrides any of them and the report
records "deviation by ADR-NNNN".

- OpenAPI **3.1.0** — nullability via `type: [string, null]`, never `nullable: true` (3.0 style).
- Error envelope **`{code, message, details?}`**, `code` = neutral `module.error_name` snake_case.
- **Cursor** pagination (`?after=&before=&limit=`) wrapped in `{items, has_next, has_prev, next_cursor}` — never offset.
- **URL** versioning (`/api/v1/...`) — never a `?v=2` query param.
- **BearerAuth** global; a public endpoint declares explicit `security: []`.
- `$ref` mandatory for shared schemas; placeholder data only in `example` blocks (no real PII).
