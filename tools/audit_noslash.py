#!/usr/bin/env python3
"""No-slash round A-to-Z audit (Pass 1 / Pass 2).

Serves site/out/ on 127.0.0.1:8317 with a Vercel-faithful URL model:
  - '/' -> out/index.html (200)
  - '/path' (no slash) -> out/<path>.html (200) if it exists
  - '/path/' (slash, not homepage) -> 308 to '/path' (per vercel.json redirects)
  - static files (/sitemap.xml, /robots.txt, /_next/..., /images/...) served as-is
Fetches are made with redirects DISABLED so a 308 surfaces as 308, not a
followed 200. Checks, per page (53): status 200 direct, canonical == served
URL == sitemap loc, og:url, H1 1x + doc-verbatim, title/description (REPORT
lengths only — U5 wording is the user's call), JSON-LD parsed (types +
counts + FAQ verbatim + all URL values no-slash), forbidden strings,
internal links (fetch every href, nested anchors, body self-links,
orphans via BFS), sitemap/robots/llms.txt, images (alt/size/EXIF/AI strings/
cross-page hero repeats), crawl-waste (no dual-200 forms, no chains, no 404s).
Usage: python3 tools/audit_noslash.py [out.json]
Writes JSON + prints a summary. Exit 1 if any PROBLEM.
"""
import json, os, re, sys, threading, urllib.request, urllib.error
from collections import Counter, defaultdict
from html import unescape
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, urljoin, unquote

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'out')
PORT = 8317
DOMAIN = 'https://www.tulsawaterdamagerepair.com'
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
PAGE_BY_SLUG = {p['slug']: p for p in pages}
FLIPPED_OLD = ['/services/','/service-areas/claremore-ok/','/service-areas/owasso-ok/',
  '/service-areas/jenks-ok/','/service-areas/glenpool-ok/','/service-areas/bixby-ok/',
  '/service-areas/broken-arrow-ok/','/service-areas/sand-springs-ok/',
  '/service-areas/skiatook-ok/','/service-areas/coweta-ok/','/service-areas/catoosa-ok/',
  '/service-areas/collinsville-ok/','/service-areas/sapulpa-ok/','/service-areas/midtown-tulsa/',
  '/about-us/','/contact/','/service-areas/brookside-tulsa/','/service-areas/south-tulsa/',
  '/service-areas/west-tulsa/','/service-areas/north-tulsa/',
  '/services/ac-drain-line-overflow-cleanup/','/services/appliance-leak-water-damage/',
  '/services/water-heater-leak-cleanup/','/services/roof-leak-water-damage/',
  '/services/slab-leak-water-damage/','/service-areas/east-tulsa/',
  '/service-areas/cherry-street-tulsa/','/commercial/','/resources/']
FLIPPED_NEW = {o[:-1] for o in FLIPPED_OLD}
REDIRECTS = {}
try:
    v = json.load(open(os.path.join(BASE, 'vercel.json')))
    for r in v.get('redirects', []):
        REDIRECTS[r['source']] = r['destination']
except FileNotFoundError:
    pass

MIME = {'.html': 'text/html', '.xml': 'application/xml', '.txt': 'text/plain',
        '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json',
        '.png': 'image/png', '.webp': 'image/webp', '.ico': 'image/x-icon',
        '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json'}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        # URL-decode: browsers request chunk paths percent-encoded
        # (/_next/.../%5B%5B...slug%5D%5D/...) while the file on disk uses
        # literal brackets. Real static hosts decode before lookup.
        path = unquote(urlparse(self.path).path)
        if path != '/' and path.endswith('/'):
            dest = REDIRECTS.get(path)
            if dest:
                self.send_response(308)
                self.send_header('Location', dest)
                self.end_headers()
                return
            self.send_error(404)
            return
        if path == '/':
            f = os.path.join(OUT, 'index.html')
        else:
            rel = path.lstrip('/')
            cand = os.path.join(OUT, rel + '.html')
            if os.path.exists(cand):
                f = cand
            else:
                f = os.path.join(OUT, rel)
        if not os.path.isfile(f):
            self.send_error(404)
            return
        ext = os.path.splitext(f)[1]
        data = open(f, 'rb').read()
        self.send_response(200)
        self.send_header('Content-Type', MIME.get(ext, 'application/octet-stream'))
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(path):
    try:
        with OPENER.open('http://127.0.0.1:%d' % PORT + path, timeout=20) as r:
            return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace')
    except Exception as e:
        return 0, {}, str(e)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []          # (href, in_content, in_a_depth)
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
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    problems, notes = [], []
    res = {'problems': problems, 'notes': notes, 'pages': {}, 'counts': {}}
    link_status = Counter()
    all_imgs = defaultdict(list)  # src -> [slugs]
    faq_total = 0
    type_counts = Counter()
    title_lens, desc_lens = {}, {}

    for p in pages:
        slug = p['slug']
        pr = {'problems': []}
        res['pages'][slug] = pr
        st, hdr, html = fetch(slug)
        pr['status'] = st
        if st != 200:
            problems.append(f'{slug}: canonical status {st} (expected 200 direct)')
            pr['problems'].append(f'status {st}')
            continue
        lp = LinkParser()
        lp.feed(html)
        # canonical / og:url / sitemap
        canon = DOMAIN + slug
        if lp.canonical != canon:
            problems.append(f'{slug}: canonical {lp.canonical!r} != {canon!r}')
            pr['problems'].append('canonical')
        if lp.og_url != canon:
            problems.append(f'{slug}: og:url {lp.og_url!r} != {canon!r}')
            pr['problems'].append('og:url')
        # H1
        h1s = [h for h in lp.h1 if h]
        pr['h1'] = h1s
        if len(h1s) != 1:
            problems.append(f'{slug}: H1 count {len(h1s)}')
            pr['problems'].append('h1-count')
        elif h1s[0] != re.sub(r'\s+', ' ', p['h1']).strip():
            problems.append(f"{slug}: H1 mismatch {h1s[0][:60]!r} vs doc {p['h1'][:60]!r}")
            pr['problems'].append('h1-text')
        # title / description: report only
        title_lens[slug] = len(lp.title)
        desc_lens[slug] = len(lp.meta_desc or '')
        if lp.title != p['metaTitle']:
            problems.append(f'{slug}: <title> mismatch vs doc')
            pr['problems'].append('title')
        if (lp.meta_desc or '') != p['metaDescription']:
            problems.append(f'{slug}: meta description mismatch vs doc')
            pr['problems'].append('description')
        # JSON-LD
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
            # BreadcrumbList last item == canonical
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
        # forbidden strings in visible HTML
        vis = visible_text(html)
        for bad in ('waterdamagetulsa', '918) 578', '918) 675', '918) 972', '918) 478',
                    '(/services/', '(/resources/', '(/service-areas/', '[Embed Google Map',
                    'Here are all 10 pages', 'All 10 pages done'):
            if bad in vis:
                problems.append(f'{slug}: forbidden string in visible HTML: {bad!r}')
                pr['problems'].append('forbidden-string')
        # dangling See and / See
        if re.search(r'\bSee\s+and\b', vis):
            problems.append(f'{slug}: dangling "See and" in visible text')
            pr['problems'].append('see-and')
        # nested anchors
        if lp.nested_a:
            problems.append(f'{slug}: nested anchors {lp.nested_a}')
            pr['problems'].append('nested-a')
        # images
        for src, alt in lp.imgs:
            all_imgs[src].append(slug)
            if alt is None or alt.strip() == '':
                problems.append(f'{slug}: img missing alt: {src}')
                pr['problems'].append('img-alt')
        # internal links
        body_targets = Counter()
        self_links = 0
        for href, in_content in set(lp.links):
            if not href.startswith('/') or href.startswith('//'):
                continue
            bare = href.split('#')[0].split('?')[0]
            if bare in ('', '/'):
                link_status['home'] += 1
                continue
            if bare.startswith('/_next') or bare.startswith('/images/') or '.' in bare.rsplit('/', 1)[-1]:
                st3, _, _ = fetch(bare)
                link_status[st3] += 1
                if st3 != 200:
                    problems.append(f'{slug}: broken asset link {bare} -> {st3}')
                    pr['problems'].append('asset-link')
                continue
            st3, hdr3, _ = fetch(bare)
            link_status[st3] += 1
            if st3 != 200:
                problems.append(f'{slug}: broken internal link {bare} -> {st3}')
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
        # slash variant must 308 to canonical (no dual 200) — flipped pages only
        if slug in FLIPPED_NEW:
            vst, vhdr, _ = fetch(slug + '/')
            pr['slash_variant'] = vst
            if vst != 308:
                problems.append(f'{slug}: slash variant status {vst} (expected 308)')
                pr['problems'].append('slash-variant')
            elif vhdr.get('Location') != slug:
                problems.append(f"{slug}: slash variant Location {vhdr.get('Location')!r} != {slug!r}")
                pr['problems'].append('slash-location')
            # no redirect chain: canonical must be 200 direct (already checked)
        pr['status'] = st

    # sitemap / robots / llms
    st, _, sm = fetch('/sitemap.xml')
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    lastmods = re.findall(r'<lastmod>([^<]+)</lastmod>', sm)
    res['counts']['sitemap_locs'] = len(locs)
    res['counts']['sitemap_lastmods'] = Counter(lastmods)
    if st != 200 or len(locs) != 53:
        problems.append(f'sitemap: status {st}, locs {len(locs)} (expected 53)')
    if set(locs) != {DOMAIN + p['slug'] for p in pages}:
        problems.append(f'sitemap locs != canonical set: {set(locs) ^ {DOMAIN + p["slug"] for p in pages}}')
    if any(not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm) for lm in lastmods):
        problems.append('sitemap: non-date-only lastmod found')
    if '<image:image' in sm:
        problems.append('sitemap contains image entries')
    st, _, rb = fetch('/robots.txt')
    ua_groups = len(re.findall(r'^User-agent:', rb, re.M))
    res['counts']['robots_user_agents'] = ua_groups
    if st != 200 or ua_groups != 23 or 'Sitemap:' not in rb:
        problems.append(f'robots.txt: status {st}, User-agent lines {ua_groups} (expected 23 = wildcard + 22 AI groups)')
    llms = open(os.path.join(BASE, 'public', 'llms.txt'), encoding='utf-8').read()
    llms_urls = re.findall(r'https://www\.tulsawaterdamagerepair\.com[^\s\)\]]*', llms)
    res['counts']['llms_links'] = len(llms_urls)
    res['counts']['llms_trailing_slash'] = [u for u in llms_urls if u != DOMAIN + '/' and u.endswith('/')]
    if set(llms_urls) != {DOMAIN + p['slug'] for p in pages}:
        problems.append(f'llms.txt links != canonical set: {set(llms_urls) ^ {DOMAIN + p["slug"] for p in pages}}')
    if res['counts']['llms_trailing_slash']:
        problems.append(f"llms.txt trailing-slash links: {res['counts']['llms_trailing_slash']}")
    if '(918) 395-9320' not in llms or '400 S 129th E Ave' not in llms:
        problems.append('llms.txt missing NAP')
    # orphans via BFS from home
    seen, queue = set(), ['/']
    while queue:
        cur = queue.pop()
        if cur in seen:
            continue
        seen.add(cur)
        st2, _, h2 = fetch(cur)
        if st2 != 200:
            continue
        lp2 = LinkParser()
        lp2.feed(h2)
        for href, _ in lp2.links:
            if href.startswith('/') and not href.startswith('//'):
                bare = href.split('#')[0].split('?')[0]
                if bare and bare not in seen:
                    queue.append(bare)
    orphans = sorted(p['slug'] for p in pages if p['slug'] not in seen)
    res['counts']['reachable_from_home'] = len(seen & {p['slug'] for p in pages})
    if orphans:
        problems.append(f'orphan pages: {orphans}')
    # vercel redirects coverage
    missing = [s for s in FLIPPED_OLD if s not in REDIRECTS]
    res['counts']['vercel_redirects'] = len(REDIRECTS)
    if missing:
        problems.append(f'vercel.json missing redirects for: {missing}')
    if len(REDIRECTS) != 29:
        problems.append(f'vercel.json redirects {len(REDIRECTS)} != 29')
    # images: alt/size/EXIF/AI/cross-page heroes
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
    res['counts']['faq_total'] = faq_total
    res['counts']['ld_types'] = dict(type_counts)
    res['counts']['link_status'] = dict(link_status)
    res['counts']['title_len_over60'] = sum(1 for v in title_lens.values() if v > 60)
    res['counts']['desc_len_over160'] = sum(1 for v in desc_lens.values() if v > 160)
    res['counts']['title_lens'] = title_lens
    res['counts']['desc_lens'] = desc_lens
    # privacy/terms must not exist / not be in sitemap
    for extra in ('/privacy-policy', '/terms-of-service', '/privacy-policy/', '/terms-of-service/'):
        stx, _, _ = fetch(extra)
        if stx == 200:
            problems.append(f'{extra} serves 200 (should not exist / must be noindex + excluded)')
    res['counts']['problems'] = len(problems)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'qa-noslash-round', 'audit.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(res, open(out_path, 'w'), indent=1)
    server.shutdown()
    print(f"pages: {len(pages)}  canonical-200: {sum(1 for p in res['pages'].values() if p.get('status') == 200)}/53")
    print(f"link fetches by status: {dict(link_status)}")
    print(f"FAQ total: {faq_total}  LD types: {dict(type_counts)}")
    print(f"sitemap locs: {len(locs)}  robots UA groups: {ua_groups}  llms links: {len(llms_urls)}")
    print(f"titles >60ch: {res['counts']['title_len_over60']}  descriptions >160ch: {res['counts']['desc_len_over160']}")
    print(f"reachable from home: {res['counts']['reachable_from_home']}/53  vercel redirects: {len(REDIRECTS)}")
    print(f"distinct hero files: {len(hero_use)}  hero files reused across pages: {len(res['counts']['hero_files_reused'])}")
    print(f"PROBLEMS: {len(problems)}")
    for pr in problems:
        print('  -', pr)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
