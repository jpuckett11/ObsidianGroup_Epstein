#!/usr/bin/env python3
"""
Aviloop.com Wayback Machine snapshot timeline harness.

Pulls every 200-OK snapshot of aviloop.com from 2018 forward, dedupes by
content digest, downloads the raw HTML via the id_ replay endpoint
(no Wayback toolbar), extracts visible text + key metadata, and diffs
consecutive snapshots to produce a timeline of what changed when.

Output:
    snapshots/{timestamp}.html      raw HTML per unique snapshot
    extracted/{timestamp}.txt       normalized visible text per snapshot
    extracted/{timestamp}.meta.json structured metadata per snapshot
    TIMELINE.md                     human-readable change timeline
"""
from __future__ import annotations
import os, json, re, time, sys
import urllib.request, urllib.parse
import difflib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
SNAPSHOTS = ROOT / "snapshots"
EXTRACTED = ROOT / "extracted"
TIMELINE  = ROOT / "TIMELINE.md"

TARGET_URL = "aviloop.com"
START_YEAR = 2018
DELAY_BETWEEN_REQUESTS = 1.2  # be polite to the Wayback Machine
USER_AGENT = "obsidianwatch-aviloop-research/1.0"

# --- CDX index fetch ---------------------------------------------------------

def fetch_cdx_index():
    """Get list of all snapshots from CDX server. Dedupe by digest within URL."""
    qs = urllib.parse.urlencode({
        "url": TARGET_URL,
        "output": "json",
        "fl": "timestamp,original,statuscode,digest,length",
        "collapse": "digest",  # WM-side dedupe by content fingerprint
        "from": f"{START_YEAR}0101",
    })
    url = f"http://web.archive.org/cdx/search/cdx?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    if not data:
        return []
    return [
        {"timestamp": row[0], "original": row[1], "statuscode": row[2],
         "digest": row[3], "length": row[4]}
        for row in data[1:]
        if row[2] == "200"
    ]

# --- Snapshot fetch ----------------------------------------------------------

def fetch_snapshot(ts: str, original: str) -> bytes:
    """Pull raw HTML from Wayback id_ endpoint (no toolbar overlay)."""
    url = f"https://web.archive.org/web/{ts}id_/{original}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

# --- Text extraction ---------------------------------------------------------

class TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "noscript"}
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip_depth = 0
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
    def handle_data(self, data):
        if self.skip_depth == 0:
            t = data.strip()
            if t:
                self.parts.append(t)

def extract_meta(html: str) -> dict:
    meta = {}
    m = re.search(r"<title[^>]*>([^<]*)</title>", html, re.IGNORECASE)
    if m: meta["title"] = m.group(1).strip()
    for pat in [
        ('og:description', r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)'),
        ('description',    r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)'),
        ('og:title',       r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)'),
        ('og:image',       r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)'),
    ]:
        m = re.search(pat[1], html, re.IGNORECASE)
        if m: meta[pat[0]] = m.group(1).strip()
    # Wix structured data, often in inline JSON blobs
    for sd in re.finditer(r'application/ld\+json[^>]*>([^<]+)', html):
        try:
            parsed = json.loads(sd.group(1))
            meta.setdefault("ld_json", []).append(parsed)
        except Exception:
            pass
    return meta

def extract_text(html: str) -> str:
    ex = TextExtractor()
    try:
        ex.feed(html)
    except Exception:
        pass
    # Collapse runs of whitespace, dedupe consecutive duplicates
    parts = []
    prev = None
    for p in ex.parts:
        p = re.sub(r"\s+", " ", p)
        if p != prev:
            parts.append(p)
            prev = p
    return "\n".join(parts)

# --- Diff and timeline -------------------------------------------------------

def diff_summary(prev_text: str, curr_text: str, max_lines: int = 12) -> dict:
    prev_lines = prev_text.splitlines()
    curr_lines = curr_text.splitlines()
    added = []
    removed = []
    for line in difflib.unified_diff(prev_lines, curr_lines, n=0, lineterm=""):
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("+") and line[1:].strip():
            added.append(line[1:].strip())
        elif line.startswith("-") and line[1:].strip():
            removed.append(line[1:].strip())
    return {
        "added_count": len(added),
        "removed_count": len(removed),
        "added_sample": added[:max_lines],
        "removed_sample": removed[:max_lines],
    }

def fmt_ts(ts: str) -> str:
    return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"

# --- Main --------------------------------------------------------------------

def main():
    log = lambda m: (print(m, flush=True),)
    log(f"[{time.strftime('%H:%M:%S')}] fetching CDX index for {TARGET_URL} from {START_YEAR}-01-01...")
    snapshots = fetch_cdx_index()
    log(f"[{time.strftime('%H:%M:%S')}] {len(snapshots)} unique-content snapshots returned by CDX")

    if not snapshots:
        log("nothing to do")
        return

    snapshots.sort(key=lambda s: s["timestamp"])

    # Step 1: download anything we don't already have
    for i, snap in enumerate(snapshots, 1):
        ts = snap["timestamp"]
        path = SNAPSHOTS / f"{ts}.html"
        if path.exists():
            continue
        try:
            data = fetch_snapshot(ts, snap["original"])
            path.write_bytes(data)
            log(f"[{time.strftime('%H:%M:%S')}] {i:>3}/{len(snapshots)}  ✓ {ts}  {len(data)//1024} KB")
        except Exception as e:
            log(f"[{time.strftime('%H:%M:%S')}] {i:>3}/{len(snapshots)}  ✗ {ts}  {e}")
        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Step 2: extract text and metadata
    log("extracting text + metadata...")
    extracted = []
    for snap in snapshots:
        ts = snap["timestamp"]
        html_path = SNAPSHOTS / f"{ts}.html"
        if not html_path.exists():
            continue
        try:
            html = html_path.read_text(errors="ignore")
        except Exception:
            continue
        text = extract_text(html)
        meta = extract_meta(html)
        (EXTRACTED / f"{ts}.txt").write_text(text)
        (EXTRACTED / f"{ts}.meta.json").write_text(json.dumps(meta, indent=2))
        extracted.append((ts, text, meta))
    log(f"extracted {len(extracted)} snapshots")

    # Step 3: diff sequential, produce timeline
    timeline_rows = []
    prev_ts, prev_text, prev_meta = None, "", {}
    for ts, text, meta in extracted:
        diff = diff_summary(prev_text, text)
        title_changed = prev_meta.get("title") != meta.get("title")
        desc_changed = prev_meta.get("og:description") != meta.get("og:description")
        timeline_rows.append({
            "ts": ts,
            "prev_ts": prev_ts,
            "title": meta.get("title", ""),
            "title_changed": title_changed,
            "description": meta.get("og:description", ""),
            "desc_changed": desc_changed,
            "diff": diff,
        })
        prev_ts, prev_text, prev_meta = ts, text, meta

    # Step 4: write TIMELINE.md
    out = [
        "# Aviloop.com Wayback Timeline\n",
        f"\nSource: Wayback Machine CDX index for `{TARGET_URL}`, 200-OK responses,",
        f" content-digest deduplicated. Range: {START_YEAR}-01-01 onward.",
        f" Unique snapshots: **{len(extracted)}**.\n",
    ]
    for i, row in enumerate(timeline_rows):
        ts_fmt = fmt_ts(row["ts"])
        out.append(f"\n## {ts_fmt}  (snapshot {i+1}/{len(timeline_rows)})")
        out.append(f"\nReplay: https://web.archive.org/web/{row['ts']}/https://www.aviloop.com/")
        out.append(f"\n- **Title:** {row['title']}")
        if row['title_changed'] and row['prev_ts']:
            out.append(f"  - *changed from previous*")
        if row.get("description"):
            out.append(f"\n- **Description:** {row['description']}")
            if row['desc_changed'] and row['prev_ts']:
                out.append(f"  - *changed from previous*")
        d = row["diff"]
        if row['prev_ts']:
            out.append(f"\n- **Diff vs {fmt_ts(row['prev_ts'])}:** +{d['added_count']} / -{d['removed_count']} text lines")
            if d['added_sample']:
                out.append("  - **Added (sample):**")
                for line in d['added_sample']:
                    out.append(f"    - {line[:240]}")
            if d['removed_sample']:
                out.append("  - **Removed (sample):**")
                for line in d['removed_sample']:
                    out.append(f"    - {line[:240]}")

    TIMELINE.write_text("\n".join(out))
    log(f"wrote TIMELINE.md ({TIMELINE.stat().st_size//1024} KB)")
    log("done.")

if __name__ == "__main__":
    main()
