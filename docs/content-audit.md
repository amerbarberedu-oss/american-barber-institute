# Content Audit — ABI Black (toward v0.2.0)

Verified comparison of the live site's content against the authoritative scrape
(`~/website-source-collection/abi-app-123.vercel.app/`, incl. `authenticated/`
backend dumps). All claims below were checked against actual files — not assumed.

_Date: 2026-06-18 · Baseline: v0.1.0_

## What's already solid (no action needed)
- **FAQ page** present (`src/pages/faq.html`) with plan-dependent pricing.
- **Spanish:** 6 ES output pages exist (`es/`). Partial — see gap below.
- **Blog:** 10 blog partials (`src/pages/blog-*.html`) — covers the scrape's 8 posts.
- **Programs/pricing:** 500hr ($5,600 morning / $4,600 afternoon-weekend), 50hr
  refresher ($1,500), 3hr contagious ($100) all present and consistent.

## Gaps to close for 0.2.0 (verified, prioritized)
1. **Job listings not shown.** Scrape has **373** jobs; site shows placement-office
   info only. Action: display a curated sample (e.g. 15–25 recent) with a clear
   "placement office handles the rest" framing — 373 static listings is too heavy.
2. **Gallery depth.** Site gallery references ~15 images; scrape has **75**
   `gallery_items`. Action: expand the curated gallery to ~30–40 strong images
   with lazy-loading + lightbox.
3. **Spanish parity.** 6 ES pages exist but not full parity with EN. Action: map
   EN→ES coverage; translate the highest-traffic missing pages (programs, FAQ, contact).
4. **Instructor depth.** Confirm each named instructor has a card + photo + short bio.

## Accuracy items to CONFIRM WITH OWNER (do not change unilaterally)
- **200-hour program** appears on the site but is **not** in the backend `courses`
  table (only 500hr / 50hr / 3hr are). Is it a live offering? Keep, or remove?
- **Contagious-disease price:** site shows **$100** = the backend course `price`
  field (correct). The backend also has a schedule-plan `total` of **$50** — likely
  a deposit or stale plan. Confirm the $50 is not a current advertised price.
- (See `docs/migration/content-conflicts.md` for the resolved 500hr price item.)

## Notes
- Backend tables (jobs/gallery) are large; this is a **static** site, so content is
  curated/baked at build time, not live-queried. Curation choices above reflect that.
