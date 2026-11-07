#!/usr/bin/env python3
"""Merge images-a.json + images-b.json (written by the image subagents)
into site/content/images.json. Slots missing from both stay absent — the
template renders a branded panel for those, never a filler photo."""
import json, os, sys
BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site/content')
merged = {}
missing = []
for name in ('images-a.json', 'images-b.json'):
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        print(f'{name}: not present yet, skipping')
        continue
    d = json.load(open(path))
    for k, v in d.items():
        if k == 'missing':
            missing.extend(v)
            continue
        if k not in merged:
            merged[k] = dict(v)
            continue
        # Per-field merge: a null hero/body in one file must NEVER clobber a
        # filled slot from the other (B re-searched A's hero slots, found
        # nothing, and logged them missing — its nulls overwrote A's heroes).
        for field in ('hero', 'body'):
            if merged[k].get(field) is None and v.get(field) is not None:
                merged[k][field] = v[field]
            elif merged[k].get(field) is not None and v.get(field) is not None:
                print(f'WARNING: duplicate {field} for {k} in {name} — keeping first')
# `missing` is the agents' own log (hero slots they could not fill); the
# merged audit below is the source of truth for what is actually empty.
json.dump(merged, open(os.path.join(BASE, 'images.json'), 'w'), indent=1)
filled = sum(1 for v in merged.values() if v.get('hero'))
body = sum(1 for v in merged.values() if v.get('body'))
print(f'merged: {len(merged)} slugs, {filled} heroes, {body} body images, {len(missing)} missing slots')
for m in missing:
    print('  MISSING:', m)
