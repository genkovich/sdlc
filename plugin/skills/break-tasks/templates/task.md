---
id: T1
title: "<imperative, specific title>"
layer: "migration|domain|infra|app|ports|ui|tests|wiring|docs"
deps: []                # task ids that must finish first
acs: ["AC-01"]          # PRD §5 acceptance criteria this task satisfies
files_hint: ["path/or/dir/the/task/touches"]
owner: "<owner / TBD lead>"
estimate: "S"           # S/M/L or hours
status: "todo"
---

# T1 — <title>

## Why

<!-- instruction: 1–2 sentences. Link the upstream source, don't paste it:
derives from [PRD §AC-01](../PRD.md), [sad §6](../sad.md), [ADR-0001](../adr/0001-....md). -->

## What

<!-- instruction: the concrete change, scoped to ≤1 day / one reviewable PR. Name the files/dirs
(same as files_hint). For a migration task: the **staged** up + down files under
`docs/features/<slug>/migrations/<NN>_*` (which `implement-tasks` promotes into the live `migrations/`).
For a ports task: the handler + its dto + errors. For a ui task: the screen/component reusing the
repo's existing design-system primitives + tokens (per architecture-map.md §Frontend) — a *new*
component only when no existing primitive fits. Keep it within one layer where possible. -->

## Definition of Done

<!-- instruction: testable bullets. e.g.: -->
- [ ] <unit/integration test for this task passes>
- [ ] <staged migration is promoted to live `migrations/`, then applies and reverts cleanly> (migration tasks)
- [ ] <handler returns the PRD'd outcome for AC-01> (ports tasks)
- [ ] <component renders + the visual-regression / component test passes> (ui tasks)
- [ ] lint + vet clean

## Notes

<!-- instruction: gotchas, the lane this shares with another task (overlapping files_hint), any
Hard Rule it must respect. -->
