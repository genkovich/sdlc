<!-- Template for api-forge — copied to docs/features/<slug>/contracts/cli.md ONLY when the  -->
<!-- sad.md frontmatter `target_surfaces` includes `cli`. This is the command/flag/exit-code  -->
<!-- surface derived from the PRD acceptance criteria and sad.md §6 flows. Every command here  -->
<!-- maps to a §4 user story. Delete this file if the surface is not `cli`.                  -->
---
status: Draft
owner: "<Backend Lead>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: M
---

# CLI Contract — <feature>

Command-line interface surface for the flows declared in `sad.md` `target_surfaces: [cli]`.
Like the OpenAPI contract, this is **derived** from the PRD acceptance criteria and `sad.md` §6
flows — every command here maps to a §4 user story; every exit code maps to an `alt`-branch.

## Global flags

<!-- Flags that apply to every subcommand. Derive from cross-cutting PRD requirements (auth,
     verbosity, output format). Never invent flags with no origin in any input. -->

| Flag | Short | Type | Description |
|---|---|---|---|
| `--help` | `-h` | bool | Print usage and exit 0. |
| `--version` | | bool | Print version string and exit 0. |
| `--output` | `-o` | `text\|json` | Output format (default: text). |

## Command: `<binary> <command> [subcommand]`

<!-- One block per PRD §4 user story. -->

### Usage

```
<binary> <command> [flags] [args]
```

<!-- One-line purpose — from PRD §4 user story title. -->

### Flags

| Flag | Short | Required | Type | Default | Description |
|---|---|---|---|---|---|
| `--<flag>` | | yes/no | string/int/bool | | `<traces to a PRD AC or data-model.md field>` |

### Arguments

| Arg | Required | Description |
|---|---|---|
| `<arg>` | yes | `<origin: PRD §4 US-N>` |

### Exit codes

<!-- Derive from sad.md §6 alt-branches — one exit code per branch. -->

| Code | Meaning | Origin |
|---|---|---|
| 0 | Success | happy path |
| 1 | General error | any unhandled error |
| 2 | Invalid arguments | alt: validation failure (PRD §5 AC-N) |
| 3 | `<domain error name>` | alt: `<sad.md §6 branch>` |

### Output (exit 0)

```
# text format (default)
<example output — placeholder data only, never real PII>
```

```json
// json format (--output json)
{
  "<field>": "<traces to a data-model.md column or PRD AC>"
}
```

### Error output (exit ≠ 0, stderr)

```
Error: <module>.<error_name>: <human-readable reason>
```

<!-- Error code convention: same neutral `module.error_name` snake_case as the HTTP contract. -->

## Backwards-compat policy

- **Additive-only:** a new optional flag is fine; removing or renaming a flag or changing an
  exit code meaning is a breaking change and requires a major version bump.
- Flag order is **not** significant; short-flag aliases are **stable** once published.
