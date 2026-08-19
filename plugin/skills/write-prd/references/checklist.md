# write-prd — Definition of Done + Anti-patterns

Used at the end of Protocol step 7. The SKILL.md `## Definition of Done` keeps the hardest-hitting non-negotiables inline; the full list lives here.

## Definition of Done

- [ ] `docs/features/<slug>/PRD.md` written; all sections filled (or `<!-- N/A: reason -->`).
- [ ] `docs/features/<slug>/.size` exists after this stage (read if present; classified + written here if absent).
- [ ] §4 holds at least one US per glossary role + per §2 goal.
- [ ] All AC testable in Given/When/Then form.
- [ ] NFR rows have numeric targets (no «fast» / «as fast as possible»).
- [ ] Non-goals explicitly listed with a reason (at least 3 entries, each with reason from idea-brief §6).
- [ ] §5 AC coverage spans all 5 types (happy / error / authorization / domain invariant / cross-context) after drops + OQ-migrations. OQ-migrated AC do NOT count toward coverage.
- [ ] **Every retained §4 US has at least one §5 AC** (the use-case floor — a retained US with zero ACs is a DoD failure, not a depth choice). OQ-migrated AC do NOT count.
- [ ] §5 AC contains **0** forbidden tokens (HTTP verbs, URL paths, status-code numerics, `module.error_name` strings, JSON-schema fragments, SQL/DB constructs). Pre-write regex scan emitted 0 hits — or all hits explicitly overridden in critic resolution with recorded rationale.
- [ ] §6.1 Security has 3-5 abuse cases.
- [ ] §8 Open Questions has a row for every `save_as_oq` with owner + due. No lone «TBD» without both fields.
- [ ] Roles in §4 US match CONTEXT glossary exactly (no `user`/`admin` invented if the glossary defines specific roles).
- [ ] Step 4 `AskUserQuestion` (channels) ran before reading any additional channel (or marked N/A if `--reference` was passed and user explicitly declined other channels).
- [ ] Step 7 edits-log maintained: every `Edit`/`Drop`/`Add`/`Save as Open Question` resolution appended one entry with `{item_id, action, before, after, user_reason}`.
- [ ] Every `save_as_oq` resolution from step 7 appears in §8 with **both** owner AND due filled (no lone owner, no lone due — missing either downgrades to `drop` with a warning surfaced to the user).
- [ ] Critic (`sdlc:critic`) ran on the post-Socratic draft + edits-log; every finding resolved via `AskUserQuestion` or overridden with rationale (recorded as a «Decision override» bullet in §1 ¶4).
- [ ] Roadmap updated (if `docs/roadmap.md` exists) — feature promoted to Now or registered.

## Anti-patterns (full list)

In addition to the inline anti-patterns in SKILL.md:

- **Skipping the interview front** — the idea must be captured in 1-3 sentences verbatim via `AskUserQuestion` before any drafting begins. Reconstructing the idea from the model's guess is a correctness failure, not a speed trade-off.
- **Naming concrete technologies in §1–§3** — a specific datastore, broker, framework, or library. The PRD is WHAT + WHY; HOW lives in `architecture-design`.
- **Implementation leak in AC** — HTTP verbs / URL paths / status-code numerics / `module.error_name` strings / JSON fragments / SQL constructs in §5 AC text. That mapping lives in `api-forge` (HTTP/schema/error-string) and `decide-adr` (DB-constraint decisions).
- **Treating brainstorm or initiatives artifacts as PRD inputs.** PRD draws only from CONTEXT + idea-brief (required) plus user-selected additional channels.
- **Propose without reading code** (when `Reference module code` channel was selected). The whole point of write-prd is grounding in real patterns.
- **Accept AC without Given/When/Then.** «feature works» / «happy path» phrasing fails DoD. Regenerate into GWT before `AskUserQuestion`.
- **Ignore template inline instructions.** `<!-- Skill instruction: ... -->` comments are the per-section contract. Skipping them produces a structurally-correct but content-empty PRD.
- **One AskUserQuestion for «approve all US».** Loses per-item edit affordance. Section is batch-rendered first (7a) so the user sees the big picture, then one question per item (7b).
- **Save-as-OQ without owner+due.** Skill MUST ask follow-up `AskUserQuestion` immediately after the user picks this option. If user leaves either field blank, the migration is downgraded to `Drop` with an explicit warning surfaced — never silently shipped with a half-filled §8 entry.
- **Retained §4 US with no §5 AC.** Even at `easy` depth, the use-case floor is a correctness floor. If `easy` depth can't infer an AC for a retained US, that decision is one of the irreversible/un-inferable ones it must ask about.
- **Dispatching `general-purpose` instead of `sdlc:critic`** without first checking availability. Fall back only on confirmed unavailability.
- **Skip critic step.** §7 Socratic loop only catches per-item issues — it cannot see cross-item drift caused by user edits. Writing the file without running the critic ships that drift downstream.
- **Resolve critic findings unilaterally** (without `AskUserQuestion`). The critic surfaces contested decisions to the user. Picking «revert» or «amend» without asking re-introduces the silent-edit failure mode.
