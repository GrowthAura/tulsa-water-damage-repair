#!/usr/bin/env python3
"""Fix: mirror the See/see cuts into FAQ `a_text` (plain-text field the FAQPage
schema is built from). The first cut pass only edited `a_html` (visible),
leaving 42 FAQ schema answers still ending in a dangling 'See' — visible !=
schema. a_text stores apostrophes as &#x27; entities, so comparison unescapes
first; the write cuts the trailing fragment from the RAW a_text string.
FAILS (no write) if any a_text differs from strip_tags(a_html) by anything
other than a trailing dangling See/see/See-and (after unescaping)."""
import json, re, html
from html.parser import HTMLParser

BASE = '/home/hatch/workspace/tulsa-water-damage-repair/site'
d = json.load(open(f'{BASE}/content/pages.json'))

class TE(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []
    def handle_data(self, x): self.parts.append(x)
    def text(self): return ''.join(self.parts)

def strip_tags(s):
    x = TE(); x.feed(s or ''); return html.unescape(x.text()).strip()

def norm(s):
    return re.sub(r'\s+', ' ', (s or '').strip())

def cut_trailing_see(s):
    """Remove a trailing dangling 'See and' or 'See'/'see' from a string."""
    s2 = re.sub(r'\s+See\s+and\s*$', '', s)
    s2 = re.sub(r'\s+[Ss]ee\.?\s*$', '', s2)
    return s2

fixed = []
other_diffs = []
for p in d:
    for fi, f in enumerate(p.get('faqs', [])):
        a_html = f.get('a_html', '')
        a_text = f.get('a_text', '')
        vis = norm(strip_tags(a_html))
        sch = norm(html.unescape(a_text))
        if vis == sch:
            continue
        cand = cut_trailing_see(sch)
        if cand == vis:
            # apply the same cut to the RAW a_text (entities intact)
            raw_new = cut_trailing_see(a_text.rstrip())
            assert norm(html.unescape(raw_new)) == vis, (p['slug'], fi, raw_new[-80:], vis[-80:])
            fixed.append({'slug': p['slug'], 'faq': fi, 'q': f['q'][:60],
                          'before': sch[-70:], 'after': cand[-70:]})
            f['a_text'] = raw_new
        else:
            other_diffs.append({'slug': p['slug'], 'faq': fi, 'q': f['q'][:60],
                                'visible_tail': vis[-90:], 'schema_tail': sch[-90:]})

print('a_text See-cuts applied:', len(fixed))
for x in fixed:
    print('  ', x['slug'], 'FAQ', x['faq'], '::', repr(x['before'][-45:]), '->', repr(x['after'][-45:]))
print('OTHER diffs (not fixed, need review):', len(other_diffs))
for x in other_diffs:
    print('  ', x)
assert not other_diffs, 'unexplained a_text/a_html diffs — not writing'
json.dump(d, open(f'{BASE}/content/pages.json', 'w'), indent=2, ensure_ascii=False)
json.dump(fixed, open(f'{BASE}/qa-home-round/faq-atext-cuts.json', 'w'), indent=2, ensure_ascii=False)
print('pages.json written.')
