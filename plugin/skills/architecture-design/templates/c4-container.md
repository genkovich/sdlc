---
status: Draft
owner: "<Architect name>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: S
stage: "06"
ticket: "<ticket-id>"
---

# C4 — Container

<!-- Stages 04-05 → see sdlc/plugin/skills/architecture-design/SKILL.md -->
<!-- Standalone L2 C4Container snippet — embedded inline in SAD §5. One Container per declared -->
<!-- target_surface (frontmatter). Syntax → references/c4-mermaid-syntax.md -->

```mermaid
C4Container
    title Container diagram — <feature>

    Person(user, "<User>")

    Container_Boundary(c1, "<Our system>") {
        Container(web, "Web app", "React", "<...>")
        Container(api, "API", "Go / Chi", "<...>")
        ContainerDb(db, "Database", "PostgreSQL", "<...>")
        ContainerDb(cache, "Cache", "Redis", "<...>")
    }

    System_Ext(ext, "<External>")

    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "API calls", "JSON / HTTPS")
    Rel(api, db, "Reads/writes", "SQL")
    Rel(api, cache, "Caches", "Redis protocol")
    Rel(api, ext, "Integrates", "REST")
```
