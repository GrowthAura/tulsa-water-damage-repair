#!/usr/bin/env python3
"""Site-wide repeat audit: all 53 sitemap routes, one page at a time.
Flags, per page (main content only: between </header> and the final CTA):
  A. duplicate card title hrefs (same service/area/resource card twice)
  B. duplicate H2 texts on the same page
  C. same href as BOTH a card link AND a plain body link (cards-vs-list pattern)
  D. same image file used twice on the same page
  E. same href linked twice in plain body prose (doc cross-links; reported only)
Header/footer/nav links are excluded. Run after export; serve not needed.
Usage: python3 tools/audit_repeats.py
"""
import json, os, re
from collections import Counter
from urllib.parse import urlparse

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'out')

sitemap = open(os.path.join(BASE, 'public', 'sitemap.xml')).read()
urls = re.findall(r'<loc>(https://www\.tulsawaterdamagerepair\.com([^<]*))</loc>', sitemap)
print(f'routes in sitemap: {len(urls)}')


def resolve(slug):
    slug = slug or '/'
    if slug == '/':
        return os.path.join(OUT, 'index.html')
    p = slug.strip('/')
    d = os.path.join(OUT, p, 'index.html')
    if os.path.exists(d):
        return d
    f = os.path.join(OUT, p + '.html')
    if os.path.exists(f):
        return f
    return None


def norm(h):
    # compare hrefs ignoring the trailing slash: Next <Link> renders card
    # hrefs with a trailing slash while doc prose links keep the doc's form.
    if h and h != '/' and h.endswith('/'):
        return h[:-1]
    return h


def main_slice(html):
    # main content: after the header, before the final CTA section
    start = html.find('</header>')
    end = html.find('<section class="final-cta"')
    if start < 0 or end < 0:
        return html
    return html[start:end]


rows = []
for _full, slug in urls:
    path = resolve(slug)
    if not path:
        rows.append((slug, 'UNRESOLVED FILE', '', ''))
        continue
    html = open(path).read()
    main = main_slice(html)

    # A. card title hrefs
    card_hrefs = re.findall(r'<article class="card[^"]*">.*?<h3><a href="([^"]+)"', main, re.S)
    dup_cards = [k for k, v in Counter(card_hrefs).items() if v > 1]

    # B. duplicate H2s (visible text, entities kept)
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', main, re.S)
    h2_text = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s]
    dup_h2 = [k for k, v in Counter(h2_text).items() if v > 1]

    # C. card hrefs also present as plain body links (strip card articles first)
    no_cards = re.sub(r'<article class="card[^"]*">.*?</article>', '', main, flags=re.S)
    plain_hrefs = re.findall(r'<a href="([^"]+)"', no_cards)
    plain_set = set(norm(p) for p in plain_hrefs)
    card_set = set(norm(c) for c in card_hrefs)
    both = sorted(card_set & plain_set)

    # D. duplicate images on the page (whole file: hero + cards + body)
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    dup_imgs = [k for k, v in Counter(imgs).items() if v > 1]

    # E. plain body hrefs linked twice or more (doc prose cross-links)
    dup_plain = [k for k, v in Counter(norm(p) for p in plain_hrefs).items() if v > 1]

    rows.append((slug, dup_cards, dup_h2, both, dup_imgs, dup_plain))

print()
print('=== A. duplicate card hrefs ===')
bad = [r for r in rows if len(r) > 2 and r[1]]
print('pages with dup cards:', len(bad))
for r in bad:
    print(' ', r[0], r[1])

print()
print('=== B. duplicate H2s ===')
bad = [r for r in rows if len(r) > 2 and r[2]]
print('pages with dup H2:', len(bad))
for r in bad:
    print(' ', r[0], r[2])

print()
print('=== C. href as BOTH card link and plain body link ===')
bad = [r for r in rows if len(r) > 3 and r[3]]
print('pages with card+plain overlap:', len(bad))
for r in bad:
    print(' ', r[0], r[3])

print()
print('=== D. duplicate images on one page ===')
bad = [r for r in rows if len(r) > 4 and r[4]]
print('pages with dup images:', len(bad))
for r in bad:
    print(' ', r[0], r[4])

print()
print('=== E. plain body href linked 2+ times (doc prose; report only) ===')
bad = [r for r in rows if len(r) > 5 and r[5]]
print('pages with repeated plain hrefs:', len(bad))
for r in bad:
    print(' ', r[0], r[5])
