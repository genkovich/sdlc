---
name: prepare-design-spec
description: >
  Turn a raw UI request or confirmed product idea into a repository-aware design spec and a
  testable Definition of Done before opening Figma, Pencil, or another design tool. Use when the
  user asks for a "design spec", "UI spec", "design spec for Figma or Pencil", "Definition of Done
  for a screen", "design-to-code handoff", or invokes "/sdlc-prepare-design-spec SLUG". Reads
  the real repository and existing SDLC artifacts, then writes one
  docs/features/SLUG/design-spec.md that contains the specification and an embedded, traced Definition of
  Done. Do not use for broad product discovery, architecture design, implementation, or browser
  verification.
---

# Skill: prepare-design-spec (SDLC design-entry utility)

Create the contract that both a designer and an implementation agent can follow in a single
design-spec.md: its specification half (BR-XX) says what must be designed and what existing product behavior must
survive; its Definition of Done half says how the team will prove the result is complete.

This skill closes a specific SDLC gap:

```text
raw idea → interview / PRD → prepare-design-spec → Figma or Pencil → implementation → verify-ui
```

It does not invent a redesign from taste. It traces every important statement to the user's words,
an existing SDLC artifact, or evidence in the repository.

## Owner

Product designer or frontend engineer, with the product owner confirming scope and the developer
confirming implementation constraints.

## When to use

- Before creating or revising a screen in Figma, Pencil, Sketch, or code.
- When a UI task exists but nobody can explain where its spec or acceptance boundary came from.
- When design-to-code work risks dropping existing behavior, async states, accessibility, or reuse.
- When several tools must solve the same design task and need one comparable contract.
- After `interview` or `write-prd` for a larger feature; directly from a small raw request for a
  bounded UI iteration.

Do not use it to discover the entire product strategy: run `interview` first. Do not use it to
verify a finished screen in a browser: run `verify-ui` after implementation.

## Inputs

- `<slug>` in kebab-case, for example `meme-editor`.
- A raw request, issue, `idea-brief.md`, or `PRD.md`.
- The target repository, including the current UI, routes, styles, tests, and design assets.
- Optional design references supplied by the user. Never choose a new external visual direction
  without explicit evidence or approval.

## Protocol

1. **Name the raw request.** Preserve the user's original request verbatim in the design spec. If the
   request is missing, ask for one to three plain-language sentences: who needs what change and why.

2. **Choose the evidence source.** Look for, in order:
   `docs/features/<slug>/PRD.md`, `docs/features/<slug>/idea-brief.md`, a linked issue, and the user's
   raw request. Record which sources exist. A missing PRD is acceptable for a small UI iteration;
   missing intent is not.

3. **Inspect the real product before proposing design.** Read the route entry point, styles or
   tokens, reused components, data calls, navigation targets, and relevant tests. Run only
   read-only discovery commands. Record exact paths and current behavior in `Current evidence`.

4. **Reconstruct the current user flow.** Write the start state, user actions, system responses,
   success outcome, and recovery paths. Do not reduce an interactive screen to a screenshot.

5. **Ask only questions the repository cannot answer.** Cover these seven decisions:
   user and job, trigger, target route/surface, required actions, states and failures, reuse and
   constraints, and proof of success. Batch only the unresolved questions and explain why each
   answer changes the design.

6. **Derive the specification.** Copy `templates/design-spec.md` to
   `docs/features/<slug>/design-spec.md` and fill the specification sections (1–15). Use `N/A — <reason>`
   instead of deleting a section. Requirements must describe observable product behavior, not an
   arbitrary implementation.

7. **Separate facts, decisions, and proposals.** Mark every material item as one of:
   `Confirmed` (user or SDLC artifact), `Observed` (repository evidence), or `Proposed` (needs
   approval). Do not quietly turn a model preference into a requirement.

8. **Specify the design surface.** Define target routes, desktop/mobile frames, content, component
   and token reuse, state specimens, responsive behavior, accessibility, and explicit non-goals.
   For a redesign, state which existing product semantics must remain unchanged.

9. **Write the handoff contract.** Map each design element to its likely code owner or existing
   component. If no reusable owner exists, say `new component candidate`; do not invent a path.

10. **Derive the Definition of Done from risk.** Fill the Definition of Done section (16) of the
    same `design-spec.md`. Add at least one check for every specification section
    that could fail: structure, tokens/reuse, states, behavior, responsive layout, accessibility,
    deterministic gates, live browser evidence, and repository scope.

11. **Make every DoD item testable.** Each row must name the expected result and its evidence:
    repository path, command, browser action, screenshot, design-node inspection, or API outcome.
    Replace vague words such as `nice`, `modern`, `correct`, and `pixel-perfect` with observable
    criteria.

12. **Trace the contract.** Give each requirement an ID (`BR-01`, `BR-02`, ...) and each DoD item
    an ID (`DOD-01`, `DOD-02`, ...). The DoD table must link back to one or more requirement IDs in
    the same file, and the requirement-coverage table must list every BR-ID.
    No requirement may be left without proof.

13. **Run the spec-ready gate.** Confirm: no invented routes or dependencies; current behavior
    is documented; desktop and mobile are covered where relevant; empty/loading/success/error and
    interactive states are covered; reuse and non-goals are explicit; every requirement maps to a
    DoD check; all `Proposed` decisions are visible.

14. **Present the student-repeatable summary.** Return four blocks: `What we learned from the
    repository`, `What the user decided`, `What remains proposed`, and `Run next`. The next action is
    a design tool only when the spec-ready gate passes.

15. **Handoff.** Design with the approved spec in Figma or Pencil. Implement against `design-spec.md`.
    Then run deterministic project checks and `verify-ui` against the live route. A generated image
    or an agent success message is never completion evidence.

## Questions for discussion

Use these only when the answer is not already in the repository or upstream artifacts:

- Who is trying to complete what job on this screen?
- What starts the flow, and what outcome tells the user they are done?
- Which route or product surface owns the change?
- Which actions and data must remain functional after the redesign?
- Which empty, loading, success, error, hover, focus, and disabled states matter?
- Which components, tokens, API contracts, navigation, and content must be reused?
- What must not change, and what evidence will prove that it did not break?

## Definition of Done

- `docs/features/<slug>/design-spec.md` exists, contains no unexplained empty sections, and every DoD check names concrete evidence.
- The raw request and all evidence sources are recorded.
- Current route, behavior, state, reuse, responsive, accessibility, and non-goal constraints are
  represented as requirement IDs.
- Every requirement ID is covered by at least one DoD row.
- `Confirmed`, `Observed`, and `Proposed` statements are distinguishable.
- No route, dependency, component, token, or API contract is presented as fact without evidence.
- The spec-ready gate passes before a design tool is asked to author the screen.

## Anti-patterns

- **Opening Figma before naming the problem.** The tool will fill gaps with taste, so the result
  cannot be reviewed against product intent.
- **Copying a polished spec without showing its sources.** Students can reproduce the demo but
  cannot create the next spec on their own.
- **Treating a screenshot as the product.** Static output hides async, error, focus, disabled, and
  responsive behavior that implementation must preserve.
- **Writing `looks modern` as DoD.** It has no falsifiable evidence, so reviewers cannot agree on
  completion.
- **Inventing a new design system during a small iteration.** Unapproved dependencies and tokens
  expand scope and make the design-to-code handoff dishonest.
- **Letting the agent declare itself done.** Completion requires repository commands and live UI
  evidence, not a narrative report.
- **Duplicating PRD or architecture work.** This skill narrows a confirmed product change into a UI
  contract; it does not replace upstream product or system design.

## Templates

- [`templates/design-spec.md`](templates/design-spec.md)

## Example invocation

```text
/sdlc-prepare-design-spec meme-editor

Raw request: Improve the current meme generator so a person can edit both captions,
preview the result, and save it without breaking the existing gallery.

Inspect app/page.tsx, app/globals.css, /api/memes/random, /api/memes, and /gallery.
Create the design spec and Definition of Done before opening Figma or Pencil.
```

Expected outputs:

```text
docs/features/meme-editor/design-spec.md
```
