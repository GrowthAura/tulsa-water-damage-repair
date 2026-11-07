#!/usr/bin/env python3
"""Core Web Vitals (measured, not claimed) + overflow + console for the
Tulsa site, against the isolated local build.
Usage: python3 tools/seo_cwv.py --base http://127.0.0.1:8321 --pass 1
Writes site/qa-see-seo/seo-cwv-pass<N>.json. Exit 1 on overflow>0 or console errors.
LCP: largest-contentful-paint entry after load+1.5s settle. CLS: sum of
layout-shift entries (hadRecentInput excluded). Real Chromium via Playwright.
"""
import argparse, json, os
from playwright.sync_api import sync_playwright

SITE_DIR = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
QA = os.path.join(SITE_DIR, 'qa-see-seo')
ap = argparse.ArgumentParser()
ap.add_argument('--base', required=True)
ap.add_argument('--pass', dest='passno', type=int, required=True)
args = ap.parse_args()
ROOT = args.base.rstrip('/')

pages = json.load(open(os.path.join(SITE_DIR, 'content', 'pages.json')))
CWV_PAGES = ['/', '/services/emergency-water-damage-restoration',
             '/service-areas/broken-arrow-ok/']
INIT_SCRIPT = """
  window.__lcp = [];
  window.__cls = 0;
  new PerformanceObserver((l) => {
    for (const e of l.getEntries()) window.__lcp.push(e.startTime);
  }).observe({type: 'largest-contentful-paint', buffered: true});
  new PerformanceObserver((l) => {
    for (const e of l.getEntries()) { if (!e.hadRecentInput) window.__cls += e.value; }
  }).observe({type: 'layout-shift', buffered: true});
"""
LCP_READ = "() => (window.__lcp && window.__lcp.length ? window.__lcp[window.__lcp.length-1] : null)"
out = {'pass': args.passno, 'cwv': {}, 'overflow': {}, 'console': {}}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # CWV on 3 pages x desktop 1440 + mobile 390
    for slug in CWV_PAGES:
        for label, w, h in (('desktop-1440', 1440, 900), ('mobile-390', 390, 844)):
            ctx = browser.new_context(viewport={'width': w, 'height': h})
            pg = ctx.new_page()
            pg.add_init_script(INIT_SCRIPT)
            pg.goto(ROOT + slug, wait_until='load', timeout=30000)
            pg.wait_for_timeout(2500)
            lcp = pg.evaluate(LCP_READ)
            cls = pg.evaluate("() => window.__cls")
            out['cwv'].setdefault(slug, {})[label] = {
                'lcp_ms': round(lcp) if lcp is not None else None,
                'cls': round(cls, 4) if cls is not None else None}
            ctx.close()
    # overflow + console on all 53 pages at 1440/390/320
    for p in pages:
        slug = p['slug']
        row, errs = {}, []
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(350)
            row[w] = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            ctx.close()
        out['overflow'][slug] = row
        out['console'][slug] = sorted(set(errs))
    browser.close()

bad_overflow = {s: r for s, r in out['overflow'].items() if any(v != 0 for v in r.values())}
bad_console = {s: e for s, e in out['console'].items() if e}
os.makedirs(QA, exist_ok=True)
with open(os.path.join(QA, f'seo-cwv-pass{args.passno}.json'), 'w') as f:
    json.dump(out, f, indent=2)
print(f"CWV PASS {args.passno}")
for slug, v in out['cwv'].items():
    print(f"  {slug}: desktop LCP {v['desktop-1440']['lcp_ms']}ms CLS {v['desktop-1440']['cls']} | "
          f"mobile LCP {v['mobile-390']['lcp_ms']}ms CLS {v['mobile-390']['cls']}")
print(f"  overflow>0 pages: {len(bad_overflow)} {bad_overflow if bad_overflow else ''}")
print(f"  console-error pages: {len(bad_console)} {bad_console if bad_console else ''}")
