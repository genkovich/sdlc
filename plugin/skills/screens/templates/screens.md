---
status: draft            # draft | approved
input: "<prd | design-spec | story | idea-brief | frames (read mode, no other source) — the input-ladder source>"
tool: "<the canon's tool (pencil | figma | another tool's name) or code — copied from docs/design/design-system.md, or code when degraded>"
mode: draw               # draw (the agent drew the states) | read (frames drawn by the designer, read only)
updated_at: "<YYYY-MM-DD>"
---

# Screens — <feature>

> The **screen manifest**: every screen in every state, written by `/sdlc:screens`. Code is built to
> these states and `verify-ui` checks them; `break-tasks` / `implement-tasks` / `review-feature`
> get this file named in their prompt (they do not read it on their own yet). Downstream uses
> **only this manifest**, never the raw design file (`.pen`, Figma, any other tool).
> Provenance tokens: `S-N`, `W-NN`, `N-NN` (from the command), `D-NN` (derived), `frame:<node id>` (read mode), `BR-NN`, `AC-NN`, `§6:<flow>`,
> `contract:<status>`; `derived` alone = a standard state class added by the agent.

## Source

<!-- instruction: where the visuals live. A design tool → the canon's design_file (repo path or
     URL) + the frame naming + the MCP server used; code → «inline wireframes below». Name a
     degradation here when the tool's MCP was unavailable, and a missing-PNG gap when the tool
     could not export. -->

- **Tool:** <tool name | code> (from `docs/design/design-system.md`), through <MCP server | —>
- **Mode:** <draw | read — frames drawn by the designer, read only: <file + node(s) read>; frame → state: <frame name> → SCR-NN · <state>, …; not screens of <slug>: <frames>>
- **File:** <`docs/design/<name>.pen` or the file URL, frames `<slug> · SCR-NN · <state>` (page mode: on the page «Screens · <slug>») | inline wireframes below>
- **PNG folder:** <`docs/features/<slug>/screens/` | N/A (code mode) | N/A (no export in this session)>
- **Inputs used:** <`ux-flows.md`, `design-spec.md`, `story.md`, `sad.md` §6, `contracts/` — whichever existed>
- **Degradation / gaps:** <none | «<tool> MCP unavailable — code-mode wireframes» | «no permission to write into <design_file> — code-mode wireframes» | «<tool>: no export in this session — node ids only» | …>
- **State access:** <how to open each state in the running app — URL parameter (`?state=error`) / fixture switch / test account; filled when the screens are built; `verify-ui` reads it>

## Screens

<!-- instruction: one ### SCR-NN section per inventory row of ux-flows.md. The state table is
     DERIVED (_shared/design-line.md §3): a row for EACH of the six classes (default / loading /
     empty / error / success / validation), a real state or `N/A: <reason>`; then the named states
     from the flow branches landing here: `<class>-<variant>` (error-undelivered) or a bare
     kebab-case feature name (ended), each with its source token. Components: names from the
     design-system inventory, or `NEW: <name>` (read mode: «matched by name: <name>» or «not from
     the library: <what it imitates>» where that applies). Source-ref: a design tool → node id +
     PNG path (node id alone when §Source names the no-export gap); read mode: the designer's node
     id, «drawn by the agent» for a state drawn on «Screens · <slug>», or «missing — ask the
     designer»; code → «wireframe below»; an N/A row → «—» (no frame, no PNG). -->

### SCR-01 — <screen name>

| State | Source | Trigger / condition | Components (from the inventory) | Source-ref |
|---|---|---|---|---|
| default | S-1 | <…> | <Button, Card, …> | <node id> · `screens/SCR-01-default.png` |
| loading | derived | <…> | <Skeleton> | <…> |
| empty | W-01 | <…> | <EmptyState> | <…> |
| error | W-02 | <…> | <ErrorBanner> | <…> |
| success | N/A: <reason> | — | — | — |
| validation | N/A: <reason, e.g. the disabled Send button is a component state> | — | — | — |
| <error-variant or feature-state> | <W-NN / D-NN> | <…> | <…> | <…> |

```text
+--------------------------------------+
| <wireframe: SCR-01 default — code    |
|  mode only; one per state that needs |
|  a distinct layout>                  |
+--------------------------------------+
```

## Behaviour

<!-- instruction: read mode (draw mode: only what the flows say). Pop-ups, transitions,
     animations, gestures, taken only from what the design tool returned — annotations, prototype
     reactions (trigger → action, transition, duration), Code Connect instructions — each with its
     source, so code work never goes back to the design file for it. A screen with nothing found
     gets «nothing found — a note asked from the designer». -->

| Screen · state | Element | Trigger → result | Source |
|---|---|---|---|
| <SCR-01 · default> | <Send button> | <on click → opens overlay «Report», dissolve 200 ms> | <prototype reaction, node <id> / annotation / Code Connect instruction> |

## Ask the designer

<!-- instruction: read mode — every state marked «missing» (what to draw and its branch token)
     and every screen without behaviour notes. Otherwise «None.» -->

- <SCR-02 · error-undelivered — the message that could not be sent (W-02): frame missing>

## New components

<!-- instruction: every `NEW:` component named above, every `code-only` component drawn for the
     first time, and every existing library component this run changed («Changed: <component>»)
     — one row each; add it to docs/design/design-system.md §Component inventory when it is built,
     and run `/sdlc:design-system` («Оновити») after a «Changed:» row. Where: the library frame, or
     «Drafts · <slug>» on the page «Screens · <slug>» when the canon says writes are not allowed and
     the person allowed that page (the designer's library is untouched; the designer takes them
     from there). Read mode also lists «not from the library» blocks (a detached or hand-built
     imitation of <component>), `design-only` components («create in code once and add to the
     canon») and components not in the canon («run /sdlc:design-system «Оновити»»). If none:
     «None — all screens compose the existing inventory.» -->

| Component | Why no existing component fits / what changed and why | Where | Added to design-system |
|---|---|---|---|
| <name> | <one line> | <library frame / Drafts · <slug>> | <pending / done> |
| Changed: <component> | <what changed and why> | <library frame / Drafts · <slug> (changed copy)> | <run «Оновити»> |

## Assumptions

<!-- instruction: every `D-NN` / `derived` state and every decision taken without asking (easy depth,
     headless run). Otherwise «None.» -->

None.
