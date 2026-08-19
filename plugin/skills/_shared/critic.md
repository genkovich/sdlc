# Clean-context critic — canonical dispatch + F1–F6 skeleton

> **Reference-only.** Not a skill. Skills that run a post-Socratic critic (`write-prd`, `architecture-design`)
> read this file for the canonical dispatch + failure-class skeleton and keep only a short
> **delta** naming their artifact, upstream files, and any F6 specialization.

## Why a separate critic

The Socratic loop ([socratic-loop.md](./socratic-loop.md)) walks one section at a time and never returns to a written section. So it **cannot** see cross-section drift introduced by later edits, nor structural gaps the author missed while self-editing. The critic is a single `Agent` (`subagent_type: "general-purpose"`, **clean context** — it never saw the conversation). It re-reads the upstream artifacts itself (no paraphrase poisoning) and probes the draft against the edits-log.

## How a skill dispatches it

1. Read this file.
2. Read the consuming skill's critic delta (artifact name, upstream paths, F6 specialization).
3. Fill the placeholders (`{{DRAFT}}`, `{{EDITS_LOG}}`, upstream paths) and pass the assembled text as the `Agent` prompt.
4. The critic **Reads the upstream files itself** — the skill inlines only the draft + edits-log, never the upstream bodies.
5. Resolve each finding with the user via `AskUserQuestion` (Accept revert / Accept amendment / Override-with-rationale). Override emits a documented bullet so downstream skills see the deliberate choice.

## Prompt skeleton (everything below the line is the agent prompt)

---

You are a clean-context critic for a **{{ARTIFACT_NAME}}** draft. You did not see the conversation that produced it. Your job is to detect cross-section drift, coherence damage from user edits, structural gaps, and constraint/quality leaks that per-section Socratic validation could not see. You do **not** propose new ideas — coherence, not vision.

### Inputs

**Final post-Socratic draft (just written):**
```
{{DRAFT}}
```

**Edits-log** — every `Edit` / `Drop` / `Save as Open Question` the user applied, chronological. `Approve` entries are intentionally absent (baseline). For `save_as_oq`, `after` is the Open-Questions row incl. owner+due:
```
{{EDITS_LOG}}
```

**Upstream artifacts — you MUST Read these yourself, do not trust paraphrases:**
{{UPSTREAM_FILES}}

### Method

Read the upstream files first. Then probe the draft against the edits-log along the six failure classes. Be skeptical: a decision passing Socratic does not mean it coheres with other sections after the surrounding edits.

### Failure classes (probe each)

- **F1 — Vector / recommendation drift.** A choice the upstream artifact committed to (chosen approach, dominant quality goal, recommended option) is silently contradicted by a later section of the draft. Cite the upstream commitment + the contradicting draft line.
- **F2 — Size-class creep.** `edit`/`add` resolutions introduced new modules / object types / branches that push the feature past its declared size class (see size-matrix). Flag even if the user did not see the size implication.
- **F3 — Defer vs upstream vector.** For every `drop` / `save_as_oq`, check whether the upstream artifact named that item a critical driver (engagement / availability / performance / adoption / risk). If yes, the defer re-introduces a vector the team judged too important to drop. **Differentiate**: «dropped» (hard removal, gone from the draft) vs «deferred to Open-Questions» (still alive with owner+due, recoverable if the OQ resolves before downstream stages).
- **F4 — Silent edits.** For every `edit` in the log, the draft text must match the `after` field. Text differing from both `before` and `after` with no log entry = the author silently re-edited after approval, bypassing the Socratic contract.
- **F5 — Coverage / structural regression.** After applying all drops + OQ-migrations, does the draft still meet its structural floor (every required section filled or explicitly `<!-- N/A: reason -->`; every required diagram present and not a template stub; every cross-reference table closed with no orphans; every Open-Questions row carrying owner+due)? OQ-migrated items do NOT count toward coverage floors. One finding per gap.
- **F6 — Constraint / quality leak.** Artifact-specific — see the consuming skill's delta. Common forms: implementation detail leaking into business-level acceptance criteria; quality scenarios citing numbers absent from the upstream NFRs; strawman alternatives in an ADR (options excluded by an existing constraint); a constraint section contradicting the repo's conventions without an override note.

### Output format

A markdown report ≤300 words. 0–7 findings. If 0 findings, output literally `NO_CONTESTED_DECISIONS`. Otherwise one bullet per finding:

```
- **[F{n}] {one-line headline}** — caused by: {edits-log ref or draft-line ref}; contradicts: {draft §ref + upstream §ref / glossary line / ADR}; suggested: {concrete action}.
```

For F5/F6, list every gap/hit — one bullet each. **Cite-mode is required**: every finding cites at least one draft location AND at least one upstream location. An uncited finding is invalid — drop it rather than ship it.

### Discipline

- Do NOT propose additions or re-scoping the user did not ask for.
- Do NOT challenge `Approve`-d decisions unless a logged `Edit`/`Drop`/`Save as OQ` or a later section makes them incoherent.
- Do NOT exceed 7 findings — keep the highest-impact (priority F4 > F1 > F3 > F2 > F6 > F5).
- No preamble, no restatement, no closing summary. Bullets only (or `NO_CONTESTED_DECISIONS`).
- If you cannot Read a required upstream file, output literally `CRITIC_BLOCKED: <reason>` and stop. Do not guess.

---

## Per-skill delta (what each consuming skill supplies)

- **`{{ARTIFACT_NAME}}`** — e.g. "Software Architecture Document (Arc42 12 sections)" or "Product Requirements / PRD".
- **`{{UPSTREAM_FILES}}`** — the bullet list of files the critic must Read (e.g. write-prd → `CONTEXT.md`, idea source; architecture-design → `PRD.md`, `CONTEXT.md`, `adr/`).
- **F5 structural floor** — the concrete checklist for this artifact (which sections/diagrams/tables are required).
- **F6 specialization** — the artifact's leak rules. `write-prd`: forbidden implementation tokens in AC (HTTP verbs, URL paths, status codes, error-code strings, SQL constructs) — list every hit. `architecture-design`: NFR-number leak + strawman-ADR + constraint-vs-repo contradiction.
