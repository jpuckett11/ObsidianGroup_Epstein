# Chain of Custody, Document Integrity Manifest

## Investigator

**Name:** Jay Puckett  
**Organization:** Obsidian Watch Group  
**Email:** obsidianinvestigations@pm.me  
**PGP Key ID:** `9267A71E3F0A4EED2F973F9BA3E252F24635CC6C`  
**Key Type:** ed25519 (EdDSA)  
**Key Expires:** 2027-05-19  
**Public Key File:** `signing_key.asc`  

## Signed Documents

The investigation publishes three separate PDFs, each signed independently.

### When Lady Justice Was Truly Blind

| Field | Value |
|-------|-------|
| File | `When_Lady_Justice_Was_Truly_Blind.pdf` |
| Signature | `When_Lady_Justice_Was_Truly_Blind.pdf.asc` |
| SHA-256 | `e5e519945400c8539a5e4fe9580be7b5fbfa49b53f429fe00d430e024c225bea` |
| Signed | 2026-06-07 |
| Signer | Jay Puckett (Obsidian Watch Group) |

### The Chronological Case Study of J. Epstein, Evidence Edition

| Field | Value |
|-------|-------|
| File | `The_Chronological_Case_Study_of_J_Epstein_Evidence.pdf` |
| Signature | `The_Chronological_Case_Study_of_J_Epstein_Evidence.pdf.asc` |
| SHA-256 | `20a445889d2b85c3415568c9ffaa10ca05e07170dc1b4d84c5b3742261beb45f` |
| Signed | 2026-06-07 |
| Signer | Jay Puckett (Obsidian Watch Group) |

### The Chronological Case Study of J. Epstein, Documentary Edition

| Field | Value |
|-------|-------|
| File | `The_Chronological_Case_Study_of_J_Epstein_Documentary.pdf` |
| Signature | `The_Chronological_Case_Study_of_J_Epstein_Documentary.pdf.asc` |
| SHA-256 | `6cc24b784edeb321d4d252d4c246a590d48f20afa74eaea01a94548cf0627f7e` |
| Signed | 2026-06-07 |
| Signer | Jay Puckett (Obsidian Watch Group) |

## Verification Instructions

To verify a document has not been tampered with:

```bash
# 1. Import the public key
gpg --import signing_key.asc

# 2. Verify the signature for the document you want to check
gpg --verify When_Lady_Justice_Was_Truly_Blind.pdf.asc When_Lady_Justice_Was_Truly_Blind.pdf
gpg --verify The_Chronological_Case_Study_of_J_Epstein_Evidence.pdf.asc The_Chronological_Case_Study_of_J_Epstein_Evidence.pdf
gpg --verify The_Chronological_Case_Study_of_J_Epstein_Documentary.pdf.asc The_Chronological_Case_Study_of_J_Epstein_Documentary.pdf

# 3. Verify the SHA-256 hashes match
sha256sum *.pdf
# Should match the hashes in the Signed Documents tables above.
```

A valid signature confirms:
- The document was signed by the holder of private key `9267A71E3F0A4EED2F973F9BA3E252F24635CC6C`
- The document has not been modified since signing
- The timestamp on the signature reflects when it was signed

## Update Log

| Date | Version | SHA-256 | Change |
|------|---------|---------|--------|
| 2026-05-25 | 1.0 | `ede7e1fed...737c4c` | Initial publication, 13 chapters |
| 2026-05-25 | 1.1 | `9227d1c9f...a9a275` | Added Zorro Ranch missing girls chapter, investigator name + PGP info to PDF |
| 2026-05-25 | 2.0 | `1041a1c53...e057b` | Complete rewrite, 55 pages, 16 chapters, 5 appendices, all findings, $2.146B financial audit, transport photo forensics, full biography timeline |
| 2026-05-25 | 3.0 | `4e2bf572a...6c453` | Integrity corrections: fixed deredaction count (100% not 57%), corrected cream cheese as literal food orders, credited R.S. Taylor/$412.3M gap, credited NYT/NYDFS names, separated Chabad CHS memo from evidence log recovery, adjusted novel findings count from 63 to 50+ verified |
| 2026-05-25 | 7.0 | `060525d92...07cb7a` | Complete V7 rewrite, Definitive Edition. 145 pages, 40 chapters, 7 appendices, 8 parts. All 57 source files integrated. Hundreds of hours of investigation. Full biography timeline, financial audit ($2.146B), intelligence operation (5 corroborating sources), trafficking (MC2/Ehnbom/Zampolli chains), death forensics (3 neck fractures, transport photo analysis), Mandelson (€500B tip, arrest), 60-country map, 153-vessel AIS tracking, GPS forensics, 50+ verified findings. All sources credited. |
| 2026-05-26 | 7.1 | `dadb92860...527d61d` | V7 Build 2, Expanded to 206 pages. Added Ivana Trump UES cluster, Kushner Affinity pipeline ($6B AUM), Trump sons / Dominari chain, Schlaff/Stasi/Putin Dresden / BAWAG €1B Honig pump-and-dump, full perpetrator accounting ($9.35B / $16.61:$1 ratio), Bill Richardson Zorro Ranch verification, Brazil victims / São Paulo apartment / Zorro Ranch buried girls hypothesis, ProtonMail DNS configured for obsidianwatch.org via Cloudflare. |
| 2026-05-26 | 7.2 | `be4108781...4855ae08` | V7 Build 3, Definitive Edition, 231 pages, 48 chapters. NEW: Chapter XLVIII "The Story, Told Straight", unified narrative from origins through operation, end, and damage. Deaths expanded to 14 connected individuals (added Bill Richardson Sep 2023, Carolyn Andriano May 2023 overdose, Leigh Skye Patrick May 2017 overdose). Financial corrections from verification agent: Deutsche Bank uses NYDFS-verified language only; Palantir 2026 cap corrected to $300B+; Thiel figure reduced to verified $40M Valar LP; Carbyne/Axon $60M clarified as $20M cash + $40M shares. Kushner Affinity AUM updated to $6B / $110M+ Saudi government payments. Mark Epstein HDI directorship, Gratitude America full timeline, Liquid Funding Bermuda chairmanship added. |
| 2026-06-07 | 8.0 | (see Signed Documents tables above) | Restructured the single V7.2 monolith into a three-document set: (a) `When_Lady_Justice_Was_Truly_Blind.pdf` as the lead narrative for general readers (85 pages, 27,740 words, 13 chapters), (b) `The_Chronological_Case_Study_of_J_Epstein_Evidence.pdf` as the dense cited reference (42 pages, three-tier evidentiary standard), (c) `The_Chronological_Case_Study_of_J_Epstein_Documentary.pdf` as the earlier documentary build retained for continuity. The original unified PDF filename `The_Chronological_Case_Study_of_J_Epstein.pdf` and its V7.2 signature `.asc` are retired; the SHA-256 `be4108781...4855ae08` is preserved here for historical audit. Each of the three current PDFs is signed independently with its own detached `.asc`. Corpus scale through this revision: 3,482,240 documents read, 688+ investigation hours, 85+ named individuals, 56+ corporate entities, $3.2B+ financial flows documented, 20 FOIA requests filed. |

## Notes

- All updates to the case study will be re-signed and this manifest updated
- Previous hashes are preserved in the update log for audit trail
- Git commit history provides additional timestamping via GitHub's servers
- The PGP signature provides cryptographic proof of authorship independent of GitHub

---

*This chain of custody is maintained by the lead investigator. The signing key is under sole control of Jay Puckett.*
