#!/usr/bin/env node
/**
 * Post-export VERIFICATION (no-slash URL form, 2026-11-08 round).
 *
 * With trailingSlash:false Next.js exports every route natively as a flat
 * <path>.html file (only '/' exports as index.html). There is nothing left
 * to copy — the old copy step (trailingSlash:true era) would now FAIL
 * because no <path>/index.html files exist for no-slash routes.
 *
 * This script therefore VERIFIES the export instead of copying:
 *  - every no-slash route in content/pages.json has its flat <path>.html
 *  - '/' has out/index.html
 *  - NO <path>/index.html exists for any flipped (no-slash) route — a
 *    stray index.html would let the slash form serve 200 alongside the
 *    no-slash canonical (duplicate content / crawl waste).
 * Fails the build (exit 1) if any check fails, so `npm run export` still
 * gates on the URL form.
 */
const fs = require('fs');
const path = require('path');

const pages = require('../content/pages.json');
const out = path.join(__dirname, '..', 'out');
let flat = 0;
let errors = 0;
for (const p of pages) {
  if (p.slug === '/') {
    const indexFile = path.join(out, 'index.html');
    if (!fs.existsSync(indexFile)) {
      console.error('MISSING index.html for homepage /');
      errors++;
    }
    continue;
  }
  const flatFile = path.join(out, p.slug.replace(/^\//, '') + '.html');
  const dirIndex = path.join(out, p.slug.replace(/^\//, ''), 'index.html');
  if (!fs.existsSync(flatFile)) {
    console.error('MISSING flat .html for', p.slug);
    errors++;
  } else {
    flat++;
  }
  if (fs.existsSync(dirIndex)) {
    console.error('STRAY index.html for no-slash route', p.slug, '(slash form would also serve 200)');
    errors++;
  }
}
if (errors > 0) {
  console.error(`post-export verification FAILED: ${errors} error(s)`);
  process.exit(1);
}
console.log(`post-export: verified ${flat} flat .html files + homepage index.html, 0 stray index.html`);
