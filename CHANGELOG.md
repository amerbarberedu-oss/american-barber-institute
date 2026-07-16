# Changelog — American Barber Institute (americanbarberinstitute.com)

All notable changes to this site are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versions stay in
the **0.x** range throughout the upgrade cycle; the move to **1.0.0** happens only
when the client approves the official production release.

## [0.4.0] — 2026-07-16
Nav/hero/header redesign parity across the whole site, a critical contrast bug
fix, and a full-site audit (cleanup, SEO/AEO, performance, responsive QA).

### Fixed — critical
- **Sitewide dark-section contrast bug.** `editorial.min.css`'s minifier was
  stripping the descendant-combinator space before every `:is(...)` selector
  (e.g. `.band--petrol .ed-card :is(h3,h4)` → broken `...ed-card:is(h3,h4)`),
  silently breaking ~22 selectors and dropping text contrast to ~1.1:1 on dark
  sections sitewide. Fixed; verified 7–16:1 across sampled pages.
- **Spanish structured data was English on 70 of 72 `/spanish/` pages.**
  `src/build.py` built one `schema_tags` string from the English title/body and
  reused it verbatim for the Spanish twin — FAQPage answers, BreadcrumbList
  name/URL, and the Organization `description`/`slogan` were all English on a
  Spanish page. Now builds a separate ES schema from the Spanish
  title/canonical/body (the real translated body when one exists), with a new
  `ORG_SCHEMA_ES` constant for the org description/slogan.
- **Mobile hero was buried ~1200px below the fold on Bronx + all 4 landing
  pages.** They used a fixed `min-height:1220px` for the mobile hero photo box
  instead of the homepage's `aspect-ratio:872/1804`, pushing the entire
  headline/CTA/countdown off the first screen.
- **Bronx + all 4 landing pages were running the homepage's superseded "v4"
  hero design** (own code comment literally said so) while the homepage had
  moved to "v5": gapped grid + rounded photo card + top-anchored copy + dark
  gradient overlay + 900px breakpoint, instead of v5's no-gap full-bleed photo,
  bottom-anchored copy, no gradient, bordered countdown cells, and 1000px
  breakpoint. Rebuilt to match, keeping only campus copy/photo-crop/accent-color
  as legitimate differences.
- Landing-page header unified into one responsive component (`.hdr2`, see
  Design system below) instead of two always-stacked rows; removed the
  "$150/week" promo strip and "LIMITED SEATS AVAILABLE" banner per client
  request.
- Spanish landing pages: hero feature-chip text overflowed the viewport on
  mobile (a classic flexbox/grid `min-width:auto` bug — longer Spanish labels
  couldn't shrink/wrap inside their grid column). Fixed with `min-width:0`.
- Sticky mobile CTA bar and the fixed to-top button covered the last line(s) of
  footer text on mobile/tablet; footer now reserves space for them.
- Sticky 3-button CTA bar overflowed by ~10px at exactly 360px viewport width
  (same `min-width:auto` grid-item issue as above).
- 35 English pages had visible, well-formatted FAQ accordions with **no**
  `FAQPage` schema (19 other pages on the site already paired the same content
  pattern with schema correctly) — added across the flagship program page, all
  11 blog posts, and 23 other pages. `faq_schema_from()` extended to support
  both markup patterns used site-wide (`<div class="a">` wrapper and bare `<p>`
  after `</summary>`) so no page silently got an empty/invalid FAQPage block.
- Removed the Fraunces Google Fonts request (7 weight/style variants, loaded
  on every single page): confirmed unused anywhere on the live site — a later
  CSS file overrides `--font-display` to Inter Tight, and that override was
  never reverted after Fraunces was originally wired in. Added weight 900 to
  the Inter request to cover the site's existing `font-weight:900` usage that
  Fraunces had been (invisibly) supplying.
- `.display`/`.display--xl` (the H1/H2 heading system used on ~200 guide/blog/
  pillar pages) reduced from up to 4.6–4.8rem down to 3.1–3.5rem — H2 section
  headers were rendering almost as large as the page H1.
- Bronx page's `<title>` trimmed from 94 characters (will truncate in SERPs)
  to 63.

### Removed (dead code)
- 4 unreferenced images (~924KB): superseded pre-v2 hero photos and an orphaned
  webp variant.
- ~550 lines of dead CSS across `funnels.css`/`landing.css`: three successive
  generations of superseded landing-page header/hero/countdown/promo/seats
  components (`.lfx-*`, `.lf-topbar`/`.lf-hdr`/`.lf-brand`/`.lf-phone`/
  `.lf-lang`/`.lf-hero`/`.lf-cd`/`.lf-form`/`.lf-pills`, `.hair-*`), a dead
  "monogram avatar" instructors-page module (`.inst-avatar*`), `.site-seats*`,
  `.hair-call-btn`, `.hx-featbox`, `.inst-photo`. Each confirmed via HTML *and*
  JS grep (some classes are only ever applied at runtime by `funnels.js`) before
  removal, not by static search alone. **Not fully exhaustive** — a large dead
  "v1 splash-page" module (`.inst-*` continues beyond what's listed above,
  `.lf-form`/`.lf-stats` neighbors) remains in `landing.css`, confirmed dead but
  deferred to a dedicated cleanup pass since it's interleaved with live rules
  rather than cleanly contiguous.
- 3 fully-merged, no-longer-needed git branches
  (`preview/mass-rollout-2026-07-14`, `preview/spanish-translation-2026-07-14`,
  `countdown-perpetual-fix-2026-07-14`).

### Changed
- Cache-bust versions bumped for every touched asset, in the same commit as
  both generators' own templates/constants (the "sed the pages but not the
  TEMPLATE" failure mode was specifically checked for and found clean).

### Notes
- Full-site audit also surfaced (not yet acted on, flagged for follow-up):
  a local-only git branch with real unmerged SEO work and no remote backup;
  a `client/preview/ghl-form-2col-2026-07-15` remote branch that contradicts a
  memory note claiming it was deleted; guides pages missing `Article`/author
  schema despite showing a byline; several page titles/descriptions outside
  the ideal SEO length range; sitemap hreflang annotations only present for 3
  of 74 EN/ES page pairs; ~45 gallery images that would benefit from WebP;
  `logo-final.gif` is a 60-frame animated GIF used as a static logo.

## [0.3.0] — 2026-07-14
Full Spanish (`/spanish/`) content parity + ES header-logo fix.

### Spanish translations
- Translated the 46 remaining `/spanish/` pages from the English-passthrough
  "Traducción completa en español próximamente" banner to full, human-quality
  Latin-American Spanish: all 11 blog posts, the blog + guides indexes, 10
  city/location pages, 6 core pages (instructors, jobs, haircuts, schedules,
  resources, partners), 13 informational pages, 3 program pages, and 404.
  Every `/spanish/` URL on the site now serves real Spanish — **zero banner
  pages remain** (was 46/72 English-behind-banner).
- Bespoke Spanish `<title>` + meta description for the 10 location pages (they
  previously fell through to the English meta — a duplicate-title SEO bug) and
  all 11 blog posts (previously auto-generated).
- ES blog posts now carry the same author byline as EN (E-E-A-T parity),
  rendered in Spanish and linking to `/spanish/instructors`.
- Internal absolute links inside translated pages rewritten to stay in
  `/spanish/`; tag/structure parity verified byte-for-byte vs each EN source,
  so FAQ/Video schema extraction and asset paths carry over unchanged.

### Fixed
- Header logo 404'd (showed alt text) on every generated `/spanish/` page: the
  logo `src` used the nav-link root instead of the asset root, resolving to
  `/spanish/assets/...`. Now uses correct asset depth on all ES pages via a new
  `aroot` param in `_header_nav`. EN pages unaffected (default preserves prior
  behavior). Pre-existing since the 0.2.0 header rewrite.

### Notes
- Sitemaps already listed all `/spanish/` URLs and robots.txt already allows
  them — no sitemap/robots changes required.
- English pages, shared template, CSS/JS, and the 4 hand-crafted pages
  (`index`, `bronx`, `spanish/index`, `spanish/bronx`) are byte-identical.

## [0.2.0] — 2026-07-14
Landing-page + homepage release pass and full pre-launch audit.

### Landing pages (all 4: Manhattan/Bronx × EN/ES)
- Hero rebuilt to mirror the homepage `.hx` hero exactly — photo + gradient +
  live countdown + feature list + reserve-form card (replaced the earlier
  broken/duplicated hero that used abi.edu's photo).
- Header reduced to two rows — language toggle, then logo + campus phones.
  Navbar and campus switcher removed (landing pages are standalone); logo is
  no longer a link so it can't navigate to the main site.
- Campus-only phone numbers (no Haircut line); full "English/Español" switcher
  on every viewport.
- Multi-channel chat launcher (SMS / Instagram / WhatsApp / Messenger) ported
  site-wide from abi.edu (`assets/js/chat.js`).

### Homepage + Bronx
- Hero gradient changed from a 100° diagonal (drew a slanted "seam" / dark
  middle band) to a smooth left→right fade; photo reads brighter, no line.
- Mobile nav drawer now includes **Home** (was desktop-only).
- Language switcher shows full **English / Español** on all viewports.
- Phone chips: Manhattan 3 (EN/ES + Haircut), Bronx 2 (Bronx + Haircut), on
  desktop and mobile.
- Dropped ineffective hero-image `<link rel=preload>` hints (cleared Chrome
  "preloaded but not used" console warnings).

### SEO / AEO / sitemaps (pre-launch audit remediation)
- **Canonical fix (blocker):** `bronx.html`, `spanish/index.html`,
  `spanish/bronx.html` had `rel=canonical` pointing at `abi.edu` — corrected to
  self-referencing `www.americanbarberinstitute.com` URLs.
- Added the 5-tag hreflang block (en/en-US/es/es-US/x-default) to the 4
  hand-crafted pages (homepage + Bronx, EN + ES).
- Removed `robots.txt` `Disallow: /blog/` (contradicted the submitted
  post-sitemap and blocked 11 blog posts from indexing) and the stale
  `Disallow: /_archive/` rule — applied in the generator (`src/build.py`).
- Fixed `llms.txt` general contact email to `admissions@americanbarberinstitute.com`.
- Fixed half-translated accreditor name on the 2 hand-crafted Spanish pages.

### GHL forms
- Unified to the 4 client-provided forms with campus routing; landing pages
  use campus-specific forms, main site + contact + jobs use the .com form.

### Cleanup
- Removed tracked dev cruft: `landing-funnels/src/patch_build.py`,
  `landing-funnels/src/fix.py`, `.vscode/`.
- Removed stale/misfiled docs: `docs/AUDIT-REPORT.md` (belonged to the
  abi.edu repo) and `docs/content-audit.md` (completed v0.2.0 planning snapshot).

### Known remaining (non-blocking)
- 46 of 72 Spanish pages still serve English body content behind a disclosed
  "translation coming soon" banner — a dedicated translation pass is tracked
  separately. The 26 fully-translated pages cover the highest-traffic routes.

## [0.1.0] — 2026-06-18
Baseline for the production upgrade cycle — the full current site, handover-ready.

- **Architecture:** zero-dependency static HTML generated by Python
  (`src/build.py` + `src/build_landing_pages.py`); Vercel serves the built files directly.
- **Content:** English + Spanish pages — home, about, programs
  (500-hour Master, 200-hour, SMP, license transfer, etc.), schedule, admissions,
  tuition, instructors, jobs, gallery, blog, FAQ, contact, veterans, ACCESS-VR,
  partners, resources, and splash/landing pages.
- **Mobile:** mobile-first CSS with `viewport-fit=cover` + iOS safe-area insets and
  `prefers-reduced-motion` support.
