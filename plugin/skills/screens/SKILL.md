---
name: screens
model: inherit
effort: high
agents: []
description: >
  Use to produce the screen manifest for a UI feature — every screen in every state (the six
  classes default / loading / empty / error / success / validation, each real or N/A, plus named
  states from flow branches) with reuse-first component picks — written to
  docs/features/{slug}/screens.md, plus one exported PNG per state in docs/features/{slug}/screens/
  when drawing in pen.dev (Pencil MCP) or Figma. Draws per the canon's tool; code mode (inline
  markdown wireframes) is always available and is the fallback when the MCP is missing. Works
  WITHOUT a PRD or SAD: states derive from ux-flows branches, the design-spec state inventory and
  the story's «what can go wrong» answers, each marked with its source; with sad.md and contracts
  present it also derives states from §6 branches and API error responses. Pencil gates: active
  document checked before every write, .pen JSON never edited by hand, every PNG exported and
  checked with test -s (exists and is not empty), Cmd+S before commit, save and close before git checkout. Triggers on
  "screens for {slug}", "screen states for {slug}", "draw the screens", "mockups for {slug}",
  "/sdlc:screens {slug}", "екрани для {slug}", "стани екранів {slug}", "намалюй екрани". The
  manifest is the contract for code, never the raw design file: verify-ui reads it; point
  break-tasks / implement-tasks / review-feature at it by name.
triggers:
  - /sdlc:screens
  - "screens for"
  - "screen states for"
  - "draw the screens"
  - "екрани для"
  - "стани екранів"
  - "намалюй екрани"
stage: "util"
---

# Skill: screens (SDLC design line — step 4, per feature)

Turns the flows into the **screen manifest**: for every `SCR-NN` from `ux-flows.md`, every state
the user can hit, the components that state is built from, and a source-ref to the drawn frame and
its PNG. Whatever the tool, **the manifest is the contract** for code — downstream never opens the
`.pen` or the Figma file (`verify-ui` reads the manifest; the backbone skills are pointed at it by
name, [`../_shared/design-line.md`](../_shared/design-line.md) §1). Two rules carry the stage:

- **States are derived, not invented.** `default` plus every state a source implies: a `W-NN` or
  `D-NN` branch from `ux-flows.md`, a `design-spec.md` §8 row (`BR-NN`), a PRD §5 AC, a `sad.md`
  §6 `alt`/`else` branch, a contract error response. Each non-default state carries its provenance
  token ([`../_shared/design-line.md`](../_shared/design-line.md) §3); a state class that does not
  apply gets one explicit `N/A: <reason>` row.
- **Reuse first.** Components come from `docs/design/design-system.md` §Component inventory by
  name; `NEW: <name>` only with the one-line reason no existing component fits.

**Degrade, don't refuse.** No PRD, no SAD (module 5): states come from the flows, the design spec
and the story. With `sad.md`, a declared `target_surfaces` without any UI surface means this stage
does not apply — say so and stop.

Tool modes, layout and the pen.dev rules → [`../_shared/design-line.md`](../_shared/design-line.md)
§2, §6, §7. Questions per [`../_shared/ask-style.md`](../_shared/ask-style.md); confirm-vs-proceed
per [`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

Designer + frontend developer (often the same solo developer). In the backbone the PM confirms the
states match the ACs; `verify-ui` later checks the built screens against this manifest.

## Inputs

- `<slug>` — feature slug.
- (Expected) `docs/features/<slug>/ux-flows.md` — the `SCR-NN` inventory + the branches landing on
  each screen. **Absent → soft**: offer `/sdlc:ux-flows <slug>` first, or derive the inventory from
  `design-spec.md` / the story with a **noted gap** in §Source — never a silent invention.
- (Expected) `docs/design/design-system.md` — `tool`, `pen_file` / `figma_file`, the component
  inventory, the conventions. **Absent → `code` mode** + recommend `/sdlc:design-system`.
- (Optional) `docs/features/<slug>/design-spec.md` — §8 state inventory, §9 reuse decisions, `BR-NN`.
- (Optional, backbone) `PRD.md` §5, `sad.md` (`target_surfaces` + §6 branches),
  `contracts/openapi.yaml` (error responses).
- (Optional) `--depth=easy|medium|hard`, else `interview_depth` from `.claude/sdlc.local.md`, else
  `medium` — governs the per-screen confirm volume, never the state coverage.

## Protocol

1. **Read + resolve the mode.** Read every input above that exists. `sad.md` present and its
   `target_surfaces` contains no `web-frontend` / `mobile-app` / `desktop-app` → STOP: no UI
   surface. Resolve the tool from the canon; the tool's MCP not connected in this session → `code`
   mode with a named degradation (§Source + handoff).

2. **Derive states per screen.** For each `SCR-NN`, per the one vocabulary in
   [`../_shared/design-line.md`](../_shared/design-line.md) §3 «State vocabulary»: **check the six
   classes** (`default`, `loading`, `empty`, `error`, `success`, `validation`), each gets a row, a
   real state or one `N/A: <reason>` row; **then add the named states** from every source that lands
   on this screen (`W-NN`, `D-NN`, `BR-NN`, `AC-NN`, `§6:<flow>`, `contract:<status>`):
   `<class>-<variant>` for a second state of one class (`error-undelivered`), or a bare kebab-case
   feature name for a product state that fits no class (`ended`), each with its source token.
   An `N/A` row gets no frame and no PNG. Hover / focus / disabled are component states from the
   inventory, not screen frames. Pick components per state from
   the inventory by name; the look of each error/empty/loading state follows the canon's
   conventions. A `NEW:` component needs its why-no-existing-fits line and goes to §New components.
   Confirm per screen: `medium`/`hard` one `AskUserQuestion` per screen («Прийняти» /
   «Виправити» / «Винести у відкрите питання» / «Викинути»); `easy` or no question channel →
   derive, record in `## Assumptions`, proceed.

3. **Write the manifest progressively.** At the first screen, bootstrap
   [`./templates/screens.md`](./templates/screens.md) → `docs/features/<slug>/screens.md`
   (frontmatter `tool` from the canon, `input:` per the ladder, §Source). Write each `### SCR-NN`
   section as soon as that screen is confirmed and drawn.

4. **Draw per the tool.**
   - **`code`** — one ASCII wireframe per state that needs a distinct layout, inline under the
     screen's table. No PNGs.
   - **`figma`** — draw into the canon's `figma_file` through the Figma MCP; record the node id per
     state; export PNGs if the session's Figma tools can, else name the gap in §Source.
   - **`pencil`** — the **pen.dev gates**, in this order, per
     [`../_shared/design-line.md`](../_shared/design-line.md) §7:
     a. **Active document.** `get_app_state` → the active document must be the canon's `pen_file`.
        Mismatch → STOP and ask the user to open it. Repeat the check before each batch of writes
        if the user touched the app in between.
     b. **No hand edits.** Every change goes through `execute`; never read or write the `.pen`
        with file tools, `sed` or scripts. Read `read_skill` → `execute.md` once before drawing.
     c. **Frames.** One top-level frame per state (none for an `N/A` row), named
        `<slug> · SCR-NN · <state>`, placed left to right in flow order (default first, then the
        other states below it), with `clip: true`.
        Components are `ref` instances of the reusable components in the same document — never
        redrawn copies. A `NEW:` component is created once as `reusable: true` and then instanced.
        An inventory row marked `code-only` (in code, no node in the document yet) is **not**
        `NEW:` and needs no why-line: draw it once in the canon's `library_frame` as
        `reusable: true` under its inventory name, matching the code, instance it, and list it
        in the handoff so `/sdlc:design-system` («Оновити») records its node id.
     d. **Look.** `TakeScreenshot` each finished screen and fix clipping/collapse before moving on.
     e. **Export + `test -s`.** Inside `execute`:
        `Export([nodeId1, nodeId2, …], "png", "<repo>/docs/features/<slug>/screens")` (absolute
        directory). It writes **one file per node, named by the node id**: `<dir>/<nodeId>.png`.
        For each state: `test -s <dir>/<nodeId>.png` → `mv` it to `SCR-NN-<state>.png` →
        `test -s` again. `-s` = the file exists **and** is not empty: an export can leave no file
        or an empty one without a failing status. A failed check fails the gate: retry that node
        once, then report the state as not exported. Record node id **and** PNG path in the
        state's Source-ref cell.
     f. **Persist.** Ask the user for **Cmd+S in pen.dev**; confirm `pen_file` changed on disk
        (`stat` before/after). Remind: **save and close the `.pen` before any `git checkout`,
        `pull` or `rebase`**.

5. **Structural self-check** — re-read `screens.md` **from disk** and verify **6 items**:
   (1) every `SCR-NN` from `ux-flows.md` has a section (or the noted-gap fallback is stated in §Source);
   (2) every screen has a row for each of the six classes, a real state or an explicit
   `N/A: <reason>` row;
   (3) every non-default, non-`N/A` state carries a provenance token (`W`/`D`/`BR`/`AC`/`§6`/
   `contract`, or `derived` for a standard class the agent added itself), named states included;
   (4) every component name exists in the canon inventory or sits in §New components with a reason;
   (5) `pencil`/`figma`: every state row except `N/A` rows has a node id; `code`: every distinct
   layout has a wireframe;
   (6) `pencil`/`figma`: every PNG path in the manifest passes `test -s` (run it, don't assume);
   `N/A` rows have no PNG and are skipped.
   Fix and re-check at most 2 cycles; surface anything unresolved — never silently.

6. **Propose commits + handoff.** Propose one commit for the manifest + PNGs
   (`screens: <slug> screens.md + PNG`) and, on pencil, a separate one for `pen_file`
   (`screens: <slug> <pen_file>`) only when `git status --porcelain -- <pen_file>` shows it changed —
   an unsaved `.pen` is named in the handoff, not committed. Nobody reviews the `.pen` diff: the
   PNGs are what goes into the PR. Unresolved self-check item → no commits, say why. Then emit the
   **stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did*
   (tool or the degradation, N screens × N states, N `NEW:` components, «PNG: n/n exported, test -s
   passed», «self-check: 6/6 pass», the proposed commits) + *Review* (`docs/features/<slug>/screens.md`,
   `docs/features/<slug>/screens/`, + `pen_file` when drawn) + *Run next*: build the screens in code
   following the manifest (one component at a time, no twins of inventory components) and fill
   §Source «State access» as you build, then `/sdlc:verify-ui <slug>`; in the backbone, `/clear`,
   then `/sdlc:break-tasks <slug>` with `docs/features/<slug>/screens.md` named in the prompt (it
   does not read the manifest on its own yet).

## Definition of Done

- `docs/features/<slug>/screens.md` exists: §Source per the canon's tool (or the named degradation),
  one section per `SCR-NN` with its state table, components reuse-first, §New components filled or
  «None».
- Every non-default state traces to a source token; nothing invented, nothing silently missing.
- Every screen has a row for each of the six classes (a real state or `N/A: <reason>`), plus its
  named states from flow branches.
- `pencil`/`figma`: every state except an `N/A: <reason>` row has a node id and an exported PNG at
  `docs/features/<slug>/screens/SCR-NN-<state>.png` that passed `test -s`; an `N/A` row has neither.
  `code`: the wireframes are inline.
- `pencil`: the active-document check passed before every write; the `.pen` was changed only
  through the MCP; the user saved it.
- The manifest is the only thing downstream needs.

## Anti-patterns

- **Happy-path-only screens.** A screen with just `default` hides the states users actually hit;
  the error/empty derivation is the point of this stage.
- **States with no source.** Every non-default state traces to a token; a state with no origin is
  scope creep in a costume.
- **A twin of an inventory component.** Redrawing a button or a card that the library already has
  breaks the code handoff; instance it, or declare `NEW:` with the reason.
- **Trusting the export's silence.** An export can leave no file or an empty one without a failing
  status; `test -s` every PNG.
- **Editing `.pen` JSON**, or writing into whatever document happens to be open.
- **Committing an unsaved design.** Only the user's Cmd+S writes the `.pen` to disk.
- **Switching branches with the `.pen` open.** Save and close it first.
- **Blocking on a missing MCP.** `code` mode is always there; degrade with a named degradation.
- **Making downstream read the design file.** Node ids are for humans; the manifest carries
  everything code needs.

## References & template

- [`./templates/screens.md`](./templates/screens.md) — the manifest scaffold; inline comments are
  the generation contract.
- [`../_shared/design-line.md`](../_shared/design-line.md) — provenance tokens, tool modes, pen.dev
  rules, file layout.
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — the `target_surfaces` gate when `sad.md` exists.
- [`../verify-ui/SKILL.md`](../verify-ui/SKILL.md) — reads this manifest (states + PNG paths) after
  the screens are built.
