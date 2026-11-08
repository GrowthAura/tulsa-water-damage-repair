# Tier 1 AI-Search Fixes — Findings (2026-11-08)

Research: AI Overview / ChatGPT / Claude / Perplexity ranking deep research
(report: ~/workspace/research_notes/ai-search-schema-ranking-tulsa-20261108-0740/report.md).
User approved the three Tier 1 code fixes + push (12:49 PKT). No other change
was made: no words touched, no titles/descriptions (U5), no dead doc phrases
(U8), no IndexNow submission, no other schema type added.

## Fix 1 — Business schema subtype: LocalBusiness → HomeAndConstructionBusiness

- Source: `app/[[...slug]]/page.js`, `jsonLd()` — the single emitter (verified by
  grep: the only `LocalBusiness` string in source was this one line + its comment).
- Before: `'@type': 'LocalBusiness'` on all 53 pages.
- After: `'@type': 'HomeAndConstructionBusiness'`; single @id
  `https://www.tulsawaterdamagerepair.com/#business` and ALL fields unchanged
  (name, telephone, url, address, areaServed, openingHours 00:00–23:59 7 days).
- NOT EmergencyService (schema.org: that type is a fire station / ER).
- Verified in built output: HomeAndConstructionBusiness on **53/53** pages;
  plain-LocalBusiness business type on **0** pages (checked the JSON-LD script
  and the escaped flight payload in all 53 canonical files).

## Fix 2 — robots.txt: explicit AI-bot Allow groups

- Source: `site/public/robots.txt`. Original lines kept exactly:
  `User-agent: * / Allow: /`, Sitemap line, Host line.
- Added 10 AI search-bot groups: Googlebot, Bingbot, OAI-SearchBot,
  ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User,
  DuckAssistBot, YouBot.
- Added 9 AI training-bot groups (his established allow-everything pattern):
  GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot,
  Meta-ExternalAgent, Meta-ExternalFetcher, cohere-ai, Bytespider.
- NOT added: deprecated tokens anthropic-ai / Claude-Web (verified absent).
- Verified in built `out/robots.txt`: **19/19** explicit `User-agent: X / Allow: /`
  groups present. (Note: the live domain's robots.txt previously had only the
  `*` group — the named tokens existed only in another site's memory, not in
  this build. Functionally `*` already allowed all crawlers; the explicit
  groups now make it unambiguous per bot.)

## Fix 3 — Article schema on the 10 guide pages

- Source: `app/[[...slug]]/page.js`, `jsonLd()` — gated on
  `page.type === 'resource'` (exactly the 10 /resources/ guides; the
  /resources/ hub is type `resources-hub` and is excluded).
- Node per guide: `@type: Article`, headline = page H1 verbatim,
  author = publisher = `{ '@id': 'https://www.tulsawaterdamagerepair.com/#business' }`
  (the business itself — NO person name invented),
  datePublished = dateModified = `2026-11-07` (sitemap lastmod / site publish
  date; pages.json carries no per-page dates, so no earlier date was invented).
- Verified in built output: Article JSON-LD on **exactly 10/10** guide pages,
  valid JSON (parsed), headline verbatim vs H1 on 10/10, author/publisher @id
  correct on 10/10, dates correct on 10/10; Article on **0** other pages
  (including the /resources/ hub).

## Build + structural verification (fresh `npm run export`, exit 0)

- 56 static pages generated; post_export: **23 flat .html** copies made,
  30 slash routes use index.html.
- `tools/verify_site.py` (local server :8317): pages checked **53**,
  internal link fetches **2,395 × 200, PROBLEMS 0**, reachable from home 54/53,
  exit 0. FINDINGS-round1.md restored from git afterwards (verifier overwrites it).
- No other visible change: before/after diff of homepage, one service page and
  one guide page — visible HTML (scripts stripped) byte-identical; the ONLY
  token changes are LocalBusiness → HomeAndConstructionBusiness (home/service)
  and subtype + Article node tokens (guide). No words changed anywhere.
- Homepage screenshots (Playwright, 1280×900 + 390×844): **0 changed pixels**
  before vs after.
- `?v=` check: 0 in any text file (html/js/css/json/txt/xml). Two .webp files
  contain the byte sequence `?v=` inside binary image data (md5-identical to
  the pre-existing public/ sources, no URL nearby) — not cache-buster URLs.

## Push

- main: <SHA — filled at push time>
- gh-pages: <SHA — filled at push time>
- Live preview verified after push: home 200, one no-slash URL 200 direct,
  robots.txt live shows the new groups, one guide page live shows Article
  schema + new subtype.

## His side — still pending (NOT attempted)

- Search Console "Search generative AI" Include setting.
- Google Business Profile completion + steady genuine Google review flow.
- Claim/complete Yelp + Bing Places + Apple Business Connect; verify Bing indexing.
- WAF/Cloudflare check (no bot blocking).
- U5 titles/descriptions wording call; U8 7 dead doc phrases; U2 IndexNow
  submission (only after www serves OUR site).
