import Link from 'next/link';
import { SITE, TRUST_CHECKS, normSlug, shortName, SERVICE_TITLES } from '../lib-meta';
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
              <article className="card reveal" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{shortName(slug)}</Link>
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
          <article className="card reveal" key={it.href}>
            <CardMedia img={img} label={it.titleHtml.replace(/<[^>]*>/g, '')} />
            <div className="card-body">
              <h3>
                <Link href={it.href} dangerouslySetInnerHTML={{ __html: it.titleHtml }} />
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
    <section className="section resource-cards" aria-label={heading || 'Resources'}>
      <div className="container">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        {heading && <h2>{heading}</h2>}
        <div className="cards">
          {slugs.map((slug) => {
            const p = PAGE_BY_SLUG[slug];
            if (!p) return null;
            const img = pageImage(slug).hero;
            return (
              <article className="card reveal" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{p.h1}</Link>
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
  return (
    <section className="section" aria-label={heading || 'Service areas'}>
      <div className="container">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        {heading && <h2>{heading}</h2>}
        <div className="cards">
          {slugs.map((slug) => {
            const p = PAGE_BY_SLUG[slug];
            if (!p) return null;
            const img = pageImage(slug).hero;
            return (
              <article className="card reveal" key={slug}>
                <CardMedia img={img} label={shortName(slug)} />
                <div className="card-body">
                  <h3>
                    <Link href={slug}>{shortName(slug)}</Link>
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
        <div className="final-cta-card reveal">
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
            <a className="btn btn-cream" href="/contact/">
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
      title={title || `Map — ${query}`}
      src={`https://www.google.com/maps?q=${encodeURIComponent(query)}&output=embed`}
      loading="lazy"
      referrerPolicy="no-referrer-when-downgrade"
    />
  );
}
