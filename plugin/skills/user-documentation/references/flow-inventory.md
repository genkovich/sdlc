# Flow inventory — how the list of flows is built, classified and frozen

> Protocol for step 4 of the skill. The output is the ONLY input the manifest builder uses;
> after the user confirms it, the list is frozen for the whole run.

## Three sources, merged

1. **`--flows a,b,c` (explicit).** If the user passed flows, they are the primary list — the
   other two sources only enrich metadata (start URLs, types), never add flows.
2. **Repo scan — dispatch `sdlc:explorer`** (fallback: the generic `Explore` agent) with a
   prompt naming the repo root and asking for: the route table (router config, page
   components), the navigation components (sidebar/menu items and where they lead), and any
   obvious CRUD surfaces. Explorer returns route → page-component pairs with `file:line`
   anchors; it does not decide what a "flow" is.
3. **Live snapshot.** The parent opens the app itself (`playwright-cli open` → `snapshot` on
   the landing page after auth) and reads the real navigation: menu items, dashboard cards,
   visible actions. The live app wins over the repo when they disagree (feature-flagged routes,
   dead code).

Merge rule: one candidate flow per **user goal**, not per route. "Create a session" is one
flow even though it touches three routes; "Settings" is several flows (members, roles,
danger zone) even though it is one route.

## Granularity heuristics

- A flow ≈ 5–15 journal actions and 1–10 screenshots. Bigger → split; a flow with 1 action
  and 1 screenshot → probably a step of a neighbour flow.
- Name flows by the goal in Title Case: `create-session` → `Flow - Create Mentorship Session`.
- Every product usually has: one `auth` flow, one dashboard/landing overview, one flow per
  primary CRUD object, plus reference docs for role/status matrices.

## Classification (per flow, before anything runs)

| Field | Values | Rule of thumb |
|-------|--------|---------------|
| `doc_type` | `task-flow` | "how do I do X" — a step chain with a beginning and an end |
| | `state-reference` | "what do the states look like" — badge on/off, status matrix, role views |
| | `auth` | the login flow; gets the OAuth special-case treatment |
| `mutates` | `true` | walking it creates/edits/deletes data (submits a form, toggles a flag) |
| | `false` | pure navigation and reading |

When unsure about `mutates` — mark `true`; the cost is serialization, the alternative is
corrupted parallel screenshots. Note that a `state-reference` flow becomes `mutates: true`
the moment the needed states must be created through the UI.

## Confirmation gate (AskUserQuestion)

Present the merged list as a table — slug, proposed title, `doc_type`, `mutates`, start URL,
one-line scope — and ask the user to confirm/trim. Multi-select which flows to run when the
list is long. Explain in the question what `mutates` implies (those run sequentially, they
will create `Docgen:`-prefixed records in the app's data).

**After confirmation the list is frozen**: no agent may add, split or merge flows mid-run.
A discovered gap goes into the final report as "candidate for the next run", not into this
run's manifest.
