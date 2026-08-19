---
name: verify-ui
model: sonnet
effort: medium
agents: []
description: >-
  Use to verify a UI surface's acceptance criteria through a LIVE browser run — open the
  running app, drive the scenario, read the real page state (DOM, computed styles, storage),
  and return a per-AC pass/fail with evidence. This is the browser feedback channel: it catches
  what compiles and "passes the logic" but is visually or behaviourally broken. Triggers on
  "verify ui for {slug}", "verify {story} in the browser", "перевір UI {story}",
  "прокликай {story} у браузері", "verify AC through the UI", "/sdlc-verify-ui {slug-or-story}".
  CLI-first (token-efficient `playwright-cli` in bash, the default for loops/CI); Playwright MCP
  stays available for live stateful debugging. Reads the AC from the feature/story file, never
  invents criteria, never fixes code — it only renders a verdict. Hard-refuses if no dev server
  is reachable.
triggers:
  - /sdlc-verify-ui
  - "verify ui for"
  - "verify in the browser"
  - "перевір UI"
  - "прокликай"
  - "verify AC through the UI"
stage: "util"
---

# Skill: verify-ui (SDLC utility — the browser feedback channel)

`verify-ui` is the **live-run** verification channel for a UI surface. Где детермінований
гейт (типи + тести) безсилий — компілюється, «логіка проходить», а кнопка не клікається, поле
не приймає ввід, відступ з'їхав, стан після перезавантаження губиться — це ловить **тільки**
реальний прогін у браузері. Skill бере acceptance-критерії (AC) фічі/story, проганяє сценарій
проти запущеного застосунку, читає **справжній стан сторінки** і ставить дискретний вердикт
по кожному AC.

Це канал **верифікації результату**, а не написання коду: skill не «лагодить» — він лише
рендерить вердикт із доказом. Фікс — окремий крок (`implement-tasks`).

Поверхня вирішує, чи цей канал доречний: `verify-ui` працює, тільки коли `sad.md`
`target_surfaces` містить `web-frontend` (чи інший UI-зріз) → [`../_shared/surfaces.md`](../_shared/surfaces.md).
Для бекенд-only фічі браузерний канал не дає сигналу — там тести/контракти/логи.

## CLI за замовчуванням, MCP — для живого дебагу

Канонічний інструмент каналу — **Playwright**, але в двох формах:

- **`playwright-cli` (дефолт).** Команди в bash, токен-ефективні: не вантажать у контекст
  величезні схеми інструментів і повні дерева доступності. Це дефолт для циклів і CI, бо
  сценарій зафіксований і його треба дешево прогнати багато разів. Vendor (Microsoft) прямо
  рекомендує CLI для кодинг-агентів.
- **Playwright MCP** — для вузького випадку: жива розвідка зі збереженням стану, коли ще не
  знаєш, що зламано, і агент має клікати й реагувати в реальному часі. Тримати MCP у циклі на
  сотні ітерацій — найшвидший спосіб спалити бюджет токенів.

> `playwright-cli` молодий (pre-1.0, поч. 2026), але first-party і vendor-sanctioned. Перед
> прогоном звір актуальний синтаксис команд (`playwright-cli --help`).

### Встановлення (одноразово)

```bash
npm install -g @playwright/cli@latest   # CLI для агентів
npx playwright install chromium          # браузер
playwright-cli install --skills          # дати агенту «навички» CLI (SKILL.md від Playwright)
```

## Передумова (GATE)

Застосунок має бути піднятий (dev-сервер). Якщо `playwright-cli open <url>` падає на конекті —
**не вигадуй стан**, спочатку підніми сервер (`npm run dev` / `make dev`) і повтори. Без живого
застосунку skill hard-refuse.

## Кроки

1. **Знайти AC.** Прочитай файл фічі/story (`docs/features/<slug>/PRD.md` §5, або `tasks/<story>.md`)
   — витягни блоки Given/When/Then. Перевіряй **тільки** те, що там є.
2. **Відкрити застосунок.** `playwright-cli open <url>` (напр. `http://localhost:5173`).
3. **Зчитати початковий стан.** `playwright-cli snapshot` — повертає не картинку, а текстове
   дерево елементів із рефами (`e21` тощо). Обери елементи, на які посилаються AC.
4. **Відтворити сценарій.** Для кожного AC виконай When через CLI: `click <ref>`, `type <text>`,
   `fill <ref> <text>`, `press <key>`, `select <ref> <val>`. Потім **прочитай реальний стан** під
   Then: `snapshot` (DOM), `eval "<js>"` (обчислені стилі/значення — напр. `getComputedStyle`),
   `localstorage-get <key>` (персистенція), `reload` (чи переживає стан перезавантаження).
5. **Зафіксувати доказ.** `playwright-cli screenshot` зберігає знімок як артефакт прогону.

## Output — дискретний вердикт по AC (evidence-before-assertion)

```
<story> · verify-ui
  AC-1  FAIL — відступ кнопки «Скасувати» 8px, еталон 12px (getComputedStyle padding-x = 8px)
  AC-2  PASS — форма зберігає й закривається; у списку оновлена картка
  AC-3  SKIP — недосяжно, поки AC-1 червоний
Підсумок: FAIL (1/3). Доказ: tmp/<story>-after.png
```

- Кожен FAIL — з **очікуваним vs фактичним** значенням, прочитаним зі сторінки (не «здається»).
- Вердикт прив'язаний до конкретних AC зі story-файлу, не загальне «працює/ні».
- Є посилання на screenshot-доказ.

## Design→code на вході (Figma) — окремий, вхідний канал

Якщо AC посилаються на макет, агент читає **структуру** дизайну через офіційний **Figma Dev Mode
MCP** (дерево вузлів, layout, токени, компоненти) — не пласку картинку. Але це **вхідний** канал
(як агент *читає* дизайн); перевірка *результату* все одно через `verify-ui` у браузері. Тобто
Figma MCP браузерний канал не заміняє, а доповнює.

## Acceptance criteria цього skill-а

- Вердикт по кожному AC зі story/PRD, з фактичним значенням із живого стану сторінки.
- Прогін через `playwright-cli` за замовчуванням (MCP — лише якщо явно потрібен живий дебаг).
- Є screenshot-доказ прогону.

## Anti-patterns

- **Не вигадуй AC** — перевіряй тільки те, що є у story/PRD.
- **Не підміняй браузер юніт-тестом** — суть каналу саме в реальному DOM/поведінці.
- **Не «лагодь» код тут** — skill лише ставить вердикт; фікс — окремий крок (`implement-tasks`).
- **Не рапортуй PASS без прочитаного стану** — «виглядає правильно» без `snapshot`/`eval` — це
  не доказ, а здогад.
- **Не тримай MCP у довгому циклі** заради зручності — це токен-яма; цикл = CLI.

## References

- [`../_shared/surfaces.md`](../_shared/surfaces.md) — таксономія `target_surfaces`; цей канал
  доречний лише для UI-поверхонь.
- [`../_shared/handoff.md`](../_shared/handoff.md) — формат stage-handoff блока.
- [`review-feature`](../review-feature/SKILL.md) — незалежний clean-context рев'юер diff проти
  AC; `verify-ui` — його браузерний помічник на UI-поверхні (рев'юер дивиться diff, verify-ui
  дивиться живий екран).

## Stage handoff

> **verify-ui → implement-tasks / review-feature.** Якщо є FAIL — повертай конкретні AC у
> `implement-tasks` з фактичним vs очікуваним; якщо все PASS на UI-поверхні — передавай у
> `review-feature` для незалежного рев'ю diff. Доказ (screenshot + рядки вердикту) додай до
> `docs/features/<slug>/_review/`.
