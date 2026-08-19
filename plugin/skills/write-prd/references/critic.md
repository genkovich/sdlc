# write-prd — delta over the shared critic

Read [`../../_shared/critic.md`](../../_shared/critic.md) for the canonical dispatch and F1–F6 skeleton. write-prd supplies only the deltas below; the skill fills the placeholders and dispatches one clean-context `Agent` via `subagent_type: "sdlc:critic"`.

## Placeholders

- **`{{ARTIFACT_NAME}}`** = "Product Requirements Document (PRD) — context / goals / user stories / acceptance criteria / NFRs / KPIs".
- **`{{DRAFT}}`** = the in-memory `PRD.md` draft (full text, post-Socratic).
- **`{{EDITS_LOG}}`** = the step-7 edits-log (every `edit | drop | add | save_as_oq` entry; `Approve` absent — it is the baseline).
- **`{{UPSTREAM_FILES}}`** (the critic Reads these itself):
  - `docs/features/<slug>/CONTEXT.md` — canonical glossary (roles, domain terms).
  - `docs/features/<slug>/idea-brief.md` — §2 Problem, §3 Users, §6 Out of scope, §11 RICE, §13 Recommendation.
  - Any reference module / doc paths the user named in step 4 (paths only, not bodies).

## Dispatch

Single `Agent` call, `subagent_type: "sdlc:critic"`, **clean context** — the critic did not see the Socratic conversation. If `sdlc:critic` is unavailable at runtime, fall back to `general-purpose` with the same prompt body.

Inline into the prompt: the full post-Socratic in-memory PRD draft + the step-7 edits-log + the upstream file paths (not bodies). The critic re-reads the upstream files itself in clean context — no paraphrase poisoning.

## F5 structural floor (this artifact)

After applying all `drop`-s and `save_as_oq`-migrations:

- §4 holds ≥1 US per glossary role + per §2 goal.
- **Every retained §4 US has ≥1 AC in §5** (use-case floor — a retained US with no AC silently breaks downstream `complete-sequence-diagrams` use-case coverage and `review-feature` end-to-end trace). OQ-migrated AC do NOT count toward this floor.
- §5 holds ≥1 AC of each of the 5 coverage types (happy / error / authorization / domain invariant / cross-context). OQ-migrated AC do NOT count.
- §6 NFR rows all carry a numeric target + measurement (no adjectives, no lone TBD).
- §8 Open Questions has a row for every `save_as_oq` with owner + due (no lone «TBD»).

## F6 specialization — forbidden-token leak (the load-bearing check)

This is write-prd's primary F6. Scan §5 AC text for the forbidden tokens in [`draft-generation.md`](./draft-generation.md) (HTTP verbs, URL paths, status numerics, `module.error_name` strings, JSON fragments, SQL/driver constructs). **List every hit**, one bullet per AC line:

```
- **[F6] AC-NN contains forbidden tokens** — line: "<verbatim snippet>"; hits: <token1>, <token2>; suggested: rewrite into business form (actor-observable outcome) OR move the HTTP/error/schema detail to `api-forge` or `decide-adr`.
```

Also flag any concrete technology name (datastore / broker / framework / library) appearing in §1–§3 — those belong to `architecture-design`.

## F1 specialization — approach drift

If the edits-log dropped/edited a US or AC tied to the committed approach in §1 ¶3, check that §1 ¶3 still states that approach accurately (cites idea-brief §13 recommendation). A PRD whose body no longer matches its own «committed approach» paragraph is drift.

## F3 specialization — defer vs idea-brief vector

For every `drop` / `save_as_oq` in the edits-log, check whether idea-brief §6 (Out of scope), §13 (Recommendation), or §11 (RICE) named that item as a critical engagement / adoption / risk driver. **Differentiate**: «dropped» (hard removal) vs «deferred to Open Questions» (softer — still alive in §8 with owner+due, recoverable if the OQ resolves before downstream stages).

## Resolution loop

For each finding, surface it via `AskUserQuestion`:

- **`Accept revert / amendment as suggested`** — apply the critic's suggested edit verbatim.
- **`Accept amendment (different wording)`** — user types alternative wording; skill applies that.
- **`Override (rationale)`** — keep the draft as-is, user provides the rationale.

Constraints:
- ≤2 `AskUserQuestion` batches, max 4 questions per batch. The user's **second** answer per finding is final.
- **`Override` resolutions emit a bullet** into the draft §1 Context ¶4: «<finding-headline> — overridden by author, rationale: <user-rationale>». This makes the deliberate choice visible to downstream skills.

After resolution, re-run the Self-check inline non-negotiables (see SKILL.md `## Definition of Done`). If any still fail — re-open the relevant `AskUserQuestion` once, then proceed.

## Pre-write regex backup for F6

Independent of the critic, before writing the file run a regex scan over §5 AC text for forbidden tokens (HTTP verbs, paths starting with `/`, bare status codes `200|201|400|401|403|404|409|500|503|5xx`, `[a-z_]+\.[a-z_]+`, JSON fragments, SQL constructs). Any hit **not** already overridden in the critic resolution → re-open `AskUserQuestion` for that AC line. This is the safety net if the critic missed a token (e.g. truncated output).

## Failure modes

- **Critic timeout / error** → STOP, report to user. Never fall back to silent write.
- **Critic returns `CRITIC_BLOCKED: <reason>`** (cannot Read upstream files) → STOP and report to user. Do not guess.
- **Critic returns malformed output** (no bullets, no `NO_CONTESTED_DECISIONS`, no `CRITIC_BLOCKED`) → re-dispatch once with «Your previous output did not match the required format» appended; if still malformed → STOP and ask the user how to proceed.
- **User picks `Override` for every finding** → allowed (PRD authorship is the user's call), but every override emits a §1 ¶4 bullet so the override trail is auditable.
