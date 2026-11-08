#!/usr/bin/env python3
"""Pass-2 render sweep: H1 visibility + hero presence on ALL 53 pages
(desktop viewport), on the identical local build via Playwright.
Usage: python3 tools/h1_sweep.py <pass_tag>
Writes qa-noslash-round/h1-<tag>.json
"""
import json, os, sys, threading
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_noslash import Handler  # noqa: E402

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
PORT = 8319
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else 'pass2'
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        for p in pages:
            slug = p['slug']
            page = ctx.new_page()
            page.goto(f'http://127.0.0.1:{PORT}{slug}', wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(600)
            r = page.evaluate("""() => {
              const h1s = [...document.querySelectorAll('h1')];
              const h = h1s[0];
              if (!h) return {count: 0};
              const rect = h.getBoundingClientRect();
              const cs = getComputedStyle(h);
              const hero = document.querySelector('section.hero');
              const img = hero ? hero.querySelector('img') : null;
              return {count: h1s.length, text: h.textContent.trim(),
                visible: cs.display !== 'none' && cs.visibility !== 'hidden' && rect.height > 0 && rect.width > 0,
                top: Math.round(rect.top), height: Math.round(rect.height),
                hero: !!hero, heroImg: img ? img.getAttribute('src') : null,
                overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth};
            }""")
            r['doc_h1'] = p['h1']
            r['h1_match'] = (r.get('text') == p['h1'])
            out[slug] = r
            page.close()
        browser.close()
    json.dump(out, open(os.path.join(BASE, 'qa-noslash-round', f'h1-{tag}.json'), 'w'), indent=1)
    server.shutdown()
    bad = {s: v for s, v in out.items() if v.get('count') != 1 or not v.get('visible') or not v.get('h1_match') or v.get('overflowX', 0) != 0}
    nohero = [s for s, v in out.items() if not v.get('heroImg')]
    print(f"pages swept: {len(out)}  H1 1x+visible+verbatim+no-overflow: {len(out)-len(bad)}/{len(out)}")
    print(f"pages without hero img (brand panel fallback): {len(nohero)} {nohero}")
    for s, v in bad.items():
        print('  BAD', s, v)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
