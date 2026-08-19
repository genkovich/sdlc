---
name: user-documentation
model: sonnet
effort: medium
agents: [explorer, doc-flow]
description: >-
  Use to generate END-USER documentation for a LIVE web application: Playwright walks the app,
  captures state screenshots (optional screencast replays), and clean-context doc-flow subagents
  write one flow guide each in the reference style, finished with a linked User Guide index.
  Detects the target automatically (Obsidian vault → wikilink embeds, repo docs/ → markdown
  embeds). Triggers on "generate user documentation", "document the app flows", "user guide from
  the live app", "згенеруй користувацьку документацію", "задокументуй флоу застосунку",
  "юзер-гайд по застосунку", "/sdlc-user-documentation <target-dir>". Hard-refuses if no dev
  server is reachable or playwright-cli is not installed.
triggers:
  - /sdlc-user-documentation
  - "generate user documentation"
  - "document the app flows"
  - "user guide from the live app"
  - "згенеруй користувацьку документацію"
  - "задокументуй флоу"
stage: "util"
---

# Skill: user-documentation (cross-cutting — живий застосунок → користувацька документація)

Генерує **користувацьку** (не dev) документацію з живого веб-застосунку: інвентаризація флоу →
детермінований прогін кожного флоу в браузері з журналом дій і скріншотами станів → окремий
clean-context агент пише один flow-документ строго з журналу → тонкий User Guide індекс з лінками
на всі флоу. Опційно — скринкасти через реплей журналу. Джерело правди для стилю —
[`./references/style-guide.md`](./references/style-guide.md); для відтворюваності —
[`./references/determinism.md`](./references/determinism.md).

Браузерний канал — **`playwright-cli`** (канон плагіна, див. `verify-ui`): токен-ефективний CLI
для циклів. Playwright MCP у пайплайні — задокументований anti-pattern.

**Owner:** батько-оркестратор (цей skill) володіє манифестом, гейтом, індексом і когерентністю;
кожен флоу цілком (браузер + текст) належить одному агенту `sdlc:doc-flow`.

## When to use

- Продукт має UI, який уже працює на dev/staging, і потрібен user guide «як користуватись» —
  з реальними скріншотами, а не з уяви.
- Оновлення документації після відчутних UI-змін (перегенерація — той самий протокол).
- НЕ для dev-доки (architecture/API — це backbone-стадії), НЕ для статичних сайтів без флоу.

## Inputs

```
/sdlc-user-documentation <target-dir> [--flows a,b,c] [--video] [--base-url URL] [--embed wikilink|markdown]
```

- `<target-dir>` — тека, куди лягають документи (vault-тека або `docs/user-guide/` репо).
- `--flows` — явний список слагів; без нього список будується інвентаризацією (крок 4).
- `--video` — після доків згенерувати скринкасти реплеєм журналів.
- `--base-url` — адреса застосунку; без неї питаємо користувача на кроці 2.
- `--embed` — примусовий синтаксис вставок; без нього — автодетект (крок 1).

**Gate (hard refuse):**

1. `playwright-cli --version` падає → відмова з інструкцією:
   `npm install -g @playwright/cli@latest && npx playwright install chromium`.
2. Dev server не відповідає на `<base-url>` → відмова: «підніми застосунок і повтори» (не
   вигадуємо стан — прецедент `verify-ui`).
3. Auth-стратегія невідома → AskUserQuestion (варіанти: без авторизації / кроки логіна /
   готовий state-файл / службовий токен). Без відповіді — відмова.

## Protocol

1. **Детект цілі й синтаксису.** Walk-up від `<target-dir>` до кореня: знайшов `.obsidian/` →
   vault → `embed_syntax: wikilink`; інакше → `markdown`. `--embed` — override. Шляхи з
   пробілами (iCloud vault) — завжди в лапках.
2. **Gate** (див. вище) + зафіксувати `base_url` і назву продукту.
3. **Auth bootstrap** (раз per роль, робить БАТЬКО): пройти логін за обраною стратегією →
   `playwright-cli -s=docgen-auth state-save` → `<target>/.docgen/auth-<role>.json` → закрити
   сесію. Субагенти тільки `state-load` — жоден агент не логіниться сам.
4. **Інвентаризація флоу** → протокол у [`./references/flow-inventory.md`](./references/flow-inventory.md):
   merge трьох джерел (`--flows` / скан репо через `sdlc:explorer`, fallback `Explore` / живий
   `snapshot` навігації); класифікація кожного флоу `doc_type` (task-flow / state-reference /
   auth) і `mutates` (чи змінює дані). AskUserQuestion: підтвердити список + типи + scope.
   **Після підтвердження список заморожений.**
5. **Манифест** `<target>/.docgen/flows-manifest.json` + створити теки `screenshots/<slug>/`:

   ```json
   {
     "product_name": "Beer LMS",
     "base_url": "http://localhost:5173",
     "target_dir": "/abs/path/to/target",
     "embed_syntax": "wikilink",
     "viewport": { "capture": "1280x800", "publish_width": 780 },
     "video": false,
     "data_prefix": "Docgen:",
     "flows": [
       {
         "slug": "create-session",
         "title": "Create Mentorship Session",
         "doc_type": "task-flow",
         "mutates": true,
         "start_url": "/mentorship",
         "auth_state": ".docgen/auth-mentor.json",
         "scope": "list → create dialog → toast; без edit/delete",
         "out_file": "Flow - Create Mentorship Session.md",
         "screenshots_dir": "screenshots/create-session",
         "journal": ".docgen/journals/create-session.jsonl",
         "session": "df-1",
         "status": "pending"
       }
     ]
   }
   ```

6. **Фан-аут `sdlc:doc-flow`** (fallback: general-purpose з тим самим промптом). **Батчування
   за `mutates`, не за кількістю**: read-only флоу паралельно батчами ≤3; мутуючі — СТРОГО
   ПОСЛІДОВНО після read-only (конкурентні мутації спільної БД псують скріни сусідів: агент A
   створює запис посеред прогону B — і список у B різний між його власними кроками). Промпт
   кожному агенту інлайнить (clean context — агент не бачить цієї розмови):
   - worker preamble: «execute directly, do not spawn sub-agents, use tools directly, report
     results with absolute file paths»;
   - його JSON-entry з манифеста (з абсолютизованими шляхами) + global-поля (`base_url`,
     `embed_syntax`, `data_prefix`, `product_name`);
   - абсолютні шляхи: style-guide, determinism, шаблон
     `${CLAUDE_PLUGIN_ROOT}/skills/user-documentation/templates/flow-doc.md`, auth-state;
   - **назви всіх флоу цього прогону** — Related Flows лінкує тільки заплановані доки, не
     вигадані;
   - cwd-гігієна: всі playwright-cli команди запускати з власної тимчасової теки (артефакти
     `.playwright-cli/` падають у cwd і не мають засмічувати ціль/vault);
   - імена сесій короткі (`df-<n>` за індексом флоу) — довші впираються в ліміт unix-socket
     шляху (determinism.md §5).

   Очікуваний фінальний рядок — sentinel `DOCFLOW_OK ...` / `DOCFLOW_FAIL ...`. На FAIL —
   **1 retry**; знову FAIL → `status: failed` у манифесті, пайплайн продовжується.
7. **User Guide індекс** (батько): з H1 + лід-абзаца кожного готового дока + манифеста зібрати
   тонкий `<Product> - User Guide.md` за
   [`./templates/user-guide-index.md`](./templates/user-guide-index.md). Кожен флоу злінкований
   (vault: `[[Flow - X]]`; repo: `[Flow - X](<Flow - X.md>)`). Індекс v1 без власних скрінів.
8. **Опційний скринкаст** (`--video`): для обраних флоу
   ```bash
   "${CLAUDE_PLUGIN_ROOT}/skills/user-documentation/scripts/replay-screencast.sh" \
     "<target>/.docgen/journals/<slug>.jsonl" "<target>/screencasts/<slug>.webm" \
     "<target>/.docgen/auth-<role>.json" "<base-url>" "<start-url>"
   ```
   → секція `## Screencast` з embed-ом одразу після ліда. Для мутуючих флоу попередити
   користувача: реплей створить ще один `Docgen:`-запис.
9. **Механічний гейт**:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/user-documentation/scripts/validate-docs.py" \
     "<target-dir>" --embed <mode> [--video]
   ```
   Червоне → точкові фікси (батько сам, без агентів) → re-run до зеленого.
10. **Когерентність** (батько; БЕЗ `sdlc:critic` — його проби зашиті під PRD/SAD, а батько тут
    clean-context by construction): grep-звірка між доками — назва продукту однакова, ролі та
    статуси називаються консистентно, терміни збігаються з UI.
11. **Handoff.** Git-репо → запропонувати commit `docs: user documentation for <product>`
    (ТІЛЬКИ шляхи цілі); vault → без коміту (obsidian-git сам). Закрити СВОЇ сесії
    (`-s=<name> close`, ніколи `close-all`). `.docgen/` лишається — журнали = сировина для
    майбутніх `--video`. Завершити **stage-handoff блоком** за
    [`../_shared/handoff.md`](../_shared/handoff.md), utility-варіант: *Run next* = «resume
    your backbone stage» або повторний виклик з `--video`.

## Questions for discussion (відкрите, перевіряється живим прогоном)

- Чи існує `video-start --size` у playwright-cli 0.1.13 (у help не підтверджено). Якщо ні —
  розмір відео = розмір в'юпорта (1280×800), що нас і так влаштовує.
- Чи приймає `run-code` контекст іменованої сесії так, як очікуємо, — перший живий реплей
  скринкаста це підтвердить/спростує.
- Pacing-пауза реплею 0.5–1.0s (`PACE` env у replay-screencast.sh) — підібрати на око.

## Definition of Done

- Кожен підтверджений флоу має `DOCFLOW_OK` (≤1 retry) або чесний `failed` у манифесті й у
  фінальному звіті — без тихих пропусків.
- `validate-docs.py` зелений (exit 0) на `<target-dir>`.
- Індекс існує і лінкує всі згенеровані флоу; embed-синтаксис відповідає режиму цілі.
- `.docgen/` містить манифест + журнали всіх пройдених флоу.
- Всі `docflow-*`/`replay-*`/`docgen-auth` сесії закриті.
- При `--video` — .webm існує і вбудований у відповідний док.

## Anti-patterns

- **Не вигадуй UI.** Жодного факту поза журналом/snapshot (єдиний виняток — `doc_type: auth`,
  явно позначений у [`../../agents/doc-flow.md`](../../agents/doc-flow.md)).
- **Не жени мутуючі флоу паралельно** — це головне джерело недетермінованих скрінів.
- **Не тримай Playwright MCP у циклі** — канон CLI (прецедент `verify-ui`); MCP лише для
  живого дебагу поза пайплайном.
- **Не публікуй скрін ширший за 780px** — це нересайзнутий кадр, який втік з пайплайна.
- **Не використовуй `> [!note]`** — доки мають рендеритись на GitHub, лише `> **Note:**`.
- **Не змішуй embed-синтаксиси** — режим один на весь target, з манифеста.
- **Не роби `close-all`/kill-all** — паралельні агенти діляться машиною.
- **Не «лагодь» застосунок** — знайдений баг іде у звіт/Troubleshooting, не у код.
- **Не дублюй шпаргалку CLI** — `playwright-cli install --skills` ставить власний SKILL.md;
  тут лише скіло-специфічні гочі (determinism.md §5).

## Templates / References

- [`./templates/flow-doc.md`](./templates/flow-doc.md) — шаблон flow-документа (тип А + вставний
  блок типу Б + хвостові таблиці).
- [`./templates/user-guide-index.md`](./templates/user-guide-index.md) — тонкий індекс v1.
- [`./references/style-guide.md`](./references/style-guide.md) — кодифікація еталонного стилю.
- [`./references/determinism.md`](./references/determinism.md) — data state, 780px, журнал,
  інваріанти валідатора, CLI-гочі.
- [`./references/flow-inventory.md`](./references/flow-inventory.md) — протокол інвентаризації.
- [`../verify-ui/SKILL.md`](../verify-ui/SKILL.md) — браузерний канал верифікації AC; той самий
  CLI-канон, інша мета (вердикт, не документація).

## Example invocation

```
/sdlc-user-documentation "~/vault/Beer-LMS-docs" --flows create-session,authentication --video
```

Приклад диспатчу одного флоу (крок 6):

```
Task(subagent_type="sdlc:doc-flow", prompt="
  Execute directly, do not spawn sub-agents, use tools directly, report results with absolute
  file paths.
  Document ONE flow of 'Beer LMS' (base_url http://localhost:5173, embed_syntax wikilink,
  data_prefix 'Docgen:').
  Flow entry: {"slug":"create-session", ... (повний JSON-entry, шляхи абсолютні)}.
  Read first: <abs>/references/style-guide.md, <abs>/references/determinism.md,
  template <abs>/templates/flow-doc.md. Auth: state-load <abs>/.docgen/auth-mentor.json.
  Session: df-1. Sibling flows this run: Authentication, Session Lifecycle.
  End with the DOCFLOW_OK/DOCFLOW_FAIL sentinel line.")
```

## Stage handoff

> **user-documentation → (utility, ad-hoc).** Наприкінці друкується stage-handoff блок за
> [`../_shared/handoff.md`](../_shared/handoff.md): *What I did* — скільки флоу OK/failed, шлях
> до індексу й доків, запропонований коміт (для git-цілі); *Review* — індекс + кожен flow-док +
> звіт валідатора; *Run next* — resume your backbone stage (напр. `/sdlc-ship-feature <slug>`)
> або повторний виклик із `--video` / рештою флоу. `/clear` опційний (utility-варіант).
