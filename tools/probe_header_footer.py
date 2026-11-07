#!/usr/bin/env python3
"""Header + footer probe: screenshots (header/footer, desktop + mobile,
mobile menu open), H1/overflow/console checks, and a full fetch of every
header + footer link on every sitemap page. Writes site/qa-header-footer/.
Usage: python3 tools/probe_header_footer.py (serve.py must run on :8317)."""
import json, os, re, urllib.request
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-header-footer')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

def fetch(path):
    try:
        with urllib.request.urlopen(ROOT + path, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f'ERR:{e}'

# sitemap slugs (strip domain)
sm = open(os.path.join(BASE, 'public', 'sitemap.xml')).read()
slugs = sorted(set(re.findall(r'https://tulsawaterdamagerepair\.com([^<\s]*)', sm)))
print('sitemap slugs:', len(slugs))

PAGES = [('/', 'home'), ('/services/emergency-water-damage-restoration', 'service'),
         ('/service-areas/broken-arrow-ok/', 'area'), ('/contact/', 'contact')]
rows, all_hf_links = [], set()
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug, safe in PAGES:
        row = {'slug': slug, 'widths': {}}
        for w in (1440, 390):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            errors = []
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(400)
            m = pg.evaluate("""() => {
              const q = s => document.querySelector(s);
              const hdr = q('.site-header'), ftr = q('.site-footer');
              const hdrLinks = [...hdr.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
              const ftrLinks = [...ftr.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
              const iframes = [...document.querySelectorAll('iframe')].map(f => f.src);
              return {
                overflow: document.documentElement.scrollWidth - window.innerWidth,
                h1: document.querySelectorAll('h1').length,
                headerH: hdr ? Math.round(hdr.getBoundingClientRect().height) : null,
                headerSticky: hdr ? getComputedStyle(hdr).position : null,
                headerVisibleAfterScroll: null,
                brandText: hdr ? hdr.querySelector('.brand').textContent.trim().replace(/\\s+/g,' ') : null,
                brandMarkHTML: hdr ? hdr.querySelector('.brand-mark').innerHTML : null,
                ctaVisible: (() => { const c = q('.header-cta'); if (!c) return false;
                  const r = c.getBoundingClientRect(); return r.width > 0 && getComputedStyle(c).display !== 'none'; })(),
                mobileCallBar: (() => { const b = q('.mobile-call-bar'); if (!b) return false;
                  const r = b.getBoundingClientRect(); return r.width > 0 && getComputedStyle(b).display !== 'none'; })(),
                footerCols: ftr ? ftr.querySelectorAll('.footer-col').length : 0,
                footerHeadings: ftr ? [...ftr.querySelectorAll('.footer-col h3')].map(h => h.textContent.trim()) : [],
                footerMap: !!ftr.querySelector('.footer-map iframe'),
                iframes, hdrLinks, ftrLinks,
              };
            }""")
            # sticky check: scroll down, header still at top of viewport
            pg.evaluate("window.scrollTo(0, 800)")
            pg.wait_for_timeout(300)
            m['headerVisibleAfterScroll'] = pg.evaluate(
                "() => { const h = document.querySelector('.site-header'); const r = h.getBoundingClientRect(); return r.top <= 0 && r.bottom > 0; }")
            pg.evaluate("window.scrollTo(0, 0)")
            pg.wait_for_timeout(200)
            m['consoleErrors'] = errors
            for h in m['hdrLinks'] + m['ftrLinks']:
                if h.startswith('/'):
                    all_hf_links.add(h)
            row['widths'][w] = m
            # screenshots: header top + footer
            hdr = pg.locator('.site-header')
            hdr.screenshot(path=os.path.join(OUT, f'{safe}-header-{w}.png'))
            ftr = pg.locator('.site-footer')
            ftr.screenshot(path=os.path.join(OUT, f'{safe}-footer-{w}.png'))
            if w == 390:
                # open mobile menu, screenshot it
                pg.click('.mobile-head summary', timeout=5000)
                pg.wait_for_timeout(400)
                pg.screenshot(path=os.path.join(OUT, f'{safe}-mobile-menu-{w}.png'))
                m['mobileMenuOpen'] = pg.evaluate(
                    "() => document.querySelector('.mobile-head details').open")
                m['mobileMenuLinks'] = pg.evaluate(
                    "() => [...document.querySelectorAll('.mobile-menu a[href]')].map(a => a.getAttribute('href'))")
                for h in m['mobileMenuLinks']:
                    if h.startswith('/'):
                        all_hf_links.add(h)
            ctx.close()
        rows.append(row)
    browser.close()

# fetch every distinct header/footer link found
link_rows = []
for h in sorted(all_hf_links):
    st = fetch(h)
    link_rows.append({'href': h, 'status': st})
broken = [r for r in link_rows if r['status'] != 200]
print(f'header/footer distinct links: {len(link_rows)}  broken(non-200): {len(broken)}')
for b in broken:
    print('  BROKEN:', b)

# fetch every sitemap URL too
sm_broken = []
for s in slugs:
    st = fetch(s if s else '/')
    if st != 200:
        sm_broken.append({'href': s, 'status': st})
print(f'sitemap URLs: {len(slugs)}  broken: {len(sm_broken)}')
for b in sm_broken:
    print('  SITEMAP BROKEN:', b)

json.dump({'pages': rows, 'hf_links': link_rows, 'hf_broken': broken,
           'sitemap_broken': sm_broken}, open(os.path.join(OUT, 'probe.json'), 'w'), indent=1)
print('probe.json written')
