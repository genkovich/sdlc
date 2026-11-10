---
status: Living
tool: code               # code | pencil (pen.dev) | figma | <any design tool's lowercase name, with its MCP in the session> — the one committed source of the design-tool choice
design_file: ""          # tool ≠ code → the design document: a repo path (docs/design/app.pen) or the file URL (https://www.figma.com/design/<key>/<name>); code → ""
library_frame: ""        # tool ≠ code → the frame / page / section that holds the reusable components, as design-keeper recognized or created it (e.g. "Components · Chat"); left "" only when design-keeper reported «none» (read-only tool, no library and no permission, inventory run) — then the reason goes under ## Assumptions; code → ""
# Legacy synonyms, still read when design_file is empty (canons written by sdlc 4.7):
#   pen_file (tool: pencil) and figma_file (tool: figma). New canons write only design_file.
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

<!-- instruction: mirrors the frontmatter `tool`. A design tool → the design document
     (`design_file`) that holds BOTH the component library and the feature screens, how nodes are
     referenced, and how the agent reaches it (from the design-keeper report); code → screens.md
     carries inline markdown wireframes. Feature skills read this, never re-ask. -->

- **Tool:** <tool name | code> — <one line why>
- **Library location:** <`design_file`, frame / page `<library_frame>` (node id) / «the in-repo components are the library»>
- **Feature screens:** <a design tool: top-level frames `<slug> · SCR-NN · <state>` in the same document (Figma: on a page per feature) / code: inline wireframes in `docs/features/<slug>/screens.md`>
- **Agent access:** <MCP server; capabilities used — target / read / write / save / look / export, from the design-keeper report; «none» on code>
- **Foundations write permission:** <«repo file — written without asking» / «created in this run — written» / «allowed by the person, <YYYY-MM-DD>» / «not allowed — proposals under Assumptions; screens uses Drafts · <slug>» / «N/A (code)»> — the owner rule of design-line §6 gate 6; `screens` and «Оновити» read it

## Token source

<!-- instruction: where colors / spacing / typography come from. Cite a file (code) or the
     tool-side variables. A screen never re-declares a token inline. When step 4b built the
     foundation (references/foundation.md): the origin, the chosen direction, the files written and
     every «text on background» pair with its computed contrast ratio per theme. -->

- **Origin:** <existing token files | collected from values written in code | starter foundation (interview) | none yet>
- **Direction:** <name — one line why, sources `answer` / `ref:N` | «—» when tokens already existed>
- **Colors:** <source> — `<file>` or <tool variables>
- **Spacing / sizing / radius:** <source> — `<file>`
- **Typography:** <source> — `<file>`
- **Themes:** <light only | light + dark — where the dark values live>
- **Contrast (AA):** <«—» and no table when step 4b did not run | the table below, every pair, both themes>

| Pair (text on background) | Light | Dark |
|---|---|---|
| <text on bg> | <ratio, e.g. 12.6:1> | <ratio> |

## Component inventory

<!-- instruction: the reusable primitives screens compose. Code-side rows cite file:line; tool-side
     rows (a design tool: every component in the design-keeper report) cite the node id / URL. A component in
     both = ONE row with both anchors; only in the design document → Notes starts with `design-only`;
     only in code → `code-only` (not `NEW:`; `screens` draws it into the library frame on first
     use). An empty project's starter set (references/foundation.md §6): Source `starter set` until
     design-keeper draws it (then the node id), Notes `design-only — starter set, no code yet`,
     «States it supports» = the variants to draw. screens.md may use only these names, or declare
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

## Sources

<!-- instruction: only when step 4b built the foundation. One row per reference the person gave
     or the repo had; unread ones stay listed. `ref:code` = the scan of values written in code.
     Otherwise: «None.» -->

| Ref | What (URL / path / Figma node) | Signals taken (palette, fonts, density, radii) | Read |
|---|---|---|---|
| <ref:1> | <https://… / docs/brand/logo.svg / node 12:34> | <#1D4ED8 primary; Inter; airy; 8 px radii> | <read / unread: why> |

## Assumptions

<!-- instruction: one line each.
     - A decision made without asking (headless / no question channel):
       «Assumed: <decision> = <value> — because <reason>».
     - Step 4b: every decision of the foundation interview, also the confirmed ones, with its
       source tag — «<decision> = <value> — answer (round N)» / «— ref:N» / «— derived»; each merge
       of near-identical values written in code; a headless proposal as «Proposed, not written:
       direction <name>: …» (+ the starter set in an empty project).
     - Foundations the design-keeper proposed but did not write (a document with an owner, no
       permission): «Proposed, not written: <group> · <name> = <value> (<theme>)».
     Otherwise: «None.» -->

None.
