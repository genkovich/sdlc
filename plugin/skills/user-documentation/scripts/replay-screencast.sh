#!/usr/bin/env bash
# replay-screencast.sh — deterministic replay of a doc-flow action journal into a .webm.
#
# Usage:
#   replay-screencast.sh <journal.jsonl> <out.webm> <auth-state.json> <base-url> [start-url]
#
# Replays the closed action dictionary (goto/click/fill/select/press/hover/check/uncheck)
# through `playwright-cli run-code` — Playwright's auto-wait comes for free and no fluent
# grammar is passed as CLI arguments. Screenshot journal entries become video-chapter markers.
# PACE (env, default 0.7s) is a purely visual pause between actions.
#
# Known limits (documented, accepted):
#   - DB state at replay time differs from the original walk — a mutating flow will create
#     one more record. Fine for a screencast; warn the user before replaying mutators.
#   - Video size follows the viewport (1280x800).

set -uo pipefail

if [ $# -lt 4 ]; then
    grep '^#' "$0" | head -20; exit 2
fi

JOURNAL=$1; OUT=$2; AUTH=$3; BASE_URL=$4; START_URL=${5:-}
PACE=${PACE:-0.7}
# Session names must stay SHORT: the CLI daemon listens on a unix socket whose path includes
# the session name, and macOS caps socket paths at ~104 bytes ("listen EINVAL" = over budget).
# A slug-derived name can blow that budget, so the session is a short slug checksum.
SLUG=$(basename "$JOURNAL" .jsonl)
SESSION="rp-$(printf '%s' "$SLUG" | cksum | awk '{print $1}')"

command -v playwright-cli >/dev/null || { echo "ERROR: playwright-cli not installed" >&2; exit 1; }
[ -f "$JOURNAL" ] || { echo "ERROR: journal not found: $JOURNAL" >&2; exit 1; }

pw() { playwright-cli -s="$SESSION" "$@"; }

WORKDIR=$(mktemp -d)
trap 'pw close >/dev/null 2>&1 || true; rm -rf "$WORKDIR"' EXIT

# --- compile the journal into numbered run-code snippets -------------------------------
python3 - "$JOURNAL" "$WORKDIR" <<'PY' > "$WORKDIR/cmds.tsv"
import json, sys
from pathlib import Path

journal, workdir = sys.argv[1], Path(sys.argv[2])
METHODS = {"click": "click()", "hover": "hover()", "check": "check()", "uncheck": "uncheck()"}

def sel(entry):
    """Primary selector expression from the fluent locator, fallback from css."""
    loc = (entry.get("locator") or "").strip()
    css = (entry.get("css") or "").strip()
    primary = f"page.{loc}" if loc.startswith(("getBy", "locator(")) else None
    fallback = f"page.locator({json.dumps(css)})" if css else None
    return primary or fallback, fallback if primary else None

n = 0
for line in open(journal, encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    a = e.get("action")
    n += 1
    tag = f"{n:04d}"
    if a == "screenshot":
        (workdir / f"{tag}.note").write_text(e.get("note") or e.get("file", ""), encoding="utf-8")
        print(f"CHAPTER\t{tag}")
        continue
    if a == "goto":
        js = f"async page => {{ await page.goto({json.dumps(e.get('url', ''))}); }}"
        (workdir / f"{tag}.js").write_text(js, encoding="utf-8")
        print(f"CODE\t{tag}\t-")
        continue
    if a == "press" and not (e.get("locator") or e.get("css")):
        key = e.get("value") or e.get("key") or ""
        js = f"async page => {{ await page.keyboard.press({json.dumps(key)}); }}"
        (workdir / f"{tag}.js").write_text(js, encoding="utf-8")
        print(f"CODE\t{tag}\t-")
        continue

    if a in METHODS:
        method = METHODS[a]
    elif a == "fill":
        method = f"fill({json.dumps(e.get('value', ''))})"
    elif a == "select":
        method = f"selectOption({json.dumps(e.get('value', ''))})"
    elif a == "press":
        method = f"press({json.dumps(e.get('value') or e.get('key') or '')})"
    else:
        (workdir / f"{tag}.note").write_text(line, encoding="utf-8")
        print(f"SKIP\t{tag}")
        continue

    primary, fallback = sel(e)
    if primary is None:
        (workdir / f"{tag}.note").write_text(line, encoding="utf-8")
        print(f"SKIP\t{tag}")
        continue
    (workdir / f"{tag}.js").write_text(f"async page => {{ await {primary}.{method}; }}", encoding="utf-8")
    if fallback:
        (workdir / f"{tag}.fb.js").write_text(f"async page => {{ await {fallback}.{method}; }}", encoding="utf-8")
        print(f"CODE\t{tag}\tfb")
    else:
        print(f"CODE\t{tag}\t-")
PY

# --- drive the browser ------------------------------------------------------------------
pw open "$BASE_URL"        || { echo "ERROR: cannot open $BASE_URL" >&2; exit 1; }
pw resize 1280 800
[ -f "$AUTH" ] && pw state-load "$AUTH"
[ -n "$START_URL" ] && pw goto "$START_URL"
mkdir -p "$(dirname "$OUT")"
pw video-start "$OUT"      || { echo "ERROR: video-start failed" >&2; exit 1; }

FAILED=0
while IFS=$'\t' read -r type tag flag; do
    case "$type" in
        CODE)
            if ! pw run-code "$(cat "$WORKDIR/$tag.js")" >/dev/null 2>&1; then
                if [ "$flag" = "fb" ] && pw run-code "$(cat "$WORKDIR/$tag.fb.js")" >/dev/null 2>&1; then
                    :
                else
                    echo "WARN: step $tag failed: $(cat "$WORKDIR/$tag.js")" >&2
                    FAILED=$((FAILED + 1))
                fi
            fi
            sleep "$PACE"
            ;;
        CHAPTER)
            pw video-chapter "$(cat "$WORKDIR/$tag.note")" >/dev/null 2>&1 || true
            sleep "$PACE"
            ;;
        SKIP)
            echo "WARN: unreplayable journal line skipped: $(cat "$WORKDIR/$tag.note")" >&2
            ;;
    esac
done < "$WORKDIR/cmds.tsv"

pw video-stop
pw close

if [ -f "$OUT" ]; then
    echo "OK: $OUT ($(du -h "$OUT" | cut -f1)) — $FAILED failed step(s)"
    [ "$FAILED" -gt 0 ] && exit 3
    exit 0
fi
echo "ERROR: no video produced at $OUT" >&2
exit 1
