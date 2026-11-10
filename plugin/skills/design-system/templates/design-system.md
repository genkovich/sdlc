---
status: Living
tool: code               # pencil | figma | code — the one committed source of the design-tool choice
pen_file: ""             # tool: pencil → the .pen document, e.g. docs/design/app.pen; else ""
library_frame: ""        # tool: pencil → the top-level frame that holds the reusable components, as pen-keeper recognized or created it (e.g. "Components · Chat"); else ""
figma_file: ""           # tool: figma → the Figma file URL; else ""
updated_at: "<YYYY-MM-DD>"
---

# Design system — <project name>

> The project's **design canon**, written once per repo by `/sdlc:design-system` and read by
> `ux-flows`, `prepare-design-spec`, `screens` and `verify-ui`. Committed: the tool choice and the
> inventory are team-wide. `docs/architecture-map.md` §Frontend (when present) is the inventory of
> the **code**; this file is the **design-side** canon. Refresh with `/sdlc:design-system` when the
> foundation changes.

## Platform posture

<!-- instruction: ONE primary posture + a one-line rationale. ux-flows uses it as the default for
     every feature; a feature that deviates says so in its ux-flows.md. -->

- **Posture:** <mobile-first | desktop-first | responsive-both> — <why, one line>
- **Breakpoints / device classes:** <named breakpoints or device classes, or "-">

## Design tool

<!-- instruction: mirrors the frontmatter `tool`. pencil → the .pen document that holds BOTH the
     component library and the feature screens; figma → the file + how nodes are referenced;
     code → screens.md carries inline markdown wireframes. Feature skills read this, never re-ask. -->

- **Tool:** <pencil | figma | code> — <one line why>
- **Library location:** <`docs/design/<name>.pen`, frame `<library_frame>` (node id) / Figma file URL / «the in-repo components are the library»>
- **Feature screens:** <pencil: top-level frames `<slug> · SCR-NN · <state>` in the same document / figma: a page per feature / code: inline wireframes in `docs/features/<slug>/screens.md`>

## Token source

<!-- instruction: where colors / spacing / typography come from. Cite a file (code) or the
     tool-side variables. A screen never re-declares a token inline. -->

- **Colors:** <source> — `<file>` or <tool variables>
- **Spacing / sizing / radius:** <source> — `<file>`
- **Typography:** <source> — `<file>`
- **Themes:** <light only | light + dark — where the dark values live>

## Component inventory

<!-- instruction: the reusable primitives screens compose. Code-side rows cite file:line; tool-side
     rows (pencil: every component in the pen-keeper report) cite the node id / URL. A component in
     both = ONE row with both anchors; only in the design document → Notes starts with `design-only`;
     only in code → `code-only` (not `NEW:`; `screens` draws it into the library frame on first
     use). screens.md may use only these names, or declare
     `NEW: <name>` with a why-no-primitive-fits line (then the component is added here). -->

| Component | Source (`file:line` / node / URL) | States it supports | Notes |
|---|---|---|---|
| <Button> | `<path>:<line>` · node `<id>` | default / hover / disabled / loading | <…> |
| <Toast> | node `<id>` | default | design-only — <no code yet> |

## Interaction & writing conventions

<!-- instruction: the cross-screen rules every new screen follows — one line each. screens derives
     the look of every error / empty / loading state from these. -->

- **Errors:** <toast / inline / page-level — the one pattern this project uses>
- **Empty states:** <the pattern — text + CTA / illustration + CTA / …>
- **Loading:** <skeleton / spinner / progressive — the one pattern>
- **Validation:** <on-blur / on-submit; how errors attach to fields>
- **Microcopy tone:** <one line>

## Assumptions

<!-- instruction: only when a decision was made without asking (headless / no question channel):
     one line each — «Assumed: <decision> = <value> — because <reason>». Otherwise: «None.» -->

None.
