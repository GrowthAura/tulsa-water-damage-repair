#!/usr/bin/env python3
"""Technical SEO + schema probe for Tulsa Water Damage Repair (SEO rounds).
Fresh re-verification from scratch each pass — NOT a recycled report.

Usage:
  python3 tools/seo_probe.py --out ~/workspace/seo-build-tmp/out \
      --base http://127.0.0.1:8321 --pass 1
Reads content/pages.json + public/sitemap.xml + public/robots.txt from the
REAL site dir, checks the BUILT html in --out over HTTP at --base.
Writes site/qa-see-seo/seo-pass<N>.json + prints a defect list.
Exit 1 if any defect found.
"""
import argparse, json, os, re, sys, urllib.request, urllib.error
from html import unescape
from collections import Counter

SITE_DIR = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
QA = os.path.join(SITE_DIR, 'qa-see-seo')
HOST = 'https://tulsawaterdamagerepair.com'
PHONE = '(918) 395-9320'
ADDR = {'@type': 'PostalAddress', 'streetAddress': '400 S 129th E Ave', 'addressLocality': 'Tulsa',
        'addressRegion': 'OK', 'postalCode': '74108', 'addressCountry': 'US'}

def shortname(slug):
    """Mirror of lib.js shortName()."""
    last = slug.rstrip('/').split('/')[-1] or 'home'
    last = re.sub(r'-ok$', '', last)
    last = re.sub(r'-tulsa$', '', last)
    return ' '.join(w[:1].upper() + w[1:] for w in last.split('-'))

ap = argparse.ArgumentParser()
ap.add_argument('--out', required=True)
ap.add_argument('--base', required=True)
ap.add_argument('--pass', dest='passno', type=int, required=True)
args = ap.parse_args()
OUT = args.out
ROOT = args.base.rstrip('/')

pages = json.load(open(os.path.join(SITE_DIR, 'content', 'pages.json')))
BY_SLUG = {p['slug']: p for p in pages}
defects, notes = [], []

def fetch(path):
    try:
        with urllib.request.urlopen(ROOT + path, timeout=20) as r:
            return r.status, r.read().decode('utf-8', 'replace'), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), {}
    except Exception as e:
        return 0, str(e), {}

def norm(p):
    return '/' if p == '/' else p.rstrip('/')

# ---------- per-page checks over live HTTP ----------
results = {}
all_hrefs = Counter()
see_anchors = {}
commercial_inbound = []
for p in pages:
    slug = p['slug']
    row = {'slug': slug, 'defects': []}
    st, html, _h = fetch(slug)
    row['status'] = st
    if st != 200:
        row['defects'].append(f'canonical URL status {st}')
        results[slug] = row
        continue
    # variant form must also serve 200 (dual-file guarantee)
    variant = slug[:-1] if slug.endswith('/') and slug != '/' else slug + '/'
    st2, _, _ = fetch(variant)
    row['variant_status'] = st2
    if st2 != 200:
        row['defects'].append(f'variant {variant} status {st2}')
    # --- title / description verbatim ---
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    row['title'] = unescape(m.group(1)) if m else None
    if row['title'] != p['metaTitle']:
        row['defects'].append('title mismatch vs pages.json')
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    row['desc'] = unescape(m.group(1)) if m else None
    if row['desc'] != p['metaDescription']:
        row['defects'].append('meta description mismatch vs pages.json')
    if len(p['metaTitle']) > 60:
        row['defects'].append(f"TITLE-LENGTH-ONLY title {len(p['metaTitle'])} chars >60 (verbatim doc — report only)")
    if len(p['metaDescription']) > 160:
        row['defects'].append(f"DESC-LENGTH-ONLY description {len(p['metaDescription'])} chars >160 (verbatim doc — report only)")
    # --- canonical / og:url exactly 1 each, self-matching ---
    cans = re.findall(r'<link rel="canonical" href="([^"]*)"', html)
    row['canonicals'] = cans
    if len(cans) != 1:
        row['defects'].append(f'{len(cans)} canonical tags (want 1)')
    elif cans[0] != HOST + slug:
        row['defects'].append(f"canonical {cans[0]} != {HOST + slug}")
    ogurls = re.findall(r'<meta property="og:url" content="([^"]*)"', html)
    row['og_urls'] = ogurls
    if len(ogurls) != 1:
        row['defects'].append(f'{len(ogurls)} og:url tags (want 1)')
    elif ogurls[0] != HOST + slug:
        row['defects'].append(f"og:url {ogurls[0]} != {HOST + slug}")
    # --- og + twitter ---
    for tag, want in [('og:title', p['metaTitle']), ('og:description', p['metaDescription'])]:
        mm = re.findall(r'<meta property="%s" content="([^"]*)"' % tag, html)
        if len(mm) != 1:
            row['defects'].append(f'{len(mm)} {tag} tags (want 1)')
        elif unescape(mm[0]) != want:
            row['defects'].append(f'{tag} mismatch vs doc')
    for tag in ('og:type', 'og:site_name'):
        mm = re.findall(r'<meta property="%s" content="([^"]*)"' % tag, html)
        if len(mm) != 1:
            row['defects'].append(f'{len(mm)} {tag} tags (want 1)')
    mm = re.findall(r'<meta property="og:type" content="([^"]*)"', html)
    if mm and mm[0] != 'website':
        row['defects'].append(f"og:type={mm[0]} (want website)")
    mm = re.findall(r'<meta property="og:image" content="([^"]*)"', html)
    row['og_image'] = mm
    if len(mm) > 1:
        row['defects'].append(f'{len(mm)} og:image tags (want 0 or 1)')
    if mm:
        if not mm[0].startswith(HOST + '/'):
            row['defects'].append(f'og:image not absolute site URL: {mm[0]}')
        w = re.findall(r'<meta property="og:image:width" content="([^"]*)"', html)
        h = re.findall(r'<meta property="og:image:height" content="([^"]*)"', html)
        if w != ['1200'] or h != ['800']:
            row['defects'].append(f'og:image dims {w}x{h} (want 1200x800)')
    for tag, want in [('twitter:card', 'summary_large_image'),
                      ('twitter:title', p['metaTitle']),
                      ('twitter:description', p['metaDescription'])]:
        mm = re.findall(r'<meta name="%s" content="([^"]*)"' % tag, html)
        if len(mm) != 1:
            row['defects'].append(f'{len(mm)} {tag} tags (want 1)')
        elif unescape(mm[0]) != want:
            row['defects'].append(f'{tag} mismatch')
    twimg = re.findall(r'<meta name="twitter:image" content="([^"]*)"', html)
    if len(twimg) > 1:
        row['defects'].append(f'{len(twimg)} twitter:image tags')
    if bool(twimg) != bool(mm and row['og_image']):
        row['defects'].append('twitter:image presence != og:image presence')
    # --- H1 ---
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    h1txt = [unescape(re.sub(r'<[^>]+>', '', h)).strip() for h in h1s]
    row['h1'] = h1txt
    if len(h1txt) != 1:
        row['defects'].append(f'H1 count {len(h1txt)}')
    elif re.sub(r'\s+', ' ', h1txt[0]).strip() != re.sub(r'\s+', ' ', p['h1']).strip():
        row['defects'].append('H1 text mismatch vs doc')
    # --- images: alt present, no AI word, file exists ---
    for mimg in re.finditer(r'<img\b[^>]*>', html):
        tag = mimg.group(0)
        src = (re.search(r'src="([^"]*)"', tag) or [None, ''])[1]
        altm = re.search(r'alt="([^"]*)"', tag)
        if altm is None:
            row['defects'].append(f'img missing alt: {src}')
        elif altm.group(1).strip() == '':
            row['defects'].append(f'img empty alt: {src}')
        if re.search(r'(?i)\bai\b|ai-generated|artificial intelligence', (altm.group(1) if altm else '') + ' ' + src):
            row['defects'].append(f'AI word in img alt/src: {src}')
        if src.startswith('/'):
            code, _, _ = fetch(src.split('#')[0])
            if code != 200:
                row['defects'].append(f'img src 404: {src}')
    # --- See anchors (must be 0) ---
    see = re.findall(r'<a\b[^>]*>(?:<[^>]+>)*\s*See\b', html)
    see_anchors[slug] = len(see)
    if see:
        row['defects'].append(f'{len(see)} "See" anchors remain')
    # --- internal links: resolve + self-links in body + /commercial/ inbound ---
    hrefs = re.findall(r'<a\b[^>]*href="([^"]*)"', html)
    body = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
    body = re.sub(r'<header.*?</header>', '', body, flags=re.S)
    body = re.sub(r'<footer.*?</footer>', '', body, flags=re.S)
    body = re.sub(r'<section class="final-cta".*?</section>', '', body, flags=re.S)
    body = re.sub(r'<section class="section" style="padding: ?2\.5rem 0">.*?</section>', '', body, flags=re.S)  # NavyBand intro+CTA chrome
    body_hrefs = re.findall(r'<a\b[^>]*href="([^"]*)"', body)
    for href in set(body_hrefs):
        if norm(href.split('#')[0].split('?')[0]) == norm(slug) and href.split('#')[0]:
            row['defects'].append(f'body self-link: {href}')
    for href in set(hrefs):
        if href.startswith('/') and not href.startswith('//') and not href.startswith('/_next'):
            clean = href.split('#')[0].split('?')[0] or '/'
            all_hrefs[clean] += 1
            if clean == '/commercial/':
                commercial_inbound.append(slug)
            st3, _, _ = fetch(clean)
            if st3 != 200:
                row['defects'].append(f'broken internal link {href} -> {st3}')
    # --- JSON-LD ---
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    row['ld_scripts'] = len(lds)
    if len(lds) != 1:
        row['defects'].append(f'{len(lds)} JSON-LD scripts (want 1)')
        results[slug] = row
        continue
    try:
        ld = json.loads(lds[0])
    except Exception as e:
        row['defects'].append(f'JSON-LD unparseable: {e}')
        results[slug] = row
        continue
    graph = ld[0].get('@graph', []) if isinstance(ld, list) else ld.get('@graph', [])
    types = [g.get('@type') for g in graph]
    row['schema_types'] = types
    lb = next((g for g in graph if g.get('@type') == 'LocalBusiness'), None)
    if not lb:
        row['defects'].append('LocalBusiness MISSING from this page')
    else:
        if lb.get('telephone') != PHONE:
            row['defects'].append(f"LocalBusiness phone {lb.get('telephone')}")
        if lb.get('name') != 'Tulsa Water Damage Repair':
            row['defects'].append('LocalBusiness name mismatch')
        if lb.get('address') != ADDR:
            row['defects'].append(f"LocalBusiness address mismatch: {lb.get('address')}")
        if lb.get('@id') != HOST + '/#business':
            row['defects'].append(f"LocalBusiness @id {lb.get('@id')}")
    bc = next((g for g in graph if g.get('@type') == 'BreadcrumbList'), None)
    if not bc:
        row['defects'].append('BreadcrumbList MISSING')
    else:
        items = bc.get('itemListElement', [])
        # expected: Home + optional parent + self; homepage = Home only
        exp = [{'name': 'Home', 'item': HOST + '/'}]
        if p['type'] == 'service':
            exp.append({'name': 'Services', 'item': HOST + '/services/'})
        elif p['type'] == 'resource':
            exp.append({'name': 'Resources', 'item': HOST + '/resources/'})
        if p['type'] != 'homepage':
            exp.append({'name': shortname(slug), 'item': HOST + slug})
        got = [{'name': it.get('name'), 'item': it.get('item')} for it in items]
        poss = [it.get('position') for it in items]
        if poss != list(range(1, len(items) + 1)):
            row['defects'].append(f'breadcrumb positions {poss}')
        if got != exp:
            row['defects'].append(f'breadcrumb mismatch: got {got} want {exp}')
        # JSON-LD breadcrumb names must match the VISIBLE breadcrumb text
        vis_last = re.search(r'<span aria-current="page">([^<]+)</span>', html)
        if p['type'] != 'homepage' and vis_last and items:
            if items[-1].get('name') != vis_last.group(1).strip():
                row['defects'].append(f"breadcrumb last name JSON-LD {items[-1].get('name')!r} != visible {vis_last.group(1).strip()!r}")
        vis_parents = re.findall(r'<nav class="crumbs"[^>]*>(.*?)</nav>', html, re.S)
        if vis_parents:
            vis_links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', vis_parents[0])
            # visible parent links (skip Home) must match JSON-LD parent items
            jl_parents = [(it.get('item', '').replace(HOST, ''), it.get('name')) for it in items[1:-1]]
            if vis_links[1:] != jl_parents:
                row['defects'].append(f'breadcrumb parents visible {vis_links[1:]} != JSON-LD {jl_parents}')
    faq = next((g for g in graph if g.get('@type') == 'FAQPage'), None)
    faqs = p.get('faqs') or []
    if faqs and not faq:
        row['defects'].append('FAQPage MISSING (page has FAQs)')
    if not faqs and faq:
        row['defects'].append('FAQPage present but page has 0 FAQs')
    if faq:
        ents = faq.get('mainEntity', [])
        if len(ents) != len(faqs):
            row['defects'].append(f'FAQ schema count {len(ents)} != visible {len(faqs)}')
        else:
            for qe, qv in zip(ents, faqs):
                if qe.get('@type') != 'Question' or qe.get('name') != unescape(qv['q']):
                    row['defects'].append(f"FAQ schema Q mismatch: {qv['q'][:50]}")
                    break
                ans = qe.get('acceptedAnswer', {})
                if ans.get('@type') != 'Answer' or ans.get('text') != unescape(qv['a_text']):
                    row['defects'].append(f"FAQ schema A mismatch: {qv['q'][:50]}")
                    break
        # visible FAQ questions are the <h3> inside each <summary> in .faq-list
        vis_qs = [unescape(q) for q in re.findall(r'<summary>\s*<h3>([^<]+)</h3>', html)]
        schema_qs = [e.get('name') for e in ents]
        if sorted(vis_qs) != sorted(schema_qs):
            row['defects'].append(f'visible FAQ questions {len(vis_qs)} != schema Q {len(schema_qs)}')
    # WebPage / Service / WebSite sanity
    if p['type'] == 'service' and 'Service' not in types:
        row['defects'].append('Service schema missing on service page')
    if 'WebSite' not in types:
        row['defects'].append('WebSite schema missing')
    results[slug] = row

# ---------- sitemap / robots ----------
st, sm, _ = fetch('/sitemap.xml')
sm_locs = re.findall(r'<loc>([^<]+)</loc>', sm) if st == 200 else []
sm_mods = re.findall(r'<lastmod>([^<]+)</lastmod>', sm)
sitemap = {'status': st, 'count': len(sm_locs), 'lastmod_count': len(sm_mods),
           'lastmod_values': sorted(set(sm_mods)),
           'set_equals_canonical': set(sm_locs) == {HOST + p['slug'] for p in pages},
           'has_image_entries': ('<image:image' in sm or 'image:' in sm)}
if st != 200:
    defects.append('sitemap.xml status ' + str(st))
if len(sm_locs) != 53:
    defects.append(f'sitemap count {len(sm_locs)} != 53')
if len(sm_mods) != 53:
    defects.append(f'sitemap lastmod count {len(sm_mods)} != 53')
if not sitemap['set_equals_canonical']:
    defects.append(f"sitemap loc set != canonical set: {set(sm_locs) ^ {HOST + p['slug'] for p in pages}}")
if sitemap['has_image_entries']:
    defects.append('sitemap contains image entries')
st, rb, _ = fetch('/robots.txt')
robots = {'status': st, 'body': rb}
if st != 200:
    defects.append(f'robots.txt status {st}')
if 'Sitemap: https://tulsawaterdamagerepair.com/sitemap.xml' not in rb:
    defects.append('robots.txt missing/incorrect Sitemap line')
if 'User-agent: *' not in rb or 'Allow: /' not in rb:
    defects.append('robots.txt missing User-agent/Allow')

# ---------- orphan BFS from home ----------
seen, queue = set(), ['/']
while queue:
    cur = norm(queue.pop())
    if cur in seen:
        continue
    seen.add(cur)
    stc, htmlc, _ = fetch(cur)
    if stc != 200:
        continue
    for href in re.findall(r'<a\b[^>]*href="([^"]*)"', htmlc):
        if href.startswith('/') and not href.startswith('//'):
            clean = href.split('#')[0].split('?')[0] or '/'
            if clean and norm(clean) not in seen:
                queue.append(clean)
orphans = sorted(p['slug'] for p in pages if norm(p['slug']) not in seen)

# ---------- trailing-slash consistency ----------
slash_forms = {}
for p in pages:
    slash_forms[p['slug']] = 'slash' if p['slug'].endswith('/') else 'noslash'
sm_noslash = [u for u in sm_locs if not u.endswith('/')]
canon_noslash = [HOST + p['slug'] for p in pages if not p['slug'].endswith('/')]
slash_mismatch = set(sm_noslash) ^ set(canon_noslash)

all_defects = []
for slug, row in results.items():
    for d in row['defects']:
        all_defects.append(f'{slug}: {d}')
for d in defects:
    all_defects.append(d)
if orphans:
    all_defects.append(f"ORPHANS (unreachable from home by BFS): {orphans}")
if slash_mismatch:
    all_defects.append(f'trailing-slash sitemap/canonical mismatch: {slash_mismatch}')
real_defects = [d for d in all_defects if 'LENGTH-ONLY' not in d]
length_only = [d for d in all_defects if 'LENGTH-ONLY' in d]

report = {
    'pass': args.passno, 'pages': len(pages),
    'status_non200': {s: r['status'] for s, r in results.items() if r['status'] != 200},
    'variant_non200': {s: r['variant_status'] for s, r in results.items() if r.get('variant_status') != 200},
    'see_anchors_total': sum(see_anchors.values()),
    'see_anchors_by_page': {k: v for k, v in see_anchors.items() if v},
    'commercial_inbound_from': sorted(set(commercial_inbound)),
    'orphans': orphans,
    'reachable_from_home': len(seen),
    'sitemap': sitemap, 'robots': {'status': robots['status']},
    'slash_mismatch': sorted(slash_mismatch),
    'defects': real_defects, 'length_only_notes': length_only,
    'per_page': {s: {'defects': r['defects'], 'schema_types': r.get('schema_types')} for s, r in results.items()},
}
os.makedirs(QA, exist_ok=True)
with open(os.path.join(QA, f'seo-pass{args.passno}.json'), 'w') as f:
    json.dump(report, f, indent=2)
print(f"PASS {args.passno}: pages={len(pages)} defects={len(real_defects)} (length-only notes={len(length_only)})")
print(f"  see_anchors={sum(see_anchors.values())} commercial_inbound={sorted(set(commercial_inbound))} orphans={orphans}")
print(f"  sitemap={sitemap['count']} locs, lastmod={sitemap['lastmod_count']}, set==canonical: {sitemap['set_equals_canonical']}")
for d in real_defects:
    print('  -', d)
print('  LENGTH-ONLY (verbatim, report only):')
for d in sorted(set(length_only)):
    print('   *', d.split(': ', 1)[-1], '| pages:', sum(1 for x in length_only if x.split(': ', 1)[-1] == d.split(': ', 1)[-1]))
sys.exit(1 if real_defects else 0)
