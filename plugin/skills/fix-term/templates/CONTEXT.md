---
status: Living
updated_at: "<today YYYY-MM-DD>"
---

# Domain Context — <slug or repo>

<!--
CONTEXT.md is the domain glossary — not a PRD and not a scratch pad. NO implementation
detail here (no datastore/broker/framework names, no API contracts) — only domain words
and the boundaries between them. Implementation choices live in the SAD and ADRs;
behaviour lives in PRD.md.

Multi-context repos: each bounded context has its own CONTEXT.md at its root path
(registered in CONTEXT-MAP.md). System-wide terms that span all contexts live in the
repo-root CONTEXT.md. Never duplicate a term across files — pick one owner.

Terms get fixed inline, the moment they surface in an interview / PRD / review — never
batched «I'll consolidate later». Empty H2 → prune before commit; keep only the sections
that carry real content. ## Glossary is mandatory; the other two are optional.
-->

## Glossary

<!-- One line per term: name · one-sentence canonical definition · one-sentence boundary
     (what it is NOT / the concept it gets confused with). Alphabetical once there are a few. -->
- <term> — <one-sentence definition>. NOT <concept it's confused with + how it differs>.

## Invariants

<!-- Domain rules that hold across the whole feature/codebase — phrased «X always must / can
     never». These are rules ABOVE any single acceptance criterion, not PRD AC. Prune the
     section if there are none. -->
- <invariant in the form «X always must / can never»>

## Out of scope

<!-- Concepts the author explicitly placed outside this domain, with a one-line reason — so
     nobody re-litigates them in six months. Prune the section if there are none. -->
- <out-of-scope concept · reason it's excluded>
