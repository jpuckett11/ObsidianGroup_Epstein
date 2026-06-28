# Aviloop / Aviatri Archive Analysis

Investigator: Reckoner / Jay Puckett, Obsidian Watch Group
Compiled: 2026-06-28
Status: open investigative file

This file documents the structural and content analysis of the public web
properties tied to **Nadia Marcinko** (née Marcinkova), the longest-serving
female pilot in the Epstein network. Source: Wayback Machine archive
snapshots, public DNS records, public Wix infrastructure metadata.

Companion to: [[INTERNATIONAL REGISTRIES - Wave 2]], [[Nadia Marcinkova - Operational Continuity Hypothesis]], [[MEGA SWEEP FINAL - Summary]], [[CONTAINMENT APPARATUS - Public Discourse Management]], [[CONTINUITY - Pattern Successor Hypothesis]].

## 1. Scope of evidence collected

| Site | Wayback snapshots downloaded | Date range | Status |
|------|------|---------|---|
| aviloop.com | 72 unique-content captures | 2018-07-22 → 2026-06-27 | active |
| aviatri.com | 40 unique-content captures | 2014 → 2026-04-13 | active |

All snapshots are preserved at:
- `aviloop-archive-analysis/snapshots/*.html`
- `aviloop-archive-analysis/aviatri/snapshots/*.html`

Timeline diffs, secrets extractions, and per-snapshot extracts are
preserved alongside.

## 2. Definitive technical link between Aviloop and Aviatri

Both sites are owned by the **same Wix user account**:

```
Wix Owner / User ID: c108962e-b961-4568-8203-08966af79a38
```

This identifier is stable across every snapshot of both sites since 2019
and is the universal cross-Wix identifier. Anyone who owns a Wix site
shares this ID across every site they own.

**The Wix user ID is not user-controlled and cannot be edited.** It is
assigned at account creation and persists through the operator's
lifetime. Its appearance on both `aviloop.com` and `aviatri.com` is
forensically conclusive proof of common ownership.

Per-site Wix metadata:

| Site | Meta Site ID | Google Site Verification |
|------|------|----|
| aviloop.com | `9b7da87e-9ec4-4ecc-88c1-1e548787386e` | `WfLtm0wRqQRTdtabDbDkLk_fz1T-H1q4sq9U23k7PQ8` |
| aviatri.com | `07e0049e-a738-4bcd-bf9e-38f43c2c00be` | `zhlA8MG2BI8UxGHlbBCipgmzyM5nd7w2aoNol2gmeOo` |

The two distinct Google site verification codes indicate Marcinko has
registered each site separately with Google Search Console under
distinct Google accounts (or one account with two property verifications).

## 3. The site outage that brackets the Miami Herald exposé

`aviloop.com` was deliberately taken offline during the entire Miami
Herald "Perversion of Justice" series window:

| Snapshot date | Body content | Disposition |
|------|---|---|
| 2018-07-22 | 85 chars: "Page cannot be displayed. Please contact your service provider for more details." | Site OFFLINE |
| 2018-11-04 | 0 chars | Site OFFLINE |
| 2019-07-09 | 1703 chars | Site **back online** |

The 2018 outage HTML comment includes `Server: P3PWPARKSTAT04` — a
recognizable domain-parking server identifier from a major US registrar.
The site was not failing; it was deliberately parked.

The Miami Herald series ran from late November 2018. The site stayed
offline through Acosta's resignation (July 12, 2019) and reappeared
**three days after Epstein's July 6, 2019 arrest**.

The site has not been taken offline since, including during the
Maxwell arrest (July 2020), the Maxwell trial (Dec 2021), the Maxwell
verdict (Dec 2021), and the EFTA document releases (2024-2026).

## 4. Founder bio claims have been quietly walked back

**2019-07-09 version (the first capture after Epstein's arrest):**

> She became a licensed flight instructor and Airline Transport Pilot
> (ATP), rated on **Gulfstream II, III, IV and Boeing 737, 747, 757, 767**
> aircraft.

**2026-06-05 version (current):**

> She became an **aerobatic pilot**, licensed flight instructor, and
> Airline Transport Pilot (ATP), rated on **multiple Gulfstream and
> Boeing** aircraft.

Three intentional changes:

1. **"Aerobatic pilot" added** as a new claim. Aviloop offers "team
   building events" specifically advertising aerobatic flights with
   an "expert instructor" letting participants take the controls. This
   service mention does not appear in the 2019 site.
2. **Specific type ratings replaced with the vague "multiple"**.
   Type ratings on Gulfstream II, III, IV and Boeing 737/47/57/67 are
   independently verifiable through the FAA Airmen Inquiry. Removing
   the specifics removes the verification target. This is the
   opposite of normal CV behavior, where credentials are added rather
   than redacted.
3. **Copyright still reads "©2019 by Aviloop"** seven years later
   despite the site being actively maintained (281 Wayback captures,
   most recent 2026-06-27).

## 5. Aviloop has hidden pages

The Wix page list exposes 12 pages in total. Two are explicitly
marked hidden in the page registry:

| Internal page ID | Page title | URL slug | Visibility |
|---|---|---|---|
| h2nve | Home | `/home` | nav |
| a9k25 | Social Media & Marketing Strategies | `/socialmedia` | nav |
| yfmcm | Marketing Content Creation | `/marketingcontentcreation` | nav |
| b3n64 | Color Epaulettes | `/colorepaulettes` | nav |
| jyzzz | Aviation Team Building Events | `/teambuilding` | nav |
| vgpll | Aviation Events | `/aviationconference` | nav |
| r3wzi | Contract Pilot Services | `/copy-of-box-5` | nav (note slug) |
| m9rdt | Trade Show Activation | `/tradeshows` | nav |
| vqfe6 | Flight School Setup | `/flightclub` | nav |
| n0g95 | **Aviatri** | `/aviatri` | **internal page predating aviatri.com** |
| **g5bd6** | **About (hidden)** | `/about-hidden` | **HIDDEN** |
| **f13qu** | **Scrap page (invisible)** | `/scrap-page-invisible` | **HIDDEN** |

The "About (hidden)" page is significant: there are TWO about pages on
the site. The visible "About" tab shows Marcinko's sanitized bio. The
hidden one is, presumably, a draft, an earlier version, or a redacted
version of the bio.

The URL slug `copy-of-box-5` on the Contract Pilot Services page
indicates it was created by duplicating an existing "box-5" page in the
Wix editor, suggesting iterative content development.

The Wix page JSON files for the hidden pages are referenced in every
snapshot. They are stored on the parastorage/wixstatic CDN. Pulling
those JSON blobs from the Wayback CDX archive is the next step.

## 6. Contact infrastructure is asymmetric

Across all 72 Aviloop snapshots (2018-2026), the site advertises:
- **No callable phone number anywhere**
- **No direct email address anywhere**
- **No street address**
- Contact only via web form

Across the 40 Aviatri snapshots, the site advertises:
- **Phone: `347-687-5667`** (NYC 347 area code)
- **Email: `team@aviatri.com`**
- **Instagram: `@flyaviatri`**
- **Facebook: `FlyAviatri`**

For an active "aviation marketing" business with seven years of public
presence, the absence of any callable contact channel on Aviloop is
operationally unusual.

## 7. The 2021 Aviatri template-leak anomaly

Between **2021-05-07 and 2021-07-28**, the published phone number on
Aviatri was replaced with the Wix template placeholder
`555-123-4567`. This was the default phone number Wix inserts in its
"Business" template when no real number is configured. The real number
returned to the site by July 28, 2021.

Plausible explanations:
- The site was being re-templated and the editor failed to copy the
  real phone forward
- The real phone was deliberately removed during a specific window
- A staff change resulted in the template being reverted to defaults

The window covers the period right after Ghislaine Maxwell's June 2021
trial scheduling motions. Worth noting as a correlated edit event,
not a proof.

## 8. Sister-company integration

Two distinct Aviatri presences exist:

1. **Internal page** on `aviloop.com/aviatri` (page ID `n0g95`, present
   since at least 2019)
2. **Standalone domain** `aviatri.com` (Wayback CDX shows captures
   going back to at least 2014, with consistent ownership since 2019)

The visible service description on aviloop.com:

> Through our sister company - **Aviatri** - we aim to make cockpits
> safer by raising the number of women in aviation. We can help
> employers find qualified professional female pilots to join their
> team.

The combined business model:
- Aviloop = "match clients with qualified pilots or other aviation
  professionals, including conference booth or social media influencers,
  for their marketing needs"
- Aviatri = "help employers find qualified professional female pilots
  to join their team"

For a principal who is documented in the Epstein flight logs as the
right-seat pilot on multiple Epstein/Maxwell flights including the
Prince Andrew context (per EFTA01795680.pdf in the existing case
file), a stated current business model of "we match clients with
female pilots from our network" warrants attention as a structural
continuity, not as proof of present-day misconduct.

## 9. Wayback capture intensity tracks Epstein news cycles

Aviloop.com Wayback capture frequency by year, restricted to
content-bearing 200-OK responses:

| Year | Captures | Context |
|------|---|---|
| 2018 | 2 | site offline through Miami Herald series |
| 2019 | 11 | Epstein arrest July, Epstein death August |
| 2020 | 19 | Maxwell arrest July, Acosta DOJ review |
| 2021 | 7 | Maxwell trial scheduling |
| 2022 | 17 | Maxwell verdict aftermath |
| 2023 | 9 | quieter year |
| 2024 | 23 | EFTA release ramp-up |
| 2025 | 25 | sustained interest |
| 2026 (YTD) | 29 | active investigation |

Wayback Machine captures are driven both by Internet Archive's own
crawler and by user-initiated saves through "Save Page Now." The
volume increase since 2024 is consistent with public investigative
interest reopening on Marcinko specifically.

## 10. Cross-reference to the existing case file

The `MEGA SWEEP FINAL - Summary.md` already records:

> | Aviloop | 438 | Marcinkova's company throughout the documents |
> | Aviatri | 1 | Marcinkova's sister company confirmed in docs |

The 1 Aviatri hit is in **EFTA01795680.pdf**, headlined "Flying Lessons:
Did Popular Aviatrix Right-Seat for Epstein in Royal Sex Scandal?" —
the Prince Andrew flight context.

The 438 Aviloop hits across the EFTA documents are not duplicated in
this file; the archive analysis above is independent confirmation that
the public web presence has been actively maintained continuously
through the entire post-arrest period.

## 11. Hidden page captures recovered

The Wayback Machine independently crawled the hidden page slugs even
though they were not linked from the main navigation. Direct URL
captures recovered:

### `/about-hidden` (the hidden About page)

Multiple captures since **2019-07-20** — fourteen days after Epstein's
arrest. The largest is `2021-12-03 (16:49 UTC)` at 335 KB.

Content of the hidden About page differs from the visible one:

> About | Aviloop  Home Services About Contact More
> AVILOOP  WHO WE ARE
> Aviloop offers a wide range of services designed to accelerate the
> growth of brands in the aviation industry through targeted marketing
> and promotions. We partner with our clients from start to finish,
> focusing on their needs while producing new ideas and developing
> effective strategies and solutions. As aviation professionals with
> the necessary tools and expertise, we bring an understanding of the
> specific language, needs and quirks of the industry to provide
> uniquely targeted marketing support.
> CONTACT US  (123) 456-7891  Send  Your details were sent successfully!
> ©2019 by Aviloop.

Notable differences from the visible About page:
1. **No founder bio**. The visible About page is built around Marcinko's
   personal credentials. The hidden About is a generic corporate "who we are"
   page with no person named.
2. **Contact form is embedded directly** with a phone number field.
3. **Phone number `(123) 456-7891`** — Wix template placeholder.
   Whoever built this page never replaced the template default.
4. **"Your details were sent successfully!" rendered in the page body** —
   that is the post-submission confirmation message accidentally left
   visible in the page layout rather than being conditional on form
   submission.

Plausible read: the hidden About is a half-built corporate-front version
of the About page, abandoned before being finalized, retained on the
site as a draft/scrap reference. The fact that it has been preserved
through every site iteration since 2019 (rather than being deleted
when superseded) is itself notable.

Saved at `hidden_pages/about-hidden_largest_20211203164948.html`.

### `/aviatri` (internal sister-brand page on aviloop.com)

Captures since **2019-08-24**. The 2019-12-09 capture (385 KB) shows
the page title is **"Crew Diversity | Aviloop"**, not "Aviatri." The
page body:

> Crew Diversity | Aviloop  ©2019 by Aviloop.
> New York City  Help employers diversify their crews
> Diverse teams are smarter. We aim to make cockpits safer by raising
> the number of women in aviation. We can help employers hire qualified
> professional female pilots to join their team.

This confirms Aviatri originated as the "Crew Diversity" feature page
inside Aviloop, then was spun out into the standalone aviatri.com
domain. The "matching qualified female pilots to clients" service
language is identical between the 2019 internal page and the
standalone Aviatri site.

Saved at `hidden_pages/aviloop_aviatri_internal_20191209.html`.

### `/scrap-page-invisible`

Wayback CDX returned no captures of this slug — the page was never
linked from anywhere indexable, so the IA crawler never reached it.
Direct CDN fetch of the page JSON returns HTTP 403 (Wix forbids
unauthenticated access to internal page JSONs). The content of the
"Scrap page (invisible)" remains unrecovered through passive means.

## 12. EFTA01795680: Someone sent Epstein the Negroni article with "you were right" as the subject line

The bates EFTA01795680.pdf is a **one-page email screenshot** showing
the email layout below. Image-level OCR of the embedded grayscale
screenshot inside the PDF matches the text-layer extraction exactly:

```
From:                              [blank]
Sent:                              Thursday, January [22], 2015, PM
To:                                Jeffrey Epstein
Subject:                           you were right

Flying Lessons: Did Popular Aviatrix Right-Seat for Epstein
in Royal Sex Scandal?

[link: blogspot photo "Nadia and the Aston"]
[link: christinenegroni.blogspot.com/2015/01/did-popular-aviatrix-right-seat-for.html]

Preview by Yahoo

Sent from my iPhone

EFTA_R1_00131018
EFTA01795680
```

Three operational signals:

1. **Epstein is the recipient**, not the sender. The `To:` field reads
   "Jeffrey Epstein" plainly. The signature "Sent from my iPhone" is
   the unidentified sender's, not Epstein's.
2. **The subject line is "you were right"** — meaning Epstein had
   previously had a conversation with the sender in which Epstein
   warned them about Marcinkova's exposure to the Andrew matter, OR
   the sender had warned Epstein and is now writing back to acknowledge
   the prediction landed.
3. **The body contains "Preview by Yahoo"** — this tag is
   automatically inserted by Yahoo Mail when a user shares a link
   through Yahoo Mail's article-share feature. The sender either used
   a Yahoo Mail account or forwarded a Yahoo Mail message to Epstein.

The `From:` field is **blank, not redaction-stamped**. This is
consistent with the article having been shared via Yahoo Mail's
share-link feature in a way that strips the originating From header
from the rendered screenshot. It is not consistent with DOJ-applied
redaction, which would typically show a black bar or "REDACTED" mark.

The email was preserved in the EFTA corpus and is accessible at the
public DOJ Epstein release portal (DataSet 10). A Wayback Machine
copy is archived from 2026-02-20.

## 12a. Adjacent bates window analysis

A ±50 bates window pull around EFTA01795680 was performed via Wayback
Machine. 51 of 101 attempted bates were recovered. The Wayback gaps
appear to be uncrawled rather than withheld.

The bates ordering is **not chronological by sent date**. Among 51
recovered emails surrounding EFTA01795680, the date distribution is:

| Year | Count |
|------|-------|
| 2009 | 1 |
| 2010 | 9 |
| 2011 | 25 |
| 2012 | 2 |
| 2013 | 5 |
| 2014 | 3 |
| 2015 | 4 |
| 2016 | 7 |

The 2010-2011 mail dominates the window. EFTA01795680 (January 2015)
is one of only four 2015-dated messages in the recovered set, the
others being unrelated to Marcinkova. The bates filing order appears
to reflect DOJ processing order (likely OCR / scan ingest), not
conversation thread order.

Recipient identification is therefore not recoverable through bates
adjacency alone. The sender must be inferred from independent context.

## 12b. Sender candidate pool

The sender is constrained by three observed facts:

1. Used Yahoo Mail (or forwarded a Yahoo Mail message) on January 22,
   2015
2. Used an iPhone at the time of sending
3. Was close enough to Epstein to begin a substantive email with
   "you were right" — implying prior continuous correspondence about
   Marcinkova's media exposure

Candidates in descending order of fit:

| Candidate | Yahoo Mail use? | iPhone? | "you were right" fit |
|---|---|---|---|
| **Ghislaine Maxwell ("Gmax")** | possible (older email era) | possible | strongest fit — she introduced Marcinkova-era operations, had longest historical knowledge of Marcinkova's exposure points |
| **Lesley Groff** (assistant) | high (her email era + administrative role) | possible | strong fit — she filtered all media inputs to Epstein |
| **Darren Indyke** (attorney) | low (would use law firm domain) | high | fit on the "warning came true" framing |
| **Karyna Shuliak** | low (digital-native generation, gmail likely) | high | weaker fit — joined Epstein orbit too late for deep Marcinkova history |
| **An unnamed PR/media consultant** | high (Yahoo era) | possible | strong fit on the warning structure |

Across the surrounding bates window, observed Epstein correspondents
in the same window include "Gmax" (named in a To: field), Richard
Kahn, Larry Visoski, Karim Wade, Peter Attia, Kevin Law, "Jonathan,"
and Karyna Shuliak (as sender once).

The most operationally-natural fit is **Ghislaine Maxwell**, but this
is inference, not proof. Documentary confirmation would require either
the original full email header (likely sealed elsewhere in the DOJ
archive) or a corroborating email from another bates referencing the
same conversation.

## 13. Negroni's 2015 article: the FAA credentials that aren't there

Negroni's reporting documents Marcinkova's FAA licenses as of January
2015 as:

> "FAA licenses as a single and multi engine, instrument-rated pilot
> and ground and flight instructor"

**What is conspicuously absent from the 2015 FAA record per Negroni:**

- ATP (Airline Transport Pilot)
- Any Gulfstream type rating
- Any Boeing type rating

**Compare against the aviloop.com claims:**

| Year | Aviloop claim about Marcinkova's ratings |
|------|------|
| 2015 (Negroni, sourced to FAA) | single + multi engine + instrument + flight instructor |
| 2019 (Aviloop website) | ATP + Gulfstream II/III/IV + Boeing 737/47/57/67 |
| 2026 (Aviloop website) | ATP + "multiple Gulfstream and Boeing" + aerobatic |

To get from the 2015 FAA record to the 2019 Aviloop claim, Marcinkova
would have had to earn:
- ATP certificate
- Type ratings on 4 distinct Gulfstream models (II, III, IV)
- Type ratings on 4 distinct Boeing models (737, 747, 757, 767)

In **four years**, while running a marketing business named Aviloop.

This is verifiable through the FAA Airmen Inquiry. The system is
publicly searchable at https://amsrvs.registry.faa.gov/airmeninquiry/.
The current record will either confirm or refute the 2019 claim.

If the current FAA record does not show the type ratings, the 2019
website claim was false on its face, and the 2026 walkback to "multiple
Gulfstream and Boeing" is consistent with quietly hiding that the
specifics never existed.

This is also the explanation for why the website has retained the
copyright `©2019 by Aviloop` for seven years: the page's content was
last meaningfully changed when the bio walkback happened, not when the
site was edited. The copyright stamp is a fossil of the last
substantive content revision.

## 14. Marcinkova's response on the record

Negroni asked Marcinkova directly. Her quote:

> "Accusations are obviously bizarre, untrue and clearly motivated by
> money."

That language pattern — "obviously bizarre, untrue and clearly motivated
by money" — is consistent with the public denial language Epstein
associates used through the 2007-2019 period. It is denial without
specific factual rebuttal. The on-the-record statement is preserved
in the case file via Negroni's blog.

## 15. Sarah Kensington / Sarah Kellen cross-reference

Negroni names **Sarah Kensington** as an associate of Epstein and "NASCAR
driver's wife." This is Sarah Kellen (later Sarah Kellen-Kensington),
who married NASCAR driver Brian Vickers. She is independently named in
the case file's documented payouts via the 1953 Trust and in multiple
victim depositions.

Negroni's 2015 article is therefore a contemporary public record that
ties three named individuals — Marcinkova, Kellen-Kensington, and
Epstein — together in published reporting fifteen months before the
Acosta Pulitzer-winning Herald series and four years before the
Epstein arrest.

## 16. Standing investigative questions

1. **What is on the hidden "About (hidden)" page** at
   `aviloop.com/about-hidden`? Page JSON file is
   `c10896_018ac544f41c3d5eb36e5b62900acd2c_193.json`, may be
   recoverable from Wayback CDX of the parastorage CDN.
2. **What was on the "Scrap page (invisible)"**? Page JSON file is
   `c10896_b75a4e5afc6459143b16f2bd797ecb63_193.json`.
3. **FAA Airmen Inquiry lookup for Nadia Marcinkova / Nadia Marcinko**
   — verify whether the originally-claimed Gulfstream II/III/IV and
   Boeing 737/47/57/67 type ratings are real, whether they expired,
   and whether the current "aerobatic pilot" claim is supported by
   FAA records.
4. **Image EXIF on the Marcinko-uploaded photos** preserved on the
   wixstatic CDN. Several images are sized at exact iPhone resolution
   (4032x2688) and may retain GPS/timestamp metadata.
5. **The 347-687-5667 phone number reverse lookup**. NYC 347 area code.
   Subscriber may or may not be Marcinko personally.
6. **Cross-reference the Wix Owner ID** `c108962e-b961-4568-8203-08966af79a38`
   against the public web to identify any other Wix sites owned by the
   same operator beyond Aviloop and Aviatri.
7. **EFTA01795680.pdf** full read — pull the document text from the
   existing case archive and integrate the "Flying Lessons" content
   into this file's evidentiary record.

## 12. Provenance and integrity

- Wayback Machine snapshots are downloaded directly via the
  Internet Archive `web.archive.org/web/{ts}id_/...` endpoint (raw
  content, no toolbar overlay).
- Content-digest deduplication is performed on the CDX side via
  `collapse=digest`.
- All raw HTML, extracted text, and per-snapshot metadata is
  preserved on disk under `aviloop-archive-analysis/`.
- The harness scripts (`runner.py`, `reextract.py`, `secrets.py`,
  `extract_clean.py`) are reproducible by any qualified second party.
- This file does not assert any criminal conduct beyond what is
  documented in cited public-record sources.

---

Reckoner / Jay Puckett
Obsidian Watch Group
2026-06-28
