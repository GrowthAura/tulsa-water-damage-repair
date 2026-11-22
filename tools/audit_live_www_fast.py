#!/usr/bin/env python3
"""Fast PARALLEL live www audit (Pass 1, ea8c25b).

Same checks as audit_live_www.py but fetches concurrently (20 workers)
because sequential fetching through the sandbox proxy is too slow.
Fetches all 53 www pages + every unique internal href + images + files,
then checks: canonical/og/H1/title/desc (vs doc), JSON-LD (types + FAQ
verbatim + URL values no-slash), named phrases, nested anchors, body
self-links, orphans (BFS), sitemap/robots/llms, favicon hashes, images
(alt + live 200 + EXIF/AI on local files + hero repeats), vercel.json
must NOT exist, slash variants 308 (resolved Location).
Usage: python3 tools/audit_live_www_fast.py [out.json]
Exit 1 if any PROBLEM.
"""
import hashlib, json, os, re, sys, urllib.request, urllib.error
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
WWW = 'https://www.tulsawaterdamagerepair.com'
DOMAIN = WWW
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
NAMED_PHRASES = ['Full details on how we handle this:', 'Full details on our page.',
  'Full details:', 'Full breakdown:', 'Full category and class breakdown:',
  'Full drying details:', 'Full drying process:', 'Full cost guide:',
  'Detailed guide:', 'Related services: and', 'Full checklist:']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (postpush-audit-fast)'})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=30) as r:
            raw = r.read()
            return url, r.status, dict(r.headers), raw.decode('utf-8', 'replace'), raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        return url, e.code, dict(e.headers), raw.decode('utf-8', 'replace'), raw
    except Exception as e:
        return url, 0, {}, str(e), b''


def fetch_many(urls, workers=20):
    out = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch_url, u): u for u in urls}
        for f in as_completed(futs):
            u, st, hdr, body, raw = f.result()
            out[u] = (st, hdr, body, raw)
    return out


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = []
        self.title = ''
        self._in_title = False
        self._in_h1 = False
        self.imgs = []
        self.a_depth = 0
        self.nested_a = 0
        self.in_content = False
        self._content_depth = 0
        self.meta_desc = None
        self.canonical = None
        self.og_url = None
        self.json_ld = []
        self._in_ld = False
        self._ld_buf = ''

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'div':
            if 'content-block' in d.get('class', ''):
                self._content_depth = 1
                self.in_content = True
            elif self.in_content:
                self._content_depth += 1
        if tag == 'a':
            if self.a_depth > 0:
                self.nested_a += 1
            self.a_depth += 1
            if 'href' in d:
                self.links.append((d['href'], self.in_content))
        if tag == 'h1':
            self._in_h1 = True
        if tag == 'title':
            self._in_title = True
        if tag == 'img':
            self.imgs.append((d.get('src', ''), d.get('alt', None)))
        if tag == 'meta' and d.get('name') == 'description':
            self.meta_desc = d.get('content', '')
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonical = d.get('href')
        if tag == 'meta' and d.get('property') == 'og:url':
            self.og_url = d.get('content')
        if tag == 'script' and d.get('type') == 'application/ld+json':
            self._in_ld = True
            self._ld_buf = ''

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_content:
            self._content_depth -= 1
            if self._content_depth <= 0:
                self.in_content = False
                self._content_depth = 0
        if tag == 'a' and self.a_depth > 0:
            self.a_depth -= 1
        if tag == 'h1':
            self._in_h1 = False
        if tag == 'title':
            self._in_title = False
        if tag == 'script' and self._in_ld:
            self._in_ld = False
            self.json_ld.append(self._ld_buf)

    def handle_data(self, data):
        if self._in_h1:
            self.h1.append(data.strip())
        if self._in_title:
            self.title += data.strip()
        if self._in_ld:
            self._ld_buf += data


def visible_text(html):
    t = re.sub(r'<script[\s\S]*?</script>', ' ', html)
    t = re.sub(r'<style[\s\S]*?</style>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return unescape(t)


def main():
    problems = []
    res = {'problems': problems, 'pages': {}, 'counts': {}}
    # 1) fetch all 53 pages in parallel
    page_urls = [DOMAIN + p['slug'] for p in pages]
    fetched = fetch_many(page_urls)
    link_status = Counter()
    all_imgs = defaultdict(list)
    faq_total = 0
    type_counts = Counter()
    title_lens, desc_lens = {}, {}
    phrase_hits = Counter()
    hrefs_to_check = {}  # href -> (slug, in_content)
    body_targets = {}   # slug -> Counter
    for p in pages:
        slug = p['slug']
        pr = {'problems': []}
        res['pages'][slug] = pr
        url = DOMAIN + slug
        st, hdr, html, _raw = fetched.get(url, (0, {}, '', b''))
        pr['status'] = st
        if st != 200:
            problems.append(f'{slug}: www status {st} (expected 200 direct)')
            pr['problems'].append(f'status {st}')
            body_targets[slug] = Counter()
            continue
        lp = LinkParser()
        lp.feed(html)
        canon = DOMAIN + slug
        if lp.canonical != canon:
            problems.append(f'{slug}: canonical {lp.canonical!r} != {canon!r}')
            pr['problems'].append('canonical')
        if lp.og_url != canon:
            problems.append(f'{slug}: og:url {lp.og_url!r} != {canon!r}')
            pr['problems'].append('og:url')
        h1s = [h for h in lp.h1 if h]
        pr['h1'] = h1s
        if len(h1s) != 1:
            problems.append(f'{slug}: H1 count {len(h1s)}')
            pr['problems'].append('h1-count')
        elif h1s[0] != re.sub(r'\s+', ' ', p['h1']).strip():
            problems.append(f"{slug}: H1 mismatch {h1s[0][:60]!r} vs doc {p['h1'][:60]!r}")
            pr['problems'].append('h1-text')
        title_lens[slug] = len(lp.title)
        desc_lens[slug] = len(lp.meta_desc or '')
        if lp.title != p['metaTitle']:
            problems.append(f'{slug}: <title> mismatch vs doc')
            pr['problems'].append('title')
        if (lp.meta_desc or '') != p['metaDescription']:
            problems.append(f'{slug}: meta description mismatch vs doc')
            pr['problems'].append('description')
        try:
            graphs = []
            for raw in lp.json_ld:
                ld = json.loads(raw)
                graphs.extend(ld if isinstance(ld, list) else [ld])
            nodes = []
            for g in graphs:
                nodes.extend(g.get('@graph', [g]) if isinstance(g, dict) else [])
            types = Counter(n.get('@type') for n in nodes)
            for t, c in types.items():
                type_counts[t] += c
            pr['ld_types'] = dict(types)
            for n in nodes:
                for k in ('url', '@id'):
                    v = n.get(k)
                    if isinstance(v, str) and v.startswith(DOMAIN):
                        if v != DOMAIN + '/' and v.endswith('/'):
                            problems.append(f"{slug}: JSON-LD {n.get('@type')} {k} has trailing slash: {v}")
                            pr['problems'].append('ld-trailing-slash')
            faq = next((n for n in nodes if n.get('@type') == 'FAQPage'), None)
            if p['faqs']:
                faq_total += len(p['faqs'])
                if not faq:
                    problems.append(f'{slug}: FAQPage schema missing')
                    pr['problems'].append('faqpage-missing')
                else:
                    ents = faq.get('mainEntity', [])
                    if len(ents) != len(p['faqs']):
                        problems.append(f"{slug}: FAQ schema {len(ents)} != visible {len(p['faqs'])}")
                        pr['problems'].append('faq-count')
                    else:
                        for qe, qv in zip(ents, p['faqs']):
                            if qe.get('name') != unescape(qv['q']) or qe.get('acceptedAnswer', {}).get('text') != unescape(qv['a_text']):
                                problems.append(f"{slug}: FAQ schema Q/A mismatch: {qv['q'][:50]}")
                                pr['problems'].append('faq-verbatim')
                                break
            else:
                if faq:
                    problems.append(f'{slug}: unexpected FAQPage schema')
                    pr['problems'].append('faqpage-unexpected')
            bc = next((n for n in nodes if n.get('@type') == 'BreadcrumbList'), None)
            if not bc:
                problems.append(f'{slug}: BreadcrumbList missing')
                pr['problems'].append('breadcrumb-missing')
            elif p['type'] != 'homepage':
                last = bc.get('itemListElement', [])[-1]
                if last.get('item') != canon:
                    problems.append(f"{slug}: breadcrumb last item {last.get('item')} != canonical")
                    pr['problems'].append('breadcrumb-item')
        except Exception as e:
            problems.append(f'{slug}: JSON-LD parse error: {e}')
            pr['problems'].append('ld-parse')
        vis = visible_text(html)
        for bad in ('waterdamagetulsa', '918) 578', '918) 675', '918) 972', '918) 478',
                    '(/services/', '(/resources/', '(/service-areas/', '[Embed Google Map',
                    'Here are all 10 pages', 'All 10 pages done'):
            if bad in vis:
                problems.append(f'{slug}: forbidden string in visible HTML: {bad!r}')
                pr['problems'].append('forbidden-string')
        if re.search(r'\bSee\s+and\b', vis):
            problems.append(f'{slug}: dangling "See and" in visible text')
            pr['problems'].append('see-and')
        for ph in NAMED_PHRASES:
            if ph in vis:
                phrase_hits[ph] += 1
                problems.append(f'{slug}: named dangling phrase present: {ph!r}')
                pr['problems'].append('named-phrase')
        if re.search(r'<a[^>]*>\s*and\s*</a>', html):
            problems.append(f'{slug}: bare <a>and</a> present')
            pr['problems'].append('bare-and')
        if '?v=' in html:
            problems.append(f'{slug}: ?v= query string present')
            pr['problems'].append('query-v')
        if lp.nested_a:
            problems.append(f'{slug}: nested anchors {lp.nested_a}')
            pr['problems'].append('nested-a')
        for src, alt in lp.imgs:
            all_imgs[src].append(slug)
            if alt is None or alt.strip() == '':
                problems.append(f'{slug}: img missing alt: {src}')
                pr['problems'].append('img-alt')
        bt = Counter()
        for href, in_content in set(lp.links):
            if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            if href.startswith('http'):
                continue
            if not href.startswith('/'):
                continue
            bare = href.split('#')[0].split('?')[0]
            if bare in ('', '/'):
                link_status['home'] += 1
                continue
            hrefs_to_check.setdefault(bare, []).append((slug, in_content))
            if in_content:
                bt[bare] += 1
        body_targets[slug] = bt
        pr['body_links'] = sum(bt.values())
        pr['body_link_dups'] = {t: c for t, c in bt.items() if c > 1}
        self_links = sum(1 for t, c in bt.items() if t == slug for _ in range(c))
        if self_links:
            problems.append(f'{slug}: body self-links {self_links}')
            pr['problems'].append('self-link')
    # 2) fetch every unique internal href in parallel
    uniq = sorted(hrefs_to_check)
    link_results = fetch_many([DOMAIN + u for u in uniq])
    for bare, users in hrefs_to_check.items():
        st, hdr, _, _ = link_results.get(DOMAIN + bare, (0, {}, '', b''))
        link_status[st] += 1
        if st != 200:
            for slug, _ in users:
                problems.append(f'{slug}: broken internal link {bare} -> {st}')
    # 3) slash variants (all 52) in parallel
    slash_urls = [DOMAIN + p['slug'] + '/' for p in pages if p['slug'] != '/']
    slash_results = fetch_many(slash_urls)
    n308 = 0
    for p in pages:
        if p['slug'] == '/':
            continue
        slug = p['slug']
        st, hdr, _, _ = slash_results.get(DOMAIN + slug + '/', (0, {}, '', b''))
        res['pages'][slug]['slash_variant'] = st
        res['pages'][slug]['slash_location'] = hdr.get('Location')
        if st != 308:
            problems.append(f'{slug}: slash variant status {st} (expected 308)')
            res['pages'][slug]['problems'].append('slash-variant')
        elif urljoin(DOMAIN + slug + '/', hdr.get('Location') or '') != DOMAIN + slug:
            problems.append(f"{slug}: slash variant Location {hdr.get('Location')!r} resolves != {DOMAIN + slug!r}")
            res['pages'][slug]['problems'].append('slash-location')
        else:
            n308 += 1
    res['counts']['slash_308_correct'] = n308
    # 4) sitemap / robots / llms / key (live)
    st, _, sm, _ = fetch_url(WWW + '/sitemap.xml')[1:]
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    lastmods = re.findall(r'<lastmod>([^<]+)</lastmod>', sm)
    res['counts']['sitemap_locs'] = len(locs)
    res['counts']['sitemap_lastmods'] = dict(Counter(lastmods))
    if st != 200 or len(locs) != 53:
        problems.append(f'sitemap: status {st}, locs {len(locs)} (expected 53)')
    if set(locs) != {DOMAIN + p['slug'] for p in pages}:
        problems.append(f'sitemap locs != canonical set: {set(locs) ^ {DOMAIN + p["slug"] for p in pages}}')
    if any(not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm) for lm in lastmods):
        problems.append('sitemap: non-date-only lastmod found')
    if '<image:image' in sm:
        problems.append('sitemap contains image entries')
    st, _, rb, _ = fetch_url(WWW + '/robots.txt')[1:]
    ua_groups = len(re.findall(r'^User-agent:', rb, re.M))
    res['counts']['robots_user_agents'] = ua_groups
    if st != 200 or ua_groups != 23 or 'Sitemap:' not in rb:
        problems.append(f'robots.txt: status {st}, User-agent lines {ua_groups} (expected 23)')
    st, _, lm, _ = fetch_url(WWW + '/llms.txt')[1:]
    llms_urls = re.findall(r'https://www\.tulsawaterdamagerepair\.com[^\s\)\]]*', lm)
    res['counts']['llms_links'] = len(llms_urls)
    res['counts']['llms_trailing_slash'] = [u for u in llms_urls if u != DOMAIN + '/' and u.endswith('/')]
    if set(llms_urls) != {DOMAIN + p['slug'] for p in pages}:
        problems.append(f'llms.txt links != canonical set: {set(llms_urls) ^ {DOMAIN + p["slug"] for p in pages}}')
    if res['counts']['llms_trailing_slash']:
        problems.append(f"llms.txt trailing-slash links: {res['counts']['llms_trailing_slash']}")
    if '(918) 395-9320' not in lm or '400 S 129th E Ave' not in lm:
        problems.append('llms.txt missing NAP')
    st, _, _, _ = fetch_url(WWW + '/b52262ce2b2f10b691644dccabf66495.txt')[1:]
    res['counts']['indexnow_key_status'] = st
    if st != 200:
        problems.append(f'IndexNow key file status {st} (expected 200)')
    # 5) orphans via BFS from home (using already-fetched pages + link map)
    seen = set()
    queue = ['/']
    page_hrefs = {}
    for p in pages:
        url = DOMAIN + p['slug']
        st2, _, html2, _ = fetched.get(url, (0, {}, '', b''))
        if st2 != 200:
            continue
        lp2 = LinkParser()
        lp2.feed(html2)
        page_hrefs[p['slug']] = [h.split('#')[0].split('?')[0] for h, _ in lp2.links
                                 if h.startswith('/') and not h.startswith('//')]
    while queue:
        cur = queue.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for h in page_hrefs.get(cur, []):
            if h and h not in seen:
                queue.append(h)
    orphans = sorted(p['slug'] for p in pages if p['slug'] not in seen)
    res['counts']['reachable_from_home'] = len(seen & {p['slug'] for p in pages})
    if orphans:
        problems.append(f'orphan pages: {orphans}')
    # 6) vercel.json must NOT exist
    vj = os.path.join(BASE, 'vercel.json')
    res['counts']['vercel_json_exists'] = os.path.exists(vj)
    if os.path.exists(vj):
        problems.append('vercel.json EXISTS in repo (user forbade all redirects; deleted in ea8c25b)')
    res['counts']['vercel_redirects'] = 0
    # 7) favicon hashes (live www vs local build)
    fav_files = ['favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png',
                 'favicon-48x48.png', 'favicon-192x192.png', 'favicon-512x512.png',
                 'favicon-512x512-maskable.png', 'apple-touch-icon.png', 'favicon-master.png']
    fav_results = fetch_many([WWW + '/' + f for f in fav_files])
    fav_match = {}
    for f in fav_files:
        stf, _, _, raw_live = fav_results.get(WWW + '/' + f, (0, {}, '', b''))
        local = os.path.join(BASE, 'out', f)
        if not os.path.exists(local):
            fav_match[f] = 'local-missing'
            continue
        h_local = hashlib.md5(open(local, 'rb').read()).hexdigest()
        h_live = hashlib.md5(raw_live).hexdigest() if raw_live else ''
        fav_match[f] = 'MATCH' if (stf == 200 and h_live == h_local) else f'MISMATCH live={stf} md5={h_live[:8]} local={h_local[:8]}'
        if fav_match[f] != 'MATCH':
            problems.append(f'favicon {f}: {fav_match[f]}')
    res['counts']['favicon_match'] = fav_match
    # 8) images: EXIF/AI/hero repeats on identical local files + live 200 for srcs
    from PIL import Image
    img_problems = []
    hero_use = defaultdict(list)
    images = json.load(open(os.path.join(BASE, 'content', 'images.json')))
    for slug, slots in images.items():
        for kind in ('hero', 'body'):
            e = (slots or {}).get(kind)
            if not e:
                continue
            f = os.path.join(BASE, 'public', e['file'].lstrip('/'))
            if kind == 'hero':
                hero_use[e['file']].append(slug)
            if not os.path.exists(f):
                img_problems.append(f'{slug} {kind}: missing file {e["file"]}')
                continue
            if any(x in e['file'].lower() for x in ('ai-', '-ai', 'midjourney', 'dall', 'gpt', 'generated')):
                img_problems.append(f'{slug} {kind}: AI string in filename {e["file"]}')
            if any(x in (e.get('alt') or '').lower() for x in ('ai-generated', 'midjourney', 'dall-e', 'chatgpt')):
                img_problems.append(f'{slug} {kind}: AI string in alt')
            try:
                im = Image.open(f)
                exif = im.getexif()
                if exif:
                    img_problems.append(f'{slug} {kind}: EXIF present ({len(exif)} tags) {e["file"]}')
            except Exception as ex:
                img_problems.append(f'{slug} {kind}: PIL error {ex}')
    res['counts']['hero_files_reused'] = {f: s for f, s in hero_use.items() if len(s) > 1}
    res['counts']['distinct_hero_files'] = len(hero_use)
    res['counts']['img_srcs_distinct'] = len(all_imgs)
    res['counts']['img_tags_total'] = sum(len(v) for v in all_imgs.values())
    problems.extend(img_problems)
    img_srcs = [s for s in all_imgs if s.startswith('/')]
    img_results = fetch_many([WWW + s.split('#')[0].split('?')[0] for s in img_srcs])
    asset_status = Counter()
    img_bad = []
    for src in img_srcs:
        stf, _, _, _ = img_results.get(WWW + src.split('#')[0].split('?')[0], (0, {}, '', b''))
        asset_status[stf] += 1
        if stf != 200:
            img_bad.append(f'{src} -> {stf}')
    if img_bad:
        problems.append(f'img srcs not 200 on www: {img_bad[:10]}')
    res['counts']['img_fetch_status'] = dict(asset_status)
    res['counts']['faq_total'] = faq_total
    res['counts']['ld_types'] = dict(type_counts)
    res['counts']['link_status'] = dict(link_status)
    res['counts']['title_len_over60'] = sum(1 for v in title_lens.values() if v > 60)
    res['counts']['desc_len_over160'] = sum(1 for v in desc_lens.values() if v > 160)
    res['counts']['title_lens'] = title_lens
    res['counts']['desc_lens'] = desc_lens
    res['counts']['phrase_hits'] = dict(phrase_hits)
    res['counts']['unique_internal_hrefs'] = len(uniq)
    for extra in ('/privacy-policy', '/terms-of-service', '/privacy-policy/', '/terms-of-service/'):
        stx, _, _, _ = fetch_url(WWW + extra)[1:]
        if stx == 200:
            problems.append(f'{extra} serves 200 on www (should not exist)')
    res['counts']['problems'] = len(problems)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'qa-postpush-live', 'audit_www_fast.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(res, open(out_path, 'w'), indent=1)
    print(f"pages: {len(pages)}  www-200: {sum(1 for p in res['pages'].values() if p.get('status') == 200)}/53")
    print(f"unique internal hrefs fetched: {len(uniq)}  link fetches by status: {dict(link_status)}")
    print(f"slash 308 correct: {n308}/52")
    print(f"FAQ total: {faq_total}  LD types: {dict(type_counts)}")
    print(f"sitemap locs: {len(locs)}  lastmods: {dict(Counter(lastmods))}  robots UA: {ua_groups}  llms links: {len(llms_urls)}")
    print(f"titles >60ch: {res['counts']['title_len_over60']}  descriptions >160ch: {res['counts']['desc_len_over160']}")
    print(f"reachable from home: {res['counts']['reachable_from_home']}/53  vercel.json exists: {res['counts']['vercel_json_exists']}")
    print(f"distinct hero files: {len(hero_use)}  hero reused: {len(res['counts']['hero_files_reused'])}")
    print(f"img tags: {res['counts']['img_tags_total']} distinct srcs: {len(all_imgs)} img fetch: {dict(asset_status)}")
    print(f"favicon: {fav_match}")
    print(f"phrase hits: {dict(phrase_hits)}")
    print(f"PROBLEMS: {len(problems)}")
    for pr in problems:
        print('  -', pr)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
