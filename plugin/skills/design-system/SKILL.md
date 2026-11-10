---
name: design-system
model: inherit
effort: medium
agents: [explorer, pen-keeper]
description: >
  Use to establish the project's design canon once per repo — docs/design/design-system.md: the
  design-tool choice (pen.dev via Pencil MCP / Figma MCP / code-only markdown), the platform
  posture (mobile-first / desktop-first / responsive), the token source, the reusable component
  inventory, and the cross-screen conventions (errors, empty, loading, validation). Triggers on
  "set up the design system", "design canon", "which design tool", "establish the UI foundation",
  "/sdlc:design-system", "налаштуй дизайн-систему", "дизайн-канон проєкту", "яким інструментом
  малюємо", "зафіксуй токени і компоненти". Read by ux-flows (posture), screens (tool + inventory),
  prepare-design-spec (reuse) and verify-ui. On tool: pencil it also prepares the .pen document
  (never by writing its JSON), seeds tokens and reconciles the document's component library (an
  existing library is recognized, never duplicated) through the pen-keeper agent.
  Utility — run it before the first UI feature; works on a repo with no architecture map.
triggers:
  - /sdlc:design-system
  - "set up the design system"
  - "design canon"
  - "which design tool"
  - "налаштуй дизайн-систему"
  - "дизайн-канон проєкту"
  - "яким інструментом малюємо"
stage: "util"
---

# Skill: design-system (SDLC design line — step 1, once per repo)

Fixes the **design canon** in `docs/design/design-system.md`: which tool screens are drawn with
(`pencil` / `figma` / `code`), the platform posture, where tokens come from, the component inventory
every new screen must compose, and the cross-screen conventions. `docs/architecture-map.md`
§Frontend (when `map-architecture` has run) stays the inventory of the **code**; this file is the
**design-side** canon the design line reads. The tool choice is committed here, team-wide — never in
`.claude/sdlc.local.md` (per-developer and gitignored).

File layout, the tool modes and the pen.dev rules → [`../_shared/design-line.md`](../_shared/design-line.md).
Question phrasing → [`../_shared/ask-style.md`](../_shared/ask-style.md).

## Owner

Whoever owns the product's look: designer, frontend lead, or the solo developer.

## Inputs

- (Optional) `docs/architecture-map.md` §Frontend / UI foundation + its `frontend:` key — the code
  inventory this canon cites. **Absent is normal** in a young repo (module 5 has no map yet): the
  skill scans the code itself in step 2.
- (Optional) an existing `docs/design/design-system.md` — updated in place, never silently overwritten.
- (Optional) a starter `.pen` file the user already has (a course kit, a teammate's library).
- The design-tool MCPs this session actually has (Pencil / Figma) — probed in step 3.

## Protocol

1. **Check existing.** If `docs/design/design-system.md` exists, show its `tool`, posture and
   inventory size and ask (one `AskUserQuestion`): «Лишити як є» (STOP, nothing to do) /
   «Оновити» / «Перебудувати» (the full protocol from step 2). Never overwrite silently.
   **«Оновити»** keeps `tool`, posture, token source and every convention line a person edited;
   it only reconciles the inventory, in place:
   a. rescan the code side (step 2);
   b. `tool: pencil` → run step 5b–5d: pen-keeper re-reads the document's reusable components and
      returns the library frame (persist only when it reports writes);
   c. reconcile the inventory rows in place per step 5e: add new components, fill missing anchors,
      re-mark `design-only` / `code-only`; a row whose anchor no longer resolves is listed under
      `## Assumptions`, not deleted;
   d. bump `updated_at`, then run steps 6 and 7.

2. **Scan the code side.** Read `docs/architecture-map.md` §Frontend if it exists and is current.
   Otherwise dispatch the [`explorer`](../../agents/explorer.md) agent — `subagent_type:
   "sdlc:explorer"` (fallback `subagent_type: "Explore"`, per
   [`../_shared/agent-roster.md`](../_shared/agent-roster.md)) — for: the component library
   (e.g. `components/ui/`), the token files (CSS variables, theme config), the styling approach, and
   the shared primitives, each with a `file:line`. A repo with no UI code yet is fine: the canon
   starts with tokens only and the inventory grows as screens add `NEW:` components.

3. **Detect tools, then ask ONE question set.** Probe which design-tool MCPs this session has
   (Pencil: `get_app_state`/`execute`; Figma: its read/write tools) — don't assume. Then **one
   `AskUserQuestion` call** with up to 3 questions:
   **(a) tool** — the detected tool first as «(Recommended)»; `code` (markdown wireframes) is
   **always** offered, needs no MCP and never blocks; **(b) platform posture** — mobile-first /
   desktop-first / responsive-both; **(c) token source** — the code file(s) from step 2 / the tool's
   variables / «ще немає». No question channel (headless) → pick the detected tool or `code`, the
   posture the code suggests, the token files found; record them under `## Assumptions` per
   [`../_shared/design-line.md`](../_shared/design-line.md) §5.

4. **Write the canon section by section.** Copy [`./templates/design-system.md`](./templates/design-system.md)
   to `docs/design/design-system.md` (`mkdir -p docs/design`) right after step 3, then write each
   part as soon as it is decided: frontmatter `tool` + `pen_file` / `figma_file` (only the one
   matching the tool; the other stays `""`), posture, token source, the component inventory (every
   row cites `file:line` for code or the node/URL for tool-side components), and the conventions.
   On `pencil` the default `pen_file` is the one `.pen` that already exists under `docs/design/`
   (a kit, a teammate's file) when there is exactly one; else `docs/design/<project>.pen`.
   `library_frame` and the tool-side inventory rows come from the pen-keeper report (step 5e).

5. **Prepare the pen.dev document** (`tool: pencil` only — figma links an existing file, `code` needs
   nothing). A canon that names a `pen_file` nobody created is the #1 way this skill «did nothing».
   Rules per [`../_shared/design-line.md`](../_shared/design-line.md) §7:
   a. **File.** `pen_file` absent → either copy a starter the user names (`cp <kit>.pen <pen_file>`)
      or ask the user to create a new document in pen.dev and save it at `pen_file`. **Never write
      `.pen` JSON yourself**, not even an «empty stub».
   b. **Open + verify.** Ask the user to open `pen_file` in pen.dev (macOS: `open <pen_file>`), then
      check with `get_app_state` that the active document IS `pen_file`. Mismatch → stop and repeat
      the ask; never write into a foreign document.
   c. **Seed.** Dispatch the [`pen-keeper`](../../agents/pen-keeper.md) agent — `subagent_type:
      "sdlc:pen-keeper"` (no fallback: without the Pencil MCP this step degrades to `code` mode) —
      with the canon path, `pen_file`, `library_frame` (empty on a first run), the token source
      files and the inventory. It re-checks the active document, recognizes the document's library
      frame (the one the canon names, else the frame that holds the reusable components;
      «DS · Foundations» is created only in a document with none), seeds the variables (light +
      dark when the source has both), and returns a reconcile report with every reusable component
      by name + node id. It draws core primitives only in a document with no reusable components;
      in a document that already has a library it draws nothing.
   d. **Persist.** Report `writes: N` → relay «Cmd+S у pen.dev» and confirm the file on disk changed
      (`stat` mtime/size before vs after) before calling the canon done. Report `writes: none` →
      nothing to save; the file is expected unchanged.
   e. **Merge the report into the canon.** Write the report's library frame name to `library_frame`
      (and §Design tool «Library location»). Merge its components into the inventory: a component
      present in code and in the document = one row with both anchors (`file:line` · node id); only
      in the document = a row with the node id, Notes `design-only`; only in code = Notes
      `code-only`. Every component the report lists gets a row, so `screens` never marks one of
      them `NEW:`.
      **Pairing.** Code and document rarely share names (`Badge` in code, «Tag / Neutral» in the
      kit). Pair by the project's own map when the repo has one (e.g. a «.pen → code» list in
      `AGENTS.md`), else by the name family (the part before ` / `: «Button / Primary / Large» ↔
      `Button`). No certain pair → keep two rows (`design-only`, `code-only`) and list the
      candidates under `## Assumptions`; never guess. A `code-only` row is not `NEW:` either:
      `screens` draws that component into the library frame the first time a screen needs it.

6. **Structural self-check** — re-read the file **from disk** and verify **5 items**:
   (1) `tool` ∈ {pencil, figma, code};
   (2) the tool ↔ file fields agree — `pencil` ⇒ `pen_file` and `library_frame` non-empty,
   `figma` ⇒ `figma_file` non-empty, `code` ⇒ all three `""`;
   (3) every inventory row carries a source anchor (`file:line` or node/URL), and on `pencil`
   every component in the pen-keeper report has a row;
   (4) no `<placeholder>` survives outside comments;
   (5) `tool: pencil` ⇒ `test -s <pen_file>` passes, and either step 5d saw the file change on disk
   or the pen-keeper report says `writes: none` (everything already matched).
   Fix and re-check at most 2 cycles; surface anything unresolved — never silently.

7. **Propose commits + handoff.** Propose one commit for the canon
   (`design-system: docs/design/design-system.md`) and, on pencil, a separate one for the `.pen`
   (`design-system: <pen_file> library`) only when `git status --porcelain -- <pen_file>` shows it
   changed. Unresolved self-check item → propose no commit and say why. Then emit the
   **stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md), utility variant —
   *What I did* (tool, posture, inventory size, «self-check: 5/5 pass», the proposed commits) +
   *Review* (`docs/design/design-system.md`, + `pen_file`) + *Run next*: `/sdlc:ux-flows <slug>` for
   the UI feature in flight; `/clear` optional.

## Definition of Done

- `docs/design/design-system.md` exists with `tool` ∈ {pencil, figma, code}, a stated platform
  posture, a token source, conventions, and an inventory whose every row cites its source.
- The tool ↔ `pen_file` / `figma_file` fields agree.
- `tool: pencil` ⇒ the `.pen` exists on disk and is not empty, holds the seeded token variables and
  its component library frame (recognized, or created only in an empty document) named in
  `library_frame`, with no second library beside it; every reusable component in the document has
  an inventory row; the user saved it whenever pen-keeper wrote anything. No `.pen` byte was
  written by hand.

## Anti-patterns

- **The tool choice in `.claude/sdlc.local.md`.** Two teammates would draw in different tools; the
  canon is committed, in this one file.
- **Re-asking the tool per feature.** `ux-flows` / `screens` read the canon; the question is asked
  once, here.
- **Copying `architecture-map.md` §Frontend.** The map inventories the code; this file cites it and
  adds the design side, never a second copy of the same rows.
- **Blocking on a missing MCP.** No Pencil/Figma in the session → `code` mode; degrade, don't block.
- **An inventory row without an anchor.** A component that cites nothing is a guess.
- **A second library next to the kit's.** A starter document already holds its components under
  its own frame name; a new «DS · Foundations» beside it creates twin Button / Input / Badge, and
  the kit-only components (Toast, Spinner …) never reach the inventory, so `screens` marks them `NEW:`.
- **Writing a `.pen` stub by hand.** The format belongs to the app; create the file in pen.dev or
  copy a real one.
- **Writing into whatever document is open.** The Pencil MCP targets the ACTIVE document; skipping
  the `get_app_state` check pollutes a foreign file.
- **Assuming the MCP saved to disk.** It edits in memory; only the user's Cmd+S persists.

## References & template

- [`./templates/design-system.md`](./templates/design-system.md) — the canon scaffold; inline
  comments are the per-section contract.
- [`../_shared/design-line.md`](../_shared/design-line.md) — layout, tool modes, pen.dev rules.
- [`../_shared/agent-roster.md`](../_shared/agent-roster.md) — `explorer` / `pen-keeper` dispatch.
- [`../../agents/pen-keeper.md`](../../agents/pen-keeper.md) — the `.pen` reconcile contract (step 5c).
