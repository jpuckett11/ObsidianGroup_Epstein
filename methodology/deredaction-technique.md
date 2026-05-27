# Deredaction Technique: Cross-Reference Method

## Overview

The DOJ Epstein Files contain duplicate versions of the same FBI evidence log with different levels of redaction. By comparing these two versions line-by-line, 965 of 1,704 redacted entries were recovered (57% success rate).

## The Document Pair

| Document | EFTA Number | Pages | Redactions |
|----------|-------------|-------|-----------|
| Heavily redacted | EFTA02730486.pdf | 255 | 1,704 [REDACTED] markers |
| Less redacted | EFTA02730741.pdf | 255 | 0 [REDACTED] markers |

Both documents are in **VOL00012** of the DOJ Data Set 10 release. They appear to be two production versions of the same FBI evidence inventory log, likely produced at different stages of the litigation with different redaction decisions applied.

## Methodology

### Step 1: Extract Full Text
```python
import fitz

doc1 = fitz.open("EFTA02730486.pdf")  # heavily redacted
doc2 = fitz.open("EFTA02730741.pdf")  # less redacted

text1 = "\n".join([doc1[i].get_text("text") for i in range(len(doc1))])
text2 = "\n".join([doc2[i].get_text("text") for i in range(len(doc2))])
```

### Step 2: Find Unique Content in Less-Redacted Version
```python
lines1 = set(l.strip() for l in text1.split("\n") if l.strip() and len(l.strip()) > 10)
lines2 = set(l.strip() for l in text2.split("\n") if l.strip() and len(l.strip()) > 10)

# Lines only in the less-redacted version = recovered content
only_in_doc2 = lines2 - lines1
```

### Step 3: Filter Meaningful Content
The second revision added Bates stamps (EFTA numbers) to each page. These need to be filtered out:
```python
meaningful = [l for l in only_in_doc2 if not l.startswith("EFTA") and len(l) > 15]
```

## Key Recoveries

### Most Significant: "Chabad" Revealed

**Redacted version (EFTA02730486):**
> "(U) [REDACTED] involvement in U.S. Presidential pardon petitions and influences from Russia and Israel on [REDACTED] and [REDACTED]"

**Unredacted version (EFTA02730741):**
> "(U) **Chabad's** involvement in U.S. Presidential pardon petitions and influences from Russia and Israel on **Pres[ident]**"

### Categories of Recovered Content

| Category | Count | Examples |
|----------|-------|---------|
| Interview/proffer names | 150 | Jason Mojica, Angel Arroyo, Carlos Sanchez-Galan |
| Evidence items | 85 | "Search Warrant for six binders," cell phone warrants |
| MCC witness names | 34+ | Tova Noel, Michael Thomas, Jabraddrick Durant, Dr. Imeri |
| Intelligence entries | Various | "Alleged Money Laundering by Howard Lutnick via BGC Financial" |

### Why This Works

The two documents were produced at different times during the legal proceedings. The less-redacted version (EFTA02730741) appears to have been produced before a more aggressive redaction pass was applied to create EFTA02730486. The government may not have realized both versions would end up in the same public data set.

## Limitations

- 568 redactions remain unresolved (the less-redacted version also doesn't contain these entries)
- Image-burned redactions (text removed before scanning) cannot be recovered through PDF structure analysis
- Some recovered content is truncated (OCR captured partial text at page boundaries)

## Applicability to Other Documents

This technique can be applied to ANY document pair where:
1. The same content exists in two versions
2. Different redaction decisions were applied
3. Both versions are accessible

The `pdf_find_duplicates` tool in our MCP server automates the search for potential duplicate pairs by comparing text fingerprints across directories.

## Tools

The full MCP server with 75 document research and PDF forensic tools is available in this repository under `/tools/`.
