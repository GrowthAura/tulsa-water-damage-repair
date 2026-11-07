'use client';
import { useEffect } from 'react';

/* Tier 1 reveal: CSS transitions + IntersectionObserver. Zero WebGL, no heavy JS.
   Mounted once in the root layout so it observes .reveal elements on EVERY
   page (cards, h2s, final CTA). Without this mount, .reveal elements stay at
   opacity:0 forever — that silently hid all homepage cards. */
export function Reveal({ children, className = '' }) {
  useEffect(() => {
    const els = document.querySelectorAll('.reveal:not(.in)');
    if (!('IntersectionObserver' in window)) {
      els.forEach((el) => el.classList.add('in'));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('in');
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' },
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, []);
  return <div className={className}>{children}</div>;
}
