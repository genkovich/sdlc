# sdlc — SDLC toolkit for Claude Code

Full idea-to-ship pipeline as a Claude Code plugin: 21 skills — a 12-stage
map-architecture → ship backbone, ideation interview (feature **and greenfield
project** modes with an easy/medium/hard depth regulator), a **scaffold** skill that
materializes a new project from the public [base-tpl](https://github.com/genkovich/base-tpl)
template with subtractive batteries, plus cross-cutting utilities: live-browser UI
verification (`verify-ui`), end-user documentation generation (`user-documentation`),
design specs, ADRs, review checklists.

## Install

```bash
claude plugin marketplace add genkovich/sdlc
claude plugin install sdlc@sdlc        # user scope: skills available in every folder
```

## Start a new project (greenfield flow)

```bash
mkdir my-app && cd my-app && claude
```

Then inside Claude Code:

1. `/sdlc-interview` — greenfield mode interviews the idea and writes `docs/idea-brief.md`
   (pick **easy** depth for a quick pass).
2. `/sdlc-scaffold` — asks stack + battery questions (frontend, deploy, CI,
   Prometheus+Grafana, freshness pin bump) and materializes the project from base-tpl.
   Unselected batteries are physically absent; "yes to everything" reproduces the
   template byte-for-byte.
3. `/init` — generate the root CLAUDE.md; then `make check` and `make up`.

## Feature flow (inside an existing repo)

`/sdlc-interview <slug>` → `write-prd` → `clarify-prd` → `architecture-design` →
`break-tasks` → `plan-tests` → `implement-tasks` → `review-feature` → `ship-feature`,
with `classify-size` gating how much ceremony each feature size gets.

See [CHANGELOG.md](CHANGELOG.md) for versions.

## License

MIT
