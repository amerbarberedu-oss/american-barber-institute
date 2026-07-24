# American Barber Institute — americanbarberinstitute.com

A "careers & licensing hub" companion site to [abi.edu](https://www.abi.edu) (the
school's primary domain). Informational content — how to become a barber in NY,
licensing requirements, career guides — that funnels readers toward enrolling at
abi.edu, deliberately targeting different search intent from abi.edu so the two
sites don't compete with each other in search.

- **Current version:** 0.5.0 (2026-07-24) — see [CHANGELOG.md](CHANGELOG.md)
- **Canonical domain:** https://www.americanbarberinstitute.com (LIVE since
  2026-07-08 — the "DNS cutover pending" note below this line predates launch; the real, current site is reachable right
  now at the Vercel alias below)
- **Vercel alias:** https://american-barber-institute.vercel.app
- **Vercel project:** `american-barber-institute` on team `amerbarberedu-oss-projects`

## Recent changes (2026-07-16)

Full-site audit + cleanup pass: nav/hero/header redesign parity, a critical
sitewide contrast bug, Spanish structured-data localization, FAQ schema
coverage, dead-code cleanup, and 3 responsive bugs. Full detail in
[CHANGELOG.md](CHANGELOG.md) `[0.4.0]` — highlights:
- Bronx + all 4 landing pages were still running the homepage's **superseded
  hero/header design** (own code comments literally said "v4"/pre-unification)
  while the homepage had moved on. Rebuilt to match — see "Design system" below.
- **Critical:** a CSS minifier bug had been silently dropping text contrast to
  ~1.1:1 on every dark section sitewide since commit `8c8912d`. Fixed.
- **Critical:** 70 of 72 Spanish pages were serving **English structured data**
  (FAQPage answers, breadcrumbs, org description) reused verbatim from the
  English twin. Fixed at the generator level — see "Design system" below.
- Added `FAQPage` schema to 35 English pages that had visible FAQ content but
  no matching schema (AEO gap).
- Removed the Fraunces webfont (unused sitewide — a later CSS file silently
  overrode the font variable months ago and nobody removed the font request).
- ~550 lines of dead CSS removed (three past generations of superseded
  landing-page components), 4 dead images, 3 fully-merged git branches.

## Recent changes (2026-07-14)

Landing-page + homepage release pass and full pre-launch audit:
- **Landing pages** (4): rebuilt hero to exactly mirror the homepage `.hx` hero (photo + gradient + live countdown + feature list + form card); removed the navbar and campus switcher; logo is non-clickable (landing pages are standalone); campus-only phone numbers (no Haircut line); multi-channel chat launcher (SMS/Instagram/WhatsApp/Messenger) ported from abi.edu. *(Header further changed 2026-07-16 — see above.)*
- **Homepage + Bronx**: hero gradient switched from a 100° diagonal (drew a slanted "seam") to a smooth left→right fade; mobile nav drawer now includes Home; language switcher shows full "English/Español" on all viewports; Manhattan shows 3 phone chips (EN/ES + Haircut), Bronx 2 (Bronx + Haircut) on desktop and mobile.
- **SEO/AEO pre-launch fixes**: corrected cross-domain canonicals on `bronx.html` + Spanish home/bronx (were pointing at abi.edu); added hreflang to the 4 hand-crafted pages; removed the `robots.txt` `Disallow: /blog/` (contradicted the submitted post-sitemap) and the stale `/_archive/` rule; fixed `llms.txt` contact email to the .com address.
- **Cleanup**: dropped tracked dev cruft (`patch_build.py`, `fix.py`, `.vscode/`) and stale docs (`AUDIT-REPORT.md`, `content-audit.md`).

## Recent changes (2026-07-09)

**Developer roles defined:**
- **Kazi** — Frontend, UI/UX, HTML/CSS/JS, SEO, build scripts
- **Arhum Abdullah** — GA4, GTM, Google Ads, Meta Pixel, Clarity, CallRail, ClickCease, Vercel Analytics, consent mode, CSP analytics domains

> ⚠️ **Do NOT modify** `assets/js/analytics.js`, GTM/GA4/Ads/Pixel config, or CSP analytics domains without Arhum's sign-off.

**What changed:**
- **Mobile responsiveness** — bulletproof hamburger menu on all devices using `min()` clamping
- **Toggle styling** — seg-toggle glider in nav-drawer now teal with white active text (was invisible white-on-white); fixed `calc()` spacing in minified CSS
- **campus.js v4** — phone labels now show language ("English"/"Spanish") not location; auto-detects `/spanish/` pages and renders Spanish labels ("Inglés"/"Español"/"Corte"); removed "Clinic" from "Haircut Clinic" everywhere
- **Full Spanish translation** — 72 `/spanish/` pages: nav, footer, CTAs, drawer links, CTA buttons, countdown, Google reviews, contagious diseases course, form labels. Comprehensive body content translation.
- **Spanish image fixes** — 35 pages had broken logo (relative `src="assets/"` → absolute `src="/assets/"`)
- **Google rating** — standardized to 4.1 across all pages and structured data
- **2-card grid** — program pages with 2 cards center properly
- **Contact form placement** — form appears immediately after hero text on mobile

## What this is

A fully static site — plain HTML/CSS/vanilla JS, no framework, no build
toolchain, no Node dependency at request time — generated by two independent
Python scripts that stamp content partials into a shared template and write
finished `.html` files straight into the repo, which Vercel serves as-is.

## Design system

- **Hero pattern ("v5")** — `.hx`/`.hx-photo`/`.hx-copy`/`.hx-h1`/`.hx-next`,
  defined identically (structurally) in the 4 hand-crafted files' inline
  `<style>` and in `landing-funnels/assets/css/funnels.css`'s `#content .hx`
  block: full-bleed photo (no border-radius), no-gap photo/form grid,
  bottom-anchored copy, no dark gradient overlay (text relies on its own
  text-shadow), fixed ~400px copy column on desktop, bordered countdown-cell
  boxes, 1000px breakpoint. Manhattan's `index.html` is the canonical
  reference — if you change the hero anywhere, check Bronx and all 4 landing
  pages for drift (this exact drift caused a full redesign-parity pass on
  2026-07-16).
- **Editorial heading system** — `.display`/`.display--xl` in
  `assets/css/editorial.css`, used as the H1/H2 on ~200 guide/blog/pillar
  pages (everything generated by `src/build.py` except the 4 hero pages).
  `.display--xl` is the page H1, bare `.display` is used for in-page H2
  section headers. Landing-funnels pages use a completely separate heading
  system (`.lf-h1`/`.lf-h2`/`.lf-h3` in `funnels.css`) — don't conflate them.
- **Unified header (`.hdr2`)** — `assets/css/site-header.css`, landing-funnels
  pages only. One responsive row: desktop shows logo/phones/language-toggle
  on one line; mobile wraps to two lines (logo+toggle, then phones) via CSS
  `order` on the same markup, not two different DOM structures.
- **Campus theming** — `body.bx-gold` (Bronx) vs. the default teal theme,
  applied via `CAMPUS_BY_PAGE` in `src/build.py` (main site) or per-page CSS
  custom properties in `funnels.css` (landing pages, `--lf-accent` etc.).
- **Cache-busting** — every CSS/JS file is referenced with a manual `?v=N`
  query string. **A version bump must land in the same commit as the
  generator's own template/constant** (`src/build.py`'s TEMPLATE string,
  `landing-funnels/src/build.py`'s `CSS_V`/`JS_V`) or the next rebuild
  silently reverts every already-bumped page back to the old version. Don't
  hardcode current version numbers in docs (they drift fast) — grep the
  generators for the live value.
- **Known dead code (don't build on top of it):** `assets/css/landing.css`
  still contains a large superseded "v1 splash-page" module (`.inst-*`
  instructors styling, `.lf-form`/`.lf-stats`-adjacent rules) — confirmed
  unused via HTML+JS grep on 2026-07-16 but not yet removed since it's
  interleaved with live rules rather than cleanly contiguous. If you're
  hunting for "the instructors page styling" or similar, grep the actual
  class name used in the current HTML first — there may be an unused
  same-topic block elsewhere in the file that isn't it.

## Repository structure

```
american-barber-institute/
├── vercel.json              ← routing (clean URLs, redirects, security headers)
├── robots.txt · sitemap.xml · page/post/programs-sitemap.xml
├── index.html · bronx.html                 ← hand-crafted (NOT generated — see below)
├── spanish/index.html · spanish/bronx.html ← Spanish twins of the above, also hand-crafted
├── about.html, contact.html, faq.html, gallery.html, ... ← generated by src/build.py
├── programs/                ← program detail pages (Manhattan + Bronx variants)
├── guides/                  ← informational SEO content (how to become a barber, licensing, etc.)
├── blog/                    ← blog posts
├── spanish/                 ← Spanish twin of every page above (see i18n note below)
├── landing-funnels/         ← SEPARATE generator + output for the 2 paid-ad landing pages (EN+ES = 4 pages)
│   └── src/build.py
├── assets/
│   ├── css/   *.css (source) + *.min.css (served — regenerate with clean-css-cli after editing source)
│   ├── js/    analytics.js, campus.js, chatbot.js, effects.js, main.js
│   └── img/
└── src/                      ← SOURCE — never served directly (excluded via .vercelignore)
    ├── build.py              ← builds every page above except landing-funnels/ and the 4 hand-crafted files
    ├── build_landing_pages.py  ← DORMANT: location-page generator, LOCATIONS=[] (client asked to remove
    │                             mass SEO location pages 2026-07-07); currently produces 0 pages
    ├── blog_manifest.json     ← list of blog posts consumed by build.py
    ├── data.py                 (landing-funnels only)
    └── pages/                  ← content partials, one file per page — EDIT THESE, not the root .html files
        └── es-<partial>.html   ← real human Spanish translation override (see i18n note)
```

**Golden rule:** edit `src/pages/*.html` (or the templates inside `src/build.py`),
then rebuild. Never hand-edit a generated `.html` file at the repo root or under
`spanish/`/`programs/`/`guides/`/`blog/` — the next build silently overwrites it.
The only files that are *never* touched by `build.py` are `index.html`,
`bronx.html`, `spanish/index.html`, `spanish/bronx.html`, and everything under
`landing-funnels/`.

## Build

```bash
python3 src/build.py                    # main site + Spanish twins → repo root
cd landing-funnels && python3 src/build.py   # 4 ad-landing pages (Manhattan/Bronx × EN/ES)
```

`src/build.py` prints e.g. `built 122 pages + sitemap.xml + robots.txt`.
`landing-funnels/src/build.py` prints `4 landing pages generated.`

If you changed a `.css` source file, re-minify before deploying:
```bash
npx --yes clean-css-cli -o assets/css/<name>.min.css assets/css/<name>.css
```

## Deploying

This project is **Vercel git-integrated** — pushing to `main` on the `client`
remote auto-deploys to production. There is no separate deploy script or CLI
step required:

```bash
git push client main
```

`vercel.json` sets `cleanUrls: true` and `trailingSlash: false`. There is no
custom deploy tooling in this repo (an earlier `src/deploy_vercel.py` hardcoded
the wrong Vercel project name from a copy-pasted template and has been removed
— it was never functional against this project).

## Internationalization (Spanish)

Every English page has a Spanish twin at `/spanish/<slug>` (**not** `/es/` — the
old WordPress site that previously lived on this domain already used
`/spanish/` and has real historical traffic to prove it, so the URL structure
was matched to preserve that rather than adopting the ISO-standard `/es/`
convention abi.edu uses). `vercel.json` 301-redirects any `/es/...` request to
its `/spanish/...` equivalent.

`src/build.py` auto-generates a `/spanish/<slug>` twin for every English page.
By default the twin is the English body with Spanish headers/footers. Common UI phrases (headings, CTAs, buttons, nav, footer) have been bulk-translated via scripts. Longer body content on interior pages (blogs, guides) still has some English paragraphs — these need individual human translation. If a real, human-translated override file exists at `src/pages/es-<partial>.html`, that content is used instead.

## Tracking & analytics

`assets/js/analytics.js` boots **Google Tag Manager `GTM-NKLLGPC`** (shared with
abi.edu) plus a direct `gtag()` config for this site's *own* GA4 stream
(`G-B4TC0VGH2S`) — the GTM container's built-in GA4 tag is hardcoded to abi.edu's
stream, so this direct call is what makes .com traffic show up in its own
property. Meta Pixel, Microsoft Clarity, CallRail, ClickCease, and the Google
Ads conversion tag are all configured **inside the GTM web UI**, not in code.
There is no cookie-consent banner (client decision, 2026-07-08) — Consent Mode
v2 is set to granted-by-default for all regions.

Semantic events pushed to `dataLayer` for GTM triggers: `phone_click` (tel:
taps), `email_click` (mailto: taps), `generate_lead` (form submissions —
GoHighLevel forms are cross-origin iframes, so leads are also captured via the
`/thank-you` and `/gracias` pages, which the GHL form redirect must point at).

## Chatbot & forms

GoHighLevel chat widget (`widgets.leadconnectorhq.com/loader.js`, widget id
`6a627d266f3b01a586d50e87`) on every page — **no `defer` attribute**, that
breaks the live-connect behavior. Contact forms are GHL iframes, routed per
audience: a main "edu" form, a Manhattan landing form, and a Bronx landing form.

An earlier in-house chatbot ("Alex", `assets/js/chatbot.js`) is dormant —
not loaded on the main site (only still wired into the 4 `landing-funnels/`
pages). Kept in place rather than deleted; there's an inline comment at its
would-be call site describing how to re-enable it if GHL is ever swapped out.

## Campus context

Two physical campuses (Manhattan, Bronx). Pages are campus-aware via
`assets/js/campus.js` and `CAMPUS_BY_PAGE` in `src/build.py` — the sticky phone
strip, campus-switch pill, and page background swap based on which campus a
page (or the visitor's last choice) is for. `bronx.html` / `spanish/bronx.html`
apply a `.bx-gold` theme class; everything else defaults to the Manhattan/teal
theme.

## Maintenance notes

- **Content edits:** change the partial in `src/pages/`, then rebuild. Root
  `.html` files (except the 4 hand-crafted ones) are build output.
- **New blog post:** add a partial + a `src/blog_manifest.json` entry, rebuild.
- **New Spanish translation:** add `src/pages/es-<partial>.html`, rebuild — no
  code change needed, the override is picked up automatically.
- **Images:** unreferenced files get cleaned up periodically (a 2026-07-08 sweep
  removed 9 confirmed-orphaned images) — before adding a new hero/background
  image, check whether an existing one already covers the use case.
- **Secrets:** never commit tokens or `.env*` files — `.gitignore`/`.vercelignore`
  already exclude them; if you ever see one tracked, treat it as a live incident
  (rotate the credential), not just a cleanup item.

---

## Live URLs

### Main Website
| Page | URL |
|---|---|
| **Homepage (English)** | https://www.americanbarberinstitute.com/ |
| **Homepage (Spanish)** | https://www.americanbarberinstitute.com/spanish/ |
| **Bronx (English)** | https://www.americanbarberinstitute.com/bronx |
| **Bronx (Spanish)** | https://www.americanbarberinstitute.com/spanish/bronx |

### Landing Pages
| Landing Page | URL |
|---|---|
| **500-Hour Master Barber (Manhattan EN)** | https://www.americanbarberinstitute.com/500-hours-master-barber-program-landing-page/ |
| **500-Hour Master Barber (Manhattan ES)** | https://www.americanbarberinstitute.com/500-hours-master-barber-program-landing-page/spanish/ |
| **Master Barber Program (Bronx EN)** | https://www.americanbarberinstitute.com/master-barber-program-bronx/ |
| **Master Barber Program (Bronx ES)** | https://www.americanbarberinstitute.com/master-barber-program-bronx/spanish/ |

---

© American Barber Institute (ABI). GI BILL® is a registered trademark of the
U.S. Department of Veterans Affairs.
