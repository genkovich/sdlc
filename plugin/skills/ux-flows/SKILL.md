---
name: ux-flows
model: inherit
effort: high
agents: []
description: >
  Use to derive how the user moves through a UI feature — mermaid flowcharts with the happy path
  and the error branches, a screen inventory (SCR-NN ids), and a coverage table — written to
  docs/features/{slug}/ux-flows.md. Works WITHOUT a PRD: from a 3–5 sentence user story (inline or
  docs/features/{slug}/story.md) it drafts the happy path, asks «what can go wrong» for the error
  branches, and marks branches with no acceptance-criterion source as derived from the story. With
  PRD.md present it runs in full mode: one flow per UI-touching user story, branches from the §5
  ACs. Both at once: text in the command next to a PRD (or another source) adds instructions —
  narrow to one story, add failures, screens or constraints — each marked N-NN, a contradiction
  with the PRD asked once and recorded as a PRD gap. Triggers on "ux flows for {slug}", "user flows for {slug}", "screen flow for {slug}",
  "/sdlc:ux-flows {slug}", "юзер-флоу для {slug}", "флоу екранів {slug}", "потік екранів {slug}",
  "намалюй флоу користувача", "що може піти не так". Always markdown + mermaid, whatever the design
  tool. Feeds prepare-design-spec and screens; architecture-design (target-surface evidence) and
  plan-tests (e2e-through-UI paths) get it named in their prompt. Skipped only for features with no
  human-facing UI.
triggers:
  - /sdlc:ux-flows
  - "ux flows for"
  - "user flows for"
  - "юзер-флоу для"
  - "флоу екранів"
  - "що може піти не так"
stage: "util"
---

# Skill: ux-flows (SDLC design line — step 2, per feature)

Draws **how the user moves** through a UI feature: one mermaid `flowchart` per user goal (happy
path + the error branches), the **screen inventory** (`SCR-NN` — the id contract `screens` details
next), and a coverage table that shows where every story sentence, failure or acceptance criterion
ended up. The artifact is **always markdown + mermaid**, whatever `docs/design/design-system.md`
picks as the drawing tool: flows are about movement between screens, not about their look.

**Two modes (plus extra instructions in the command), one skill — degrade, don't refuse.** The intent comes from the input ladder in
[`../_shared/design-line.md`](../_shared/design-line.md) §3:

- **Full mode** — `docs/features/<slug>/PRD.md` exists: one flow per UI-touching §4 user story,
  one branch per relevant §5 AC. Same coverage rules as `complete-sequence-diagrams`.
- **Story mode** — no PRD: the input is a short user story (`story.md`, `design-spec.md`,
  `idea-brief.md`, or inline). The happy path comes from the story's sentences (`S-N`); the error
  branches come from the «what can go wrong» question (`W-NN`); anything inferred without
  confirmation is derived (`D-NN`) and listed under `## Assumptions`.
- **A source plus text in the command** — either mode above, and the command also carries text
  (`/sdlc:ux-flows chat <text>` while `PRD.md` exists). The source stays the base; the text adds
  instructions the source does not have: narrow to one story, add failures, screens or
  constraints. Each item is `N-NN` (from the invocation) and gets its branch, screen or note and a
  coverage row, per [`../_shared/design-line.md`](../_shared/design-line.md) §3 «Text in the
  invocation». With no source at all, the text is the story (`S-N`).

Each diagram is confirmed **in prose, never as raw mermaid** →
[`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md); parse-validated per
[`../_shared/mermaid-check.md`](../_shared/mermaid-check.md); questions per
[`../_shared/ask-style.md`](../_shared/ask-style.md); confirm-vs-proceed per
[`../_shared/interview-depth.md`](../_shared/interview-depth.md).

## Owner

Whoever owns the user experience (PM, designer, or the solo developer). In full mode the PM confirms
each flow matches a real user story; the Tech Lead flags flows that imply architecture (they become
`architecture-design` input, not decisions here).

## Inputs

- `<slug>` — kebab-case feature slug.
- **The intent** — resolved by the input ladder ([`../_shared/design-line.md`](../_shared/design-line.md) §3):
  `PRD.md` → `design-spec.md` → `story.md` → `idea-brief.md` → inline story → ask for 3–5 sentences.
  Only a missing intent stops the skill; a missing PRD never does.
- (Optional) **text in the command next to a found source** — additional instructions, `N-NN`
  (design-line §3); never a replacement for the source.
- (Expected) `docs/design/design-system.md` — the platform posture. **Absent → not a block**: assume
  the posture the code suggests, and recommend `/sdlc:design-system` in the handoff.
- (Optional) `CONTEXT.md` — canonical role names for the actors.
- (Optional) `--depth=easy|medium|hard`, else `interview_depth` from `.claude/sdlc.local.md`, else
  `medium`. This skill does not open its own depth question.

## Protocol

1. **Resolve the intent + read.** Walk the input ladder and record the source used. Story given
   inline, no source 1–4 found and no `docs/features/<slug>/story.md` yet → write it verbatim from
   [`./templates/story.md`](./templates/story.md) to `docs/features/<slug>/story.md` first, so the
   next skills read the same words. Number the story's sentences `S-1`…`S-n`. Read
   `docs/design/design-system.md` (posture; note its absence) and `CONTEXT.md` if present. In full
   mode read PRD §1, §4 (which user stories touch a UI?) and §5.
   **Text in the command next to the source** → split it into items and number them `N-01`…:
   a narrowing (which story or goal), an added failure, an added screen, a constraint. A narrowing
   limits which stories get flows; the rest stay listed as out of scope by the command, not
   dropped. An item that contradicts the source (an AC, a story sentence) → one `AskUserQuestion`
   per [`../_shared/ask-style.md`](../_shared/ask-style.md): «Лишити як у джерелі (Recommended)» /
   «Зробити як у команді»; whatever is picked, record the decision under `## Assumptions` and, when the source is
   the PRD, add the contradiction to the handoff as a PRD gap for `/sdlc:clarify-prd`. No question
   channel → follow the source and record the contradiction the same way.

2. **Draft the happy path(s).** Full mode: one flow per UI-touching §4 user story (only the ones an
   `N-NN` narrowing keeps, when the command gave one); a backend-only
   story is listed as out of scope with one line, not drawn. Story mode: one flow per distinct user
   goal in the story (usually one). Name every screen the flow visits and give it an `SCR-NN` id.

3. **Ask «what can go wrong»** — story mode always; full mode at `hard`, and at any depth when the
   command text asks to think about failures (for failures the ACs missed). An added failure from
   the command is already `N-NN`: it is not offered again as an option. One `AskUserQuestion`,
   `multiSelect: true`, built per [`../_shared/design-line.md`](../_shared/design-line.md) §4: the
   drafted happy path in one sentence as context, up to 4 failures most likely **for this story**
   as options, «Other» for the rest; every step that calls the server gets its own failure
   candidate, and when they do not fit into 4 options a second question follows. Each picked item
   becomes `W-NN` (source: the user's answer) and gets a branch. In the
   same call, only if the canon is absent or the story implies a different platform, add a second
   question to confirm the posture. **No question channel** (headless / `claude -p`) → derive
   one failure per server-calling step plus the story's likely ones yourself as `D-NN`, and
   continue per §5 of the same file.

4. **Write + confirm each flow — prose, never raw mermaid.** Bootstrap
   [`./templates/ux-flows.md`](./templates/ux-flows.md) → `docs/features/<slug>/ux-flows.md` on the
   first flow (Read the template, Write the file; never `cp` from the plugin's folder); write each flow as soon as it is drafted. Validate it parses per
   [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md). When the real parser could not run
   (no `mmdc`, no permission for `npx`), say so in the handoff in one line and name what checked it
   instead («mermaid: `npx` not permitted — structural lint per mermaid-check.md»); never report a
   parse that did not run. Then describe it in plain words —
   the happy path and **every** branch. `medium`/`hard`: one `AskUserQuestion` per flow with the
   4-state actions («Прийняти» / «Виправити» / «Винести у відкрите питання» / «Викинути»); on
   «Виправити» regenerate that one flow (one round, second answer final). `easy` or no question
   channel: write + one-line summary into `## Assumptions` and proceed.
   On the canvas there are no transitions between screens: say in the prose that the drawing tool
   will show these screens as static frames left to right, and the clickable flow lives in code;
   `/sdlc:screens` also draws this flow as a board «Flow · <name>» from this mermaid (a diagram of
   the sequence, drawn arrows, still no transitions in pen.dev).

5. **Inventory + coverage.** Fill the screen inventory (`SCR-NN`, purpose, entry, exit, and which
   branches land on it — the states `screens` will draw). Fill the coverage table: one row per
   story sentence `S-N` and per `W-NN` (story mode) or per §5 AC (full mode), plus one row per
   `N-NN` item from the command in either mode, each pointing to the flow/branch/screen that shows
   it, or an explicit `N/A: <reason>`. Every row carries its provenance
   token per [`../_shared/design-line.md`](../_shared/design-line.md) §3. Stamp frontmatter
   `input:` (`prd` / `design-spec` / `story` / `idea-brief`) and `updated_at`.

6. **Structural self-check** — re-read the file **from disk** and verify **5 items** (count with
   Read / Grep, never a composed `$(…)` command):
   (1) every UI-touching §4 user story (full mode) or every story sentence (story mode) is shown by a
   flow or marked out of scope;
   (2) every SCR id used in a flow exists in the inventory, and every inventory row appears in ≥1 flow;
   (3) every §5 AC / every `W-NN` / every `N-NN` from the command appears in the coverage table with
   a flow/branch/screen or an explicit N/A, and every contradiction with the source is recorded
   under `## Assumptions` (and, with a PRD source, in the handoff as a PRD gap);
   (4) every mermaid block parses (by the parser, or by the fallback the handoff names);
   (5) every branch and coverage row has a provenance token, and every `D-NN` / `derived` item is
   listed under `## Assumptions`.
   Fix and re-check at most 2 cycles; surface anything unresolved — never silently.

7. **Propose the commit + handoff.** Propose `ux-flows: <slug> ux-flows.md` (with `story.md` when
   this run created it). Unresolved self-check item → no commit, say why. Then emit the
   **stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — *What I did*
   (mode + input source + «and N items from the command» when there were some, N flows, N screens,
   N `W` / N `D` / N `N` items, the PRD gaps for `/sdlc:clarify-prd`, N assumptions,
   «self-check: 5/5 pass», how the mermaid was checked (the parser, or the named fallback), the
   proposed commit; + «`docs/design/design-system.md` absent — run
   `/sdlc:design-system`» when it was) + *Review* (`docs/features/<slug>/ux-flows.md`) + *Run next*:
   `/clear`, then `/sdlc:prepare-design-spec <slug>`; in full mode with no `sad.md` yet,
   `↳ or /sdlc:architecture-design <slug>` with `docs/features/<slug>/ux-flows.md` named in the
   prompt as target-surface evidence (it does not read the file on its own yet).

## Definition of Done

- `docs/features/<slug>/ux-flows.md` exists: platform decisions, the `SCR-NN` inventory, one flow per
  UI-touching user story / story goal (happy path + error branches), the coverage table.
- Story mode: the error branches came from the «what can go wrong» answer (`W-NN`) or are visibly
  derived (`D-NN`) and listed under `## Assumptions`; nothing pretends to be an acceptance criterion.
- Full mode: zero silently uncovered UI ACs.
- Text in the command next to a source: every item is an `N-NN` with its branch, screen or note and
  a coverage row; the source was not replaced; every contradiction was asked (or, headless,
  followed the source), recorded under `## Assumptions` and, with a PRD source, handed off as a
  PRD gap.
- Every flow was confirmed in prose (or written + summarized at `easy` / headless); every mermaid
  block parses.
- No visual design leaked in: no component names, no layout, no styling — that is `screens`.

## Anti-patterns

- **Refusing because there is no PRD.** A 3–5 sentence story is enough input; degrade to story mode.
- **Happy path only.** The point of this step is the branches the story does not mention; ask
  «what can go wrong» before drawing the screens.
- **Disguising guesses as requirements.** A branch the user never confirmed is `D-NN`, not `W-NN`
  and never `AC-NN`.
- **Drawing screens here.** Components, states and layout belong to `screens`.
- **Deciding architecture here.** «SPA vs SSR», «needs a websocket» — flag it for
  `architecture-design`.
- **Raw mermaid as the confirmation prompt** — the anti-pattern
  [`diagram-presentation.md`](../_shared/diagram-presentation.md) exists to kill.
- **Promising transitions in the design tool.** pen.dev has no links between frames; the clickable
  flow is the code. The arrows on a `screens` flow board are a drawn diagram, not transitions.
- **Dropping the command text because a PRD exists.** The PRD is the base, the text adds to it;
  ignoring it loses exactly what the person just asked for.
- **Letting the command text overrule the PRD silently.** A contradiction is one question and a PRD
  gap, never a quiet rewrite of an AC.

## References & templates

- [`./templates/ux-flows.md`](./templates/ux-flows.md) — output scaffold; inline comments are the
  generation contract.
- [`./templates/story.md`](./templates/story.md) — the short user story, written when it came inline.
- [`../_shared/design-line.md`](../_shared/design-line.md) — input ladder, provenance tokens, the
  «what can go wrong» question, headless rule, file layout.
- [`../_shared/diagram-presentation.md`](../_shared/diagram-presentation.md) ·
  [`../_shared/mermaid-check.md`](../_shared/mermaid-check.md) — confirm-in-prose + parse-validation.

## Example invocation

```text
/sdlc:ux-flows chat Як користувач Threads Premium, після взаємного метчу я хочу
одразу написати людині в застосунку, а не переходити в Threads. Чат відкривається з вікна метчу.
Я бачу, що моє повідомлення доставлене, і бачу відповідь без перезавантаження сторінки.
```

Story mode (no PRD): the text is the story. Expected outputs: `docs/features/chat/story.md`,
`docs/features/chat/ux-flows.md`.

```text
/sdlc:ux-flows chat лише історія про перше повідомлення після метчу; подумай, що буде, коли
мережа зникне посеред відправки, і додай екран, де видно, що людина вже прочитала
```

Full mode with `docs/features/chat/PRD.md` present: the PRD is the base (its US and ACs give the
flows and branches); the text adds `N-01` (narrow to the first-message story; the other stories
are listed as out of scope by the command), `N-02` (a send failure on a lost network, which also
triggers the «what can go wrong» question at any depth) and `N-03` (a «read» screen the PRD does
not have). Each `N-NN` gets a coverage row; if `N-03` contradicts an AC (say, the PRD forbids read
receipts), one question decides and the contradiction goes to the handoff as a PRD gap for
`/sdlc:clarify-prd`. Expected output: `docs/features/chat/ux-flows.md` (no `story.md`).
