#!/usr/bin/env python3
"""A-to-Z sitewide check (design round): overflow 390/320 + H1=1 + console
errors for all 53 routes, card-image load counts, header/footer + sitemap
link check (local HTTP), FAQ schema vs visible Q&A.
Usage: python3 tools/probe_a2z.py
Writes site/qa-design/a2z.json
"""
import json, os, re, urllib.request
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-design')
ROOT = 'http://127.0.0.1:8317'
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
res = {'routes': {}, 'links': {}, 'faq': {}}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for p in pages:
        slug = p['slug']
        row = {'h1': None, 'overflow': {}, 'console': []}
        for w in (390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(350)
            row['overflow'][w] = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            if w == 390:
                row['h1'] = pg.evaluate("() => document.querySelectorAll('h1').length")
                row['console'] = sorted(set(errs))
            ctx.close()
        res['routes'][slug] = row
    # card images loaded on home / hub / resources
    for slug in ('/', '/services/', '/resources/'):
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(1200)
        n = pg.evaluate("() => [...document.querySelectorAll('.card img')].filter(im => im.complete && im.naturalWidth > 0).length + '/' + document.querySelectorAll('.card img').length")
        res['routes'][slug]['card_imgs'] = n
        ctx.close()
    browser.close()

# ---- link check over out/ html (local server) ----
html_files = []
for root, _d, fs in os.walk(os.path.join(BASE, 'out')):
    for f in fs:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))
hrefs = set()
for f in html_files:
    t = open(f, encoding='utf-8').read()
    for m in re.findall(r'href="([^"]+)"', t):
        if m.startswith('/') and not m.startswith('//'):
            hrefs.add(m.split('#')[0].split('?')[0] or '/')
    for m in re.findall(r'src="([^"]+)"', t):
        if m.startswith('/') and not m.startswith('//'):
            hrefs.add(m.split('#')[0].split('?')[0] or '/')
broken = []
for h in sorted(hrefs):
    if h in ('/', ''):
        continue
    try:
        req = urllib.request.Request(ROOT + h, method='GET')
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status != 200:
                broken.append((h, r.status))
    except Exception as e:
        broken.append((h, getattr(e, 'code', str(e))))
res['links'] = {'internal_refs': len(hrefs), 'broken': broken}
# ---- sitemap ----
sm = open(os.path.join(BASE, 'public', 'sitemap.xml'), encoding='utf-8').read()
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
res['sitemap'] = {'count': len(locs), 'in_pages_json': sum(1 for u in locs if any(u.endswith(p['slug'].rstrip('/')) or u == 'https://tulsawaterdamagerepair.com/' and p['slug'] == '/' for p in pages))}
# ---- FAQ schema vs visible ----
bad_faq = []
for p in pages:
    slug = p['slug']
    path = os.path.join(BASE, 'out', slug.strip('/') or 'index')
    html_path = path + '.html' if os.path.exists(path + '.html') else os.path.join(path, 'index.html')
    if not os.path.exists(html_path):
        continue
    t = open(html_path, encoding='utf-8').read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not m:
        continue
    try:
        ld = json.loads(m.group(1))
    except Exception:
        bad_faq.append((slug, 'unparseable json-ld'))
        continue
    graph = ld[0].get('@graph', []) if isinstance(ld, list) else []
    faq = next((g for g in graph if g.get('@type') == 'FAQPage'), None)
    vis_qs = re.findall(r'<h3>([^<]+)</h3>', t)
    if faq:
        schema_qs = [e['name'] for e in faq.get('mainEntity', [])]
        if sorted(schema_qs) != sorted([q for q in vis_qs if q in [f['q'] for f in p.get('faqs', [])]]):
            if set(schema_qs) != set(f['q'] for f in p.get('faqs', [])):
                bad_faq.append((slug, 'schema vs doc faqs differ'))
    elif p.get('faqs'):
        bad_faq.append((slug, 'has faqs but no FAQPage schema'))
res['faq'] = {'mismatches': bad_faq}
json.dump(res, open(os.path.join(OUT, 'a2z.json'), 'w'), indent=1)
ov = [(s, r['overflow']) for s, r in res['routes'].items() if r['overflow'].get(390, 0) > 0 or r['overflow'].get(320, 0) > 0]
h1bad = [(s, r['h1']) for s, r in res['routes'].items() if r['h1'] != 1]
con = [(s, r['console']) for s, r in res['routes'].items() if r['console']]
print('routes:', len(res['routes']), '| overflow pages:', len(ov), ov)
print('h1 != 1:', h1bad)
print('console errors:', con)
print('card imgs:', {s: res['routes'][s].get('card_imgs') for s in ('/', '/services/', '/resources/')})
print('internal refs:', res['links']['internal_refs'], '| broken:', res['links']['broken'])
print('sitemap:', res['sitemap'])
print('faq mismatches:', res['faq']['mismatches'])
