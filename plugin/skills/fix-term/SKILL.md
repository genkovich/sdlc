---
name: fix-term
description: >-
  Use to capture or update domain terms in CONTEXT.md before their meaning
  drifts — whenever a fuzzy word shows up in an interview, PRD, or review and
  you want one canonical definition plus a NOT-reference so a homonym can't
  bite you in six months.
  Triggers on "add term {X}", "what is {X} in our domain", "add to CONTEXT",
  "fix the glossary", "define {X}", "/sdlc-fix-term {term}", "fix term {X}",
  "додай термін", "онови глосарій", "що означає {X}".
  Lazy-bootstraps docs/features/{slug}/CONTEXT.md (or repo-root CONTEXT.md;
  multi-context repos also get CONTEXT-MAP.md updated) from a template, checks
  for a conflicting existing entry, asks for a one-sentence definition + the
  concept it's confused with, and appends one line to ## Glossary. Skip generic
  tech words (HTTP, queue, cache) — those are not domain terms.
  Output: created/edited CONTEXT.md (+ CONTEXT-MAP.md updated when multi-context).
  Runs anytime, no input gate; write-prd and architecture-design read its
  ## Glossary as the canonical source of role and domain-term names.
triggers:
  - /sdlc-fix-term
  - "fix term"
  - "add term"
  - "what is X in our domain"
  - "add to CONTEXT"
  - "fix the glossary"
  - "define X"
  - "додай термін"
  - "онови глосарій"
---

# Skill: fix-term

Lazy utility that fixes the meaning of a domain term in `CONTEXT.md` the moment it first surfaces, so its sense doesn't drift across the pipeline. For each term it captures a one-sentence canonical definition and — when the word is ambiguous — a **NOT-reference** naming the concept it's confused with. Runs anytime, with no upstream gate: a single term mid-interview, or a batch handed over by `write-prd`. The output feeds `write-prd` (role + domain-term names) and `architecture-design` (invariants), which treat `## Glossary` as canonical and override anything that contradicts it.

This is a capture utility, not a Socratic stage — it does **not** run the shared Socratic loop or critic. The one shared dependency is question phrasing:
→ [`../_shared/ask-style.md`](../_shared/ask-style.md)

## Owner

Whoever drives the conversation — anyone who spots ambiguity. Tech Lead approves the canonical form when a term is contested.

## Inputs

- `<term>` — the domain word/phrase to fix. If not given, ask for it.
- (Optional) `<slug>` — feature slug; targets `docs/features/<slug>/CONTEXT.md`. Absent → single-context check below.
- (Optional) `<context>` — bounded-context name (for multi-context repos); detected via `CONTEXT-MAP.md`.
- (Optional) `pending_glossary_terms` — a batch handed over by `write-prd` after it writes the PRD. Process each term in turn.
- (Optional) proposed phrasings already surfaced in an interview/brainstorm — offer them as definition options instead of asking blank.

## Protocol

1. **Detect context mode.** `test -f CONTEXT-MAP.md` at the repo root.
   - **Multi-context** (file exists and contains real rows): ask which bounded context `<term>` belongs to: «Available contexts: `<list from CONTEXT-MAP.md>`.» (phrasing per [`../_shared/ask-style.md`](../_shared/ask-style.md)). Target `<ctx>/CONTEXT.md`. If the context isn't yet registered in CONTEXT-MAP.md, add a row now (`| <ctx> | <path> | <1-line scope> |`).
   - **Single-context** (no CONTEXT-MAP.md or only a stub): if `<slug>` is given → `docs/features/<slug>/CONTEXT.md`; otherwise → repo-root `CONTEXT.md`. One glossary per file; don't split a term across both.
2. **Generic-term filter.** Reject words that name infrastructure or transport rather than the business domain (e.g. HTTP, queue, cache, the datastore, a framework, JSON, REST, gRPC). Refuse: «`<term>` is technical, not a domain word — its choice belongs in the SAD or an ADR, not the glossary». Continue only for genuine domain vocabulary.
3. **Bootstrap (lazy).** `test -f <target>`. Missing → copy [`./templates/CONTEXT.md`](./templates/CONTEXT.md) to `<target>`. Present → read it.
4. **Conflict check.** `grep -i "^- <term>" <target>`.
   - Found, identical sense → STOP, report «already in the glossary».
   - Found, different sense → escalate via `AskUserQuestion` (phrasing per [`../_shared/ask-style.md`](../_shared/ask-style.md)): «`<term>` is already defined as `<existing>` — same concept or a different one?». If different, propose a disambiguating pair of names (e.g. a billing-scoped vs a runtime-scoped variant) and fix both.
   - Not found → continue.
5. **Ask the canonical definition** — one `AskUserQuestion`: «Define `<term>` in this domain, in one sentence». Offer interview/brainstorm phrasings as options when available; otherwise free text. Follow the explanatory style in [`../_shared/ask-style.md`](../_shared/ask-style.md) — gloss every technical term inline, explain why the definition matters.
6. **Ask the NOT-reference** — one `AskUserQuestion`: «Which concept does `<term>` get confused with, so a future reader doesn't mix them up?». No plausible homonym → `None`.
7. **Compose one line.** `- <term> — <one-sentence definition>. NOT <confused concept + how it differs>.` — or, when step 6 = None, `- <term> — <definition>.`
8. **Append under `## Glossary`.** Read the file, insert the line in `## Glossary` (alphabetical if the section is already sorted, else at the end). Never rewrite existing entries.
9. **Prune empty H2s.** On a fresh bootstrap, delete `## Invariants` / `## Out of scope` if they hold no real content — only `## Glossary` is mandatory. (A genuine invariant or out-of-scope note goes in its section, never as implementation detail.)
10. **Stamp + commit + handoff.** Set `updated_at: <today>` in the frontmatter. Propose `context: + <term>` (or `context: + <term>, <term2>` for a batch). May fold into the caller's intake/PRD commit. Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) (utility variant) — *What I did* + *Review* (`CONTEXT.md`) + *Run next*: resume your backbone stage (e.g. `/sdlc-architecture-design <slug>`); `/clear` optional.

## Definition of Done

- `<target>` exists and contains `<term>` under `## Glossary` in the «one-sentence canonical + optional NOT-reference» format.
- Any conflict with an existing entry is resolved (reported as duplicate, or disambiguated into distinct names).
- Generic tech words are refused, not stored.
- Empty H2 sections are pruned on bootstrap; `## Glossary` remains.
- Multi-context: `CONTEXT-MAP.md` has a row for the context; the term lands in the correct bounded-context `CONTEXT.md`.
- `updated_at` reflects today; a commit is proposed.

## Anti-patterns

- **Glossary as PRD or scratch pad.** Implementation detail («counter stored with a 1-minute TTL») belongs in the SAD/ADR, not here.
- **Empty H2 «for completeness».** A heading with no bullets — prune it.
- **Silent edits.** Adding a term without confirming the definition; the author must control the glossary.
- **Batched «I'll add them later».** Capture each term the moment it surfaces — deferral loses it.
- **Storing generic tech words.** HTTP, queue, the datastore name — refuse them.
- **Rewriting on re-run.** The skill reads and appends; it never overwrites the file.
- **Ambiguous term with no NOT-reference.** A homonym without «NOT …» is a six-month confusion waiting to happen.
- **Multi-context term in the wrong file.** When `CONTEXT-MAP.md` exists, each term must land in the file that owns its bounded context — not always the root.

## References & templates

- [`./templates/CONTEXT.md`](./templates/CONTEXT.md) — output scaffold; inline comments are the per-section contract (Glossary mandatory, Invariants/Out-of-scope pruned when empty).
- [`../_shared/ask-style.md`](../_shared/ask-style.md) — phrasing for the definition / NOT-reference / conflict questions.
- [`../_shared/handoff.md`](../_shared/handoff.md) — stage-handoff block format (utility variant).
- [`../../../document-templates/CONTEXT-MAP.md`](../../../document-templates/CONTEXT-MAP.md) — CONTEXT-MAP.md scaffold for multi-context repos.

## Example invocation

> **User:** «add term tenant for rate-limiting-per-user»
> **Skill:** `test -f CONTEXT-MAP.md` → not exists. Single-context. `<slug>` = `rate-limiting-per-user` → target `docs/features/rate-limiting-per-user/CONTEXT.md`. Generic filter: `tenant` is domain → continue. File missing → copy template. `grep "^- tenant"` → not found. Definition Q → «a billable customer organisation owning 1+ users». NOT-reference Q → «NOT user — a user is one person inside a tenant». Compose `- tenant — a billable customer organisation owning 1+ users. NOT user (a user is one person inside a tenant).` → append under `## Glossary` → prune empty `## Invariants`/`## Out of scope` → `updated_at: 2026-05-29` → commit `context: + tenant`. Emit handoff block (utility variant): *What I did* — appended `tenant` to `docs/features/rate-limiting-per-user/CONTEXT.md`; *Run next* — resume `/sdlc-architecture-design rate-limiting-per-user`.
