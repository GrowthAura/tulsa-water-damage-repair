import Link from 'next/link';
import { SITE, FOOTER_SERVICES, FOOTER_AREAS, shortName } from '../lib-meta';

export default function Footer({ showMap = true }) {
  return (
    <footer className="site-footer">
      {showMap && (
        <div className="footer-map">
          <iframe
            title={`Map — ${SITE.address}`}
            src={`https://www.google.com/maps?q=${encodeURIComponent(SITE.mapQuery)}&output=embed`}
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
      )}
      <div className="container">
        <div className="footer-cols">
          <div className="footer-col">
            <h3>Tulsa Water Damage Repair</h3>
            <p>
              Water damage restoration across Tulsa County, day or night. We extract water, dry the
              structure to measured targets and document everything for your insurance claim.
            </p>
            <p className="footer-hours">Crews Standing By 24/7</p>
            <p>
              <strong>{SITE.address}</strong>
              <br />
              <a href={SITE.phoneHref}>{SITE.phone}</a>
            </p>
          </div>
          <div className="footer-col">
            <h3>Services</h3>
            <ul>
              {FOOTER_SERVICES.map((s) => (
                <li key={s}>
                  <Link href={s}>{shortName(s)}</Link>
                </li>
              ))}
              <li>
                <Link href="/services/" className="footer-more">
                  View all services
                </Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h3>Service Area</h3>
            <p>Serving Tulsa, Oklahoma &amp; surrounding areas.</p>
            <ul>
              {FOOTER_AREAS.map((s) => (
                <li key={s}>
                  <Link href={s}>{shortName(s)}</Link>
                </li>
              ))}
              <li>
                <Link href="/#which-tulsa-areas-do-you-serve" className="footer-more">
                  View all areas
                </Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h3>Resources</h3>
            <p>Guides and cost information from Tulsa Water Damage Repair.</p>
            <ul>
              <li>
                <Link href="/resources/" className="footer-more">
                  Blog
                </Link>
              </li>
            </ul>
            {showMap && (
              <div className="footer-mini-map">
                <iframe
                  title={`Map — ${SITE.address}`}
                  src={`https://www.google.com/maps?q=${encodeURIComponent(SITE.mapQuery)}&output=embed`}
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                />
              </div>
            )}
          </div>
          <div className="footer-col">
            <h3>Emergency Help</h3>
            <p>Speak with Tulsa Water Damage Repair about your restoration needs.</p>
            <a className="btn btn-cyan" href={SITE.phoneHref}>
              <span>Call Now ·</span>
              <span>{SITE.phone}</span>
            </a>
            <br />
            <a className="btn btn-cream" href="/contact/">
              Request Emergency Service
            </a>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} Tulsa Water Damage Repair</span>
          <span>
            <Link href="/about-us/">About Us</Link>
            {' · '}
            <Link href="/resources/">Blog</Link>
            {' · '}
            <Link href="/contact/">Contact</Link>
            {' · '}
            {/* Plain <a>: /sitemap.xml is a static file, not a Next route — a
                next/link here makes the router prefetch /sitemap.xml.txt (RSC)
                and log a console 404. */}
            <a href="/sitemap.xml">Sitemap</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
