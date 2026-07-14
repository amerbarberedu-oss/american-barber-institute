# Changelog — American Barber Institute (americanbarberinstitute.com)

All notable changes to this site are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/). Versions stay in
the **0.x** range throughout the upgrade cycle; the move to **1.0.0** happens only
when the client approves the official production release.

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
