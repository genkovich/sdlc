---
name: scaffold
model: inherit
effort: medium
agents: []
description: >-
  Use to materialize a new full-stack project from the base-tpl template with a
  subtractive battery interview. Triggers on "scaffold a new project",
  "/sdlc-scaffold", "заскафолдь проєкт", "новий проєкт з темплейта",
  "розгорни проєкт з base-tpl", "scaffold from template" — typically right after
  /sdlc-interview produced docs/idea-brief.md in an empty folder. Reads the brief
  (name/context), asks stack + battery questions (web frontend, deploy, CI,
  Prometheus+Grafana observability, freshness bump), then runs base-tpl's
  scaffold.sh: full template copy with unselected batteries physically removed.
  "Yes to everything" reproduces the template byte-for-byte. Not the same as
  /sdd:scaffold (which materializes a skeleton planned by /sdd:survey inside an
  SDD flow) — this one copies a ready-made template into an empty folder.
triggers:
  - /sdlc-scaffold
  - scaffold a new project
  - scaffold from template
  - заскафолдь проєкт
  - новий проєкт з темплейта
  - розгорни проєкт з base-tpl
---

# Skill: scaffold (new project from base-tpl)

Матеріалізує новий проєкт із темплейта **base-tpl** субтрактивно: копіюється повний
наповнений шлях, невибрані батарейки **фізично видаляються** (теки, сервіси compose,
CI-джоби, рядки README). «Так на все» = темплейт байт-у-байт. Механіка вирізання живе
у `scaffold.sh` в корені base-tpl і тестується CI-матрицею base-tpl — цей скіл лише
збирає відповіді і викликає двигун.

## Джерело темплейта

1. Якщо задано env `SDLC_BASE_TPL` — використовуй цей шлях (локальний клон base-tpl).
2. Інакше — свіжий shallow-клон публічного репо:
   ```bash
   git clone --depth 1 https://github.com/genkovich/base-tpl /tmp/base-tpl-$$
   ```
   Клон разовий, після скафолда його можна видалити.

## Кроки

### 1. Контекст: idea-brief

Якщо у поточній теці є `docs/idea-brief.md` (продукт `/sdlc-interview` у greenfield-режимі) —
прочитай його: назва продукту (kebab-case slug) і суть беруться звідти, назву не питай
(лише підтверди slug одним рядком у першому питанні кроку 2). Якщо brief-а нема —
спитай назву проєкту (kebab-case slug) перед техінтерв'ю.

Ціль скафолда — **поточна тека**, якщо вона порожня або містить лише `docs/` з brief-ом;
інакше — нова тека `./<slug>`.

### 2. Техінтерв'ю — виклик А (стек)

Один AskUserQuestion із чотирма питаннями; рекомендований варіант першим:

1. **Мова бекенда:** Go (Recommended) / PHP / Python / TypeScript
2. **Архітектура:** Модульний моноліт (Recommended) / Мікросервіси
3. **Фронтенд:** React + FSD (Recommended) / Без фронта / Flat React
4. **Auth:** Google OAuth (Recommended) / Без auth / Email + password

**Чесність про наповнення base-tpl.** Наповнені шляхи зараз:

| Вибір | Стан |
|---|---|
| Go + моноліт | ✅ `templates/go-react` |
| React + FSD | ✅ (той самий шлях) |
| **Без фронта** | ✅ реальна субтракція (`--no-web`) |
| Google OAuth | ✅ вшито в темплейт |
| PHP / Python / TypeScript | 🔒 ще не наповнено |
| Мікросервіси | 🔒 ще не наповнено |
| Flat React | 🔒 ще не наповнено |
| Без auth / Email + password | 🔒 ще не наповнено (auth вшито в темплейт) |

Вибір 🔒-варіанта → зупинись і скажи прямо: «цей шлях у base-tpl ще не наповнено —
наповни `templates/<стек>` у base-tpl або обери наповнений варіант». Не генеруй
заглушок замість темплейта.

### 3. Техінтерв'ю — виклик Б (батарейки)

Другий AskUserQuestion: одне multiSelect-питання про батарейки + одне про freshness:

1. **Батарейки** (multiSelect, всі увімкнені за замовчуванням — Enter лишає все):
   - **Deploy** — `deploy/` (Caddy авто-TLS, prod-compose) + deploy-workflow (GHCR → VPS → health-гейт)
   - **CI** — `.github/workflows/ci.yml` (ті самі перевірки, що `make check`)
   - **Моніторинг** — Prometheus + Grafana локально і в проді (ендпоінт `/metrics` в api лишається завжди)
2. **Freshness** — оновити піни інфраструктури до свіжих версій? Так (Recommended) / Ні.

Невибрана батарейка фізично зникає: тека, сервіси compose, CI-джоби, рядки README.

### 4. Виклик двигуна

```bash
BASE_TPL=${SDLC_BASE_TPL:-/tmp/base-tpl-$$}   # див. «Джерело темплейта»
OWNER=$(gh api user -q .login 2>/dev/null || echo example)
"$BASE_TPL/scaffold.sh" "$TARGET" "$SLUG" "$OWNER" \
  [--no-web] [--no-deploy] [--no-ci] [--no-observability] \
  [--brief docs/idea-brief.md] \
  [--no-git]   # лише якщо обрано freshness — git init робиться після бампів
```

`scaffold.sh` сам: копіює tracked-файли темплейта, вирізає невибрані батарейки за
маркерами `battery:<name>`, перейменовує бренд (`myapp` → slug, `MyApp` → Display,
`example/myapp` → owner/slug), копіює `api/.env.docker.example` → `api/.env.docker`,
кладе brief у `docs/idea-brief.md` і робить `git init` + t0-коміт.

### 5. Freshness (якщо обрано)

Після субтракції, до git init (тому `--no-git` у кроці 4):

1. Зістав піни поверхні стека: Go toolchain і base-образи в `api/Dockerfile`,
   `GO_VERSION`/`NODE_VERSION` у workflows, docker-теги (`postgres`, `prom/prometheus`,
   `grafana/grafana`, `caddy`, `nginx`), версії GitHub Actions.
2. Свіжі версії бери через **context7** (`resolve-library-id` → `query-docs`);
   для docker-тегів і Actions, яких context7 не знає — WebSearch або registry
   (hub.docker.com, github releases). Якщо жоден інструмент недоступний —
   чесно скіпни freshness зі звітом, скафолд не блокуй.
3. Застосуй бампи → гейт: `make check` (при `--no-web` — `make api-check`).
   Червоно → відкат бампів (скафолд віддається зеленим, зі звітом що і чому відкачено).
4. Заверши: `git init -b main && git add -A && git commit -m "t0: scaffold <slug> from base-tpl (go-react)"`.

Бампаються **піни інфраструктури**, не `go.mod`/`package-lock.json` (залежності коду
оновлюються своїм циклом у проєкті).

### 6. Фінальне повідомлення

- **`/init`** — кореневого CLAUDE.md у темплейті навмисно немає; згенеруй його вже
  з контекстом проєкту (`api/CLAUDE.md`, `web/CLAUDE.md` і path-rules приїхали з темплейтом).
- `make check` — наскрізна перевірка.
- `make up` → повний локальний стек (порти — у README проєкту).
- Google-логін потребує реальних `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` в `api/.env.docker`.
- Далі по SDLC: фічі через `/sdlc-interview <slug>` (feature mode) у новому репо.

## Поширені помилки

- Скіл починає «допомагати» руками після scaffold.sh (правити файли, докручувати) —
  ні: скафолд закінчується t0-комітом, все інше — окремі кроки у проєкті.
- Вибрано 🔒-варіант, а скіл згенерував заглушку сам — заборонено, чесна відмова.
- Freshness бампнув go.mod/package-lock — відкат: це піни коду, не інфри.
- Забутий `--no-git` при freshness → бампи розмазуються по історії після t0.
