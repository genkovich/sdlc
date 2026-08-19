---
name: interview
description: >
  Consolidated 14-phase ideation skill — Socratic interview, autonomous
  competitive research, 3 strategic approaches via parallel sub-agents,
  multi-perspective review (Engineer/Executive/UX), devil's advocate,
  Claude-proposed RICE/Feasibility. Single entry-point for ideation phase.
  Produces idea-brief.md (15 sections, ≤5 pages). Triggers on "raw idea",
  "capture an idea", "interview a feature X", "brief for X", "new feature X",
  "idea brief", "intake feature X", "start new feature", "ideation for {slug}",
  "/sdlc-interview {slug}". Also runs project-level in an empty folder
  (greenfield mode): "new project idea", "greenfield brief", "інтерв'ю нового
  проєкту", "/sdlc-interview" without slug outside a repo — writes docs/idea-brief.md
  for the whole product. Has a depth regulator (easy / medium / hard; easy =
  3-4 checkpoints for a quick pass). Replaces the prior intake + brainstorm + interview
  trio. ADRs are no longer part of this skill — they are spawned inline by
  the architecture-design skill at gate 04-05. Not to be confused with the global `interview` skill
  (stress-testing ideas) — this one is bound to SDLC ideation phase and
  writes an artifact into docs/features/.
---

# Skill: interview (SDLC ideation phase — single entry-point)

Consolidated 14-phase ideation runner. Single entry-point for the ideation phase. Replaces the prior atomic trio `intake` + `brainstorm` + `interview` with one autonomous Claude-driven protocol. Output: a single `docs/features/<slug>/idea-brief.md` with 15 sections (≤5 pages), no separate `brainstorm.md` / `initiatives.md`.

## Why this consolidation

Single entry-point for ideation. Replaces intake + brainstorm + interview. Autonomous Claude-driven research (competitive analysis, strategic approaches, multi-perspective review, devil's advocate, RICE/Feasibility proposals) with user confirms via AskUserQuestion. No more user-input RICE numbers («calculator game»). No more separate brainstorm.md / initiatives.md. ADR is not a gate-1 concern — it moves to gate 3 (after sad.md (architecture-design) §Trade-offs); the ideation phase stays pure product.

## Owner

Idea author (PM / Eng / CTO / anyone). Tech Lead joins at multi-perspective review (phase 6) if asked.

## When to use

- «capture an idea <slug>», «new brief for <feature>», «raw idea for <feature>».
- «interview a feature <slug>», «ideation for <slug>», «brief for <feature>».
- «intake feature <slug>», «start new feature with CONTEXT», «full intake for <slug>».
- `/sdlc-interview <slug>` as explicit invocation.
- **Greenfield**: user is in an empty folder (no `.git`, no `docs/`) with a new product idea — «new project idea», «бриф нового продукту». Runs project-level, see «Greenfield mode» below.
- User drops a raw idea in prose and asks «format this per SDLC» / «run ideation for <slug>».
- Glossary-aware: on start the skill reads `CONTEXT.md` if it exists (repo root or `docs/features/<slug>/`), keeps the glossary as session state, and triggers `sdlc:fix-term` inline for new domain terms.
- Skip if `docs/features/<slug>/idea-brief.md` already exists with `status: Confirmed` and is fresh (≤2 weeks) — update it first, don't rewrite.

## Inputs

- `<slug>` — kebab-case, short (`rate-limiting`, `goals-tracking`). If the user didn't give one — suggest 2-3 options based on the idea.
- (Optional) prior notes / links / ticket the user already has.

## Depth regulator (first checkpoint)

Перше AskUserQuestion кожного запуску — глибина інтерв'ю. Записується у frontmatter brief-а (`depth:`).

- **easy** — 3–4 чекпойнти, швидкий прохід: Phase 1 (ідея), Phase 2 одним батчем (2–3 питання: користувач/біль · критерій успіху · скоуп), Phases 9–11 злиті в один підсумковий confirm (Claude пропонує RICE + рекомендацію разом). Phases 4–8 Claude проходить сам без sub-agents: 1–2 швидкі пошуки для §6, три approaches по одному абзацу, devil's advocate — власний список з 3–5 ризиків. Всі 15 секцій заповнюються, але компактно.
- **medium** (default) — повний 14-фазний протокол нижче, як є.
- **hard** — повний протокол + додатковий Socratic-батч у Phase 2 і ширший §6 (5+ конкурентів).

Easy не скасовує чесність чекпойнтів: його 3–4 AskUserQuestion — справжні, фабрикація відповідей недопустима так само, як у medium/hard.

## Greenfield mode (project-level brief)

**Детект:** поточна тека порожня, або без `.git` і без `docs/` — це новий проєкт, не фіча в наявному репо. Інакше — feature mode (протокол нижче без змін).

Відмінності greenfield від feature mode:

- **Артефакт:** `docs/idea-brief.md` у корені теки (без `docs/features/<slug>/`). Той самий 15-секційний шаблон; `<slug>` всюди означає назву продукту (kebab-case — стане slug-ом скафолда).
- **Phase 10 Feasibility:** репо ще нема — сканувати нічого. Claude чесно базує ☑/☐ на відповідях про команду/стек («greenfield — оцінка від команди, не від репо») і питає користувача, як завжди.
- **Phase 14 handoff:** наступний крок не `sdlc:write-prd`, а **`sdlc:scaffold`** — матеріалізація проєкту з темплейта; brief поїде в нове репо разом зі скафолдом. Commit не пропонується (git-репо ще не існує — його створить scaffold).
- **CONTEXT.md / glossary:** якщо файлу нема — pending-терміни лишаються в brief §15 Open questions, fix-term не викликається.

## Mode handling

**This skill is planning-mode-native.** Phases 0-11 виконуються повністю у read-only режимі (Read, WebSearch, Agent, AskUserQuestion). Лише на переході 11 → 12 викликається `ExitPlanMode` із synthesized planом, після чого Phase 12 копіює template і пише `idea-brief.md` на диск.

**Why:** AskUserQuestion checkpoints у Phases 1, 2, 9, 10, 11 — це не «clarifying questions», а **обовʼязковий data-input protocol**. Користувач має фактично зайти у глибину ідеї; без цього artifact = reconstruction з памʼяті моделі, не interview.

**Auto Mode override:** якщо у сесії активний `Auto Mode` system-reminder, він **не** скасовує AskUserQuestion-checkpoints у цьому skill. Auto Mode стосується «pause to check whether I should proceed»-моментів між фазами, не data input. Фабрикація raw idea, Socratic answers, RICE/Feasibility/Recommendation confirms = nullify whole interview.

## AskUserQuestion style — junior-friendly Ukrainian (mandatory from 2026-05-23)

Кожен `AskUserQuestion` у цьому skill-у (Phases 1, 2, 9, 10, 11) формулюється так, щоб **PM без технічного background або junior-розробник першого року** міг відповісти без помічника поряд.

**Mandatory shape:**

1. **Українська мова всюди** — labels + descriptions. Технічні ідентифікатори (RICE, R/I/C/E score, Feasibility ☑/☐, Approach A/B/C) залишаються англійською — це назви; але «дії» опцій — українською («Прийняти Approach C», «Підкорегувати E нижче», «Позначити TBD», «Confirm + перейти до Phase 11»).

2. **`question` поле — 3-4 речення** з трьох блоків:
   - **КОНТЕКСТ** — звідки взялося це питання, на якій Phase ми зараз, що уже зібрано (1-line recap)
   - **ЧОМУ ВАЖЛИВО** — що зривається, якщо відповідь буде неправильною (напр. «RICE без розуміння Effort = decision based on wishful thinking; Phase 11 буде з кривим foundation»)
   - **ЯКА ДУМКА ПОТРІБНА** — на що дивитися перед вибором; чи треба перечитати prior phase output

3. **Option `description` — 3-5 речень** з трьох елементів:
   - **Що технічно станеться**: який рядок у idea-brief зміниться, які later phases на цю відповідь впливають
   - **Що опція означає простими словами** — без жаргону:
     - Не «RICE score 80, Approach C» → «RICE-формула (Reach × Impact × Confidence / Effort) дала 80 для варіанту C; це значить, що C виглядає більш виправданим за ресурсами, ніж A (60) або B (45) — але це Claude-прогноз, не facts»
     - Не «Feasibility 3/3 ☑» → «всі три блоки feasibility (Skills, Time, Tech) Claude позначив як «підтверджено» — це значить, що у команди є експертиза, у release-windows є місце, і tech-stack не блокує. Якщо щось з цього TBD — Phase 11 Recommendation буде з warning»
     - Не «strategic vector» → «головний напрям, у якому ми йдемо: напр., «consolidate content delivery всередину BeerLMS» — все, що suggests розширення scope поза цей напрям, у Phase 8-9 буде flagged як scope creep»
   - **Hidden trade-off** — якщо опція має наслідок, який junior міг би не побачити (напр. «Mark recommendation as TBD» → «всі downstream skill-и (write-prd, architecture-design) hard-refuse поки status не Confirmed — це блокує всю SDLC-pipeline для цієї фічі») — згадати це прямо у description

**Заборонено:** стислі англомовні labels («Confirm», «Adjust», «TBD»); однорядкові descriptions; технічні терміни без розшифровки; trade-off-и заховані у follow-up.

**Why:** PM-аудиторія цього skill-у працює з product-мовою, не з engineering-жаргоном; junior-аудиторія не має повного контексту про SDLC-pipeline. Дослівна цитата фідбеку 2026-05-23: «Треба щоб пояснення були ще більш зрозумілими для людей котрі буквально джуни в розробці» (контекст — sdlc:architecture-design, з вимогою «закласти не тільки в архітектуру а і в бриф ідею і в врайт прд»). Цю вимогу віддзеркалено в `sdlc:architecture-design/references/ask-examples.md` і `sdlc:write-prd/references/ask-examples.md`.

**Planning mode compatibility:** оскільки усі Write-операції зосереджені у Phase 12 (post-ExitPlanMode), skill коректно стартує у будь-якому permission mode (default / acceptEdits / plan / Auto). Якщо ExitPlanMode недоступний (тобто сесія була запущена не в plan mode) — Phase 12 виконується одразу після Phase 11, без переходу.

## Protocol

**14 phases. Phases 0-11 read-only. Phase 11.5 = ExitPlanMode. Phases 12-14 execute writes + self-check + commit propose.**

### 0. Pre-plan setup (read-only)

- **Read** `./templates/idea-brief.md` — завантажити skeleton у session memory (NO copy yet).
- **Read** `CONTEXT.md` (root and `docs/features/<slug>/` if exists) — завантажити `## Glossary` у session state.
- **Verify** `docs/features/<slug>/idea-brief.md` does not exist with `status: Confirmed` (else: skip, update existing).
- **NO Write / Edit / mkdir.** Setup стає одним з steps плану, який буде виконано у Phase 12.

### 0.25. Depth checkpoint (AskUserQuestion — mandatory)

Одне питання: глибина (див. «Depth regulator»). easy → скорочений маршрут фаз; medium/hard → повний. У greenfield mode це ж питання підтверджує назву продукту (kebab-case), якщо користувач її ще не дав.

### 1. Idea capture (AskUserQuestion — mandatory)

One AskUserQuestion для raw paragraph: «опиши ідею в 1-3 реченнях своїми словами». Persist verbatim у session memory як §1 Raw idea draft. Не редагувати — це baseline.

### 2. Socratic deep dive (AskUserQuestion — mandatory)

Pick 3-5 питань з 5 категорій based on idea-shape:
- **Problem clarity** (що саме болить, для кого, як часто).
- **Solution validation** (чому саме це рішення, що пробували раніше).
- **Success criteria** (що означає «спрацювало» — конкретний metric).
- **Constraints** (timeline, budget, team capacity, dependencies).
- **Strategic fit** (як це лягає у roadmap / OKR / business outcome).

Delivery: AskUserQuestion батчами по 2-3 (не all-at-once).

### 3. Glossary capture (deferred fix-term)

На кожному новому domain-слові у відповідях користувача — додати term до session-state list `pending_glossary_terms`. **НЕ викликати** `sdlc:fix-term` зараз — це писало б у CONTEXT.md, що недопустимо у planning mode. Skip generic tech terms (HTTP, JSON, queue, cache, database). Terms apply-ються у Phase 12 (post-ExitPlanMode) перед Write idea-brief.md.

### 4. Competitive research (Claude-driven, read-only)

Claude автономно:
- WebSearch + `mcp__plugin_qmd_qmd__query` для 3-5 конкурентів / adjacent solutions.
- Формує таблицю: **Product · URL · Features · Value (1-5 per feature) · Gap** у session memory.
- Кожен рядок з footnote: date and search query used.
- Якщо internal tool без market — `N/A — internal tool` з reason.

NO user input у цій фазі — Claude робить research, користувач лише review після.

### 5. Strategic approaches (3 паралельні Agent.tool calls, read-only)

Shared prompt template, 3 personas виконуються паралельно через окремі sub-agents:
- **Variant-A (Simplicity):** найкоротший шлях, MVP-style, мінімум moving parts.
- **Variant-B (Differentiation):** wow-factor / strategic moat / unique angle.
- **Variant-C (Balanced):** trade-off між A та B.

Кожен sub-agent повертає 1-paragraph approach з:
- **Name** (3-5 word).
- **Thesis** (1 sentence, product language — NO tech terms like Redis/Postgres/Kafka).
- **For whom** (which segment from §3 Users).
- **Outcome metric** (1 KPI: baseline → target).
- **Key trade-off** (1 line).
- **Effort signal**: S / M / L.

### 6. Multi-perspective review (3 паралельні Agent.tool calls, read-only)

Three personas виконуються паралельно через sub-agents, кожен бачить усі 3 approaches з §5:
- **Engineer** — concerns / risks / blockers. Explicitly told у prompt: «no library/DB names — abstract concerns only (latency, throughput, complexity, integration surface)».
- **Executive** — business value / opportunity cost / strategic fit.
- **UX-researcher** — user friction / discoverability / onboarding curve.

Кожен повертає 3-5 bullets з concerns / value / risks для **кожного** з 3 approaches.

Build §8 Synthesis matrix (3 personas × 3 approaches) з 6-word justifications per cell (+/0/-) у session memory.

### 7. Trade-offs + edge cases (synthesis, read-only)

Claude synthesizes у session memory (no user input — review/edit only):
- Trade-offs per approach: pros / cons table.
- 5-8 edge cases that any approach must handle (data, integrations, failure modes, ops).

### 8. Devil's advocate (1 Agent.tool call з clean context, read-only)

Spawn 1 sub-agent з чистим контекстом (NO upstream session memory), prompt: «знайди як це може провалитись. 5-10 attack vectors з production signals (що саме зламається, як це проявиться у monitoring/customer churn/incident)».

Найкритичніший attack vector → reserved для §10 Risks. Решта — для §9 Edge cases.

### 9. Claude-proposed RICE (AskUserQuestion — mandatory)

Claude обчислює R/I/C/E з upstream sections:
- **Reach** ← §3 Users (кількість users / quarter affected).
- **Impact** ← §2 Problem severity + Executive perspective bullets.
- **Confidence** ← кількість TBDs / open questions; багато unresolved → 0.5; всі факти конкретні → 1.0.
- **Effort** ← Effort signal з §7 approaches (S = 1-2 person-weeks, M = 3-5, L = 6-12).

Compute `R × I × C / E`. AskUserQuestion per number (4 окремі checkpoints або 1 multiSelect батч) з опціями: `Confirm N` / `Adjust higher` / `Adjust lower` / `Mark TBD`. Rationale у idea-brief цитує upstream секцію.

### 10. Claude-proposed Feasibility (read-only repo scan + AskUserQuestion — mandatory)

Claude scans the project repo (read-only `find`/`ls`/`Glob` over feature dirs `docs/features/`, `src/`, `app/`, `pkg/`, `services/`, project-specific paths) для adjacent features which already shipped similar tech / workflow.

Proposes 3 checkboxes:
- **Tech** ☑/☐ — з обґрунтуванням («similar to <existing feature> in <module>»).
- **Skills** ☑/☐ — з обґрунтуванням («team already shipped <X>, same skill applies»).
- **Time** ☑/☐ — з обґрунтуванням («similar feature <X> shipped in <N> weeks»).

AskUserQuestion per checkbox (3 окремі або 1 multiSelect батч): `Confirm ☑` / `Flip to ☐ — <reason>` / `TBD`.

### 11. Recommendation synthesis (AskUserQuestion — mandatory)

Claude picks один з 3 approaches з §5 + writes 3-5 sentence rationale у session memory.

Rationale MUST explicitly cite:
- RICE score from §11.
- Feasibility state from §12.
- ≥1 multi-perspective synthesis matrix cell from §8.
- ≥1 competitive gap from §6.

AskUserQuestion для user confirm: `Accept recommendation` / `Pick different approach` / `Mark recommendation as TBD`.

### 11.5. ExitPlanMode handoff (planning → execute)

Усе вище — session memory only. Тепер skill **викликає `ExitPlanMode`** з planом який містить:

1. Create directory `docs/features/<slug>/` (if absent).
2. Copy template `./templates/idea-brief.md` → `docs/features/<slug>/idea-brief.md`.
3. Apply pending glossary terms (Phase 3 list) via `sdlc:fix-term` to `CONTEXT.md`.
4. Fill 15 sections + Related + DoD self-check у новому файлі з усього session memory (Phases 1-11).
5. Update frontmatter: `status: Confirmed`, `value_score.{rice,state,confirmed_at}`, `feasibility_state: confirmed`.
6. Run Phase 13 self-check (regex, length, citations).
7. Propose commit + next owner.

Якщо ExitPlanMode tool недоступний (skill стартував не у plan mode) — пропустити цей step і виконати Phase 12 напряму. План у session memory залишається тим самим.

### 12. Execute: fill expanded idea-brief

Після `ExitPlanMode` (або одразу, якщо plan mode не активний):

- **mkdir** `docs/features/<slug>/` if absent.
- **Copy** template → `docs/features/<slug>/idea-brief.md`.
- **Apply** pending glossary terms (call `sdlc:fix-term` for each, якщо що).
- **Edit/Write** усі секції 1-15 + Related + DoD self-check з session memory. Update frontmatter:
  - `status: Confirmed`
  - `value_score.rice: <N>`, `value_score.state: confirmed`, `value_score.confirmed_at: <today YYYY-MM-DD>`
  - `feasibility_state: confirmed`
  - `updated_at: <today>`

Parked approaches (2 non-recommended з §5) — у §14 з reason + revisit trigger.

### 13. Self-check vs DoD

Run all checks (Read + grep over the file just written):
- **15 sections present.** Все 1-15 + Related + DoD self-check filled.
- **No anti-pattern terms у body.** Regex check (excluding DoD self-check meta-line): `\b(Postgres|Redis|Kafka|MySQL|SM-2|FSRS|Leitner|SQLAlchemy|gorm|JSONB)\b` + `p99`. **Word-boundary важливий**: `chi` як substring у «architecture» — false positive; додати `\b`.
- **Length ≤ 5 pages** (~2200 words ±10%). If over — compress §5 Approaches paragraphs and §6 Competitive table.
- **Rationale citations.** §13 Recommendation cites §6 (1 gap) + §8 (1 cell) + §11 (RICE) + §12 (Feasibility).

If any check fails → identify offending section, re-Edit it, then re-check.

### 14. Propose commit + next owner

Suggest commit (do not auto-execute):

```
01: idea-brief for <slug>
```

Next owner: PM + Tech Lead → `sdlc:write-prd <slug>` (gate тепер з idea-brief.md `status: Confirmed`).

**Greenfield mode:** замість write-prd наступний крок — `sdlc:scaffold` (матеріалізує проєкт з темплейта і забирає `docs/idea-brief.md` у нове репо); commit не пропонується, git-репо створить scaffold.

ADR (`sdlc:architecture-design`) НЕ викликається на gate 1 — це gate 3 concern (after sad.md (architecture-design) §Trade-offs). Якщо рекомендація з §13 виглядає як hard-to-reverse technical choice — note that у §15 Open questions, але don't open ADR thread here.

## Questions for discussion

- Який слаг — kebab-case, short, no date?
- Який сегмент користувачів страждає найбільше від цієї проблеми?
- Чому саме зараз — який trigger (incident / contract / deadline)?
- Який метрик ми використовуємо щоб виміряти, що це спрацювало?
- Які з 3 strategic approaches ближче до того, як команда зазвичай вирішує подібні задачі?
- Чи погоджуєшся з Claude-proposed RICE numbers — чи треба коригувати?
- Чи всі 3 Feasibility checkboxes реально закриті, чи десь є unknown?

## Definition of Done

- `docs/features/<slug>/idea-brief.md` created and committed.
- All 15 sections filled (no empty H2, `<!-- TBD -->` allowed where honestly missing).
- No anti-pattern tech terms у тілі (verified by internal regex check, word-boundaries on).
- Length ≤ 5 pages (~2200 words ±10%).
- Frontmatter `status: Confirmed`, `value_score.state: confirmed`, `feasibility_state: confirmed`, `confirmed_at: <date>`.
- §13 Recommendation rationale cites RICE (§11) + Feasibility (§12) + ≥1 multi-perspective cell (§8) + ≥1 competitive gap (§6).
- **AskUserQuestion checkpoints actually fired** у Phases 1, 2, 9, 10, 11 (verify через user-message trail). Якщо хоч один був фабрикований → artifact NOT DoD-valid.
- Next-stage owner assigned (PM + Tech Lead → `sdlc:write-prd`).

## Anti-patterns

- **Inventing competitors because «we need to write something».** Better `N/A — internal tool` with reason than fake research. Competitors = «all the same» without links — that's not research, that's laziness. Phase 4 must produce real URLs + features + value ratings.
- **User-input RICE («calculator game»).** Old skill asked user for Reach/Impact/Confidence/Effort — user has no grounding to answer. New flow: Claude proposes from upstream sections (Users → Reach, Executive perspective → Impact, TBDs → Confidence, Effort signal → Effort). User only confirms or adjusts.
- **Tech terms in idea-brief body** (Postgres, Redis, Kafka, SM-2, FSRS, p99 latency, JSONB). This is a PRODUCT brief. Tech lives у PRD §6 + sad.md (architecture-design) + ADR (gate 3+). Phase 13 self-check enforces this.
- **Single approach in §5.** Strategic approaches MUST be 3 (Simplicity / Differentiation / Balanced). One approach = decision already taken, nothing to evaluate.
- **Skip multi-perspective review.** Engineer-only view → blind to business / UX risks. Executive-only view → blind to implementation cost. Need all 3 perspectives in §6 to balance.
- **Devil's advocate from same session context.** Phase 8 MUST spawn sub-agent з clean context, otherwise it's biased by all the optimism upstream.
- **Skip Feasibility repo scan.** Phase 10 must do `find`/`ls` over feature dirs and cite adjacent shipped features. «Tech: ☑ — we know how» without citation = guess.
- **Recommendation без rationale citing 4 upstream sections.** Phase 11 rationale MUST cite §6 (competitive gap), §8 (multi-perspective cell), §11 (RICE), §12 (Feasibility). Otherwise it's «I feel like A».
- **Propose ADR at end of phase 14.** ADR moves to gate 3 (after sad.md (architecture-design)). Gate 1 is pure product — no tech locks-in.
- **Brainstorm-style transcript dump.** §14 Parked & rejected is structured (table with status / reason / revisit trigger), not raw chat log.
- **Solution-mode prose in §2 Problem.** «We need to add Redis» → wrong section. §2 is the problem only; solutions live у §7 Approaches.
- **Fabricating user answers under Auto Mode.** `Auto Mode Active` system-reminder каже «work without stopping for clarifying questions» — це стосується pause-to-check моментів, а не in-flow AskUserQuestion checkpoints цього skill. Phases 1, 2, 9, 10, 11 MUST fire real AskUserQuestion-и; генерувати raw idea / Socratic answers / RICE confirms / Feasibility confirms / recommendation accept без user-input = reconstruction artifact, не interview. Якщо AskUserQuestion відкинуто через permission denial — зупинитись і повідомити користувача, не обходити.
- **Writing files inside planning mode.** Phases 0-11 read-only. Якщо skill стартував у plan mode і ти спробуєш Write/Edit/mkdir раніше ніж ExitPlanMode (Phase 11.5) — permission deny. Тримай весь artifact у session memory до Phase 12.

## Template

→ [./templates/idea-brief.md](./templates/idea-brief.md)

## Example invocation

> **User:** «interview a feature: 3 клієнти за тиждень поскаржилися на 429s через сусідів, треба per-user rate limit»
>
> **Skill behavior (planning-mode-friendly flow):**
>
> **— Plan mode (read-only) —**
> 1. **Phase 0** — suggests slug `rate-limiting-per-user`. User confirms. **Read** template і root `CONTEXT.md`. NO copy yet.
> 2. **Phase 1** — AskUserQuestion: «опиши ідею в 1-3 реченнях». Captures raw paragraph verbatim у session memory як §1 draft.
> 3. **Phase 2** — Socratic batch 1 (AskUserQuestion): «який сегмент клієнтів?» «як часто це б'є?» Batch 2 (AskUserQuestion): «що пробували раніше?» «що означає 'спрацювало' — який метрик?»
> 4. **Phase 3** — у відповідях з'явився термін «tenant» → додається до `pending_glossary_terms` (fix-term викликається у Phase 12, бо CONTEXT.md write).
> 5. **Phase 4** — Claude робить WebSearch: Kong per-consumer, Tyk, AWS API Gateway throttling, Cloudflare rate-limit. Будує §6 таблицю у session memory.
> 6. **Phase 5** — 3 паралельні sub-agents (single message):
>    - A (Simplicity): «Per-tenant request quota at edge proxy» — fastest, generic, S effort.
>    - B (Differentiation): «Adaptive per-tenant quota based on plan-tier» — pricing leverage, L effort.
>    - C (Balanced): «Static per-tenant quota з self-serve config» — M effort, customer can tweak.
> 7. **Phase 6** — 3 sub-agents (Engineer / Executive / UX) review усі 3 паралельно. Engineer abstract (no Redis/nginx). Synthesis matrix у session memory.
> 8. **Phase 7** — Claude synthesizes trade-offs + 6 edge cases у session memory.
> 9. **Phase 8** — sub-agent з clean context: «how does this fail?» Returns 7 attack vectors. Top → reserved для §10 Risks.
> 10. **Phase 9** — Claude proposes RICE: R=200, I=2, C=0.8, E=3 → 107. AskUserQuestion per number; user adjusts Effort to 4 → Score = 80.
> 11. **Phase 10** — Claude scans repo (read-only): finds adjacent `usage-metering`. Proposes 3 ☑. AskUserQuestion per checkbox; user confirms all 3.
> 12. **Phase 11** — Claude picks **Approach C**. Rationale cites: RICE=80, Feasibility 3/3 ☑, Engineer bullet, Kong gap. AskUserQuestion: user accepts.
>
> **— ExitPlanMode handoff —**
> 13. **Phase 11.5** — `ExitPlanMode` із plan: «create dir, copy template, apply fix-term tenant, fill 15 sections, run self-check, propose commit».
>
> **— Execute (post-plan) —**
> 14. **Phase 12** — `mkdir docs/features/rate-limiting-per-user/`, copy template, `sdlc:fix-term tenant`, Write idea-brief.md з усіма секціями. Frontmatter `status: Confirmed`, `confirmed_at: 2026-05-21`.
> 15. **Phase 13** — self-check: 15 sections ✓, no Postgres/Redis у body ✓, 4.2 pages ✓, citations ✓.
> 16. **Phase 14** — Commit message proposed: `01: idea-brief for rate-limiting-per-user` (user executes). Next: PM + Tech Lead → `sdlc:write-prd rate-limiting-per-user`.
