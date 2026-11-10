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
  "прокликай {story} у браузері", "verify AC through the UI", "/sdlc:verify-ui {slug-or-story}".
  CLI-first (token-efficient `playwright-cli` in bash, the default for loops/CI); Playwright MCP
  stays available for live stateful debugging. Reads the criteria from every source present —
  PRD §5 or a task file, design-spec.md §16, and every state in the screens.md tables (with the
  exported PNG of each state as the mockup reference); never invents criteria, never fixes
  code — it only renders a verdict, written to docs/features/{slug}/_review/verify-ui-<date>.md.
  Hard-refuses if no dev server is reachable.
triggers:
  - /sdlc:verify-ui
  - "verify ui for"
  - "verify in the browser"
  - "перевір UI"
  - "прокликай"
  - "verify AC through the UI"
stage: "util"
---

# Skill: verify-ui (SDLC utility — the browser feedback channel)

`verify-ui` is the **live-run** verification channel for a UI surface. Там, де детермінований
гейт (типи + тести) безсилий — компілюється, «логіка проходить», а кнопка не клікається, поле
не приймає ввід, відступ з'їхав, стан після перезавантаження губиться — це ловить **тільки**
реальний прогін у браузері. Skill бере acceptance-критерії (AC) фічі/story, проганяє сценарій
проти запущеного застосунку, читає **справжній стан сторінки** і ставить дискретний вердикт
по кожному AC.

Це канал **верифікації результату**, а не написання коду: skill не «лагодить» — він лише
рендерить вердикт із доказом. Фікс — окремий крок (`implement-tasks`).

Поверхня вирішує, чи цей канал доречний: `verify-ui` працює, коли `sad.md`
`target_surfaces` містить `web-frontend` (чи інший UI-зріз) → [`../_shared/surfaces.md`](../_shared/surfaces.md),
**або**, коли `sad.md` ще немає (дизайн-лінія без PRD/SAD, модуль 5), у фічі є `screens.md` чи
`design-spec.md` → [`../_shared/design-line.md`](../_shared/design-line.md).
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
npm install -g @playwright/cli@latest
playwright-cli install-browser chrome   # лише якщо open каже: Browser "chrome" is not installed
playwright-cli install --skills          # необовʼязково: «навички» CLI для агента (SKILL.md від Playwright)
```

`open` за замовчуванням бере системний Google Chrome (канал `chrome`); якщо його нема, CLI сам
друкує команду встановлення, це рядок 2.

## Передумова (GATE)

Застосунок має бути піднятий (dev-сервер). Якщо `playwright-cli open <url>` не може підʼєднатися —
**не вигадуй стан**, спочатку підніми сервер (`npm run dev` / `make dev`) і повтори. Без живого
застосунку skill hard-refuse.

## Кроки

1. **Зібрати критерії з усіх джерел, що є** (не лише з першого):
   - `docs/features/<slug>/PRD.md` §5 (Given/When/Then) або `tasks/<story>.md`, якщо є;
   - `docs/features/<slug>/design-spec.md` §16: рядки DoD шарів Behavior / States / Responsive /
     Accessibility / Live evidence, з їхніми `BR-NN`;
   - `docs/features/<slug>/screens.md`: кожен стан кожного `SCR-NN` = одна перевірка (дійти до
     стану, прочитати DOM, звірити компоненти й текст з таблицею). Імена станів за словником
     [`../_shared/design-line.md`](../_shared/design-line.md) §3: шість класів плюс названі стани
     з гілок флоу (`error-undelivered`, `ended`). Рядок `N/A: <reason>` не перевірка: такого стану
     нема, у вердикт він не йде.

   Як відкрити кожен стан у запущеному застосунку, бери з рядка «State access» у §Source
   `screens.md` (URL-параметр, перемикач фікстури, тестовий акаунт). Стан, до якого не дійти ні
   звичайними діями в UI, ні цим способом, отримує SKIP із причиною; стан не вигадуємо і не
   підробляємо.

   Коли кілька джерел описують одне й те саме, це один рядок вердикту з усіма id
   (`AC-03 · DOD-04 · SCR-02 error-undelivered`). Перелічи у звіті взяті джерела. Перевіряй
   **тільки** те, що в них є.
2. **Відкрити застосунок.** `playwright-cli open <url>` (напр. `http://localhost:5173`).
3. **Зчитати початковий стан.** `playwright-cli snapshot` — повертає не картинку, а текстове
   дерево елементів із рефами (`e21` тощо). Обери елементи, на які посилаються AC.
4. **Відтворити сценарій.** Для кожного AC виконай When через CLI: `click <ref>`, `type <text>`,
   `fill <ref> <text>`, `press <key>`, `select <ref> <val>`. Потім **прочитай реальний стан** під
   Then: `snapshot` (DOM), `eval "<js>"` (обчислені стилі/значення — напр. `getComputedStyle`),
   `localstorage-get <key>` (персистенція), `reload` (чи переживає стан перезавантаження).
5. **Зафіксувати доказ.** `playwright-cli screenshot` зберігає знімок як артефакт прогону — у
   `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/`.
6. **Звірка з макетом (якщо є PNG).** Коли `screens.md` для перевіреного стану має PNG
   (`docs/features/<slug>/screens/SCR-NN-<state>.png`), зроби знімок живої сторінки в тому самому
   стані й viewport і постав обидва шляхи в рядок вердикту. Вердикт і далі визначається з прочитаного
   стану сторінки та таблиці станів (компоненти, текст, наявність стану), не з піксельного
   порівняння картинок. Нема PNG (code-mode) → крок пропускається.
7. **Записати вердикт у файл.** `mkdir -p docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/`
   і запиши блок вердикту (формат нижче) у `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md`:
   джерело критеріїв, рядок на кожну перевірку, шляхи до знімків з кроку 5 і PNG з кроку 6,
   підсумок. Перевір `test -s` (файл є і не порожній) на сам звіт і на кожен знімок, на який він посилається. Повторний
   прогін того ж дня перезаписує файл. У чат іде той самий блок, але файл обовʼязковий: без нього
   прогону не було.

## Output — дискретний вердикт по AC (evidence-before-assertion)

```
<story> · verify-ui · джерела критеріїв: PRD §5 · design-spec §16 · screens.md
  AC-1  FAIL — відступ кнопки «Скасувати» 8px, еталон 12px (getComputedStyle padding-x = 8px)
  AC-2  PASS — форма зберігає й закривається; у списку оновлена картка
  AC-3  SKIP — недосяжно, поки AC-1 червоний
  DOD-04 · SCR-02 empty  PASS — є EmptyState і CTA «Написати першим»; макет: screens/SCR-02-empty.png · живий: _review/verify-ui-<date>/SCR-02-empty.png
Підсумок: FAIL — 2 PASS · 1 FAIL · 1 SKIP. Звіт: docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md
```

- **SKIP не прохід.** Підсумок PASS лише тоді, коли нема жодного FAIL і жодного SKIP; інакше
  FAIL з лічильниками. Кожен рядок SKIP називає, що заблокувало (недосяжний стан, нема способу
  відкрити його в «State access», червоний попередній AC).
- Кожен FAIL — з **очікуваним vs фактичним** значенням, прочитаним зі сторінки (не «здається»).
- Вердикт прив'язаний до конкретних AC зі story-файлу, не загальне «працює/ні».
- Є посилання на screenshot-доказ.
- Звіт записано в `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md`, знімки поруч у
  `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/`.

## Design→code на вході (Figma) — окремий, вхідний канал

Якщо AC посилаються на макет, агент читає **структуру** дизайну через офіційний **Figma Dev Mode
MCP** (дерево вузлів, layout, токени, компоненти) — не пласку картинку. Але це **вхідний** канал
(як агент *читає* дизайн); перевірка *результату* все одно через `verify-ui` у браузері. Тобто
Figma MCP браузерний канал не заміняє, а доповнює.

## Acceptance criteria цього skill-а

- Вердикт по кожному AC зі story/PRD, з фактичним значенням із живого стану сторінки.
- Підсумок PASS лише без FAIL і без SKIP; кожен SKIP названо з причиною.
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
> `implement-tasks` з фактичним vs очікуваним; SKIP теж повертається в код (добудувати спосіб
> дійти до стану, «State access») і прогін повторюється; якщо все PASS на UI-поверхні — передавай у
> `review-feature` для незалежного рев'ю diff. Доказ (рядки вердикту + screenshot) — у
> `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>.md` і теці
> `docs/features/<slug>/_review/verify-ui-<YYYY-MM-DD>/`. У дизайн-лінії без PRD (модуль 5) все PASS
> означає, що фіча закрита; FAIL повертається в код за таблицею станів `screens.md`.
