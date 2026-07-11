# American Barber Institute — Project State

## Ownership
- **Owner:** Alex — American Barber Institute
- **GitHub:** amerbarberedu-oss/american-barber-institute
- **Vercel:** amerbarberedu-oss-projects (prj_2RZVHYjsjp1QifRzSAdPamax1xEh)
- **Domain:** americanbarberinstitute.com / www.americanbarberinstitute.com
- **Developers:** Kazi (Frontend), Arhum Abdullah (Analytics/GTM)

## Last Updated
- **Date:** 2026-07-11
- **Agent:** Antigravity
- **Branch:** `main`
- **Status:** ✅ STABLE — Starting new change cycle

## Rollback Point (DO NOT DELETE)
- **Commit:** `74e0c8f` — chore: unify GHL forms
- **Date:** 2026-07-11
- **Note:** This is the last known stable state BEFORE any new changes.
  If anything goes wrong, revert to this commit:
  ```bash
  git reset --hard 74e0c8f
  ```

## Deployment Workflow
1. Make all changes locally
2. Test on localhost (python3 src/serve.py)
3. Deploy to preview (vercel deploy --no-prod)
4. Verify preview in browser
5. Only then deploy to production (vercel deploy --prod)

## Git Remote
- `origin` → amerbarberedu-oss/american-barber-institute (Alex's GitHub)
- Push command: `git push origin main`

## Current Versions
- Check `src/build.py` for CSS/JS version numbers

## Stashed Changes
- Experiment branch `experiment/compact-contact-form` has stashed contact form changes
- Apply with: `git stash pop` (on that branch only)
