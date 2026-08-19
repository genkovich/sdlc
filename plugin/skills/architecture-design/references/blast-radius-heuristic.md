# Blast-radius heuristic — when an architectural decision becomes ADR-worthy

## TL;DR (короткий вступ українською)

**Blast radius** перекладаємо як **«масштаб удару»** — наскільки боляче буде передумати рішення через 3 місяці. Три критерії:

1. **Чи переробка займе ≥3 днів?** (Незворотнє.)
2. **Чи це бачать ≥2 модулі?** (Зачіпає кілька модулів.)
3. **Чи є чесна альтернатива?** (Не «вибір серед однакових бібліотек»; не «вибір, виключений обмеженням стеку».)

Якщо хоч 2 з 3 → ADR. Якщо 0 — inline у sad.md. Очікувана кількість ADR на функцію розміру M — 5-12.

Канонічний приклад: ADR-0001 «Зберігати урок як таблицю блоків різних типів» з `course-lesson-mvp` — 3 з 3 → ADR.

---

The `architecture-design` skill makes 15-30 decisions per pass. Without a gate, you'd either generate one ADR per decision (kills the ADR genre — too much noise) or zero ADRs (loses the *why* of the important ones). The blast-radius heuristic picks the right 5-12. It is architecture-design's per-skill Socratic gate, run on every **Approved** decision (see [socratic-loop.md](./socratic-loop.md)).

## The three criteria

A decision crosses the threshold if it scores **2 of 3** (a single criterion = borderline — ask explicitly):

### 1. Irreversible

> If we picked a different option three months from now, would the rework take ≥3 days?

Examples that **fire** this criterion:
- **Storage choice** (вибір сховища: реляційна БД як Postgres, документна БД як Mongo, файлове сховище як S3 + DynamoDB) — переробка займає тижні через міграцію даних.
- **Synchronous vs asynchronous module coupling** (синхронний виклик одного модуля до іншого vs обмін через події у фоні) — змінює форму даних і модель збоїв.
- **ID strategy** (UUID v4 — випадковий; UUID v7 — час+випадковий, сортується; ULID — теж сортований; auto-increment INT) — переробка потребує *backfill* (скрипт, який пробігає всі існуючі записи і дописує нові ID).
- **Auth model** (сесії з cookie; JWT-токени; per-request tokens — кожен запит несе власний токен) — змінює форму всіх запитів.
- **Sharding key** (ключ, за яким дані розкидаються по серверах БД) — змінити пізніше = переписати всю кластеризацію.

Examples that **don't fire**:
- **Library choice within the same language** — наприклад, `slog` vs `zerolog` (обидві — структурне логування для Go). Переробка = search-and-replace, кілька годин.
- **Configuration value** (значення налаштування) — таймаут 5 с проти 10 с. Один PR.
- **Naming** (перейменування полів) — `Goal.objective` vs `Goal.title`. IDE робить це за хвилину.

### 2. Multi-module impact

> Does this decision change contracts seen by ≥2 modules?

Examples that **fire**:
- An event schema that crosses module boundaries.
- A shared error code namespace (`user.*`, `goal.*`).
- A pagination convention used by multiple endpoints.
- A migration that adds a column other modules read.

Examples that **don't fire**:
- Internal function naming inside one module.
- Private repo method signature.
- A log format used only by one service.

### 3. Has legitimate alternatives

> Will a reader six months from now ask "why not X?" where X is a real, non-strawman alternative?

This is the "surprising in 6 months" filter. It excludes:
- Decisions where the alternative is obviously worse (no straw man ADRs).
- Decisions where the alternative is excluded by an existing constraint (no ADR for "use Go because the repo is in Go").

It catches:
- Choices that look arbitrary from the code (e.g. why this caching TTL? why this circuit-breaker threshold?).
- Trade-offs where two reasonable engineers would pick differently.
- Anything where the option set was 2-3 serious options, not 1.

## How to use the heuristic during a Socratic pass

After each `AskUserQuestion` and the user's choice:

1. **Score it.** Quick mental check on the three criteria — how many fire?
2. **Decide:**
   - **0 fires** → inline in sad.md, no ADR.
   - **1 fire** → borderline. Default to inline unless the section is §4 Solution Strategy (where the bar is lower because strategy-level decisions are by definition broad).
   - **2+ fires** → ADR.
3. **On borderline, ask explicitly:** "This is borderline ADR-worthy because of <criterion>. Lock as ADR or keep inline?" with options `Lock as ADR` (Recommended if irreversible) / `Inline only`.

## Why 5-12 is the target range per feature

- **Below 5:** you're probably under-ADR-ing — either you're missing irreversibilities, or the feature is genuinely XS/S and that's fine.
- **5-12:** healthy range for an M-sized feature. Each ADR is a real decision with future reread value.
- **Above 12:** you're probably over-ADR-ing — bundling, scoping, or moving tactical detail into sad.md inline is likely needed.

For XS/S features, 2-4 ADRs is fine. For L/XL, 10-15 may be appropriate.

## Closing self-review

Before validating the run, check:

1. Does §9 reference every file in `adr/`? No orphans.
2. Does every ADR have a Status (Accepted) and a Decision outcome (not just a context)?
3. For each ADR — would the heuristic still gate it through if you ran it again? (Sanity check that you didn't ADR-ify a trivial config value.)
4. For inline decisions — does any of them feel like it should have been an ADR? Promote it.

## Anti-patterns

- **ADR-ifying an alternative you rejected.** The ADR is about the chosen path. Alternatives go in `## Considered options`, not their own ADR.
- **ADR with `Status: Proposed` from this skill.** Synchronous decisions with the user → `Accepted`. Use `decide-adr` for asynchronous Proposed→Accepted flows.
- **One ADR per Quality Goal.** Quality Goals live in §10; ADRs document specific *decisions* taken because of those goals.
- **A title that describes the problem, not the decision.** `0003-rate-limiting.md` (bad) vs `0003-sliding-window-with-redis.md` (good).
