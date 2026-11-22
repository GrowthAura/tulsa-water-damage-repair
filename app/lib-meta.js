/* Client-safe site metadata — NO page data, NO JSON imports.
   This module is imported by 'use client' components (Header, ContactForm),
   so NOTHING in it may pull in content/pages.json (796 KB) or
   content/images.json: before this split, importing lib.js from a client
   component bundled the whole pages.json into the shared client chunk
   (986-…js = 694 KB, homepage transfer >1.1 MB).
   Server-only data (PAGES, PAGE_BY_SLUG, IMAGES, pageImage) lives in
   ./lib.js, which client components must NEVER import. */

export const SITE = {
  brand: 'Tulsa Water Damage Repair',
  domain: 'www.tulsawaterdamagerepair.com',
  url: 'https://www.tulsawaterdamagerepair.com',
  phone: '(918) 395-9320',
  phoneHref: 'tel:+19183959320',
  address: '400 S 129th E Ave, Tulsa, OK 74108',
  mapQuery: '400 S 129th E Ave, Tulsa, OK 74108',
};

export function normSlug(s) {
  if (!s) return '/';
  return s === '/' ? '/' : s.replace(/\/$/, '') || '/';
}

export function shortName(slug) {
  const last = slug.replace(/\/$/, '').split('/').filter(Boolean).pop() || 'home';
  return last
    .replace(/-ok$/, '')
    .replace(/-tulsa$/, '')
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

export function parentOf(page) {
  if (page.type === 'service') return { label: 'Services', href: '/services' };
  /* No /service-areas/ hub route exists, so area pages have no parent crumb:
     linking "Service Areas" to "/" was a duplicate Home link with a wrong name. */
  if (page.type === 'area') return null;
  if (page.type === 'resource') return { label: 'Resources', href: '/resources' };
  return null;
}

/* Service groups for nav dropdown + cards — order follows the doc's homepage groups. */
export const SERVICE_GROUPS = [
  {
    label: 'Emergency & Water Removal',
    slugs: [
      '/services/emergency-water-damage-restoration',
      '/services/water-mitigation',
      '/services/flood-damage-restoration',
      '/services/flooded-basement-cleanup',
      '/services/sewage-backup-cleanup',
    ],
  },
  {
    label: 'Water Damage by Source',
    slugs: [
      '/services/burst-pipe-water-damage',
      '/services/slab-leak-water-damage',
      '/services/water-heater-leak-cleanup',
      '/services/appliance-leak-water-damage',
      '/services/ac-drain-line-overflow-cleanup',
      '/services/roof-leak-water-damage',
    ],
  },
  {
    label: 'Water Damage by Material',
    slugs: ['/services/ceiling-water-damage', '/services/hardwood-floor-drying'],
  },
  {
    label: 'Mold, Fire & Storm',
    slugs: [
      '/services/mold-remediation',
      '/services/storm-damage-repair',
      '/services/fire-damage-restoration',
      '/services/smoke-soot-damage-cleanup',
    ],
  },
  {
    label: 'Commercial',
    slugs: ['/services/commercial-water-damage'],
  },
];

export const SERVICE_SLUGS = SERVICE_GROUPS.flatMap((g) => g.slugs);

/* Doc service names per href, taken from the /services/ hub's grouped lists
   (the <strong> service name in each item). The homepage's grouped lists
   carry the same 18 services as single links with no <strong> separator, so
   the hub names give the title/description boundary there. Both slash forms
   are keyed because the doc mixes them.
   STATIC LITERAL (U1, 2026-11-08): previously computed at runtime by
   scanning PAGES (which forced the whole pages.json into the client
   bundle). Values are verbatim from the hub doc lists — including the
   <a> tags some carry (parseServiceItem strips those at render time,
   B1 fix). Regenerate from content/pages.json if the hub lists change:
   for each ul-block item in the /services/ hub page, map href -> <strong>
   inner HTML, plus the normSlug(href) key. */
export const SERVICE_TITLES = {
  '/services/burst-pipe-water-damage': '<a href="/services/burst-pipe-water-damage">Burst pipe water damage</a>',
  '/services/slab-leak-water-damage': '<a href="/services/slab-leak-water-damage">Slab leak water damage</a>',
  '/services/slab-leak-water-damage': '<a href="/services/slab-leak-water-damage">Slab leak water damage</a>',
  '/services/water-heater-leak-cleanup': '<a href="/services/water-heater-leak-cleanup">Water heater leak cleanup</a>',
  '/services/water-heater-leak-cleanup': '<a href="/services/water-heater-leak-cleanup">Water heater leak cleanup</a>',
  '/services/appliance-leak-water-damage': '<a href="/services/appliance-leak-water-damage">Appliance leak water damage</a>',
  '/services/appliance-leak-water-damage': '<a href="/services/appliance-leak-water-damage">Appliance leak water damage</a>',
  '/services/ac-drain-line-overflow-cleanup': '<a href="/services/ac-drain-line-overflow-cleanup">AC drain line overflow cleanup</a>',
  '/services/ac-drain-line-overflow-cleanup': '<a href="/services/ac-drain-line-overflow-cleanup">AC drain line overflow cleanup</a>',
  '/services/roof-leak-water-damage': '<a href="/services/roof-leak-water-damage">Roof leak water damage</a>',
  '/services/roof-leak-water-damage': '<a href="/services/roof-leak-water-damage">Roof leak water damage</a>',
  '/services/ceiling-water-damage': 'Ceiling and drywall water damage',
  '/services/hardwood-floor-drying': 'Hardwood floor drying',
  '/services/fire-damage-restoration': '<a href="/services/fire-damage-restoration">Fire damage restoration</a>',
  '/services/smoke-soot-damage-cleanup': '<a href="/services/smoke-soot-damage-cleanup">Smoke and soot cleanup</a>',
  /* Homepage service-list cards (2026-11-08): the 3 homepage groups have no
     <strong>, so parseServiceItem falls back to this map. Plain titles here —
     the card's <Link> is the single link; values are stripped of <a> at render. */
  '/services/emergency-water-damage-restoration': 'Emergency water damage restoration',
  '/services/water-mitigation': 'Water mitigation and structural drying',
  '/services/flood-damage-restoration': 'Flood damage restoration',
  '/services/flooded-basement-cleanup': 'Flooded basement and crawlspace cleanup',
  '/services/sewage-backup-cleanup': 'Sewage backup cleanup',
  '/services/mold-remediation': 'Mold remediation',
  '/services/storm-damage-repair': 'Storm damage repair',
  '/services/commercial-water-damage': 'Commercial water damage restoration',
};

export const AREA_GROUPS = [
  {
    label: 'Tulsa Neighborhoods',
    slugs: [
      '/service-areas/midtown-tulsa',
      '/service-areas/brookside-tulsa',
      '/service-areas/south-tulsa',
      '/service-areas/west-tulsa',
      '/service-areas/north-tulsa',
      '/service-areas/east-tulsa',
      '/service-areas/cherry-street-tulsa',
    ],
  },
  {
    label: 'Nearby Communities',
    slugs: [
      '/service-areas/broken-arrow-ok',
      '/service-areas/owasso-ok',
      '/service-areas/bixby-ok',
      '/service-areas/jenks-ok',
      '/service-areas/sand-springs-ok',
      '/service-areas/glenpool-ok',
      '/service-areas/claremore-ok',
      '/service-areas/catoosa-ok',
      '/service-areas/collinsville-ok',
      '/service-areas/skiatook-ok',
      '/service-areas/coweta-ok',
      '/service-areas/sapulpa-ok',
    ],
  },
];

export const AREA_SLUGS = AREA_GROUPS.flatMap((g) => g.slugs);

/* Footer best-ever service picks (theme rule: header/footer carry only the best). */
export const FOOTER_SERVICES = [
  '/services/emergency-water-damage-restoration',
  '/services/water-mitigation',
  '/services/flood-damage-restoration',
  '/services/mold-remediation',
  '/services/burst-pipe-water-damage',
  '/services/sewage-backup-cleanup',
  '/services/storm-damage-repair',
  '/services/hardwood-floor-drying',
  '/services/commercial-water-damage',
];

export const FOOTER_AREAS = [
  '/service-areas/broken-arrow-ok',
  '/service-areas/owasso-ok',
  '/service-areas/bixby-ok',
  '/service-areas/jenks-ok',
  '/service-areas/sand-springs-ok',
  '/service-areas/glenpool-ok',
  '/service-areas/claremore-ok',
  '/service-areas/catoosa-ok',
  '/service-areas/collinsville-ok',
  '/service-areas/skiatook-ok',
  '/service-areas/coweta-ok',
  '/service-areas/sapulpa-ok',
];

/* Geo — rebuild 2026-11-22 (§6a). Business coords are the verified lookup
   of the business address (36.15467, -95.83348). Suburb coords were verified
   with real geocoding (street/full-address level, correct city + county)
   2026-11-22; the 7 Tulsa neighborhoods sit inside Tulsa, so they carry
   the business (Tulsa) coords — logged, not invented. */
export const BUSINESS_GEO = { latitude: 36.15467, longitude: -95.83348 };

export const AREA_GEO = {
  '/service-areas/broken-arrow-ok': { name: 'Broken Arrow, Oklahoma', latitude: 36.07077, longitude: -95.7962 },
  '/service-areas/owasso-ok': { name: 'Owasso, Oklahoma', latitude: 36.26806, longitude: -95.85502 },
  '/service-areas/bixby-ok': { name: 'Bixby, Oklahoma', latitude: 35.93809, longitude: -95.88054 },
  '/service-areas/jenks-ok': { name: 'Jenks, Oklahoma', latitude: 36.02427, longitude: -95.97524 },
  '/service-areas/sand-springs-ok': { name: 'Sand Springs, Oklahoma', latitude: 36.13966, longitude: -96.10843 },
  '/service-areas/glenpool-ok': { name: 'Glenpool, Oklahoma', latitude: 35.96465, longitude: -96.0103 },
  '/service-areas/claremore-ok': { name: 'Claremore, Oklahoma', latitude: 36.30566, longitude: -95.6079 },
  '/service-areas/catoosa-ok': { name: 'Catoosa, Oklahoma', latitude: 36.18809, longitude: -95.74602 },
  '/service-areas/collinsville-ok': { name: 'Collinsville, Oklahoma', latitude: 36.36423, longitude: -95.84014 },
  '/service-areas/skiatook-ok': { name: 'Skiatook, Oklahoma', latitude: 36.36818, longitude: -95.99799 },
  '/service-areas/coweta-ok': { name: 'Coweta, Oklahoma', latitude: 35.95195, longitude: -95.65021 },
  '/service-areas/sapulpa-ok': { name: 'Sapulpa, Oklahoma', latitude: 35.99932, longitude: -96.09716 },
  '/service-areas/midtown-tulsa': { name: 'Midtown Tulsa, Oklahoma', latitude: 36.12959, longitude: -95.9741 },
  '/service-areas/brookside-tulsa': { name: 'Brookside, Tulsa, Oklahoma', latitude: 36.10418, longitude: -95.972 },
  '/service-areas/south-tulsa': { name: 'South Tulsa, Oklahoma', latitude: 36.06785, longitude: -95.93277 },
  '/service-areas/west-tulsa': { name: 'West Tulsa, Oklahoma', latitude: 36.13503, longitude: -96.00252 },
  '/service-areas/north-tulsa': { name: 'North Tulsa, Oklahoma', latitude: 36.21862, longitude: -95.97471 },
  '/service-areas/east-tulsa': { name: 'East Tulsa, Oklahoma', latitude: 36.17328, longitude: -95.94032 },
  '/service-areas/cherry-street-tulsa': { name: 'Cherry Street, Tulsa, Oklahoma', latitude: 36.14073, longitude: -95.97128 },
};

export function pageGeo(slug) {
  return AREA_GEO[slug] || { name: 'Tulsa, Oklahoma', ...BUSINESS_GEO };
}

/* Area identity (#4, follow-up 2026-11-23): one distinct "at a glance"
   block per directional area page (South / West / North / East Tulsa only).
   Every fact is drawn from that page's own doc content in
   content/pages.json (ZIP/coverage lists + intro + pattern sections).
   Nothing invented, no clean ZIP partition forced (74127 spans West +
   North, 74145 spans South + East, exactly as the doc states it).
   Maps URLs verified live 2026-11-23 (all HTTP 200; South needed a
   browser user agent on the first hit, 403 on curl's default UA, then
   200 twice with a browser UA). Coordinates reuse AREA_GEO. */
export const AREA_IDENTITY = {
  '/service-areas/south-tulsa': {
    variant: 'slab',
    name: 'South Tulsa',
    eyebrow: 'South Tulsa at a glance',
    heading: 'Slab homes, attic air handlers, and hail roofs',
    lede: "South Tulsa from 61st Street south past 101st, Sheridan to Memorial and beyond is slab homes, attic-mounted air handlers and roofs that take hail every spring. That construction pattern drives South Tulsa's three most common water damage calls: slab leaks that spread under flooring for weeks before anyone notices, AC condensate overflows that soak ceilings overnight in July, and water heaters that pick the worst possible night to fail.",
    stat: { value: '1970s to 2000s', label: 'when most South Tulsa slab homes were built' },
    zips: [
      { code: '74133', note: 'The heart of South Tulsa, 71st to 101st between Sheridan and Memorial' },
      { code: '74136', note: 'West of the BA Expressway, including Southern Hills' },
      { code: '74137', note: 'South of 101st, toward the Creek Turnpike' },
      { code: '74135', note: 'Southern portions' },
      { code: '74145', note: 'Southern portions' },
    ],
    neighborhoods: ['Southern Hills', 'Tanglewood', 'Woodland Hills', 'Forest Ridge', 'Regency Park'],
    corridorNote: 'plus the corridors toward the Creek Turnpike',
    nearby: ['Bixby', 'Jenks', 'Broken Arrow', 'Brookside'],
    patterns: [
      { title: 'Slab leaks', text: 'The most common hidden damage in South Tulsa. Copper and CPVC lines buried in the slab fail as expansive clay soil swells after rain and contracts during drought, and water spreads under flooring for weeks before anyone notices.' },
      { title: 'AC condensate overflow', text: 'Attic air handlers produce gallons of condensation a day in July and August. One clogged drain line can stain a ceiling within hours and soak through the drywall in a day.' },
      { title: 'Hail and water heaters', text: 'The 71st, 81st, 91st and 101st Street corridors take neighborhood-wide hail in spring, and garage, closet and attic water heaters 15 to 25 years old are entering the failure window.' },
      { title: 'Mingo Creek drainage', text: 'Properties near Mingo Creek tributaries can take on storm runoff during stalled spring storms. Rising outside water is Category 3.' },
    ],
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=South+Tulsa,+Tulsa,+OK',
  },
  '/service-areas/west-tulsa': {
    variant: 'river',
    name: 'West Tulsa',
    eyebrow: 'West Tulsa at a glance',
    heading: 'West of the Arkansas River, shaped by the 2019 flood',
    lede: "West Tulsa sits on the Arkansas River's west bank and in May to June 2019, that geography put floodwater in homes and businesses that had never taken on water before. But flooding is only part of the picture. Red Fork and the Westside hold some of the oldest residential construction in the city: 1920s to 1960s homes with galvanized pipes, cast-iron drains, crawlspaces and sewer laterals that back up when the system overloads during storms.",
    stat: { value: '2019', label: 'the May to June flood, Keystone Dam releases, river levels not seen since 1986' },
    floodYears: [
      { year: '1984', note: 'River flood reached West Tulsa' },
      { year: '1986', note: 'Last comparable river levels before 2019' },
      { year: '2019', note: 'Keystone Dam releases, Category 3 water in homes and businesses' },
    ],
    floodNote: 'The 1984, 1986 and 2019 floods all affected West Tulsa, making it one of the most flood-exposed areas in the Tulsa metro.',
    zips: [
      { code: '74107', note: 'Red Fork, the Westside, and neighborhoods west of the Arkansas River' },
      { code: '74127', note: 'Garden City, the Southwest Boulevard corridor, toward Sand Springs' },
    ],
    neighborhoods: ['Red Fork', 'Westside', 'Garden City'],
    corridorNote: 'plus the Southwest Boulevard corridor',
    nearby: ['Sand Springs', 'Sapulpa', 'Jenks'],
    patterns: [
      { title: 'Arkansas River flooding', text: 'Low-lying properties along the river corridor took on Category 3 floodwater in 2019. Every porous material it contacts must be removed, not dried.' },
      { title: 'Sewer backup', text: 'Mid-20th-century sewer infrastructure overloads during heavy rain and river flooding, backing sewage up through floor drains and ground-level toilets.' },
      { title: '1920s to 1960s homes', text: 'Galvanized supply lines corrode from the inside, cast-iron drains crack from root intrusion, and plaster walls hold water far longer than drywall.' },
      { title: 'Mold after the flood', text: 'Homes flooded in 2019 that were never dried to measured targets can still harbor mold inside wall cavities and crawlspaces years later.' },
    ],
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=West+Tulsa,+Tulsa,+OK',
  },
  '/service-areas/north-tulsa': {
    variant: 'oldest',
    name: 'North Tulsa',
    eyebrow: 'North Tulsa at a glance',
    heading: "The city's oldest housing stock, and the leaks that hide in it",
    lede: "North Tulsa has some of the city's oldest housing stock: 1920s to 1950s homes with original galvanized supply lines, cast-iron sewer laterals under decades-old trees, plaster walls, crawlspaces over damp clay, and plumbing that has been in service for 70 to 100 years. Water damage here often starts small and stays hidden: a slow drip inside a plaster wall, a crawlspace that has been damp for years, a sewer lateral narrowing from root intrusion for a decade.",
    stat: { value: '70 to 100 years', label: 'how long North Tulsa plumbing has been in service' },
    zips: [
      { code: '74106', note: 'Greenwood, the North Peoria corridor' },
      { code: '74110', note: "Kendall-Whittier's northern edge, Dawson" },
      { code: '74126', note: 'Owen Park, the North Lewis corridor' },
      { code: '74130', note: 'Northern residential areas' },
      { code: '74127', note: 'Areas north of the river corridor' },
    ],
    neighborhoods: ['Greenwood', 'Owen Park', 'Dawson', 'Kendall-Whittier'],
    corridorNote: 'plus the North Peoria and North Lewis corridors',
    nearby: ['Owasso', 'Skiatook', 'Midtown'],
    patterns: [
      { title: 'Aging galvanized supply lines', text: 'Galvanized steel corrodes from the inside over decades until it fails at a joint, often inside a plaster wall where the leak runs for days or weeks before a stain appears.' },
      { title: 'Root-cracked sewer laterals', text: 'Mature tree roots grow into clay and cast-iron laterals, narrowing the pipe until a partial blockage becomes a full Category 3 backup through floor drains and low toilets.' },
      { title: 'Crawlspace moisture and mold', text: 'Pier-and-beam homes sit over crawlspaces where clay soil holds moisture year-round. Without a vapor barrier, ground moisture grows mold on structural wood silently, often for years.' },
      { title: 'Bird Creek flooding', text: 'Low-lying areas near Bird Creek tributaries can flood during stalled spring storms. Rising outside water is Category 3 and needs NFIP flood coverage.' },
    ],
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=North+Tulsa,+Tulsa,+OK',
  },
  '/service-areas/east-tulsa': {
    variant: 'base',
    name: 'East Tulsa',
    eyebrow: 'East Tulsa at a glance',
    heading: 'The widest mix of homes in Tulsa, and our home base',
    lede: "East Tulsa runs from 1950s ranch homes off Admiral and 11th Street to 1980s slab neighborhoods near 61st, plus warehouses, shops and light-industrial buildings along the Memorial and Sheridan corridors. That mix means every kind of water damage shows up here: galvanized pipe failures in ranch homes, slab leaks in 1970s to 1980s construction, overnight appliance floods, commercial roof leaks over inventory, and Mingo Creek drainage that overflows during stalled spring storms.",
    stat: { value: '1950s to 1980s', label: 'the housing eras East Tulsa spans, the widest range in the metro' },
    baseNote: 'Our base at 400 S 129th E Ave sits in East Tulsa, making East Tulsa our closest service area with the shortest response times.',
    eras: [
      { era: '1950s ranch', note: 'Admiral and 11th Street' },
      { era: '1970s to 1980s slab', note: 'Slab neighborhoods near 61st' },
      { era: 'Warehouses and shops', note: 'Memorial and Sheridan corridors' },
    ],
    zips: [
      { code: '74112', note: 'Admiral Place area, older ranch neighborhoods' },
      { code: '74115', note: 'North of Admiral, including Mohawk Park area' },
      { code: '74116', note: 'Northeast East Tulsa' },
      { code: '74128', note: 'East toward Catoosa' },
      { code: '74129', note: 'Central East Tulsa, the 31st to 51st Street corridor' },
      { code: '74134', note: 'South of 51st along Memorial' },
      { code: '74145', note: '51st to 71st between Sheridan and Memorial' },
      { code: '74146', note: 'East of Memorial, toward Broken Arrow line' },
    ],
    neighborhoods: ['Admiral Place', 'Mohawk Park'],
    corridorNote: 'plus the 31st to 51st Street corridor and the Memorial and Sheridan corridors',
    nearby: ['Broken Arrow', 'Catoosa', 'South Tulsa', 'Midtown'],
    patterns: [
      { title: '1950s ranch plumbing', text: 'Galvanized supply lines and cast-iron drains fail inside walls, and plaster walls, original hardwood and pier-and-beam crawlspaces need longer, material-specific drying.' },
      { title: 'Slab leaks, 1970s to 1980s', text: 'Copper lines buried in concrete have been stressed by expansive clay soil for 40 to 50 years. These homes are now well past the failure window for buried supply lines.' },
      { title: 'Appliance and water heater failures', text: 'Water heaters, washing machine hoses and refrigerator ice-maker lines in homes 15 to 30 or more years old fail with increasing frequency, almost always overnight.' },
      { title: 'Mingo Creek and flat commercial roofs', text: 'Low-lying areas near Mingo Creek take on storm runoff in the 51st to 71st Street corridors, and flat roofs on warehouses and shops along Admiral, Memorial and Sheridan pond water and take hail.' },
    ],
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=East+Tulsa,+Tulsa,+OK',
  },
};

/* Resource pages, in doc order. The /resources/ hub lists all ten, so no
   resource page is an orphan: /resources/water-damage-vs-flood-damage-
   insurance-oklahoma has zero inbound body links in the doc; the other nine
   are linked from body copy (several via the parser's remapped paths).
   Footer chrome (header/footer links are exempt from the doc-only link
   rule) links only the hub, not the individual pages. */
export const RESOURCE_SLUGS = [
  '/resources/water-damage-restoration-cost-tulsa',
  '/resources/mold-after-water-damage-tulsa',
  '/resources/how-to-file-water-damage-insurance-claim-tulsa',
  '/resources/first-24-hours-after-water-damage',
  '/resources/oklahoma-water-damage-insurance-guide',
  '/resources/how-long-does-water-damage-take-to-dry',
  '/resources/how-to-prevent-frozen-pipes-tulsa',
  '/resources/water-damage-vs-flood-damage-insurance-oklahoma',
  '/resources/water-damage-categories-and-classes-explained',
  '/resources/signs-of-hidden-water-damage',
];

/* Trust-band checks — verbatim fragments from the homepage doc text. */
export const TRUST_CHECKS = [
  'Crews Standing By 24/7',
  'IICRC S500 Drying Standards',
  'Readings Logged Daily',
  'Insurance Claim Documentation',
];

export function areaMapQuery(slug) {
  const seg = slug.replace(/\/$/, '').split('/').pop() || '';
  const tulsaHoods = ['midtown', 'brookside', 'south', 'west', 'north', 'east', 'cherry-street'];
  const base = seg.replace(/-ok$/, '').replace(/-tulsa$/, '').replace(/-/g, ' ');
  const name = base.replace(/\b\w/g, (c) => c.toUpperCase());
  if (tulsaHoods.includes(seg.replace(/-tulsa$/, ''))) return `${name}, Tulsa, OK`;
  return `${name}, OK`;
}
