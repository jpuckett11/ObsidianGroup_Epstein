#!/usr/bin/env python3
"""
Re-extract visible body text from Wix-rendered Aviloop snapshots.
Wix embeds the actual page copy inside heavily-styled inline HTML, so the
standard HTMLParser pass left most of it behind. This pass strips
scripts/styles/comments and *all* HTML tags, then normalizes whitespace
and dedupes lines.
"""
import re, json, html, difflib
from pathlib import Path

ROOT = Path(__file__).parent
SNAPSHOTS = ROOT / "snapshots"
EXTRACTED = ROOT / "extracted"
TIMELINE = ROOT / "TIMELINE_v2.md"

def visible_text(raw: str) -> str:
    s = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<noscript\b[^>]*>.*?</noscript>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[\xa0​ ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    sentences = re.split(r"(?<=[\.!\?])\s+(?=[A-Z])", s)
    out, prev = [], None
    for snt in sentences:
        snt = snt.strip()
        if len(snt) < 15:
            continue
        if snt == prev:
            continue
        out.append(snt)
        prev = snt
    return "\n".join(out)

def fmt_ts(ts: str) -> str:
    return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"

def main():
    files = sorted(SNAPSHOTS.glob("*.html"))
    extracted = []
    for path in files:
        ts = path.stem
        raw = path.read_text(errors="ignore")
        text = visible_text(raw)
        out_path = EXTRACTED / f"{ts}.body.txt"
        out_path.write_text(text)
        extracted.append((ts, text, len(text)))

    sizes = [(ts, n) for ts, _, n in extracted]
    biggest = sorted(sizes, key=lambda x: -x[1])[:5]
    smallest = sorted([s for s in sizes if s[1] > 0])[:5]
    print(f"snapshots: {len(extracted)}")
    print(f"largest body text: {biggest}")
    print(f"smallest non-empty: {smallest}")

    # Pairwise diff timeline
    out = [
        "# Aviloop.com Wayback Timeline (v2)",
        "",
        f"Re-extracted visible body text from Wix-rendered HTML.",
        f"Source: Wayback Machine snapshots, deduplicated by content digest, from 2018-01-01.",
        f"Total snapshots: **{len(extracted)}**.",
        "",
    ]
    prev_ts, prev_text = None, ""
    for ts, text, _ in extracted:
        if prev_text:
            diff_lines = list(difflib.unified_diff(prev_text.splitlines(), text.splitlines(), n=0, lineterm=""))
            added = [l[1:].strip() for l in diff_lines if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
            removed = [l[1:].strip() for l in diff_lines if l.startswith("-") and not l.startswith("---") and l[1:].strip()]
        else:
            added, removed = [], []
        out.append(f"\n## {fmt_ts(ts)}  ({len(text)} chars)")
        out.append(f"\nReplay: https://web.archive.org/web/{ts}/https://www.aviloop.com/\n")
        if prev_ts:
            out.append(f"**Diff vs {fmt_ts(prev_ts)}**: +{len(added)} / -{len(removed)} sentences")
            if added:
                out.append("\n**Added:**")
                for line in added[:25]:
                    out.append(f"- {line[:400]}")
                if len(added) > 25:
                    out.append(f"- ... and {len(added) - 25} more")
            if removed:
                out.append("\n**Removed:**")
                for line in removed[:25]:
                    out.append(f"- {line[:400]}")
                if len(removed) > 25:
                    out.append(f"- ... and {len(removed) - 25} more")
        prev_ts, prev_text = ts, text
    TIMELINE.write_text("\n".join(out))
    print(f"wrote {TIMELINE.name} ({TIMELINE.stat().st_size//1024} KB)")

if __name__ == "__main__":
    main()
