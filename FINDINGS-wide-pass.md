# Headings Full-Wide + H2/H3 Colour Pass — Findings

Date: 2026-11-07 ~14:30 PKT. Scope: CSS/layout only — no words, images, links, schema, phone, or sections changed.
Build: `npm run export` green (55/55 static pages, post-export dual files). Served locally on 127.0.0.1:8317.
Measurement: `site/tools/measure_wide.py` (widths + screenshots, desktop 1440 / mobile 390) and
`site/tools/probe_colours.py` (computed colours + WCAG contrast). Screenshots: `site/qa-wide/`
(`before-*` = before wide pass, `after-*` = after wide pass / before colour pass,
`colour2-*` = final). 320px overflow spot-checked separately.

## 1. Wide pass — what was capped, and what changed

Every heading/intro width cap found in `app/globals.css` + `app/[[...slug]]/page.js`:

| Element | Before | After |
|---|---|---|
| `.hero h1` | max-width 46rem (736px) | no cap — full container |
| `.hero .hero-intro` | max-width 38rem (608px) | no cap — full container |
| Navy-band lead (inner-page intro, inline style) | maxWidth 52rem (832px) | no cap — full container |
| Split text column (`.split` ≥1024px) | 7fr / 5fr (text 635px, aside 453px) | 8fr / 4fr (text 725px, aside 363px) |
| `.call-strip p` | max-width 40rem | no cap — fills flex space |
| `.final-cta-card p` | max-width 40rem | no cap — full card |
| `.faq-list` | max-width 52rem, centred | no cap — full parent width |

Only the outer `.container` (76rem) remains as the full-width boundary. Sticky aside kept:
still `position: sticky; top: 7rem` at desktop, 363px wide (image 363×242, still a proper
sticky photo beside long paragraphs); on mobile it stays `relative` and stacks above the text.

## 2. Wide pass — measured rendered widths (px, container content = 1136 @1440, 350 @390)

| Page @1440 | Metric | Before | After |
|---|---|---|---|
| Homepage | H1 | 736 | **1136** (+54%) |
| Homepage | hero intro | 608 | **1136** (+87%) |
| Homepage | first H2 | 1136 | 1136 (already full) |
| Homepage | FAQ list | 832 | **1136** |
| Homepage | call-strip p | 640 (capped) | 713 (flex fill) |
| Emergency service | H1 | 736 | **1136** |
| Emergency service | navy-band lead | 832 | **1136** (+37%) |
| Emergency service | first H2 / text col | 635 | **725** (+14%) |
| Emergency service | sticky aside | 453 (sticky) | 363 (sticky) |
| Emergency service | FAQ list | 635 | **725** |
| Flood service | H1 / lead / H2 / aside | 736 / 832 / 635 / 453 | **1136 / 1136 / 725 / 363** |
| Broken Arrow area | H1 / lead / H2 / aside | 736 / 832 / 635 / 453 | **1136 / 1136 / 725 / 363** |

@390 mobile: all measured widths already full (350px) before and after — unchanged, as designed.
Overflow: 0 at 1440 / 390 / 320 on all 4 sampled pages. H1 = 1 everywhere. Console errors: 0.

## 3. Colour pass — H2/H3 hierarchy (Edmond palette only)

Before: H1/H2/H3 all `var(--ink)` #17324A on light, all cream on navy — flat, no hierarchy.
After, consistent sitewide:

| Element | Before | After | Contrast (measured) |
|---|---|---|---|
| H2 on light (cream / tan / blue-gray / white) | ink #17324A | **navy #073B66** (strong section colour) | 10.38:1 on cream |
| H3 on light | ink #17324A | **blue #0056A3** (harmonious accent) | 6.63:1 on cream, 7.34:1 on white |
| H2 on navy | cream | cream (unchanged) | 10.38:1 |
| H3 on navy | cream | **cyan-light #7FDBFF** | 7.38:1 (brand-panel H3, ceiling page) |
| Card-title links (cream cards) | ink | **blue**, hover navy | 6.63:1 |
| FAQ question H3s | ink | **blue** | 6.63:1 |
| Footer column H3 labels | cream | cream (unchanged — footer label component, cyan bar accent) | — |
| Hero H1 | cream on navy | cream on navy (unchanged) | 10.38:1 |

All measured contrasts ≥ 4.5:1 (WCAG AA). Full probe table: `site/qa-wide/colours.json`
(`site/tools/probe_colours.py`, 14 targets).

**Defect caught by the probe, fixed in-pass:** the first `.section-navy h3` rule leaked
cyan-light onto card-title H3 elements sitting on cream cards inside navy sections
(measured 1.41:1 on cream — the visible link text was already blue, but the element
colour was wrong). Fix: `.section-navy .card-body h3 { color: var(--blue); }`.
Re-probe after fix: 0 fails. Two probe "MISSING" rows are by design, not defects:
homepage navy sections render no H2 (heading prop not passed — hub page covers navy H2),
and the brand panel only renders on pages with no body image (verified on ceiling page).

## 4. Visual check (viewed pixels, not code-only)

Viewed: `colour2-home-1440` (hero H1 now 2 lines full-width, intro full-width, navy H2,
blue card titles, blue FAQ questions), `colour2-services_emergency-…-1440` (full-width H1,
full-width navy-band intro, navy H2, blue H3 subheads, sticky aside image beside text),
`colour2-home-390-top` (mobile: navy H2 full-width, no overflow, call bar present).
No text runs under the sticky image, no contrast change besides the intended H2/H3 colours,
no layout break at any width.

## 5. Not changed

Content/words, images, links, schema, phone, header/footer, cards, maps, forms — untouched.
Two CSS files only: `app/globals.css`, `app/[[...slug]]/page.js` (one inline style removed).
