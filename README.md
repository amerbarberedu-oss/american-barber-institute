# American Barber Institute (ABI) — Website

New York's only dedicated barber school (est. 1996). This repository contains the
complete marketing website: a fast, zero-framework static site generated from Python,
served on Vercel, in English and Spanish.

- **Canonical domain:** https://www.abi.edu (pending DNS cutover) · **Staging:** https://abi-website-black-lime.vercel.app

---

## 1. What this is

A fully static website — plain HTML, CSS and vanilla JavaScript — produced by two small
Python generators. There is **no runtime framework, no build toolchain, no Node
dependency**: the generators stamp content partials into a shared template and write
finished `.html` files to the repository root, which Vercel serves directly.

Why this approach:

- **Fast** — no hydration, tiny payloads, instant loads.
- **Cheap & durable** — static files on a CDN; nothing to break at runtime.
- **Easy to edit** — content lives in readable HTML partials; one command rebuilds the site.

---

## 2. Repository structure

```
abi-website/
├── README.md                  ← this file
├── AUDIT-REPORT.md            ← multi-method audit findings + analytics activation guide
├── vercel.json                ← Vercel routing (clean URLs, security headers)
├── robots.txt                 ← crawler directives
├── sitemap.xml                ← generated sitemap (with lastmod)
├── llms.txt                   ← guidance for AI search engines / LLMs
│
│   ── Generated, served at the site root (DO NOT hand-edit; rebuilt by the generators) ──
├── index.html                 ← English splash landing (home, "/")
├── classic-home.html          ← full long-form English home page
├── about.html  instructors.html  admissions.html  schedule.html  tuition.html
├── haircuts.html  jobs.html  partners.html  resources.html  gallery.html
├── faq.html  contact.html  veterans.html  access-vr.html  privacy.html  404.html
├── programs/                  ← program detail pages (500h, 200h, 50h, SMP, CD, license transfer) + index
├── jobs/                      ← job-opportunities board (347 shops) + shop-registration
├── blog/                      ← 9 articles + blog index
├── es/                        ← Spanish splash, home, and landing pages
├── splash-page-1/ splash-page-2/                       ← campaign splash variants
├── 500-hours-master-barber-program-landing-page/       ← ad landing pages
├── master-barber-program-bronx/
│
├── assets/
│   ├── css/   style.css · brand.css · landing.css · effects.css   (cache-busted with ?v=NN)
│   ├── js/    main.js · landing.js · effects.js · analytics.js
│   └── img/   photos, logo, favicon, instructors/, partners/
│
└── src/                       ← SOURCE — everything that builds the site (never served)
    ├── build.py               ← builds the main site pages from src/pages/*.html
    ├── build_landing_pages.py ← builds the EN/ES splash, landing & campaign pages
    ├── deploy_vercel.py        ← deploys to Vercel via REST (no CLI needed)
    ├── blog_manifest.json      ← list of blog posts consumed by build.py
    └── pages/                  ← content partials (one file per page; edit these)
```

**Golden rule:** edit content in `src/pages/*.html` (and the templates in
`src/build.py` / `src/build_landing_pages.py`), then **rebuild**. Never hand-edit the
generated `.html` files at the root — they are overwritten on every build.

---

## 3. Build & deploy

### Build locally

```bash
python3 src/build.py                 # main pages → repo root
python3 src/build_landing_pages.py   # splash / landing / es pages
```

`build.py` prints e.g. `built 46 pages + sitemap.xml + robots.txt`;
`build_landing_pages.py` prints `10 pages generated.`

### Deploy to production (Vercel)

```bash
VERCEL_TOKEN=*** python3 src/deploy_vercel.py
```

This uploads every tracked file except source/docs (`src/`, `*.md`, `.claude/`), creates
a **production** deployment, and aliases it to `abi-website-black.vercel.app`. Routing,
clean URLs and security headers are defined in `vercel.json`.

### Typical workflow

1. Edit a partial in `src/pages/` (or a template/CSS).
2. If you changed CSS, bump the cache version (e.g. `landing.css?v=48` → `?v=49`) in both generators.
3. `python3 src/build.py && python3 src/build_landing_pages.py`
4. Commit, push to `main`, deploy with `deploy_vercel.py`.

---

## 4. Pages & content

| Area | Pages |
|---|---|
| **Home** | `index.html` (splash), `classic-home.html` (full home) |
| **Programs** | 500-Hour Master Barber, 200-Hour Fundamentals, 50-Hour Refresher, Scalp Micro-Pigmentation, 3-Hour Contagious Diseases, License Transfer, + index |
| **Admissions** | Admissions & requirements, Schedule, **interactive Tuition & Payment Calculator** |
| **People** | Instructors (Manhattan + Bronx teams, real photos) |
| **Careers** | Job Placement, **Job Opportunities board (347 NYC shops, searchable)**, Shop Registration |
| **Funding** | Veterans / GI Bill®, ACCES-VR |
| **Public** | $3 Student Haircuts menu, Gallery (lightbox), Partners |
| **Content** | Blog (9 articles), FAQ, Resources, Contact, Privacy, 404 |
| **Spanish** | Full Spanish splash + home + landing pages under `/es/` |

**Contact model — two language lines only:**
English **(212) 290-2289** · Spanish **(212) 290-0278**. (Header shows both as call
buttons; footer lists both. No third call button.)

**Campuses:** Manhattan — 48 West 39th Street, NY 10018 · Bronx — 121 Westchester Square, NY 10461.

---

## 5. Design system

- **Themes:** five selectable color themes (Blue, Midnight, Classic, Emerald, Noir) via the
  top-bar dots; the choice is remembered in `localStorage` and applied before paint to avoid flashes.
- **Typography:** Oswald (display), Poppins/Inter (body) from Google Fonts.
- **CSS files:** `style.css` (base), `brand.css` (theme tokens), `landing.css` (components +
  revision packs), `effects.css` (motion). All linked with a `?v=NN` cache-buster bumped on change.
- **Effects:** tasteful 3-D card tilt, scroll-reveal, gallery/video hover polish, animated
  logo and countdown — all gated behind `prefers-reduced-motion`.
- **Social icons:** branded square tiles (Facebook, Instagram, X, YouTube, Pinterest) with
  per-brand hover color, lift and glow.
- **Responsive:** verified clean at 390 px (mobile) and 1280 px (desktop) — no overflow.

---

## 6. SEO / AEO (answer-engine optimization)

- Unique, length-optimized `<title>` (≤60c) and meta description (≤160c) per page.
- **Structured data (JSON-LD):** TradeSchool / LocalBusiness with rating, Course, Person
  (instructors), BreadcrumbList, FAQPage.
- Open Graph + Twitter cards, canonical URLs, `hreflang` EN/ES.
- `sitemap.xml` with `lastmod`, `robots.txt`, and **`llms.txt`** so AI search engines can
  read a clean summary of the school.
- Real values (counters, next class date) are baked into the HTML at build time, not
  JS-only, so crawlers see them.

See **AUDIT-REPORT.md** for the full technical-SEO / accessibility / conversion audit.

---

## 7. Analytics & Ads

`assets/js/analytics.js` is a **single consent-aware loader** that boots one
container — **Google Tag Manager `GTM-NKLLGPC`**. GA4 (`G-J6BNX36TS3`), Meta
Pixel, Microsoft Clarity, CallRail, ClickCease and Google Ads (`AW-949292069`)
are all managed **inside the GTM web UI** — do not add/remove those tags in code.

What the file does:
- Sets **Google Consent Mode v2** defaults before GTM loads (EEA/UK denied-by-default,
  US granted with opt-out), and injects an accessible **cookie-consent banner**.
- Pushes semantic events into `dataLayer` for GTM triggers: `generate_lead`
  (form submits), `phone_click` (`tel:` taps), `email_click` (`mailto:`).
- Captures GoHighLevel iframe leads via a `postMessage` listener **and** the
  `/thank-you` & `/gracias` pages (GHL forms redirect there on submit).

**To wire conversions:** in GTM create triggers `CE - generate_lead` and
`CE - phone_click`, map them to GA4 / Google Ads / Meta, and publish. No code
change is needed to add or edit tags.

---

## 8. Interactivity (vanilla JS)

- **Countdown + next-class date** to the first Monday of next month (`main.js`, values pre-baked).
- **Tuition & Payment Calculator** (`tuition.html`) — live totals, down payment and weekly
  plan per program/schedule, plus a program comparison table.
- **Job board search** — instant client-side filter over 347 shops.
- **Gallery lightbox**, **theme switcher**, **mobile nav drawer**, **call sheet**, **back-to-top**.

---

## 9. Maintenance notes

- **Content edits:** change `src/pages/*.html`, then rebuild. The root `.html` files are build output.
- **Blog:** posts are content partials `src/pages/blog-*.html` listed in
  `src/blog_manifest.json`; `build.py` assembles `blog/` and the blog index. To add a post,
  add a partial and a manifest entry, then rebuild.
- **Gallery:** curated images live in `assets/img/`; the grid markup is in
  `src/pages/gallery.html`.
- **Images:** keep paths root-absolute (`/assets/img/...`) so they resolve on clean-URL routes.
- **Secrets:** never commit API tokens. The Vercel token is passed via the `VERCEL_TOKEN`
  environment variable at deploy time only.

---

## 10. Project history (what was built)

A condensed log of the major work delivered:

1. **Foundation & content** — full site generated from the reference school content:
   home, programs, admissions, instructors, schedule, haircuts, jobs, resources, FAQ,
   contact, veterans, ACCES-VR, privacy, blog, gallery, Spanish edition.
2. **Brand & UI** — exact logo, one-line school name, five color themes, glassmorphism,
   per-page background photography, animated logo, refined CTAs.
3. **Conversion & SEO/AEO** — JSON-LD, OG/Twitter, hreflang, sitemap/robots/llms.txt,
   length-optimized titles & descriptions, trust strip, countdown, testimonials.
4. **Accessibility & QA** — contrast fixes, alt text, heading order, focus states, a
   repeatable headless mobile/desktop sweep (390 px & 1280 px) for overflow/404/console errors.
5. **New sections & pages** — Partners, Job Opportunities board (347 shops) + Shop
   Registration, instructor photos, interactive Tuition Calculator + comparison table.
6. **Client mobile-reference content** — "Everything You Need to Succeed" badge grid,
   "Barber Career Earnings" tiers, job-placement stats + shop chips, hero urgency/schedule
   strip, reserve-form campus/language fields, "Stop Waiting" final CTA — added in the
   site's own design, responsive on mobile and desktop.
7. **Analytics & Ads** — GA4 + Meta Pixel scaffolding with conversion events (see §7).
8. **Audit** — multi-method technical-SEO / accessibility / conversion audit with fixes
   (`AUDIT-REPORT.md`); fixed a real bug where the instructors meta description was
   truncated by unescaped quotes.
9. **Final cleanup & restructure** — removed unused assets and archive-only generator
   scripts, moved the build tooling under `src/`, untracked editor/Vercel metadata,
   and documented the whole project here.

---

© American Barber Institute (ABI). GI BILL® is a registered trademark of the U.S.
Department of Veterans Affairs.
