---
name: ship-feature
model: inherit
effort: medium
agents: []
description: >-
  Use to close the loop after review — verify the feature actually works, write the changelog,
  and open the pull request. Triggers on "ship {slug}", "open a PR for {slug}", "changelog for
  {slug}", "prepare {slug} for merge", "/sdlc-ship-feature {slug}", "відправ фічу {slug}",
  "створи PR для {slug}", "changelog для {slug}". Gate: refuses if
  docs/features/{slug}/_review/review-<date>.md does not show PASS (produced by review-feature).
  Runs the feature end-to-end to confirm it actually works (not just green tests), drafts a
  changelog + PR body that link PRD/ACs/ADRs and the SDLC-Task commit history, detects the git
  forge (gh for GitHub / glab for GitLab) and proposes the right PR-create command, then moves the
  feature to Shipped in docs/roadmap.md. Never auto-merges to main — merging is the user's call.
  Output: docs/features/{slug}/CHANGELOG.md + PR body (proposed command or URL).
triggers:
  - /sdlc-ship-feature
  - "ship "
  - "open a PR for"
  - "changelog for"
  - "prepare for merge"
  - "відправ фічу"
  - "створи PR для"
  - "changelog для"
stage: "18"
---

# Skill: ship-feature (SDLC stage 18 — terminal)

The closing step. `review-feature` confirmed the change is correct on paper; `ship-feature` confirms it **works in reality** and packages it for merge. The loop ends here: a reviewed, verified change with a changelog and an open PR — not a merge to main (that stays a human decision).

Forge-agnostic and stack-agnostic: verification commands are detected the same way `implement-tasks` detects them; the PR step targets whatever forge the remote points at (GitHub via `gh`, GitLab via `glab`, or copy-paste).

## Owner

The implementer (drives) + the reviewer who signed off in `review-feature`.

## Inputs

- `<slug>` — feature slug (same one used by every upstream stage).
- **Gate (hard refuse):** `docs/features/<slug>/_review/review-<date>.md` showing `PASS`. If missing or showing `CHANGES REQUESTED` → refuse with: «run `/sdlc-review-feature <slug>` first — ship-feature requires a PASS verdict».
- Read: `docs/features/<slug>/PRD.md` (what to claim in the changelog), `docs/features/<slug>/adr/` (decisions worth recording), the feature's commits (`SDLC-Task` trailer history via `git log --grep SDLC-Task`).

## Protocol

1. **Gate check.** Confirm `docs/features/<slug>/_review/review-<date>.md` exists and its verdict is `PASS` (search for the most recent date). If absent or non-PASS → hard refuse with the pointer above.

2. **Final verification — does it actually work.** Re-run the detected gate (unit + integration where available + lint + vet). Then **run the feature for real** against its acceptance criteria — not just "tests pass": start the app / hit the endpoint / exercise the flow and observe the PRD's outcomes (e.g. the default-on read returns defaults; an invalid value is rejected). If the app cannot be run here (no runtime, no Docker), say so explicitly and record what was verified vs deferred — never claim verified-working when only tests compiled.

3. **Write the changelog.** From [`./templates/changelog.md`](./templates/changelog.md): what changed, why (link `PRD.md` + the key ADRs), any migration/operational note (e.g. "adds migration 000023 — run it on deploy"), and how to use it. Partner-facing if the change is partner-facing. Write to `docs/features/<slug>/CHANGELOG.md`.

4. **Prepare the PR body.** Ensure the work is on a feature branch (not the default branch). Draft the PR body from [`./templates/pr-body.md`](./templates/pr-body.md): summary, the ACs it satisfies, links to PRD/sad/ADRs, the `SDLC-Task` commit list, the test + verification evidence, and any migration/rollback note.

5. **Detect the forge + propose the PR command.** Inspect the git remote URL:
   - `github.com` → `gh pr create --title "feat(<slug>): <summary>" --body-file docs/features/<slug>/pr-body.md`
   - `gitlab.com` or self-hosted GitLab (any non-github remote) → `glab mr create --title "feat(<slug>): <summary>" --description-file docs/features/<slug>/pr-body.md`
   - Remote undetectable / unknown forge → print the branch name + body for manual PR creation.
   **Propose** the command — do not push to a shared remote unasked and never merge to main.

6. **Update the roadmap → Shipped.** Move this feature's item from **Now** to **Shipped** in `docs/roadmap.md`: add the date, the outcome one-liner, a link to `docs/features/<slug>/`, and the PR link/command. Remove the item from the Now table. If `docs/roadmap.md` does not exist → skip and note it (roadmap is optional at this stage).

7. **Terminal handoff.** Emit the **stage-handoff block** per [`../_shared/handoff.md`](../_shared/handoff.md) — terminal variant. *What I did* (verification result: verified-working / what was deferred and why; the roadmap update). *Review* (the changelog path + the PR body path). *Run next* = **Done** — the PR command (or URL if the user already ran it); «merging to main is your call». There is no `/sdlc-` successor.

## Definition of Done

- Gate passed: `_review/review-<date>.md` shows PASS — the skill confirmed it before proceeding.
- The gate was re-run and the feature was exercised against its ACs (or the deferral was stated explicitly with the reason).
- `docs/features/<slug>/CHANGELOG.md` exists, linking PRD + load-bearing ADRs and including the operational note (migrations, flags).
- `docs/features/<slug>/pr-body.md` is prepared with the full PR body.
- The forge-appropriate PR command is proposed (work is on a feature branch; main untouched).
- `docs/roadmap.md` updated — feature moved to Shipped (or skip noted if roadmap absent).

## Anti-patterns

- **Shipping without a PASS review.** The gate is unconditional — `review-feature` must confirm correctness before `ship-feature` runs.
- **"Tests pass" ≠ "it works".** Run the actual feature against the PRD's outcomes; green unit tests don't prove the wired system behaves.
- **Claiming verified when you only compiled.** If the runtime/Docker wasn't available, say what was deferred — don't overstate.
- **Auto-merging to main / pushing to a shared remote unasked.** Propose the PR; the merge is the team's call.
- **A changelog that restates the diff.** Say what changed and why (link the PRD + ADR), plus the operational note (migrations, flags) — not a file list.
- **Forgetting the migration/rollback note** when the change includes one — the deployer needs it.
- **Skipping the roadmap update.** If `docs/roadmap.md` exists, the Shipped move is not optional — delivery itself keeps the roadmap current.

## References & templates

- [`./templates/changelog.md`](./templates/changelog.md) — changelog scaffold.
- [`./templates/pr-body.md`](./templates/pr-body.md) — PR description scaffold (forge-agnostic).
- [`../_shared/handoff.md`](../_shared/handoff.md) — stage-handoff block format (terminal variant).
