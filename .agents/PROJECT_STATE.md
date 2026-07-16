# American Barber Institute — Project State

## Ownership
- **Owner:** Alex — American Barber Institute
- **GitHub:** amerbarberedu-oss/american-barber-institute
- **Vercel:** amerbarberedu-oss-projects (prj_2RZVHYjsjp1QifRzSAdPamax1xEh)
- **Domain:** americanbarberinstitute.com / www.americanbarberinstitute.com (DNS cutover pending)
- **Developers:** Kazi (Frontend/UI/SEO/build), Arhum Abdullah (Analytics/GTM/CSP)

## Last Updated
- **Date:** 2026-07-16
- **Branch:** `preview/nav-contrast-content-audit-2026-07-16` (not yet merged to `main`)
- **Status:** Full-site audit + cleanup pass complete: nav/hero/header redesign parity
  (Bronx + all 4 landing pages now match the homepage's v5 hero and unified `.hdr2`
  header), sitewide contrast fix, heading-size reduction, dead file/CSS/branch cleanup,
  Spanish structured-data localization fix, FAQPage schema added to 35 pages, 3
  responsive bugs fixed, Fraunces webfont removed (was unused sitewide). Awaiting
  explicit client go-live to merge to `main`.

## Deployment Workflow (git-integrated — no CLI deploys)
Vercel is connected to the GitHub repo and auto-deploys on push.
1. Make changes locally; run the generators:
   `cd src && python3 build.py`, then `cd landing-funnels/src && python3 build.py`.
2. Verify locally in a browser (any static server, e.g. `python3 -m http.server`),
   or push the preview branch and open the Vercel preview URL.
3. Commit as `American Barber Institute <amerbarberedu@gmail.com>`.
4. Push the preview branch: `git push client preview/<topic>`.
5. **Preview-first go-live:** only after explicit client approval, merge the
   preview branch into `main`. The push to `main` is what auto-deploys production.
   **Never push `main` directly.**

## Git Remote
- Single remote: `client` → https://github.com/amerbarberedu-oss/american-barber-institute
- Push command: `git push client <branch>`  (there is no `origin` remote)

## Current Asset Versions
Do not hardcode specific version numbers here — they change on every CSS/JS edit
and this note has gone stale twice already. Source of truth is always the
generators themselves: grep `?v=` in `src/build.py`'s TEMPLATE string and
`landing-funnels/src/build.py`'s `CSS_V`/`JS_V` constants. A version bump must
be applied to BOTH the already-built HTML files and the generator's own
template/constant in the same commit, or the next rebuild silently reverts it.

## Rollback
- Production `main` is the rollback point until a new release is merged.
- To undo an unmerged preview change, revert the commit or reset the preview branch.
