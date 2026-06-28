#!/usr/bin/env python3
"""Aviatri.com Wayback snapshot harness. Same logic as Aviloop runner, target swapped."""
from __future__ import annotations
import os, json, re, time, sys
import urllib.request, urllib.parse
import difflib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
SNAPSHOTS = ROOT / "snapshots"
EXTRACTED = ROOT / "extracted"
TIMELINE = ROOT / "TIMELINE.md"

TARGET_URL = "aviatri.com"
START_YEAR = 2014
DELAY_BETWEEN_REQUESTS = 1.2
USER_AGENT = "obsidianwatch-aviatri-research/1.0"

def fetch_cdx_index():
    qs = urllib.parse.urlencode({
        "url": TARGET_URL, "output": "json",
        "fl": "timestamp,original,statuscode,digest,length",
        "collapse": "digest", "from": f"{START_YEAR}0101",
    })
    url = f"http://web.archive.org/cdx/search/cdx?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if not data: return []
    return [{"timestamp": row[0], "original": row[1], "statuscode": row[2],
             "digest": row[3], "length": row[4]}
            for row in data[1:] if row[2] == "200"]

def fetch_snapshot(ts: str, original: str) -> bytes:
    url = f"https://web.archive.org/web/{ts}id_/{original}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

class TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript"}
    def __init__(self):
        super().__init__()
        self.parts, self.skip_depth = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS: self.skip_depth += 1
    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth > 0: self.skip_depth -= 1
    def handle_data(self, data):
        if self.skip_depth == 0:
            t = data.strip()
            if t: self.parts.append(t)

def extract_text(html: str) -> str:
    ex = TextExtractor()
    try: ex.feed(html)
    except Exception: pass
    parts, prev = [], None
    for p in ex.parts:
        p = re.sub(r"\s+", " ", p)
        if p != prev: parts.append(p); prev = p
    return "\n".join(parts)

def extract_meta(html: str) -> dict:
    meta = {}
    m = re.search(r"<title[^>]*>([^<]*)</title>", html, re.IGNORECASE)
    if m: meta["title"] = m.group(1).strip()
    for pat in [
        ('og:description', r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)'),
        ('description',    r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)'),
        ('og:title',       r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)'),
    ]:
        m = re.search(pat[1], html, re.IGNORECASE)
        if m: meta[pat[0]] = m.group(1).strip()
    return meta

def fmt_ts(ts): return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"

def main():
    log = lambda m: print(m, flush=True)
    log(f"[{time.strftime('%H:%M:%S')}] fetching CDX index for {TARGET_URL} from {START_YEAR}-01-01")
    snapshots = fetch_cdx_index()
    log(f"[{time.strftime('%H:%M:%S')}] {len(snapshots)} unique-content snapshots returned")
    if not snapshots:
        log("nothing to do"); return
    snapshots.sort(key=lambda s: s["timestamp"])

    for i, snap in enumerate(snapshots, 1):
        ts = snap["timestamp"]
        path = SNAPSHOTS / f"{ts}.html"
        if path.exists(): continue
        try:
            data = fetch_snapshot(ts, snap["original"])
            path.write_bytes(data)
            log(f"[{time.strftime('%H:%M:%S')}] {i:>3}/{len(snapshots)}  ✓ {ts}  {len(data)//1024} KB")
        except Exception as e:
            log(f"[{time.strftime('%H:%M:%S')}] {i:>3}/{len(snapshots)}  ✗ {ts}  {e}")
        time.sleep(DELAY_BETWEEN_REQUESTS)

    log("extracting...")
    extracted = []
    for snap in snapshots:
        ts = snap["timestamp"]
        html_path = SNAPSHOTS / f"{ts}.html"
        if not html_path.exists(): continue
        html = html_path.read_text(errors="ignore")
        text = extract_text(html)
        meta = extract_meta(html)
        (EXTRACTED / f"{ts}.txt").write_text(text)
        (EXTRACTED / f"{ts}.meta.json").write_text(json.dumps(meta, indent=2))
        extracted.append((ts, text, meta))

    log(f"writing TIMELINE.md ({len(extracted)} snapshots)")
    out = [f"# Aviatri.com Wayback Timeline", "",
           f"Source: {TARGET_URL} CDX index from {START_YEAR}-01-01.",
           f"Unique snapshots: **{len(extracted)}**", ""]
    prev_text, prev_meta, prev_ts = "", {}, None
    for ts, text, meta in extracted:
        diff_lines = list(difflib.unified_diff(prev_text.splitlines(), text.splitlines(), n=0, lineterm=""))
        added = [l[1:].strip() for l in diff_lines if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
        removed = [l[1:].strip() for l in diff_lines if l.startswith("-") and not l.startswith("---") and l[1:].strip()]
        out.append(f"\n## {fmt_ts(ts)}  ({len(text)} chars)")
        out.append(f"Replay: https://web.archive.org/web/{ts}/https://www.{TARGET_URL}/")
        out.append(f"\n- **Title:** {meta.get('title','')}")
        if meta.get('og:description'): out.append(f"- **Description:** {meta['og:description']}")
        if prev_ts:
            out.append(f"- **Diff vs {fmt_ts(prev_ts)}:** +{len(added)} / -{len(removed)} text lines")
            for line in added[:10]: out.append(f"  - + {line[:240]}")
            for line in removed[:10]: out.append(f"  - - {line[:240]}")
        prev_text, prev_meta, prev_ts = text, meta, ts
    TIMELINE.write_text("\n".join(out))
    log("done")

if __name__ == "__main__":
    main()
