# American Barber Institute — Project State

## Ownership
- **Owner:** Alex — American Barber Institute
- **GitHub:** amerbarberedu-oss/american-barber-institute
- **Vercel:** amerbarberedu-oss-projects (prj_2RZVHYjsjp1QifRzSAdPamax1xEh)
- **Domain:** americanbarberinstitute.com / www.americanbarberinstitute.com (DNS cutover pending)
- **Developers:** Kazi (Frontend/UI/SEO/build), Arhum Abdullah (Analytics/GTM/CSP)

## Last Updated
- **Date:** 2026-07-14
- **Branch:** `preview/mass-rollout-2026-07-14` (not yet merged to `main`)
- **Status:** ✅ Pre-launch audit complete (READY-AFTER-FIXES). All blocker/high SEO
  findings fixed on the preview branch; awaiting explicit client go-live to merge to `main`.

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
Source of truth is the generators. As of 2026-07-14:
`landing.min.css?v=160`, `campus.js?v=4`, main `main.js`/`effects.js?v=33`,
`chatbot.js?v=32`; landing-funnels `CSS_V=65`. Check `src/build.py` and
`landing-funnels/src/build.py` for live values.

## Rollback
- Production `main` is the rollback point until a new release is merged.
- To undo an unmerged preview change, revert the commit or reset the preview branch.
