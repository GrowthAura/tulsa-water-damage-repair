#!/usr/bin/env python3
"""Generate public/sitemap.xml (URLs ONLY — no image entries, no noindex URL)
and public/robots.txt from site/content/pages.json. Canonical forms are the
doc's exact slugs."""
import json, os
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
# lastmod is DATE-ONLY (YYYY-MM-DD, no time component). Rule (2026-11-08
# no-slash round): EVERY page's URL and/or links changed in this round —
# the 29 flipped pages changed URL, and the other 24 changed because the
# header/footer/hub links on every page flipped to no-slash forms — so all
# 53 pages carry 2026-11-08. Verified by diffing the rendered output of
# every page against the pre-round build (see
# FINDINGS-url-noslash-technical-seo-2x.md, word-diff section).
LASTMOD_DEFAULT = '2026-11-08'
LASTMOD_2026_11_07 = set()
urls = sorted({p['slug'] for p in pages})
assert len(urls) == 53, f'expected 53 urls, got {len(urls)}'
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    lines.append('  <url>')
    lines.append(f'    <loc>{DOMAIN}{u}</loc>')
    lines.append(f'    <lastmod>{"2026-11-07" if u in LASTMOD_2026_11_07 else LASTMOD_DEFAULT}</lastmod>')
    lines.append('  </url>')
lines.append('</urlset>')
open(os.path.join(BASE, 'public', 'sitemap.xml'), 'w').write('\n'.join(lines) + '\n')
# NOTE: this script used to also write a minimal robots.txt — REMOVED.
# public/robots.txt is maintained separately with the 22-group AI-bot Allows
# (Tier 1 + Phase 2); regenerating the minimal version here would regress it.
print(f'sitemap.xml: {len(urls)} URLs, no image entries')
