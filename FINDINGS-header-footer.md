# Header + Footer Best-Ever Pass — FINDINGS

- Date: 2026-11-07 ~15:20 PKT. Scope: components only — `app/components/Header.jsx`,
  `app/components/Footer.jsx`, `app/globals.css` (their styling). No words/content invented,
  no doc content changed, no phone/address changed, no new pages. `page.js` / `Shared.jsx`
  untouched (parallel hub-cards agent owns them).
- Probe: `site/tools/probe_header_footer.py` (new) — header/footer screenshots at 1440/390
  (home, service, area, contact), mobile-menu-open screenshots, H1/overflow/console/sticky
  checks, plus a full fetch of every distinct header+footer link and every sitemap URL.
  Screenshots: `site/qa-header-footer/` (header-*/footer-*/mobile-menu-* + `probe.json`).
- Build: `npm run export` green (53 routes; 23 flat .html copies, 30 slash routes).
  Two builds total (second after the console-404 fix); no collision with the parallel agent.

## What changed

### Header
- Brand mark: 💧 emoji → inline SVG water drop (cyan drop + white highlight dot, matching
  the favicon design) in the navy tile — crisp at every size, no extra request.
- Nav: added **Blog** (`/resources/`) to the desktop nav (Home · Services▾ · Service
  Areas▾ · About Us · Blog · Contact) and to the mobile menu. It was missing in both.
- Header CTA: the stacked "EMERGENCY? / (918) 395-9320" layout never applied — the rule
  `.header-cta .btn` targeted a non-existent child. Replaced with `.header-cta` itself, so
  the CTA now renders stacked as designed (verified in the 1440 header screenshot).
- Mobile menu: was an in-flow column inside the header flex row — baseline screenshot
  showed links squeezed into a narrow right-hand strip with wrapped text, and the ☎ phone
  button stretched into a giant vertical cyan bar the full height of the open menu.
  Fixed: menu is now a full-width overlay under the sticky header
  (`position: absolute; left: 0; right: 0; top: 100%`, max-height 100dvh−5rem, scrollable),
  `.mobile-head` gets `align-items: center`. Verified: full-width readable links, phone
  button stays a normal square.

### Footer (now 5 columns — the ≥1024px grid was already 5-col, one slot was empty)
- Brand col: added **"● Crews Standing By 24/7"** (doc-verbatim trust fragment) above the
  NAP. NAP exact and unchanged: 400 S 129th E Ave, Tulsa, OK 74108 · (918) 395-9320.
- Services col: removed the misplaced **Contact** link (it belongs to the Emergency col,
  which already links /contact/).
- Service Area col: **"View all areas"** pointed at `/` (homepage — no areas hub exists).
  Now points at `/#which-tulsa-areas-do-you-serve`, the homepage's real areas section.
- Resources col (new): factual line (the /resources/ hub's own intro) + the single
  **Blog → /resources/** link. No individual blog links re-added (deliberately removed
  before; stays that way).
- Emergency Help col: unchanged (Call Now + Request Emergency Service buttons).
- Footer-bottom: unchanged — About Us · Blog · Contact · Sitemap. No privacy/terms links:
  those pages do not exist in the sitemap, so none were invented.
- Contrast fix (caught by viewed pixels): the brand-col phone link rendered in global
  link-blue #0056A3 on navy (~2.9:1, unreadable). Added `.footer-col p a` pale-on-navy
  rule (hover cyan-light).
- Console-404 fix (caught by the probe): desktop loads logged
  `Failed to load resource: 404` for `/sitemap.xml.txt?_rsc=...` — Next's `<Link>` was
  prefetching RSC data for `/sitemap.xml`, which is a static file, not a route. Changed
  the footer Sitemap link to a plain `<a href="/sitemap.xml">`. Console is now 0.
- Map rule verified unchanged: footer map on home + service pages, none on area/contact
  (they carry their own body map); exactly 1 iframe per page in the probe.

## Verification (fresh, after final rebuild)

| Check | Result |
|---|---|
| Header + footer distinct links fetched | **44, 0 broken** (was 43 before; +1 Blog link) |
| Sitemap URLs fetched | **53, 0 broken** |
| Overflow (1440/390, 4 pages) | **0** |
| H1 | **1** on all 4 pages |
| Console errors | **0** (was 1 per desktop page before the Sitemap-link fix) |
| Sticky header | 81px, stays visible after scroll, desktop + mobile |
| Desktop header CTA | visible (stacked EMERGENCY? + phone) |
| Mobile call bar | visible at 390, phone correct |
| Mobile menu | opens, full-width overlay, 42 links, all fetched 200 |
| Footer columns | 5, headings: Brand · Services · Service Area · Resources · Emergency Help |

## Notes / not defects
- The Google Maps iframe request fails in this sandbox (`ERR_TUNNEL_CONNECTION_FAILED`
  to google.com — no external network here). On a real browser with internet it loads;
  the embed markup, lazy loading and map rule are all verified. Not a site defect.
- Footer element screenshots show the sticky header overlapping the capture mid-frame —
  a locator-screenshot artifact (sticky header stays at viewport top while the footer
  element is scrolled into view), not a layout defect.
- No social links, certifications, reviews or invented links added anywhere.
