'use client';
import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { SITE, SERVICE_GROUPS, AREA_GROUPS } from '../lib-meta';

export default function Header() {
  const navRef = useRef(null);
  useEffect(() => {
    const root = navRef.current;
    if (!root) return;
    const onToggle = (e) => {
      if (e.target.tagName !== 'DETAILS' || !e.target.open) return;
      root.querySelectorAll('details[open]').forEach((d) => {
        if (d !== e.target) d.removeAttribute('open');
      });
    };
    root.addEventListener('toggle', onToggle, true);
    const onKey = (e) => {
      if (e.key === 'Escape') root.querySelectorAll('details[open]').forEach((d) => d.removeAttribute('open'));
    };
    document.addEventListener('keydown', onKey);
    return () => {
      root.removeEventListener('toggle', onToggle, true);
      document.removeEventListener('keydown', onKey);
    };
  }, []);

  return (
    <header className="site-header">
      <div className="container" ref={navRef}>
        <Link className="brand" href="/" aria-label="Tulsa Water Damage Repair — home">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" aria-hidden="true">
              <path
                d="M12 2.5c0 0-6.5 7.6-6.5 12a6.5 6.5 0 0 0 13 0c0-4.4-6.5-12-6.5-12Z"
                fill="#00BFFF"
              />
              <circle cx="9.4" cy="15.2" r="1.7" fill="#fff" />
            </svg>
          </span>
          <span>
            Tulsa Water Damage Repair
            <small>Tulsa, Oklahoma</small>
          </span>
        </Link>
        <nav className="main-nav" aria-label="Main">
          <Link href="/">Home</Link>
          <details>
            <summary>Services ▾</summary>
            <div className="nav-drop">
              {SERVICE_GROUPS.map((g) => (
                <div key={g.label}>
                  <p className="drop-group">{g.label}</p>
                  {g.slugs.map((s) => (
                    <Link key={s} href={s}>
                      {shortFor(s)}
                    </Link>
                  ))}
                </div>
              ))}
              <p className="drop-group">All Services</p>
              <Link href="/services/">View every service →</Link>
            </div>
          </details>
          <details>
            <summary>Service Areas ▾</summary>
            <div className="nav-drop">
              {AREA_GROUPS.map((g) => (
                <div key={g.label}>
                  <p className="drop-group">{g.label}</p>
                  {g.slugs.map((s) => (
                    <Link key={s} href={s}>
                      {shortFor(s)}
                    </Link>
                  ))}
                </div>
              ))}
            </div>
          </details>
          <Link href="/about-us/">About Us</Link>
          <Link href="/resources/">Blog</Link>
          <Link href="/contact/">Contact</Link>
        </nav>
        <a className="btn btn-cyan header-cta" href={SITE.phoneHref}>
          <span className="btn-small">Emergency?</span>
          {SITE.phone}
        </a>
        <div className="mobile-head">
          <a className="btn btn-cyan" href={SITE.phoneHref} aria-label={`Call ${SITE.phone}`}>
            ☎
          </a>
          <details>
            <summary className="btn btn-cream" aria-label="Open menu">
              ☰ Menu
            </summary>
            <div className="mobile-menu">
              <Link href="/">Home</Link>
              {SERVICE_GROUPS.map((g) => (
                <div key={g.label}>
                  <p className="drop-group">{g.label}</p>
                  {g.slugs.map((s) => (
                    <Link key={s} href={s}>
                      {shortFor(s)}
                    </Link>
                  ))}
                </div>
              ))}
              <p className="drop-group">Service Areas</p>
              {AREA_GROUPS.flatMap((g) => g.slugs).map((s) => (
                <Link key={s} href={s}>
                  {shortFor(s)}
                </Link>
              ))}
              <Link href="/about-us/">About Us</Link>
              <Link href="/resources/">Blog</Link>
              <Link href="/contact/">Contact</Link>
              <a className="btn btn-cyan" href={SITE.phoneHref}>
                Call Now · {SITE.phone}
              </a>
            </div>
          </details>
        </div>
      </div>
    </header>
  );
}

function shortFor(slug) {
  const last = slug.replace(/\/$/, '').split('/').pop() || '';
  return last
    .replace(/-ok$/, '')
    .replace(/-tulsa$/, '')
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
