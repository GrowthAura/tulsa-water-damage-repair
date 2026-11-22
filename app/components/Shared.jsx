import Link from 'next/link';
import { SITE, TRUST_CHECKS, normSlug, shortName, SERVICE_TITLES, AREA_IDENTITY } from '../lib-meta';
import { PAGE_BY_SLUG, pageImage } from '../lib';

export function TrustBand() {
  return (
    <section className="trust-band" aria-label="Why call us">
      <div className="container">
        <ul>
          {TRUST_CHECKS.map((c) => (
            <li key={c}>
              <span className="check" aria-hidden="true">✓</span>
              {c}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function CardMedia({ img, label }) {
  if (img) {
    return (
      <div className="card-media">
        <img src={img.file} alt={img.alt} width={800} height={450} loading="lazy" />
      </div>
    );
  }
  return (
    <div className="card-media">
      <div className="media-fallback">{label}</div>
    </div>
  );
}

export function ServiceCards({ slugs, heading, eyebrow }) {
  return (
    <section className="section" aria-label={heading || 'Our services'}>
      <div className="container">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        {heading && <h2>{heading}</h2>}
        <div className="cards">
          {slugs.map((slug) => {
            const p = PAGE_BY_SLUG[slug];
            if (!p) return null;
            const img = pageImage(slug).hero;
            return (
              <article className="card" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{shortName(slug)}</Link>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </h3>
                  <p>{p.blurb}</p>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* Doc grouped service lists (hub + homepage) as card grids.
   Each list item has exactly one /services/ link. On the hub the item has a
   <strong> service name: title = the <strong> text, description = the item's
   remaining text with link tags stripped (every word kept verbatim). On the
   homepage the whole item is one link with no <strong>: title = the doc's
   service name for that href (from the hub lists), description = the item's
   remaining text after that title. Link = the item's href.
   Image = that service's own hero image from the top card grid (reused);
   services with no hero image (sewage, slab-leak) get the branded panel.
   serviceListItems returns null for any other list shape, so plain lists
   (documentation, checklists) are never converted. */
function parseServiceItem(html) {
  const hrefs = [...html.matchAll(/href="([^"]+)"/g)].map((m) => m[1]);
  if (hrefs.length !== 1) return null;
  if (!hrefs[0].startsWith('/services/')) return null;
  const strong = html.match(/<strong>([\s\S]*?)<\/strong>/);
  if (strong) {
    const desc = html
      .replace(/<strong>[\s\S]*?<\/strong>/, '')
      .replace(/<\/?a[^>]*>/g, '')
      .trim();
    // titleHtml must NOT contain its own <a>: ServiceListCards wraps it in a
    // <Link>, and a nested <a> is invalid HTML (browsers split it into two
    // links to the same target — 120 duplicate card links sitewide).
    // Strip the anchor tags, keep the title words verbatim.
    return { href: hrefs[0], titleHtml: strong[1].replace(/<\/?a[^>]*>/g, ''), descHtml: desc };
  }
  // Homepage shape: the whole item is one link with no <strong> separator.
  // Title = the doc's service name for this href (from the hub's grouped
  // lists); description = the item's remaining text after that title.
  // Items that are just the service name get no description paragraph.
  const titleHtml = SERVICE_TITLES[hrefs[0]] || SERVICE_TITLES[normSlug(hrefs[0])];
  if (!titleHtml) return null;
  const text = html.replace(/<\/?a[^>]*>/g, '').trim();
  const desc = text.toLowerCase().startsWith(titleHtml.replace(/<[^>]*>/g, '').toLowerCase())
    ? text.slice(titleHtml.replace(/<[^>]*>/g, '').length).trim()
    : text;
  // SERVICE_TITLES values come from the hub's <strong> items and may contain
  // their own <a> — strip it here too (same nested-<a> blunder as the hub
  // branch above); the card's <Link> is the single link.
  return { href: hrefs[0], titleHtml: titleHtml.replace(/<\/?a[^>]*>/g, ''), descHtml: desc };
}

export function serviceListItems(items) {
  if (!Array.isArray(items) || items.length === 0) return null;
  const out = [];
  for (const it of items) {
    const parsed = parseServiceItem(it);
    if (!parsed) return null;
    out.push(parsed);
  }
  return out;
}

export function ServiceListCards({ items }) {
  return (
    <div className="cards">
      {items.map((it) => {
        const img = pageImage(it.href).hero || pageImage(normSlug(it.href)).hero;
        return (
          <article className="card" key={it.href}>
            <CardMedia img={img} label={it.titleHtml.replace(/<[^>]*>/g, '')} />
            <div className="card-body">
              <h3>
                <Link href={it.href} dangerouslySetInnerHTML={{ __html: it.titleHtml }} />
                <span className="card-arrow" aria-hidden="true">→</span>
              </h3>
              {it.descHtml && <p dangerouslySetInnerHTML={{ __html: it.descHtml }} />}
            </div>
          </article>
        );
      })}
    </div>
  );
}

export function ResourceCards({ slugs, heading, eyebrow }) {
  return (
    <section className="section section-mist resource-cards" aria-label={heading || 'Resources'}>
      <div className="container">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        {heading && <h2>{heading}</h2>}
        <div className="cards">
          {slugs.map((slug) => {
            const p = PAGE_BY_SLUG[slug];
            if (!p) return null;
            const img = pageImage(slug).hero;
            return (
              <article className="card" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{p.h1}</Link>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </h3>
                  <p>{p.blurb}</p>
                </div>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

export function AreaCards({ slugs, heading, eyebrow }) {
  /* Embedded inside the homepage content container (not a top-level section),
     so it renders as a rounded mist panel rather than a full-bleed section. */
  return (
    <section className="area-cards-panel" aria-label={heading || 'Service areas'}>
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      {heading && <h2>{heading}</h2>}
      <div className="cards">
          {slugs.map((slug) => {
            const p = PAGE_BY_SLUG[slug];
            if (!p) return null;
            const img = pageImage(slug).hero;
            return (
              <article className="card" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{shortName(slug)}</Link>
                    <span className="card-arrow" aria-hidden="true">→</span>
                  </h3>
                  <p>{p.blurb}</p>
                </div>
              </article>
            );
          })}
      </div>
    </section>
  );
}

export function FaqList({ faqs }) {
  if (!faqs || faqs.length === 0) return null;
  return (
    <div className="faq-list">
      {faqs.map((f, i) => (
        <details key={i}>
          <summary>
            <h3>{f.q}</h3>
            <span className="faq-toggle" aria-hidden="true">+</span>
          </summary>
          <div className="faq-answer" dangerouslySetInnerHTML={{ __html: f.a_html }} />
        </details>
      ))}
    </div>
  );
}

export function FinalCta() {
  return (
    <section className="final-cta" aria-label="Get help now">
      <div className="container">
        <div className="final-cta-card">
          <div className="accent-line on-navy">
            <p className="eyebrow on-navy" style={{ margin: 0 }}>
              Start with a clear assessment
            </p>
          </div>
          <h2>Water damage right now? Call {SITE.phone}</h2>
          <p>
            Every hour water sits, it spreads deeper into drywall, subfloor and framing. Call now
            and a dispatcher will give you a realistic arrival window for your address.
          </p>
          <div className="hero-ctas">
            <a className="btn btn-cyan" href={SITE.phoneHref}>
              Call Now · {SITE.phone}
            </a>
            <a className="btn btn-cream" href="/contact">
              Request Emergency Service
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

export function MapBlock({ query, title }) {
  return (
    <iframe
      className="map-frame"
      title={title || `Map · ${query}`}
      src={`https://www.google.com/maps?q=${encodeURIComponent(query)}&output=embed`}
      loading="lazy"
      referrerPolicy="no-referrer-when-downgrade"
    />
  );
}

/* Area identity (#4, follow-up 2026-11-23): one bespoke "at a glance"
   section per directional area page (South / West / North / East Tulsa
   only). Each variant has its own layout and emphasis, drawn from that
   area's own doc content. South leads with slab + attic AC, West with
   the 2019 river flood, North with 1920s to 1950s housing age, East with
   the widest housing-era mix and the business base. Renders nothing for
   any other slug. No links except the verified Google Maps link + phone. */
function IdentityFooter({ d, mapsBtn, showCall = true }) {
  return (
    <div className="ai-foot">
      <a className={`btn ${mapsBtn || 'btn-outline'}`} href={d.mapsUrl} target="_blank" rel="noopener">
        See {d.name} on Google Maps
        <span aria-hidden="true">↗</span>
      </a>
      {showCall && (
        <a className="btn btn-cyan" href={SITE.phoneHref}>
          Call Now · {SITE.phone}
        </a>
      )}
    </div>
  );
}

function HoodLine({ d }) {
  return (
    <div className="ai-hoods-block">
      <p className="ai-hoods-label">Neighborhoods</p>
      <ul className="ai-hoods">
        {d.neighborhoods.map((n) => (
          <li key={n}>{n}</li>
        ))}
      </ul>
      {d.corridorNote && <p className="ai-corridor">{d.corridorNote}</p>}
      <p className="ai-nearby">Nearby: {d.nearby.join(', ')}</p>
    </div>
  );
}

function AreaIdentitySouth({ d }) {
  return (
    <section className="section area-identity area-identity--slab" aria-label={`${d.name} at a glance`}>
      <div className="container">
        <div className="ai-head">
          <div>
            <p className="eyebrow">{d.eyebrow}</p>
            <h2>{d.heading}</h2>
          </div>
          <p className="ai-stat">
            <span className="ai-stat-value">{d.stat.value}</span>
            <span className="ai-stat-label">{d.stat.label}</span>
          </p>
        </div>
        <p className="ai-lede">{d.lede}</p>
        <div className="ai-zip-band">
          <p className="ai-zip-label">ZIP codes we cover in {d.name}</p>
          <ul className="ai-zips ai-zips--row">
            {d.zips.map((z) => (
              <li key={z.code}>
                <strong>{z.code}</strong>
                <span>{z.note}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="ai-split">
          <div>
            <h3 className="ai-subhead">What goes wrong here most</h3>
            <ol className="ai-patterns ai-patterns--numbered">
              {d.patterns.map((p, i) => (
                <li key={p.title}>
                  <span className="ai-num" aria-hidden="true">{String(i + 1).padStart(2, '0')}</span>
                  <div>
                    <strong>{p.title}</strong>
                    <span>{p.text}</span>
                  </div>
                </li>
              ))}
            </ol>
          </div>
          <aside className="ai-hood-panel">
            <HoodLine d={d} />
          </aside>
        </div>
        <IdentityFooter d={d} />
      </div>
    </section>
  );
}

function AreaIdentityWest({ d }) {
  return (
    <section className="section section-navy area-identity area-identity--river" aria-label={`${d.name} at a glance`}>
      <div className="container">
        <p className="eyebrow on-navy">{d.eyebrow}</p>
        <h2>{d.heading}</h2>
        <p className="ai-lede on-navy">{d.lede}</p>
        <div className="ai-timeline">
          {d.floodYears.map((f) => (
            <div className="ai-year" key={f.year}>
              <span className="ai-year-value">{f.year}</span>
              <span className="ai-year-note">{f.note}</span>
            </div>
          ))}
        </div>
        <p className="ai-flood-note">{d.floodNote}</p>
        <div className="ai-split ai-split--river">
          <div>
            <h3 className="ai-subhead on-navy">ZIP codes we cover in {d.name}</h3>
            <ul className="ai-zip-cards">
              {d.zips.map((z) => (
                <li key={z.code}>
                  <strong>{z.code}</strong>
                  <span>{z.note}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="ai-subhead on-navy">What goes wrong here most</h3>
            <ul className="ai-patterns ai-patterns--plain">
              {d.patterns.map((p) => (
                <li key={p.title}>
                  <strong>{p.title}</strong>
                  <span>{p.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        <HoodLine d={d} />
        <IdentityFooter d={d} mapsBtn="btn-cream" />
      </div>
    </section>
  );
}

function AreaIdentityNorth({ d }) {
  return (
    <section className="section section-mist area-identity area-identity--oldest" aria-label={`${d.name} at a glance`}>
      <div className="container">
        <p className="ai-age-banner">
          <span className="ai-age-value">{d.stat.value}</span>
          <span className="ai-age-label">{d.stat.label}</span>
        </p>
        <p className="eyebrow">{d.eyebrow}</p>
        <h2>{d.heading}</h2>
        <p className="ai-lede">{d.lede}</p>
        <div className="ai-split">
          <div>
            <h3 className="ai-subhead">What goes wrong here most</h3>
            <ul className="ai-pattern-cards">
              {d.patterns.map((p) => (
                <li key={p.title}>
                  <strong>{p.title}</strong>
                  <span>{p.text}</span>
                </li>
              ))}
            </ul>
          </div>
          <aside className="ai-zip-card">
            <h3 className="ai-subhead">ZIP codes we cover in {d.name}</h3>
            <dl className="ai-zip-list">
              {d.zips.map((z) => (
                <div key={z.code}>
                  <dt>{z.code}</dt>
                  <dd>{z.note}</dd>
                </div>
              ))}
            </dl>
          </aside>
        </div>
        <HoodLine d={d} />
        <IdentityFooter d={d} />
      </div>
    </section>
  );
}

function AreaIdentityEast({ d }) {
  return (
    <section className="section area-identity area-identity--base" aria-label={`${d.name} at a glance`}>
      <div className="container">
        <div className="ai-base-banner">
          <p className="ai-base-kicker">Our base is here</p>
          <p className="ai-base-address">{SITE.address}</p>
          <p className="ai-base-note">{d.baseNote}</p>
          <a className="btn btn-cyan" href={SITE.phoneHref}>
            Call Now · {SITE.phone}
          </a>
        </div>
        <p className="eyebrow">{d.eyebrow}</p>
        <h2>{d.heading}</h2>
        <p className="ai-lede">{d.lede}</p>
        <div className="ai-eras">
          {d.eras.map((e, i) => (
            <div className="ai-era" key={e.era}>
              <span className="ai-era-step" aria-hidden="true">{i + 1}</span>
              <strong>{e.era}</strong>
              <span>{e.note}</span>
            </div>
          ))}
        </div>
        <h3 className="ai-subhead">ZIP codes we cover in {d.name}</h3>
        <ul className="ai-zips ai-zips--grid">
          {d.zips.map((z) => (
            <li key={z.code}>
              <strong>{z.code}</strong>
              <span>{z.note}</span>
            </li>
          ))}
        </ul>
        <h3 className="ai-subhead">What goes wrong here most</h3>
        <ul className="ai-pattern-cards">
          {d.patterns.map((p) => (
            <li key={p.title}>
              <strong>{p.title}</strong>
              <span>{p.text}</span>
            </li>
          ))}
        </ul>
        <HoodLine d={d} />
        <IdentityFooter d={d} showCall={false} />
      </div>
    </section>
  );
}

export function AreaIdentity({ slug }) {
  const d = AREA_IDENTITY[slug];
  if (!d) return null;
  if (d.variant === 'river') return <AreaIdentityWest d={d} />;
  if (d.variant === 'oldest') return <AreaIdentityNorth d={d} />;
  if (d.variant === 'base') return <AreaIdentityEast d={d} />;
  return <AreaIdentitySouth d={d} />;
}

/* About links (#6, follow-up 2026-11-23): authority citations at the bottom
   of the About page ONLY. Local + industry authorities, every URL verified
   live 2026-11-23 (all HTTP 200; BBB is a search page, clearly labeled —
   this business has no BBB profile page and none is implied). NO social
   links: the business has no social profiles yet, so none are listed.
   Wording is neutral: no membership, award, year, or review claims. */
const ABOUT_AUTHORITIES = [
  {
    name: 'Tulsa Regional Chamber of Commerce',
    url: 'https://tulsachamber.com/',
    desc: 'The Tulsa business community and the metro economy this site serves.',
  },
  {
    name: 'City of Tulsa',
    url: 'https://www.cityoftulsa.org/',
    desc: 'City services, permits, and local government for Tulsa residents.',
  },
  {
    name: 'IICRC',
    url: 'https://www.iicrc.org/',
    desc: 'The inspection, cleaning, and restoration industry body behind the S500 water damage and S520 mold standards this site follows.',
  },
  {
    name: 'FEMA Flood Map Service Center',
    url: 'https://msc.fema.gov/portal/home',
    desc: 'Check any Tulsa address against the official flood map. The flood guides on this site point here.',
  },
  {
    name: 'U.S. EPA: Mold',
    url: 'https://www.epa.gov/mold',
    desc: 'The EPA mold guidance behind the 24 to 48 hour drying window the mold guides cite.',
  },
  {
    name: 'FloodSmart: National Flood Insurance Program',
    url: 'https://www.floodsmart.gov/',
    desc: 'The federal flood insurance program, including the 30 day waiting period the insurance guides explain.',
  },
  {
    name: 'Better Business Bureau: Tulsa water damage restoration search',
    url: 'https://www.bbb.org/search?find_text=Water%20Damage%20Restoration&find_loc=Tulsa%2C%20OK',
    desc: 'BBB listings for water damage restoration businesses in Tulsa.',
  },
];

export function AboutLinks() {
  return (
    <section className="section section-mist about-links" aria-label="Sources and authorities">
      <div className="container">
        <p className="eyebrow">Sources and authorities</p>
        <h2>Why you can trust this local content</h2>
        <p className="about-links-lede">
          This site is written for Tulsa homes and Tulsa conditions. The pages below are the public sources the content follows and checks against: the local chamber and the City of Tulsa, the restoration industry standard, and the federal flood and mold guidance the insurance guides cite.
        </p>
        <ul className="about-links-grid">
          {ABOUT_AUTHORITIES.map((a) => (
            <li key={a.url} className="about-link-card">
              <a href={a.url} target="_blank" rel="noopener">
                {a.name}
                <span aria-hidden="true">↗</span>
              </a>
              <p>{a.desc}</p>
            </li>
          ))}
        </ul>
        <p className="about-links-note">
          This business has no social media profiles yet, so none are listed here.
        </p>
      </div>
    </section>
  );
}
