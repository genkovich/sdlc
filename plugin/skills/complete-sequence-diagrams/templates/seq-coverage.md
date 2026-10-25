<!-- Template for `complete-sequence-diagrams` step 7 — written INLINE into docs/features/<slug>/sad.md §6   -->
<!-- as the LAST block of §6 (after every `### <flow name>` block, before `## 7`). Heading text is FIXED:   -->
<!-- a re-run finds `### Coverage: US/AC → flows` and replaces the whole block (heading → summary line).    -->
<!-- Rows: every PRD §4 user story (in §4 order), then every PRD §5 AC (in §5 order). IDs exactly as the PRD -->
<!-- spells them (US-01, AC-04b, …). No GAP rows may remain in the written table.                          -->
<!--   Realized by — the `### <flow name>` heading text(s) from §6; `—` when How = N/A.                    -->
<!--   How         — `flow` (dedicated flow) · `branch` (an alt/else inside a flow) · `N/A` (non-runtime). -->
<!--   Note        — the branch label for `branch`; the one-line reason for `N/A`; empty for `flow`.       -->
<!-- `**Flags:**` is appended by step 8 (new participants, ADR-worthy decisions) — flag only, no ADR here.  -->

### Coverage: US/AC → flows

| ID | Realized by (§6 heading) | How | Note |
|---|---|---|---|
| US-01 | `<flow name>` | flow | |
| US-02 | `<flow name>`, `<other flow name>` | flow | |
| AC-01 | `<flow name>` | flow | |
| AC-02 | `<flow name>` | branch | `alt <error condition from acceptance criteria>` |
| AC-03 | — | N/A | <one-line reason, e.g. authorization enforced in middleware — not a runtime flow> |

Coverage: <n>/<n> user stories · <m>/<m> ACs — <k> non-runtime N/A.

**Flags:** <none | `<participant>` not declared in §5 — for architecture-design · <decision> worth an ADR — for /sdlc:decide-adr>
