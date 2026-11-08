/* Server-only page data. NEVER import this module from a 'use client'
   component: it imports content/pages.json (796 KB) + content/images.json
   at module top level, and any client import bundles the whole dataset
   into client JS (U1: that was the 694 KB chunk 986). Client components
   import metadata from ./lib-meta.js instead (SITE, groups, titles —
   literals only, no JSON). Server components may import from here. */
import pagesDataRaw from '../content/pages.json';
import imagesData from '../content/images.json';

/* Re-export client-safe metadata so server-side importers keep one import
   path. (These come from ./lib-meta.js and carry no page data.) */
export {
  SITE,
  normSlug,
  shortName,
  parentOf,
  SERVICE_GROUPS,
  SERVICE_SLUGS,
  SERVICE_TITLES,
  AREA_GROUPS,
  AREA_SLUGS,
  FOOTER_SERVICES,
  FOOTER_AREAS,
  RESOURCE_SLUGS,
  TRUST_CHECKS,
  areaMapQuery,
} from './lib-meta';

/* The parser HTML-escapes plain-text fields (blurb, intro, h1, FAQ questions,
   h2 text, schema answer text) because it also builds HTML strings from them.
   Those fields are rendered as JSX text or JSON strings, where React/JSON
   would escape the & a second time and the page would show literal &#x27;.
   Decode entities in PLAIN-TEXT fields only — `html`/`a_html` fields stay
   escaped because they are injected as HTML via dangerouslySetInnerHTML. */
const NAMED = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
  ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“',
  hellip: '…', copy: '©', reg: '®', trade: '™',
};
function unescapeEntities(s) {
  if (typeof s !== 'string' || !s.includes('&')) return s;
  return s
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(parseInt(d, 10)))
    .replace(/&([a-zA-Z]+);/g, (_, n) => (NAMED[n] !== undefined ? NAMED[n] : `&${n};`));
}
function fixPage(p) {
  const q = { ...p };
  for (const f of ['h1', 'metaTitle', 'metaDescription', 'blurb', 'intro']) {
    if (q[f]) q[f] = unescapeEntities(q[f]);
  }
  if (Array.isArray(q.faqs)) {
    q.faqs = q.faqs.map((f) => ({ ...f, q: unescapeEntities(f.q), a_text: unescapeEntities(f.a_text) }));
  }
  if (Array.isArray(q.blocks)) {
    q.blocks = q.blocks.map((b) => {
      const nb = { ...b };
      if (nb.text) nb.text = unescapeEntities(nb.text);
      if (nb.plain) nb.plain = unescapeEntities(nb.plain);
      return nb;
    });
  }
  return q;
}
const pagesData = pagesDataRaw.map(fixPage);

export const PAGES = pagesData;
export const IMAGES = imagesData && typeof imagesData === 'object' ? imagesData : {};
export const PAGE_BY_SLUG = Object.fromEntries(PAGES.map((p) => [p.slug, p]));

export function pageImage(slug) {
  const entry = IMAGES[slug] || {};
  return {
    hero: entry.hero ? { ...entry.hero } : null,
    body: entry.body ? { ...entry.body } : null,
  };
}
