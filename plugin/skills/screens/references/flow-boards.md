# Flow boards — the flows as a sequence on the canvas

> **Reference-only.** `screens` reads this in draw mode, step 4f, **the last drawing step**: after
> the state grid is drawn, every PNG is exported and the states have passed the self-check (a state
> the self-check adds is drawn and exported first, so it is on its board): each flow of `ux-flows.md` gets one board «Flow · <flow name>» that
> shows the flow as a sequence of the real states. The mermaid flow in `ux-flows.md` stays the
> source; the board is its render. Read mode never draws a board (§6).

## 1. What a board is

- One **top-level frame** (Figma: a **section**) named exactly `Flow · <flow name>`: the flow's
  heading in `ux-flows.md` **without its provenance tokens** («Flow: написати Анні просто з
  вікна метчу (S-1…S-3)» → `Flow · написати Анні просто з вікна метчу`). It is placed next to the
  state grid (to its right); in page mode on the «Screens · <slug>» page.
- A title (`Flow · <flow name>`) and one legend line: solid grey = the happy path, dashed grey = a
  branch, dashed red = an error.
- **No new question** in draw mode, headless too: a board is drawn for every flow, as part of the
  run.
- **Never a frame of the feature.** Boards are not states: `screens` step 4a («frames of this
  feature already there?») and read mode skip every top-level frame or section whose name starts
  with `Flow · ` and every board node id recorded in `screens.md` §Flows. A rerun of `screens` on
  the same document asks nothing new because of them. Layers inside a board are named `Step · …`,
  `Arrow · …`, `Label · …`, `Snapshot`, `Caption`, never with a state frame's name pattern.
- **Never a library component either** (both skills, every tool): a state frame
  `<slug> · SCR-NN · <state>` and a `Flow · …` board are never reusable components and never
  inventory rows, even when someone has made one reusable. `design-keeper` and `design-system`
  leave them out of the library and the inventory; `screens` never instances them.
- **Everything on the document's variables** (the project's names for foreground, muted
  foreground, destructive, border and background, e.g. `$muted-foreground`, `$destructive`,
  `$border-strong`, `$background`, plus the type and spacing variables). The thumbnails are the
  only fills that are pictures.

## 2. From mermaid to the board

Read each ```mermaid flowchart in `ux-flows.md` in order:

| Mermaid | On the board |
|---|---|
| a node with an `SCR-NN` id (`A[SCR-01 screen]`) | a **screen node**: the thumbnail of the state the node or its incoming branch names (`SCR-02 error` → the `error` state; a branch token `W-02` → the state of that token in the screen's table; else `default`), with two caption lines above it: `SCR-NN · <state>` and the node's own short label |
| a decision `B{…}` | **no node**: its condition goes into the trigger label of each edge that leaves it («надсилає, збій мережі (D-02)»), and those edges start from the screen before the decision |
| any other node (a start, an end, a screen outside the feature: `([…])`, `(…)`) | a **terminal pill**: grey border, muted text |
| an edge `-->|label|` | an **arrow** with its label: the trigger, its condition when it came from a decision, and its token (««написати», назва треду невідома (D-01)») |

**Three edge styles:**

- **solid grey** — the happy path (`S-N`, `AC-NN` of the main story);
- **dashed grey** — a branch that is not a failure (later, a choice, «back», an empty case);
- **dashed red** (destructive) — an error (`W-NN` / `D-NN` of a failure, `contract:4xx/5xx`, a
  retry from an error). A screen node whose state is `error`, `error-*` or `ended` gets a red
  border and a red caption.

**A screen node with no drawn state** (its state row is `N/A` or «missing») is a **dashed card
«немає кадру»** (in the project's language) with the same two captions, never an empty or a
made-up thumbnail.

**Layout** (the rehearsal's generator works like this):

- **columns** = the order of the steps, left to right; **rows** = the happy path in the middle
  row, branches and errors in rows above and below it;
- an edge leaves and enters a node at an **offset along the node's side**, so two edges between
  the same pair of nodes (the forward edge and a «retry» back) never share a line; a back edge to
  the same column goes as an **elbow** around the node;
- a label sits on its edge (about the middle, moved along it when two labels would meet), in a
  small frame filled with the background so the line does not run through the words;
- **one bus for the same edge from many nodes**: several edges with the same target and the same
  label from different nodes (a «назад (D-06)» from every state of the conversation) are drawn as
  one shared line that collects them, with one label («назад з кожного стану (D-06)») and one
  arrowhead at the target, so they never cross each other or a red edge;
- thumbnails at about 0.4 of the state frame (156 × 338 for a 390 × 844 phone frame), the column
  gap wide enough for the longest label.

The thumbnails are the **exported PNGs of step 4e**, so the boards come after the export; a state
re-exported later means the board is redrawn. No export in the session → the screen node is a
card with its two captions and no thumbnail, and the board's own PNG is the same named gap in
§Source.

## 3. pen.dev

From the schema (`read_skill({ path: "pen-schema.md" })`; it has no line, arrow or connector type:
`Frame | Group | Rectangle | Ellipse | Path | Polygon | Text | Note | Icon | Script | Browser | Ref`):

- **The board** is a top-level frame with `layout: "none"`, nodes placed by `x` / `y`, the theme
  of the state frames (`theme`).
- **A thumbnail is a PNG image fill, nothing else**: a rectangle with `fill: { type: "image",
  url, mode: "contain" }`, the `url` relative to the `.pen` (`docs/design/app.pen` →
  `../features/<slug>/screens/SCR-02-empty.png`). Not a `ref` to the state frame: a `ref` does not
  scale (it stays 390 × 844), and making the state frames `reusable: true` for it would put them
  into the document's reusable components, where `design-keeper` and `screens` would count the
  screens as components.
- **An arrow** is a `path` whose SVG `geometry` draws the line **and** its arrowhead (a small
  triangle in the same geometry, filled). There is no marker and no dash property: a **dashed**
  arrow is a geometry of separate segments (`M … L … M … L …`).
- **An edge label** is a `text` inside a small frame filled with `$background`, placed on the
  edge.
- **Look by screenshot, not by `ctx.problems`**: on a `layout: "none"` board it reports false
  «partially / fully clipped» problems. `TakeScreenshot` the board, check that every node, arrow
  and label is visible and nothing overlaps; fix once and look again.
- **Edges are not bound to nodes**, so a board is never patched: when it has to change, it is
  **redrawn whole** — delete the old board (the node id from `screens.md` §Flows **and** the exact
  name `Flow · <flow name>` both match; nothing else, no name pattern) and draw it again. Whether
  it has to change is decided by its input fingerprint (§5).

## 4. Figma

**The board** is a section «Flow · <flow name>» with the same nodes, arrows, labels and styles.

- **Thumbnails are snapshots of the state frames**: `exportAsync` of the frame → an image →
  the image fill of a `Snapshot` rectangle; under it a `Caption` «<frame name> · <node id> ·
  знімок <YYYY-MM-DD>» linking to the real frame. **Never a copy of a state frame**: a copy is a
  second live set of states with instances and reactions, and read mode would then see twin
  states and twin reactions. A snapshot does not update by itself: the date on the caption says
  when it was taken, and a rerun takes it again.
- **Real prototype connections** between the state frames, written with the plugin API
  (`setReactionsAsync`) and read back: **On tap → Navigate to**, **Dissolve 150 ms** (or the
  canon's motion convention), the trigger on the **real element** the mermaid edge names (the
  button, the row, the «Назад» in the top bar; a layer nested in an instance works).
- **A flow starting point** per flow, named after the flow, on the flow's first state frame (the
  page's `flowStartingPoints`).
- **What Prototype cannot do stays on the board only:** a branch by condition (a send that fails,
  a conversation that was closed) has no tap that causes it. Do not imitate it with a delay or a
  hidden hotspot; never invent a trigger. A target with no frame (the dashed «немає кадру» card)
  gets no reaction.

Only where the run may write (design-line §6 gate 6): a repo file, a file the person created in
this run, or page mode («Screens · <slug>»). A designer's file without permission gets nothing,
as today. The handoff lists every connection made and every edge that stayed board-only.

## 5. `screens.md` §Flows

One row per flow:

| Flow | Board node id | Nodes → states | Input fingerprint | PNG |
|---|---|---|---|---|
| `Flow · <name>` | `<id>` | `SCR-01 · default` → `SCR-02 · empty` → `SCR-02 · success`; error `SCR-02 · error`; `SCR-02 · ended (немає кадру)` | `ux-flows <hash12>` · `png <hash12> …` | `screens/flow-01.png` |

**The input fingerprint** says what the board was drawn from: the git blob hash of `ux-flows.md`
(the file that holds the flow's mermaid) and of every state PNG on the board, the first 12
characters of each, taken with **one plain command per call**: `git hash-object <file> <file> …`
lists several files in one call (no pipe, no `$(…)`). It is a git command, a class the skill runs
anyway (`git status`, commits), so it brings no new permission prompt; it works on files not yet
committed. On a rerun, `screens` takes the fingerprint again:

- **the same** → the board is not touched; the handoff says «board up to date: Flow · <name>»;
- **different** (the flows changed, a state PNG was re-exported, a state was added or removed on
  this flow, a row has no fingerprint yet) → the board is redrawn whole (§3) and its row updated.

Figma adds the prototype: the flow starting point and every reaction (element → target), and the
edges that are board-only. Each board is exported to `docs/features/<slug>/screens/flow-NN.png`
(NN = the flow's order in `ux-flows.md`), one command per call, `test -s` on the final path, as
for the states.

## 6. Read mode

Read mode draws no board. It reads the designer's prototype in a read-only `figma_execute`: the
page's **`flowStartingPoints`** (each a flow, with its name and its first frame) and every
state frame's **`reactions`** (the trigger node, the trigger, the destination frame, the
transition). §Flows gets one row per flow starting point, its sequence followed along the
reactions, every step with the source `frame:<node id>`; when `ux-flows.md` has flows, every
difference is listed (a branch the prototype lacks, a link the flows lack). A `Flow · …` section
or frame in the designer's file is a board, never a state. No prototype → §Flows says «no
prototype in the file», and the flows stay as `ux-flows.md` has them. pen.dev has no prototype:
§Flows there comes from `ux-flows.md` only.

## 7. Self-check (the `screens` self-check item 8)

Draw mode: every flow of `ux-flows.md` has a board whose node id is in §Flows, with its input
fingerprint, drawn after the states passed their self-check (every state of the flow is on it); every screen node
on it shows the PNG (Figma: the snapshot) of a drawn state or the dashed «немає кадру» card; no
state frame or board became a library component or an inventory row; every board PNG passes
`test -s` (one call per file); every board was checked by a screenshot; Figma: every reaction
written was read back, and §Flows lists the board-only edges. Read mode: §Flows is read from the
prototype, or says «no prototype in the file».
