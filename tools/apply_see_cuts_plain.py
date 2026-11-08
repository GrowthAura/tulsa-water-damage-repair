#!/usr/bin/env python3
"""Follow-up: cut the 8 PLAIN-text 'See and' fragments found by re-verification.
These are 'See  and' with a plain (unlinked) 'and' at the end of a paragraph /
FAQ answer — the same dangling family as the 18 anchored ones, missed by the
first pass because the first pass only matched '<a>and</a>'."""
import json, re

BASE = '/home/hatch/workspace/tulsa-water-damage-repair/site'
d = json.load(open(f'{BASE}/content/pages.json'))
by_slug = {p['slug']: p for p in d}
targets = [
    ('/service-areas/sand-springs-ok/', 9, None),
    ('/service-areas/skiatook-ok/', 13, None),
    ('/service-areas/sapulpa-ok/', 9, None),
    ('/service-areas/midtown-tulsa/', 10, None),
    ('/service-areas/midtown-tulsa/', None, 2),
    ('/service-areas/brookside-tulsa/', 10, None),
    ('/service-areas/north-tulsa/', 10, None),
    ('/resources/signs-of-hidden-water-damage', 23, None),
]
cuts = json.load(open(f'{BASE}/qa-home-round/see-cuts-applied.json'))
pat = re.compile(r' ?See +and\s*$')
for slug, bi, fi in targets:
    p = by_slug[slug]
    if fi is not None:
        text = p['faqs'][fi]['a_html']
        setter = lambda v: p['faqs'].__setitem__(fi, {**p['faqs'][fi], 'a_html': v})
        where = f'FAQ {fi}'
    else:
        text = p['blocks'][bi]['html']
        setter = lambda v, b=bi: p['blocks'].__setitem__(b, {**p['blocks'][b], 'html': v})
        where = f'block {bi}'
    matches = pat.findall(text)
    assert len(matches) == 1, f'{slug} {where}: expected 1 plain See-and, found {len(matches)} :: {text[-140:]}'
    assert '<a' not in matches[0], f'{slug} {where}: anchor present, not plain :: {text[-140:]}'
    new = pat.sub('', text, count=1)
    assert new.rstrip().endswith('.'), f'{slug} {where}: result does not end with a period :: {new[-140:]}'
    setter(new)
    cuts.append({'type': 'see-and-plain', 'slug': slug, 'block': bi, 'faq': fi,
                 'before': text[-140:], 'after': new[-140:]})
    print('cut', slug, where, '::', repr(text[-60:]), '->', repr(new[-60:]))

json.dump(d, open(f'{BASE}/content/pages.json', 'w'), indent=2, ensure_ascii=False)
json.dump(cuts, open(f'{BASE}/qa-home-round/see-cuts-applied.json', 'w'), indent=2, ensure_ascii=False)
print('done. total cut records:', len(cuts))
