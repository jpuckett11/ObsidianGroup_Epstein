#!/usr/bin/env python3
"""
Aggressive Wix-aware extractor. Drops inline base64 data URIs, strips all
HTML/CSS, then keyword-walks the result to pull only sentences that contain
domain-relevant terms. Output is the clean factual body of each snapshot,
suitable for diffing.
"""
import re, html as html_mod
from pathlib import Path

ROOT = Path(__file__).parent
SNAPSHOTS = ROOT / "snapshots"
EXTRACTED = ROOT / "extracted"

# Strong filter: only keep sentences mentioning these terms.
# These are the actual aviloop content keywords.
KEYWORDS = re.compile(
    r"\b(Aviloop|Nadia|Marcink|aviation|pilot|flight|airline|cabin|"
    r"marketing|brand|promotion|campaign|conference|event|trade.?show|"
    r"contact|home|service|about|client|Gulfstream|Boeing|ATP|"
    r"instructor|charter|team\s+building|targeted|launched|founded|"
    r"based|located|@aviloop|info@|hello@|nadia@|@gmail|@hotmail|"
    r"LinkedIn|Instagram|Twitter|Facebook|Manhattan|New York|NYC|"
    r"301|66th|East 66th|Park Avenue|Madison)\b",
    re.IGNORECASE,
)

def is_clean_ascii(s: str) -> bool:
    if not s: return False
    ascii_pct = sum(1 for c in s if 32 <= ord(c) < 127) / len(s)
    return ascii_pct > 0.95

def visible_clean(raw: str) -> list[str]:
    s = raw
    # 1. drop wayback machine wrapping
    s = re.sub(r"<!--\s*BEGIN WAYBACK TOOLBAR INSERT.*?END WAYBACK TOOLBAR INSERT\s*-->", "", s, flags=re.DOTALL)
    # 2. drop scripts, styles, noscript, and HTML comments
    s = re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<noscript\b[^>]*>.*?</noscript>", "", s, flags=re.DOTALL | re.IGNORECASE)
    # 3. drop inline base64 data URIs (font embeds, image embeds)
    s = re.sub(r'data:[^;]+;base64,[A-Za-z0-9+/=]{20,}', '', s)
    # 4. strip all HTML tags
    s = re.sub(r"<[^>]+>", " ", s)
    # 5. unescape entities
    s = html_mod.unescape(s)
    # 6. normalize whitespace
    s = re.sub(r"[ ​  ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    # 7. break into sentences
    sentences = re.split(r"(?<=[\.!\?])\s+(?=[A-Z])", s)
    # 8. keyword filter + ascii filter + length filter + dedupe
    out, seen = [], set()
    for snt in sentences:
        snt = snt.strip()
        if len(snt) < 18 or len(snt) > 600:
            continue
        if not is_clean_ascii(snt):
            continue
        if not KEYWORDS.search(snt):
            continue
        key = re.sub(r"\s+", " ", snt.lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(snt)
    return out

def main():
    files = sorted(SNAPSHOTS.glob("*.html"))
    print(f"processing {len(files)} snapshots...")
    for path in files:
        ts = path.stem
        raw = path.read_text(errors="ignore")
        sentences = visible_clean(raw)
        clean_path = EXTRACTED / f"{ts}.clean.txt"
        clean_path.write_text("\n".join(sentences))
    sizes = [(p.stem.replace(".clean", ""), len(p.read_text())) for p in EXTRACTED.glob("*.clean.txt")]
    sizes.sort(key=lambda x: -x[1])
    print("Top 10 by clean content size:")
    for ts, n in sizes[:10]:
        print(f"  {ts}  {n} bytes")

if __name__ == "__main__":
    main()
