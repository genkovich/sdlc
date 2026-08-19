# Determinism — how two runs of the same flow produce the same document

> The pipeline's promise: re-running a flow against the same app state yields the same steps,
> the same screenshots, the same doc. Every rule here exists because its absence broke that
> promise somewhere.

## 1. Data state is the root of determinism

- **`mutates` classification is mandatory.** At inventory time every flow is marked
  `mutates: true/false` — does walking it change application data? The parent schedules
  read-only flows in parallel batches (≤3) and mutating flows **strictly sequentially** after
  them. Two concurrent mutators corrupt each other's screenshots: agent A creates a record in
  the middle of agent B's walk, and B's list screenshots disagree between B's own steps.
- **Test-data prefix.** Everything an agent creates through the UI starts with the manifest's
  `data_prefix` (default `Docgen:`) — "Docgen: React Hooks Deep Dive". Recognizable in
  screenshots, greppable for cleanup.
- **Type B needs observed states.** A state-reference doc documents only states that exist on
  screen. If the DB lacks a state (no cancelled session anywhere), the agent creates it through
  the UI (that flow is `mutates: true` by definition) — or fails honestly with
  `reason=states-not-observable`. Inventing a state from imagination is the cardinal sin.
- **Known nondeterminism is documented, not hidden.** Calendar views, relative dates
  ("2 days ago"), live counters — screenshots of these legitimately differ between runs. The
  doc stays valid; just don't anchor step text to the volatile value.

## 2. Viewport & the exact-780px contract

- Headless Chromium has device scale factor 1 — that is what makes pixel math stable. A headed
  browser on a Retina display doubles it and breaks the contract. **Headless only.**
- Capture viewport: `resize 1280 800` right after `open`, before any navigation.
- Full-view publish path: capture at 1280 → `sips --resampleWidth 780 <in> --out <out>`
  (macOS, zero-dep). Fallback: `magick <in> -resize 780x <out>`.
- Element crops are published as captured — never resized. Any PNG wider than 780 in the
  output is an unresized capture that escaped the pipeline; the validator rejects it.

## 3. The action journal

`<target>/.docgen/journals/<slug>.jsonl` — one JSON object per line, `seq` from 1:

```json
{"seq":3,"action":"fill","locator":"getByLabel('Title')","css":"#session-title","value":"Docgen: React Hooks Deep Dive","note":"fill the required title"}
{"seq":4,"action":"screenshot","file":"04-title-filled.png","note":"The form with the title filled in"}
```

- `action` ∈ `goto | click | fill | select | press | hover | check | uncheck | screenshot`.
  This closed dictionary IS the replay contract — the screencast script re-executes exactly
  these verbs and nothing else.
- `locator` — Playwright fluent locator from `generate-locator`; `css` — a plain CSS fallback
  used when the fluent one fails on replay.
- `screenshot` records carry `file` (basename inside the flow's screenshots dir) and become
  `video-chapter` markers on replay.
- The journal is append-only during the walk and is the ONLY source of facts for the writing
  phase. It stays in `.docgen/` after the run — it is the raw material for `--video` replays.

## 4. Invariants (what `validate-docs.py` enforces mechanically)

1. H1 == basename; no frontmatter; `---` between top-level sections.
2. Step/State numbering gapless from 1.
3. Every embed resolves to an existing file; no orphan PNGs under `screenshots/`.
4. Screenshot names match `^\d{2}-[a-z0-9-]+\.png$`; embed order follows the numbers.
5. PNG width ≤ 780 (IHDR check, no image library needed).
6. 1–10 embeds per doc; one embed syntax per target, matching the manifest mode.
7. No `> [!` callouts; Related Flows links resolve; the index links every flow doc.
8. With `--video`: every `## Screencast` embed resolves to an existing `.webm`.

## 5. playwright-cli gotchas specific to this skill

1. Command order is fixed: `open` → `resize 1280 800` → `state-load` → `goto <start_url>`.
   Resizing after navigation invalidates earlier screenshots.
2. `--filename <absolute path>` on EVERY `screenshot` call — otherwise the PNG lands in
   `.playwright-cli/` under a timestamp name and is lost to the pipeline.
3. Sessions are namespaced: every command carries `-s=<session>`. A bare command without
   `-s=` talks to the default session — someone else's browser. Names must be SHORT: the
   daemon's unix-socket path embeds the session name and macOS caps socket paths at ~104
   bytes — `df-create-session` already hits the limit and dies with `listen EINVAL ... .sock`.
   Convention: the manifest assigns `df-<n>` (flow index) for walks; the replay script derives
   `rp-<cksum>` itself.
4. Close only your own session (`-s=<session> close`). `close-all` / kill-alls murder the
   parallel siblings.
5. There is **no `wait` command** (pre-1.0 CLI). Settle = poll `snapshot` until the element
   that proves the new state exists. Never `sleep`-and-hope before a screenshot.
6. `generate-locator <ref>` gives the fluent locator for the journal; grab it in the same
   snapshot generation as the action — refs go stale after the page changes.
7. Auth is bootstrapped once by the parent (`state-save` → `.docgen/auth-<role>.json`);
   agents only ever `state-load`. No agent logs in by itself.
8. `run-code "async page => { ... }"` executes arbitrary Playwright against the session —
   the replay path uses it exclusively (auto-wait for free, no fluent-grammar guessing in
   CLI arguments).
9. The CLI is pre-1.0: verify syntax against `playwright-cli --help` when something errors —
   flags drift between releases. This file documents intent, the CLI documents itself.
10. Video: `video-start <out.webm>` → actions → `video-chapter "<note>"` per screenshot
    marker → `video-stop`. Video size follows the viewport (1280×800).
