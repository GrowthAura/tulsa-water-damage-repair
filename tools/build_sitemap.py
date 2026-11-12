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
- lastmod is DATE-ONLY (YYYY-MM-DD). Three dates (his order 2026-11-12,
  to avoid a bulk-stamp penalty): TODAY (2026-11-12) on the 10 key pages,
  2026-11-07 on the 10 resource guides, 2026-11-08 on the other 33.
"""
import json, os, re, sys
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
TODAY = '2026-11-12'

# 10 key pages carry today's date (his order: ~10 pages on today).
TODAY_PAGES = {
    '/',
    '/services',
    '/services/emergency-water-damage-restoration',
    '/services/water-mitigation',
    '/services/mold-remediation',
    '/services/flood-damage-restoration',
    '/services/burst-pipe-water-damage',
    '/commercial',
    '/contact',
    '/resources',
}

def hero_file(slug):
    """Hero image filename for a page (verified to exist in public/images/)."""
    if slug == '/':
        return 'home-tulsa-water-damage-repair.webp'
    if slug == '/resources':
        return 'resources-hub-tulsa-water-damage-repair.webp'
    return slug.strip('/').replace('/', '-') + '-tulsa-water-damage-repair.webp'

def lastmod_for(slug):
    if slug in TODAY_PAGES:
        return TODAY
    if slug.startswith('/resources/'):
        return '2026-11-07'
    return '2026-11-08'

def images_for(slug):
    """Every /images/ photo actually rendered on this page (built HTML)."""
    html_path = os.path.join(BASE, 'out', 'index.html') if slug == '/' else os.path.join(BASE, 'out' + slug + '.html')
    if os.path.exists(html_path):
        html = open(html_path, encoding='utf-8', errors='ignore').read()
        imgs = sorted(set(re.findall(r'src="(/images/[^"]+\.(?:webp|jpg|jpeg|png))"', html)))
        if imgs:
            return imgs
    # Fallback: hero only (built HTML not present yet).
    return ['/images/' + hero_file(slug)]

urls = sorted({p['slug'] for p in pages})
assert len(urls) == 53, f'expected 53 urls, got {len(urls)}'
assert len(TODAY_PAGES) == 10, f'expected 10 today pages, got {len(TODAY_PAGES)}'

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
