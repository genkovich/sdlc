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
  when drawing in a design tool through its MCP (pen.dev, Figma or any other) that can export.
  Draws per the canon's tool; code mode (inline markdown wireframes) is always available and is the
  fallback when the MCP is missing. Works WITHOUT a PRD or SAD: states derive from ux-flows
  branches, the design-spec state inventory and the story's «what can go wrong» answers, each
  marked with its source; with sad.md and contracts present it also derives states from §6
  branches and API error responses. Design-tool gates, the same for every tool: the tool's target
  document checked before every write, the design file never edited by hand, every PNG exported
  and checked with test -s (exists and is not empty) or named as a gap when the tool cannot export,
  the document saved (save tool, autosave or Cmd+S) before commit; pen.dev: save and close before
  git checkout. Triggers on "screens for {slug}", "screen states for {slug}", "draw the screens",
  "mockups for {slug}", "/sdlc:screens {slug}", "екрани для {slug}", "стани екранів {slug}",
  "намалюй екрани". The manifest is the contract for code, never the raw design file: verify-ui
  reads it; point break-tasks / implement-tasks / review-feature at it by name.
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
design file (`verify-ui` reads the manifest; the backbone skills are pointed at it by name,
[`../_shared/design-line.md`](../_shared/design-line.md) §1). Two rules carry the stage:

- **States are derived, not invented.** `default` plus every state a source implies: a `W-NN`,
  `D-NN` or `N-NN` branch from `ux-flows.md`, a `design-spec.md` §8 row (`BR-NN`), a PRD §5 AC, a `sad.md`
  §6 `alt`/`else` branch, a contract error response. Each non-default state carries its provenance
  token ([`../_shared/design-line.md`](../_shared/design-line.md) §3); a state class that does not
  apply gets one explicit `N/A: <reason>` row.
- **Reuse first.** Components come from `docs/design/design-system.md` §Component inventory by
  name; `NEW: <name>` only with the one-line reason no existing component fits.

**Degrade, don't refuse.** No PRD, no SAD (module 5): states come from the flows, the design spec
and the story. With `sad.md`, a declared `target_surfaces` without any UI surface means this stage
does not apply — say so and stop.

Tool modes, layout, the gates for every tool and the per-tool rules →
[`../_shared/design-line.md`](../_shared/design-line.md) §2, §6–§9. Questions per
[`../_shared/ask-style.md`](../_shared/ask-style.md); confirm-vs-proceed per
[`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

Designer + frontend developer (often the same solo developer). In the backbone the PM confirms the
states match the ACs; `verify-ui` later checks the built screens against this manifest.

## Inputs

- `<slug>` — feature slug.
- (Expected) `docs/features/<slug>/ux-flows.md` — the `SCR-NN` inventory + the branches landing on
  each screen. **Absent → soft**: offer `/sdlc:ux-flows <slug>` first, or derive the inventory from
  `design-spec.md` / the story with a **noted gap** in §Source — never a silent invention.
- (Expected) `docs/design/design-system.md` — `tool`, the design file (`design_file`, else the
  legacy synonym per design-line §6), `library_frame`, «Agent access», the component inventory,
  the conventions. **Absent → `code` mode** + recommend `/sdlc:design-system`.
- (Optional) `docs/features/<slug>/design-spec.md` — §8 state inventory, §9 reuse decisions, `BR-NN`.
- (Optional, backbone) `PRD.md` §5, `sad.md` (`target_surfaces` + §6 branches),
  `contracts/openapi.yaml` (error responses).
- (Optional) `--depth=easy|medium|hard`, else `interview_depth` from `.claude/sdlc.local.md`, else
  `medium` — governs the per-screen confirm volume, never the state coverage.

## Protocol

1. **Read + resolve the mode.** Read every input above that exists. `sad.md` present and its
   `target_surfaces` contains no `web-frontend` / `mobile-app` / `desktop-app` → STOP: no UI
   surface. Resolve the tool from the canon and find its MCP in this session per
   [`../_shared/design-line.md`](../_shared/design-line.md) §6 (deferred tools included; start from
   the canon's «Agent access» line); map its capabilities (target document, read, write, save,
   look, export). Not connected → `code` mode with a named degradation (§Source + handoff). Connected
   but with no write tool → `code` mode too, named («<tool> MCP is read-only in this session»).
   **Permission to write** (design-line §6 gate 6). Read the canon's «Foundations write
   permission» line; no such line (a canon from 4.7) → the owner rule itself (a repo path is
   allowed, a URL is not).
   - Allowed → draw as below.
   - Not allowed → this run writes **nothing** into the designer's file on its own. Read the
     canon's «Screens write permission» line: «allowed — «Screens · <slug>» pages» → **page
     mode**; «not allowed» → `code` mode, named («no permission to write into <design_file> —
     code-mode wireframes»); not asked yet (or the person wants to change it) → interactive: one
     `AskUserQuestion` per [`../_shared/ask-style.md`](../_shared/ask-style.md): «Намалювати
     екрани на окремій сторінці «Screens · <slug>» у цьому файлі?» — «Так, лише на цій сторінці»
     (the state frames and a «Drafts · <slug>» frame with new components go there; the library and
     every other page stay untouched) / «Ні, вайрфрейми в markdown» (`code` mode, no PNG);
     headless → `code` mode, nothing asked. Write the answer into the canon's §Design tool
     «Screens write permission» line («allowed — «Screens · <slug>» pages, <YYYY-MM-DD>» / «not
     allowed — code mode» / «not asked — a headless run used code mode»), so the next run reuses
     it.
   The canon's `library_frame` is empty: writes allowed → `code` mode, named («the design document
   has no library yet — run `/sdlc:design-system`»), so the document stays empty for the
   foundations run; page mode → draw, with every component in «Drafts · <slug>».

2. **Derive states per screen.** For each `SCR-NN`, per the one vocabulary in
   [`../_shared/design-line.md`](../_shared/design-line.md) §3 «State vocabulary»: **check the six
   classes** (`default`, `loading`, `empty`, `error`, `success`, `validation`), each gets a row, a
   real state or one `N/A: <reason>` row; **then add the named states** from every source that lands
   on this screen (`W-NN`, `D-NN`, `N-NN`, `BR-NN`, `AC-NN`, `§6:<flow>`, `contract:<status>`):
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
   - **A design tool** (`tool` ≠ `code`) — the gates, in this order, per
     [`../_shared/design-line.md`](../_shared/design-line.md) §6, then the tool's specifics below:
     a. **Target document.** The tool's target is the canon's design file (absolute paths for a
        local file, file keys for a URL). Mismatch → STOP and ask the user to open it. Repeat the
        check before each batch of writes if the user touched the app in between. Before the first
        write, read the tool's own guide once (§6 gate 3); a local file: `stat` it now.
     b. **No hand edits.** Every change goes through the tool's write tools; never read or write
        the design file with file tools, `sed` or scripts.
     c. **Frames.** One top-level frame per state (none for an `N/A` row), named
        `<slug> · SCR-NN · <state>`, placed left to right in flow order (default first, then the
        other states below it), content clipped to the frame.
        **A state frame holds only the layers of that state.** Build each state from instances;
        never copy the `default` frame and hide what does not belong (`enabled: false`, a hidden
        layer, zero opacity): hidden leftovers of other states (a «retry» button in `default`, an
        input block in `ended`) show up in the Layers panel and confuse the next reader. A copied
        frame gets those layers **deleted**, not hidden.
        Components are instances of the reusable components in the same document — never
        redrawn copies; a variant is picked through the tool's variant mechanism (§7.12 pen.dev,
        §8 Figma). Where a new component goes depends on the permission (step 1):
        - **writes allowed** — a `NEW:` component is created once as a reusable component in the
          canon's `library_frame`, then instanced. An inventory row marked `code-only` (in code, no
          node in the document yet) is **not** `NEW:` and needs no why-line: draw it once there
          under its inventory name, matching the code, instance it, and list it in the handoff so
          `/sdlc:design-system` («Оновити») records its node id;
        - **page mode** (no write permission, the person allowed «Screens · <slug>») — every state
          frame goes on the page «Screens · <slug>» (Figma: a page; another tool: its page, else one
          top-level frame of that name), and every `NEW:` and `code-only` component is drawn in a
          frame «Drafts · <slug>» on the same page and instanced from there; the library and every
          other page stay untouched; the handoff lists the drafts for the designer.

        **Changing an existing library component** (a fourth tab in the TabBar, a new Button
        variant) is allowed only with a line «Changed: <component> — what and why» in §New
        components and in the handoff, with the advice to run `/sdlc:design-system` («Оновити»).
        In page mode the original is never changed: a changed copy goes in «Drafts · <slug>» under
        the same name + « (changed)», and the screens instance the copy.
     d. **Look.** Screenshot each finished screen through the tool and fix clipping/collapse before
        moving on.
     e. **Export + `test -s`.** Per state, a PNG at
        `<repo>/docs/features/<slug>/screens/SCR-NN-<state>.png` (absolute path) through the
        tool's export: a tool that writes files → rename its output to that name; a tool that
        returns a URL → `curl -sSfL -o <path> <url>`. `test -s` every file at its final path (`-s` =
        exists **and** is not empty: an export can leave no file or an empty one without a failing
        status). **One command per call** (design-line §6 gate 5): `test -s <file>`, then `mv
        <from> <to>`, then `test -s <to>`, each its own Bash call; no loops, no `&&`, no helper
        script, nothing written to `/tmp` or elsewhere outside the repo. A failed check fails the
        gate: retry that node once, then report the state as not exported. Record node id **and** PNG path in the state's Source-ref cell. **No export
        capability** in the session (an image returned only into the conversation is a look) → no
        PNG; name the gap in §Source («<tool>: no export in this session — node ids only»); the
        node id stays the source-ref.
     f. **Persist.** Save through the tool per §6 gate 4: a `save` tool → call it; a tool that
        saves by itself → nothing; neither → ask the user. A local file: confirm it changed on disk
        (`stat` before/after); a URL: read the frames back.

     **pen.dev** (`tool: pencil`, design-line §7):
     - a: `get_app_state` → the active document must be the canon's `.pen`; pass its `uri`
       (`file://<absolute path>`) wherever a tool asks for one. Guide:
       `read_skill({ path: "execute.md" })` once before drawing.
     - b–c: every change goes through `execute`; frames with `clip: true`; components are `ref`
       instances, a `NEW:` or `code-only` component is created with `reusable: true`; each variant
       is its own component; no node of a state frame has `enabled: false`.
     - d: `TakeScreenshot` each finished screen.
     - e: inside `execute`, `Export([nodeId1, nodeId2, …], "png", "<repo>/docs/features/<slug>/screens")`
       (absolute directory) writes **one file per node, named by the node id**:
       `<dir>/<nodeId>.png`. For each state, three separate calls: `test -s <dir>/<nodeId>.png`,
       `mv <dir>/<nodeId>.png <dir>/SCR-NN-<state>.png`, `test -s <dir>/SCR-NN-<state>.png`.
     - f: `save` with the document's `uri` (no `save` tool → ask the user for **Cmd+S in pen.dev**);
       confirm the `.pen` changed on disk (`stat` before/after). Remind: **save and close the
       `.pen` before any `git checkout`, `pull` or `rebase`**.

     **Figma** (`tool: figma`, design-line §8):
     - a: Figma Console → the canon's file key is in `figma_list_open_files` (Desktop Bridge
       running in it) and is the active target, or pass `fileKey` on every call; the official Figma
       MCP → the file key goes into every call, writing needs `use_figma` (beta), edit access and a
       Full seat.
     - c: frames on the feature's page (`<slug>`); instances of the library's components
       (`figma_instantiate_component` or `figma_execute`), a variant = a component-set property;
       page mode → the page «Screens · <slug>» with its «Drafts · <slug>» frame; no hidden layer
       (`visible: false`) in a state frame.
     - d: `figma_capture_screenshot` (Console) / `get_screenshot` (official).
     - e: Console → after the look, `figma_get_component_image` per frame returns a URL → `curl` →
       `test -s` (it renders the cloud state, which can lag behind the live drawing; no URL or a
       failed `curl` → the named gap for that state); the
       official server's `get_screenshot` is a look, not an export → a PNG only through another
       export tool in the session, else the named gap.
     - f: Figma saves by itself; read the frames back.

5. **Structural self-check** — re-read `screens.md` **from disk** and verify **7 items**:
   (1) every `SCR-NN` from `ux-flows.md` has a section (or the noted-gap fallback is stated in §Source);
   (2) every screen has a row for each of the six classes, a real state or an explicit
   `N/A: <reason>` row;
   (3) every non-default, non-`N/A` state carries a provenance token (`W`/`D`/`N`/`BR`/`AC`/`§6`/
   `contract`, or `derived` for a standard class the agent added itself), named states included;
   (4) every component name exists in the canon inventory or sits in §New components with a reason;
   every library component this run changed has a «Changed: <component> — what and why» row; in
   page mode every state frame sits on «Screens · <slug>» and every `NEW:`, `code-only` and changed
   component in its «Drafts · <slug>» frame, nothing elsewhere in the file; without write
   permission and without that page, the run is in `code` mode and the canon's «Screens write
   permission» line is filled;
   (5) `tool` ≠ `code`: every state row except `N/A` rows has a node id; `code`: every distinct
   layout has a wireframe;
   (6) `tool` ≠ `code`: every PNG path in the manifest passes `test -s` (run it, one call per file,
   no loop; don't assume); a non-`N/A` state without a PNG is allowed only when §Source names the
   no-export gap; `N/A` rows have no PNG and are skipped;
   (7) `tool` ≠ `code`: read every state frame back through the tool: no hidden node in it
   (`enabled: false`, `visible: false`, zero opacity), no layer of another state.
   Fix and re-check at most 2 cycles; surface anything unresolved — never silently.

6. **Propose commits + handoff.** Propose one commit for the manifest + PNGs
   (`screens: <slug> screens.md + PNG`; plus the canon when this run wrote its «Screens write
   permission» line) and, when the design file is a local path, a separate one
   for it (`screens: <slug> <design_file>`) only when `git status --porcelain -- <design_file>`
   shows it changed — an unsaved design file is named in the handoff, not committed. Nobody reviews
   a design file's diff: the PNGs are what goes into the PR. Unresolved self-check item → no
   commits, say why. Then emit the **stage-handoff block** per
   [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did* (tool or the degradation, N
   screens × N states, N `NEW:` components, every «Changed:» component with the advice to run
   `/sdlc:design-system` («Оновити»), in page mode the page «Screens · <slug>» and the list of
   components in «Drafts · <slug>» for the designer, the permission answer when it was asked, «PNG: n/n exported, test -s passed» or the named no-export gap, «self-check:
   7/7 pass», the proposed commits; every number counted from disk) + *Review*
   (`docs/features/<slug>/screens.md`, `docs/features/<slug>/screens/`, + the design file when
   drawn) + *Run next*: build the screens in code following the manifest (one component at a time,
   no twins of inventory components) and fill §Source «State access» as you build, then
   `/sdlc:verify-ui <slug>`; in the backbone, `/clear`, then `/sdlc:break-tasks <slug>` with
   `docs/features/<slug>/screens.md` named in the prompt (it does not read the manifest on its own
   yet).

## Definition of Done

- `docs/features/<slug>/screens.md` exists: §Source per the canon's tool (or the named degradation),
  one section per `SCR-NN` with its state table, components reuse-first, §New components filled or
  «None».
- Every non-default state traces to a source token; nothing invented, nothing silently missing.
- Every screen has a row for each of the six classes (a real state or `N/A: <reason>`), plus its
  named states from flow branches.
- `tool` ≠ `code`: every state except an `N/A: <reason>` row has a node id and, when the session can
  export, a PNG at `docs/features/<slug>/screens/SCR-NN-<state>.png` that passed `test -s`; without
  an export capability the gap is named in §Source; an `N/A` row has neither. `code`: the wireframes
  are inline.
- `tool` ≠ `code`: the target-document check passed before every write; the design file was changed
  only through the tool's MCP; it was saved (a local file changed on disk, a cloud file read back).
- `tool` ≠ `code`: every state frame holds only its own layers (no hidden leftovers); every changed
  library component has its «Changed:» line and the «Оновити» advice; without write permission
  nothing was written into the designer's file except on the «Screens · <slug>» page the person
  allowed (state frames + «Drafts · <slug>», listed in the handoff), otherwise the run used `code`
  mode; the answer sits in the canon's «Screens write permission» line.
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
- **Calling a screenshot an export.** An image the tool shows only in the conversation is not on
  disk; without an export, name the gap.
- **Editing the design file by hand** (`.pen` JSON included), or writing into whatever document
  happens to be open.
- **Committing an unsaved design.** In pen.dev only a save (`save` tool or the user's Cmd+S) writes
  the `.pen` to disk; check it with `stat`.
- **Switching branches with the `.pen` open.** Save and close it first.
- **Blocking on a missing MCP.** `code` mode is always there; degrade with a named degradation.
- **Making downstream read the design file.** Node ids are for humans; the manifest carries
  everything code needs.
- **States made by hiding layers.** A copy of `default` with the other states' layers switched off
  looks right on the canvas and wrong in the Layers panel; each state frame holds only its layers.
- **Silently editing a library component.** A changed TabBar or Button without a «Changed:» line
  drifts from the canon and the code; in a designer's file it is never edited, only copied to
  «Drafts · <slug>» on the allowed «Screens · <slug>» page.
- **Writing into a designer's file without asking.** No write permission → one question about a
  separate «Screens · <slug>» page, else `code` mode; headless never writes there.
- **Shell chains and temp scripts.** `for … do`, `&&` and a script in `/tmp` are rejected headless
  and need a permission prompt each in an interactive run; one plain command per call.

## References & template

- [`./templates/screens.md`](./templates/screens.md) — the manifest scaffold; inline comments are
  the generation contract.
- [`../_shared/design-line.md`](../_shared/design-line.md) — provenance tokens, tool modes, the gates
  for every tool (§6), pen.dev (§7), Figma (§8), any other tool (§9), file layout.
- [`../_shared/surfaces.md`](../_shared/surfaces.md) — the `target_surfaces` gate when `sad.md` exists.
- [`../verify-ui/SKILL.md`](../verify-ui/SKILL.md) — reads this manifest (states + PNG paths) after
  the screens are built.
