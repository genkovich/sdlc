<!-- Format: MADR (Markdown Any Decision Record — формат запису архітектурних рішень). -->

---
status: Accepted                                # Proposed → Accepted → Superseded by NNNN. Цей skill пише Accepted одразу.
owner: "<decision owner — usually Architect>"   # Хто несе відповідальність за рішення
reviewers: []                                   # Хто переглянув ADR перед merge (зазвичай Tech Lead + Security якщо стосується)
updated_at: "<YYYY-MM-DD>"                      # Дата останнього оновлення (для Superseded — дата заміни)
feature_size: M                                 # XS/S/M/L/XL — успадковується з PRD
stage: "04-05"                                  # Стадія SDLC, на якій ADR народився
ticket: "<ticket-id>"                           # Тікет із трекера (Jira/Linear), що тригернув функцію
---

# NNNN — <title in imperative: e.g. "Use sliding window for rate limiting">

<!-- Spawned by sdlc:architecture-design when a decision crosses the blast-radius threshold. -->
<!-- See sdlc/plugin/skills/architecture-design/references/blast-radius-heuristic.md -->
<!-- ВАЖЛИВО: заголовок описує РІШЕННЯ, не проблему. -->
<!-- ✓ "Зберігати урок як таблицю блоків різних типів"  -->
<!-- ✗ "Стратегія зберігання уроку"                     -->

- **Status:** Accepted
- **Date:** <YYYY-MM-DD>
- **Deciders:** <names — usually the Architect + the user during the Socratic walk>

## Context

<2-4 sentences: what is happening, why this decision needs to be made now. Pull from sad.md §3 (Context) + the section that triggered this ADR.>

<!-- Приклад (з 0001-content-storage-strategy.md):                                                              -->
<!-- "PRD §4 говорить: methodist складає урок зі змішаного контенту — текст + відео + картинки.                 -->
<!--  Питання: у якій формі зберігаємо тіло уроку у БД? Це фундаментальне рішення, від нього залежить API,      -->
<!--  форма фронт-редактора, можливість перевпорядкування блоків." (3 речення)                                  -->

## Decision drivers

<bullets — the quality goals / constraints that pushed the choice>

- <e.g. NFR latency p95 ≤ 5 ms (PRD §NFR)>
- <e.g. Multi-tenant isolation requirement (PRD §Constraints)>
- <e.g. Existing Redis cluster — no new infra cost>

<!-- Принцип: кожен буліт — або з PRD §6 NFR, або з §2 SAD Constraints, або з §1 топ-3 якостей. -->
<!-- НЕ вигадуй драйверів — це фільтр від «pet decisions» (рішень з власних уподобань архітектора). -->

## Considered options

<List ALL options that were presented in AskUserQuestion, including the ones the user rejected. One-line summary each.>

1. **<Option A>** — <one sentence describing the option>.
2. **<Option B>** — <one sentence>.
3. **<Option C>** — <one sentence>.

<!-- ВАЖЛИВО: усі опції, які реально розглядалися — включно з тими, що користувач відкинув. -->
<!-- НЕ додавай страшмена (опцію, яку обмеження стеку вже виключають) — це F6-помилка критика. -->

## Decision outcome

**Chosen:** Option <letter or name>. <1-2 sentences rationale — why this option won over the alternatives, referencing the decision drivers above.>

## Consequences

**Positive**
- <e.g. Per-tenant fairness — bursts in tenant A don't starve tenant B>
- <e.g. Reuses existing Redis cluster — no new infra>

**Negative**
- <e.g. ~30% more memory per key vs fixed window>
- <e.g. Counter math is slightly more complex to reason about>

**Neutral**
- <e.g. Migration to fixed window later is possible but requires data backfill>

<!-- Чесний наслідок-лог відрізняється від «забули» тим, що Negative і Neutral заповнені теж, не лише Positive. -->

## Links

<!-- Без цієї секції ADR — файл-сирота. ADR живе у трьох звʼязках з іншими файлами:               -->
<!--   1) угору до PRD (який user story тригернув)                                                  -->
<!--   2) угору до §N SAD (до якої секції прикріплене)                                              -->
<!--   3) у сторону до сусіднього ADR (якщо разом утворюють один договір)                          -->

- PRD: [[../PRD.md]]
- SAD: [[../sad.md]] §<N>
- Related ADR: <[[NNNN-other]] if any>
