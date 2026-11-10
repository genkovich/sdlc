# Design line — order, file layout, input ladder, and design-tool rules

> **Reference-only.** Not a skill. The design-line skills (`design-system`, `ux-flows`,
> `prepare-design-spec`, `screens`), the `design-keeper` agent and `verify-ui` read this file for
> where their artifacts live, where a feature's intent comes from when there is no PRD yet, and the
> hard rules for drawing in a design tool through its MCP (pen.dev, Figma, any other) or in plain
> markdown. Each skill keeps a one-line pointer and its own delta; the rules live **only** here.

## TL;DR (короткий вступ українською)

Дизайн-лінія = пʼять кроків, які повторюються на кожній UI-фічі:

```text
/sdlc:design-system (раз на репо) → /sdlc:ux-flows <slug> → /sdlc:prepare-design-spec <slug>
  → /sdlc:screens <slug> → код екранів → /sdlc:verify-ui <slug>
```

- **Без PRD теж працює.** Нема `PRD.md` → вхід = коротка історія користувача на 3-5 речень
  (`docs/features/<slug>/story.md` або прямо в команді). Гілки помилок беремо з питання «що може
  піти не так», а стани без джерела в AC позначаємо як виведені з історії. Є PRD і SAD (модуль 6+)
  → поведінка повна. Деградація, не відмова. Є PRD і ще текст у команді → PRD лишається основою,
  а текст додає вказівки (звузити до історії, додати збої чи екрани) з позначкою `N-NN`;
  суперечність з PRD = одне питання і прогалина PRD для `/sdlc:clarify-prd`.
- **Канон дизайну репо-рівня** лежить у `docs/design/`, усе фічеве лежить у `docs/features/<slug>/`.
- **Інструмент будь-який, у якого є MCP у сесії.** У каноні `tool` = `pencil` (pen.dev), `figma`
  або назва іншого інструмента; документ дизайну лежить у полі `design_file` (шлях у репо або URL).
  Старі поля `pen_file` і `figma_file` теж читаються. Бібліотеку звіряє один агент `design-keeper`
  для будь-якого інструмента: сам знаходить tools інструмента, читає його гайд і йде тими самими
  кроками.
- **Перед записом перевіряємо, що відкритий саме файл з канону**, інакше стоп. Дозвіл писати
  визначає власник файла. Файл у репо належить тому, хто запускає скіл: пишемо без питання, і в
  headless теж. Файл за URL (Figma тощо), який не створили в цьому прогоні: одне питання, а без
  відповіді лише пропозиції. Без дозволу `screens` у файл дизайнера нічого не пише: питає, чи
  можна намалювати екрани на окремій сторінці «Screens · <slug>» (там же «Drafts · <slug>» з
  новими компонентами); «ні» або headless → code mode. Аркуш основ і компоненти малюємо тільки в
  порожньому файлі, і аркуш однаковий у кожному інструменті.
- **pen.dev:** `.pen` руками не правимо; після змін зберегти (`save` з `uri` або Cmd+S); перед
  `git checkout` зберегти й закрити; PNG кожного стану експортуємо і перевіряємо `test -s`, бо
  експорт може тихо не створити файл або лишити його порожнім.
- **Figma:** зберігається сама. Для Figma Console у відкритому файлі має працювати плагін Desktop
  Bridge. PNG буде, коли якийсь tool пише файл або дає посилання на нього; інакше прогалина в
  §Source, а id вузлів лишаються.
- **Нема токенів або проєкт порожній** → `design-system` збирає основу разом з людиною: коротке
  сократичне інтервʼю, референси, 2-3 напрямки на вибір, потім токени двома шарами (світла і темна
  тема, контраст AA пораховано) у файл теми проєкту або `docs/design/tokens.json`, і стартовий
  набір компонентів. Без каналу питань лише пропозиція в каноні.
- **Екрани вже намалював дизайнер** → `screens` у режимі розбору (`--from <url>`): читає фрейми,
  у файл нічого не пише, розкладає на екрани й стани, позначає, чого бракує, і звіряє компоненти
  з інвентарем; привʼязка «компонент дизайну ↔ компонент коду» з props живе в каноні.
- **code-mode доступний завжди**: нема MCP → markdown-вайрфрейми і названа деградація.

---

## 1. The line and where it plugs into the backbone

| Step | Skill | Runs | Reads | Writes |
|---|---|---|---|---|
| 1 | `design-system` | once per repo (refresh when the foundation changes) | the code's tokens + components; `docs/architecture-map.md` if present | `docs/design/design-system.md` (+ the design document through its tool, `tool` ≠ `code`; + the tokens in the project's theme file or `docs/design/tokens.json` when it built the foundation) |
| 2 | `ux-flows` | per UI feature | the input ladder (§3) + the canon | `docs/features/<slug>/ux-flows.md` (+ `story.md` when the story came inline) |
| 3 | `prepare-design-spec` | per UI feature | the input ladder + `ux-flows.md` + the canon + the repo | `docs/features/<slug>/design-spec.md` |
| 4 | `screens` | per UI feature | `ux-flows.md` + `design-spec.md` + the canon (+ `sad.md` §6, contracts when present); read mode: the designer's frames | `docs/features/<slug>/screens.md` + `docs/features/<slug>/screens/*.png` (read mode: nothing in the design file) |
| 5 | `verify-ui` | after the screens are built in code | every state in `screens.md` + `design-spec.md` §16 (+ PRD §5 when present) | `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md` + its screenshots folder |

**Without the backbone (a story, no PRD/SAD)** — run the five steps in order; every skill accepts a
missing upstream artifact and says what it used instead.

**Inside the backbone (PRD + SAD exist)** — `ux-flows` runs after `clarify-prd` and before
`architecture-design` (the flows are evidence for `target_surfaces`); `prepare-design-spec` runs
after `ux-flows`; `screens` runs after `api-forge` and before `break-tasks` (by then the states are
derivable from §5 ACs, `sad.md` §6 branches and the contract error responses). The `screens.md`
manifest is the contract downstream work is pointed at, never the raw design file. `verify-ui`
reads it; `break-tasks`, `implement-tasks` and `review-feature` do not read it on their own yet, so
name the file in their prompt (`/sdlc:break-tasks <slug>` + «UI states:
`docs/features/<slug>/screens.md`»). The same holds for `ux-flows.md` and `architecture-design` /
`plan-tests`.

The order is a recommendation, not a gate: each skill reads whatever upstream artifacts already
exist and names the missing ones in its handoff.

## 2. File layout (fixed — the module checklist is written against it)

```text
docs/design/design-system.md                     # canon: tool, posture, tokens, component inventory
docs/design/tokens.json                          # only when design-system built the foundation in a project with no stack (DTCG)
docs/design/<name>.<ext>                         # a tool with files on disk (pencil: .pen): the one design document (components + screens); a cloud tool (figma) keeps only its URL in the canon
docs/features/<slug>/story.md                    # the short user story (when there is no PRD)
docs/features/<slug>/ux-flows.md                 # flows + screen inventory (SCR-NN) + coverage
docs/features/<slug>/design-spec.md              # spec (BR-NN) + embedded Definition of Done (DOD-NN)
docs/features/<slug>/screens.md                  # manifest: screens × states × components
docs/features/<slug>/screens/SCR-NN-<state>.png  # tool ≠ code, when the tool can export: one PNG per state
docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md   # live browser verdict
docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/     # its screenshots
```

Repo-level canon goes under `docs/design/`; everything feature-specific goes under
`docs/features/<slug>/`, like every other SDLC artifact. Never invent a third location.

**Templates are read and written, never copied with `cp`.** A skill's template lives in the
plugin's folder; Claude Code treats the plugin cache as a sensitive path, so `cp` from it stops
the run for a permission prompt (and is refused headless). Read the template with Read, write the
artifact with Write.

## 3. The input ladder — where a feature's intent comes from

Every design-line skill resolves the feature's intent once, top-down, and uses the **first**
source that exists. It records which one it used (frontmatter `input:` + the handoff).

1. `docs/features/<slug>/PRD.md` — §4 user stories + §5 acceptance criteria (`AC-NN`). **Full mode.**
2. `docs/features/<slug>/design-spec.md` — §5 target flow, §6 requirements (`BR-NN`), §8 states.
3. `docs/features/<slug>/story.md` — the short user story.
4. `docs/features/<slug>/idea-brief.md` — the interview's brief.
5. **Inline story** in the invocation («/sdlc:ux-flows chat Як користувач, я …») —
   the first skill that receives it writes it verbatim to `docs/features/<slug>/story.md` (from
   `ux-flows/templates/story.md`) so the next skills read the same words.
6. Nothing at all → ask for 3–5 plain sentences: who, what they want to do, why, how they know it
   worked. Missing intent is the only reason to stop; a missing PRD or SAD never is.

**Read mode of `screens`: the frames are a source.** When `screens` reads a designer's frames
and sources 1–5 are absent, the frames themselves are the intent: screens from the frame names,
row labels and groups, `input: frames`, no question asking for sentences; it stops only when
there are no frames. Every other skill keeps the ladder as above.

**Degrade, don't refuse.** Sources 2–5 are **story mode**: there are no `AC-NN` ids, so the skills
number what they find and keep its origin visible.

**Text in the invocation next to a source** (`ux-flows`). When the ladder found a source 1–4 and
the command also carries text («/sdlc:ux-flows chat лише історія про першого співрозмовника, і
подумай, що буде, коли мережа зникне»), the source stays the base and the text is **additional
instructions**: narrow to one story, add failures, screens or constraints the source does not
mention. Each such item gets its own token `N-NN` (from the invocation) in the flows, the screen
inventory and the coverage table; `ux-flows.md` §Source quotes the items (they are not written to
`story.md`), and the later skills read them from there. It never replaces the source:

- **Text contradicts the source** (e.g. the PRD says a chat opens only after a match, the text says
  from any profile) → one `AskUserQuestion`: follow the source / follow the text. Whatever is
  picked, the decision goes under `## Assumptions`, and with a PRD source the contradiction is
  also a PRD gap for `/sdlc:clarify-prd`. Headless → follow the source, record it the same way.
- **Text asks to think about failures** → the «what can go wrong» question (§4) runs in full mode
  too, at any depth.
- No source above the inline story (source 5) → the text *is* the story: `S-N`, not `N-NN`.

### Provenance tokens (every derived branch, state and requirement carries one)

| Token | Meaning | Where it comes from |
|---|---|---|
| `AC-NN` | PRD acceptance criterion | `PRD.md` §5 |
| `BR-NN` | design-spec requirement | `design-spec.md` §6 |
| `S-N` | sentence N of the story | `story.md` / inline story |
| `N-NN` | an additional instruction from the invocation text, next to a source 1–4 | the command line («з команди») |
| `frame:<node id>` | a state the designer drew that no flow branch names (read mode of `screens`) | the designer's frame |
| `W-NN` | «what can go wrong» item the user confirmed | the §4 question below |
| `§6:<flow>` / `contract:<status>` | SAD runtime branch / API error response | `sad.md` §6, `contracts/` (backbone only) |
| `D-NN` (`derived`) | inferred by the agent from the story, **not** confirmed by anyone | headless runs, `easy` defaults |

A state or branch with no `AC`/`BR`/`§6`/`contract` source is marked as coming from the story
(`S-N`, `W-NN`), from the invocation (`N-NN`) or as derived (`D-NN`, so flows and tables can point at it). Derived items are
listed in the artifact's `## Assumptions` section so a human can veto them; they never silently
become requirements. When a user later confirms a `D-NN`, it is renumbered as the next `W-NN`.

### State vocabulary — one list for `design-spec.md` §8, `screens.md` and `verify-ui`

The six classes below are **checked for every screen**: each gets a row, either a real state or one
`N/A: <reason>` row. On top of them a screen may have **named states** that come from flow
branches (see the list under the table). The same id names the row in `design-spec.md` §8, the row
in `screens.md`, the design-tool frame (`<slug> · SCR-NN · <state>`), the PNG (`SCR-NN-<state>.png`)
and the `verify-ui` verdict row.

| Class | Meaning | Older names it replaces |
|---|---|---|
| `default` | the screen with its normal data, ready to use | Ready |
| `loading` | waiting for data or for an action to finish | Saving, Pending |
| `empty` | nothing to show yet | — |
| `error` | something failed; the screen says what and how to recover | — |
| `success` | an action finished; the user sees the confirmation | — |
| `validation` | input rejected before it is sent | — |

- **Named states** come from flow branches and sit next to the six classes:
  - `<class>-<variant>` in kebab-case when it is a second state of one class: `error-undelivered`,
    `error-peer-unavailable`, `empty-first-open`;
  - a bare kebab-case feature name when the branch is a product state that fits none of the
    classes: `ended` (the other person closed the conversation; not an error, not empty).

  Every named state carries its source token (`W-NN`, `D-NN`, `N-NN`, `AC-NN`, `BR-NN`, `S-N` …) and gets
  its own frame, PNG and verdict row under the same id. A bare name never reuses a class name.
- **Hover / focus / disabled are component states**, not screen states. They come from the
  components in `docs/design/design-system.md` («States it supports») and get no screen frame.
- **Default reading of the classes, no source needed (`derived`):** a screen that fetches data or
  sends an action has `loading` and `error` (the network can be slow or fail even when nobody
  named it); a screen that shows a list or a history has `empty`; a screen with an action that
  finishes with feedback has `success`; a screen with user input has `validation` unless the
  rejection is only a disabled control. These are real states with the token `derived`; dropping
  one needs an `N/A` with a concrete reason about this screen (`loading · N/A: the modal opens with
  data already on screen`), never «no source».
- A class that does not apply to a screen gets one `N/A: <reason>` row, never silence. An `N/A` row
  has **no frame, no PNG and no verdict row**: it records that the class was checked
  (`validation · N/A: the disabled Send button is a component state`).

## 4. «What can go wrong» — the branch question in story mode

A story describes the happy path. The error branches are where amateur UI comes from, so in story
mode `ux-flows` asks for them explicitly after it has drafted the happy path:

- **One `AskUserQuestion`, `multiSelect: true`**, phrased per [`ask-style.md`](./ask-style.md):
  context = the drafted happy path in one sentence; up to 4 options = the most likely failures
  **for this story** (pick from: no data yet / empty, slow or failed network, the other person or
  object is gone or blocked, input rejected, no permission or not signed in, duplicate or
  rate-limited action). Every step that calls the server gets a failure candidate of its own
  (creating, sending, loading a list); when there are more candidates than 4 options, ask a second
  question rather than dropping them. The free-text «Other» answer adds more.
- Each chosen item becomes `W-NN` (Confirmed by the user) and gets a branch in a flow.
- In full mode (PRD present) the same question runs once for failures the ACs missed at `hard`
  depth, and at any depth when the invocation text asks to think about failures; any `W-NN` there
  is also flagged as a PRD gap for `/sdlc:clarify-prd`.

## 5. Runs with no one to ask (headless, `claude -p`, CI)

If the session has no question channel (`AskUserQuestion` unavailable, denied, or the run is
non-interactive), the skill **does not stop and does not invent answers silently**: it takes the
`easy` path — decides with defaults, marks every such decision as `derived` and every inferred
failure as `D-NN`, writes them into the artifact's `## Assumptions` section, and says
«no question channel — N assumptions recorded» in the handoff.

## 6. Tool modes — any design tool with an MCP, or `code`

The tool is chosen **once** in `docs/design/design-system.md` frontmatter `tool:`; no feature skill
re-asks it. Never store the choice in `.claude/sdlc.local.md` (per-developer, gitignored).

**`tool` names the product, not the MCP server.** `pencil` = pen.dev, `figma` = Figma (whichever
Figma server the session has, §8), any other lowercase product name = that tool (§9), `code` = no
design tool. Canons written before 4.8 keep `pencil` / `figma` and stay valid.

**The canon's design document.** Frontmatter `design_file`: a repo path for a tool that keeps
files on disk (`docs/design/app.pen`), the file URL for a cloud tool
(`https://www.figma.com/design/<fileKey>/<name>`). Everywhere a skill or agent reads «the canon's
design file», it resolves it in this order: `design_file`, else the legacy `pen_file`, else the
legacy `figma_file` (canons written by sdlc 4.7). New canons write only `design_file`.
`library_frame` = the frame, page or section that holds the reusable components. It stays `""`
when the keeper reported that nothing could be drawn (a read-only tool, an empty document without
write permission, a read-only `inventory` run); the canon then says why in `## Assumptions`.
`screens` with an empty `library_frame`: writes allowed → `code` mode, named («the design document
has no library yet — run `/sdlc:design-system`»), so the document stays empty for the
foundations run; writes not allowed → gate 6 (the «Screens · <slug>» question, else `code` mode).

| Mode | Screens live in | Per-state source-ref | PNG per state |
|---|---|---|---|
| a design tool (`pencil`, `figma`, `<name>`) | the canon's design file (one document holds the library and the screens) | node id | required when the session can export (gate 5 below); else a named gap in `screens.md` §Source |
| `code` | inline markdown wireframes in `screens.md` | «wireframe below» | none — the built screen + the `verify-ui` screenshot are the visual evidence |

**Flow boards** (draw mode): after the state grid, `screens` draws each flow of `ux-flows.md` as a
board «Flow · <flow name>», the real states' thumbnails joined by labelled arrows, error branches
dashed; the mermaid stays the source, the board is its render. A `Flow · ` frame is never a frame
of the feature (no read-mode question, no state). Figma adds real prototype connections and a flow
starting point. Procedure: `screens/references/flow-boards.md`.

**Read mode** (`/sdlc:screens <slug> --from <url>`, «розбери екрани дизайнера»): the designer
already drew the screens. `screens` reads their frames through the tool's read tools, writes
**nothing** into the design file (no permission needed), maps each frame to a screen and a state,
marks every class drawn / `N/A` / missing, maps every instance to the canon's inventory, and
records the behaviour the tool returns. The manifest has the same format, so `verify-ui` and the
code work do not change. Procedure: `screens/references/read-frames.md`.

**What counts as a design tool.** An MCP server in this session whose tools can read a design
document's nodes (frames, components, variables). Find it by listing the session's tools, deferred
ones included (load a deferred tool's schema before calling it). A browser, a docs server or a
screenshot service is not a design tool. The tool prefix differs per session (`mcp__pencil__…`,
a plugin prefix, `mcp__figma-console__…`), so match by the tool names, never by a fixed prefix.

**Capabilities** — what to look for in any design tool; §7–§9 name them per tool:

| Capability | pen.dev (§7) | Figma (§8) | another tool (§9) |
|---|---|---|---|
| target document | `get_app_state`: the active document; tools take its `uri` | Console: `figma_get_status`, `figma_list_open_files`; official: the file key in every call | its «current document» tool, else the id it takes per call |
| its own guide for agents | `read_skill()`, then `read_skill({ path })` | the Figma plugin's skills, the `create_design_system_rules` prompt; Console: the server's instructions | whatever it ships |
| read nodes / components / variables | a read-only `execute` | Console: `figma_search_components`, `figma_get_variables`, `figma_get_styles`; official: `get_metadata`, `get_variable_defs`, `search_design_system` | its read tools |
| write | `execute` | Console: `figma_execute` and the variable tools; official: `use_figma` (beta) | its write tools; none → report only |
| save | `save` with the `uri` (newer servers), else the user's Cmd+S | saves by itself | a `save` tool, else the user saves |
| look | `TakeScreenshot` inside `execute` | Console: `figma_capture_screenshot`; official: `get_screenshot` | its screenshot tool |
| export a PNG to disk | `Export` inside `execute` writes `<nodeId>.png` | Console: `figma_get_component_image` returns a URL → `curl` | a tool that writes a file or returns a URL |

**The gates, the same for every tool** (`design-keeper` and `screens` follow them; the tool's
section adds its specifics):

1. **Target-document gate before every write.** The tool's target must be the canon's design
   file. Compare absolute paths for a file on disk and file keys for a URL, never the raw strings.
   Another document, none, or the app closed → STOP and tell the user exactly what to open; never
   write into a foreign document, never create probe nodes.
2. **Only the tool changes the document.** Never read, edit or rewrite the design file on disk
   with file tools, `sed`, `python` or `jq`; copying a whole file (`cp kit.pen docs/design/app.pen`)
   is fine.
3. **The tool's own guide governs how to call its tools** (syntax, batching, where nodes go). Read
   it once, before the first call that depends on it (pen.dev: before the first `execute`,
   read-only queries included), at the latest before the first write. The schema and the property
   names come from that guide; when it is silent, read an existing node of the same kind and copy
   its shape. **Never create a probe node** to guess a name (a top-level `probe` frame was left in a
   real document this way). The guide never overrides these gates: which document, what may be
   written, one library per document (§7.11 applies to every tool), when to stop.
4. **Save, then check.** A `save` tool → call it; a tool that saves by itself → nothing to do;
   neither → ask the user to save. Then check: a local file must change on disk (`stat -f '%m %z'`
   before and after on macOS, `stat -c '%Y %s'` on Linux); a URL is checked by reading the written
   variables / nodes back through the tool. An unsaved local file is named in the handoff, never
   committed.
5. **Export gate.** A PNG counts only when the file exists at its final path and passes `test -s`
   (exists and is not empty): an export can leave no file or an empty one without a failing status.
   An image the tool returns only into the conversation is a look, not an export. No export
   capability in the session → no PNG and a named gap in `screens.md` §Source; the node id stays
   the source-ref. Shell steps run **one command per call**: `test -s <file>`, then `mv`, then
   `test -s` again, each its own call; no loops, no `&&` chains, no `$(…)` substitutions or pipes
   (a headless run rejects them, an interactive one asks permission for each), no helper scripts
   outside the repo (no `/tmp`). Counting for a self-check or a handoff goes through Read and Grep
   (its count mode), never a composed command; looking around goes through Glob and Read, never
   `ls` / `wc` (on the plugin's own folder neither). A subagent whose result the next step needs
   (the explorer's map, the keeper's report) is dispatched in the foreground
   (`run_in_background: false`), so the run never pauses on «still scanning, waiting».
6. **Who may write: the file's owner decides** (`allow_writes`, recorded in the canon as
   «Foundations write permission»):
   - `design_file` is a **repo path** → the file belongs to the person running the skill: write
     without asking, headless too;
   - `design_file` is a **URL** (Figma or another cloud tool) and the person **created it in this
     `design-system` run** → write;
   - a URL file not created in this run, **empty or with a library** → one question to the person,
     showing what would be written; headless → no permission, only proposals in the canon.

   Without permission `design-keeper` writes nothing and returns proposals, and `screens` writes
   **nothing** into the designer's file on its own: interactive, it asks once «Намалювати екрани
   на окремій сторінці «Screens · <slug>» у цьому файлі?». Yes → every state frame goes on that
   page (Figma: a page; another tool: its page, else one top-level frame), and new, `code-only`
   and changed components go in a frame «Drafts · <slug>» on the same page, listed in the handoff
   for the designer; the library and every other page stay untouched. No, or headless → `code`
   mode (inline wireframes, no PNG). The answer is recorded in the canon as «Screens write
   permission», next to «Foundations write permission», and reused until the person changes it. With
   permission or without, the foundations sheet, the components (and the temporary «DS ·
   Directions» sheet of `design-system` step 4b) are drawn only in an empty document; a document
   with a library only gets its missing foundations.

**The foundations sheet — one layout in every tool.** `design-keeper` draws it in an empty
document, the same structure in pen.dev, Figma or any other tool: a frame «Foundations» with a
title and one subtitle line; «Colours» as one card per theme side by side (dark and light), every
semantic colour a swatch with its name and the primitive under it, the theme set by the tool's own
mechanism on the card (Figma: the collection mode; pen.dev: `theme` on the card frame);
«Typography» as one row per size of the scale (name, font / size / line height, a sample line);
«Spacing» as bars with name and value, each bar's width bound to its variable; «Radii» as squares
with name and value. Every value is bound to a variable or style, never a literal. The components
go below it. The detail lives in `design-keeper` step 5.

**Token values follow the code on «Оновити».** When a token changes in the code, `design-system`
«Оновити» has the keeper set the mirroring variable to the new value, per theme: without a
question in a repo file, after one question that shows «before → after» in a URL file with write
permission, never without permission. New tokens are added; a variable the code does not have
(a designer's own, or a token deleted from the code) is never touched or deleted, only listed.
The sheet follows by itself; its numbers and value labels are rewritten.

**Local path vs URL.** Every disk step (`test -s <file>`, `stat` before/after,
`git status --porcelain -- <file>`, a separate commit for the design file) applies only when the
design file is a local path. A URL has nothing in the repo to check or commit.

**Degrade, don't block.** The chosen tool's MCP is not connected in this session → run `code`
mode and write the degradation into `screens.md` §Source and the handoff («<tool> MCP unavailable
— code-mode wireframes»).

## 7. pen.dev (Pencil MCP) — hard rules

The Pencil tools: `get_app_state`, `execute`, `read_skill`, `get_style`, `save` (newer servers),
`browser`, prefixed per session (e.g. `mcp__pencil__execute`). The design file is a local `.pen`.
Every `execute` and `save` call carries the document (the parameter the tool's schema names:
`uri` = `file:///<absolute path>`, or `filePath` = the absolute path), the snippet in `input`
(never `code`), and a `description` (3–8 words starting with a verb, shown in pen.dev's history).
No call goes without the document, even when the server would fall back to the active one.

1. **Never edit `.pen` JSON by hand.** The file is JSON on disk, but it is changed only through the
   pen.dev app, its MCP, or its CLI: no `Read`/`Edit`/`Write`, no `sed`, no `python`, no
   `json.dumps` on a `.pen`. Copying a whole file (`cp kit.pen docs/design/app.pen`) is fine.
2. **Open-document gate before every write.** Older servers write into whatever document is
   active in the app; newer ones take the document's `uri` and refuse a document that is not open
   («wrong .pen file»). Either way, call `get_app_state` first; continue only when the canon's
   design file is the active document, and pass it in **every** `execute` and `save` call (`uri` =
   `file:///<absolute path>`, or `filePath`, whichever the schema names), not only where a call
   would fail without it. Anything else (another file, no file, app closed) →
   STOP and ask the user to open the `.pen` in pen.dev (macOS: `open <path>`); never write into a
   foreign document, never create probe nodes.
3. **Persist, then check the disk.** MCP edits live in the app's memory until the document is
   saved. When the server offers a `save` tool, call it with the document's `uri`; otherwise ask
   the user for Cmd+S. Then confirm the file on disk changed (`stat -f '%m %z' <path>` before/after
   on macOS, `stat -c '%Y %s'` on Linux). An unsaved `.pen` is named in the handoff, never committed.
4. **Before `git checkout` / `pull` / `rebase`: save and close the `.pen`.** An open document
   survives the branch switch in memory and the next save writes the old branch's design over
   the new one.
5. **Conflicts are resolved in the app.** Keep both versions, open one as the base, re-apply the
   other's changes in pen.dev. Never merge `.pen` JSON by hand.
6. **One app version per team.** A newer pen.dev rewrites the file format on save; keep a copy of
   the file before opening it in a different version.
7. **No transitions between frames.** pen.dev has no prototyping links. A flow on the canvas =
   static frames placed left to right in flow order, plus the flow board `screens` draws
   («Flow · <name>»: the states' thumbnails joined by drawn arrows), which is a diagram, not
   transitions. A clickable flow lives in code (a `browser` node can show `localhost` next to the
   frames).
8. **Export gate.** Inside `execute`: `Export([nodeId1, nodeId2, …], "png", "<absolute dir>")`
   writes one file per node, named by the node id: `<dir>/<nodeId>.png`. An export can fail
   without a failing status, leaving no file or an empty one, so for **every** node:
   `test -s <dir>/<nodeId>.png` → `mv` to `SCR-NN-<state>.png` → `test -s` again (`-s` = exists
   and is not empty), one command per call (§6 gate 5). A failed check fails the gate; the screen
   is not done.
9. **Variable sync overwrites.** Syncing variables from CSS overwrites same-named variables in the
   document (a dark-theme colour was lost this way); keep a copy of the `.pen` before a sync.
10. **The PNGs are the review surface.** A real `.pen` is megabytes of JSON with random ids; nobody
    reviews its diff in a PR. Put the exported PNGs in the PR instead.
11. **One component library per document.** A document that already has reusable components (a
    course kit, a teammate's file) already has its library, whatever its frame is called
    («Components · Chat»): it is recognized, never duplicated. «DS · Foundations» is created only
    in a document with no reusable components at all, and only there does `design-keeper` draw
    the foundations sheet and the components. In a document with a library, a component that
    exists only in code (`code-only` in the canon) is drawn by `screens` the first time a screen
    needs it (into the library frame; without write permission only on the «Screens · <slug>» page
    the person allowed, §6 gate 6). The procedure lives in `design-keeper`; the canon records the
    frame as `library_frame`. The same rule holds in every tool.
12. **A variant is its own component.** pen.dev has no variant sets: each variant, size and state
    is a separate reusable component named `<Component> / <Variant> / <Size or state>`.

## 8. Figma (optional, when the team has a designer)

The canon's design file is the file URL; its file key is the path segment after `/design/` (or
`/file/`). `library_frame` is **the page** that holds the components, written as `<page>`, or
`<page> / <section>` when they sit in one section of it; a page is Figma's top level, so
components on a page's canvas are never `(top level)`. Screens
record a node id per state. Two MCP servers exist; use whichever the session has:

- **Figma Console MCP** (Southleft, not a Figma product). Writes only into files where the
  **Desktop Bridge** plugin runs in Figma Desktop (Plugins → Development → import the manifest that
  `npx figma-console-mcp@latest --print-path` prints, then run it in the file). `figma_get_status`
  (with `probe: true`) and `figma_list_open_files` tell which files are connected and which one is
  the active target; with several connected, pass `fileKey` on every call (`figma_execute` takes
  one). `figma_execute` runs plugin-API JavaScript in the file; variables also through
  `figma_setup_design_tokens` / `figma_batch_create_variables`; components through
  `figma_search_components` (node ids are per session: search again in every session).
  Look: `figma_capture_screenshot`. PNG to disk: `figma_get_component_image` returns an image URL
  (it goes through the REST API, so it needs the token the server was started with) → `curl -sSfL
  -o <path> <url>` → `test -s`. REST renders the cloud state, which can lag behind what the plugin
  just drew (`figma_capture_screenshot` shows the live state): export after the look; no URL or a
  failed `curl` → that state is the named gap. Its server instructions are its guide.
- **Official Figma MCP.** Reading works on any plan: `get_metadata`, `get_variable_defs`,
  `get_design_context`, `get_screenshot`; `search_design_system` and `get_libraries` on the remote
  server only. Writing (`use_figma`) is **beta**, remote only, and needs edit access to the file and
  a **Full** seat outside the user's own drafts (a Dev seat writes only in its drafts). Read calls
  are limited per seat (View / Collab: 20 a month), so read in batches. Its guide: the Figma
  plugin's skills (`figma-use` before `use_figma`, `figma-generate-library` for a library) and the
  `create_design_system_rules` prompt. `get_screenshot` is a look; a PNG on disk needs another tool
  in the session, else a named gap.

Common to both:

- **Figma saves by itself.** Nothing to ask; the check is a read-back of what was written.
- **Variants are a component set** with variant properties (`Variant`, `Size`, `State`), not
  separate components.
- **Foundations:** colours as variables in one collection with a `Light` and a `Dark` mode; radii,
  spacing and type sizes as number variables; type families as string variables or text styles.
  **A type scale kept as text styles counts as present** (one text style per size, with its
  family, size and line height): no number variables are proposed for it.
- **Variables are grouped with `/`:** a token `--gray-0` is the variable `gray/0`, `--space-4` is
  `space/4`; match names with `-` and `/` treated alike between a group and its step.
- **`figma_get_variables` caches:** pass `refreshCache: true` (Console), or read the variables in
  a read-only `figma_execute`, so a long session never compares against a stale copy.
- **A paint bound to a variable needs a visible fallback:** `setBoundVariableForPaint` keeps the
  paint's own colour as the fallback, and dashed strokes were drawn with it (black on black). Set
  the variable's resolved value first (`variable.resolveForConsumer(node).value`), then bind.
- **Annotations are read as the node property `annotations`**, in a read-only `figma_execute`.
  Not `figma_get_annotations`: in a live run it created the file's four preset annotation
  categories (`isPreset: true`), a write that read mode must not do.
- **A Figma file is a URL, so it usually belongs to a designer.** Unless the person created it in
  this run, anything is written only with permission (§6 gate 6); without it the foundations are
  proposals in the canon, and `screens` draws only on a page «Screens · <slug>» the person allowed
  (else `code` mode).
- No export tool in the session → name the missing PNGs as a gap in `screens.md` §Source; the node
  ids remain the source-ref.
- **The design ↔ code binding lives in the canon**, as in pen.dev: an inventory row carries both
  anchors and the «Design ↔ code props» cell (`Variant=Outline ↔ variant="outline"`), read from
  the code. `AGENTS.md` only points at the canon; code work follows `screens.md`.
- **Code Connect is a layer on top of that binding, not a replacement.** With components connected
  through Code Connect, the official Figma server puts each one into a node's context as a
  `<CodeConnectSnippet>` marker: the design properties, the import, a snippet and the
  instructions (instructions from Code Connect UI arrive as user rules; a UI mapping gives the
  component and its basic usage, a CLI mapping the full snippet). Requirements (developers.figma.com,
  checked 2026-11-10): the MCP integration on Professional, Organization, Government and
  Enterprise plans with a Full or Dev seat, and on Professional only the active library and
  framework are returned; Code Connect UI on a Dev or Full seat on Professional, Organization and
  Enterprise (its page does not mention Government), one active library and framework on
  Professional. When the session's server returns Code Connect for a component, `design-system`
  takes the props mapping from it and says so; without it the mapping is read from the code.
  Writing mappings: on Professional the MCP refused it in a live run (2026-10-25), the CLI
  (`npx figma connect publish`) published them.

## 9. Any other design tool

The same §6 steps, by capability: find the tool's target-document, read, write, save, look and
export tools; read its guide once; pass the target-document gate; write only what the rules allow.
The canon's `tool` is the product's lowercase name and `design_file` its path or URL. The tool has
nothing to write with → `design-keeper` only recognizes and reports (missing foundations become
proposals). No export → a named gap. No MCP for it in the session → `code` mode. The keeper's
report names the tools it used, and `design-system` records them in the canon so `screens` starts
from the same ones.

## 10. Code mode

Always available, needs no MCP. `screens.md` carries one ASCII wireframe per state that needs a
distinct layout. The manifest table is the same contract in every mode: `verify-ui` reads it, and
downstream code work is pointed at it (§1), never at the design file.
