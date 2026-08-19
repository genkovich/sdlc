---
status: Draft
owner: "<Tech Lead name>"
reviewers: ["<SRE name>"]
updated_at: "<YYYY-MM-DD>"
feature_size: M
stage: "07"
ticket: "<ticket-id>"
---

# Deployment

<!-- Deployment-diagram scaffold for SAD §7 (Deployment view) → see sdlc/plugin/skills/architecture-design/SKILL.md -->
<!-- N/A allowed for XS/S that reuses an existing deployment unit with no change. -->

```mermaid
flowchart TB
    subgraph prod[Production]
        subgraph k8s[Kubernetes cluster]
            api1[API replica 1]
            api2[API replica 2]
            api3[API replica N]
        end
        pg[(PostgreSQL primary)]
        pgr[(PostgreSQL replica)]
        redis[(Redis cluster)]
    end

    LB[Load balancer] --> api1
    LB --> api2
    LB --> api3
    api1 --> pg
    api2 --> pg
    api3 --> pg
    api1 --> redis
```

## Resources / scaling

| Component | Replicas | CPU / mem | Scale trigger |
|---|---|---|---|
| API | <N> | <m / Mi> | <CPU > 70%> |
| Redis | <N> | <m / Mi> | manual |
| Postgres | 1 primary + <N> replicas | <m / Mi> | manual |

## Networking
- <Network policy / mTLS / secrets management>
