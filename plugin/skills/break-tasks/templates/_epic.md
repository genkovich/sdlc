# Epic — <slug>

> **PRD:** [PRD.md](../PRD.md) · **Design:** [sad.md](../sad.md) · **Data model:** [data-model.md](../data-model.md) · **API:** [openapi.yaml](../contracts/openapi.yaml) · **ADRs:** [adr/](../adr/)

## Goal

<!-- instruction: 2–3 sentences — what shipping this epic delivers, tied to PRD §2 Goals. -->

## Scope

- **In:** <the layers/modules this epic touches>.
- **Out:** <explicit non-scope, from PRD §3>.

## Task map

<!-- instruction: the dependency graph as a Mermaid flowchart. This is the same DAG as tasks.json.
Validate it per ../_shared/mermaid-check.md before committing. -->

```mermaid
flowchart LR
    T1[T1 migration] --> T3
    T2[T2 domain] --> T3[T3 infra]
    T3 --> T4[T4 app] --> T5[T5 ports]
    T5 --> T6[T6 tests]
```

## Tasks

See [tracker.md](./tracker.md) for status. Machine contract: [tasks.json](./tasks.json).

| # | Task | Layer | Blocked by | DoD (short) |
|---|---|---|---|---|
| T1 | <title> | migration | — | <one line> |
| T2 | <title> | domain | — | <one line> |

## Risks / Hard rules

<!-- instruction: any PRD §6 NFR / sad §11 constraint a task must not violate. -->
