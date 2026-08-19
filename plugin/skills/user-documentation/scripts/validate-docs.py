#!/usr/bin/env python3
"""Mechanical gate for user-documentation output.

Usage:
    validate-docs.py <target-dir> [--embed wikilink|markdown|auto] [--video] [--strict]

Validates every `Flow - *.md` plus the `* - User Guide.md` index in <target-dir> against the
style-guide invariants (see references/determinism.md §4). Zero dependencies: PNG width is read
straight from the IHDR header. Exit code 1 when any ERROR is found; WARNINGs never fail the run
unless --strict.
"""

import argparse
import re
import sys
from pathlib import Path

PNG_NAME_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.png$")
WIKI_EMBED_RE = re.compile(r"!\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")
MD_EMBED_RE = re.compile(r"!\[[^\]]*\]\(<?([^)>]+?)>?\)")
WIKI_LINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:[|#][^\]]*)?\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(<?([^)>]+?)>?\)")
STEP_RE = re.compile(r"^(#{2,3}) Step (\d+)[:.]")
STATE_RE = re.compile(r"^(#{2,3}) State (\d+)[:.]")


def png_width(path: Path):
    try:
        with open(path, "rb") as f:
            head = f.read(24)
    except OSError:
        return None
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return None
    return int.from_bytes(head[16:20], "big")


def strip_code_fences(lines):
    out, fenced = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else ln)
    return out


class Doc:
    def __init__(self, path: Path, target: Path):
        self.path = path
        self.target = target
        self.raw = path.read_text(encoding="utf-8")
        self.lines = strip_code_fences(self.raw.splitlines())
        self.errors = []
        self.warnings = []

    @property
    def name(self):
        return self.path.name

    @property
    def basename(self):
        return self.path.stem

    def err(self, check, msg):
        self.errors.append((check, msg))

    def warn(self, check, msg):
        self.warnings.append((check, msg))

    # -- embeds ------------------------------------------------------------
    def embeds(self):
        """(syntax, raw-path) pairs for image/video embeds."""
        found = []
        for ln in self.lines:
            for m in WIKI_EMBED_RE.finditer(ln):
                found.append(("wikilink", m.group(1).strip()))
            for m in MD_EMBED_RE.finditer(ln):
                found.append(("markdown", m.group(1).strip().replace("%20", " ")))
        return found

    def png_embeds(self):
        return [(s, p) for s, p in self.embeds() if p.lower().endswith(".png")]

    def doc_links(self):
        links = []
        for ln in self.lines:
            for m in WIKI_LINK_RE.finditer(ln):
                links.append(m.group(1).strip())
            for m in MD_LINK_RE.finditer(ln):
                p = m.group(1).strip().replace("%20", " ")
                if p.lower().endswith(".md"):
                    links.append(Path(p).stem)
        return links


def check_frame(doc: Doc):
    if doc.lines and doc.lines[0].strip() == "---":
        doc.err("no-frontmatter", "file starts with frontmatter fence")
    first = next((ln for ln in doc.lines if ln.strip()), "")
    if first.strip() != f"# {doc.basename}":
        doc.err("h1-basename", f"H1 is {first.strip()!r}, expected '# {doc.basename}'")
    # --- between consecutive top-level sections
    h2_idx = [i for i, ln in enumerate(doc.lines) if ln.startswith("## ")]
    for a, b in zip(h2_idx, h2_idx[1:]):
        if not any(doc.lines[i].strip() == "---" for i in range(a + 1, b)):
            doc.err("hr-separators", f"no '---' between '{doc.lines[a].strip()}' and '{doc.lines[b].strip()}'")
    if "> [!" in doc.raw:
        doc.err("no-obsidian-callouts", "uses '> [!...]' callout; use '> **Note:**'")


def check_numbering(doc: Doc):
    h2_steps, h3_groups, states = [], {}, []
    cur_h2 = None
    for ln in doc.lines:
        if ln.startswith("## "):
            cur_h2 = ln
        m = STEP_RE.match(ln)
        if m:
            if m.group(1) == "##":
                h2_steps.append(int(m.group(2)))
            else:
                h3_groups.setdefault(cur_h2, []).append(int(m.group(2)))
        m = STATE_RE.match(ln)
        if m:
            states.append(int(m.group(2)))
    for label, seq in [("Step(##)", h2_steps)] + [
        (f"Step(### under {str(g).strip()[:40]})", s) for g, s in h3_groups.items()
    ] + [("State", states)]:
        if seq and seq != list(range(1, len(seq) + 1)):
            doc.err("step-numbering", f"{label} sequence {seq} is not gapless from 1")


def check_embeds(doc: Doc, is_index: bool, video: bool):
    pngs = doc.png_embeds()
    syntaxes = {s for s, _ in doc.embeds()}
    if len(syntaxes) > 1:
        doc.err("embed-syntax", f"mixed embed syntaxes in one doc: {sorted(syntaxes)}")
    lo = 0 if is_index else 1
    if not (lo <= len(pngs) <= 10):
        doc.err("embed-count", f"{len(pngs)} png embeds (allowed {lo}-10)")
    seen = set()
    last_num_per_dir = {}
    for _, rel in pngs:
        f = (doc.target / rel).resolve()
        if not f.is_file():
            doc.err("embed-exists", f"missing file: {rel}")
            continue
        if rel in seen:
            doc.warn("embed-duplicate", f"{rel} embedded more than once in this doc")
        seen.add(rel)
        base = f.name
        if not PNG_NAME_RE.match(base):
            doc.err("png-name", f"{base} does not match NN-kebab-state.png")
        else:
            num, d = int(base[:2]), str(f.parent)
            if last_num_per_dir.get(d, 0) > num:
                doc.warn("embed-order", f"{base} embedded after a higher-numbered shot from the same dir")
            last_num_per_dir[d] = max(last_num_per_dir.get(d, 0), num)
        w = png_width(f)
        if w is None:
            doc.err("png-width", f"{rel}: not a readable PNG")
        elif w > 780:
            doc.err("png-width", f"{rel} is {w}px wide (max 780; full views must be exactly 780)")
    # screencast embeds
    webms = [(s, p) for s, p in doc.embeds() if p.lower().endswith(".webm")]
    for _, rel in webms:
        if not (doc.target / rel).resolve().is_file():
            doc.err("screencast", f"missing screencast file: {rel}")
    if video and "## Screencast" in doc.raw and not webms:
        doc.err("screencast", "has a '## Screencast' section but no .webm embed")


def check_related(doc: Doc, flow_stems: set):
    in_section = False
    for ln in doc.lines:
        if ln.startswith("## "):
            in_section = ln.strip() == "## Related Flows"
            continue
        if in_section:
            for name in (WIKI_LINK_RE.findall(ln) or []) + [Path(p).stem for p in MD_LINK_RE.findall(ln) if p.lower().endswith(".md")]:
                stem = name.strip()
                if stem not in flow_stems and not (doc.target / f"{stem}.md").is_file():
                    doc.err("related-flows", f"link target not found: {stem}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--embed", choices=["wikilink", "markdown", "auto"], default="auto")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings also fail the run")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"ERROR: target dir not found: {target}")
        return 1

    flow_paths = sorted(target.glob("Flow - *.md"))
    index_paths = sorted(target.glob("* - User Guide.md"))
    if not flow_paths:
        print(f"ERROR: no 'Flow - *.md' documents in {target}")
        return 1

    docs = [Doc(p, target) for p in flow_paths + index_paths]
    flow_stems = {p.stem for p in flow_paths}

    for doc in docs:
        is_index = doc.path in index_paths
        check_frame(doc)
        check_numbering(doc)
        check_embeds(doc, is_index, args.video)
        check_related(doc, flow_stems)

    # one embed syntax across the whole target, matching --embed
    global_syntaxes = {s for d in docs for s, _ in d.embeds()}
    global_errors = []
    if len(global_syntaxes) > 1:
        global_errors.append(("embed-syntax", f"mixed embed syntaxes across docs: {sorted(global_syntaxes)}"))
    elif args.embed != "auto" and global_syntaxes and global_syntaxes != {args.embed}:
        global_errors.append(("embed-syntax", f"docs use {global_syntaxes.pop()}, manifest mode is {args.embed}"))

    # index must link every flow
    if not index_paths:
        global_errors.append(("index-links-flows", "no '* - User Guide.md' index found"))
    else:
        linked = {s for idx in index_paths for s in Doc(idx, target).doc_links()}
        for stem in sorted(flow_stems - linked):
            global_errors.append(("index-links-flows", f"index does not link '{stem}'"))

    # orphan PNGs: reference pool = ALL .md files in the target dir
    referenced = set()
    for md in target.glob("*.md"):
        for _, rel in Doc(md, target).png_embeds():
            referenced.add((target / rel).resolve())
    shots_dir = target / "screenshots"
    global_warnings = []
    if shots_dir.is_dir():
        for png in sorted(shots_dir.rglob("*.png")):
            if png.resolve() not in referenced:
                global_errors.append(("orphan-png", f"never embedded: {png.relative_to(target)}"))

    if args.video and not any("## Screencast" in d.raw for d in docs):
        global_errors.append(("screencast", "--video set but no doc has a '## Screencast' section"))

    # ---- report -----------------------------------------------------------
    n_err = n_warn = 0
    for doc in docs:
        if not doc.errors and not doc.warnings:
            print(f"✓ {doc.name}")
            continue
        print(f"{'✗' if doc.errors else '⚠'} {doc.name}")
        for check, msg in doc.errors:
            print(f"    ERROR {check}: {msg}")
            n_err += 1
        for check, msg in doc.warnings:
            print(f"    warn  {check}: {msg}")
            n_warn += 1
    if global_errors or global_warnings:
        print("GLOBAL (whole target dir)")
        for check, msg in global_errors:
            print(f"    ERROR {check}: {msg}")
            n_err += 1
        for check, msg in global_warnings:
            print(f"    warn  {check}: {msg}")
            n_warn += 1

    print(f"\nSUMMARY: {n_err} error(s), {n_warn} warning(s) across {len(docs)} doc(s)")
    return 1 if n_err or (args.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
