# Read mode — the designer already drew the screens

> **Reference-only.** `screens` reads this when the screens exist in the design document and the
> job is to read them, not to draw them («розбери екрани дизайнера», `--from <url>`). The output
> is the same `screens.md` as in draw mode, so `verify-ui` and the code work downstream do not
> change. Tool-agnostic per `_shared/design-line.md` §6; Figma is the main case, pen.dev or any
> other tool works the same where the frames already exist.

## 1. Input and the one rule

- **When:** only when asked for (`--from <url>`, «розбери екрани дизайнера», «screens from the
  designer's frames», «екрани вже в документі»), or when the person picks «Розібрати ці фрейми»
  in the one question `screens` step 4a asks when the file already holds frames of this feature
  it did not draw. Without either, `screens` draws, with no extra question.
- **Where the frames are:** a link with a node (Figma: `https://www.figma.com/design/<fileKey>/…?node-id=<id>`,
  a page, a section or one frame; `node-id=12-34` in a URL is node `12:34` in the API), or
  «the screens are already in the document» (then every top-level frame whose name points at
  this feature: the slug, a screen name from `ux-flows.md`, `SCR-NN`).
- **Nothing is written into the design file.** No frame, no rename, no fix, no comment. So no
  write permission is needed and the canon's permission lines are not read. A drawing of missing
  states happens only in §5, and only after the person says yes.
- **The target is checked for reading.** The link's file key (or the open document) is the
  canon's design file → components map by node id / component key. Another file (a designer's
  working file) → allowed, read only; components then map by component key, else by name, and
  §Source says which file was read.
- **No MCP for the tool in this session** → read mode cannot run: STOP and say what to connect
  (Figma Console with Desktop Bridge in the file, or the official Figma MCP); never guess frames
  from a screenshot. **No canon** → read mode still runs; every component is then «not in the
  canon» and the handoff recommends `/sdlc:design-system`.
- **Read through the tool's read tools only** (design-line §6 «Capabilities»): Figma Console:
  `figma_get_status` / `figma_list_open_files` (the file must have Desktop Bridge running for
  runtime reads), `figma_execute` with read-only plugin-API code (annotations, a node's
  `reactions` and the page's `flowStartingPoints` too, §4),
  `figma_capture_screenshot`, `figma_get_variables` with `refreshCache: true` (in a long session
  it returns a stale cache otherwise); the official Figma MCP: `get_metadata`, `get_design_context`,
  `get_screenshot`, `get_code_connect_map`; pen.dev: a read-only `execute`. Property names come
  from the tool's guide or from an existing node, never from a probe node. **Not**
  `figma_get_annotations`: in a live run it created the file's four preset annotation categories
  (`isPreset: true`), a write.

## 2. Frames → screens and states

1. List every frame under the given node: name, node id, size, and its tree (instances with their
   main component, text, hidden layers).
2. Map each frame to a screen and to a state (the six classes and the named states of
   `_shared/design-line.md` §3), by its name («Chat · Error», «SCR-02 empty»), by what it shows
   (an `EmptyState` instance → `empty`, a disabled Send with an inline message → `validation`)
   and by the branches landing on the screen. The screens come from the first source that exists:
   `ux-flows.md` (`SCR-NN`), the story, the design spec, else **the frames themselves**.
   **No flows, no story, no spec is a full read, not a degraded one** (a Figma lesson has no
   flows): number the screens `SCR-NN` from the frames' names, the labels of the rows or
   sections on the page and how the frames are grouped; frontmatter `input: frames`; no question
   asking for 3–5 sentences. A state that only a frame name gives (`ended`, `empty-no-topic`) is a
   named state with the source `frame:<node id>`, not a `D-NN`. Stop only when the link holds no
   frames at all.
3. **Ambiguous frames are asked about in one batch**: one `AskUserQuestion` (up to 4 questions,
   one per frame, each frame's name and a one-line description of what it shows, the options =
   the likely screen · state pairs, the most likely first as «(Recommended)», + «Other»). More
   than 4 → a second batch. Headless → pick the most likely pair, record it under
   `## Assumptions` with the reason.
4. A frame that maps to no screen of this feature (another feature, a moodboard, a component
   sheet) is listed in §Source as «not a screen of <slug>», never forced into a state. A
   top-level frame or section named `Flow · …` (a flow board, flow-boards.md) is skipped
   silently: it is a diagram, not a screen.
5. Two frames for the same screen · state (two versions) → one question which one is current
   (the one placed later / named «final» / «v2» first, «(Recommended)»); headless → that one,
   recorded under `## Assumptions`.
6. **Hidden layers in a designer's frame** (switched off, zero opacity) are not a state: never
   count a frame as `error` because a hidden error banner sits in it. List them under
   `## Assumptions` (frame, layer name); when a hidden layer looks like a state of its own (an
   error banner, an empty message), also add «is <layer> a separate state?» to §Ask the designer.
   Nothing is unhidden or deleted: read mode writes nothing.

## 3. Coverage — every class, every screen

For every screen, each of the six classes and each named state from the flow branches gets a row
with one of three statuses:

- **drawn** — the designer's frame: node id (+ PNG, §6);
- **N/A: <reason>** — the class does not apply (as in draw mode);
- **missing** — the flows or the canon's conventions imply it, no frame shows it. Source-ref:
  «missing — ask the designer».

The missing states go into `screens.md` §Ask the designer: one line each, what to draw and why
(the branch token: `W-01`, `D-02`, `AC-03`). Then one question (interactive): «Попросити
дизайнера (Recommended)» (only the list, nothing drawn; the designer's file stays theirs) /
«Домалювати відсутні стани на сторінці «Screens · <slug>»» → §5. Headless → only the list.

## 4. Components and behaviour

**Every instance → its main component → the canon's inventory row**, in this order:

1. by node id (the inventory row's node anchor) or component key (a library component in another
   file);
2. else by name (the main component's name, or its component set's name) — marked «matched by
   name» in the Components cell and listed under `## Assumptions`.

Then mark what is not a clean instance:

- **not from the library** — a detached instance or a hand-built block that looks like a
  component (a frame named «Button», a group with a rectangle and a label): the Components cell
  says «not from the library: <what it imitates>», and the row's note asks whether the real
  component should be used;
- **in the design, no code** — the main component maps to an inventory row marked `design-only`:
  it goes to §New components as «create in code once and add to the canon»;
- **in the design, not in the canon** — the main component has no inventory row at all: §New
  components «not in the canon: run `/sdlc:design-system` («Оновити»)».

**Behaviour: only what the tool really gives.** Pop-ups, transitions and animations are not in a
static frame. Read, where the session's tool has it:

- **annotations** on the frames and their nodes, read as the node property `annotations` in a
  read-only `figma_execute` (each has `label`, `labelMarkdown`, `properties`, `categoryId`; Figma
  plugin API). Do not call `figma_get_annotations` or the `figma.annotations` category methods:
  the Console tool created the file's preset categories in a live run, and the category API is
  not documented as write-free. Report a category by its `categoryId`; its name needs that API,
  so ask the person first and name the side effect, or leave the id;
- **prototype reactions** of the nodes (Figma: a node's `reactions`: the trigger, e.g. on click,
  and the action, e.g. open an overlay, navigate to a frame, with its transition and duration);
- on pen.dev and another tool: its notes or comments on nodes, when its read tools return them;
- **Code Connect instructions**, when the official Figma server put them into a node's context
  (`<CodeConnectSnippet>`; design-line §8). Which annotations the official server returns is not
  documented: use them if they come, promise nothing.

**Flows from the prototype.** Read the page's `flowStartingPoints` (each a flow, with its name)
and every state frame's `reactions` (trigger node, trigger, destination, transition) in a
read-only `figma_execute`; they give `screens.md` §Flows with the flows' names (each step's source
`frame:<node id>`) and §Behaviour rows (on tap → <target>, dissolve 150 ms), per
[`./flow-boards.md`](./flow-boards.md) §6. Read mode draws no board, and a `Flow · …` section is
a board, never a state.

Every finding goes into `screens.md` §Behaviour with its source; the code work then does not go
back to the design file for it. Nothing found for a screen → say so in §Behaviour and add «a note
on how <screen> behaves» to §Ask the designer.

## 5. Drawing the missing states (only after a yes)

Only after «Домалювати» in §3: draw the missing states with the draw mode of the `screens` skill
(step 4, all its gates), **on the page (or top-level frame) «Screens · <slug>»**, never next to
the designer's frames and never inside them. The design file needs write permission as in draw
mode (a repo file: yes; a URL: the canon's «Screens write permission», else the question of
`screens` step 1). Each drawn state's row says «drawn by the agent» in its Source-ref, so the
designer sees which frames are not theirs.

## 6. PNG per state

As in draw mode: every **drawn** state (designer's or agent's) gets a PNG at
`docs/features/<slug>/screens/SCR-NN-<state>.png` through the tool's export, one command per
call, `test -s` on the final path; no export capability → the named gap in §Source. Exporting
writes into the repo, not into the design file.

## 7. What `screens.md` records in read mode

- frontmatter `mode: read`;
- §Source: «Mode: read — frames drawn by the designer, read only», the file and node(s) read,
  every frame → screen · state (and the frames that are not screens of this feature);
- the state tables as in draw mode (Source-ref: the designer's node id + PNG, `N/A` or
  «missing — ask the designer»);
- §Flows from the prototype, or «no prototype in the file» (flow-boards.md §6);
- §Behaviour, §Ask the designer, §New components (with the «not from the library», «create in
  code», «not in the canon» rows), `## Assumptions` (name matches, picked pairs, picked versions).

## 8. Self-check in read mode (replaces items 5–7 of the skill's self-check)

(5) every state row is drawn (node id), `N/A` or «missing — ask the designer», and every missing
one is in §Ask the designer; (6) every drawn state's PNG passes `test -s` (one call per file), or
§Source names the no-export gap; (7) every instance in the read frames maps to an inventory row
(or is marked «matched by name», «not from the library», «design-only» or «not in the canon»),
§Behaviour has a line for every screen (findings or «nothing found»), and nothing was written
into the design file except, after a yes, on «Screens · <slug>».
