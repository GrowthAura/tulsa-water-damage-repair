#!/usr/bin/env python3
"""Generate public/sitemap.xml (URLs ONLY — no image entries, no noindex URL)
and public/robots.txt from site/content/pages.json. Canonical forms are the
doc's exact slugs."""
import json, os
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
# lastmod is DATE-ONLY (YYYY-MM-DD, no time component). Split across the two
# work days, from the rounds' records (never invented):
# - 2026-11-08: the 51 pages whose content/links changed on 2026-11-08 —
#   48 pages via the dedupe/doc-audit round (commit 4f51b09, verified by
#   diffing content/pages.json 0b822f6 -> HEAD); /about-us/,
#   /services/fire-damage-restoration and /services/smoke-soot-damage-cleanup
#   via this round's See cuts; homepage via cards + See cuts; the 10 guides
#   via Tier 1 Article schema (all 10 are inside the 48).
# - 2026-11-07: the only 2 pages with NO content/link change on 2026-11-08:
#   /contact/ and /resources/ (no dedupe/doc-audit edit, no See cut, no cards).
LASTMOD_DEFAULT = '2026-11-08'
LASTMOD_2026_11_07 = {'/contact/', '/resources/'}
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
