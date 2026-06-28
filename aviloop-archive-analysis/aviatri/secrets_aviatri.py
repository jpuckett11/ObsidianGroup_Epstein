#!/usr/bin/env python3
"""
Secrets extractor for archived Wix sites.

Pulls every identifier-like artifact from snapshot HTML:
    - email addresses
    - phone numbers (US + intl format)
    - social media handles and profile URLs
    - HTML comments (often leak vendor TODOs, edit notes)
    - Wix site IDs, page IDs, master page IDs
    - Google Analytics UA-/G- IDs, GTM IDs, Facebook pixel IDs
    - Site verification codes (Google, Bing, Pinterest)
    - Linked image URLs from wixstatic CDN (filenames sometimes leak)
    - Linked PDF/document URLs
    - Subdomain mentions
    - Internal Wix admin IDs (siteOwnerId etc)

Produces SECRETS.md report with grouping by category and first-seen-on date.
"""
import re, json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/obsidian/ObsidianGroup_Epstein/aviloop-archive-analysis/aviatri")
SNAPSHOTS = ROOT / "snapshots"
OUT = ROOT / "SECRETS.md"

# --- Patterns ---------------------------------------------------------------
PAT = {
    "email":             re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"),
    "phone_us":          re.compile(r"(?:\+?1[\s\-.])?\(?\d{3}\)?[\s\-.]\d{3}[\s\-.]\d{4}"),
    "phone_intl":        re.compile(r"\+\d{1,3}[\s\-.]?\(?\d{1,4}\)?[\s\-.]\d{1,4}[\s\-.]\d{1,4}(?:[\s\-.]\d{1,4})?"),
    "linkedin":          re.compile(r"linkedin\.com/(?:in|company|pub)/[a-zA-Z0-9\-_.]+"),
    "twitter_x":         re.compile(r"(?:twitter\.com|x\.com)/[a-zA-Z0-9_]+"),
    "instagram":         re.compile(r"instagram\.com/[a-zA-Z0-9_.]+"),
    "facebook":          re.compile(r"facebook\.com/[a-zA-Z0-9_.\-]+"),
    "youtube":           re.compile(r"youtube\.com/(?:user|channel|c|@)[/]?[a-zA-Z0-9_\-.@]+"),
    "html_comment":      re.compile(r"<!--((?:(?!-->).)+)-->", re.DOTALL),
    "wix_metaSiteId":    re.compile(r'(?:metaSiteId|meta_?site_?id)[\"\\\']?\s*[:=]\s*[\"\\\']([a-f0-9\-]{8,})', re.IGNORECASE),
    "wix_siteId":        re.compile(r'(?:^|\W)siteId[\"\\\']?\s*[:=]\s*[\"\\\']([a-f0-9\-]{8,})', re.IGNORECASE),
    "wix_userId":        re.compile(r'(?:userId|ownerId|siteOwnerId)[\"\\\']?\s*[:=]\s*[\"\\\']([a-f0-9\-]{8,})', re.IGNORECASE),
    "wix_pageId":        re.compile(r'(?:pageId|masterPageId)[\"\\\']?\s*[:=]\s*[\"\\\']([a-zA-Z0-9_\-]+)', re.IGNORECASE),
    "google_analytics":  re.compile(r"UA-\d{4,10}-\d{1,4}|G-[A-Z0-9]{6,12}"),
    "gtm":               re.compile(r"GTM-[A-Z0-9]{4,9}"),
    "fb_pixel":          re.compile(r"fbq\([\"'](?:init|track)[\"'][^)]*[\"']?(\d{12,18})[\"']?"),
    "google_verify":     re.compile(r'name=[\"\\\']google-site-verification[\"\\\']\s+content=[\"\\\']([a-zA-Z0-9_\-]+)'),
    "bing_verify":       re.compile(r'name=[\"\\\']msvalidate\.01[\"\\\']\s+content=[\"\\\']([a-zA-Z0-9_\-]+)'),
    "wixstatic_img":     re.compile(r'https?://static\.wixstatic\.com/media/([a-zA-Z0-9~_.\-]+?\.(?:jpg|jpeg|png|gif|webp|svg))', re.IGNORECASE),
    "pdf_doc":           re.compile(r'https?://[^\s\'\"<>]+\.(?:pdf|docx?|xlsx?|pptx?|csv)', re.IGNORECASE),
    "subdomain":         re.compile(r'\b([a-zA-Z][a-zA-Z0-9\-]*)\.aviloop\.com\b', re.IGNORECASE),
}

# Strip Wayback's iframe injects that pollute results
WAYBACK_NOISE = re.compile(r"web\.archive\.org|archive\.org|wmwave|playback\.js|wombat|web-static")

def is_noise(value: str) -> bool:
    return bool(WAYBACK_NOISE.search(value))

def is_valid_email(e: str) -> bool:
    if is_noise(e): return False
    bad_domains = ("wixpress.com", "wix.com", "example.com", "example.org", "sentry.io",
                   "google.com", "googletagmanager.com", "youtube.com")
    return not any(e.lower().endswith("@" + d) or e.lower().endswith("." + d) for d in bad_domains)

def is_valid_phone(p: str) -> bool:
    digits = re.sub(r"\D", "", p)
    return 7 <= len(digits) <= 15

# --- Main ------------------------------------------------------------------
def collect():
    findings = defaultdict(lambda: defaultdict(list))  # category -> value -> [(ts, count)]
    for path in sorted(SNAPSHOTS.glob("*.html")):
        ts = path.stem
        html = path.read_text(errors="ignore")
        for name, pat in PAT.items():
            for m in pat.finditer(html):
                raw_val = m.group(1) if m.groups() else m.group(0)
                val = raw_val.strip()
                if not val: continue
                if name in ("wixstatic_img", "pdf_doc"):
                    if is_noise(val): continue
                if name == "email":
                    if not is_valid_email(val): continue
                if name in ("phone_us", "phone_intl"):
                    if not is_valid_phone(val): continue
                if name == "html_comment":
                    # only keep substantive comments, skip wayback boilerplate
                    if is_noise(val): continue
                    val = re.sub(r"\s+", " ", val).strip()
                    if len(val) < 20: continue
                if len(val) > 600: continue  # skip giant blobs
                findings[name][val].append(ts)
    return findings

def write_report(findings):
    out = [
        "# Aviatri.com Secrets Extraction",
        "",
        f"Source: {len(list(SNAPSHOTS.glob('*.html')))} Wayback snapshots from 2018-01-01 forward.",
        "Method: pattern extraction across all snapshot HTML.",
        "",
        "Wayback Machine and Wix internal infrastructure URLs filtered out.",
        "",
    ]
    label = {
        "email":            "## Emails",
        "phone_us":         "## US-format Phone Numbers",
        "phone_intl":       "## International-format Phone Numbers",
        "linkedin":         "## LinkedIn",
        "twitter_x":        "## Twitter / X",
        "instagram":        "## Instagram",
        "facebook":         "## Facebook",
        "youtube":          "## YouTube",
        "html_comment":     "## HTML Comments",
        "wix_metaSiteId":   "## Wix Meta Site ID",
        "wix_siteId":       "## Wix Site ID",
        "wix_userId":       "## Wix Owner / User ID",
        "wix_pageId":       "## Wix Page IDs",
        "google_analytics": "## Google Analytics IDs",
        "gtm":              "## Google Tag Manager IDs",
        "fb_pixel":         "## Facebook Pixel IDs",
        "google_verify":    "## Google Site Verification Codes",
        "bing_verify":      "## Bing Site Verification Codes",
        "wixstatic_img":    "## Image Filenames on Wix CDN",
        "pdf_doc":          "## PDF / Office Document URLs",
        "subdomain":        "## Subdomains Mentioned",
    }
    for cat, hdr in label.items():
        if cat not in findings or not findings[cat]:
            continue
        out.append(hdr)
        items = sorted(findings[cat].items(), key=lambda x: x[1][0])  # by first seen
        for val, ts_list in items[:200]:
            first = ts_list[0]
            last = ts_list[-1]
            cnt = len(ts_list)
            first_fmt = f"{first[:4]}-{first[4:6]}-{first[6:8]}"
            last_fmt = f"{last[:4]}-{last[4:6]}-{last[6:8]}"
            display = val if len(val) < 200 else val[:200] + "…"
            out.append(f"- `{display}`  · first seen {first_fmt}, last seen {last_fmt}, {cnt} snapshots")
        if len(items) > 200:
            out.append(f"- ... and {len(items) - 200} more unique values")
        out.append("")
    OUT.write_text("\n".join(out))
    print(f"wrote {OUT.name} ({OUT.stat().st_size//1024} KB)")
    print(f"categories with hits: {sum(1 for c in label if findings.get(c))}")

if __name__ == "__main__":
    findings = collect()
    write_report(findings)
