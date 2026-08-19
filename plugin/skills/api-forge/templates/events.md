<!-- Template for api-forge — copied to docs/features/<slug>/contracts/events.md ONLY when the -->
<!-- feature has async flows (a sad.md §6 sequence with a <message-bus> / <external-system> -->
<!-- participant, an enqueue/deliver message, or a retry note). One `## Event` block per async -->
<!-- message in the sequences. Event names use the domain language from data-model.md, not a -->
<!-- broker/library idiom. Delete this file if the feature is fully synchronous. -->
---
status: Draft
owner: "<Backend Lead>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: M
---

# Events — <feature>

Async contract for the flows drawn in `sad.md` §6. Each event is a published fact; subscribers
read it. Like the OpenAPI contract, this is **derived** from the sequences — every event here
maps to an enqueue/deliver message in a §6 diagram.

## Channel: `<channel-name>`

- **Producer:** `<service>` — the building block that owns the flow.
- **Consumers:** `<list of services / jobs that subscribe>`.
- **Delivery:** at-least-once | exactly-once.
- **Ordering:** key-based (by `<field>`) | none.

## Event: `<module>.<action>.v<N>`

<!-- Name = the neutral `module.action.vN` convention. The envelope mirrors the HTTP error model's -->
<!-- spirit: a small, stable, machine-readable head + a typed `data` body. -->

```json
{
  "event_id": "<uuid>",
  "event_type": "<module>.<action>",
  "version": <N>,
  "occurred_at": "<iso8601>",
  "data": {
    "<field>": "<type — traces to a data-model.md column where one exists>"
  }
}
```

- **Required fields:** `<event_id, event_type, version, occurred_at, ...>`.
- **Origin:** sad.md §6 `<flow name>` → message `<enqueue ...>`.
- **Backwards-compat policy:** additive-only — a new optional field is fine; removing or renaming
  a field is a new version (`v<N+1>`). Subscribers must ignore unknown fields.

## Idempotency & retry

<!-- Pull these numbers from the §6 retry note and dead-letter branch — do not invent them. -->

- **Idempotency:** consumers dedupe on `event_id` (a redelivery carries the same id).
- **Retry:** `<N>` attempts with exponential backoff.
- **Dead-letter:** route to `<channel-name>.dlq` after `<N>` failed attempts; on-call drains it.

## Schema registry

- Registry: `<url / repo path>` — where the canonical schema for each event version lives.
- Validator: `<tool the repo already uses>` — detect it; do not assume one.
