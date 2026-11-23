#!/usr/bin/env python3
"""Generate public/sitemap.xml — MOST ADVANCED (Google 2026 best practice):
per URL: <loc> + <lastmod> + <image:image>/<image:loc> for EVERY meaningful
photo actually on that page (hero + content/card photos), NOT just the hero.
- NO <title> on <url> (no such field exists in the sitemaps protocol;
  page titles live in HTML <title>/H1/og:title).
- NO <changefreq> / <priority> (Google ignores both).
- NO image:title / image:caption / image:geo_location / image:license
  (deprecated by Google May 2022, no effect after 2022-08-06).
- NO video / news / hreflang (no videos, not a news publisher, single-language).
- Image URLs are read from the BUILT out/ HTML (ground truth of what is on
  each page) — a photo is listed only if it is actually rendered on that page.
  Falls back to the page's hero file if the built HTML is not present.
  All images are /images/*.webp real photos (no logos/icons in /images/).
- lastmod is DATE-ONLY (YYYY-MM-DD). Four dates (his order 2026-11-23):
  2026-11-23 on the 24 pages with substantive Nov 23 changes (follow-up
  round + 4 cuts: homepage, About, the 4 directional areas, all 18
  services — eyebrow cut + new schema + text/header), 2026-11-22 on the
  18 pages whose last substantive change was the Nov 22 rebuild (other
  15 areas, Contact, services hub, commercial), 2026-11-07 on the 10
  resource guides (blogs, unchanged — his order), 2026-11-12 on the
  resources hub (unchanged). NOTE: no page carries a date it did not
  actually change on — Nov 22 = rebuild day, Nov 23 = follow-up + cuts
  day, both real change days (unlike the 2026-11-13 request, which had
  zero commits and was refused as a false date).
"""
import json, os, re, sys
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
DOMAIN = 'https://www.tulsawaterdamagerepair.com'

# 24 pages with substantive Nov 23 changes (honest only — never stamp a
# date a page did not actually change on). Follow-up round + 4 cuts.
NOV23_PAGES = {
    '/',
    '/about-us',
    '/service-areas/south-tulsa',
    '/service-areas/west-tulsa',
    '/service-areas/north-tulsa',
    '/service-areas/east-tulsa',
    '/services/ac-drain-line-overflow-cleanup',
    '/services/appliance-leak-water-damage',
    '/services/burst-pipe-water-damage',
    '/services/ceiling-water-damage',
    '/services/commercial-water-damage',
    '/services/emergency-water-damage-restoration',
    '/services/fire-damage-restoration',
    '/services/flood-damage-restoration',
    '/services/flooded-basement-cleanup',
    '/services/hardwood-floor-drying',
    '/services/mold-remediation',
    '/services/roof-leak-water-damage',
    '/services/sewage-backup-cleanup',
    '/services/slab-leak-water-damage',
    '/services/smoke-soot-damage-cleanup',
    '/services/storm-damage-repair',
    '/services/water-heater-leak-cleanup',
    '/services/water-mitigation',
}

def hero_file(slug):
    """Hero image filename for a page (verified to exist in public/images/)."""
    if slug == '/':
        return 'home-tulsa-water-damage-repair.webp'
    if slug == '/resources':
        return 'resources-hub-tulsa-water-damage-repair.webp'
    return slug.strip('/').replace('/', '-') + '-tulsa-water-damage-repair.webp'

def lastmod_for(slug):
    if slug in NOV23_PAGES:
        return '2026-11-23'
    if slug.startswith('/resources/'):
        return '2026-11-07'
    if slug == '/resources':
        return '2026-11-12'
    return '2026-11-22'

def images_for(slug):
    """Every /images/ photo actually rendered on this page (built HTML)."""
    html_path = os.path.join(BASE, 'out', 'index.html') if slug == '/' else os.path.join(BASE, 'out' + slug + '.html')
    if os.path.exists(html_path):
        html = open(html_path, encoding='utf-8', errors='ignore').read()
        imgs = sorted(set(re.findall(r'src="(/images/[^"]+\.(?:webp|jpg|jpeg|png))"', html)))
        if imgs:
            return imgs
    # Fallback: no <img src> on this page (e.g. /contact has a null hero) —
    # return NO images. Never invent a hero filename: the old fallback
    # derived '<slug>-tulsa-water-damage-repair.webp' and listed the deleted
    # contact orphan in the sitemap (verification 2026-11-22).
    return []

urls = sorted({p['slug'] for p in pages})
assert len(urls) == 53, f'expected 53 urls, got {len(urls)}'
assert len(NOV23_PAGES) == 24, f'expected 24 Nov-23 pages, got {len(NOV23_PAGES)}'

# Verify every listed image file exists in public/images/ before writing.
total_imgs = 0
page_images = {}
for u in urls:
    imgs = images_for(u)
    for im in imgs:
        f = os.path.join(BASE, 'public', im.lstrip('/'))
        assert os.path.exists(f), f'image missing for {u}: {im}'
    page_images[u] = imgs
    total_imgs += len(imgs)

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
counts = {}
for u in urls:
    lm = lastmod_for(u)
    counts[lm] = counts.get(lm, 0) + 1
    lines.append('  <url>')
    lines.append(f'    <loc>{DOMAIN}{u}</loc>')
    lines.append(f'    <lastmod>{lm}</lastmod>')
    for im in page_images[u]:
        lines.append('    <image:image>')
        lines.append(f'      <image:loc>{DOMAIN}{im}</image:loc>')
        lines.append('    </image:image>')
    lines.append('  </url>')
lines.append('</urlset>')
open(os.path.join(BASE, 'public', 'sitemap.xml'), 'w').write('\n'.join(lines) + '\n')
print(f'sitemap.xml: {len(urls)} URLs, {total_imgs} image entries, lastmod counts: {counts}')
