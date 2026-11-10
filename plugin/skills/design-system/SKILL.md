---
name: design-system
model: inherit
effort: medium
agents: [explorer, design-keeper]
description: >
  Use to establish the project's design canon once per repo — docs/design/design-system.md: the
  design-tool choice (any design tool whose MCP the session has — pen.dev, Figma, others — or
  code-only markdown), the platform posture (mobile-first / desktop-first / responsive), the token
  source, the reusable component inventory, and the cross-screen conventions (errors, empty,
  loading, validation). Triggers on "set up the design system", "design canon", "which design
  tool", "establish the UI foundation", "/sdlc:design-system", "налаштуй дизайн-систему",
  "дизайн-канон проєкту", "яким інструментом малюємо", "зафіксуй токени і компоненти", "збери
  дизайн-систему з нуля", "build a design system from scratch". Read by
  ux-flows (posture), screens (tool + inventory), prepare-design-spec (reuse) and verify-ui. On a
  design tool it also prepares the design document (never by writing its file by hand), seeds the
  foundations and reconciles the document's component library (an existing library is recognized,
  never duplicated; a designer's file gets foundations only with permission) through the
  design-keeper agent, the same for every tool. A project with no tokens yet, or an empty one,
  gets its foundation built with the user: a short Socratic interview, references, 2–3 directions
  to choose from, then two-layer light/dark tokens in the project's theme file (or
  docs/design/tokens.json when there is no stack) with AA contrast checked, and a starter
  component set. Utility — run it before the first UI feature; works on a repo with no
  architecture map and on an empty project.
triggers:
  - /sdlc:design-system
  - "set up the design system"
  - "design canon"
  - "which design tool"
  - "налаштуй дизайн-систему"
  - "дизайн-канон проєкту"
  - "яким інструментом малюємо"
  - "збери дизайн-систему з нуля"
  - "build a design system from scratch"
stage: "util"
---

# Skill: design-system (SDLC design line — step 1, once per repo)

Fixes the **design canon** in `docs/design/design-system.md`: which tool screens are drawn with
(a design tool with an MCP — `pencil` for pen.dev, `figma`, another product name — or `code`), the
platform posture, where tokens come from, the component inventory every new screen must compose,
and the cross-screen conventions. `docs/architecture-map.md` §Frontend (when `map-architecture`
has run) stays the inventory of the **code**; this file is the **design-side** canon the design
line reads. The tool choice is committed here, team-wide — never in `.claude/sdlc.local.md`
(per-developer and gitignored).

File layout, the tool modes, the gates for every tool and the per-tool rules →
[`../_shared/design-line.md`](../_shared/design-line.md) §2, §6–§9. A project with no tokens
yet → [`./references/foundation.md`](./references/foundation.md) (step 4b).
Question phrasing → [`../_shared/ask-style.md`](../_shared/ask-style.md); depth per
[`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

Whoever owns the product's look: designer, frontend lead, or the solo developer.

## Inputs

- (Optional) `docs/architecture-map.md` §Frontend / UI foundation + its `frontend:` key — the code
  inventory this canon cites. **Absent is normal** in a young repo (module 5 has no map yet): the
  skill scans the code itself in step 2.
- (Optional) an existing `docs/design/design-system.md` — updated in place, never silently
  overwritten. Its design file is `design_file`, else a legacy synonym (design-line §6).
- (Optional) a starter design document the user already has (a course kit `.pen`, a teammate's
  library, a designer's Figma file).
- The design-tool MCPs this session actually has — probed in step 3.
- (Optional) references for a new foundation (links, screenshots, a Figma file, a brand book, a
  logo) — asked in step 4b when the project has no tokens.
- (Optional) `--depth=easy|medium|hard`, else `interview_depth` from `.claude/sdlc.local.md`, else
  `medium` — governs the step-4b interview only; this skill opens no depth question.

## Protocol

**Looking around, the cheap way.** Find files with Glob (`docs/design/*`, `src/components/ui/*`),
read them with Read, search with Grep; read this skill's template and the shared files by their
relative paths with Read. No `ls`, `wc` or `cat`, and nothing chained with `;`, `&&` or `|`: each
of them is a permission prompt on camera and a rejection headless.

1. **Check existing.** If `docs/design/design-system.md` exists, show its `tool`, posture and
   inventory size and ask (one `AskUserQuestion`): «Лишити як є» (STOP, nothing to do) /
   «Оновити» / «Перебудувати» (the full protocol from step 2). Never overwrite silently.
   **«Оновити»** keeps `tool`, posture, token source and every convention line a person edited;
   it reconciles the inventory and brings the document's token values in line with the code, in
   place:
   a. rescan the code side (step 2);
   b. `tool` ≠ `code` → run steps 5b–5e: design-keeper re-reads the document's reusable components
      and returns the library frame (persist only when it reports writes). `allow_writes` comes
      from the canon's «Foundations write permission» line as recorded (no such line, a canon from
      4.7 → the owner rule of step 5a decides); the question of step 5d is asked again only when
      the person says they want to change it (in the invocation or in the «Other» of this step's
      question);
      **token values that changed in the code** (a lesson changes `--primary` in the CSS, the
      document still has the old one): the keeper sorts the document's variables against the
      canon's token source into updated / added / left (design-keeper step 4). Who decides:
      - `design_file` is a repo path → dispatch with `update_values: true`, no question; the
        «before → after» list still goes into the report and the handoff;
      - a URL with write permission → dispatch with `update_values: false` first; the report's
        «changed, not written» list → one `AskUserQuestion` per
        [`../_shared/ask-style.md`](../_shared/ask-style.md) that **shows** the list
        («`primary`: `#2563eb` → `#7c3aed` (light)» …): «Оновити ці значення у файлі
        (Recommended)» → re-dispatch with `update_values: true` / «Лишити як є, записати список у
        канон»;
      - a URL without write permission, or headless on a URL → nothing written; the list goes
        under `## Assumptions` as «Proposed, not written: …».
      Variables the source does not have (a designer's own, or tokens deleted from the code) are
      never touched or deleted, only listed. New tokens from the code are added as before. The
      foundations sheet follows by itself; the keeper rewrites the numbers and value labels on it
      (design-line §7 rule 9 for pen.dev: the committed `.pen` is the copy before such a sync;
      `git status --porcelain -- <design_file>` shows uncommitted changes → say so in the question
      or the report);
   c. reconcile the inventory rows in place per step 5f: add new components, fill missing anchors,
      re-mark `design-only` / `code-only`; a row whose anchor no longer resolves is listed under
      `## Assumptions`, not deleted;
   d. a foundation that is only proposed (`## Assumptions` «Proposed, not written», a headless run)
      → offer to run step 4b with that proposal as direction A;
   e. write the sync result into §Token source «Last sync with the document» (date, updated N,
      added N, left N, counted from the keeper's read-back); when the canon has a «Contrast» table
      and a colour in it changed, recompute those pairs (one inline command) and update the table,
      naming a pair that now fails AA in the handoff; bump `updated_at`, then run steps 6 and 7;
      the handoff names every updated value (before → after), every added token and every
      variable left alone.

2. **Scan the code side.** Read `docs/architecture-map.md` §Frontend if it exists and is current.
   Otherwise dispatch the [`explorer`](../../agents/explorer.md) agent **in the foreground**
   (`run_in_background: false`: the canon is written from its map, so wait for it; never end the
   turn with «сканування ще триває, чекаю») — `subagent_type: "sdlc:explorer"` (fallback
   `subagent_type: "Explore"`, per [`../_shared/agent-roster.md`](../_shared/agent-roster.md)). Its
   prompt says: read files with Read, list with Glob, search with Grep (a JSON token file too, with
   Read), no `python`, `ls`, `wc` and no `;` / `&&` / `|` chains. It maps: the component library
   (e.g. `components/ui/`), the token files (CSS variables, theme config), the styling approach, and
   the shared primitives, each with a `file:line`. **No token files found** (by the map or the
   scan) → the explorer also scans for values written straight into styles (colours, font sizes,
   spacing, radii) with their count and `file:line`, per
   [`./references/foundation.md`](./references/foundation.md) §2: in the same dispatch, or in a
   dispatch for that scan alone when the map was used (only the prompt changes; the agent is
   shared). Then name the case: **A** token files exist;
   **B** no token files, but UI code or written-in values; **C** empty project: no token files, no
   UI components, no written-in values (possibly no stack at all). A repo with no UI code yet is
   fine: case C builds its foundation in step 4b, and the inventory grows as screens add `NEW:`
   components.

3. **Detect tools, then ask ONE question set.** List the session's MCP tools, deferred ones
   included, and keep every server that can read a design document's nodes, per
   [`../_shared/design-line.md`](../_shared/design-line.md) §6 «What counts as a design tool»
   (pen.dev: `get_app_state` / `execute`; Figma Console: `figma_get_status` / `figma_execute`;
   official Figma: `get_metadata` / `use_figma`; any other by its tools) — don't assume. Then **one
   `AskUserQuestion` call** with up to 3 questions:
   **(a) tool** — every detected design tool as its own option, named by its product (`pencil`,
   `figma`, `<name>`); first, as «(Recommended)», the one whose document already sits in the repo
   or the conversation, else the only one detected; more than 3 detected → the 3 most likely, the
   rest through «Other». `code` (markdown wireframes) is **always** offered, needs no MCP and never
   blocks. Each description says what the tool can do in this session (write? export PNG?) per
   §6 «Capabilities»; **(b) platform posture** — mobile-first / desktop-first / responsive-both,
   the one the code suggests first as «(Recommended)» (its breakpoints, the layout of its
   screens); **(c) token source** — case A: the code file(s) from step 2 «(Recommended)» / the
   tool's variables / «ще немає»;
   case B: «Зібрати з того, що знайдено в коді» (Recommended when values were found) / «Стартова
   основа» / «Лишити без токенів»; case C: «Зібрати основу разом» (Recommended) / «Лишити без
   токенів»; in B and C also «Взяти зі змінних інструмента» when the design document already holds
   variables (per [`./references/foundation.md`](./references/foundation.md) §1). Each description
   says what happens next: the building options start the short interview of step 4b, nothing is
   written before the person picks a direction.
   A cloud tool whose file URL is not in the repo or the conversation → after the answers, ask for
   the URL in one plain sentence. No question channel (headless) → pick the detected tool or `code`,
   the posture the code suggests, the token files found (cases B and C: the headless path of
   [`./references/foundation.md`](./references/foundation.md) §7); record them under
   `## Assumptions` per [`../_shared/design-line.md`](../_shared/design-line.md) §5.

4. **Write the canon, building the foundation first when there is none.**
   a. **The canon, section by section.** Read
      [`./templates/design-system.md`](./templates/design-system.md) with Read and write it with
      Write to `docs/design/design-system.md` right after step 3 (never `cp` from the plugin's
      folder: Claude Code treats the plugin cache as a sensitive path and stops for a permission
      prompt; Write creates `docs/design/` itself), then write each
      part as soon as it is decided: frontmatter `tool` + `design_file` (`""` on `code`; never
      write a legacy synonym from design-line §6 into a new canon), posture, token source, the
      component inventory (every row cites `file:line` for code, the node/URL for tool-side
      components, or `starter set` for a starter row not drawn yet), and the conventions (when the
      foundation was not built in step 4b: read them from the code, from how its components show
      errors, empty lists, loading and validation, each marked `derived` under `## Assumptions`;
      no question for them). Default
      `design_file`: a tool with files on disk → the one file of that tool already under
      `docs/design/` (a kit, a teammate's file) when there is exactly one, else
      `docs/design/<project>.<ext>` (`.pen` on pencil); a cloud tool → the URL from step 3.
      `library_frame`, «Agent access», «Foundations write permission» and the tool-side inventory
      rows come from the design-keeper report (step 5f).
   b. **Build the foundation** — only when step 3 (c) chose to build one (cases B and C), per
      [`./references/foundation.md`](./references/foundation.md). A short Socratic interview at the
      run's depth (§3: round 1 on context, the references asked in plain text and read, round 2
      follow-ups at medium / hard), then 2–3 directions with hex palette, font pair, radii,
      density and a why-line, each contrast-checked; on a design tool with an empty document that
      may be written (step 5a's owner rule gives `allow_writes: true`) `design-keeper` draws them
      side by side (`mode: directions`, after step 5a–5b), else a markdown table. The person picks or mixes, one «що змінити» round, and only then: the
      starter foundation (§4: palette + semantic layer per theme, type scale, 4 px spacing, radii,
      every «text on background» pair at AA, computed), written as tokens (§5) into the project's
      theme file the person names (no stack → `docs/design/tokens.json`, DTCG), shown as a diff and
      proposed as its own commit. Case C also writes the starter component set (§6) into the
      inventory as `design-only` rows. The answers, the references and every decision with its
      source go into `## Sources` and `## Assumptions` (§8). **Headless** → no interview, nothing
      written but the canon: one proposed direction under `## Assumptions` (§7).

5. **Prepare the design document** (`tool` ≠ `code`; `code` needs nothing). A canon that names a
   design file nobody created, or a Figma link nobody reconciled, is the #1 way this skill «did
   nothing». Rules per [`../_shared/design-line.md`](../_shared/design-line.md) §6 and the tool's
   section (§7 pen.dev, §8 Figma, §9 any other):
   a. **Document.** A tool with files on disk and no file at `design_file` → either copy a starter
      the user names (`cp <kit>.pen <design_file>`) or ask the user to create a new document in the
      tool and save it at `design_file`. **Never write the tool's file format yourself**, not even
      an «empty stub». A cloud tool: the file lives at its URL; a new one is created by the user in
      the tool (or with the tool's own create-file tool when the session has one).
      **Who may write** (design-line §6 gate 6, the file's owner decides): `design_file` is a repo
      path → it belongs to the person running the skill, `allow_writes: true`, no question, headless
      too; a URL the person created in this run → `true`; any other URL, empty or with a library →
      `false` for the first dispatch, then the step-5d question.
   b. **Open + verify.** Ask the user to open the document where the tool's MCP can reach it:
      pen.dev → open `design_file` in pen.dev (macOS: `open <design_file>`); Figma Console → open the
      URL in Figma Desktop and run the Desktop Bridge plugin in it (Plugins → Development); the
      official Figma MCP → nothing to open, the account needs edit access for writes. Then check
      with the tool's target-document tool (`get_app_state`, `figma_list_open_files`, a first read
      of the file) that the target IS `design_file` (paths or file keys, §6 gate 1). Mismatch →
      stop and repeat the ask; never write into a foreign document. (Step 4b may already have run
      5a–5b for the directions sheet; then only re-check the target here.)
   c. **Reconcile.** Dispatch the [`design-keeper`](../../agents/design-keeper.md) agent in the
      foreground (`run_in_background: false`) — `subagent_type: "sdlc:design-keeper"` (no fallback: without the tool's MCP this step degrades
      to `code` mode) — with the canon path, `tool`, `design_file`, `library_frame` (empty on a
      first run), the token source files (those step 4b wrote included), the inventory (starter
      rows included), `allow_writes` (per step 5a's owner rule, or the person's yes in 5d), and
      `mode`: `reconcile` by default, `inventory` (read-only: recognize and report, write nothing)
      when the foundation is only proposed (headless step 4b); plus the node id of the
      «DS · Directions» frame from the step-4b report when there was one. In `reconcile` it first
      removes that frame, only when both the id and the exact name match. It finds the tool's tools
      and reads the tool's guide, re-checks the target document, recognizes the library frame (the
      one the canon names, else the frame that holds the reusable components; «DS · Foundations»
      is created only in a document with none), seeds the missing foundations for every group
      (colours, radii, typography, spacing; light + dark when the source has both), and returns a
      reconcile report with every reusable component by name + node id + variants. Only in a
      document with no reusable components, and only with `allow_writes: true`, it draws the
      foundations sheet in the one layout of design-line §6 (colours per theme, typography, spacing,
      radii) and the components with all their variants and states below it; in a document that
      already has a library it draws nothing. Without `allow_writes` it writes nothing and
      proposes.
   d. **Permission for a file at a URL.** The report says `writes: none — proposals: N` (a URL
      file not created in this run, `allow_writes` was `false`) → one `AskUserQuestion` per
      [`../_shared/ask-style.md`](../_shared/ask-style.md) that **shows** the proposals (count per
      group, the first names with values, and in an empty file «would draw: the foundations sheet +
      N components») and says whose file it is: «Лише записати пропозицію в канон
      (Recommended)» → nothing is written into the file (it is someone else's) / «Дозволити запис у
      файл» → re-dispatch design-keeper with `allow_writes: true` (it re-checks the gate, adds only
      what is missing, never overwrites). The description of «Лише записати пропозицію» says
      plainly that `screens` will then ask once whether it may draw on a separate page «Screens ·
      <slug>» in this file, and otherwise use markdown wireframes. No question channel (headless)
      → no permission, the same as that option. Either way the proposals go under the canon's
      `## Assumptions` as «Proposed, not written: …». A tool with no write tool skips the question
      and records the proposals the same way.
   e. **Persist.** Read the report's `saved:` line; the keeper did the `stat` / read-back. «saved
      via `save`» or «saves by itself» → done. «NOT saved: the user must save» → relay it («Cmd+S у
      pen.dev: зміни поки лише в памʼяті застосунку»), then, after the user says done, `stat` the
      local file once and compare with the report's «before». `writes: none` → nothing to save; a
      local file is expected unchanged.
   f. **Merge the report into the canon.** Write the report's library frame name to `library_frame`
      (and §Design tool «Library location»; the report says «none» → leave it `""` and add
      «library_frame empty: <the report's reason>» under `## Assumptions`), its tool and
      capabilities to «Agent access», and the permission to «Foundations write permission»: «repo
      file — written without asking» / «created in this run — written» / «allowed by the person,
      <YYYY-MM-DD>» / «not allowed — proposals under Assumptions». With «not allowed», also write
      «Screens write permission: not asked yet» (`screens` asks and rewrites it); otherwise «N/A
      (writes allowed)». `screens` and «Оновити» read these lines. Merge its components into the
      inventory: a component present in code and in the document = one row with both anchors
      (`file:line` · node id); only in the document = a row with the node id, Notes `design-only`;
      only in code = Notes `code-only`. Every component the report lists gets a row, so `screens`
      never marks one of them `NEW:`. Components the report lists under «Drafts · <slug>» (on a
      «Screens · <slug>» page) are not library rows: each gets a row with its node id and Notes
      `draft — Drafts · <slug>, waiting for the designer`, and a changed copy keeps pointing at the
      original's row.
      **Pairing.** Code and document rarely share names (`Badge` in code, «Tag / Neutral» in the
      kit). Pair by the project's own map when the repo has one (e.g. a «.pen → code» list in
      `AGENTS.md`), else by the name family (the part before ` / `: «Button / Primary / Large» ↔
      `Button`; a Figma component set's name ↔ the code component). No certain pair → keep two
      rows (`design-only`, `code-only`) and list the candidates under `## Assumptions`; never
      guess. A `code-only` row is not `NEW:` either: `screens` draws that component into the
      library frame the first time a screen needs it (without write permission only in «Drafts ·
      <slug>» on a «Screens · <slug>» page the person allowed).
      **The binding lives in the canon, design ↔ code props included.** A row with both anchors
      also gets its «Design ↔ code props» cell: the design's variant properties paired with the
      props the code really has, read from the code (e.g. the `cva` `variants` block of
      `src/components/ui/button.tsx`), never invented. Figma (a component set): `Variant=Outline ↔
      variant="outline"` · `Size=Large ↔ size="lg"`; pen.dev (a component per variant): `Button /
      Outline / Large ↔ variant="outline" size="lg"`. Pair values by name (`Outline` ↔
      `outline`; `Small` / `Medium` / `Large` ↔ the code's own `sm` / `md` / `lg`). **The middle
      value with no name of its own is the code's default**: read `defaultVariants` (`Size=Medium
      ↔ size="default"` when the code has `default` and no `md`; a component description that says
      «Medium = default» confirms it). **Text properties too**: a component's text property (Figma
      TEXT property: `Label`, `Name`, `Initials`, `Placeholder`) ↔ the prop or children that
      carries that text in the code (`Label ↔ children`, `Name ↔ title`, `Initials ↔ initials`).
      An uncertain pair goes under `## Assumptions`; a design value with no prop in the code, or
      a prop only the code has (`variant="link"`), is named, not mapped. When the session's official Figma server returns Code Connect for the component
      (`get_code_connect_map`, or the props in a `<CodeConnectSnippet>`, design-line §8), take the
      mapping from it and write «from Code Connect» in the cell.

6. **Structural self-check** — re-read the file **from disk** and verify **7 items**. Count and
   check with Read and Grep (Grep's count mode for rows), or one plain command per call
   (`test -s <file>`); never a composed Bash command with `$(…)`, pipes or `&&`, which is rejected
   headless and stops an interactive run for a permission prompt:
   (1) `tool` is `code` or a lowercase design-tool name (`pencil`, `figma`, `<name>`), never empty;
   (2) the tool ↔ file fields agree — `tool` ≠ `code` ⇒ the design file (`design_file`, else a
   legacy synonym per design-line §6) is non-empty, and `library_frame` is non-empty unless the
   keeper reported «none» (a read-only tool, no library and no permission to write, `inventory`
   mode), in which case `## Assumptions` has the «library_frame empty: <reason>» line; «Foundations
   write permission» is filled; `code` ⇒ `design_file`, `library_frame` and any legacy field are
   `""` or absent;
   (3) every inventory row carries a source anchor (`file:line`, node/URL, or `starter set` for a
   starter row not drawn yet), and on a design tool every component in the design-keeper report
   has a row; every row with both anchors and design variants has its «Design ↔ code props» cell
   (read from the code, or «from Code Connect»);
   (4) no template `<placeholder>` survives outside comments (the frame-name pattern
   `<slug> · SCR-NN · <state>` in §Design tool is a naming pattern, not a placeholder);
   (5) `tool` ≠ `code`: the report's target-document check said PASS; a local design file passes
   `test -s`; and either the report says `writes: none` (everything matched, or the proposals are
   under `## Assumptions`) or the write was checked — a local file changed on disk (step 5e), a URL
   has the keeper's read-back in its `saved:` line; no «DS · Directions» frame is left in the
   document; on «Оновити», a changed value was written only per the owner rule (a repo path, or a
   URL after the person's yes), and «Last sync with the document» matches the keeper's report;
   (6) step 4b ran → `## Sources` lists every reference (read or unread) and `## Assumptions` every
   decision with its source tag (`answer` / `ref:N` / `derived`); interactive: the tokens file
   exists (`test -s`; `docs/design/tokens.json` parses with `python3 -m json.tool`), holds both
   layers and every chosen theme, and §Token source «Contrast» lists every «text on background»
   pair per theme at AA, computed; headless: nothing was written into code or a tokens file
   (`git status --porcelain` shows only the canon) and the proposal sits under `## Assumptions`;
   (7) case C → the starter component set (foundation.md §6) is in the inventory with its
   variants, as `design-only` rows (interactive) or under `## Assumptions` (headless).
   Fix and re-check at most 2 cycles; surface anything unresolved — never silently.

7. **Propose commits + handoff.** Propose one commit for the canon
   (`design-system: docs/design/design-system.md`) and, when the design file is a local path, a
   separate one for it (`design-system: <design_file> library`) only when
   `git status --porcelain -- <design_file>` shows it changed, and when step 4b wrote tokens, a
   separate one for that file with its diff (`design-system: tokens in <file>`). Unresolved
   self-check item → propose no commit and say why. **Every number in the handoff is counted from
   disk after the last write** (inventory rows, components, variables, references: count the rows
   in the file as written with Read or Grep, never from memory: a handoff once said 34 rows where
   the file had 31); the keeper's numbers come from its read-back of the document.
   Then emit the **stage-handoff block** per
   [`../_shared/handoff.md`](../_shared/handoff.md), utility variant — *What I did* (tool, posture,
   inventory size, the foundation's origin and the chosen direction, foundations written /
   proposed, «self-check: 7/7 pass», the proposed commits) + *Review*
   (`docs/design/design-system.md`, + the design file, + the tokens file) + *Run next*:
   `/sdlc:ux-flows <slug>` for the UI feature in flight; when `AGENTS.md` does not have it yet
   (check with Grep), **one line of proposal in the handoff, no question and no write**: «Можна
   додати в `AGENTS.md` рядок: UI бери з інвентаря `docs/design/design-system.md`; новий компонент
   лише якщо його там нема» (not a table); when step 4b wrote tokens into a project
   with written-in values, name the follow-up code task «replace the written-in values with the
   tokens»; `/clear` optional.

## Definition of Done

- `docs/design/design-system.md` exists with `tool` = `code` or a design-tool name, a stated
  platform posture, a token source, conventions, and an inventory whose every row cites its source.
- The tool ↔ `design_file` / `library_frame` fields agree.
- `tool` ≠ `code` ⇒ the design document was reached through its MCP behind the target-document
  gate; permission followed the file's owner (a repo file written without asking, a URL file only
  after the person's yes) and is recorded in «Foundations write permission»; the document holds
  the seeded foundations, or, without permission, the missing ones are listed under
  `## Assumptions`; its component library is named in `library_frame` (recognized, or created only
  in an empty document; empty only with the keeper's reason under `## Assumptions`), with no second
  library beside it; an empty document got the foundations sheet in the one layout of
  design-line §6; every reusable component in the document has an inventory row; every write was saved and
  checked (a local file changed on disk, a URL read back); no «DS · Directions» frame is left. No
  byte of the design file was written by hand.
- A project with no token files that chose to build one (step 4b) ⇒ the interview really ran at
  its depth (the questions fired, the references were asked for and read or listed as unread), the
  person picked a direction before anything was written; the tokens sit in two layers with every
  chosen theme in the file the person named (or `docs/design/tokens.json`, DTCG), every «text on
  background» pair passes AA in every theme with its computed ratio in the canon, no colour the
  person gave was changed silently; the change was shown as a diff and proposed as its own
  commit; `## Sources` and `## Assumptions` carry the references and every decision with its
  source. Case C: the starter component set is in the inventory and, on a design tool with an
  empty document, drawn with the foundations sheet.
- Headless ⇒ nothing but the canon was written: one proposed direction, its foundation and (case C)
  the starter set under `## Assumptions`.

## Anti-patterns

- **The tool choice in `.claude/sdlc.local.md`.** Two teammates would draw in different tools; the
  canon is committed, in this one file.
- **Re-asking the tool per feature.** `ux-flows` / `screens` read the canon; the question is asked
  once, here.
- **Copying `architecture-map.md` §Frontend.** The map inventories the code; this file cites it and
  adds the design side, never a second copy of the same rows.
- **Blocking on a missing MCP.** No MCP for the chosen tool in the session → `code` mode; degrade,
  don't block.
- **A Figma link nobody reconciles.** Writing the URL into the canon and stopping leaves the
  inventory blind to the designer's library; design-keeper reads it like any other document.
- **An inventory row without an anchor.** A component that cites nothing is a guess.
- **A second library next to the kit's.** A starter document already holds its components under
  its own frame name; a new «DS · Foundations» beside it creates twin Button / Input / Badge, and
  the kit-only components (Toast, Spinner …) never reach the inventory, so `screens` marks them `NEW:`.
- **Writing into a designer's file without asking.** A file at a URL that the person did not
  create in this run belongs to someone else: no foundations and nothing in its library before
  the step 5d «yes» (`screens` then asks for a separate «Screens · <slug>» page, else uses
  markdown wireframes). A repo file is
  the person's own and is written without asking.
- **Judging ownership by what is inside.** An empty Figma file can still be a designer's, and a
  repo `.pen` with a kit's library is still the person's: the owner rule looks at where the file
  lives (design-line §6 gate 6).
- **Handoff numbers from memory.** Count rows and components in the written file.
- **Writing a design-file stub by hand.** The format belongs to the tool; create the file in the
  tool or copy a real one.
- **Writing into whatever document is open.** Older Pencil servers write into the active document,
  newer ones into the `uri` of an open one, Figma Console into the active Desktop Bridge file;
  skipping the target-document check pollutes a foreign file.
- **Assuming an edit is saved.** In pen.dev it lives in the app's memory until `save` (or the user's
  Cmd+S); confirm a local file with `stat`, a cloud file with a read-back.
- **«Ще немає» as a dead end.** A project without tokens gets a foundation built with the person
  (step 4b); leaving it empty is their explicit choice, not the default.
- **One question instead of an interview.** A palette picked from a single question is the
  agent's taste; the rounds, the references and the directions are what make it the person's.
- **Writing tokens before the choice.** Nothing goes into code or a tokens file, and nothing but
  the temporary «DS · Directions» sheet into the design document, until a direction is picked.
- **Contrast by eye.** Compute every «text on background» ratio; a brand colour the person gave is
  never shifted silently to pass.
- **Inventing answers when nobody can be asked.** Headless proposes one direction under
  `## Assumptions` and writes nothing else.

## References & template

- [`./templates/design-system.md`](./templates/design-system.md) — the canon scaffold; inline
  comments are the per-section contract.
- [`../_shared/design-line.md`](../_shared/design-line.md) — layout, tool modes, the gates for every
  tool (§6), pen.dev (§7), Figma (§8), any other tool (§9).
- [`../_shared/agent-roster.md`](../_shared/agent-roster.md) — `explorer` / `design-keeper` dispatch.
- [`../../agents/design-keeper.md`](../../agents/design-keeper.md) — the reconcile contract for any
  design tool (step 5c) and its `directions` / `inventory` modes.
- [`./references/foundation.md`](./references/foundation.md) — no tokens yet: the cases, the
  written-in value scan, the interview, the directions, the starter foundation, writing the
  tokens, the starter component set, headless (step 4b).
- [`../_shared/interview-depth.md`](../_shared/interview-depth.md) ·
  [`../interview/SKILL.md`](../interview/SKILL.md) — the depth dial and the Socratic manner the
  step-4b interview follows.

## Example invocation

```text
/sdlc:design-system
```

In an empty project with no stack, pen.dev connected, an interactive session:

1. Step 2: `explorer` finds no token files, no UI components, no written-in values → case C.
2. Step 3: one question set → tool `pencil` (Recommended: the only design MCP), posture
   `mobile-first`, token source «Зібрати основу разом» (Recommended).
3. Step 4b at `medium`: round 1 (character «спокійний і надійний», a logo exists, like a banking
   app, both themes) → the person sends a link and the logo path, the skill reads both and lists
   the signals in `## Sources` → round 2: «Що буде, якщо основний синій стоятиме поруч із червоною
   помилкою?» → step 5a–5b create and open an empty `.pen`, 3 directions drawn in «DS · Directions»
   → «Змішати»: palette
   of B, fonts of A → no stack, so `docs/design/tokens.json` (DTCG), every pair at AA, the diff
   shown → the starter set in the inventory as `design-only`.
4. Step 5: `design-keeper` removes «DS · Directions», seeds the variables, draws «DS · Foundations»
   (the sheet + Button × variants × sizes, Input states, Badge, Avatar, Card, Header + Tab bar),
   saves, reports.
5. Steps 6–7: self-check 7/7, three proposed commits (canon, `.pen`, tokens), *Run next*
   `/sdlc:ux-flows <slug>`.
