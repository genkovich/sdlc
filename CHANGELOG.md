# Changelog

All notable changes to the `sdlc/` toolkit and `sdlc` Claude Code plugin.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [4.9.1] — 2026-11-10

### Fixed — after the Figma rehearsal of 4.9.0 (design-system → screens in read mode)

The run on the Figma file «Threads Premium» passed both self-checks (7/7) and left the file
unchanged but for one side effect (below). What the text got wrong:

- **Read mode with no flows, story or spec is a full read.** The text sent it to the ladder's
  «ask for 3–5 sentences». Now the designer's frames are the source: screens from the frame names,
  row labels and groups, `input: frames` (a new value in `screens.md`), named states from frame
  names with the new token `frame:<node id>` (not `D-NN`), no question for a story; it stops only
  when the link holds no frames (`_shared/design-line.md` §3, `read-frames.md` §2, `screens`
  inputs and self-check item 3).
- **`figma_get_annotations` wrote into the file.** It created the four preset annotation
  categories (`isPreset: true`) while read mode promised «nothing is written». Annotations are now
  read as the node property `annotations` (`label`, `labelMarkdown`, `properties`, `categoryId`,
  Figma plugin API) in a read-only `figma_execute`; neither that tool nor the `figma.annotations`
  category methods are called, a category stays its `categoryId` (its name needs that API, so it
  is asked for and the side effect named). design-line §8 says the same.
- **Props mapping:** `Size=Medium ↔ size="default"` when the code has `default` and no `md` (read
  `defaultVariants`); text properties (`Label`, `Name`, `Initials`, `Placeholder`) map to the prop or
  children that carries the text; a prop only the code has is named, not mapped.
- **A «(Recommended)» option in every question:** `design-system` step 3 (posture: the one the
  code suggests; case A token source: the code files), step 5d («Лише записати пропозицію в
  канон», the file is someone else's), the «Оновити» value question; `screens` (the «Screens ·
  <slug>» page: yes; existing frames: «Розібрати ці фрейми»); `read-frames.md` (the most likely
  screen · state pair, the later version, «Попросити дизайнера»); the `ux-flows` contradiction
  question («Лишити як у джерелі»).
- **The canon template no longer offers values with `<slug>`** that self-check item 4 then
  rejected; item 4 now says the frame-name pattern is not a placeholder. On a first run with
  «Foundations write permission: not allowed», `design-system` writes «Screens write permission:
  not asked yet», and `screens` treats it as «ask».
- **`library_frame` in Figma** is one thing everywhere: the page (`<page>`, or `<page> /
  <section>`), never `(top level)` (`design-keeper` step 3 and «Known tools», design-line §8).
- **A type scale kept as text styles counts as present** in Figma; no number variables are
  proposed for it (design-line §8, `design-keeper` step 4).
- **Hidden layers in a designer's frame** are not a state: listed under `## Assumptions`, and in
  §Ask the designer when one looks like a state; nothing unhidden.
- Cheaper ones from the same report: variable names match with `-` and `/` alike (`--gray-0` ↔
  `gray/0`, `--space-4` ↔ `space/4`); spacing seeds every step the code uses (the 4 / 8 / 12 /
  16 / 24 / 32 list was an example); case A conventions come from the code, marked `derived`, no
  question; `figma_get_variables` with `refreshCache: true` (it returned a stale cache in a long
  session).
- Not changed: the background dispatch inside a teammate session (an artefact of a run without
  subagents).

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: nothing. If an earlier read-mode run left the four preset annotation
  categories in a Figma file, they are Figma's defaults and harmless; delete them in Figma if
  unwanted.
- **Not run live:** these fixes. `claude plugin validate` passes for the plugin and the
  marketplace.

## [4.9.0] — 2026-11-10

### Added — `screens` read mode: the designer already drew the screens

`screens` could only draw. When a designer has drawn the screens in Figma (or pen.dev, or another
tool), the line now reads their frames instead of drawing a second set next to them. Details in
the new `screens/references/read-frames.md`; the manifest format is the same, so `verify-ui` and
the code work downstream do not change.

- **Entry:** `/sdlc:screens <slug> --from <url>` (a page, section or frame; Figma with `node-id`),
  or «розбери екрани дизайнера» / «screens from the designer's frames» / «екрани вже в
  документі». **Draw mode is unchanged**: without these, `screens` draws with no new question; the
  only new question comes when the design file already holds frames of this feature that the skill
  did not draw («Розібрати ці фрейми» / «Малювати свої екрани»; headless → draw, the frames listed
  under `## Assumptions`). **Nothing is written into the design file**, so no write permission is needed; a
  file other than the canon's is read too, and §Source says which.
- **Frames → screens and states:** each frame maps to an `SCR-NN` from `ux-flows.md` and a state
  (the six classes and the named states), by its name, what it shows and the branches landing on
  the screen. Ambiguous frames are asked about in one batch; headless → `## Assumptions`. A frame
  that is not a screen of this feature is listed, never forced into a state.
- **Coverage:** every class of every screen is drawn (node id) / `N/A: <reason>` / **missing**.
  The missing states go into the new §Ask the designer, or, after the person's yes, are drawn by
  the normal draw mode on «Screens · <slug>» only, marked «drawn by the agent».
- **Components:** every instance → its main component → the inventory row (node id / component
  key, else by name, marked «matched by name»). Detached instances and hand-built look-alikes are
  «not from the library»; a `design-only` component goes to §New components as «create in code
  once and add to the canon»; a component missing from the canon → «run `/sdlc:design-system`
  («Оновити»)».
- **Behaviour:** the new §Behaviour holds pop-ups, transitions and notes from what the tool really
  returns: annotations (Figma Console `figma_get_annotations`), prototype `reactions`, Code Connect
  instructions when the official server returned them (which annotations it returns is not
  documented, so they are used only if present). Nothing found → said so, and a note asked from
  the designer.
- PNG per drawn state as in draw mode (`test -s`, one command per call) or the named gap;
  frontmatter `mode: draw | read`; §Source «Mode: read — frames drawn by the designer, read only»
  with the frame → state map. Self-check items 5–7 are replaced by read-frames.md §8 in read mode.
  Triggers, Definition of Done, anti-patterns and an example invocation for both modes added.

### Added — the design ↔ code binding with props, in the canon

- **«Design ↔ code props»**, a new column of the canon's inventory: for a row with both anchors,
  the design's variant properties paired with the props the code really has, read from the code
  (`cva` variants), never invented. Figma: `Variant=Outline ↔ variant="outline"` ·
  `Size=Large ↔ size="lg"`; pen.dev: `Button / Outline / Large ↔ variant="outline" size="lg"`.
  An uncertain pair goes under `## Assumptions`. When the session's official Figma server returns
  Code Connect for the component, the mapping comes from it, marked «from Code Connect».
  `design-system` self-check item 3 checks the cell. 4.8.x had the two anchors, not the props.
- **One line for `AGENTS.md`, not a table:** when it is missing, the `design-system` handoff says
  «Можна додати в `AGENTS.md` рядок: UI бери з інвентаря `docs/design/design-system.md`; новий
  компонент лише якщо його там нема». A proposal only: no question, no write, no new stop in the
  run.
- **`_shared/design-line.md` §8: Code Connect as a layer over the canon's binding.** The official
  server puts a connected component into a node's context as `<CodeConnectSnippet>` (design
  properties, import, snippet, instructions; Code Connect UI instructions arrive as user rules).
  Requirements checked on developers.figma.com on 2026-11-10: the MCP integration on Professional,
  Organization, Government and Enterprise, a Full or Dev seat, on Professional only the active
  library and framework; Code Connect UI on a Dev or Full seat on Professional, Organization and
  Enterprise (Government not mentioned on its page). Read mode in §1, §6 and the TL;DR.
- `plugin/README.md`, `CLAUDE.md` and both manifests (4.9.0) updated.

### Fixed — after the lesson 1 rerun on 4.8.2 (pen.dev)

- **Clipped swatch labels.** Five labels (`popover-foreground`, `muted-foreground`,
  `border-strong`, `pass`, `flag-green-bg`) were cut at the edge, and the keeper wrote off pen.dev's
  «partially clipped» as rounding. A label now hugs its text or wraps inside its column, and every
  problem the tool reports (`ctx.problems` included) is a defect to fix, never cleared by a
  screenshot that looks intact.
- **Composed shell commands that would be permission prompts on camera.** The main agent listed
  the plugin cache with `ls …; wc -l`, the explorer read the tokens with `python3 -I -c … ; wc -l`.
  `design-system` now says how to look around (Glob, Read, Grep; the template and shared files by
  their relative paths), and its explorer dispatch prompt forbids `python`, `ls`, `wc` and `;` /
  `&&` / `|` chains; design-line §6 gate 5 says the same for every skill.
- **«Сканування коду ще триває. Чекаю…».** The explorer was dispatched in the background, so the
  main agent ended its turn and resumed only when the result arrived. The explorer and the keeper
  are now dispatched in the foreground (`run_in_background: false`): their results feed the next
  step.
- **Stale instances in the light-theme card** (`stale 0-size layout`) needed one nudge each, part
  of why the run took 12:52 and $5.08 against 6:01 on 4.8.0. The keeper now draws every original
  component first and builds the second theme's card in one batch afterwards.

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: to fill the new props column of an existing canon, run
  `/sdlc:design-system` → «Оновити». To read a designer's screens, run
  `/sdlc:screens <slug> --from <url>`.
- **Not run live:** read mode (frames → states, the batch question, component mapping, the
  behaviour sources, the optional drawing of missing states), the props column, and the four
  fixes from the lesson 1 rerun.
  `claude plugin validate` passes for the plugin and the marketplace.

## [4.8.3] — 2026-11-10

### Changed — «Оновити» brings changed token values into the design document

For the lesson «токени змінились у коді». Before, `design-keeper` never overwrote a variable it did
not create and only reported a different value as a conflict, so after a token changed in the
CSS, `/sdlc:design-system` → «Оновити» left the document on the old value.

- **The keeper sorts every variable against the canon's token source**, each theme separately:
  new in the code (added), the same (nothing to do), changed in the code, and in the document but
  not in the code.
- **Changed values are written per theme** (the light value into the light mode, the dark one into
  the dark mode, never one into both) when the variable mirrors a token: the same name under the
  seeding mapping, in the file the canon names as its token source. Who decides: a repo
  `design_file` → no question, but the «before → after» list is in the report and the handoff; a
  URL file with write permission → one `AskUserQuestion` that shows the list, then a re-dispatch
  with the new `update_values: true`; no permission or headless on a URL → nothing written, the
  list under `## Assumptions`.
- **Variables the code does not have** (a designer's own, or a token deleted from the code) are
  never touched or deleted, only listed as «in the document, not in the code»; one plain
  `git log -S '<name>' -- <token file>` tells a removed token apart.
- **The foundations sheet follows**: bound values update by themselves; numbers set from a value
  (the spacing bars in pen.dev) and labels that print a value are rewritten in the «Foundations»
  frame the keeper drew; a new token gets its swatch, row, bar or square.
- **Report and canon:** updated / added / left, with names, counted from the document; a new
  §Token source line «Last sync with the document»; a changed colour in the «Contrast» table is
  recomputed and a pair that now fails AA is named in the handoff. Self-check item 5 checks the
  owner rule for value writes. `_shared/design-line.md` §6 says the same in short.

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: after a token changes in the code, run `/sdlc:design-system` →
  «Оновити».
- **Not run live:** the value sync, its question for a URL file, the sheet's label and number
  rewrite, the contrast recompute. `claude plugin validate` passes for the plugin and the
  marketplace.

## [4.8.2] — 2026-11-10

### Fixed — after the lesson 1 rerun on 4.8.0 (pen.dev)

The rerun drew the foundations sheet and the components, saved through `save`, read the guide
with `read_skill({ path })` and left no probe nodes. What it still got wrong:

- **Invisible spacing bars.** In pen.dev a width bound to `$space-*` came out `width: 0`. Where a
  tool cannot bind a size to a variable, `design-keeper` sets the number read from the variable's
  value (`GetVariables()`), the label still naming the variable. The look step now also reads every
  node's size back: each element of the sheet and every component must have a non-zero width and
  height, because a screenshot does not show a 0-width bar.
- **Tokens the product does not use on the sheet.** shadcn's default `chart-*` and `sidebar-*`
  groups were drawn although no product code uses them. A token group no file of the product's
  code references (Grep over the source, without the token file, dependencies and generated
  output) stays as variables but is left off the sheet; the report lists it as «in the tokens, not
  used by the product».
- **Half of the inventory drawn.** Card, Dialog, Tabs, Switch, Textarea, Progress and Separator
  stayed `code-only`; Button had `disabled` in two variants only and no `focus` / `invalid`
  although the code styles `focus-visible` and `aria-invalid`; sizes like `icon-lg` / `icon-xl`
  were missing. Now, in an empty document, the keeper draws every inventory row (`code-only` only
  means no node yet): every variant × size in the default state, and every state the code styles
  (read from its `disabled:` / `focus-visible:` / `aria-invalid:` / `aria-selected:` /
  `data-[state=…]:` / `hover:` classes) as one row per variant in the code's default size, so a
  Button is 6 × 3 + 6 × states, not the full product. Before the report it compares what is drawn
  with the inventory and names everything not drawn, with its reason.
- **Components in the dark theme only.** With two themes, the components are defined once and
  their instances shown in both: two theme cards side by side, set like the colour cards (or a
  second row in a frame with the other theme).
- **Keeper report numbers from the document.** It said 53 components where 49 were drawn; every
  number in the report is now counted from the document after the last write.
- **`cp` of the canon template from the plugin cache** stopped the run with a «sensitive file»
  permission prompt. `design-system` reads the template with Read and writes the canon with Write;
  `screens` and `ux-flows` bootstrap their templates the same way (design-line §2).
- **Self-checks counted rows with composed Bash** (`$(…)`), which was rejected and would show
  permission prompts on camera. Counting goes through Read and Grep (count mode) or one plain
  command per call; design-line §6 gate 5 adds `$(…)` and pipes to the forbidden shapes, and the
  `design-system`, `screens` and `ux-flows` self-checks say how to count.

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: an empty pen.dev document drawn by 4.8.0 / 4.8.1 has the old sheet
  and a partial inventory; to redraw it, start from an empty document again (the keeper never
  redraws into a document that already has a library).
- **Not run live:** these fixes (the size fallback and the bounds check, the unused-group filter,
  the full inventory, both themes for components). `claude plugin validate` passes for the plugin
  and the marketplace.

## [4.8.1] — 2026-11-10

### Added — `ux-flows` reads a PRD and the command text together

The question was: «ux-flows вміє і в PRD, і в prompt? треба, щоб і те, і те». Before, the input
ladder took the first source it found, so text in the command was ignored whenever a `PRD.md`
existed.

- **The source stays the base, the text adds to it.** When the ladder finds a source (`PRD.md`,
  `design-spec.md`, `story.md`, `idea-brief.md`) and the command also carries text, the text is
  additional instructions: narrow to one story, add failures, screens or constraints the source
  does not mention. With no source at all the text is still the story (`S-N`), as before.
- **New provenance token `N-NN`** (from the invocation) in `_shared/design-line.md` §3, next to
  `S` / `W` / `D` / `AC`. Every item from the command gets its branch, screen or note, a coverage
  row, and a line in `ux-flows.md` §Source (it is not written to `story.md`); `screens` and
  `prepare-design-spec` carry the token on.
- **A contradiction with the source is one question** («Лишити як у джерелі» / «Зробити як у
  команді»); the decision goes under `## Assumptions`, and with a PRD source the contradiction also
  goes to the handoff as a PRD gap for `/sdlc:clarify-prd`. Headless: follow the source and record
  it the same way.
- **«What can go wrong» in full mode** runs at `hard`, and now at any depth when the command text
  asks to think about failures.
- `ux-flows`: mode descriptions, step 1 (split the text into `N-NN` items), step 3, step 5
  (coverage rows for `N-NN`), self-check item 3, Definition of Done, anti-patterns, the template
  (§Source «From the command», «Contradictions with the source», coverage row) and an example
  invocation for both modes. `plugin/README.md` and `CLAUDE.md` updated.

### Changed — `screens` writes nothing into a designer's file on its own

In 4.8.0, without write permission `screens` still drew its state frames and a «Drafts · <slug>»
page into the designer's file, and a headless run did so without asking anybody.

- **No permission → one question, else markdown.** Interactive: «Намалювати екрани на окремій
  сторінці «Screens · <slug>» у цьому файлі?». Yes → **page mode**: every state frame goes on that
  page, new, `code-only` and changed components go in a frame «Drafts · <slug>» on the same page,
  the library and every other page stay untouched. No → `code` mode (inline wireframes, no PNG).
  Headless without permission → `code` mode, nothing asked.
- **The answer is in the canon**: a new §Design tool line «Screens write permission», next to
  «Foundations write permission», written by `screens` and reused by the next run until the person
  changes it. The `design-system` step-5d «ні» option now says exactly this.
- `design-keeper` never takes a «Screens · <slug>» page or its Drafts for the library;
  `_shared/design-line.md` §6 gate 6, §7 rule 11, §8 and the TL;DR say the same; the `screens`
  self-check item 4, Definition of Done, handoff, anti-patterns and template follow.

### Changed — `mermaid-check.md` keeps its throwaway output in the repo

`_shared/mermaid-check.md` sent the `mmdc` output to `/tmp`. Now it goes next to the checked file
(`docs/features/<slug>/_review/_mmd_check.md`, or `docs/_review/` for a repo-level file) and is
removed afterwards by exact name, one command per call, with the `_review/` folder only when the
check created it. The `node_modules/mermaid` path parses with an inline `node -e`, no file at all.

### Fixed — design line after the 4.8.0 release

- **`design-keeper` never takes «Drafts · <slug>» for the library.** Drafts that `screens` leaves
  in a file without write permission do not count for emptiness and are not library rows; the
  keeper lists them on their own report line, and `design-system` step 5f records them as `draft`
  rows. Before, a designer's file with only drafts in it could have looked like it had a library.
- **«Оновити» on a 4.7 canon** without the «Foundations write permission» line uses the owner rule
  of step 5a (as `screens` already did).
- **The directions sheet is removed only when its node id and exact name both match**: the
  keeper's frontmatter and its «Mode `directions`» section still said «by its exact name».
- **No method names that are not from the tool's guide**: the Figma note drops a plugin-API method
  name; «the colour collection's mode set on the card frame» is the rule.
- **One shell command per call, also here:** `screens` self-check item 6 (`test -s` one call per
  file, no loop) and the keeper's own `stat` / `test -s`.
- Re-wrapped long lines in `design-system` step 5c and `verify-ui` steps 6–7.

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: nothing. To give `ux-flows` extra instructions next to a PRD, put
  them after the slug: `/sdlc:ux-flows <slug> <text>`. A Figma file without write permission: the
  next `/sdlc:screens` asks once about a «Screens · <slug>» page.
- **Not run live:** the `N-NN` path (PRD + command text, the contradiction question), the
  «Screens · <slug>» page mode and its question, the Drafts handling in the keeper, and the new
  `mermaid-check.md` output path. `claude plugin validate` passes for the plugin and the
  marketplace.

## [4.8.0] — 2026-11-10

### Changed — one `sdlc:design-keeper` for any design tool (replaces `sdlc:pen-keeper`)

`design-system` called `pen-keeper` on pen.dev and on Figma only wrote the file link into the
canon: nobody reconciled a Figma library. Instead of one agent per tool there is now one contract
for any design tool whose MCP the session has.

- **`sdlc:design-keeper`** (new; `sdlc:pen-keeper` is removed). It finds the tool's tools in the
  session, deferred ones included, and maps what they can do: target document, read, write, save,
  look, export. Before the first write it reads the tool's own guide once (pen.dev `read_skill`,
  the Figma plugin's skills or the `create_design_system_rules` prompt, a server's instructions);
  the guide governs how to call the tools, never the keeper's gates. Target-document gate:
  absolute paths for a local file, file keys for a URL, STOP with the exact user action on a
  mismatch. It lists every reusable component with its id and variants, seeds the missing
  foundations (colours in both themes, radii, typography with its scale, spacing) as the tool's
  variables, and never overwrites a variable it did not create. It writes only with
  `allow_writes` from the caller, else returns everything as proposals (see «permission by the
  file's owner» below). The foundations sheet and every variant and state of the components are
  drawn only in an empty document, with the tool's own variant mechanism (Figma: a component set
  with properties; pen.dev: a component per variant). Property names come from the tool's guide
  or an existing node, never from a probe node.
  It saves (`save` tool, autosave, or asks the user), checks the result (`stat` before/after for a
  local file, a read-back for a URL) and looks once with a screenshot. The report keeps the
  `pen-keeper` format and adds the tool, the capabilities used, the proposals and the look.
  Short notes for pen.dev, Figma Console and the official Figma MCP; any other tool goes the same
  steps by capability; nothing to write with → report only; no MCP → `code`.
- **Canon:** new frontmatter field `design_file` (a repo path or a URL); `tool` is `code` or any
  design tool's name (`pencil`, `figma`, `<name>`). `pen_file` and `figma_file` stay readable as
  legacy synonyms (`design_file`, else `pen_file`, else `figma_file`); new canons write only
  `design_file`. §Design tool gains «Agent access» (the MCP server and the capabilities used) and
  «Foundations write permission». The `design-system` and `screens` self-checks: `tool` ≠ `code` ⇒
  the design file (or a synonym) is non-empty; disk checks (`test -s`, `stat`, `git status`, the
  separate commit for the design file) run only when it is a local path.
- **`design-system`:** step 3 offers every design tool with an MCP in the session, plus `code`
  always. Step 5 «Prepare the design document» works for any tool (pen.dev: open the `.pen`; Figma
  Console: open the file in Figma Desktop with the Desktop Bridge plugin running; official Figma:
  the file key travels in every call) and dispatches `design-keeper`. New step 5d: a file at a URL
  that the person did not create in this run gets one question that shows what would be written;
  «yes» re-dispatches the keeper with `allow_writes: true`; headless → no permission, the proposals
  go under `## Assumptions`.
- **Permission by the file's owner, not by what is inside** (design-line §6 gate 6, the canon's
  «Foundations write permission»). A repo path belongs to the person running the skill: written
  without asking, headless too (a course kit `.pen` in the repo included). A URL the person
  created in this run: written. Any other URL, empty or with a library: one question; headless,
  only proposals. `screens` reads the line: without permission it never writes into the
  designer's library and puts new, `code-only` and changed components on a separate page or frame
  «Drafts · <slug>», listed in the handoff for the designer. «Оновити» reuses the recorded line
  and asks again only when the person wants to change it. `library_frame` may stay empty when the
  keeper reported a read-only tool or no library and no permission, with the reason under
  `## Assumptions`.
- **One foundations sheet in every tool**, after the reference drawn in Figma: a frame
  «Foundations» with a title and one subtitle line; colours as one card per theme side by side
  (every semantic colour a swatch with its name and the primitive under it; the theme set by the
  tool's own mechanism on the card: the collection mode in Figma, `theme` on the frame in
  pen.dev); typography as one row per size (name, font / size / line height, a sample line);
  spacing as bars whose width is bound to the variable; radii as squares; every value on a
  variable or style, never a literal; the components below. In `design-keeper` step 5 and,
  briefly, design-line §6.
- **`screens`:** step 4 draws in any design tool through the same gates (target document, only the
  tool's tools, a frame per state built from library instances, a screenshot, PNG export with
  `test -s`, save); pen.dev and Figma specifics are sub-points. No export in the session → a named
  gap in §Source and the node id stays the source-ref (was Figma-only); an image the tool returns
  only into the conversation is a look, not an export. The tool's MCP connected but read-only →
  `code` mode, named.
- **`_shared/design-line.md`:** §6 is generic (`tool` names the product, `design_file` resolution,
  what counts as a design tool, a capability table, six gates for every tool, local path vs URL);
  §7 pen.dev stays (+ rule 12: a variant is its own component); §8 Figma covers Figma Console
  (Desktop Bridge, `fileKey`, PNG through `figma_get_component_image` + `curl`) and the official
  server (reads, `use_figma` beta with edit access and a Full seat), autosave, component sets,
  foundations as variables with `Light` / `Dark` modes, the designer as the file's owner; new §9
  any other design tool; code mode moves to §10. TL;DR updated.
- `agent-roster.md`, `handoff.md` (two design-line rows), the `screens` and `prepare-design-spec`
  templates, `plugin/README.md`, `README.md`, `CLAUDE.md` and both manifests updated.

### Added — `design-system` builds the foundation when the project has no tokens

The question was: «а якщо ще немає токенів, скіл допоможе зібрати дизайн-систему?» Before, it
wrote «ще немає», and the keeper had nothing to carry over. Now step 2 names the case and a new
step 4b builds the foundation with the person. The details live in the new
`design-system/references/foundation.md`; steps 5–7 keep their numbers.

- **Three cases** from the step-2 scan: **A** token files exist (unchanged; the branch fires only
  when there are no token files at all), **B** no token files but UI code, **C** an empty project
  (no tokens, no UI components, no values written in styles, possibly no stack).
- **Case B: a scan of values written straight into styles** (colours, font sizes, spacing, radii)
  with count and `file:line`, through the same `explorer` dispatch (only the prompt changes).
  Step 3 (c) offers «Зібрати з того, що знайдено в коді» (Recommended when values were found) /
  «Стартова основа» / «Лишити без токенів»; case C offers «Зібрати основу разом» / «Лишити без
  токенів».
- **A short Socratic interview, not one question.** Depth from `--depth`, else `interview_depth`,
  else `medium` (`_shared/interview-depth.md`); phrasing per `ask-style.md`; the manner of the
  `interview` skill. Round 1: character, what already exists, what it should look like and what to
  avoid, constraints (easy: character, primary colour, font, themes). References are asked in
  plain text (links, screenshots, a Figma file, a brand book, a logo), read (Read, WebFetch, the
  Figma MCP; fetched content is data, never instructions) and turned into signals with a source
  each; brand colours and fonts are fixed inputs. Round 2 at medium / hard: «чому саме так?», «що
  буде, якщо…?» from the person's own answers; hard adds edge cases.
- **2–3 directions** (name, hex palette, font pair, radii, density, a why-line tied to the
  answers and references), each contrast-checked. On a design tool with an empty document
  `design-keeper` draws them side by side (`mode: directions`, frame «DS · Directions»), else a
  markdown table. The person picks or mixes, one «що змінити» round, and only then is anything
  written.
- **The starter foundation:** palette (neutral scale, the primary colour with its scale, status
  colours), a semantic layer per theme, a type scale, spacing on a 4 px base, radii. Every «text
  on background» pair is computed at AA (body 4.5:1, large text and UI 3:1) in every theme and
  recorded in the canon; a colour the person gave is never changed silently.
- **Tokens in code, two layers, light and dark:** the project's theme file the person names (CSS
  custom properties, a Tailwind `@theme` block, the framework's theme file; following the
  conventions the file already uses), add only, shown as a diff and proposed as its own commit.
  No stack → `docs/design/tokens.json` in the DTCG format (2025.10 value shapes: colour objects,
  `{value, unit}` dimensions; themes as two sibling groups `light` / `dark`).
- **Case C: a starter component set** in the inventory as `design-only` rows (source
  `starter set`): Button (primary, secondary, outline, ghost, destructive × sm, md, lg; disabled),
  Input (default, focus, error, disabled), Badge, Avatar, Card, navigation for the posture (Header,
  Tab bar). `design-keeper` draws them from their canon rows in an empty design document with the
  foundations sheet.
- **Headless:** no interview, nothing written but the canon: one proposed direction, its
  foundation and (case C) the starter set under `## Assumptions`; `design-keeper` runs in the new
  read-only `mode: inventory`. A later «Оновити» offers the proposal as direction A.
- **Canon template:** new `## Sources` (references with links, signals, read / unread); §Token
  source gains origin, direction and a contrast table; `## Assumptions` now also holds the
  confirmed interview decisions, each tagged `answer` / `ref:N` / `derived`.
- **`design-keeper`:** `mode: directions` (plain nodes, no reusable components, literal values,
  only in an empty document, not saved, deleted on the next `reconcile` by its exact name) and
  `mode: inventory`; a starter row is drawn from its canon row.
- Self-check of `design-system`: 7 items (was 5); `library_frame` may stay empty when nothing
  could be drawn, with the reason under `## Assumptions`; starter rows carry the anchor
  `starter set`.
  Definition of Done, anti-patterns, an example invocation, `plugin/README.md`, `README.md`,
  `CLAUDE.md` and the `design-line.md` TL;DR updated.

### Fixed — after a live run on pen.dev 1.2.22

- **Saving through the MCP.** Newer Pencil servers have a `save` tool and take the document's
  `uri` (`file://<absolute path>`), refusing a document that is not open («wrong .pen file»). The
  keeper and `screens` pass the `uri`, call `save` and confirm the file changed on disk; Cmd+S is
  asked only when the server has no `save`.
- **`read_skill` takes only `path`.** `read_skill()` returns the skill's SKILL.md, then
  `read_skill({ path: "execute.md" })` and any other file it names for the schema.
- **The whole foundation, not only colours.** Radii, typography (families, the type scale, line
  heights), spacing (the framework defaults the code uses when the source has none, flagged as
  such); a group the source lacks is reported as «not in the token source», never invented.
- **An empty document gets a real design system.** A foundations sheet (swatches of both themes,
  the type scale, spacing bars, radii) and every component variant, size and state the code
  defines, not only core primitives.
- **Default state classes need no source.** A screen that fetches or sends has `loading` and
  `error`, a list has `empty`, an action with feedback has `success`, user input has `validation`,
  all marked `derived`; dropping one needs an `N/A` with a reason about this screen.
- **A failure question for every step that calls the server.** `ux-flows` gives each such step
  (creating, sending, loading a list) its own «what can go wrong» candidate and asks a second
  question when four options are not enough; headless, it derives one `D-NN` per such step.

### Fixed — after the live lesson rehearsal on pen.dev 1.2.22

- **`screens`: changing a library component.** The agent added a fourth tab to the TabBar without
  a word. Now a change to an existing library component needs a «Changed: <component> — what and
  why» row in §New components and in the handoff, with the advice to run `/sdlc:design-system`
  («Оновити»); in a designer's file without write permission the original is never changed, a
  changed copy goes on «Drafts · <slug>».
- **`screens`: a state frame holds only its own layers.** Every conversation state was a copy of
  `default` with the other states' layers switched off (`enabled: false`): a hidden «retry» button
  and «Ended note» in `default`, a hidden input block in `ended`. Each state is now built from
  instances, a copied frame gets the foreign layers deleted, and self-check item 7 reads every
  state frame back for hidden nodes (self-check: 7 items, was 6).
- **One shell command per call, no temp scripts.** `screens` export and `verify-ui` used loops,
  `&&` chains and scripts in `/tmp`: a headless run rejected them, an interactive one would ask
  permission for each. Now `test -s`, `mv`, `test -s` run as separate calls, nothing is written
  outside the repo (design-line §6 gate 5); the contrast check of the foundation is one inline
  `python3 -c`.
- **`design-system`: handoff numbers from disk.** The handoff said 34 inventory rows where the file
  had 31; every number is now counted from the written file.
- **`verify-ui`: both pictures in every state row.** Only one row had the mockup and the live
  screenshot side by side; now every state row with a PNG carries both paths, and a self-check
  before the summary catches a missing one.
- **`ux-flows`: an honest mermaid check.** When the parser cannot run (no permission for `npx`),
  the handoff says so in one line and names the fallback that checked the flows instead.
- **No probe nodes.** The keeper (then `pen-keeper`) left a top-level `probe` frame while guessing a
  property name. Now the schema and property names come from the tool's guide; when it is silent,
  the keeper reads an existing node of that kind (`Get`); a probe node is never created
  (design-line §6 gate 3).

### Update notes

- How to update: `claude plugin marketplace update sdlc`, `claude plugin update sdlc@sdlc`, then
  restart `claude`.
- What to do after updating: nothing for an existing canon, its `pen_file` / `figma_file` is read
  as before. Anything that dispatches `sdlc:pen-keeper` by name → `sdlc:design-keeper`. A `.pen` in
  the repo (a course kit included) is written without asking, as before. A Figma file at a URL that
  the person did not create in this run now gets one question before anything is written into it;
  headless runs record proposals, and `screens` then draws new components on «Drafts · <slug>».
  To reconcile a Figma file the canon only linked, run `/sdlc:design-system` →
  «Оновити». A project whose canon says «ще немає» for tokens: run `/sdlc:design-system` →
  «Перебудувати» and pick the option that builds the foundation.
- **Not run live:** the generic keeper, the Figma path (Console and official, including the PNG
  export through `figma_get_component_image` + `curl`), the permission question, and the whole
  foundation branch (value scan, interview, directions sheet, token writing, `tokens.json`,
  starter set, headless proposal), «Drafts · <slug>», and the foundations sheet layout outside
  Figma (pen.dev `theme` on the card frame). `claude plugin validate` passes for the plugin and the marketplace.

## [4.7.0] — 2026-11-09

### Added — design line: `design-system`, `ux-flows`, `screens` + `sdlc:pen-keeper`

The course lesson «Дизайн-лінія SDLC: процес у скілах» (module 5) needs the design process as
skills, and the student has no PRD until module 6. Ported from the sdd plugin and adapted so the
whole line runs from a 3–5 sentence user story:

```text
/sdlc:design-system → /sdlc:ux-flows <slug> → /sdlc:prepare-design-spec <slug>
  → /sdlc:screens <slug> → build the screens → /sdlc:verify-ui <slug>
```

- **`design-system`** (new, once per repo) writes the canon `docs/design/design-system.md`: tool
  (`pencil` / `figma` / `code`), platform posture, token source, component inventory with source
  anchors, cross-screen conventions. Works without `docs/architecture-map.md` (scans the code via
  `sdlc:explorer`). On pen.dev it prepares the `.pen` document by copying a real file or asking the
  user to create it in the app — unlike sdd it never writes a `.pen` stub by hand — then seeds
  variables and reconciles the document's component library through the new `sdlc:pen-keeper`
  agent (an existing library is recognized; see «Fixed» below).
- **`ux-flows`** (new) writes `docs/features/<slug>/ux-flows.md`: mermaid flows, the `SCR-NN`
  screen inventory, a coverage table. **Story mode** when there is no PRD: the input is
  `story.md` or an inline story (saved verbatim to `docs/features/<slug>/story.md`); error branches
  come from one «що може піти не так» question (`W-NN`); anything inferred without confirmation is
  marked derived (`D-NN`) and listed under `## Assumptions`. With `PRD.md` it runs in full mode (one flow
  per UI-touching user story, branches from §5 ACs). Without a question channel (headless) it
  takes the easy path and records every assumption instead of stopping.
- **`screens`** (new) writes the manifest `docs/features/<slug>/screens.md` (screens × states ×
  components, reuse-first, `NEW:` only with a reason) and, on pen.dev / Figma, one PNG per state at
  `docs/features/<slug>/screens/SCR-NN-<state>.png`. Without `sad.md` the states derive from the
  flows, the design spec and the story, each with a provenance token; with `sad.md` and contracts
  they also come from §6 branches and API error responses. pen.dev gates: active-document check
  before every write, no hand edits of `.pen` JSON, `Export` + `test -s` for every PNG (an export can
  leave no file or an empty one without a failing status; `Export` names each file
  `<nodeId>.png`, the skill renames it to `SCR-NN-<state>.png`), Cmd+S before commit, save and close before `git checkout`.
  Screens are drawn in the canon's `.pen` (one document holds the components and the screens) as
  frames `<slug> · SCR-NN · <state>`.
- **`sdlc:pen-keeper`** (new agent) uses the current Pencil MCP tools (`get_app_state`,
  `read_skill`, `execute`); sdd's version still lists the removed `get_guidelines`. It inherits
  the session's tools because the Pencil tool prefix differs between an MCP server and a plugin.
- **`_shared/design-line.md`** (new) is the single source for the order, the file layout, the
  input ladder (`PRD.md` → `design-spec.md` → `story.md` → `idea-brief.md` → inline → ask), the
  provenance tokens (`AC` / `BR` / `S` / `W` / `D` / `§6` / `contract`), the headless rule
  and the pen.dev / Figma / code rules.

### Changed — `prepare-design-spec` and `verify-ui` join the line

- **`prepare-design-spec`** reads `story.md`, `ux-flows.md` and `docs/design/design-system.md`;
  §8 State inventory gains `Screen (SCR-NN)` and `Source` columns; §13 points to the canon and the
  screen manifest; DOD-04 evidence names `screens.md` + the exported PNGs; the handoff runs
  `/sdlc:screens <slug>`. Output path unchanged: `docs/features/<slug>/design-spec.md`.
- **`verify-ui`** works without `sad.md` when the feature has `screens.md` / `design-spec.md`.
  Criteria are collected from every source present (not the first one found): PRD §5 or a task
  file, `design-spec.md` §16, and every state in the `screens.md` tables; one verdict row per
  checked thing, citing all its ids.
  When a state has an exported PNG, the live screenshot of the same state is put next to it in the
  verdict row (a reference, not a pixel diff). New step 7 writes the verdict to a fixed home:
  `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md` + a screenshots folder of the same name
  (`test -s` on the report and every screenshot it cites); before, the verdict lived only in chat.
- **One state vocabulary** for `design-spec.md` §8, `screens.md`, frame/PNG names and `verify-ui`:
  the six classes `default` · `loading` · `empty` · `error` · `success` · `validation`, checked for
  every screen, plus named states from flow branches (`error-undelivered`, `ended`; see «Fixed»
  below). The old §8 rows Ready / Saving map to `default` / `loading`;
  hover / focus / disabled are component states from the inventory, not screen frames
  (`_shared/design-line.md` §3).
- `handoff.md` (five design-line rows), `agent-roster.md` (`pen-keeper`), `size-matrix.md`
  (design line is optional by surface, not by size), `plugin/README.md`, `README.md`, `CLAUDE.md`
  and both manifests (24 skills, 12 agents) updated.
- Smoke run: headless `ux-flows` in story mode on an empty repo (story «чат після метчу») wrote
  `story.md` + `ux-flows.md` (1 flow, 2 screens, 4 `D-NN` branches, 10 assumptions), mermaid parsed
  by mermaid-cli, self-check 5/5. pen.dev mode was not run.
- How to update from an older version (4.5.1 and later): `claude plugin marketplace update sdlc`,
  `claude plugin update sdlc@sdlc`, then restart `claude`. `verify-ui` needs `playwright-cli`:
  `npm install -g @playwright/cli@latest`, plus `playwright-cli install-browser chrome` only if
  `open` says `Browser "chrome" is not installed`.
- What to do after updating: nothing for existing features. To use the line, run
  `/sdlc:design-system` once, then `/sdlc:ux-flows <slug> <story>`.

### Fixed — design line review before the course recording

A review of the course series (pen.dev → SDLC design line) found holes that would break the
recording and every student's run. Fixed before release:

- **An existing component library is recognized, never duplicated.** A starter `.pen` already holds
  its library under its own frame name (the course kit: «Components · Chat»); `pen-keeper` used to
  create a second «DS · Foundations» beside it, with twin Button / Input / Badge, and the kit-only
  components (Toast, Spinner, MessageBubble, ChatRow) never reached the inventory, so `screens`
  marked them `NEW:`. Now `pen-keeper` lists every reusable component in the open document first
  and picks the library frame: the one the canon names (new frontmatter field `library_frame`),
  else the frame that holds the reusable components (`(top level)` when they sit on the canvas in
  no frame); «DS · Foundations» is created only in a document with none, and only there does
  `pen-keeper` draw primitives. In a document with a library it draws nothing: code and kit rarely
  share names (`Badge` vs «Tag / Neutral»), so adding «missing» primitives by name would create
  twins. A component that exists only in code is a `code-only` row; `design-system` pairs rows by
  the project's own «.pen → code» map or by name family and never guesses a pair; `screens` draws
  a `code-only` component into the library frame the first time a screen needs it (it is not
  `NEW:`). Its report lists every reusable
  component with its node id and says `writes: none` when nothing changed. `design-system` writes
  the frame into the canon and merges the components into the inventory (one row per component,
  both anchors when it is in code and in the document, `design-only` / `code-only` otherwise).
  Default `pen_file` = the one `.pen` already under `docs/design/`, when there is exactly one.
  «Оновити» on an existing canon now has real steps (rescan code, re-read the document,
  reconcile the inventory in place, keep edited conventions). Self-check item 5 uses `test -s` and
  passes on a clean reconcile with nothing to save (it used to demand a changed file: 4/5).
  **Not run live in pen.dev** — the library recognition needs a live run before the recording.
- **Named states beyond the six classes.** The six classes are checked for every screen (a real
  state or one `N/A: <reason>` row); on top of them a screen may have named states from flow
  branches: `<class>-<variant>` (`error-undelivered`) or a bare kebab-case name for a product state
  that fits no class (`ended`: the other person closed the conversation). Each named state carries
  its source token and gets its own frame, PNG and verdict row. An `N/A` row has no frame, no PNG
  and no verdict row; the `screens` self-check and Definition of Done now say so, so
  `validation · N/A: the disabled Send button is a component state` passes. Same wording in
  `_shared/design-line.md` §3, `screens`, `prepare-design-spec` (§8 + gate) and `verify-ui`.
- **No promises the neighbour skills don't keep.** `break-tasks`, `implement-tasks` and
  `review-feature` do not read `screens.md` yet, and `architecture-design` / `plan-tests` do not
  read `ux-flows.md`. The docs now say: `verify-ui` reads the manifest; name the file in the prompt
  of the others.
- **One browser install command.** Four places said three different things;
  `npx playwright install chromium` installs a browser `playwright-cli open` does not use by
  default (it opens the system Google Chrome, channel `chrome`). Everywhere now:
  `npm install -g @playwright/cli@latest`, then `playwright-cli install-browser chrome` only if
  `open` says `Browser "chrome" is not installed` (the command the CLI itself prints).
- **`verify-ui`: SKIP is not a pass.** The summary is PASS only with no FAIL and no SKIP; every
  SKIP names what blocked it. New `screens.md` §Source line «State access» (how to open each state
  in the running app: URL parameter, fixture switch, test account), filled when the screens are
  built; `verify-ui` reads it and SKIPs a state it cannot reach, never fakes it.
- **One input ladder.** `prepare-design-spec` pointed at `_shared/design-line.md` §3 but listed a
  different ladder; it now states only its delta (skips its own `design-spec.md`; a linked issue
  counts as the inline request).
- Smoke run after these fixes: headless `ux-flows` in story mode (story «скарга на анкету», slug
  `report`) in a fresh repo, plugin loaded with `--plugin-dir`: wrote `story.md` + `ux-flows.md`
  (1 flow, 2 screens, 7 `D-NN`: 4 branches, among them «Інше» without text → validation, and 3
  decisions), mermaid parsed by mermaid-cli, self-check 5/5. `design-system`, `screens` and
  `verify-ui` were not run; pen.dev was not run live.
- What to do: re-run `/sdlc:design-system` → «Оновити» on a pencil repo created with an earlier
  4.7.0 build, so the canon gets `library_frame` and the document's components.

## [4.6.2] — 2026-10-25

### Fixed — `complete-sequence-diagrams`: the US/AC → flow coverage table has one home, `sad.md §6`

Course lesson 6.5 asks the student for a screenshot of the use-case coverage table. Step 7 only said
the two coverage passes are «surfaced as one coverage table» — no file, no heading, no columns — so
runs varied: the table appeared in chat only, or inside `sad.md` in an ad-hoc shape, or not at all
(a curator's run on a real feature produced diagrams and nothing else). Step 6 already names where
flows go; step 7 now does the same for the table.

- **Fixed location.** The table is written into `docs/features/<slug>/sad.md` as the **last block of
  §6**, under the fixed heading **`### Coverage: US/AC → flows`** (after every `### <flow name>`
  block, before `## 7`). Chat gets only the one-line summary. This is where `review-feature`'s
  end-to-end AC trace and `api-forge`'s coverage cross-check already read; no new `_audit/` file.
- **Fixed shape.** Columns `ID | Realized by (§6 heading) | How | Note`; one row per PRD §4 user
  story (in §4 order) then per §5 AC (in §5 order), IDs as the PRD spells them; `How` is `flow` /
  `branch` / `N/A`; `Note` carries the branch label or the N/A reason. Closes with
  `Coverage: n/n user stories · m/m ACs — k non-runtime N/A.`; step 8 appends `**Flags:**` under it.
  New template `plugin/skills/complete-sequence-diagrams/templates/seq-coverage.md`.
- **Always written, idempotent.** Runs at every depth and size (easy/XS included), even when every
  row is `flow`. A re-run replaces the existing block instead of appending a second one. Only the
  N/A rows are confirmed with the user (medium/hard) or go to the assumptions ledger (easy).
- **Single-flow mode (`--flow`)** no longer says «no coverage report»: it writes the new flow above
  the coverage block and patches the rows that flow realizes; if §6 has no block yet it says so and
  points to the full run.
- DoD gets an explicit «the coverage table is in the file» item; anti-pattern «Coverage table in
  chat only» added; commit message is now `sequences: <slug> runtime flows + coverage`.
- `handoff.md` table, `plugin/README.md` and root `README.md` (which still listed a long-gone
  `diagrams/seq-*.md`) name the block; `examples/course-lesson-mvp/sad.md` §6 carries the real
  table (10 US, 19 AC, 0 N/A) instead of a comment pointing at a `_audit/sequences-*.md` file that
  was never shipped.
- What to do after updating: nothing for existing features; re-running
  `/sdlc:complete-sequence-diagrams <slug>` adds the block to an existing §6 without touching the
  drawn flows.

## [4.6.1] — 2026-10-24

### Fixed — greenfield scaffold plan path + `/sdlc:<name>` command form

- **`map-architecture` (greenfield) wrote the skeleton plan where `implement-tasks` doesn't look.**
  It wrote `docs/features/_scaffold/tasks.json`; `implement-tasks` reads
  `docs/features/<slug>/tasks/tasks.json` (the location `break-tasks` uses), so the run after a
  greenfield foundation refused with «run break-tasks first». The plan now lands at
  **`docs/features/_scaffold/tasks/tasks.json`**, and the greenfield handoff prints
  `/sdlc:implement-tasks _scaffold` as *Run next* (the `handoff.md` table has the greenfield branch too).
- **`implement-tasks` accepts the legacy location.** If `docs/features/<slug>/tasks/tasks.json` is
  absent it falls back to `docs/features/<slug>/tasks.json`, says it's using the legacy path and
  offers to `git mv` it. For a `_scaffold` set it no longer expects `PRD.md` / `sad.md` /
  `tasks/tracker.md`; `scaffold` is listed as a valid `layer` for that set.
- **Slash commands in the `/sdlc:<name>` form.** Plugin skills are invoked as `/sdlc:<name>`; the
  texts (handoff blocks, trigger phrases, refusals, `plugin/README.md`, `CLAUDE.md`,
  `CONTRIBUTING.md`, `00-overview/`) still said `/sdlc-<name>`, which the live build doesn't
  recognise, so a copied *Run next* line didn't run. All current skill names are switched;
  older CHANGELOG entries and the legacy v3 test fixtures keep the old form as history.
- What to do after updating: if you already ran a greenfield `map-architecture`, nothing is
  required (the fallback picks up the old file); optionally
  `git mv docs/features/_scaffold/tasks.json docs/features/_scaffold/tasks/tasks.json`.

## [4.6.0] — 2026-10-19

### Changed — `api-forge`: explicit verdict, 5-point drift checklist, baseline `.claude/rules/openapi.md`

Course lesson 6.6 asks the student to open `api-sync-report.md` and confirm "verdict PASS,
all 5 drift points ✓, `unresolved_origins` empty". The skill text promised a 4-point checklist
and never defined a verdict; only the example report carried both. The skill now says what the
example (and the lesson) already do.

- **`**Verdict:**` line** opens `api-sync-report.md`: `PASS` | `PASS (with deferrals)` | `FAIL`,
  derived mechanically from the checklist — `PASS` = scenario A, 5/5 ✓, nothing parked;
  `PASS (with deferrals)` = core 1–3 ✓ but something consciously parked and listed (scenario B,
  a deferred supporting point, a Save-as-OQ, a sequence gap, a default deviation without ADR);
  `FAIL` = a core point still ✗ after the 4-state resolution, ≥3 open flags, or a field with no
  origin. The report is written on every run, `FAIL` included; the handoff's *Run next* follows
  the verdict (`FAIL` → fix the source, then `--reconcile`; never `break-tasks`).
- **Drift checklist is 5 points.** 1–3 core, forward (endpoint↔model, error-code↔registry,
  validation↔constraint); 4 **Entity / AC ↔ endpoint (coverage)** — the former unnumbered
  "back-feed cross-check", now a numbered supporting point; 5 **OpenAPI ↔ sequence**, both
  directions (branch→response, and response-without-branch = sequence gap). Per-point marks:
  ✓ / ✓ (deferred: …) / ✗.
- **Section D — Deferrals** in the report: every parked item with its next step, or `none`;
  `--reconcile` reads it first and closes or carries each entry.
- **Rules bootstrap** (HTTP path): on first run the skill writes `.claude/rules/openapi.md` from
  `plugin/skills/api-forge/templates/rules-openapi-baseline.md` (error envelope, `module.error_name`
  codes, cursor pagination, URL versioning, BearerAuth, `$ref`-only, no PII in examples) and reports
  it — same mechanism as `generate-data-model` → `.claude/rules/migrations.md`. A team edit there
  counts like an ADR for the drift check.
- Protocol steps renumbered 1–9 (rules bootstrap is step 2; drift check is step 8). DoD,
  anti-patterns, `plugin/README.md` and `00-overview/definition-of-done.md` updated.
- Example `examples/course-lesson-mvp/contracts/api-sync-report.md` aligned to the shape
  (canonical verdict wording, `Rules file` header line, `Deferrals` section, generator line).

## [4.5.1] — 2026-08-19

### Changed — scaffold: єдина env-пара `api/.env.example` → `api/.env`

- base-tpl (a0ce095) схлопнув дві env-пари в одну: docker-специфіка (POSTGRES_*, PGDATA-пін,
  DATABASE_URL з хостом `postgres`) переїхала інлайном у `docker-compose.yml`, а `api/.env`
  тепер читають і локальний `make -C api run`, і compose (`env_file` + `environment`-override).
- Що зробити після оновлення: у своїх проєктах-нащадках нічого — конвенція набирає чинності
  для нових скафолдів; згадки `api/.env.docker` у скілі виправлені на `api/.env`.

## [4.2.0] — 2026-06-01

### Added — `verify-ui` skill (the live browser feedback channel)

- New cross-cutting utility skill `verify-ui` (`/sdlc-verify-ui {slug-or-story}`): verifies a UI
  surface's acceptance criteria through a **live browser run** — opens the running app, drives the
  Given/When/Then scenario, reads the **real page state** (DOM via `snapshot`, computed styles via
  `eval`, persistence via `localstorage-get`, survives `reload`), and returns a per-AC pass/fail
  with a screenshot artefact. Catches what compiles and "passes the logic" but is visually or
  behaviourally broken — the class of bug deterministic gates can't see.
- **CLI-first.** Drives `playwright-cli` in bash (token-efficient, the vendor-recommended default
  for coding-agent loops/CI). Playwright MCP stays available for live stateful debugging only.
  Install: `npm install -g @playwright/cli@latest` → `npx playwright install chromium` →
  `playwright-cli install --skills`.
- **Surface-gated** to UI `target_surfaces` (reads `sad.md`); for backend-only features the
  browser channel gives no signal and the skill says so. Verdict is **evidence-before-assertion**:
  every FAIL carries expected vs actual read from the live page, never "looks right".
- Design→code input via **Figma Dev Mode MCP** named as the *input* channel (read the design's
  structure, not a flat picture) — it complements, never replaces, result-verification in the browser.
- Plugin skill count 17 → 18 (5 cross-cutting utilities). Backs Lecture 7.6 screencast #2
  ("розробка через Playwright"); the synthetic demo carries a self-contained `verify-ui` mirror.

## [Unreleased]

### Added — `scaffold` skill + greenfield `interview` (v4.5.0, 2026-08-19)

**What you get.** A complete new-project flow that starts in an empty folder:
`mkdir my-app` → `/sdlc-interview` (greenfield mode writes a project-level
`docs/idea-brief.md`) → `/sdlc-scaffold` (materializes the project from the public
[base-tpl](https://github.com/genkovich/base-tpl) template) → `/init`.

- **New skill `scaffold`** (`/sdlc-scaffold`): asks stack questions (backend language /
  architecture / frontend / auth) and battery questions (deploy, CI, Prometheus+Grafana
  monitoring, freshness pin bump), then runs base-tpl's tested `scaffold.sh`. Batteries are
  **subtractive**: an unselected battery is physically absent from the result (folders, compose
  services, CI jobs, README lines). "Yes to everything" reproduces the template byte-for-byte.
  Unfilled paths (PHP/Python/TS backends, microservices, flat React, non-Google auth) refuse
  honestly instead of generating stubs. Freshness bumps infrastructure pins via context7
  (WebSearch/registry fallback) behind a `make check` gate with automatic rollback.
- **`interview` greenfield mode**: in an empty folder (no `.git`, no `docs/`) the skill now
  writes a **project-level** `docs/idea-brief.md` (same 15-section template; slug = product
  name) and hands off to `/sdlc-scaffold` instead of `write-prd`. Feature mode in an existing
  repo is unchanged.
- **`interview` depth regulator**: first checkpoint now asks easy / medium / hard.
  `easy` = 3-4 checkpoints (idea, one Socratic batch, one combined RICE+recommendation
  confirm) with no sub-agent fan-out — for quick passes; `medium` = the existing 14-phase
  protocol (default); `hard` = medium plus an extra Socratic batch and a wider competitive
  table. Recorded in the brief frontmatter as `depth:`.
- **Distribution**: the repo now carries `.claude-plugin/marketplace.json`, so the plugin
  installs user-scoped from the marketplace and the skills are visible in any folder —
  including the empty folder a greenfield project starts in.

**Migration.** No breaking changes. Existing feature-mode `interview` runs behave exactly as
before (the depth question defaults to medium = the previous protocol). The idea-brief template
gained one frontmatter line (`depth:`); existing briefs stay valid.


### Added — `user-documentation` skill (2026-07-30)

- New cross-cutting utility `/sdlc-user-documentation <target-dir>` generates **end-user
  documentation from a live web application**: flow inventory (repo scan + live nav snapshot,
  user-confirmed and frozen) → per-flow browser walks with a JSONL action journal and state
  screenshots → one clean-context `sdlc:doc-flow` agent per flow writes the doc **strictly from
  the journal** → a thin linked `<Product> - User Guide.md` index. Style codified from the
  Beer-LMS reference corpus (Flow-docs, exact-780px full views or element crops, `> **Note:**`
  callouts, applicable-only tail tables).
- **Deterministic by construction**: flows classified `mutates: true/false` at inventory —
  read-only flows fan out in parallel, mutating flows run strictly sequentially (concurrent
  mutators corrupt each other's screenshots); all created data carries a `Docgen:` prefix;
  state-reference docs may only document OBSERVED states (create-through-UI or honest FAIL).
- **Optional screencasts** (`--video`): `replay-screencast.sh` re-executes the journal through
  `playwright-cli run-code` (closed action dictionary == replay contract, Playwright auto-wait
  for free) into a chaptered `.webm`.
- **Mechanical gate** `validate-docs.py` (zero-dep, PNG width via IHDR): H1/frontmatter/`---`
  frame, gapless Step/State numbering, embeds resolve + no orphan PNGs, width ≤ 780, one embed
  syntax per target (vault wikilinks vs repo markdown, auto-detected via `.obsidian/` walk-up),
  index links every flow. Calibrated green on the reference corpus.
- New agent `sdlc:doc-flow` (sonnet, cyan) — walks ONE flow and writes ONE doc, sentinel
  `DOCFLOW_OK`/`DOCFLOW_FAIL` contract, ephemeral-state (toast) inversion rule, OAuth
  special-case for `doc_type: auth`.
- Live eval on beer-lms: 3/3 flows OK with zero retries (task-flow 11 steps vs reference 11,
  auth special-case, state-reference with UI-seeded states), validator 0 errors / 0 warnings,
  40s+ replayed screencast with 0 failed steps, both vault-wikilink and repo-markdown targets.
- Plugin skill count 19 → 20 (7 cross-cutting utilities). Agents 10 → 11 (`sdlc:doc-flow`).

### Added — `prepare-design-spec` skill (2026-07-15)

- New design-entry utility `/sdlc-prepare-design-spec <slug>` closes the gap between product
  discovery and Figma/Pencil authoring. It inspects the real repository, separates Confirmed,
  Observed, and Proposed statements, and writes one `docs/features/<slug>/design-spec.md` that
  contains the specification and an embedded, traced Definition of Done.
- Added self-contained specification and DoD templates with requirement-to-evidence traceability. The
  workflow ends in deterministic repository gates plus live `verify-ui` evidence; an agent success
  report or screenshot alone cannot satisfy completion.
- Plugin skill count 18 → 19 (6 cross-cutting utilities).

### Changed (template ownership refactor, 2026-05-25)

- Single-owner artefact templates relocated from `sdlc/document-templates/` into the `templates/` subfolder of their owner skill: `interview/`, `fix-term/`, `write-prd/`, `architecture-design/` (gains `c4-context.md`, `c4-container.md`, `deployment.md` alongside existing `sad-template.md`, `adr-template.md`), `complete-sequence-diagrams/`, `generate-data-model/`, `api-forge/`, `plan-tests/`. Skill folders are now self-contained — copying a skill brings its template along.
- `write-prd/PRD-template.md` moved into `write-prd/templates/PRD-template.md` for consistency (all skills now keep templates in a `templates/` subfolder).
- `decide-adr` SKILL drops the legacy fallback to `document-templates/adr/NNNN-title.md`; the canonical ADR shape stays at `architecture-design/templates/adr-template.md`, referenced cross-skill.
- All 9 affected SKILL.md files updated to read templates from `./templates/X.md` instead of `../../../document-templates/X.md`.
- `document-templates/` keeps only cross-feature / manual / legacy snippets (`CHANGELOG.md`, `CONTEXT-MAP.md`, `claude-context.md`, `review-checklist.md`, `rollback-plan.md`, `migration-plan.md`, `task-breakdown.md`, `SPEC.md`, `arc42.md`, `architecture-brief.md`, `adr/NNNN-title.md`, `diagrams/c4-component.md`). Skills do not copy from this folder during their protocol — these are snippets pulled by hand when needed.
- Empty `document-templates/api/` directory removed.
- Docs rewritten: `plugin/README.md` (skill-anatomy + key-files-per-skill table + dedicated section on what stays in `document-templates/`); point-edits in `sdlc/README.md`, `sdlc/CLAUDE.md`, `sdlc/00-overview/file-structure.md` to reflect the new layout.

### Removed (M1-M6 cleanup, 2026-05-25)

Aggressive trim — toolkit now serves the Claude Course Modules 1-6 lecture set. Skills/templates/examples not referenced by any lecture deleted. Snapshot tag: `pre-m6-cleanup-2026-05-25` (rollback point).

**Skills (24 → 11):**
- Removed 7 atomic skills with zero lecture refs: `impl-prep`, `prep-context`, `prep-review`, `ship`, `sync-kb`, `write-changelog`, `help`.
- Removed 4 deprecated stubs: `define-api` (renamed to `api-forge` in v3.3.0), `design-db` (merged into `generate-data-model`), `plan-migration` (merged into `generate-data-model`), `draw-sequence` (superseded by `complete-sequence-diagrams`; single-flow case via `--flow`).
- Removed 2 composite wrappers: `design` (03-06), `detail` (07-09). Atomic invocation is now the only entry-point — wrappers added orchestration overhead that no lecture relied on.
- Kept (after Phase C validation): `break-tasks` — Lecture 6.7 LMS lesson actively invokes `/sdlc-break-tasks`.

**Templates (3 removed):**
- `kb-note.md` (sync-kb related, no longer needed)
- `feature-rollout-plan.md` (no lecture references)
- `security-review.md` (no lecture references)

**Examples (34 → 33+1):**
- Kept `examples/rate-limiting/` (Lecture 6.1 and 6.2 Sources.md reference it as the end-to-end filled brief sample).
- Kept `examples/goals-tracking/arc42.md` (referenced in Lecture 6.4 as filled-in Arc42 sample).
- Removed rest of `examples/goals-tracking/` (idea-brief.md, SPEC.md, data-model.md, migration-plan.md, rollback-plan.md, task-breakdown.md, implementation-pack.md, README.md, adr/, api/, diagrams/, all .sql).

**Backups (.bak files):**
- Removed 12 `*.bak-2026-05-23-pre-simplify` files left over from architecture-design simplification — pre-simplify content recoverable from git history.

**Docs synced to reflect post-cleanup state:**
- `plugin.json` description trimmed to the 11 remaining skills.
- `README.md` stage table replaced with 9-stage pipeline; both `rate-limiting` and `goals-tracking/arc42.md` examples linked.
- `plugin/README.md` quickstart rewritten without composite wrappers; atomic skill table updated.
- `CLAUDE.md` GATE table updated (`write-prd`/`architecture-design`/`decide-adr`); composite-wrapper section removed; cross-cutting list trimmed.
- `00-overview/file-structure.md` removed deleted template entries.

### Removed (earlier)

- **Stage 12 (`implementation-pack`) dropped 2026-05-25** — the impl-pack aggregator (former hard pipeline gate) is gone. Downstream stages (`break-tasks`, `prep-context`, `prep-review`, `ship`, `write-changelog`) read PRD / SAD / data-model / openapi / sequences / ADR DIRECTLY (now those downstream skills are also removed in the M1-M6 cleanup above).
- Removed `plugin/skills/pack-impl/` (skill + tests).
- Removed `plugin/tests/fixtures/pack-impl/` fixtures.
- Removed `document-templates/implementation-pack.md`.
- `scripts/sdlc_lint.py` no longer requires `implementation-pack.md`.

### Added
- `complete-sequence-diagrams` skill — auditor + completer for SAD §6: reads PRD §4, cross-checks SAD §6 by US-N heading match, iteratively (per UC, user-confirmed) generates Mermaid `sequenceDiagram` blocks for missing UCs, validates with `mmdc --parse-only`, flags new actors and ADR-potential decisions, adds async patterns (idempotency, retry, DLQ) to non-`localhost` flows. Supports `--flow <name>` for single-flow ad-hoc mode (replacement for `draw-sequence`).
- `generate-data-model` skill — end-to-end persistence runner: reads PRD + SAD §6.4 + sequences (+ optional Go domain structs), produces `delivery/<slug>/data-model.md` AND live `.up.sql` + `.down.sql` pairs AND an audit report in one invocation. Opinionated defaults: timestamp filenames, `IF NOT EXISTS` everywhere, only `created_at` (no `updated_at`, immutable-first), hard delete + audit table, `CREATE INDEX CONCURRENTLY` for existing tables, auto 3-step expand→backfill→contract for breaking changes. PII guard in seeds. Includes inline drift detection (`--drift-only`) against domain structs.
- `sdlc/document-templates/rules-migrations-baseline.md` — baseline `.claude/rules/migrations.md` that `generate-data-model` writes on first run if the repo has none.

### Deprecated
- `draw-sequence` — superseded by `complete-sequence-diagrams` (single-flow case covered via `--flow <name>`).
- `design-db` — superseded by `generate-data-model` (data-model.md is one of its outputs).
- `plan-migration` — superseded by `generate-data-model` (produces actual SQL files instead of just a plan; migration-plan content folded into the audit report).

Deprecated skills kept for backward compatibility; will be removed in a future cleanup.

### BREAKING
- Removed `intake` skill — `/sdlc-interview` is now the single entry-point for ideation phase
- Removed `brainstorm` skill — its responsibilities (strategic approaches, multi-perspective, devil's advocate) merged into expanded `interview` skill
- Removed `brainstorm.md` and `initiatives.md` templates — consolidated into expanded `idea-brief.md` (15 sections)
- `propose-adr` moved from gate 1 to gate 3 (prereq: architecture-brief.md §Trade-offs)
- `interview` rewritten as 14-phase autonomous protocol with Claude-driven RICE/Feasibility (was user-input only)

## [4.0.0] — 2026-05-30

Full-cycle upgrade. The toolkit now covers the complete `map-architecture → ship` pipeline (was `interview → break-tasks`). Mirrors the upstream [sdd](https://github.com/genkovich/sdd) pipeline under course-specific skill names.

### Added

**New backbone skills (close the cycle):**
- `map-architecture` — scans the codebase once, writes `docs/architecture-map.md` (repo-root, persisted). Every later stage reads it instead of re-scanning. Carries a §Frontend/UI foundation section so design work reuses the existing design system. On a greenfield repo, also scaffolds `tasks.json`.
- `clarify-prd` — ambiguity sweep over an existing `PRD.md`: surfaces contradictions, missing acceptance criteria, and scope gaps; tightens the PRD in place before design work begins.
- `roadmap` — `/sdlc-roadmap` utility that maintains `docs/roadmap.md` (Now / Next / Later / Shipped tables); `ship-feature` moves features to Shipped automatically.
- `implement-tasks` — TDD engine: SELECT → RED → GREEN → REFACTOR → GATE → COMMIT. Three modes: **sequential** (default), **agent-team** (via `TeamCreate`), **dynamic Workflow**. Stack-agnostic command detection; promotes staged migrations from `docs/features/<slug>/migrations/` into the repo's live migrations tree (re-stamping timestamps). Adds `SDLC-Task` / `SDLC-AC` trailers to every commit. Per-project overrides in `.claude/sdlc.local.md` (auto-created, gitignored).
- `review-feature` — clean-context `sdlc:reviewer`; stage-1 traces every AC end-to-end (PRD → sequences → data-model → api → tasks → code, gated on `target_surfaces`), stage-2 covers quality and non-functional concerns. Loops back to `implement-tasks` on CHANGES REQUESTED (no `/clear`). Emits `_review/review-<date>.md` (PASS / CHANGES REQUESTED).
- `ship-feature` — run-the-feature check, changelog entry, PR body (AC + ADR links + `SDLC-Task` history), forge detection (gh / glab), moves feature to `docs/roadmap.md §Shipped`, terminal handoff block.

**New mechanisms:**
- `target_surfaces` — declared in `sad.md` frontmatter by `architecture-design`; downstream skills (`complete-sequence-diagrams`, `api-forge`, `break-tasks`, `plan-tests`, `review-feature`) gate on it instead of re-deriving the surface taxonomy each time.
- `tasks.json` — machine-readable task DAG (`id`, `title`, `layer`, `deps`, `acs`, `dod`, `files_hint`) at `docs/features/<slug>/tasks/tasks.json`; emitted by `break-tasks`, consumed by `implement-tasks`. This artefact closes the previously broken design-to-implementation cycle.
- Staged migrations — `generate-data-model` now writes migration files to `docs/features/<slug>/migrations/`; `implement-tasks` promotes them into the live migrations tree.
- Depth-dial (`_shared/interview-depth.md`) — per-stage effort control across the backbone.
- Copy-ready stage-handoff blocks (`_shared/handoff.md`) — every skill ends with a formatted block the user can paste to start the next stage.
- Mermaid-check validation (`_shared/mermaid-check.md`) — called by architecture-design and complete-sequence-diagrams before any diagram is committed.

**9 plugin-namespaced agents** (dispatched as `sdlc:<name>`): `explorer` (haiku, codebase scan), `researcher` (sonnet), `strategist` (opus), `analyst` (opus), `devils-advocate` (opus), `critic` (opus), `test-author` (sonnet), `implementer` (sonnet), `reviewer` (opus). Model / effort policy in `_shared/agent-roster.md`.

**10 shared references** in `plugin/skills/_shared/`: `agent-roster`, `ask-style`, `critic`, `diagram-presentation`, `handoff`, `interview-depth`, `mermaid-check`, `size-matrix`, `socratic-loop`, `surfaces`.

### Changed

- **Existing backbone skills rewritten** to mirror the upstream sdd pipeline content under course names:
  - `write-prd` — now code-aware (reads `architecture-map.md`), Socratic, depth-dialed; output moved to `docs/features/<slug>/PRD.md`.
  - `architecture-design` — produces SAD (Arc42 + C4 L1/L2) and declares `target_surfaces` in frontmatter; also emits `adr/NNNN-*.md` stubs.
  - `complete-sequence-diagrams` — generic participants; surface-gated UI legs (only drawn when `ui` is in `target_surfaces`).
  - `api-forge` — surface-read (contract type driven by `target_surfaces`); drift-check enforces fix-the-source-first; scenario A (typed) vs B (PRD-derived).
  - `break-tasks` — now emits `tasks.json` (machine DAG) in addition to the human tracker and task files.
  - `plan-tests` — stack-agnostic (no hardcoded tool names); surface-gated tiers.
  - `classify-size` — updated decision matrix from `_shared/size-matrix.md`.
  - `fix-term` — multi-context `CONTEXT-MAP.md` support added.
  - `decide-adr` — blast-radius worthiness gate; lifecycle Proposed → Accepted explicit.
- **Per-feature artefact path** changed from `delivery/<slug>/` to `docs/features/<slug>/`. Repo-root artefacts (`architecture-map.md`, `roadmap.md`) live under `docs/`.
- **Commit trailers** renamed `SDD-Task` / `SDD-AC` → `SDLC-Task` / `SDLC-AC`.
- `plugin.json`, `README.md`, `CLAUDE.md`, `00-overview/` updated to reflect 17-skill, 9-agent, 10-shared-ref counts and the new full-cycle description.

### Note — `generate-data-model` is a deliberate partial mirror

`generate-data-model` **intentionally does NOT adopt** the upstream sdd stance of deriving DB conventions from the target repo. It keeps the course's opinionated DB defaults: `created_at`-only audit (immutable-first, no `updated_at`), hard delete, no CHECK constraints / triggers / business-level DEFAULTs (DB as dumb storage), SQL-first migrations, timestamp-prefixed idempotent filenames. From the upstream pipeline it borrows **only** staged migrations, drift-check, and reading `architecture-map.md` as a convention source. Future maintainers: do not "fix" this toward the stack-agnostic upstream stance — the deviation is course pedagogy, not an oversight.

---

## [3.0.1] — 2026-05-19

OSS-readiness pass — translate all docs / skills / templates / overview / scripts to English and remove project- and course-specific framing so the toolkit drops into any team unchanged.

### Changed

- All 27 `plugin/skills/<name>/SKILL.md` bodies translated to English (frontmatter triggers, `## Questions for discussion`, `## Template`, anti-patterns prose). Section structure and opinionated tone preserved verbatim.
- All `document-templates/*.md` + `adr/` + `api/` + `diagrams/` skeletons translated (placeholders, `<!-- Why: ... -->` guidance, table headers, Mermaid node labels).
- `00-overview/*.md` (process-map, DoR, DoD, mvp-vs-full, rollout-plan, process-metrics, file-structure) translated end-to-end; Mermaid labels rendered in English.
- `scripts/generate-gates.sh` and `scripts/sdlc_lint.py` — comments and user-facing strings translated.
- Top-level `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `plugin/README.md`, `Makefile` translated.
- `plugin/plugin.json` `description` rewritten in clean English.

### Removed

- Course-, project-, and team-specific framing in prose (community-chat link, internal team and repo names, personal name and email in non-attribution prose). OSS attribution stays in `LICENSE` (MIT Copyright) and `plugin.json` `author` block per OSS norm.

### Not changed

- `examples/` (rate-limiting, goals-tracking) — case-study scope, intentionally left in Ukrainian and out of this pass.
- `LICENSE` — untouched (MIT Copyright preserved).
- `plugin.json` `author`, `repository`, `homepage` — untouched.
- `plugin/tests/` fixtures and rubric — out of scope for this pass.

## [3.0.0] — 2026-05-18

OSS-ready release. **Breaking** — `sdlc/01-stages/` removed; skills are now the single source of truth.

### Added

- **5 phase wrappers:** `sdlc:design` (03-07), `sdlc:detail` (08-10), `sdlc:impl-prep` (11-14), `sdlc:ship` (15-18). Each delegates to atomic skills with size-aware skip-logic per `00-overview/mvp-vs-full.md`. Single commit per phase.
- **3 cross-cutting atomic skills:**
  - `sdlc:propose-adr` — MP-threshold check (3 AskUserQuestion: hard-to-reverse / surprising / real trade-off) → ADR stub with `Status: Proposed` + bidirectional `**Locked in:**` backlink in `brainstorm.md`.
  - `sdlc:fix-term` — lazy `CONTEXT.md` glossary bootstrap (single- or multi-context via `CONTEXT-MAP.md`), canonical definition + NOT cross-reference, generic-tech-term filter, conflict check.
  - `sdlc:classify-size` — 4 AskUserQuestion (PR count / time / new module-API-migration / breaking changes) → `delivery/<slug>/.size` one-liner (XS/S/M/L/XL).
- `plugin.json` full OSS metadata: author, license, homepage, repository, keywords.
- `sdlc/LICENSE` — MIT.
- `sdlc/plugin/README.md` — install, quickstart, skill index, conventions.
- `sdlc/CONTRIBUTING.md` — how to add atomic / wrapper / template; PR checklist.
- `sdlc/CHANGELOG.md` (this file).

### Changed

- **Skill files now contain full protocol + DoD + anti-patterns** (previously skills did `Read sdlc/01-stages/NN-*.md` for protocol). Edit one place per stage, not two.
- `sdlc:intake` refactored to delegate to `sdlc:fix-term` (was inline §B CONTEXT bootstrap) and `sdlc:propose-adr` (was inline §D/§E MP-check + ADR stub). 176 → ~150 lines, no duplicated logic.
- `sdlc:intake` §G — recommends `sdlc:classify-size` as next step before design phase.
- `document-templates/*.md` HTML-comment headers updated to point at `plugin/skills/<name>/SKILL.md` (was `01-stages/NN-*.md`).
- `examples/goals-tracking/{idea-brief,SPEC}.md` HTML-comment headers updated.
- `sdlc/README.md` — stage table now points at skills, not removed stage files.
- `sdlc/CLAUDE.md` — "How to work with artefacts" rewritten to reference skills.

### Removed

- `sdlc/01-stages/01-raw-idea-intake.md` ... `18-obsidian-kb-sync.md` (18 files). Content merged into corresponding `plugin/skills/<name>/SKILL.md`. Backup tag `pre-phase-1-stages-merge` preserves prior state for diff.

## [2.1.0] — 2026-05-17

### Added

- `sdlc:intake` composite wrapper (stages 01-02 + MP-threshold ADR-propose + lazy `CONTEXT.md` glossary with inline term-resolution).
- Bidirectional `**Locked in:** [[adr/NNNN-...]]` backlink in `brainstorm.md` after ADR stub creation.

## [2.0.0] — 2026-05-15

### Added

- 16 atomic skills for stages 03-18 (`write-spec`, `draft-architecture`, `write-arc42`, `draw-c4`, `draw-sequence`, `design-db`, `plan-migration`, `define-api`, `decide-adr`, `pack-impl`, `break-tasks`, `prep-context`, `plan-tests`, `prep-review`, `write-changelog`, `sync-kb`).

### Removed

- `sdlc-stage-runner` (consolidated 18-stage runner; superseded by atomic skills with hard-prereq gates).

## [1.0.0] — 2026-05-12

### Added

- Initial Claude Code plugin scaffold with `sdlc:interview` (stage 01) and `sdlc:brainstorm` (stage 02).
- `document-templates/` for all 18 stage artefacts.
- `00-overview/` — process map, definition-of-ready, definition-of-done, MVP-vs-full matrix.
- `examples/rate-limiting/` — synthetic end-to-end example.
- `Makefile` with `sdlc-check` and `sdlc-metrics` targets.

[Unreleased]: https://github.com/genkovich/agentic-engineering-course/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/genkovich/agentic-engineering-course/compare/v3.0.1...v4.0.0
[3.0.1]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v3.0.1
[3.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v3.0.0
[2.1.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v2.1.0
[2.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v2.0.0
[1.0.0]: https://github.com/genkovich/agentic-engineering-course/releases/tag/v1.0.0
