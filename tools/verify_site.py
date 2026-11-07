#!/usr/bin/env python3
"""Structural verification of the built site (Round 1).
Serves out/ on :8317, then checks every canonical URL + variant:
200 direct, H1=1, title/description verbatim vs doc, canonical self-match,
sitemap/robots, all internal hrefs resolve, no old-brand strings,
no leftover link notation, FAQ schema matches visible Q&A.
Writes site/FINDINGS-round1.md. Exit 1 on any failure.
"""
import json, os, re, sys, urllib.request, urllib.error
from html import unescape
from collections import Counter
from html.parser import HTMLParser

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
PORT = 8317
ROOT = f'http://127.0.0.1:{PORT}'
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
FINDINGS = []

def fetch(path, expect=200):
    try:
        with urllib.request.urlopen(ROOT + path, timeout=20) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')
    except Exception as e:
        return 0, str(e)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = []
        self.title = ''
        self._in_title = False
        self._in_h1 = False
        self.imgs = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'a' and 'href' in d:
            self.links.append(d['href'])
        if tag == 'h1':
            self._in_h1 = True
        if tag == 'title':
            self._in_title = True
        if tag == 'img':
            self.imgs.append((d.get('src', ''), d.get('alt', ''), d.get('width', ''), d.get('height', '')))
    def handle_endtag(self, tag):
        if tag == 'h1': self._in_h1 = False
        if tag == 'title': self._in_title = False
    def handle_data(self, data):
        if self._in_h1: self.h1.append(data.strip())
        if self._in_title: self.title += data.strip()

def canon(path):
    return 'https://www.tulsawaterdamagerepair.com' + path

problems = []
checked_links = Counter()
for p in pages:
    slug = p['slug']
    st, html = fetch(slug)
    if st != 200:
        problems.append(f'{slug}: canonical status {st}')
        continue
    # variant form must also serve 200 (dual-file guarantee)
    variant = slug[:-1] if slug.endswith('/') and slug != '/' else slug + '/'
    st2, _ = fetch(variant)
    if st2 != 200:
        problems.append(f'{slug}: variant {variant} status {st2}')
    lp = LinkParser()
    lp.feed(html)
    h1s = [h for h in lp.h1 if h]
    if len(h1s) != 1:
        problems.append(f'{slug}: H1 count {len(h1s)} -> {h1s[:2]}')
    elif h1s[0] != re.sub(r'\s+', ' ', p['h1']).strip():
        problems.append(f"{slug}: H1 mismatch: {h1s[0][:80]!r} vs doc {p['h1'][:80]!r}")
    if lp.title != p['metaTitle']:
        problems.append(f"{slug}: <title> mismatch")
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    if not m or unescape(m.group(1)) != p['metaDescription']:
        problems.append(f'{slug}: meta description mismatch')
    m = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    if not m or m.group(1) != canon(slug):
        problems.append(f"{slug}: canonical mismatch: {m.group(1) if m else None}")
    m = re.search(r'<meta property="og:url" content="([^"]*)"', html)
    if not m or m.group(1) != canon(slug):
        problems.append(f"{slug}: og:url mismatch: {m.group(1) if m else None}")
    for bad in ('waterdamagetulsa', '918) 578', '918) 675', '918) 972', '918) 478',
                '(/services/', '(/resources/', '(/service-areas/', '[Embed Google Map',
                'Here are all 10 pages', 'All 10 pages done'):
        if bad in html and 'application/json' not in html:
            # only flag in visible content: strip scripts first
            vis = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
            if bad in vis:
                problems.append(f'{slug}: forbidden/leftover string in visible HTML: {bad!r}')
    # internal links resolve
    for href in set(lp.links):
        if href.startswith('/') and not href.startswith('//') and not href.startswith('/_next'):
            href = href.split('#')[0].split('?')[0]
            if href in ('', '/'):
                checked_links['home'] += 1
                continue
            st3, _ = fetch(href)
            checked_links[st3] += 1
            if st3 != 200:
                problems.append(f'{slug}: broken internal link {href} -> {st3}')
    # FAQ schema vs visible
    if p['faqs']:
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if not m:
            problems.append(f'{slug}: FAQ page missing JSON-LD')
        else:
            try:
                ld = json.loads(m.group(1))
                if isinstance(ld, list):
                    ld = ld[0]
                graph = ld.get('@graph', [])
                faq = next((g for g in graph if g.get('@type') == 'FAQPage'), None)
                if not faq:
                    problems.append(f'{slug}: FAQPage schema missing')
                elif len(faq.get('mainEntity', [])) != len(p['faqs']):
                    problems.append(f"{slug}: FAQ schema count {len(faq.get('mainEntity', []))} != visible {len(p['faqs'])}")
                else:
                    for qe, qv in zip(faq['mainEntity'], p['faqs']):
                        if qe.get('name') != unescape(qv['q']) or qe.get('acceptedAnswer', {}).get('text') != unescape(qv['a_text']):
                            problems.append(f"{slug}: FAQ schema Q/A mismatch: {qv['q'][:50]}")
                            break
            except Exception as e:
                problems.append(f'{slug}: JSON-LD parse error: {e}')

# sitemap + robots
st, sm = fetch('/sitemap.xml')
if st != 200:
    problems.append(f'sitemap.xml status {st}')
else:
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    if len(locs) != 53:
        problems.append(f'sitemap URL count {len(locs)} != 53')
    if '<image:image' in sm or 'image:' in sm:
        problems.append('sitemap contains image entries')
    expected = {canon(p['slug']) for p in pages}
    if set(locs) != expected:
        problems.append(f'sitemap URLs != canonical set (diff: {expected ^ set(locs)})')
st, rb = fetch('/robots.txt')
if st != 200 or 'Sitemap:' not in rb or 'Allow: /' not in rb:
    problems.append(f'robots.txt problem: status {st}')

def norm_path(p):
    if p == '/':
        return '/'
    return p.rstrip('/')

# orphans: every page reachable from home by BFS over internal links
seen = set()
queue = ['/']
while queue:
    cur = queue.pop()
    cur = norm_path(cur)
    if cur in seen:
        continue
    seen.add(cur)
    st, html = fetch(cur)
    if st != 200:
        continue
    lp = LinkParser()
    lp.feed(html)
    for href in lp.links:
        if href.startswith('/') and not href.startswith('//'):
            href = href.split('#')[0].split('?')[0]
            if href and href not in seen:
                queue.append(href)
orphans = sorted(p['slug'] for p in pages if norm_path(p['slug']) not in seen)
if orphans:
    problems.append(f'orphan pages (not reachable from home): {sorted(orphans)}')

print(f'pages checked: {len(pages)}')
print(f'internal link fetches by status: {dict(checked_links)}')
print(f'reachable from home: {len(seen)} / 53')
print(f'PROBLEMS: {len(problems)}')
for pr in problems:
    print('  -', pr)
OUT_MD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'FINDINGS-round1.md')
with open(OUT_MD, 'w') as f:
    f.write('# Testing Round 2 — structural verification\n\n' if 'round2' in OUT_MD else '# Testing Round 1 — structural verification\n\n')
    f.write(f'Pages checked: {len(pages)}\n')
    f.write(f'Internal link fetches by status: {dict(checked_links)}\n')
    f.write(f'Reachable from home: {len(seen)} / 53\n\n')
    f.write(f'## Problems ({len(problems)})\n\n')
    for pr in problems:
        f.write(f'- {pr}\n')
    if not problems:
        f.write('None — all structural checks passed.\n')
sys.exit(1 if problems else 0)
