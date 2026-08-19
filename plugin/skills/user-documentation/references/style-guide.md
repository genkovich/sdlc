# Style guide — the reference flow-document dialect

> Codified from the Beer-LMS user-documentation corpus (19 flow docs + index). This file is the
> single source of style truth for `doc-flow` agents and the index builder. When in doubt, the
> rule here wins over taste.

## File & document frame

- Filename: `Flow - <Title Case Name>.md` (spaces kept, `&` allowed). The index is
  `<Product> - User Guide.md`.
- **H1 equals the file basename** (without `.md`), first line of the file.
- **No frontmatter.** These are user-facing docs, not vault records.
- Language: **English**, second person ("you"), present tense ("A dialog opens", not
  "A dialog will be opened").
- Lead paragraph directly under H1: one or two sentences, pattern
  `This guide explains how to <goal> in <Product>.` — plus the role restriction when one exists:
  `Only users with the **Mentor** role can create sessions.`
- `---` horizontal rule between **every** pair of top-level (`##`) sections.

## Body — type A (`doc_type: task-flow`)

- Sections `## Step N: <Imperative Phrase>` — numbered from 1, no gaps
  (`## Step 2: Click "Create session"`).
- Each step: 1–2 short paragraphs. What to do, where the control is, what happens next.
- **One interactive control the user must operate = one step.** A dropdown/select with options
  gets its own step, an open-state screenshot (`06-type-dropdown-open.png`) and the options
  enumerated as bullets; the same for pickers and multi-field groups (Date + Time may share
  one step). Collapsing the whole form into a single "fill everything" step is the main way
  generated docs drift from the reference density.
- UI element names bold-quoted exactly as rendered: click **"Create session"**; field names
  bold without quotes when referred to generically (the **Title** field).
- Toasts and other transient UI text in italic quotes: _"Session created"_.
- URLs and paths in backticks: `/mentorship`, `https://meet.google.com/abc-defg-hij`.
- Field/option enumerations as bullet lists: `- **Title** (required) — The name of the session`.
- The screenshot goes at the **end of the step** it illustrates. Optional caption: one italic
  line directly under the embed (`_The Mentorship sessions list showing status badges._`).

## Body — type B (`doc_type: state-reference`)

For flows whose value is "what states exist and what you see in each" (badge on/off, status
matrix), use condition-scoped H3 blocks instead of a strict step chain:

```md
### State 1: Member WITH Mentor Badge

When a user is a mentor, you will see:
- A **"Mentor"** badge next to their name
- A **"Remove Mentor"** button to the right
```

- `### State N: <Condition>` headings, numbered from 1, each with a bullet list of observable
  facts (button text / icon / what the action does) and its own screenshot.
- A type-B doc may still open with 1–2 `## Step N:` sections for navigation ("get to the
  Members list"), then the state blocks.

## Screenshots

- Location: `screenshots/<slug>/NN-<state-name>.png`, relative to the target directory.
- Name pattern `^\d{2}-[a-z0-9-]+\.png$`; `NN` zero-padded, monotonically increasing in the
  order the doc embeds them.
- The name describes the **state pictured**, never the action: `06-type-dropdown-open.png`,
  not `06-clicking-dropdown.png`.
- Two legitimate shapes: full-viewport shot published at **exactly 780px** wide, or a tight
  element crop (any width below 780). Nothing wider than 780 ever ships.
- Budget: 1–10 screenshots per document; the corpus median is ~4. If a flow wants more than
  10, the flow is too big — split it.

## Embed syntax (target-dependent)

| Target | Embed | Doc link |
|--------|-------|----------|
| Obsidian vault | `![[screenshots/<slug>/01-x.png]]` | `[[Flow - Other Flow]]` |
| Repo `docs/` | `![](screenshots/<slug>/01-x.png)` | `[Flow - Other Flow](<Flow - Other Flow.md>)` |

One document uses ONE syntax throughout; the mode comes from the flows manifest
(`embed_syntax`), never from per-case judgment.

## Callouts

- `> **Note:** <text>` — plain blockquote with bold label. **Never** the Obsidian
  `> [!note]` form: these docs must render on GitHub and in any Markdown viewer.

## Tail sections (only the applicable ones — an empty table is a defect)

Order after the last step; each still separated by `---`:

| Section | Shape |
|---------|-------|
| `## Prerequisites` | bullet list of role/data preconditions (may open the doc instead when critical) |
| `## Troubleshooting` | table `\| Problem \| Solution \|` |
| `## Permissions Summary` | table: action rows × role columns, values Yes / No / qualified (`Yes (own)`) |
| `## Status Reference` | table: status / badge colour / meaning / allowed transitions |
| `## Error Handling` | table or bullets: error state → what the user sees → what to do |
| `## Related Flows` | bullet list of links to other flow docs |
| `## Notes` | short free-form bullets that fit nowhere else |

Every cell must come from an observed state or journal line. If nothing was observed for a
section — omit the section.

## The index (`<Product> - User Guide.md`)

Thin v1 contract:

- H1 = basename; optional `> Platform: <url>` / `> Last updated: YYYY-MM-DD` blockquote lines.
- Numbered `## N. <Area>` sections, one short paragraph each — built from the H1 + lead of
  every flow doc, grouped by product area. No own screenshots in v1.
- Final section `## Key User Flows`: every generated flow doc **linked** with a one-line
  description (`[[Flow - Create Mentorship Session]] — create a new mentorship session`).
  An unlinked flow doc is a validator error.
