'use client';
import { useEffect } from 'react';

/* Tier 1 reveal: CSS transitions + IntersectionObserver. Zero WebGL, no heavy JS.
   Mounted once in the root layout so it observes .reveal elements on EVERY
   page (cards, final CTA). Without this mount, .reveal elements stay at
   opacity:0 forever — that silently hid all homepage cards.
   Belt-and-braces: a 900ms safety timer reveals anything still hidden, so
   content can never stay invisible if the observer fails or never fires
   (the San Bruno trap: a whole article in one .reveal div never got .in). */
export function Reveal({ children, className = '' }) {
  useEffect(() => {
    const revealAll = () => {
      document.querySelectorAll('.reveal:not(.in)').forEach((el) => el.classList.add('in'));
    };
    const els = document.querySelectorAll('.reveal:not(.in)');
    if (!('IntersectionObserver' in window)) {
      revealAll();
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
    // Safety timer: if the observer never fires for an element, reveal it
    // anyway after 900ms so content is never stuck invisible.
    const timer = setTimeout(revealAll, 900);
    return () => {
      io.disconnect();
      clearTimeout(timer);
    };
  }, []);
  return <div className={className}>{children}</div>;
}
