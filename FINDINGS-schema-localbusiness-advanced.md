# FINDINGS — Advanced LocalBusiness Schema (Tulsa Water Damage Repair)
Date: 2026-11-12 ~23:05 PKT. Scope: all 53 pages, `app/[[...slug]]/page.js` jsonLd() only.
Status: **ENHANCED + VALIDATED, ZERO ERRORS. Local commit only — NOT pushed, NOT deployed.**
Source of truth: `content/pages.json` (53 pages, the doc) + real site assets in `public/`.
No fact invented. No visible page content, link, H1, or other code changed.

## 1. AUDIT — current schema BEFORE this change (baseline)

Audited every page's JSON-LD twice: fresh local build (`out/`) AND live www
(`https://www.tulsawaterdamagerepair.com`), with a purpose-built validator
(`/tmp/audit_schema.py`) checking JSON syntax, schema.org type/property validity,
Google Rich Results requirements per type, @id cross-references, URL absoluteness,
and value types — plus a second, independent validation with the `jsonschema`
library (strict JSON Schemas per node type).

**Baseline result: the old schema was ALREADY zero-error.**
- Local `out/`: 53 pages, **0 errors, 0 warnings**.
- Live www: 53 pages, **0 errors, 0 warnings**.
- Node totals (both): WebSite 53, BreadcrumbList 53, HomeAndConstructionBusiness 53,
  WebPage 53, FAQPage 51, Article 10, Service 18.
- FAQ 222/222: every Question name + acceptedAnswer text matches the doc source
  (after entity decoding — see note below).
- All @id references resolve (WebPage.isPartOf → #website, Service.provider →
  #business, Article author/publisher → #business, WebSite.publisher added later).

**Audit note (not a defect):** the first audit run flagged 67 "FAQ answer != source"
mismatches. Root cause was my comparator, not the site: `pages.json` stores
`a_text` with HTML entities (`That&#x27;s`), while the rendered schema carries the
decoded character (`That's`) — `lib.js` fixPage() decodes entities at import.
After decoding the source the same way, all 222 match exactly. No defect.

So this round was a pure ENHANCEMENT (richer entity), not a defect fix.

## 2. WHAT WAS ADDED (per page type) — all from doc / real site assets

### LocalBusiness (HomeAndConstructionBusiness) — ALL 53 pages
| Property | Value (source) |
|---|---|
| `image` | `https://www.tulsawaterdamagerepair.com/images/home-tulsa-water-damage-repair.webp` — the business's main hero photo, a real site asset |
| `logo` | `https://www.tulsawaterdamagerepair.com/favicon-512x512.png` (512×512) — the brand mark as a real image file. The header shows the same Heavy A drop as inline SVG (no logo image file exists), so the favicon-512 (same mark) is the closest real logo asset |
| `contactPoint` | ContactPoint: telephone `(918) 395-9320` (doc), contactType `customer service`, availableLanguage `English` |
| `hasOfferCatalog` | **Homepage only** — OfferCatalog "Water Damage Restoration Services" with 18 Offer items, one per real service (name = service H1 minus " in Tulsa, OK", url = service page URL, provider → #business). Inner pages carry the same business entity without the catalog (the Service node on service pages covers it). |

Unchanged and still present: name, description (about-page intro verbatim),
telephone, url, address (PostalAddress, 400 S 129th E Ave, Tulsa, OK 74108, US),
geo (36.15467, -95.83348), hasMap (footer's Google Maps URL), areaServed (20 places),
knowsAbout (18 services), openingHoursSpecification (24/7, 00:00–23:59).

### Service node — 18 service pages
| Property | Value (source) |
|---|---|
| `serviceType` | H1 minus " in Tulsa, OK" (e.g. "Water Mitigation Services") — matches knowsAbout |
| `description` | The page's own intro (doc text, entities decoded by lib.js) |
| `areaServed` | **Expanded from 1 place (Tulsa only) to the full 20-place list** — the service is offered across every area, not Tulsa alone. Shared `AREA_SERVED` const with LocalBusiness (no duplication) |
| `image` | The service's real hero image URL |

### WebPage — ALL 53 pages
| Property | Value (source) |
|---|---|
| `description` | The page's own intro (doc text) |
| `inLanguage` | `en-US` |
| `primaryImageOfPage` | The page's real hero image URL (all 53 pages have a hero) |
| `about` | **Area pages only** — the specific city/neighborhood (`City` for the 12 suburbs, `Place` for the 7 Tulsa neighborhoods; names verbatim from area H1s / AREA_SERVED) |

### WebSite — ALL 53 pages
- `inLanguage: en-US` and `publisher: { @id: …/#business }` added.

### Article — 10 resource guides
- `description` = the guide's own intro (doc text). Everything else unchanged
  (headline = H1, image = guide hero, author/publisher → #business,
  datePublished/dateModified 2026-11-07 — matches the sitemap lastmod for guides).

### Unchanged (already complete, zero-error)
- BreadcrumbList (matches visible trail exactly), FAQPage (222/222),
  LocalBusiness core fields, Article dates.

## 3. WHAT WAS DELIBERATELY NOT ADDED (and why)

- **AggregateRating / Review / any rating** — FORBIDDEN. Google's self-serving rule:
  a business must not mark up its own reviews/ratings. None in the doc either.
- **sameAs** — NO social/directory profile exists anywhere in the doc, the footer,
  or the header (searched: facebook, yelp, instagram, linkedin, twitter, bbb —
  zero hits; only google.com/maps in the footer, which is hasMap). Inventing a
  Facebook/Yelp URL would be a fabricated fact. Left out.
- **priceRange / any price** — no pricing anywhere in the doc. Left out.
- **foundingDate / founder** — not in the doc. Left out.
- **email** — no email in the doc. Left out (contactPoint has telephone only).
- **slogan** — NO slogan exists. The header brand tagline is "Tulsa, Oklahoma"
  (a location, not a slogan). Left out.
- **Certifications / licenses / awards** — none in the doc. (The doc's IICRC S500
  reference is a drying standard named in page copy, not a business credential
  to claim in schema.) Left out.
- **SearchAction on WebSite** — the site has no search function. Left out.
- **AboutPage / ContactPage types** — NOT used. They would REPLACE WebPage (not add
  to it), break the "WebPage on every page" invariant, and unlock no Google rich
  result. /about-us and /contact keep WebPage + LocalBusiness.
- **Video / News / hreflang** — no videos, not a news publisher, single-language
  US site. Not applicable.

## 4. VALIDATION — enhanced schema, ZERO errors

Rebuilt with `npm run export` (exit 0; post-export verifier: 52 flat .html +
homepage index.html, 0 stray). Validated the FRESH build with two independent
validators:

| Validator | Scope | Result |
|---|---|---|
| `/tmp/audit_schema.py` (Google Rich Results requirements + source fidelity + @id resolution + new-property checks) | 53 pages, local `out/` | **0 errors, 0 warnings** |
| `/tmp/validate_schema_jsonschema.py` (`jsonschema` lib, strict JSON Schemas per node type) | 53 pages, **291 nodes** | **0 errors** |

Spot-checks on the built HTML (all confirmed present + correct):
- Homepage LB: image, logo, contactPoint, hasOfferCatalog = 18 items (first:
  Emergency Water Damage Restoration → /services/emergency-water-damage-restoration).
- Service `/services/water-mitigation`: serviceType "Water Mitigation Services",
  description 346 chars, areaServed 20, image = its hero.
- Area `/service-areas/bixby-ok`: WebPage.about = `{City, Bixby}`.
- Article (guide): description present (452 chars on the drying-time guide).
- WebSite: inLanguage en-US, publisher → #business.

File-existence check: **every image/logo URL referenced in the schema resolves
to a real file in `out/`** (0 missing across all 53 pages).

Visible-content guard: `git diff` shows ONLY `app/[[...slug]]/page.js` changed
(113 insertions, 28 deletions), all hunks inside/around jsonLd(). Verified on the
built HTML: **all 53 H1s verbatim** vs pages.json. No link, H1, or visible text touched.
Sitemap untouched by this rebuild (public/sitemap.xml == out/sitemap.xml, 3 dates intact).

## 5. FILES CHANGED (local commit only)

- `app/[[...slug]]/page.js` — jsonLd() only: shared `AREA_SERVED` + `AREA_ABOUT`
  consts, LocalBusiness image/logo/contactPoint (+homepage hasOfferCatalog),
  WebPage description/inLanguage/primaryImageOfPage/about, Service
  serviceType/description/full areaServed/image, WebSite inLanguage/publisher,
  Article description.
- `site/FINDINGS-schema-localbusiness-advanced.md` — this file.
- NOT pushed, NOT deployed. No token used. No Vercel/GitHub touched.

## 6. REMAINING WARNINGS / OPEN ITEMS

- **None.** Zero errors, zero warnings on both validators, all 53 pages.
- Google Rich Results Test / Search Console will still need his-side confirmation
  after this goes live (the validators above are local; Google's own tool is the
  final word — but nothing here is known to fail it: no self-serving markup,
  no invented values, all URLs absolute and live).
- If a real social/directory profile (Facebook, Yelp, GBP) is ever confirmed,
  `sameAs` can be added then — only with a verified URL, never invented.
