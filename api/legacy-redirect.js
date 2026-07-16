// Safety-net fallback for any old/unknown URL that has no matching static
// page and no explicit rule in vercel.json's "redirects" array.
//
// This only runs when nothing else matched: Vercel checks static files
// and the "redirects"/"rewrites" arrays in vercel.json first, so real
// pages and assets are never touched by this file. It exists purely so
// that a dead link never serves a bare 404 -- it always sends the visitor
// to the closest relevant modern page, or the homepage.
//
// The vercel.json catch-all rewrite that routes here excludes any path
// containing a "." (file extension), so genuine missing assets (images,
// CSS, JS, etc.) still 404 normally instead of being redirected to HTML.

const CATEGORY_FALLBACKS = {
  admissions: "/contact",
  home: "/about",
  policies: "/contact",
  licensing: "/programs",
  license: "/programs",
  "license-transfer": "/programs",
  courses: "/programs",
  jobs: "/jobs",
  jobss: "/jobs",
  graduates: "/jobs",
  gallery: "/gallery",
  veterans: "/veterans",
  "va-approved-job-training-program": "/veterans",
  "vesid-program": "/access-vr-program",
  resources: "/resources",
  schedule: "/schedules",
  about: "/about",
  members: "/",
  faq: "/faq",
};

module.exports = (req, res) => {
  const path = (req.url || "/").split("?")[0];
  const segments = path.split("/").filter(Boolean);

  let langPrefix = "";
  let rest = segments;
  if (segments[0] === "es" || segments[0] === "spanish") {
    langPrefix = "/" + segments[0];
    rest = segments.slice(1);
  }

  const category = rest[0];
  const target = (category && CATEGORY_FALLBACKS[category]) || "/";
  const destination = target === "/" ? langPrefix || "/" : langPrefix + target;

  res.statusCode = 301;
  res.setHeader("Location", destination);
  res.setHeader("Cache-Control", "public, max-age=0, s-maxage=600, must-revalidate");
  res.end();
};
