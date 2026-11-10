---
status: draft            # draft | approved
input: "<prd | design-spec | story | idea-brief — the input-ladder source this run used>"
feature_size: "<XS|S|M|L|XL — mirror of .size, or '-' when there is none>"
updated_at: "<YYYY-MM-DD>"
---

# UX flows — <feature>

> How the user moves through the feature, written by `/sdlc:ux-flows` and read by
> `prepare-design-spec` and `screens` (details every inventory row); name it in the prompt of
> `architecture-design` (target-surface evidence) and `plan-tests` (e2e-through-UI paths). **Always markdown + mermaid
> `flowchart`**, whatever the design tool. Provenance tokens: `AC-NN` (PRD), `BR-NN`
> (design-spec), `S-N` (story sentence), `W-NN` («what can go wrong», confirmed by the user),
> `D-NN` (derived: inferred, not confirmed — see Assumptions).

## Source

<!-- instruction: the input used and, in story mode, the story's sentences numbered S-1…S-n
     (quote them; the full story lives in story.md). Full mode: «PRD.md §4/§5». -->

- **Input:** <`docs/features/<slug>/PRD.md` | `story.md` | …>
- **Story sentences:** <S-1 «…» · S-2 «…» · … — story mode only>

## Platform decisions

<!-- instruction: the posture these flows assume — default from docs/design/design-system.md; a
     deviation is named + justified. Plus flow-level decisions (navigation shape, dialog vs page).
     NO components, no layout — that is screens. -->

- **Posture:** <mobile-first | desktop-first | responsive-both> — <«per design-system» or the deviation + why>
- **On the canvas:** screens are static frames left to right in flow order; the clickable flow lives in code.

## Screen inventory

<!-- instruction: every distinct screen the flows visit. SCR-NN ids are the downstream contract
     (screens.md details each). «Branches landing here» lists the W/AC ids whose branch ends on this
     screen — screens turns them into states. -->

| ID | Screen | Purpose | Entry | Exit | Branches landing here |
|---|---|---|---|---|---|
| SCR-01 | <name> | <one line> | <from where> | <to where> | <W-01, AC-03, …> |

## Flows

<!-- instruction: ONE flow per UI-touching §4 user story (full mode) or per user goal in the story
     (story mode): happy path + one branch per W-NN / AC. Nodes reference SCR ids. Edge labels
     carry the provenance token of the branch. Each flow is followed by its prose account. -->

### Flow: <US-n or goal — name>

```mermaid
flowchart LR
    A[SCR-01 screen] -->|S-2 action| B{decision}
    B -->|ok| C[SCR-02 screen]
    B -->|W-01 failure| D[SCR-01 error state]
```

<one-paragraph prose account: the happy path + every branch, in plain words>

## Coverage

<!-- instruction: one row per story sentence S-N and per W-NN (story mode) or per §5 AC (full
     mode), each pointing to the flow / branch that shows it, or `N/A: <reason>`. -->

| Source | Item | Shown by | How | Note |
|---|---|---|---|---|
| S-1 | <sentence, short> | Flow <name> → <node> | flow / branch / N/A | <…> |
| W-01 | <failure> | Flow <name> → <branch> | branch | <…> |
| D-01 | <inferred failure — derived> | Flow <name> → <branch> | branch | see Assumptions |

Coverage: <n>/<n> story sentences (or user stories) · <m>/<m> failures (or ACs) — <k> N/A.

## Assumptions

<!-- instruction: every `D-NN` branch and every decision taken without asking (easy depth,
     headless run): «Assumed: <decision> — because <reason>. [veto?]». Otherwise «None.» -->

None.
