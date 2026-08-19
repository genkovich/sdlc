<!-- Template for api-forge — copied to docs/features/<slug>/contracts/public-api.md ONLY when  -->
<!-- the sad.md frontmatter `target_surfaces` includes `library-sdk`. This is the public        -->
<!-- signatures/types surface derived from PRD acceptance criteria and sad.md §6 usage flows.   -->
<!-- Every public function/type here maps to a PRD user story. Delete if surface is not         -->
<!-- `library-sdk`.                                                                              -->
---
status: Draft
owner: "<Lib owner>"
reviewers: []
updated_at: "<YYYY-MM-DD>"
feature_size: M
---

# Public API Contract — <feature>

Library/SDK surface for the feature declared in `sad.md` `target_surfaces: [library-sdk]`.
Like the OpenAPI contract, this is **derived** from the PRD acceptance criteria and `sad.md` §6
usage flows — every exported function/type here maps to a PRD §4 user story; every error maps
to an `alt`-branch. Schema names use the domain language from `data-model.md`, not a language
idiom.

## Language / runtime

<!-- Detect from the repo — do not assume. -->
- **Language:** `<detect from repo>`
- **Package name:** `<package>` (import path: `<import-path>`)
- **Minimum supported runtime:** `<version>`

## Types

<!-- One block per data-model.md entity the library exposes. Every field traces to a column. -->

### `<Entity>`

```
// field → data-model.md column (type, constraints)
<Entity> {
  id:         string (uuid)         // data-model.md → <entity>.id
  <field>:    <type> (<constraint>) // data-model.md → <entity>.<column> (maxLength/enum/nullable)
}
```

## Functions / methods

<!-- One block per PRD §4 user story. -->

### `<functionName>(<params>) → <ReturnType>`

<!-- Origin: PRD §4 US-N — <user story title> -->

**Parameters**

| Name | Type | Required | Description |
|---|---|---|---|
| `<param>` | `<type>` | yes/no | `<traces to PRD AC or data-model.md field>` |

**Returns**

`<ReturnType>` — `<what it holds, tracing to data-model.md where applicable>`.

**Errors / exceptions**

<!-- Derive from sad.md §6 alt-branches — same neutral `module.error_name` convention as HTTP. -->

| Code | Type/Exception | Origin |
|---|---|---|
| `<module>.<error_name>` | `<Error type>` | sad.md §6 `alt: <branch>` |

**Example**

```
// placeholder data only — never real PII
result = <functionName>(<placeholder-args>)
```

## Backwards-compat policy

- **Additive-only:** a new optional parameter or field in a return type is fine; removing,
  renaming, or changing the type of an exported symbol is a breaking change and requires a
  major version bump.
- Internal (unexported) symbols are **not** part of this contract.

## Versioning

- This file tracks the **public contract version**, separate from the internal implementation.
- `version` in the frontmatter of this file matches the library's published semver.
- Never bump the version silently — change it with a CHANGELOG line.
