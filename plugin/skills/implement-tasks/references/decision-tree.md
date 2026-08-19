# Decision tree — picking the execution mode (step 5)

The engine has three modes: **sequential single-agent TDD** (the floor everything degrades to), **agent team** (TeamCreate), and **dynamic Workflow**. The choice is deterministic — no judgement call at runtime.

## Inputs to the decision

From step 4 (DAG) and step 2 (settings):

- `task_count` — number of tasks.
- `parallel_width` — max tasks runnable at once (widest Kahn layer).
- `longest_chain` — critical-path length (informational; reported in the banner).
- `size` — the feature `.size` (XS/S/M/L/XL), or M if absent.
- settings: `team_mode`, `workflow_mode`, `isolation`, `max_parallel_agents`.
- runtime: is the `Workflow` tool available? is `TeamCreate` available?

## Eligibility

```
parallel_eligible :=
      isolation == "worktree"
  AND max_parallel_agents > 1
  AND parallel_width >= 2
  AND (size in {M, L, XL} OR task_count >= 4)
```

Rationale: parallelism only pays off when there is genuinely concurrent work (`parallel_width >= 2`), the feature is non-trivial (`M+` or `>=4` tasks), agents can't collide (`worktree`), and more than one is allowed.

## Selection

```
if team_mode AND parallel_eligible AND TeamCreate-available:
    → AGENT TEAM over the DAG            (see team-exec.md)
elif workflow_mode == "auto" AND parallel_eligible AND Workflow-available:
    → DYNAMIC WORKFLOW                    (see workflow-exec.md)
else:
    → SEQUENTIAL single-agent TDD (topo order)
```

`team_mode` wins over `workflow_mode` when both could apply (a human-shaped team with a reviewer is the richer mode; the workflow is the unattended one).

## Guards (apply before dispatch — they can only make the engine safer)

| Condition | Action |
|---|---|
| `team_mode: true` but `parallel_eligible` is false | Warn («team needs ≥2 parallel tasks and M+/≥4 tasks; this feature has <…>») and **downgrade** to the next applicable mode (workflow if eligible, else sequential). |
| `max_parallel_agents > 1` and `isolation: inplace` | Clamp parallelism to 1 (two agents must never edit one working tree). Effectively sequential. |
| `workflow_mode: off` | Never generate a Workflow, regardless of eligibility. |
| `Workflow` tool not available at runtime | Skip the workflow branch; fall through to team (if eligible) or sequential. Graceful degrade — never error. |
| `TeamCreate` not available at runtime | Skip the team branch; fall through to workflow or sequential. |
| `tdd: false` | Skip the RED step in every mode and warn loudly (you lose the safety net). |
| `require_integration: always` and Docker unreachable | **BLOCK** before dispatch — do not start work that can't satisfy its own gate. |
| `require_integration: auto` and Docker unreachable | Proceed; the integration tier is marked NON-red per task (not counted as pass or fail). |
| `require_integration: never` | Skip the integration tier silently (still run unit + lint + vet). |

## Banner (step 7)

After the tree + guards resolve, print exactly what will happen, e.g.:

```
SDLC implement-tasks — feature: notification-preferences
  mode          = AGENT TEAM (3 agents)        [team_mode=true, parallel_width=3, size=M]
  tdd           = on
  isolation     = worktree
  integration   = auto (docker: reachable)
  commit        = per_task  (branch: feature/notification-preferences)
  tasks         = 6   phases = 4   longest_chain = 4
```

The banner is mandatory — the user must see the mode and the settings that drove it before any code is written.
