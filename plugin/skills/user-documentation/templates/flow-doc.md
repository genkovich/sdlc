<!-- TEMPLATE for one flow document. The doc-flow agent fills it and DELETES every HTML
     comment — the shipped doc contains no comments, no frontmatter, no unfilled <...>.
     Embed syntax below is shown as <embed:path> — replace with ![[path]] (vault) or
     ![](path) (repo docs) per the manifest's embed_syntax. -->

# Flow - <Title Case Name>

This guide explains how to <goal> in <Product>. <!-- + role restriction when observed:
"Only users with the **Mentor** role can create sessions." -->

---

<!-- ══ TYPE A (doc_type: task-flow) — repeat per step, numbered from 1, no gaps ══ -->

## Step 1: <Imperative Phrase>

<What to do, where the control is — 1–2 short paragraphs. UI elements as **"Create session"**,
toasts as _"Session created"_, URLs as `/mentorship`.>

<embed:screenshots/<slug>/01-<state-name>.png>
_<Optional one-line italic caption describing the state pictured.>_

---

## Step 2: <Imperative Phrase>

<...>

<!-- Field enumerations as bullets:
- **Title** (required) — The name of the session
- **Description** (optional) — What the session will cover -->

---

<!-- ══ TYPE B (doc_type: state-reference) — insert instead of (or after) the step chain:
     an optional navigation Step 1, then one block per observed condition. ══

### State 1: <Condition>

When <condition>, you will see:
- A **"<Badge/Button text>"** <element> next to <anchor>
- <What the action does>

<embed:screenshots/<slug>/02-<state-name>.png>

-->

<!-- ══ TAIL SECTIONS — keep ONLY those with observed data, in this order, each after `---`.
     An empty or speculative table is a defect; delete unused blocks entirely. ══ -->

## Prerequisites

- <Role or data precondition observed during the walk>

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| <Observed failure state> | <What the user does about it> |

---

## Permissions Summary

| Action | <Role 1> | <Role 2> |
|--------|----------|----------|
| <Action> | Yes | No |

---

## Status Reference

| Status | Badge Color | Meaning |
|--------|-------------|---------|
| **<status>** | <colour/style> | <meaning> |

---

## Error Handling

| Error | What you see | What to do |
|-------|--------------|------------|
| <error> | <observed message> | <action> |

---

## Related Flows

- <link:Flow - Other Flow> — <one line on when to go there>
<!-- vault: [[Flow - Other Flow]] · repo: [Flow - Other Flow](<Flow - Other Flow.md>) -->

---

## Notes

> **Note:** <Short observed caveat. Plain blockquote — never `> [!note]`.>
