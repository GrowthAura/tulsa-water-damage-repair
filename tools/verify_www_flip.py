#!/usr/bin/env python3
"""Post-push WWW verification (after the Vercel flip).

Fetches every canonical URL from the LIVE www sitemap and checks:
- status 200 direct (no redirect hop)
- canonical == served URL, og:url == served URL
- H1 count 1 (static) + title/description present
- every non-homepage slash form -> 308 with Location == no-slash canonical
  (29 via vercel.json redirects + 23 via Next.js trailingSlash:false)
- sitemap 53, date-only lastmod 53x2026-11-08
- robots.txt 23 UA lines, llms.txt 53 links + NAP, 0 trailing-slash links
- IndexNow key file 200
- no ?v= in any fetched HTML
Usage: python3 tools/verify_www_flip.py [out.json]
Exit 1 if any PROBLEM.
"""
import json, os, re, sys, urllib.request, urllib.error
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
WWW = 'https://www.tulsawaterdamagerepair.com'
DOMAIN = WWW


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (postpush-www-verify)'})
    try:
        with OPENER.open(req, timeout=30) as r:
            raw = r.read()
            return r.status, dict(r.headers), raw.decode('utf-8', 'replace'), raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, dict(e.headers), raw.decode('utf-8', 'replace'), raw
    except Exception as e:
        return 0, {}, str(e), b''


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = []
        self.title = ''
        self._in_title = False
        self._in_h1 = False
        self.meta_desc = None
        self.canonical = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'h1':
            self._in_h1 = True
        if tag == 'title':
            self._in_title = True
        if tag == 'meta' and d.get('name') == 'description':
            self.meta_desc = d.get('content', '')
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonical = d.get('href')
        if tag == 'meta' and d.get('property') == 'og:url':
            self.og_url = d.get('content')

    def handle_endtag(self, tag):
        if tag == 'h1':
            self._in_h1 = False
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_h1:
            self.h1.append(data.strip())
        if self._in_title:
            self.title += data.strip()


def main():
    problems = []
    res = {'problems': problems, 'pages': {}, 'counts': {}}
    st, _, sm, _ = fetch(WWW + '/sitemap.xml')
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)
    lastmods = re.findall(r'<lastmod>([^<]+)</lastmod>', sm)
    res['counts']['sitemap_locs'] = len(locs)
    res['counts']['sitemap_lastmods'] = dict(Counter(lastmods))
    if st != 200 or len(locs) != 53:
        problems.append(f'sitemap: status {st}, locs {len(locs)} (expected 53)')
    if set(lastmods) != {'2026-11-08'}:
        problems.append(f'sitemap lastmods not all 2026-11-08: {dict(Counter(lastmods))}')
    if any(not re.fullmatch(r'\d{4}-\d{2}-\d{2}', lm) for lm in lastmods):
        problems.append('sitemap: non-date-only lastmod found')

    n200 = n308 = 0
    for loc in locs:
        pr = {}
        res['pages'][loc] = pr
        st, hdr, html, _ = fetch(loc)
        pr['status'] = st
        if st != 200:
            problems.append(f'{loc}: canonical status {st} (expected 200 direct)')
            pr['problems'] = [f'status {st}']
            continue
        n200 += 1
        hp = HeadParser()
        hp.feed(html)
        if hp.canonical != loc:
            problems.append(f'{loc}: canonical {hp.canonical!r} != {loc!r}')
        if hp.og_url != loc:
            problems.append(f'{loc}: og:url {hp.og_url!r} != {loc!r}')
        h1s = [h for h in hp.h1 if h]
        if len(h1s) != 1:
            problems.append(f'{loc}: H1 count {len(h1s)}')
        if not hp.title:
            problems.append(f'{loc}: empty <title>')
        if hp.meta_desc is None:
            problems.append(f'{loc}: meta description missing')
        if '?v=' in html:
            problems.append(f'{loc}: ?v= query string present')
        pr['h1'] = h1s
        pr['canonical_ok'] = hp.canonical == loc
        pr['og_ok'] = hp.og_url == loc
        # slash form -> 308 (all non-homepage)
        if loc != WWW + '/':
            st2, hdr2, _, _ = fetch(loc + '/')
            pr['slash_status'] = st2
            pr['slash_location'] = hdr2.get('Location')
            if st2 != 308:
                problems.append(f'{loc}: slash form status {st2} (expected 308)')
            elif urljoin(loc + '/', hdr2.get('Location') or '') != loc:
                problems.append(f"{loc}: slash form Location {hdr2.get('Location')!r} resolves != {loc!r}")
            else:
                n308 += 1
    res['counts']['canonical_200_direct'] = n200
    res['counts']['slash_308_correct'] = n308
    st, _, rb, _ = fetch(WWW + '/robots.txt')
    ua = len(re.findall(r'^User-agent:', rb, re.M))
    res['counts']['robots_user_agents'] = ua
    if st != 200 or ua != 23 or 'Sitemap:' not in rb:
        problems.append(f'robots.txt: status {st}, UA lines {ua} (expected 23)')
    st, _, lm, _ = fetch(WWW + '/llms.txt')
    urls = re.findall(r'https://www\.tulsawaterdamagerepair\.com[^\s\)\]]*', lm)
    trailing = [u for u in urls if u != DOMAIN + '/' and u.endswith('/')]
    res['counts']['llms_links'] = len(urls)
    res['counts']['llms_trailing_slash'] = len(trailing)
    if set(urls) != set(locs):
        problems.append('llms.txt links != sitemap locs')
    if trailing:
        problems.append(f'llms.txt trailing-slash links: {trailing}')
    if '(918) 395-9320' not in lm or '400 S 129th E Ave' not in lm:
        problems.append('llms.txt missing NAP')
    st, _, _, _ = fetch(WWW + '/b52262ce2b2f10b691644dccabf66495.txt')
    res['counts']['indexnow_key_status'] = st
    if st != 200:
        problems.append(f'IndexNow key file status {st} (expected 200)')
    # favicon files on www
    for f in ('favicon.ico', 'favicon-16x16.png', 'favicon-32x32.png', 'favicon-48x48.png', 'apple-touch-icon.png'):
        stf, _, _, raw = fetch(WWW + '/' + f)
        import hashlib
        local = os.path.join(BASE, 'out', f)
        h_local = hashlib.md5(open(local, 'rb').read()).hexdigest() if os.path.exists(local) else ''
        h_live = hashlib.md5(raw).hexdigest() if raw else ''
        ok = (stf == 200 and h_live == h_local)
        res['counts'].setdefault('favicon_www', {})[f] = 'MATCH' if ok else f'MISMATCH live={stf} md5={h_live[:8]} local={h_local[:8]}'
        if not ok:
            problems.append(f'www favicon {f}: {res["counts"]["favicon_www"][f]}')
    res['counts']['problems'] = len(problems)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'qa-postpush-live', 'verify_www.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(res, open(out_path, 'w'), indent=1)
    print(f"canonicals 200 direct: {n200}/53")
    print(f"slash forms 308 correct: {n308}/52")
    print(f"sitemap locs: {len(locs)} lastmods: {dict(Counter(lastmods))} robots UA: {ua} llms links: {len(urls)} trailing: {len(trailing)}")
    print(f"favicon www: {res['counts']['favicon_www']}")
    print(f"PROBLEMS: {len(problems)}")
    for pr in problems:
        print('  -', pr)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
