---
feature: <slug>
status: Draft
owner: <name-or-role>
updated_at: <YYYY-MM-DD>
---

# Design spec: <feature name>

## 1. Raw request

> <Preserve the user's original one-to-three sentence request verbatim.>

## 2. Why now

- **Problem:** <what is difficult today>
- **User:** <who experiences it>
- **Trigger:** <why this iteration is being done now>
- **Success outcome:** <observable user or product outcome>

## 3. Evidence sources

| Status | Source | What it proves |
|---|---|---|
| Observed | `<repository path>` | <current route, behavior, component, token, or contract> |
| Confirmed | `<PRD, issue, or user answer>` | <product decision> |
| Proposed | `<proposal>` | <decision that still needs approval> |

## 4. Current user flow

1. **Start:** <current entry state>
2. **Action:** <what the user does>
3. **System response:** <loading/data/error behavior>
4. **Success:** <current outcome>
5. **Recovery:** <what happens on failure>

## 5. Target user flow

1. **Start:** <target entry state>
2. **Action:** <target actions>
3. **System response:** <target feedback>
4. **Success:** <target outcome>
5. **Recovery:** <target failure behavior>

## 6. Requirements

| ID | Status | Requirement | Source |
|---|---|---|---|
| BR-01 | Observed / Confirmed / Proposed | <observable requirement> | <evidence or decision> |

## 7. Routes and frames

| Surface | Route / frame | Required content and layout |
|---|---|---|
| Current | `<route>` | <what exists now> |
| Desktop | `<width x height>` | <composition> |
| Mobile | `<width x height>` | <composition> |

## 8. State inventory

| State | Trigger | Visible result | Recovery / next action |
|---|---|---|---|
| Empty | <trigger> | <result> | <action> |
| Loading | <trigger> | <result> | <action> |
| Ready | <trigger> | <result> | <action> |
| Success | <trigger> | <result> | <action> |
| Error | <trigger> | <result> | <action> |
| Disabled / focus / hover | <trigger> | <result> | <action> |

## 9. Reuse and handoff contract

| Design responsibility | Current code owner / token | Decision |
|---|---|---|
| <element or behavior> | `<path, component, or token>` | reuse / extend / new candidate |

## 10. Responsive and accessibility contract

- **Responsive:** <ordering, resizing, overflow, reachable actions>
- **Keyboard:** <tab order, activation, focus visibility>
- **Semantics:** <labels, headings, status/error announcements>
- **Contrast and motion:** <constraints>

## 11. Content and realistic data

- <exact labels, messages, and representative data needed in design specimens>

## 12. Non-goals and forbidden changes

- <behavior, route, API, schema, dependency, or product area that must not change>

## 13. Design references

- Current UI evidence: <screenshot or route>
- Approved frame URLs / node IDs: <fill after design>
- Repo-local design file: <fill when using Pencil or similar>

## 14. Open decisions

| Decision | Why it matters | Owner | Due | Status |
|---|---|---|---|---|
| <question> | <impact> | <role> | <date> | Proposed |

## 15. Spec-ready gate

- [ ] Current product behavior is backed by repository evidence.
- [ ] Product decisions are confirmed or visibly marked Proposed.
- [ ] Requirements have stable IDs.
- [ ] Desktop/mobile, states, reuse, accessibility, and non-goals are covered.
- [ ] No route, dependency, component, token, or API has been invented as fact.
- [ ] Every requirement maps to a DOD row in section 16 below.

---

# Definition of Done

Completion means every applicable row is checked with evidence. An agent report, generated image,
or visual impression is not evidence by itself.

## 16. Done checks

| ID | Covers | Layer | Pass condition | Evidence | Done |
|---|---|---|---|---|---|
| DOD-01 | BR-<id> | Specification | The approved scope, sources, and non-goals are explicit. | Sections 1–14 review | [ ] |
| DOD-02 | BR-<id> | Design structure | Frames are named; repeated elements use reusable components or documented candidates; layout is editable. | Design tree / node inspection | [ ] |
| DOD-03 | BR-<id> | Tokens and reuse | Existing tokens and code owners are reused or every deviation is approved. | Design variables + repository diff | [ ] |
| DOD-04 | BR-<id> | States | Required empty, loading, ready, saving, success, error, hover, focus, and disabled states exist or are explicitly N/A. | State frames + browser actions | [ ] |
| DOD-05 | BR-<id> | Behavior | The complete target user flow works without breaking preserved behavior. | Live browser scenario | [ ] |
| DOD-06 | BR-<id> | Responsive | Required desktop and mobile widths work without hidden actions or horizontal scrolling. | Viewport screenshots + DOM check | [ ] |
| DOD-07 | BR-<id> | Accessibility | Controls have names, keyboard focus is visible, order is logical, and feedback is perceivable. | Keyboard run + accessibility inspection | [ ] |
| DOD-08 | BR-<id> | Deterministic gates | Repository-specific typecheck, lint, tests, and build commands pass. | Command output | [ ] |
| DOD-09 | BR-<id> | Scope | No forbidden dependency, API, schema, route, or unrelated file change appears in the diff. | `git diff --stat` + targeted diff review | [ ] |
| DOD-10 | BR-<id> | Live evidence | Each acceptance criterion has a PASS/FAIL verdict with expected vs actual evidence. | `verify-ui` report + screenshots | [ ] |

## 17. Requirement coverage

| Requirement | Covered by DoD IDs | Gap |
|---|---|---|
| BR-01 | DOD-<id> | none / <missing proof> |

## 18. Final gate

- [ ] Every requirement is covered by at least one DoD row.
- [ ] Every applicable DoD row is checked and links to evidence.
- [ ] Every `Proposed` decision (section 14) was approved or removed before implementation.
- [ ] Deterministic checks and live browser verification both passed.
- [ ] The final repository diff matches the approved scope.
