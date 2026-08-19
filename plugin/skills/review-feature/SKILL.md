---
name: review-feature
model: opus
effort: high
agents: [reviewer]
description: >-
  Use to run an independent, clean-context code review of an implemented feature against its
  PRD and acceptance criteria before shipping. Triggers on "review {slug}", "code review the
  changes for {slug}", "review the diff for {slug}", "is {slug} ready to ship",
  "/sdlc-review-feature {slug}", "переглянь зміни {slug}", "код-рев'ю фічі {slug}",
  "рев'ю diff". Dispatches the sdlc:reviewer subagent over the whole feature diff (stage 1
  PRD/AC compliance end-to-end, stage 2 quality), collects cited findings, and resolves each
  with you. Hard-refuses if the feature is not implemented yet.
  Triggers: /sdlc-review-feature {slug}. Output: docs/features/{slug}/_review/review-<date>.md.
triggers:
  - /sdlc-review-feature
  - "review the diff for"
  - "code review the changes for"
  - "is ready to ship"
  - "переглянь зміни"
  - "код-рев'ю фічі"
  - "рев'ю diff"
stage: "17"
---

# Skill: review-feature (SDLC stage 17 — Review 🚪 GATE)

The independent review gate. After `implement-tasks` has written + tested + committed the code,
`review-feature` looks at the **whole change at once, with fresh eyes** — does it actually satisfy
every acceptance criterion, and is it good code? This is distinct from the per-task gate inside
`implement-tasks` (which proves each task green): `review-feature` is the cross-cutting,
clean-context pass a human reviewer would do on the PR.

The reviewer agent has read-only tools and re-reads the PRD, contracts, and ADRs itself — the
freshness of its context is the point → [`../_shared/agent-roster.md`](../_shared/agent-roster.md).
The `target_surfaces` declared in `sad.md` frontmatter gate the AC-trace: a UI surface means UI
ACs must trace to UI-layer tasks and component / e2e-through-UI tests, not only backend ones →
[`../_shared/surfaces.md`](../_shared/surfaces.md).

## Як це читати (короткий вступ)

Це інструкція для агента, який запускає skill. Тут **5-крокова процедура** (Protocol нижче):
перевір, що є що рев'ювати → відправ незалежного reviewer → зібери cited findings → резолюй
кожен з юзером → запиши вердикт і хендоф.

**Словничок термінів:**

- *clean context* — reviewer не бачить попередньої розмови; він читає все з диска заново.
- *AC (Acceptance Criterion)* — умова приймання: конкретний перевірний результат з PRD §5.
- *SDLC-AC trailer* — рядок `SDLC-AC: AC-N` у git-коміті, що стверджує: цей commit задовольняє цей AC.
- *end-to-end AC trace* — трейс кожного AC наскрізь: PRD §5 → sequences (sad.md §6) → data-model → api → tasks → code+test.
- *target_surfaces* — задекларовані поверхні в `sad.md` frontmatter; review-feature читає їх, щоб знати, чи є UI-шар у ланцюжку трейсу.
- *stage-1* — AC-комплаєнс і end-to-end трейс; блокує ship до виправлення.
- *stage-2* — якість коду (конвенції, edge cases, безпека тощо); зазвичай не блокує.

## Owner

Tech Lead / a reviewer who did **not** write the code (independence is the point).

## When to use

- After `implement-tasks` has committed code + tests on the feature branch.
- Before `/sdlc-ship-feature <slug>`.
- Explicitly: `/sdlc-review-feature <slug>`.

## Inputs

- `<slug>` — feature slug, same as every upstream stage.
- **Gate (hard refuse):** an implemented change must exist — commits on the feature branch, or a
  non-empty working diff. If nothing is implemented → STOP: «run `/sdlc-implement-tasks <slug>`
  first — there is nothing to review».
- **Clean-context discipline.** Recommend `/clear` before invoking this skill: the reviewer must
  come to the diff without the implementation context that wrote it. This is enforced at the agent
  level (the `sdlc:reviewer` agent re-reads all artifacts itself), but a `/clear` before invocation
  eliminates the risk of the orchestrator paraphrasing context into the agent prompt.
- Read for the review baseline — the **whole AC chain**, so the trace can be checked end-to-end:
  `docs/features/<slug>/PRD.md` §5 (the full AC set — source of truth, not the diff's trailers),
  `sad.md` §6 (the sequence flows/branches each AC should appear in), `sad.md` frontmatter
  `target_surfaces` (which surfaces gate the trace), `data-model.md` /
  `contracts/openapi.yaml` / Accepted `adr/` (the contracts the code must honour),
  `test-plan.md` (the AC→test map, if a separate file), and `tasks/tasks.json` (which AC each
  task claimed).

## Protocol

1. **Gate + clean-context check.**
   Verify that an implemented change exists: `git diff <base>..HEAD --stat` on the feature branch
   (base = branch point), or a non-empty working diff. Nothing → refuse with the pointer above.
   If the user has not already run `/clear`, recommend it: «`/clear` first — the reviewer must
   be fresh-context; if you skip this, pass the PRD + contracts explicitly in the agent prompt».

2. **Scope the diff + dispatch the independent reviewer.**
   Determine the change under review: `git diff <base>..HEAD` on the feature branch. Note the
   `SDLC-AC` trailers — the ACs the implementation *claims* to satisfy. Then dispatch the
   [`reviewer`](../../agents/reviewer.md) agent — `subagent_type: "sdlc:reviewer"` (read-only,
   `model: opus`, `effort: high`, **clean context** — it re-reads PRD / contracts itself, no
   paraphrase from the parent) — over the diff, with the paths to the review-baseline artifacts
   (PRD.md §5, sad.md §6, sad.md `target_surfaces`, data-model.md, contracts/, adr/, tasks.json)
   inlined explicitly in the prompt, and the review dimensions in
   [`./references/review-dimensions.md`](./references/review-dimensions.md):

   - **Stage 1 — AC end-to-end trace (the gate that blocks ship)**
     a. *AC compliance.* For every AC the change claims (the `SDLC-AC` trailers / `tasks.json`
        `acs`): does the code produce the business-observable outcome the AC names, and is there
        a test that asserts *that outcome* (not a tautology)?
     b. *Full §4 user-story + §5 AC trace (the backstop).* Take the **whole** PRD **§4 user-story
        set + §5 AC set** — **not only the ACs the diff claims** — and trace both end-to-end:
        **PRD §5 → `sad.md` §6 sequence (a flow or branch shows it) → `data-model.md` (the
        schema supports it) → `contracts/openapi.yaml` (an endpoint/event exposes it) →
        `tasks/tasks.json` (a task claims it) → implement (code + a test asserts it)**.
        The trace spans **every surface declared in `sad.md` `target_surfaces`**: for a UI
        surface (`web-frontend` / `mobile-app` / `desktop-app`) a UI AC must trace to a `ui`-layer
        task **and** a component / e2e-through-UI test — not only a backend one. A UI AC that
        only has a backend test is a stage-1 gap. Flag anything that **drops out anywhere** in
        the chain: a user story with no AC, no §6 flow; an AC missing a flow, a task, a test, or
        code. The per-stage gates each guard one link; `review-feature` is the **end-to-end
        backstop** that catches what slipped between links and never reached the diff.
     c. *Contract fidelity.* Does the change honour `data-model.md`,
        `contracts/openapi.yaml`, and the Accepted ADRs (e.g. the audit-in-transaction
        decision), or does it quietly diverge?

   - **Stage 2 — quality (usually non-blocking)**
     Code quality dimensions per [`./references/review-dimensions.md`](./references/review-dimensions.md):
     conventions, UI reuse (for a UI surface), error + edge handling, security, boundary
     violations, test adequacy.

   For a large diff, fan out one reviewer per dimension and merge findings.

3. **Collect cited findings.**
   Each finding cites `file:line` + the AC/contract it touches, in the format:
   `- **[stage-N] <headline>** — file:line; AC: <id|n/a>; problem: <what>; suggested: <fix>.`
   Drop uncited findings — they are not actionable. A clean review returns `REVIEW_CLEAN: <scope>`.

4. **Resolve each finding with the user** via `AskUserQuestion`:
   - **Fix now** — hand the actionable finding back to `implement-tasks` / the author as a
     follow-up task; re-enter the TDD loop for it.
   - **Defer** — record in PRD §8 Open questions with owner + due.
   - **Not an issue** — the reviewer misread; record why.
   Never ship an unresolved stage-1 (AC / contract) finding.

5. **Write the review record + verdict + handoff.**
   Write `docs/features/<slug>/_review/review-<date>.md`: scope (diff stat), findings with
   verdicts, and the gate result (`PASS` / `CHANGES REQUESTED`).
   Then **emit the stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) —
   *What I did* + *Review* (`_review/review-<date>.md`) + *Run next*:
   - **PASS** → `/clear` (mandatory — ship-feature starts fresh), then
     `/sdlc-ship-feature <slug>`.
   - **CHANGES REQUESTED** → **no `/clear`** — stay in context to iterate; *Run next* =
     `/sdlc-implement-tasks <slug>` (fix the open findings, then re-review the changed surface).

## Definition of Done

- The independent `sdlc:reviewer` ran over the whole feature diff (not just per-task).
- Every claimed AC was checked for genuine satisfaction; **the whole PRD §4 user-story set +
  §5 AC set was traced end-to-end (PRD → sequences → data-model → api → tasks → implement)**
  — every §4 US has ≥1 AC and a §6 flow, every §5 AC reaches code+test — and anything that
  dropped out anywhere in the chain was flagged, not just the ACs the diff claims.
- Every in-scope user story / AC is covered or explicitly deferred with owner + due.
- Every finding is resolved (fixed / deferred / dismissed-with-reason); no open stage-1 finding
  remains.
- A review record exists at `docs/features/<slug>/_review/review-<date>.md` with a `PASS` /
  `CHANGES REQUESTED` verdict.

## Anti-patterns

- **Reviewing your own code in the same context that wrote it.** The reviewer must be
  clean-context — that's what catches blind spots. Run `/clear` before invoking; the
  `sdlc:reviewer` agent enforces isolation at the agent level.
- **Uncited findings.** «This feels off» is not actionable — cite `file:line` + the AC/contract
  or drop it.
- **Shipping with an open AC finding.** A stage-1 gap means the feature doesn't do what the PRD
  says — fix or explicitly de-scope (PRD change), never wave through.
- **Trusting the diff's `SDLC-AC` trailers as the complete AC set.** The trailers only list
  what the diff *claims*. Review traces the **whole** §5 set end-to-end — an AC that never
  reached the diff (no task wrote it, no test asserts it) is the most dangerous gap precisely
  because the trailers can't reveal it.
- **Ignoring target_surfaces for the AC trace.** A UI AC satisfied only by a backend test is a
  stage-1 gap, not a style comment. Read `sad.md` `target_surfaces`; if `web-frontend` /
  `mobile-app` / `desktop-app` is declared, check the `ui` task layer and UI test tiers too.
- **Re-litigating style the repo already settled.** Judge against the conventions + contracts,
  not personal taste.
- **Treating the per-task gate as the review.** Green tests prove each task; they don't prove
  the change coheres or that the ACs are truly met end-to-end.

## References

- [`./references/review-dimensions.md`](./references/review-dimensions.md) — the review
  dimensions + the reviewer dispatch shape (stage 1 + stage 2 probes; cited-finding format).
- [`../_shared/agent-roster.md`](../_shared/agent-roster.md) — `sdlc:reviewer` model/effort
  policy (opus, high, read-only, clean-isolated).
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — the `target_surfaces` taxonomy; the
  `review-feature` row in the gating table: UI AC → component / e2e-through-UI test.
- [`../_shared/handoff.md`](../_shared/handoff.md) — the stage-handoff block format; the
  loop-back and backbone-forward variants this skill uses.
