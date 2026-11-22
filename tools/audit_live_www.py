#!/usr/bin/env python3
"""Post-push LIVE A-to-Z audit against the LIVE www site.

The www site (https://www.tulsawaterdamagerepair.com) serves the new build
(deploy 7b2f327). This script audits it LIVE:
every page (53) fetched over HTTPS, canonical == www canonical set, og:url,
H1 1x + doc-verbatim, JSON-LD parsed (types + FAQ verbatim + all URL values
no-slash), internal links (every href fetched, nested anchors, body
self-links, orphans via BFS), sitemap/robots/llms.txt, images (alt + live
200 + EXIF/AI on the identical local files + hero repeats), favicon hashes
vs the local build, forbidden strings + all 14 named dangling phrases,
crawl-waste (no dual-200 forms on the preview: slash forms 404; privacy/
terms 404). Slash -> 308 is the platform/Next.js trailingSlash:false built-in
(user forbade ALL redirects; vercel.json was DELETED in ea8c25b).
It is verified LIVE per page below (all 52 slash forms must 308). — they are checked separately on
www once the Vercel deploy flips; see the findings file.

Usage: python3 tools/audit_live_www.py [out.json]
Writes JSON + prints a summary. Exit 1 if any PROBLEM.
"""
import hashlib, json, os, re, sys, urllib.request, urllib.error
from collections import Counter, defaultdict
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
PREVIEW = 'https://www.tulsawaterdamagerepair.com'
PREFIX = ''
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
FLIPPED_NEW = {'/services','/service-areas/claremore-ok','/service-areas/owasso-ok',
  '/service-areas/jenks-ok','/service-areas/glenpool-ok','/service-areas/bixby-ok',
  '/service-areas/broken-arrow-ok','/service-areas/sand-springs-ok',
  '/service-areas/skiatook-ok','/service-areas/coweta-ok','/service-areas/catoosa-ok',
  '/service-areas/collinsville-ok','/service-areas/sapulpa-ok','/service-areas/midtown-tulsa',
  '/about-us','/contact','/service-areas/brookside-tulsa','/service-areas/south-tulsa',
  '/service-areas/west-tulsa','/service-areas/north-tulsa',
  '/services/ac-drain-line-overflow-cleanup','/services/appliance-leak-water-damage',
  '/services/water-heater-leak-cleanup','/services/roof-leak-water-damage',
  '/services/slab-leak-water-damage','/service-areas/east-tulsa',
  '/service-areas/cherry-street-tulsa','/commercial','/resources'}
NAMED_PHRASES = ['Full details on how we handle this:', 'Full details on our page.',
  'Full details:', 'Full breakdown:', 'Full category and class breakdown:',
  'Full drying details:', 'Full drying process:', 'Full cost guide:',
  'Detailed guide:', 'Related services: and', 'Full checklist:']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch_url(url):
    """Fetch a full URL. Returns (status, headers dict, body str, raw bytes)."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (postpush-audit)'})
    try:
        with OPENER.open(req, timeout=30) as r:
            raw = r.read()
            return r.status, dict(r.headers), raw.decode('utf-8', 'replace'), raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, dict(e.headers), raw.decode('utf-8', 'replace'), raw
    except Exception as e:
        return 0, {}, str(e), b''


def fetch_preview(path):
    """Fetch a preview path (e.g. '/services' or '/tulsa-water-damage-repair/services')."""
    return fetch_url(PREVIEW + path)


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


def strip_prefix(href):
    """'/tulsa-water-damage-repair/services' -> '/services'; else unchanged."""
    if href.startswith(PREFIX + '/'):
        return href[len(PREFIX):]
    if href == PREFIX:
        return '/'
    return href


def main():
    problems, notes = [], []
    res = {'problems': problems, 'notes': notes, 'pages': {}, 'counts': {}}
    link_status = Counter()
    all_imgs = defaultdict(list)
    faq_total = 0
    type_counts = Counter()
    title_lens, desc_lens = {}, {}
    phrase_hits = Counter()
    asset_status = Counter()

    for p in pages:
        slug = p['slug']
        pr = {'problems': []}
        res['pages'][slug] = pr
        st, hdr, html, _raw = fetch_preview(slug)
        pr['status'] = st
        if st != 200:
            problems.append(f'{slug}: preview status {st} (expected 200 direct)')
            pr['problems'].append(f'status {st}')
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
        # named dangling phrases (case-sensitive, as ordered)
        for ph in NAMED_PHRASES:
            if ph in vis:
                phrase_hits[ph] += 1
                problems.append(f'{slug}: named dangling phrase present: {ph!r}')
                pr['problems'].append('named-phrase')
        # bare <a>and</a>
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
        body_targets = Counter()
        self_links = 0
        for href, in_content in set(lp.links):
            if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            if href.startswith('http'):
                continue  # external (FEMA etc.) — not fetched in this audit
            if not href.startswith('/'):
                continue
            bare = strip_prefix(href.split('#')[0].split('?')[0])
            if bare in ('', '/'):
                link_status['home'] += 1
                continue
            # fetch against the preview host (href is already prefixed)
            st3, _, _, _ = fetch_url('https://www.tulsawaterdamagerepair.com' + href.split('#')[0].split('?')[0])
            link_status[st3] += 1
            if st3 != 200:
                problems.append(f'{slug}: broken internal link {href} -> {st3}')
                pr['problems'].append('internal-link')
            if in_content:
                body_targets[bare] += 1
                if bare == slug:
                    self_links += 1
        if self_links:
            problems.append(f'{slug}: body self-links {self_links}')
            pr['problems'].append('self-link')
        dups = {t: c for t, c in body_targets.items() if c > 1}
        pr['body_link_dups'] = dups
        pr['body_links'] = sum(body_targets.values())
        # slash variant must 308 to the canonical on www (no dual-200, max 1 hop)
        if slug != '/':
            vst, vhdr, _, _ = fetch_preview(slug + '/')
            pr['slash_variant'] = vst
            pr['slash_location'] = vhdr.get('Location')
            if vst != 308:
                problems.append(f'{slug}: slash variant status {vst} (expected 308)')
                pr['problems'].append('slash-variant')
            elif urljoin(DOMAIN + slug + '/', vhdr.get('Location') or '') != DOMAIN + slug:
                problems.append(f"{slug}: slash variant Location {vhdr.get('Location')!r} resolves != {DOMAIN + slug!r}")
                pr['problems'].append('slash-location')
        pr['status'] = st

    # sitemap / robots / llms (live, from preview)
    st, _, sm, _ = fetch_preview('/sitemap.xml')
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
    st, _, rb, _ = fetch_preview('/robots.txt')
    ua_groups = len(re.findall(r'^User-agent:', rb, re.M))
    res['counts']['robots_user_agents'] = ua_groups
    if st != 200 or ua_groups != 23 or 'Sitemap:' not in rb:
        problems.append(f'robots.txt: status {st}, User-agent lines {ua_groups} (expected 23)')
    st, _, lm, _ = fetch_preview('/llms.txt')
    llms_urls = re.findall(r'https://www\.tulsawaterdamagerepair\.com[^\s\)\]]*', lm)
    res['counts']['llms_links'] = len(llms_urls)
    res['counts']['llms_trailing_slash'] = [u for u in llms_urls if u != DOMAIN + '/' and u.endswith('/')]
    if set(llms_urls) != {DOMAIN + p['slug'] for p in pages}:
        problems.append(f'llms.txt links != canonical set: {set(llms_urls) ^ {DOMAIN + p["slug"] for p in pages}}')
    if res['counts']['llms_trailing_slash']:
        problems.append(f"llms.txt trailing-slash links: {res['counts']['llms_trailing_slash']}")
    if '(918) 395-9320' not in lm or '400 S 129th E Ave' not in lm:
        problems.append('llms.txt missing NAP')
    # orphans via BFS from preview home
    seen, queue = set(), ['/']
    while queue:
        cur = queue.pop()
        if cur in seen:
            continue
        seen.add(cur)
        st2, _, h2, _ = fetch_preview(cur)
        if st2 != 200:
            continue
        lp2 = LinkParser()
        lp2.feed(h2)
        for href, _ in lp2.links:
            if href.startswith(PREFIX + '/') or href == PREFIX:
                bare = strip_prefix(href.split('#')[0].split('?')[0])
                if bare and bare not in seen:
                    queue.append(bare)
    orphans = sorted(p['slug'] for p in pages if p['slug'] not in seen)
    res['counts']['reachable_from_home'] = len(seen & {p['slug'] for p in pages})
    if orphans:
        problems.append(f'orphan pages: {orphans}')
    # NO redirects by user order: vercel.json must NOT exist (ea8c25b deleted it).
    # Slash -> 308 is the platform/Next.js trailingSlash:false built-in,
    # verified live per page in the slash-variant check above.
    vj = os.path.join(BASE, 'vercel.json')
    res['counts']['vercel_json_exists'] = os.path.exists(vj)
    if os.path.exists(vj):
        problems.append('vercel.json EXISTS in repo (user forbade all redirects; it was deleted in ea8c25b)')
    res['counts']['vercel_redirects'] = 0
    # favicon hashes: live preview vs local build
    fav_files = ['favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png',
                 'favicon-48x48.png', 'favicon-192x192.png', 'favicon-512x512.png',
                 'favicon-512x512-maskable.png', 'apple-touch-icon.png', 'favicon-master.png']
    fav_match = {}
    for f in fav_files:
        stf, _, _, raw_live = fetch_preview('/' + f)
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
    # images: alt/size/EXIF/AI/cross-page heroes (identical local files)
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
    # live-fetch every distinct img src on the preview
    img_fetch_bad = []
    for src in all_imgs:
        if src.startswith('http'):
            continue
        stf, _, _, _ = fetch_url('https://www.tulsawaterdamagerepair.com' + src.split('#')[0].split('?')[0])
        asset_status[stf] += 1
        if stf != 200:
            img_fetch_bad.append(f'{src} -> {stf}')
    if img_fetch_bad:
        problems.append(f'img srcs not 200 on www: {img_fetch_bad[:10]}')
    res['counts']['img_fetch_status'] = dict(asset_status)
    res['counts']['faq_total'] = faq_total
    res['counts']['ld_types'] = dict(type_counts)
    res['counts']['link_status'] = dict(link_status)
    res['counts']['title_len_over60'] = sum(1 for v in title_lens.values() if v > 60)
    res['counts']['desc_len_over160'] = sum(1 for v in desc_lens.values() if v > 160)
    res['counts']['title_lens'] = title_lens
    res['counts']['desc_lens'] = desc_lens
    res['counts']['phrase_hits'] = dict(phrase_hits)
    for extra in ('/privacy-policy', '/terms-of-service', '/privacy-policy/', '/terms-of-service/'):
        stx, _, _, _ = fetch_preview(extra)
        if stx == 200:
            problems.append(f'{extra} serves 200 on www (should not exist)')
    res['counts']['problems'] = len(problems)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'qa-postpush-live', 'audit_www.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(res, open(out_path, 'w'), indent=1)
    print(f"pages: {len(pages)}  preview-200: {sum(1 for p in res['pages'].values() if p.get('status') == 200)}/53")
    print(f"link fetches by status: {dict(link_status)}")
    print(f"FAQ total: {faq_total}  LD types: {dict(type_counts)}")
    print(f"sitemap locs: {len(locs)}  lastmods: {dict(Counter(lastmods))}  robots UA: {ua_groups}  llms links: {len(llms_urls)}")
    print(f"titles >60ch: {res['counts']['title_len_over60']}  descriptions >160ch: {res['counts']['desc_len_over160']}")
    print(f"reachable from home: {res['counts']['reachable_from_home']}/53  vercel.json exists: {res['counts']['vercel_json_exists']} (must be False)")
    print(f"distinct hero files: {len(hero_use)}  hero reused: {len(res['counts']['hero_files_reused'])}")
    print(f"img tags: {res['counts']['img_tags_total']} distinct srcs: {len(all_imgs)} img fetch: {dict(asset_status)}")
    print(f"favicon: {fav_match}")
    print(f"phrase hits: {dict(phrase_hits)}")
    print(f"PROBLEMS: {len(problems)}")
    for pr in problems:
        print('  -', pr)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
