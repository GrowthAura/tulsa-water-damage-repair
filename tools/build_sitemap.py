#!/usr/bin/env python3
"""Generate public/sitemap.xml (URLs ONLY — no image entries, no noindex URL)
and public/robots.txt from site/content/pages.json. Canonical forms are the
doc's exact slugs."""
import json, os
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
LASTMOD = '2026-11-07'
urls = sorted({p['slug'] for p in pages})
assert len(urls) == 53, f'expected 53 urls, got {len(urls)}'
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    lines.append('  <url>')
    lines.append(f'    <loc>{DOMAIN}{u}</loc>')
    lines.append(f'    <lastmod>{LASTMOD}</lastmod>')
    lines.append('  </url>')
lines.append('</urlset>')
open(os.path.join(BASE, 'public', 'sitemap.xml'), 'w').write('\n'.join(lines) + '\n')
robots = ('User-agent: *\nAllow: /\n\n'
          f'Sitemap: {DOMAIN}/sitemap.xml\n'
          f'Host: tulsawaterdamagerepair.com\n')
open(os.path.join(BASE, 'public', 'robots.txt'), 'w').write(robots)
print(f'sitemap.xml: {len(urls)} URLs, no image entries')
print('robots.txt written')
