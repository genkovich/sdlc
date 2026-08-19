<!-- Template for `complete-sequence-diagrams` — embedded INLINE in docs/features/<slug>/sad.md §6 (Runtime view). -->
<!-- One `### <flow name>` block per critical flow. Participants are GENERIC placeholders —  -->
<!-- replace the <...> message/note text with this flow's specifics, NOT the participant names. -->
<!-- Generic vocabulary (the only allowed participants):                                        -->
<!--   <client>          — whatever initiates the flow (UI, CLI, another service, a scheduler) -->
<!--   <ui>              — a browser/mobile/desktop UI (only when target_surfaces declares one) -->
<!--   <service>         — the building block that owns this flow (from sad.md §5)             -->
<!--   <data-store>      — the persistent store the service reads/writes                       -->
<!--   <external-system> — a third party the service calls out to                              -->
<!--   <message-bus>     — async transport (queue / event stream) for non-sync flows           -->
<!-- Naming the concrete technology is architecture-design / generate-data-model's job.        -->
<!-- When sad.md frontmatter declares a UI surface (web-frontend / mobile-app / desktop-app), -->
<!-- draw UI-driven flows: <user> (actor) -> <ui> -> <service> -> <data-store>.               -->

### <flow name>

<!-- SYNC flow: request -> response, with the error branches the PRD's acceptance criteria demand. -->
<!-- Every write becomes a persist note so generate-data-model knows what to index downstream.    -->

```mermaid
sequenceDiagram
    autonumber
    participant C as <client>
    participant S as <service>
    participant D as <data-store>

    Note over C,S: Precondition: <state required before this flow, from PRD>
    C->>S: <action>
    S->>D: <read / lookup>
    D-->>S: <result>
    S->>D: <write>
    Note over S,D: persists <entity> (see §6 / informs data-model indexes)
    D-->>S: <ack>
    S-->>C: <success outcome>
    alt <error condition from acceptance criteria>
        S-->>C: <error outcome — name it, no status numbers>
    else <second error condition>
        D-->>S: <store failure>
        S-->>C: <error outcome>
    end
    Note over C,S: Postcondition: <state guaranteed after this flow, from PRD>
```

<!-- UI-driven variant — use when sad.md target_surfaces includes web-frontend / mobile-app / desktop-app.  -->
<!-- Replace the block above with this shape for those flows.                                               -->

### <UI-driven flow name>

```mermaid
sequenceDiagram
    autonumber
    actor U as <user>
    participant UI as <ui>
    participant S as <service>
    participant D as <data-store>

    Note over U,UI: Precondition: <state required before this flow, from PRD>
    U->>UI: <user action>
    UI->>S: <request>
    S->>D: <read / lookup>
    D-->>S: <result>
    S->>D: <write>
    Note over S,D: persists <entity> (informs data-model indexes)
    D-->>S: <ack>
    S-->>UI: <success response>
    UI-->>U: <visible outcome>
    alt <error condition from acceptance criteria>
        S-->>UI: <error response>
        UI-->>U: <visible error>
    end
    Note over U,UI: Postcondition: <state guaranteed after this flow, from PRD>
```

### <async flow name>

<!-- ASYNC flow (webhook in / scheduled job / queued or event-driven step / third-party callback). -->
<!-- MUST include: idempotency-key check as the first handler step, a retry note, a dead-letter branch. -->

```mermaid
sequenceDiagram
    autonumber
    participant C as <client>
    participant B as <message-bus>
    participant S as <service>
    participant X as <external-system>
    participant D as <data-store>

    Note over C,B: Trigger: <event / schedule / callback that starts this flow>
    C->>B: <enqueue event>
    B->>S: <deliver event>
    S->>S: check idempotency key (skip if already processed)
    S->>X: <outbound call>
    X-->>S: <response>
    S->>D: <write result>
    Note over S,D: persists <entity> (informs data-model indexes)
    D-->>S: <ack>
    Note over S,X: retry <N> times with exponential backoff on failure
    alt exhausted retries
        S->>B: <route to dead-letter>
        Note over S,B: dead-letter after <N> failed attempts
    end
```
