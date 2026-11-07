# Text-size + colouring pass — FINDINGS

- Date: 2026-11-07 ~14:40 PKT. Scope: CSS only (`app/globals.css`), no words/images/links/schema/phone/layout changed. H1/H2/H3 sizes and the H2 navy / H3 blue colours from the wide pass are untouched.
- Probe: `site/tools/probe_text.py` (new) — computed font-size/line-height/colour/background/WCAG contrast at 1440/390/320, homepage + emergency service + Broken Arrow area + contact. Screenshots: `site/qa-text/` (before-*/after-* desktop full + mobile top), viewed by pixels.

## Before → after (measured, desktop 1440; mobile 390 in brackets)

| Element | Before | After |
|---|---|---|
| Body paragraph | 16px / lh 28px, slate #29485E, 8.69:1 | **18px / lh 31.5px, ink #17324A, 11.91:1** |
| List item | 16px / lh 27.2px, slate, 8.69:1 | **18px / lh 31.5px, ink, 11.91:1** |
| FAQ answer | 16px / lh 28px, slate, 8.69:1 | **18px / lh 31.5px, ink, 11.91:1** |
| Hero intro (home) | 20px [17.28px] / lh 34px, pale on navy, 9.46:1 | **23.2px [19.2px] / lh 38.3px, pale on navy, 9.46:1** |
| Navy-band lead (inner pages) | 20px [17.28px] / lh 34px, pale on navy, 9.46:1 | **23.2px [19.2px] / lh 38.3px, pale on navy, 9.46:1** |
| Table cell | 15.2px / lh 24.3px, slate on white, 9.62:1 | **16.8px / lh 27.7px, ink on white, 13.19:1** |
| Card blurb | 15.2px / lh 26.6px, ink, 11.91:1 | **16.8px / lh 28.6px, ink, 11.91:1** |
| Body link | 16px, blue #0056A3 on cream, 6.63:1 | **18px, blue, 6.63:1** (now underlined, pale underline; hover navy + cyan underline) |
| Brand-panel text | 15.2px, pale on navy, 9.46:1 | **16.8px, pale on navy, 9.46:1** |
| Brand-panel list item | 13.6px (0.85rem) | **15.2px (0.95rem)** |
| Footer text / link | 14.72px, pale on navy, 9.46:1 | **16px, pale on navy, 9.46:1** |
| Breadcrumb | 13.6px, slate, 8.69:1 | **14.4px, slate, 8.69:1** |
| Form label | 14.4px, ink on white, 13.19:1 | **15.2px, ink on white, 13.19:1** |
| Form input / note | 15.2px / 14.4px | **16px / 15.2px** |
| Trust-band item | 13px (0.8125rem) | **14.4px (0.9rem)** |
| Mobile call bar | 16px | **16.8px (1.05rem)** |
| FAQ question (H3) | 18.4px (1.15rem) | **20px (1.25rem)** |
| Card title (H3 link) | 20px, blue, 6.63:1 | unchanged (heading sizes kept) |

## Colouring (Edmond palette only — no new colours)

- Body text: slate #29485E → **ink #17324A** (richer dark navy, contrast 8.69 → 11.91:1 on cream). Navy sections keep their explicit pale-text overrides, so nothing on navy changed colour.
- Lead paragraphs on cream: **navy #073B66** (`.content-block p.lead` rule; navy-band leads keep their inline pale colour). Note: no `.content-block p.lead` element exists in the current template — the real lead text is the navy-band lead, which grew to 23.2px. The rule is dormant but harmless.
- Bold lead-ins in body copy: **navy #073B66** (`.content-block strong`), hierarchy without new colours.
- Body links: blue #0056A3 kept, **soft pale underline added** (hover: navy + cyan underline) so links stay visible on every background. Buttons, nav, card titles and footer links are untouched by this rule (scoped to `p a` / `li a` / `.faq-answer a`).
- Muted/small text stays slate (breadcrumbs) or pale-on-navy (footer, trust band) — distinct from body ink.

## Verification (fresh, after rebuild)

- Build: `npm run export` green, 56/56 static pages.
- Overflow **0** at 1440 / 390 / 320 on all 4 sampled pages; H1 = 1 everywhere; console errors **0**.
- Contrast probe: **0 fails** (<4.5:1) across all measured targets at all widths.
- Screenshots viewed by pixels (desktop tops + mobile tops, homepage + emergency service): larger readable text, navy H2, blue H3, bold navy lead-ins, sticky aside still beside the text, no text under the image, call bar visible.
- Sticky aside: still `position: sticky` at desktop (verified in the wide pass; layout untouched by this pass).

## Notes

- The top bar above the header is absent in the after screenshots — the parallel refine agent removed it (its item, not this pass).
- The service-page hero photo is the refine agent's image domain (not changed here).
- No content, image, link, schema, phone, or layout-structure change in this pass.
