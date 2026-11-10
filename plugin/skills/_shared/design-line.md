# Design line — order, file layout, input ladder, and design-tool rules

> **Reference-only.** Not a skill. The design-line skills (`design-system`, `ux-flows`,
> `prepare-design-spec`, `screens`), the `pen-keeper` agent and `verify-ui` read this file for
> where their artifacts live, where a feature's intent comes from when there is no PRD yet, and the
> hard rules for drawing in pen.dev (Pencil MCP), Figma, or plain markdown. Each skill keeps a
> one-line pointer and its own delta; the rules live **only** here.

## TL;DR (короткий вступ українською)

Дизайн-лінія = пʼять кроків, які повторюються на кожній UI-фічі:

```text
/sdlc:design-system (раз на репо) → /sdlc:ux-flows <slug> → /sdlc:prepare-design-spec <slug>
  → /sdlc:screens <slug> → код екранів → /sdlc:verify-ui <slug>
```

- **Без PRD теж працює.** Нема `PRD.md` → вхід = коротка історія користувача на 3-5 речень
  (`docs/features/<slug>/story.md` або прямо в команді). Гілки помилок беремо з питання «що може
  піти не так», а стани без джерела в AC позначаємо як виведені з історії. Є PRD і SAD (модуль 6+)
  → поведінка повна. Деградація, не відмова.
- **Канон дизайну репо-рівня** лежить у `docs/design/`, усе фічеве лежить у `docs/features/<slug>/`.
- **pen.dev:** `.pen` руками не правимо; перед записом перевіряємо активний документ; після
  змін Cmd+S; перед `git checkout` зберегти й закрити; PNG кожного стану експортуємо і
  перевіряємо `test -s`, бо експорт може тихо не створити файл або лишити його порожнім.
- **code-mode доступний завжди**: нема MCP → markdown-вайрфрейми і названа деградація.

---

## 1. The line and where it plugs into the backbone

| Step | Skill | Runs | Reads | Writes |
|---|---|---|---|---|
| 1 | `design-system` | once per repo (refresh when the foundation changes) | the code's tokens + components; `docs/architecture-map.md` if present | `docs/design/design-system.md` (+ `pen_file` on pencil) |
| 2 | `ux-flows` | per UI feature | the input ladder (§3) + the canon | `docs/features/<slug>/ux-flows.md` (+ `story.md` when the story came inline) |
| 3 | `prepare-design-spec` | per UI feature | the input ladder + `ux-flows.md` + the canon + the repo | `docs/features/<slug>/design-spec.md` |
| 4 | `screens` | per UI feature | `ux-flows.md` + `design-spec.md` + the canon (+ `sad.md` §6, contracts when present) | `docs/features/<slug>/screens.md` + `docs/features/<slug>/screens/*.png` |
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
docs/design/<name>.pen                           # pencil only: the one design document (components + screens)
docs/features/<slug>/story.md                    # the short user story (when there is no PRD)
docs/features/<slug>/ux-flows.md                 # flows + screen inventory (SCR-NN) + coverage
docs/features/<slug>/design-spec.md              # spec (BR-NN) + embedded Definition of Done (DOD-NN)
docs/features/<slug>/screens.md                  # manifest: screens × states × components
docs/features/<slug>/screens/SCR-NN-<state>.png  # pencil/figma only: one PNG per state
docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md   # live browser verdict
docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/     # its screenshots
```

Repo-level canon goes under `docs/design/`; everything feature-specific goes under
`docs/features/<slug>/`, like every other SDLC artifact. Never invent a third location.

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

**Degrade, don't refuse.** Sources 2–5 are **story mode**: there are no `AC-NN` ids, so the skills
number what they find and keep its origin visible.

### Provenance tokens (every derived branch, state and requirement carries one)

| Token | Meaning | Where it comes from |
|---|---|---|
| `AC-NN` | PRD acceptance criterion | `PRD.md` §5 |
| `BR-NN` | design-spec requirement | `design-spec.md` §6 |
| `S-N` | sentence N of the story | `story.md` / inline story |
| `W-NN` | «what can go wrong» item the user confirmed | the §4 question below |
| `§6:<flow>` / `contract:<status>` | SAD runtime branch / API error response | `sad.md` §6, `contracts/` (backbone only) |
| `D-NN` (`derived`) | inferred by the agent from the story, **not** confirmed by anyone | headless runs, `easy` defaults |

A state or branch with no `AC`/`BR`/`§6`/`contract` source is marked as coming from the story
(`S-N`, `W-NN`) or as derived (`D-NN`, so flows and tables can point at it). Derived items are
listed in the artifact's `## Assumptions` section so a human can veto them; they never silently
become requirements. When a user later confirms a `D-NN`, it is renumbered as the next `W-NN`.

### State vocabulary — one list for `design-spec.md` §8, `screens.md` and `verify-ui`

The six classes below are **checked for every screen**: each gets a row, either a real state or one
`N/A: <reason>` row. On top of them a screen may have **named states** that come from flow
branches (see the list under the table). The same id names the row in `design-spec.md` §8, the row
in `screens.md`, the pen.dev frame (`<slug> · SCR-NN · <state>`), the PNG (`SCR-NN-<state>.png`)
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

  Every named state carries its source token (`W-NN`, `D-NN`, `AC-NN`, `BR-NN`, `S-N` …) and gets
  its own frame, PNG and verdict row under the same id. A bare name never reuses a class name.
- **Hover / focus / disabled are component states**, not screen states. They come from the
  components in `docs/design/design-system.md` («States it supports») and get no screen frame.
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
  rate-limited action). The free-text «Other» answer adds more.
- Each chosen item becomes `W-NN` (Confirmed by the user) and gets a branch in a flow.
- At `hard` depth in full mode (PRD present) the same question runs once for failures the ACs
  missed; any `W-NN` there is also flagged as a PRD gap for `/sdlc:clarify-prd`.

## 5. Runs with no one to ask (headless, `claude -p`, CI)

If the session has no question channel (`AskUserQuestion` unavailable, denied, or the run is
non-interactive), the skill **does not stop and does not invent answers silently**: it takes the
`easy` path — decides with defaults, marks every such decision as `derived` and every inferred
failure as `D-NN`, writes them into the artifact's `## Assumptions` section, and says
«no question channel — N assumptions recorded» in the handoff.

## 6. Tool modes — `pencil` / `figma` / `code`

The tool is chosen **once** in `docs/design/design-system.md` frontmatter `tool:`; no feature skill
re-asks it. Never store the choice in `.claude/sdlc.local.md` (per-developer, gitignored).

| Mode | Screens live in | Per-state source-ref | PNG per state |
|---|---|---|---|
| `pencil` | the canon's `pen_file` (one document holds the components and the screens) | node id | required (§7 export gate) |
| `figma` | the canon's `figma_file` | node id | required when the Figma MCP can export; else named gap |
| `code` | inline markdown wireframes in `screens.md` | «wireframe below» | none — the built screen + the `verify-ui` screenshot are the visual evidence |

**Degrade, don't block.** The chosen tool's MCP is not connected in this session → run `code`
mode and write the degradation into `screens.md` §Source and the handoff («pencil MCP unavailable —
code-mode wireframes»). Detect the tools by probing what the session actually has; the Pencil
tools are `get_app_state`, `execute`, `read_skill`, `get_style`, `browser` (prefixed per the
session, e.g. `mcp__pencil__execute`).

## 7. pen.dev (Pencil MCP) — hard rules

1. **Never edit `.pen` JSON by hand.** The file is JSON on disk, but it is changed only through the
   pen.dev app, its MCP, or its CLI: no `Read`/`Edit`/`Write`, no `sed`, no `python`, no
   `json.dumps` on a `.pen`. Copying a whole file (`cp kit.pen docs/design/app.pen`) is fine.
2. **Active-document gate before every write.** The MCP ignores file paths and writes into
   whatever document is active in the app. Call `get_app_state` first; continue only when the
   active document is the canon's `pen_file`. Anything else (another file, no file, app closed) →
   STOP and ask the user to open `pen_file` in pen.dev; never write into a foreign document,
   never create probe nodes.
3. **Persist = the user's Cmd+S.** MCP edits live in the app's memory. After drawing, ask for
   Cmd+S, then confirm the file on disk changed (`stat -f '%m %z' <pen_file>` before/after on macOS,
   `stat -c '%Y %s'` on Linux). An unsaved `.pen` is named in the handoff, never committed.
4. **Before `git checkout` / `pull` / `rebase`: save and close the `.pen`.** An open document
   survives the branch switch in memory and the next Cmd+S writes the old branch's design over
   the new one.
5. **Conflicts are resolved in the app.** Keep both versions, open one as the base, re-apply the
   other's changes in pen.dev. Never merge `.pen` JSON by hand.
6. **One app version per team.** A newer pen.dev rewrites the file format on save; keep a copy of
   the file before opening it in a different version.
7. **No transitions between frames.** pen.dev has no prototyping links. A flow on the canvas =
   static frames placed left to right in flow order. A clickable flow lives in code (a `browser`
   node can show `localhost` next to the frames).
8. **Export gate.** Inside `execute`: `Export([nodeId1, nodeId2, …], "png", "<absolute dir>")`
   writes one file per node, named by the node id: `<dir>/<nodeId>.png`. An export can fail
   without a failing status, leaving no file or an empty one, so for **every** node:
   `test -s <dir>/<nodeId>.png` → `mv` to `SCR-NN-<state>.png` → `test -s` again (`-s` = exists
   and is not empty). A failed check fails the gate; the screen is not done.
9. **Variable sync overwrites.** Syncing variables from CSS overwrites same-named variables in the
   document (a dark-theme colour was lost this way); keep a copy of `pen_file` before a sync.
10. **The PNGs are the review surface.** A real `.pen` is megabytes of JSON with random ids; nobody
    reviews its diff in a PR. Put the exported PNGs in the PR instead.
11. **One component library per document.** A document that already has reusable components (a
    course kit, a teammate's file) already has its library, whatever its frame is called
    («Components · Chat»): it is recognized, never duplicated. «DS · Foundations» is created only
    in a document with no reusable components at all, and only there does `pen-keeper` draw
    primitives. In a document with a library, a component that exists only in code (`code-only`
    in the canon) is drawn by `screens` the first time a screen needs it. The procedure lives in
    `pen-keeper`; the canon records the frame as `library_frame`.

## 8. Figma (optional, when the team has a designer)

The canon's `figma_file` is the file URL; screens record a node id per state. Writing outside your
drafts needs a Full seat; the Figma MCP's write tools are beta. Without an export-capable Figma
tool in the session, name the missing PNGs as a gap in `screens.md` §Source — the node ids remain
the source-ref.

## 9. Code mode

Always available, needs no MCP. `screens.md` carries one ASCII wireframe per state that needs a
distinct layout. The manifest table is the same contract in every mode: `verify-ui` reads it, and
downstream code work is pointed at it (§1), never at the design file.
