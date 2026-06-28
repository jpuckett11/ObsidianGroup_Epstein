#!/usr/bin/env python3
"""
EFTA bates window pull. Centered on EFTA01795680 (Marcinkova/Negroni email),
fetches a ±50 bates window via Wayback Machine (bypassing DOJ age-gate),
extracts text, and surfaces every email by date with sender / recipient
artifacts so the conversation around January 22, 2015 can be reconstructed.
"""
import os, time, re, json, subprocess, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "window_pdfs"
TXT_DIR = ROOT / "window_txt"
PDF_DIR.mkdir(exist_ok=True)
TXT_DIR.mkdir(exist_ok=True)

CENTER = 1795680
WINDOW = 50
DOJ_BASE = "https://www.justice.gov/epstein/files/DataSet%2010/EFTA{}.pdf"
WAYBACK_AVAIL = "http://archive.org/wayback/available?url={}"
WAYBACK_REPLAY = "https://web.archive.org/web/{}id_/{}"

def avail(target):
    try:
        url = WAYBACK_AVAIL.format(target)
        with urllib.request.urlopen(url, timeout=20) as r:
            d = json.load(r)
        s = d.get("archived_snapshots", {}).get("closest")
        return s["timestamp"] if s and s.get("status") == "200" else None
    except Exception:
        return None

def fetch_pdf(ts, target, out_path):
    url = WAYBACK_REPLAY.format(ts, target)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        out_path.write_bytes(data)
        return len(data)
    except Exception as e:
        return 0

def extract_text(pdf_path, txt_path):
    try:
        subprocess.run(["pdftotext", str(pdf_path), str(txt_path)], timeout=30, capture_output=True)
        return txt_path.read_text(errors="ignore")
    except Exception:
        return ""

# Date patterns to surface
DATE_PAT = re.compile(
    r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?,?\s*"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"\d{1,2},?\s+(20\d{2})", re.IGNORECASE)
JAN_22_2015 = re.compile(r"January\s+22,?\s+2015", re.IGNORECASE)
FROM_PAT = re.compile(r"^From:\s*([^\n]+)", re.IGNORECASE | re.MULTILINE)
TO_PAT = re.compile(r"^To:\s*([^\n]+)", re.IGNORECASE | re.MULTILINE)
SUBJ_PAT = re.compile(r"^Subject:\s*([^\n]+)", re.IGNORECASE | re.MULTILINE)

def main():
    candidates = list(range(CENTER - WINDOW, CENTER + WINDOW + 1))
    print(f"window: EFTA{CENTER - WINDOW:08d} .. EFTA{CENTER + WINDOW:08d} ({len(candidates)} bates)")
    summary = []
    for n in candidates:
        bates = f"{n:08d}"
        pdf_path = PDF_DIR / f"EFTA{bates}.pdf"
        txt_path = TXT_DIR / f"EFTA{bates}.txt"
        if not pdf_path.exists():
            target = DOJ_BASE.format(bates)
            ts = avail(target)
            if not ts:
                print(f"  EFTA{bates}  no wayback capture")
                summary.append({"bates": bates, "status": "no_capture"})
                time.sleep(0.4)
                continue
            sz = fetch_pdf(ts, target, pdf_path)
            if sz < 1000:
                print(f"  EFTA{bates}  fetch failed ({sz} bytes)")
                summary.append({"bates": bates, "status": "fetch_failed"})
                time.sleep(0.4)
                continue
        # extract text
        if not txt_path.exists() or txt_path.stat().st_size == 0:
            extract_text(pdf_path, txt_path)
        text = txt_path.read_text(errors="ignore")
        dates = DATE_PAT.findall(text)
        is_jan22 = bool(JAN_22_2015.search(text))
        from_field = FROM_PAT.findall(text)
        to_field = TO_PAT.findall(text)
        subj_field = SUBJ_PAT.findall(text)
        summary.append({
            "bates": bates,
            "status": "ok",
            "size": pdf_path.stat().st_size,
            "dates": dates[:3],
            "is_jan22_2015": is_jan22,
            "from": [f.strip()[:80] for f in from_field][:3],
            "to": [t.strip()[:80] for t in to_field][:3],
            "subject": [s.strip()[:120] for s in subj_field][:3],
            "preview": text[:200].replace("\n", " "),
        })
        marker = "🔥 JAN-22-2015" if is_jan22 else ""
        print(f"  EFTA{bates}  ok  {marker}")
        time.sleep(0.3)
    # write summary
    (ROOT / "WINDOW_SUMMARY.json").write_text(json.dumps(summary, indent=2))
    # surface Jan 22 hits
    jan_hits = [s for s in summary if s.get("is_jan22_2015")]
    print(f"\n=== JANUARY 22, 2015 HITS: {len(jan_hits)} ===")
    for h in jan_hits:
        print(f"\nEFTA{h['bates']}")
        print(f"  From: {h.get('from', [])}")
        print(f"  To:   {h.get('to', [])}")
        print(f"  Subj: {h.get('subject', [])}")
        print(f"  Preview: {h['preview']}")

if __name__ == "__main__":
    main()
