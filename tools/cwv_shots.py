#!/usr/bin/env python3
"""Render checks for the no-slash round: CWV (LCP/CLS/transfer) + screenshots
on the identical local build, desktop + mobile, via Playwright.
Serves site/out/ on 127.0.0.1:8318 using the audit server's Vercel-faithful
handler (extensionless + slash->308). Usage:
  python3 tools/cwv_shots.py <pass_tag>   # writes qa-noslash-round/cwv-<tag>.json
  + screenshots to qa-noslash-round/shots-<tag>/...
"""
import json, os, sys, threading
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_noslash import Handler  # noqa: E402

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-noslash-round')
PORT = 8318
PAGES = ['/', '/services', '/contact', '/commercial']

LCP_JS = """() => new Promise((resolve) => {
  let lcp = 0;
  const po = new PerformanceObserver((list) => {
    for (const e of list.getEntries()) lcp = Math.max(lcp, e.startTime);
  });
  po.observe({type: 'largest-contentful-paint', buffered: true});
  setTimeout(() => { po.disconnect(); resolve(lcp); }, 3500);
})"""

CLS_JS = """() => new Promise((resolve) => {
  let cls = 0;
  const po = new PerformanceObserver((list) => {
    for (const e of list.getEntries()) { if (!e.hadRecentInput) cls += e.value; }
  });
  po.observe({type: 'layout-shift', buffered: true});
  setTimeout(() => { po.disconnect(); resolve(cls); }, 3500);
})"""

BYTES_JS = """() => {
  let total = 0;
  for (const e of performance.getEntriesByType('resource')) total += (e.transferSize || 0);
  const nav = performance.getEntriesByType('navigation')[0];
  if (nav) total += (nav.transferSize || 0);
  return total;
}"""


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else 'pass1'
    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright
    shots_dir = os.path.join(OUT, f'shots-{tag}')
    os.makedirs(shots_dir, exist_ok=True)
    results = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for slug in PAGES:
            name = 'home' if slug == '/' else slug.strip('/').replace('/', '_')
            for mode, ctx_kw in (
                ('desktop', {'viewport': {'width': 1440, 'height': 900}}),
                ('mobile', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True,
                 'has_touch': True, 'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'}),
            ):
                ctx = browser.new_context(**ctx_kw)
                page = ctx.new_page()
                page.goto(f'http://127.0.0.1:{PORT}{slug}', wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(4000)
                lcp = page.evaluate(LCP_JS)
                cls = page.evaluate(CLS_JS)
                total_bytes = page.evaluate(BYTES_JS)
                h1 = page.evaluate("""() => {
                  const h = document.querySelector('h1');
                  if (!h) return null;
                  const r = h.getBoundingClientRect();
                  const cs = getComputedStyle(h);
                  return {text: h.textContent.trim(), visible: cs.display !== 'none' && cs.visibility !== 'hidden' && r.height > 0 && r.width > 0, top: r.top, height: r.height};
                }""")
                hero = page.evaluate("""() => {
                  const s = document.querySelector('section.hero');
                  if (!s) return null;
                  const r = s.getBoundingClientRect();
                  const img = s.querySelector('img');
                  return {height: r.height, img: img ? {src: img.getAttribute('src'), w: img.naturalWidth, h: img.naturalHeight, dw: img.getBoundingClientRect().width, dh: img.getBoundingClientRect().height} : null};
                }""")
                overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                shot = os.path.join(shots_dir, f'{name}-{mode}.png')
                page.screenshot(path=shot)
                full = os.path.join(shots_dir, f'{name}-{mode}-full.png')
                page.screenshot(path=full, full_page=True)
                results[f'{slug}|{mode}'] = {
                    'lcp_ms': round(lcp), 'cls': round(cls, 4), 'transfer_bytes': total_bytes,
                    'transfer_kb': round(total_bytes / 1024, 1),
                    'h1': h1, 'hero': hero, 'h_overflow_px': overflow,
                    'shot': shot, 'full_shot': full,
                }
                print(f"{slug} {mode}: LCP {lcp:.0f}ms CLS {cls:.4f} {total_bytes/1024:.1f}KB H1-visible={h1 and h1['visible']} overflow={overflow}px")
                ctx.close()
        browser.close()
    json.dump(results, open(os.path.join(OUT, f'cwv-{tag}.json'), 'w'), indent=1)
    server.shutdown()
    worst_lcp = max(v['lcp_ms'] for v in results.values())
    worst_cls = max(v['cls'] for v in results.values())
    worst_kb = max(v['transfer_kb'] for v in results.values())
    print(f"worst LCP {worst_lcp}ms (budget 1800)  worst CLS {worst_cls} (budget 0)  worst transfer {worst_kb}KB (mobile budget 800)")
    print(f"mobile transfer: {[(k, v['transfer_kb']) for k, v in results.items() if k.endswith('mobile')]}")


if __name__ == '__main__':
    main()
