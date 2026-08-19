# `AskUserQuestion` examples — explanatory pattern for architecture-design

## TL;DR (короткий вступ українською)

Цей файл показує, **як саме формулювати питання користувачу** на кроках 7 (Socratic loop) і 8 (вирішення зауважень критика).

Принцип: option label — це **наступна дія skill-у** («Прийняти», «Перенести у §11 OQ»), а option description — це **3-5 речень, що технічно станеться** + **trade-off простими словами без жаргону**. Не «modify the API», а «додам поле X у таблицю Y і route Z». Не «UNION-query», а «обʼєднання 4 SELECT-ів через SQL UNION — повільніше за читання з однієї таблиці».

Канонічний наскрізний приклад — **ADR-0001 «Зберігати урок як таблицю блоків різних типів»** (`content-storage-strategy`) з навчального LMS-проєкту: далі всі фрагменти цього файлу цитують саме його.

## Загальна форма

The canonical question/option contract — junior-friendly, bilingual, label = next mechanical step, description = 3-5 sentences — lives in [`../../_shared/ask-style.md`](../../_shared/ask-style.md). Read that first. How Step 6 (Socratic batch loop) and Step 7 (critic resolution) phrase questions and options. The contract from [socratic-loop.md](./socratic-loop.md) and [critic-phase.md](./critic-phase.md) is normative; this file shows the **shape** of the dialogue so options *describe what the skill will do*, not just *what they're labelled*.

## Shape

- **Question**: 1 sentence framing the decision + (when useful) a 1-line «earlier decisions» recap so the user sees the dependency chain without scrolling.
- **Each option**:
  - `label` — 1-5 words, action-form: «Async via outbox events (Recommended)», «Sync HTTP call», «Save as Open Question», «Drop and re-frame», «Lock as ADR», «Override».
  - `description` — 1-2 sentences explaining the **mechanical next step** (no architecture philosophy, no design rationale beyond a 1-line WHY).

All decision-types (Surface / UI-architecture / Strategic / Building-block / Crosscutting bundle / Quality scenario / Risk entry / Open-architectural-decision) share the same 4-state machine: `Approve` / `Edit` / `Save as Open Question` / `Drop`. `Cancel` and `Reject` are synonyms for `Drop`.

## Target-surface decision (§4 — walked FIRST) — что саме будуємо

> **UA-коментар.** Це **перше** рішення §4 і headline-механізм скіла: *яку поверхню (surface) ми будуємо* — бекенд-сервіс, веб-фронт, мобайл, CLI, worker, library. Це `multiSelect` (можна обрати >1). Recommended-набір деривиться з PRD §1 «для кого» + §4 ролей. >1 поверхні майже завжди → ADR (мульти-модульне + незворотнє). На resolution skill пише `target_surfaces: [...]` у frontmatter SAD, і §5 малює один контейнер на кожну поверхню. → `../../_shared/surfaces.md`

```
Question:
  §4 — ЩО САМЕ будуємо для course-lesson-mvp? (можна обрати кілька)
  КОНТЕКСТ: PRD §1 каже «methodist складає урок у браузері, learner читає урок у браузері». Тобто
  є серверна частина (зберігання + контракт) і браузерний UI. Це рішення вирішується ПЕРШИМ у §4,
  бо воно гейтить §5 (один C4-контейнер на поверхню) і всі наступні стадії (api-forge, тести, задачі).
  ЧОМУ ВАЖЛИВО: >1 поверхні = мульти-модульна незворотня фіча → ADR; це також визначає, які
  артефакти згенерують наступні скіли (UI-шар задач, фронтові рівні тестів, форму контракту).
  Прочитай descriptions перед вибором.

Options:  # multiSelect
  - label: "backend-service + web-frontend (Recommended) (→ spawn ADR)"
    description: "Будуємо і бекенд-сервіс (володіє REST/JSON-контрактом + зберіганням), і веб-фронт (браузерний UI, що СПОЖИВАЄ контракт, не створює його). НАСЛІДОК: я пишу target_surfaces: [backend-service, web-frontend] у frontmatter; §5 малює ДВА контейнери (API + web/SPA); далі йде follow-on UI-architecture рішення (SSR / SPA / hybrid); api-forge згенерує OpenAPI, break-tasks додасть шар `ui`, plan-tests додасть component / visual-regression / e2e-through-UI рівні. Мульти-поверхня → спавню ADR на сам вибір."
  - label: "backend-service only (→ можливо без ADR)"
    description: "Тільки серверний сервіс із контрактом (HTTP/REST або події); UI вже існує окремо або не потрібен. НАСЛІДОК: target_surfaces: [backend-service]; §5 — один контейнер API; немає UI-шару задач і фронтових тестів. Одна поверхня → blast-radius зазвичай не спрацьовує на самому виборі."
  - label: "Save as Open Question"
    description: "Я приберу рішення про поверхні з §4 і додам рядок у §11: «Open architectural decision: target surfaces — Open question — owner: <ти введеш>, due: <ти введеш>». Без поверхонь §5 і всі наступні стадії заблоковані, тому owner+due обовʼязкові; без обох — Drop."
  - label: "Drop and re-frame"
    description: "Я викину поточний набір і запитаю ще раз з переформульованим (наприклад, додам mobile-app, якщо потрібен ще й застосунок). Це рішення обовʼязкове — другий Drop ескалюється у Save-as-OQ з owner=Architect."
```

## UI-architecture decision (§4 — one per declared UI surface)

> **UA-коментар.** Йде ОДРАЗУ після Target-surface, по разу на кожну оголошену UI-поверхню (`web-frontend` / `mobile-app` / `desktop-app`). web → SSR / SPA / hybrid; mobile → native / cross-platform. Гейтиться як будь-яке §4 стратегічне рішення (часто → ADR). Тримаємо легким: НЕ малюємо component-tree / токени / екрани — UI **переюзає** наявний design system із `architecture-map.md` §Frontend. → `../../_shared/surfaces.md`

```
Question:
  §4 UI-architecture для web-frontend — як рендериться браузерний UI редактора уроку?
  КОНТЕКСТ: methodist перетягує блоки на льоту (drag-and-drop), learner читає готову сторінку.
  architecture-map.md §Frontend показує: у репо вже є React + design-system @org/ui (Button, Card,
  Modal) + токени у tokens.css.
  ЧОМУ ВАЖЛИВО: це незворотній вибір доставки (переписати SSR↔SPA пізніше = тижні). UI ПЕРЕЮЗАЄ
  наявний design system — ми не малюємо новий.
  Прочитай descriptions.

Options:
  - label: "SPA, що споживає API (Recommended) (→ spawn ADR)"
    description: "Браузерний клієнт (React, наявний @org/ui) тримає стан редактора локально і б'є по REST-контракту бекенду. Перевпорядкування блоків — оптимістичне локальне, потім PATCH. ПЛЮСИ: миттєвий drag-and-drop без round-trip; чисте розділення UI/контракт. МІНУСИ: дублює трохи логіки валідації на клієнті; SEO-сторінка learner потребує окремого рендера. НАСЛІДОК: я спавню ADR з назвою 'spa-consuming-rest-api', §5 малює контейнер web/SPA поряд з API, екрани будуються з наявних @org/ui-компонентів + токенів (не нові), break-tasks додає шар `ui`."
  - label: "Server-rendered (SSR) (→ spawn ADR)"
    description: "Сервер віддає готовий HTML, інтерактив — точково. ПЛЮСИ: проста сторінка learner, гарне SEO. МІНУСИ: drag-and-drop редактора потребує round-trip або острівців інтерактиву. НАСЛІДОК: я спавню ADR 'server-rendered-ui', §5 малює web-контейнер як частину деплою сервера."
  - label: "Save as Open Question"
    description: "Я приберу UI-architecture з §4 і додам рядок у §11: «Open architectural decision: web UI-architecture — Open question — owner: Frontend Lead, due: <ти введеш>». Питаю owner+due далі."
  - label: "Drop and re-frame"
    description: "Я викину набір і запитаю ще раз (наприклад, hybrid замість чистого SSR/SPA). Рішення обовʼязкове для оголошеної UI-поверхні — другий Drop ескалюється у Save-as-OQ."
```

## Strategic decision (§4 Solution strategy) — канонічний приклад `course-lesson-mvp`

> **UA-коментар.** Це той самий приклад, який лекція 6.4 (Слайди 14-19) і beer-lms `adr/0001-content-storage-strategy.md` використовують як наскрізний. Питання реальне з функції `course-lesson-mvp` — «як зберігати урок зі змішаного контенту?». Зверни увагу: option label = наступна дія skill-у, не просто назва опції. Description — 3-5 речень з конкретикою (назви таблиць, ADR-номери), а не «modify the storage».

```
Question:
  §4 Solution Strategy — Як зберігати урок з content_type=mixed (текст + медіа)?
  Сценарій: methodist складає урок з блоків (текст / відео-вкладення / картинки),
  натискає Опублікувати; учень потім читає; методист хоче переставляти блоки на льоту.
  (Попередні рішення: §1 топ-3 якості — швидкість редагування, рендер сторінки учня;
   §2 у стеку Postgres + S3 для медіа; §3 актори methodist, learner.)

  ВАЖЛИВО: blast-radius 3/3 — рішення незворотнє (методисти наповнять десятки уроків →
  міграція з простоєм), зачіпає 3 модулі (фронт-редактор / бек-API / медіа-обробник),
  є чесні альтернативи. Очікувано → спавн ADR.

Options:
  - label: "Таблиця блоків різних типів + окрема таблиця медіа (Recommended) (→ spawn ADR-0001)"
    description: "Дві нові таблиці: lesson_blocks (id, lesson_id, sequence INT, type, content) і media_blobs (id, s3_url, mime, …). Колонка sequence зберігає порядок. ПЛЮСИ: NFR p95 ≤500 мс на редагування виконується природно — UPDATE один рядок (не цілий документ); перевпорядкування — одна транзакція з кількома UPDATE на sequence. МІНУСИ: дві нові таблиці у міграції; UNIQUE(lesson_id, sequence) потребує окремого ADR-сусіда. НАСЛІДОК: я спавню ADR-0001 з назвою 'content-storage-strategy', додаю рядок у §9 ADR-table, схема фіксується для `sdlc:generate-data-model`."
  - label: "Один цілісний JSON-обʼєкт у S3, метадані у БД (→ spawn ADR-0001)"
    description: "Фронт-редактор серіалізує цілий урок у JSON, кладе у S3 як lessons/{id}.json; у БД зберігається тільки lesson_id → s3_key + updated_at. ПЛЮСИ: одна БД-таблиця замість двох; додавання нового типу блоку не потребує schema-migration. МІНУСИ: при перетягуванні одного блоку фронт відправляє цілий урок ≈100 КБ; NFR p95 ≤500 мс під ризиком на великих уроках; повнотекстовий пошук всередині уроку неможливий. НАСЛІДОК: я спавню ADR-0001 з опцією 'json-blob-in-s3', додаю рядок у §9, схема для `sdlc:generate-data-model` — тільки lessons-метадані."
  - label: "Дві окремі сутності text_blocks + media_blocks, JOIN на API-рівні (→ spawn ADR-0001)"
    description: "Чисте розділення за типом контенту. API при GET /lessons/{id} робить два запити (SELECT з text_blocks і media_blocks) і зливає результат за sequence. ПЛЮСИ: чисті межі сутностей. МІНУСИ: 'mixed content' стає діравою абстракцією, бо клієнт зшиває дві окремі форми у одну; зайвий JOIN на кожен read; нові типи блоків (poll, code) потребуватимуть нових таблиць. НАСЛІДОК: я спавню ADR-0001 з опцією 'two-entities-join', додаю рядок у §9."
  - label: "Save as Open Question"
    description: "Я приберу це рішення з §4 і додам рядок у §11 Risks: «Open architectural decision: content storage strategy — Open question — Resolve before `sdlc:generate-data-model` — owner: <ти введеш>». Далі я попрошу тебе ввести owner + due одним рядком. Без обох — рішення стає Drop."
  - label: "Drop and re-frame"
    description: "Я викину поточний набір опцій і запитаю ще раз з переформульованим набором (наприклад, тільки структуровані варіанти, якщо ти відкинув JSON-blob). Використовуй, якщо у наборі опцій не вистачає важливого виміру."
```

**Що тут не junior-friendly у старій версії і як спростили:**

- Раніше було абстрактне «module-to-module integration» — тепер конкретна функція з конкретним сценарієм (methodist складає урок).
- Раніше option label = «Async via outbox events» — тепер «Таблиця блоків різних типів + окрема таблиця медіа (→ spawn ADR-0001)» з явною технічною формою і назвою ADR.
- Раніше description = одне речення з англо-жаргоном — тепер 3-5 речень з ПЛЮСИ / МІНУСИ / НАСЛІДОК і конкретними числами (p95, ≈100 КБ, кількість таблиць).

After `Save as Open Question`, the follow-up `AskUserQuestion`:

```
Question:
  Module-integration decision is migrating to §11 Open Decisions. Provide owner and due
  (YYYY-MM-DD or stage trigger like «before `/sdlc-break-tasks`»). Both mandatory.

Options:
  - label: "Provide owner + due"
    description: "You type «owner: <name/role>, due: <date or stage>» in one line; skill applies it to the §11 row."
  - label: "Cancel — Drop instead"
    description: "Skill abandons the OQ migration and applies Drop to the decision (removes from §4, no row in §11)."
```

## Building-block decision (§5)

```
Question:
  §5 Building blocks — Where does the rate-limiter logic live?
  (Earlier: §4 chose sliding-window + Redis; Explore shows APIGW middleware layer exists.)

Options:
  - label: "Middleware in APIGW (Recommended)"
    description: "Reuses APIGW lifecycle, no new deployment unit, ~80 LOC. Likely no ADR (small blast radius). Skill keeps decision verbatim, runs blast-radius gate."
  - label: "New module internal/modules/ratelimit/"
    description: "Cleaner module boundary, easier to unit-test in isolation. Cost: new module wiring + extra deployment surface. Skill keeps decision verbatim, runs blast-radius gate."
  - label: "Save as Open Question"
    description: "Skill removes the decision from §5 and adds a §11 row: «Open architectural decision: rate-limiter location — Open question — owner: <you-type>, due: <you-type>». Skill asks owner+due next. Without both, downgrades to Drop."
  - label: "Drop and re-frame"
    description: "Skill discards the current option set and asks once more with reframed options. Building-block decisions are mandatory — second drop escalates to Save as OQ with owner=Architect + warning."
```

## Crosscutting bundle (§8)

```
Question:
  §8 Crosscutting concepts — Logging / auth / errors / IDs.
  Defaults from CLAUDE.md: slog structured JSON / JWT via session middleware / domain
  sentinel → apperr JSON / UUID v7 in app layer. Override any of these for this feature?

Options:
  - label: "Keep CLAUDE.md defaults (Recommended)"
    description: "Skill writes §8 table referencing CLAUDE.md sections, no per-feature overrides. Fastest, consistent with rest of repo."
  - label: "Override one or more"
    description: "You type which crosscutting concept needs a feature-specific override + the reason; skill regenerates §8 with the override row + asks once more. Use only when PRD §6 NFR or §6.1 Security signals it (rare)."
  - label: "Save as Open Question"
    description: "Skill removes the §8 row and adds a §11 row: «Open architectural decision: crosscutting overrides — Open question — owner: <you-type>, due: <you-type>». Skill asks owner+due next."
  - label: "Drop and re-frame"
    description: "Skill discards the bundle and asks per-concept individually (slog? auth? errors? IDs?). Use when you want granular review of plumbing."
```

## Quality scenario (§10)

```
Question:
  §10 Quality requirements — QG-1 (Availability under partial failure).
  When: downstream perf module returns 5xx for ≥30s; Then: goals writes still succeed
  (PRD NFR p95 ≤ 250ms holds); How verify: chaos drill (kill perf pod for 60s, observe
  goals.write_success_rate ≥ 99.5%).
  Approve the scenario verbatim, edit, defer, or drop?

Options:
  - label: "Approve as-is"
    description: "Skill keeps QG-1 scenario verbatim in §10 and moves to QG-2."
  - label: "Edit verification method"
    description: "You type the new How-verify (e.g. «load test with k6 — 10k RPS for 5 min»); skill regenerates QG-1 and asks once more (single-iteration cap)."
  - label: "Save as Open Question"
    description: "Skill removes QG-1 scenario from §10 and adds a §11 row: «Open architectural decision: QG-1 verification method — Open question — owner: SRE, due: before `/sdlc-plan-tests`». Skill asks owner+due next."
  - label: "Drop"
    description: "Skill removes QG-1 from §10 and re-prompts you to pick a replacement Quality Goal from PRD NFR. §1 Top-3 must remain ≥3 — this is a coverage-floor case."
```

## ADR-gate decision (after Approve fires blast-radius)

```
Question:
  Blast-radius gate after «Async via outbox events» Approved.
  Score: irreversible (3 days+ rework after data accumulates) + multi-module (events
  cross goals/perf module boundaries).
  Lock as ADR or inline only?

Options:
  - label: "Lock as ADR (Recommended)"
    description: "Skill creates adr/0001-async-outbox-for-module-integration.md from the AskUserQuestion options + your rationale; adds a row to §9 ADR table; commits sad §4 + adr/0001 together in Step 6e."
  - label: "Inline only"
    description: "Skill writes the decision into §4 with rationale paragraph but no ADR file. Use when the decision feels small-blast-radius despite 2+ criteria firing — typical only for §8 crosscutting or §5 internal layout."
```

## Critic-finding resolution (Step 7)

```
Question:
  [F1] Strategic-vector drift — §4 caps «async via outbox events» (DEC-§4-modulesIntegration
  Approved at Step 6d), but §6 Critical flow 1 «happy-path goal create» shows synchronous
  call from goals → perf without outbox emit.
  PRD §6 NFR QG-1 cites availability under partial failure as dominant (line 47).
  Suggested: amend §6 flow 1 to insert outbox emit between goals.write and perf.update,
  OR mark §4 outbox decision as preliminary and re-open it in next pass.
  How do you want to resolve it?

Options:
  - label: "Accept revert"
    description: "Skill applies the critic's suggested amendment verbatim — §6 flow 1 regenerated with outbox emit step. §4 stays unchanged."
  - label: "Accept amendment (different wording)"
    description: "You type the alternative wording for §6 flow 1 (or which sad section to amend differently); skill applies your wording."
  - label: "Override"
    description: "Skill keeps §6 unchanged and emits a bullet in §1 ¶4: «Strategic-vector drift in §6 flow 1 — overridden by author, rationale: <your reason>», so downstream skills (`sdlc:complete-sequence-diagrams`, `sdlc:api-forge`) see the deliberate choice. You provide the rationale next."
```

```
Question:
  [F5] §3 C4 Context block left as template stub — Mermaid block contains placeholder
  `Person(user, "<User>", "<role + intent>")` instead of real actors from CONTEXT glossary
  + PRD §4 US.
  Suggested: regenerate §3 C4Context block with real actors (IC, EM, HR per CONTEXT) +
  external systems from the architecture-map / scan (Postgres, notification-service).
  How do you want to resolve it?

Options:
  - label: "Accept regenerate"
    description: "Skill regenerates §3 C4Context block from CONTEXT glossary + PRD §4 US + the architecture-map / scan. Skill asks once more on the regenerated block (single-iteration cap)."
  - label: "Accept amendment (different wording)"
    description: "You type the Mermaid block contents; skill applies your version verbatim."
  - label: "Override"
    description: "Skill keeps §3 unchanged and emits a §1 ¶4 bullet: «§3 C4 stub left intentional — overridden by author, rationale: <yours>». Use rarely — downstream skills (`sdlc:complete-sequence-diagrams`) need C4 Context for the flow passes."
```

```
Question:
  [F6] §10 QG-2 references a number not in PRD — scenario says «p99 ≤ 100ms» but PRD
  §6 NFR only specifies p95 (≤ 250ms) and «no p99 target this phase».
  Suggested: rewrite QG-2 to use p95 target from PRD verbatim, OR add p99 target to PRD
  §8 Open Questions before continuing.
  How do you want to resolve it?

Options:
  - label: "Rewrite into PRD-cited form"
    description: "Skill regenerates QG-2 with PRD §6 NFR p95 ≤ 250ms verbatim. Skill asks once more on the new scenario."
  - label: "Override"
    description: "Skill keeps QG-2 unchanged and emits §1 ¶4 bullet: «§10 QG-2 p99 target — overridden by author, rationale: <yours>». Use only when you're committed to PRD §8 follow-up (own the back-port to PRD)."
```

## Anti-pattern: terse option labels

```
# DON'T — option label = next mechanical step is opaque
Options:
  - Approve
  - Edit
  - Reject
  - Defer

# DO — option label is action-form, description names the next concrete step
Options:
  - label: "Approve as-is"
    description: "Skill keeps decision verbatim, runs blast-radius gate next."
  - label: "Edit"
    description: "You type new wording; skill regenerates and asks once more."
  - label: "Save as Open Question"
    description: "Skill removes decision, adds §11 row with owner+due (asked next)."
  - label: "Drop"
    description: "Skill removes decision. If mandatory, re-asks with reframed options once; if optional, leaves it out."
```

## Junior-friendly Ukrainian explanations (mandatory from 2026-05-23)

Every `AskUserQuestion` у цьому skill-у формулюється так, щоб **junior-розробник першого року** міг зрозуміти суть рішення, різницю між опціями і наслідки кожної — без помічника поряд. Старий шаблон («1-line WHY», 5-word labels) deprecated для Step 6 + Step 7.

### Mandatory shape

1. **Українська мова всюди** — labels + descriptions. Технічні ідентифікатори (ADR, JSONB, JWT, UUID, FK, GIN) залишаються англійською — це назви; але «дії» опцій — українською («Прийняти», «Відредагувати», «Перенести у §11 OQ», «Видалити»).

2. **`question` поле — 3-4 речення** з трьох блоків:
   - **КОНТЕКСТ** — чому це питання, який сценарій уявляти, що саме ми вирішуємо (в одному реченні з прикладом)
   - **ЧОМУ ВАЖЛИВО** — який QG / NFR / PRD-вектор зачіпає; blast-radius (irreversible? multi-module? впливає на performance / security / UX?); основний trade-off у грі
   - **ОПЦІЇ НИЖЧЕ** — підказка прочитати descriptions перед вибором

3. **Option `description` — 3-5 речень** із чотирьох обов'язкових елементів:
   - **Що технічно станеться**: конкретні назви таблиць / endpoint-ів / файлів / ADR-номерів. Не «modify the API», а «додам поле `is_methodist BOOLEAN` у таблицю `org_members` і новий route `POST /courses` у `internal/modules/course/ports/handler.go`».
   - **Що дістаємо / що втрачаємо** — trade-off простими словами, без жаргону:
     - Не «backfill-migration» → «скрипт, який пробігає всі існуючі записи у таблиці і дописує нові поля; під час прогону DB читається, але запис у ці рядки блокований»
     - Не «UNION-query» → «об'єднання 4 окремих SELECT-ів в один результат через SQL UNION — повільніше, ніж читання з однієї таблиці»
     - Не «GIN indexing» → «спеціальний тип індексу Postgres, який дозволяє шукати всередині JSON-полів, але займає у 3-5× більше місця і повільніше пишеться»
     - Не «cursor pagination» → «передача останнього бачаного ID клієнту, щоб наступна сторінка починалася з нього; уникає `OFFSET`, який сповільнюється на великих сторінках»
   - **Наступний механічний крок skill-у**: «я спавню ADR-NNNN з назвою X, додаю рядок у §9 ADR-table, схема фіксується для `sdlc:generate-data-model`»
   - **Hidden trade-off** — якщо є умова, при якій рішення зривається («це працює тільки якщо у вас вже Redis у стеку», «через 6 місяців у вас буде downtime для backfill», «UX змінюється для existing users і їм треба буде релогінитися») — згадати її **прямо у description**, а не у follow-up. Junior не побачить цього тригера сам.

### Заборонено

- Стислі англомовні labels («Approve», «Edit», «Drop», «Reword»)
- Однорядкові descriptions
- Технічні терміни без розшифровки (UNION, backfill, GIN, cursor, idempotent, transactional, etc.)
- Trade-off-и, заховані у follow-up («якщо вибрав це — потім спитаю про X, а він має складність Y»)

### Контр-приклад (deprecated shape)

```
- label: "Approve"
  description: "Apply decision."
```

### Правильно (mandatory shape)

```
- label: "Прийняти JSONB-колонку (→ spawn ADR-0002)"
  description: "Одна колонка lessons.body типу jsonb, яка зберігає весь масив блоків як JSON: [{type:\"text\",content:\"...\"},{type:\"video_embed\",url:\"...\"}]. ПЛЮСИ: atomic-редагування lesson одним UPDATE; додавання нового типу блоку у v2 не потребує schema-migration (зміна тільки в app-валідаторі). МІНУСИ: валідація блоків явно у app-layer (DB не знає про типи); повнотекстовий пошук всередині body вимагає GIN-індексу (спеціальний тип індексу Postgres для пошуку всередині JSON, у 3-5× більше місця і повільніше при записі). НАСЛІДОК: я спавню ADR-0002 з розписом 3 розглянутих варіантів, додаю рядок у §9 ADR-table, схема «jsonb NOT NULL DEFAULT '[]'::jsonb» зафіксована як contract для `sdlc:generate-data-model`."
```

### Why

Користувач — PM, methodist або junior dev, який вперше відкриває репозиторій. Стислі англомовні питання не дають йому ні суті рішення, ні різниці між опціями. Це зриває Socratic-cadence і робить skill придатним лише для senior-ів з повним контекстом. Дослівна цитата фідбеку 2026-05-23: «Треба щоб пояснення були ще більш зрозумілими для людей котрі буквально джуни в розробці».
