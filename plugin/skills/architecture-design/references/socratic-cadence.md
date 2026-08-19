# Socratic cadence — how to walk 12 sections without exhausting the user

## TL;DR (короткий вступ українською)

Три правила, щоб користувач не втомився від 30 питань підряд:

1. **Одне питання на невизначеність, не на параметр.** Якщо CLAUDE.md уже фіксує defaults (slog, JSON, info) — одне питання «Override defaults?», а не три окремі.
2. **Recommended першою опцією + 1 рядок ЧОМУ у description.** Не пиши довгу лекцію у самому питанні — користувач читає опції.
3. **Mini-recap кожні 5 питань.** Після 5 рішень — короткий список «що вже вирішили», щоб користувач бачив прогрес і ловив розбіжності одразу.

**Цільовий бюджет:** 8-20 питань на весь walk. Понад 25 — зона втоми.

---

A linear pass through 12 Arc42 sections plus ADR decisions can easily hit 30-60 questions if every uncertainty becomes a separate `AskUserQuestion`. That's the fatigue threshold — users start picking the first option blindly to escape, which defeats the whole point of asking. This file describes the cadence patterns that keep the user engaged.

The **depth dial** ([`../../_shared/interview-depth.md`](../../_shared/interview-depth.md)) tunes how many questions get asked at all: at `easy` the skill decides the convention-defaults itself and lists them in an assumptions ledger (asking only blast-radius decisions), at `hard` it walks every decision. The cadence rules below apply at every level — depth scales the *count*, not the *explanatory quality*.

## Three rules

### Rule 1 — One question per uncertainty, not per parameter

A section often has several related parameters that can be decided together. Bundle them.

**Bad:**
- "Which logging library? (slog / zerolog / zap)"
- "Which log format? (text / json)"
- "Which log level by default? (info / debug)"

**Good:**
- "I'm assuming the defaults from CLAUDE.md (slog, json, info). Override?" with options:
  - `Keep defaults (Recommended)` — fastest, consistent with rest of repo
  - `Override logging library` — for this feature only (rare)
  - `Override format or level` — for this feature only

This collapses 3 questions into 1 and signals "this is plumbing — don't overthink it."

### Rule 2 — Recommended first, WHY in description

Every `AskUserQuestion` follows the same shape:

- 2-4 options.
- First option is the recommendation with "(Recommended)" suffix.
- `description` is a 1-line WHY (why this is recommended, or why this is the right tradeoff for this option).
- No long explanations in the question itself — the user reads the options.

**Bad:**

```
Question: "There are several patterns for module-to-module communication.
You can use synchronous HTTP calls, which couple deployment lifecycles but
are simpler to reason about. Or you can use asynchronous events through an
outbox, which decouple modules but require eventual-consistency handling
and a worker. Which do you prefer?"
```

**Good:**

```
Question: "Module-to-module integration?"
Options:
  - Async via outbox events (Recommended)
    description: Loose coupling — perf module can be down without blocking goals writes. Cost: outbox table + worker (~150 LOC).
  - Sync HTTP call
    description: Simpler. Cost: goals writes fail when perf is down.
  - Sync via shared DB transaction
    description: Strong consistency. Cost: cross-module FK locks the refactor of either side.
```

### Rule 3 — Mini-recap every 5 questions

Every 5 `AskUserQuestion` exchanges, post a status summary in the assistant turn before the next question:

```
Recap so far (after §5 Building blocks):
- §1 — top-3 quality goals: availability, performance, recoverability
- §2 — pinned Go 1.26, Postgres 18, chi v5.1, no overrides
- §3 — context locked, C4 L1 drawn
- §4 — strategy: outbox events for coupling, Postgres-only persistence
- §5 — new module `internal/modules/goals/`, hexagonal layout
ADRs so far: 0001-outbox-pattern (§4)
Up next: §6 Runtime — which flows do you want to draw beyond the happy path?
```

This serves two purposes:
1. Lets the user see what they've decided without scrolling.
2. Surfaces drift early — if §3 says "no events" and §4 says "outbox events", the user catches it here, not in §11 Risks.

The recap goes *before* the next question, in the same assistant message. Keep it under 8 lines.

## Question budget

Aim for these targets per section. If you're consistently above, you're not bundling enough.

| Section | Typical questions | Notes |
|---|---|---|
| §1 Intro & goals | 0-1 | Usually pulled from PRD. Ask if top-3 QGs are unclear. |
| §2 Constraints | 1-2 | One bundled "any overrides on stack/versions?" Q. |
| §3 Context | 0-1 | Mostly drawn from PRD + Explore. |
| §4 Solution strategy | 2-4 | The dense one. Strategic choices → expect ADRs here. |
| §5 Building blocks | 1-3 | Module boundaries, hexagonal vs layered. |
| §6 Runtime | 1-2 | Which failure modes get sequence diagrams. |
| §7 Deployment | 0-2 | Often `<!-- N/A -->` for feature inside existing service. |
| §8 Crosscutting | 1 bundled | "Defaults from CLAUDE.md + overrides?" |
| §9 ADR index | 0 | Auto-populated. |
| §10 Quality reqs | 1-2 | Numbers from PRD NFR + verification method. |
| §11 Risks | 1-2 | "Top-3 risks you see?" then refine. |
| §12 Glossary | 0 | Auto-extract from PRD + sad.md content. |

**Total target: 8-20 questions across the whole pass.** Above 25 → fatigue territory.

## When to break the rules

If the user is clearly engaged and asking sub-questions back, you can ask more. The 25-question fatigue threshold is a default, not a hard cap. The signal to slow down is short or single-word answers — when the user starts replying just "Recommended" without elaboration on three questions in a row, bundle the next batch.

## Anti-patterns

- **Asking about a default that's already in CLAUDE.md** — that's not an uncertainty, that's a convention. Apply it; don't ask.
- **Asking the user to choose between two options with identical descriptions.** If you can't articulate the difference, neither can the user.
- **Three questions to decide one ADR.** Pick the option set first, then ask once.
- **Not asking on §4 Solution Strategy.** This section is the densest by design — that's where the architecture is actually decided. Don't paper over it.
