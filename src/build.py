#!/usr/bin/env python3
"""Static site builder for the American Barber Institute website.
Merges src/pages/*.html content partials into the base template.
Usage: python3 build.py
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'pages')
SITE_URL = 'https://www.americanbarberinstitute.com'

# ── Next class date (first Monday of upcoming month), computed at build time ──
def _next_first_monday():
    today = datetime.date.today()
    d = datetime.date(today.year, today.month, 1)
    while d.weekday() != 0:
        d += datetime.timedelta(days=1)
    if d <= today:
        y, m = (today.year, today.month + 1) if today.month < 12 else (today.year + 1, 1)
        d = datetime.date(y, m, 1)
        while d.weekday() != 0:
            d += datetime.timedelta(days=1)
    return d

_NEXT_MON = _next_first_monday()
_NEXT_DT = datetime.datetime.combine(_NEXT_MON, datetime.time(0, 0))
_DELTA = _NEXT_DT - datetime.datetime.now()
_REMAIN = max(int(_DELTA.total_seconds()), 0)
NEXT_START_LONG = _NEXT_MON.strftime('%A, %B ') + str(_NEXT_MON.day)   # "Monday, July 6"
CD_D, CD_H = str(_REMAIN // 86400), str((_REMAIN % 86400) // 3600)
CD_M, CD_S = str((_REMAIN % 3600) // 60), str(_REMAIN % 60)

# ---------------------------------------------------------------- template
TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{hreflang_block}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/og-cover.jpg">
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:locale" content="{oglocale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@amerbarberedu">
<meta name="twitter:creator" content="@amerbarberedu">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/assets/img/og-cover.jpg">
<meta name="twitter:image:alt" content="American Barber Institute — NYC barber school">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="American Barber Institute — NYC barber school">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="American Barber Institute">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="New York">
<meta name="theme-color" content="#101316">
<meta name="format-detection" content="telephone=no">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.min.css?v=37">
<link rel="stylesheet" href="{root}assets/css/brand.min.css?v=33">
<link rel="stylesheet" href="{root}assets/css/landing.min.css?v=177">
<link rel="stylesheet" href="{root}assets/css/upgrade.min.css?v=3">
<script src="{root}assets/js/analytics.js?v=8" defer></script>
<script defer src="/_vercel/insights/script.js"></script>
<script>try{{localStorage.removeItem('abi-theme');localStorage.removeItem('abi-theme-user');}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}assets/css/effects.min.css?v=32">
<link rel="stylesheet" href="{root}assets/css/editorial.min.css?v=9">
{schema}
</head>
<body class="shell2{bodyclass}" data-campus="{datacampus}" data-campus-locked="{campuslocked}" style="--page-bg:url('/assets/img/{pagebg}')">
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N9GTRLN" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
<div class="abi-deco" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>

<!-- ── UTILITY BAR: campus switcher · language · live campus phones ── -->
<div class="ubar">
  <div class="ubar-in">
    <div class="ubar-left">
      {campusswitch}
      {langtoggle}
    </div>
    <div class="ubar-right tb-calls" data-campus-phones>
      <a class="ubar-call ubar-call--admis" href="tel:+12122902289"><span class="ubar-ico" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span><span class="ubar-tag">English</span><span class="ubar-num">(212) 290-2289</span></a>
      <a class="ubar-call ubar-call--es" href="tel:+12122900278"><span class="ubar-ico" aria-hidden="true">ES</span><span class="ubar-tag">Spanish</span><span class="ubar-num">(212) 290-0278</span></a>
      <a class="ubar-call ubar-call--cut" href="tel:+18563161551"><span class="ubar-ico" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></svg></span><span class="ubar-tag">Haircut</span><span class="ubar-num">(856) 316-1551</span></a>
    </div>
  </div>
</div>
{header_nav}
<!-- ── Compact mobile phone strip (live per-campus via campus.js) ── -->
<div class="mstrip">
  <div class="mstrip-phones" data-mstrip-phones>
    <a class="mstrip-phone" href="tel:+12122902289"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span class="mstrip-t"><b>(212) 290-2289</b><i>English</i></span></a>
    <a class="mstrip-phone" href="tel:+18563161551"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></svg><span class="mstrip-t"><b>(856) 316-1551</b><i>Haircut</i></span></a>
  </div>
</div>

<main id="main">
{body}
</main>

{footer_block}

{mbar}

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{root}assets/js/main.js?v=34" defer></script>
<script src="{root}assets/js/effects.js?v=33" defer></script>
<script src="{root}assets/js/landing.js?v=33" defer></script>
<script src="{root}assets/js/upgrade.js?v=2" defer></script>
<script src="{root}assets/js/campus.js?v=6" defer></script>
<!-- GHL chat widget (VIBE AI). Alex chatbot preserved in /assets/js/chatbot.js — to restore Alex: delete this block and re-add the chatbot.js script tag. -->
<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="6a627d266f3b01a586d50e87"></script>
<script>(function(){{var t=setInterval(function(){{var w=document.querySelector("chat-widget");if(w&&w.shadowRoot){{clearInterval(t);var s=document.createElement("style");s.textContent=".lc_text-widget--prompt{{display:none!important}}@media(max-width:768px){{.lc_text-widget,.lc_text-widget--bubble{{bottom:140px!important;right:12px!important}}}}";w.shadowRoot.appendChild(s);}}}},400);setTimeout(function(){{clearInterval(t)}},15000);}})();</script>
<script src="{root}assets/js/video-sound.js?v=3" defer></script>
<script src="{root}assets/js/chat.js?v=3" defer></script>
</body>
</html>
"""

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["TradeSchool", "LocalBusiness", "EducationalOrganization"],
    "@id": SITE_URL + "/#organization",
    "name": "American Barber Institute",
    "alternateName": ["ABI", "American Barber Institute NYC"],
    "url": SITE_URL,
    "logo": {"@type": "ImageObject", "url": SITE_URL + "/icon.png", "width": 512, "height": 512},
    "image": SITE_URL + "/assets/img/og-cover.jpg",
    "foundingDate": "1996",
    "description": "New York's career-focused barber school. NYS-licensed 500-hour Master Barber program in Midtown Manhattan with financial aid, veterans GI Bill and ACCESS-VR options, and job placement.",
    "slogan": "Become a Licensed Barber in 4 Months",
    "telephone": "+1-212-290-2289",
    "email": "admissions@americanbarberinstitute.com",
    "address": [{
        "@type": "PostalAddress",
        "streetAddress": "48 West 39th Street",
        "addressLocality": "New York",
        "addressRegion": "NY",
        "postalCode": "10018",
        "addressCountry": "US"
    }, {
        "@type": "PostalAddress",
        "streetAddress": "121 Westchester Square",
        "addressLocality": "Bronx",
        "addressRegion": "NY",
        "postalCode": "10461",
        "addressCountry": "US"
    }],
    "geo": {"@type": "GeoCoordinates", "latitude": 40.7522, "longitude": -73.9849},
    # Both campuses split out as distinct sub-organizations so AI / Google
    # treat them as separate places with their own hours and phone.
    "department": [{
        "@type": "LocalBusiness",
        "@id": SITE_URL + "/#manhattan",
        "name": "American Barber Institute — Manhattan",
        "address": {"@type": "PostalAddress",
                    "streetAddress": "48 West 39th Street", "addressLocality": "New York",
                    "addressRegion": "NY", "postalCode": "10018", "addressCountry": "US"},
        "telephone": "+1-212-290-2289",
        "geo": {"@type": "GeoCoordinates", "latitude": 40.7522, "longitude": -73.9849},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday","Sunday"], "opens": "09:00", "closes": "19:00"}
        ]
    }, {
        "@type": "LocalBusiness",
        "@id": SITE_URL + "/#bronx",
        "name": "American Barber Institute — Bronx",
        "address": {"@type": "PostalAddress",
                    "streetAddress": "121 Westchester Square", "addressLocality": "Bronx",
                    "addressRegion": "NY", "postalCode": "10461", "addressCountry": "US"},
        "telephone": "+1-718-676-0640",
        "geo": {"@type": "GeoCoordinates", "latitude": 40.8401, "longitude": -73.8421},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday","Sunday"], "opens": "09:00", "closes": "19:00"}
        ]
    }],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "09:00", "closes": "19:00"}
    ],
    # Structured contact points — admissions in English + Spanish, and Bronx campus.
    # AI assistants and Google use these to confidently surface "call admissions" actions.
    "contactPoint": [
        {"@type": "ContactPoint", "telephone": "+1-212-290-2289", "contactType": "admissions",
         "areaServed": "US-NY", "availableLanguage": ["English"], "hoursAvailable": "Mo-Fr 08:00-20:00, Sa-Su 09:00-19:00"},
        {"@type": "ContactPoint", "telephone": "+1-212-290-0278", "contactType": "admissions",
         "areaServed": "US-NY", "availableLanguage": ["Spanish", "Español"], "hoursAvailable": "Mo-Fr 08:00-20:00, Sa-Su 09:00-19:00"},
        {"@type": "ContactPoint", "telephone": "+1-718-676-0640", "contactType": "admissions",
         "areaServed": "US-NY", "availableLanguage": ["English", "Spanish"], "hoursAvailable": "Mo-Fr 08:00-20:00, Sa-Su 09:00-19:00"},
        {"@type": "ContactPoint", "telephone": "+1-856-316-1551", "contactType": "customer service",
         "areaServed": "US-NY", "availableLanguage": ["English"]}
    ],
    "sameAs": [
        "https://www.facebook.com/Abi.Education/",
        "https://www.instagram.com/americanbarberinstitute/",
        "https://twitter.com/amerbarberedu",
        "https://www.youtube.com/@americanbarberinstitute",
        "https://www.tiktok.com/@americanbarberinstitute",
        "https://www.linkedin.com/company/american-barber-institute",
        "https://www.yelp.com/biz/american-barber-institute-new-york",
        "https://www.google.com/maps/place/American+Barber+Institute/@40.7522,-73.9849,17z",
        "https://www.bing.com/maps?q=American+Barber+Institute+New+York"
    ],
    "areaServed": [
        {"@type": "City", "name": "New York City"},
        {"@type": "City", "name": "Manhattan"},
        {"@type": "City", "name": "Bronx"},
        {"@type": "City", "name": "Queens"},
        {"@type": "City", "name": "Brooklyn"},
        {"@type": "City", "name": "Staten Island"},
        {"@type": "AdministrativeArea", "name": "Westchester County"},
        {"@type": "AdministrativeArea", "name": "Nassau County"},
        {"@type": "AdministrativeArea", "name": "Suffolk County"},
        {"@type": "State", "name": "New Jersey"},
        {"@type": "State", "name": "Connecticut"},
        # Neighborhood/community-level coverage: NYC (5 boroughs), Suffolk
        # County, Westchester County + Yonkers detail (client-provided local
        # SEO keyword research, 2026-07-16/17). Nassau County list pending --
        # client shared only its summary count (50), not the community table.
        {"@type": "Place", "name": "Astoria", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Long Island City", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Sunnyside", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Woodside", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Jackson Heights", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Elmhurst", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Corona", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "East Elmhurst", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Rego Park", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Forest Hills", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Kew Gardens", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Briarwood", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Fresh Meadows", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Flushing", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Murray Hill", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Whitestone", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "College Point", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Bayside", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Oakland Gardens", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Little Neck", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Douglaston", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Jamaica", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Jamaica Estates", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Jamaica Hills", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Hollis", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Hollis Hills", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Holliswood", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Queens Village", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Cambria Heights", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Laurelton", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Rosedale", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Springfield Gardens", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "St. Albans", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Richmond Hill", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "South Richmond Hill", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Woodhaven", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Glendale", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Ridgewood", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Maspeth", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Middle Village", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Ozone Park", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "South Ozone Park", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Howard Beach", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Rockaway Beach", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Far Rockaway", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Arverne", "containedInPlace": {"@type": "City", "name": "Queens"}},
        {"@type": "Place", "name": "Williamsburg", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Greenpoint", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bushwick", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bedford-Stuyvesant", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Crown Heights", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Prospect Heights", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Park Slope", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Gowanus", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Carroll Gardens", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Cobble Hill", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Boerum Hill", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Brooklyn Heights", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "DUMBO", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Downtown Brooklyn", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Red Hook", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Sunset Park", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bay Ridge", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bensonhurst", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Borough Park", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Dyker Heights", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Gravesend", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bath Beach", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Coney Island", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Brighton Beach", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Manhattan Beach", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Sheepshead Bay", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Marine Park", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Mill Basin", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Bergen Beach", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Canarsie", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "East New York", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Brownsville", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Cypress Hills", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "East Flatbush", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Flatbush", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Flatlands", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Midwood", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Kensington", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Windsor Terrace", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Fort Greene", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Clinton Hill", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Brooklyn Navy Yard", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Vinegar Hill", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Prospect Lefferts Gardens", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Sea Gate", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "Gerritsen Beach", "containedInPlace": {"@type": "City", "name": "Brooklyn"}},
        {"@type": "Place", "name": "St. George", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Tompkinsville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Stapleton", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Clifton", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Rosebank", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Fort Wadsworth", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Grymes Hill", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Concord", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Emerson Hill", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Randall Manor", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "West Brighton", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "New Brighton", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Port Richmond", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Mariners Harbor", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Elm Park", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Graniteville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Bulls Head", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Willowbrook", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Todt Hill", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "New Dorp", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Dongan Hills", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Grant City", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Midland Beach", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "South Beach", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Old Town", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Oakwood", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Oakwood Beach", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Bay Terrace", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Great Kills", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Eltingville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Annadale", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Huguenot", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Prince's Bay", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Pleasant Plains", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Richmond Valley", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Charleston", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Tottenville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Rossville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Arden Heights", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Greenridge", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Lighthouse Hill", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Egbertville", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Richmondtown", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Travis", "containedInPlace": {"@type": "City", "name": "Staten Island"}},
        {"@type": "Place", "name": "Financial District", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Battery Park City", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Tribeca", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Civic Center", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Chinatown", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Little Italy", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "SoHo", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "NoHo", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Nolita", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Greenwich Village", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "West Village", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "East Village", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Lower East Side", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Two Bridges", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Bowery", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Gramercy", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Kips Bay", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Murray Hill", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Chelsea", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Flatiron District", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Midtown Manhattan", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Midtown East", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Midtown West", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Hell's Kitchen", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Hudson Yards", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Garment District", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Times Square", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Theater District", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Turtle Bay", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Sutton Place", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Roosevelt Island", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Upper West Side", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Lincoln Square", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Manhattan Valley", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Morningside Heights", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Upper East Side", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Yorkville", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Carnegie Hill", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "East Harlem", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Central Harlem", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Hamilton Heights", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Manhattanville", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Washington Heights", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Hudson Heights", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Inwood", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Marble Hill", "containedInPlace": {"@type": "City", "name": "Manhattan"}},
        {"@type": "Place", "name": "Mott Haven", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Port Morris", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Melrose", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Concourse", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Highbridge", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Morrisania", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Morris Heights", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Mount Eden", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Mount Hope", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Tremont", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Belmont", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Fordham", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "University Heights", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Kingsbridge", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Kingsbridge Heights", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Riverdale", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "North Riverdale", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Spuyten Duyvil", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Marble Hill", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Norwood", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Bedford Park", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Woodlawn", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Wakefield", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Williamsbridge", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Baychester", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Co-op City", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Eastchester", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Edenwald", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Olinville", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Allerton", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Pelham Parkway", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Pelham Gardens", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Morris Park", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Van Nest", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Westchester Square", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Castle Hill", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Parkchester", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Soundview", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Clason Point", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Harding Park", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Throggs Neck", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Country Club", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Schuylerville", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Edgewater Park", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "City Island", "containedInPlace": {"@type": "City", "name": "Bronx"}},
        {"@type": "Place", "name": "Huntington", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Huntington Station", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Northport", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "East Northport", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Commack", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Dix Hills", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Melville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Deer Park", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "North Babylon", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "West Babylon", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Babylon", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "West Islip", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Islip", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "East Islip", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Central Islip", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Brentwood", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Bay Shore", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Brightwaters", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Sayville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "West Sayville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Oakdale", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Bohemia", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Ronkonkoma", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Lake Ronkonkoma", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Holbrook", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Holtsville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Patchogue", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Medford", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Bellport", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Blue Point", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Brookhaven", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Shirley", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Mastic", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Mastic Beach", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Center Moriches", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "East Moriches", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Manorville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Riverhead", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Wading River", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Rocky Point", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Miller Place", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Mount Sinai", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Port Jefferson", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Port Jefferson Station", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Selden", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Centereach", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "St. James", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Smithtown", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Nesconset", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Hauppauge", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Kings Park", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Lake Grove", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Farmingville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Ridge", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "East Hampton", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Southampton", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Hampton Bays", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Westhampton", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Westhampton Beach", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Sag Harbor", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Greenport", "containedInPlace": {"@type": "AdministrativeArea", "name": "Suffolk County"}},
        {"@type": "Place", "name": "Yonkers", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Mount Vernon", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "New Rochelle", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "White Plains", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Scarsdale", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Eastchester", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Tuckahoe", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Bronxville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Pelham", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Pelham Manor", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Mamaroneck", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Larchmont", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Rye", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Rye Brook", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Port Chester", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Harrison", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Purchase", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Armonk", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "North White Plains", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Valhalla", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Elmsford", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Greenburgh", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Hartsdale", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Irvington", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Dobbs Ferry", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Hastings-on-Hudson", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Ardsley", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Tarrytown", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Sleepy Hollow", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Ossining", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Briarcliff Manor", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Pleasantville", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Thornwood", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Hawthorne", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Mount Kisco", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Bedford Hills", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Katonah", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Bedford", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Chappaqua", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Croton-on-Hudson", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Buchanan", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Peekskill", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Cortlandt Manor", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Mohegan Lake", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Yorktown Heights", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Shrub Oak", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Jefferson Valley", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Somers", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Lincolndale", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Goldens Bridge", "containedInPlace": {"@type": "AdministrativeArea", "name": "Westchester County"}},
        {"@type": "Place", "name": "Getty Square", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Downtown Yonkers", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Southwest Yonkers", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Northwest Yonkers", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Southeast Yonkers", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Northeast Yonkers", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Ludlow", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Park Hill", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Nepperhan", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Nodine Hill", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Bryn Mawr", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Dunwoodie", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Lincoln Park", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Homefield", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Runyon Heights", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Beech Hill", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Crestwood", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Cedar Knolls", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Lawrence Park West", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Colonial Heights", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Colonial Corners", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Armour Villa", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Mohegan Heights", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Kimball", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Sprain Lake Knolls", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Woodstock Manor", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Wakefield Park", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Monastery Heights", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Sherwood Park", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
        {"@type": "Place", "name": "Sunnyside Park", "containedInPlace": {"@type": "City", "name": "Yonkers"}},
    ],
    "knowsLanguage": ["English", "Spanish"],
    "knowsAbout": [
        "Barbering", "Master Barber Program", "Barber Licensing",
        "Hair Cutting", "Fades", "Tapers", "Beard Trimming",
        "Straight Razor Shaving", "Hair Color", "Scalp Micropigmentation",
        "Barber Career Training", "NY State Board Exam Prep"
    ],
    "accreditedBy": {"@type": "Organization", "name": "New York State Department of Education",
                     "url": "https://www.nysed.gov/"},
    "memberOf": {"@type": "Organization", "name": "American Association of Cosmetology Schools"},
    "priceRange": "$$",
    "paymentAccepted": ["Cash", "Credit Card", "Financial Aid", "GI Bill", "ACCES-VR"],
    "currenciesAccepted": "USD"
}
# Spanish twin of ORG_SCHEMA — only `description`/`slogan` are prose that needs
# translating (address/phone/geo/URLs are language-neutral). Uses the same
# approved Spanish copy already live in the hand-crafted spanish/index.html
# (audit 2026-07-16: every generated Spanish page was reusing the English
# ORG_SCHEMA verbatim instead of this).
ORG_SCHEMA_ES = dict(ORG_SCHEMA,
    description="La única escuela dedicada de barbería en Nueva York. Programa de Barbero Maestro de 500 horas "
                "licenciado por el Estado de NY, en Midtown Manhattan y el Bronx, con ayuda financiera, GI Bill "
                "para veteranos, ACCES-VR y colocación laboral.",
    slogan="Conviértete en Barbero Licenciado en 4 Meses")

def course_schema(name, desc, hours, weeks, price, campus="manhattan"):
    location_address = ("121 Westchester Square, Bronx, NY 10461" if campus == "bronx"
                         else "48 West 39th Street, New York, NY 10018")
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": name,
        "description": desc,
        "provider": {"@type": "TradeSchool", "name": "American Barber Institute", "url": SITE_URL},
        "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "USD", "category": "Tuition"},
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "onsite",
            "courseWorkload": f"PT{hours}H",
            "location": {"@type": "Place", "name": "American Barber Institute",
                         "address": location_address}
        },
        "timeRequired": f"P{weeks}W"
    }

def video_schema(vid, name, desc, upload):
    """YouTube-backed VideoObject for rich-result eligibility (tour/haircut clips)."""
    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": name,
        "description": desc,
        "thumbnailUrl": [f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
        "uploadDate": upload,
        "contentUrl": f"https://www.youtube.com/watch?v={vid}",
        "embedUrl": f"https://www.youtube.com/embed/{vid}",
        "publisher": {"@type": "Organization", "name": "American Barber Institute",
                      "logo": {"@type": "ImageObject", "url": SITE_URL + "/icon.png"}}
    }

def _word_count(html):
    txt = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    return len([w for w in re.split(r'\s+', txt) if w])

def article_schema(title, url, slug=None, body=None, date="2024-02-01"):
    """BlogPosting schema with a named human author (E-E-A-T) instead of generic Organization.
    Each post maps to one of the ABI instructors via BLOG_AUTHORS."""
    author_name, author_role = BLOG_AUTHORS.get(slug or "", ("David Ayeoribe", "Lead Senior Instructor & Director"))
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "name": title,
        "inLanguage": "en-US",
        "isPartOf": {"@type": "Blog", "name": "American Barber Institute Blog",
                     "url": SITE_URL + "/blog/"},
        "datePublished": date,
        "dateModified": "2026-07-05",
        "image": {"@type": "ImageObject", "url": SITE_URL + "/assets/img/og-cover.jpg",
                  "width": 1200, "height": 630},
        "author": {
            "@type": "Person",
            "name": author_name,
            "jobTitle": author_role,
            "url": SITE_URL + "/instructors",
            "worksFor": {"@type": "EducationalOrganization",
                         "@id": SITE_URL + "/#organization",
                         "name": "American Barber Institute"}
        },
        "publisher": {
            "@type": "EducationalOrganization",
            "@id": SITE_URL + "/#organization",
            "name": "American Barber Institute",
            "logo": {"@type": "ImageObject", "url": SITE_URL + "/icon.png",
                     "width": 512, "height": 512}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "articleSection": "Barbering Career",
        "keywords": "barber school NYC, barber career, barbering, American Barber Institute, "
                    "NY barber license, master barber, career change, vocational training",
        "about": [
            {"@type": "Thing", "name": "Barbering"},
            {"@type": "Thing", "name": "Career in Barbering"},
            {"@type": "EducationalOrganization", "@id": SITE_URL + "/#organization"}
        ]
    }
    if body:
        wc = _word_count(body)
        if wc:
            schema["wordCount"] = wc
    return schema

# Rewrite internal links from foo.html → /foo (clean URLs match canonical + cleanUrls:true,
# eliminating the 308 redirect hop search engines were following).
def clean_links(html):
    def repl(m):
        url = m.group(1)
        low = url.lower()
        if low.startswith(("http://", "https://", "//", "mailto:", "tel:", "sms:",
                           "javascript:", "data:", "#")):
            return m.group(0)
        mm = re.match(r'^([^#?]*)([#?].*)?$', url)
        path, suffix = mm.group(1), (mm.group(2) or "")
        if path.endswith("index.html"):
            path = path[:-len("index.html")] or "/"
        elif path.endswith(".html"):
            path = path[:-len(".html")]
        return 'href="%s%s"' % (path, suffix)
    return re.sub(r'href="([^"]*)"', repl, html)

VIDEO_SCHEMAS = {
    "about.html": [
        video_schema("TFpNNqsc_EA", "American Barber Institute — Virtual Campus Tour",
                     "Take a virtual tour of the American Barber Institute Manhattan campus and clinic floor.", "2024-03-01"),
        video_schema("iU0fUj3a8uw", "Inside the ABI Barber Clinic",
                     "A look inside the hands-on barber clinic where ABI students train on real clients.", "2024-03-01"),
        video_schema("ozV_RcSk0P4", "Life as an ABI Barbering Student",
                     "What a day of training looks like for students at American Barber Institute.", "2024-03-01"),
    ],
    "haircuts.html": [
        video_schema("oM8KfWfeTWA", "$3 Student Haircuts at American Barber Institute",
                     "Get a quality cut for $3 from supervised ABI student barbers in Manhattan and the Bronx.", "2024-04-01"),
    ],
}

# ---------------------------------------------------------------- pages
_BARBER_SKILLS = [
    "Master Barber Instruction", "Hair Cutting", "Fades", "Tapers",
    "Beard Grooming", "Straight Razor Shaving", "NY State Board Exam Prep",
    "Hands-on Clinical Training"
]
def _person(name, role, campus, skills=None, years=None, languages=None):
    p = {
        "@type": "Person",
        "name": name,
        "jobTitle": role,
        "worksFor": {"@type": "EducationalOrganization",
                     "@id": SITE_URL + "/#organization",
                     "name": "American Barber Institute"},
        "workLocation": {"@type": "Place", "name": "American Barber Institute — " + campus.split(",")[0],
                         "address": campus},
        "knowsAbout": skills or _BARBER_SKILLS,
        "knowsLanguage": languages or ["English"],
        "url": SITE_URL + "/instructors"
    }
    if years is not None:
        # ABI standard: every instructor named here is also an ABI graduate.
        p["alumniOf"] = {"@type": "EducationalOrganization", "@id": SITE_URL + "/#organization",
                         "name": "American Barber Institute"}
        # Schema.org doesn't have yearsOfExperience natively — surface it via description
        # so AI assistants pick it up when summarizing the bio.
        p["description"] = f"{role} at American Barber Institute with {years}+ years in barbering."
    return p

# Each instructor's bio expanded so AI/search engines surface real expertise,
# tenure, and specialties — the E-E-A-T signal that was completely missing.
INSTRUCTORS_SCHEMA = {"@context": "https://schema.org", "@type": "ItemList",
    "name": "American Barber Institute Instructors", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": _person(n, r, c, sk, yr, lg)}
        for i, (n, r, c, sk, yr, lg) in enumerate([
            ("David Ayeoribe", "Lead Senior Instructor & Director", "Manhattan, NY",
             _BARBER_SKILLS + ["Barber School Leadership", "Curriculum Design"], 50, ["English"]),
            ("Harold \"Barkim\" Brown", "Lead Instructor", "Manhattan, NY",
             _BARBER_SKILLS + ["Celebrity Barbering", "Emmy-Featured Stylist"], 25, ["English"]),
            ("Barry Brown", "Instructor", "Manhattan, NY", _BARBER_SKILLS, 15, ["English"]),
            ("Freddie Liciaga", "Bilingual Instructor", "Manhattan, NY", _BARBER_SKILLS, 18, ["English","Spanish"]),
            ("Benny Santamaria", "Bilingual Instructor", "Manhattan, NY", _BARBER_SKILLS, 16, ["English","Spanish"]),
            ("Richard Cancel", "Bilingual Instructor", "Manhattan, NY", _BARBER_SKILLS, 14, ["English","Spanish"]),
            ("Truth \"The Barber Artist\" Quinones", "Founding Director, ABI Bronx", "Bronx, NY",
             _BARBER_SKILLS + ["Scalp Micropigmentation", "Hair Art"], 30, ["English","Spanish"]),
            ("Osvaldy \"Mr. O\" Rodriguez", "Instructor", "Bronx, NY", _BARBER_SKILLS, 12, ["English","Spanish"]),
            ("Noah Vera", "Bilingual Instructor", "Bronx, NY", _BARBER_SKILLS, 10, ["English","Spanish"]),
        ])]}

# Map each blog post to a named ABI author. AI assistants will now cite
# "according to <name>, instructor at ABI" instead of the generic "ABI says".
BLOG_AUTHORS = {
    "why-should-i-go-to-barber-school": ("David Ayeoribe", "Lead Senior Instructor & Director"),
    "a-women-barber-the-benefits-of-barber-school": ("David Ayeoribe", "Lead Senior Instructor & Director"),
    "are-barbershops-profitable-everything-you-need-t": ("David Ayeoribe", "Lead Senior Instructor & Director"),
    "first-things-first-what-happens-after-barber-sch": ("David Ayeoribe", "Lead Senior Instructor & Director"),
    "how-to-successfully-market-your-barbershop": ("Harold \"Barkim\" Brown", "Lead Instructor"),
    "modern-day-barbering-problem-overcome-them": ("Harold \"Barkim\" Brown", "Lead Instructor"),
    "diverse-haircut-training-at-american-barber-inst": ("Truth \"The Barber Artist\" Quinones", "Founding Director, ABI Bronx"),
    "barber-school-instructors-in-nyc": ("David Ayeoribe", "Lead Senior Instructor & Director"),
    "exploring-the-benefits-of-enrolling-in-the-ameri": ("David Ayeoribe", "Lead Senior Instructor & Director"),
}

FAQ_SCHEMA_PLACEHOLDER = "FAQ_SCHEMA"
VIDEO_SCHEMA_PLACEHOLDER = "GALLERY_VIDEO_SCHEMA"

PAGES = [
    # (output, partial, title, description, lang, extra_schema)
    ("about.html", "about.html",
     "Is ABI the Right Barber School for You? Meet the Team",
     "How ABI helps career-changers become licensed barbers. Our mentors, hands-on approach, and 30+ years building barber careers.",
     "en", ["FAQ_SCHEMA"]),
    ("instructors.html", "instructors.html",
     "Who Will Teach You to Barber? Meet the Mentors at ABI",
     "ABI's master instructors, including King David Ayeoribe and Emmy-featured Harold Brown, bring 50+ years of combined barbering chair time.",
     "en", [INSTRUCTORS_SCHEMA]),
    ("jobs.html", "jobs.html",
     "What Can You Do After Barber School? Career Outcomes & Job Paths",
     "Where a barber license can take you — shop chairs, booth rental, your own business — and how ABI's job-placement support helps graduates land their first role.",
     "en", ["FAQ_SCHEMA"]),
    ("gallery.html", "gallery.html",
     "See What Barber Training Looks Like — Student Work",
     "Real student cuts, the clinic floor, and daily life while training to become a barber. See what you're stepping into.",
     "en", [VIDEO_SCHEMA_PLACEHOLDER]),
    ("haircuts.html", "haircuts.html",
     "$3 Haircuts at ABI — How the Student Clinic Works",
     "The $3 student clinic is where trainees log real hours on real clients. Book a cut in Manhattan or the Bronx.",
     "en", ["FAQ_SCHEMA"]),
    ("faq.html", "faq.html",
     "Thinking About Barber School? Your Questions, Answered",
     "Answers on cost, training duration, schedules, age requirements, funding, and job placement. Everything to decide if barbering is right for you.",
     "en", ["FAQ_SCHEMA"]),
    ("schedules.html", "schedules.html",
     "Fit Barber School Around Your Life — ABI Schedules",
     "Morning, afternoon or weekend. Full-time finishes in about 4 months; weekends in 6-7. New classes start the first Monday monthly.",
     "en", ["FAQ_SCHEMA"]),
    ("contact.html", "contact.html",
     "Book a Tour or Talk to Admissions — Contact ABI",
     "See the campus before you commit. Tour 48 West 39th St, NYC, near Penn Station and Grand Central. Admissions in English or Spanish.",
     "en", [ORG_SCHEMA, "FAQ_SCHEMA"]),
    ("resources.html", "resources.html",
     "Barber Licensing Boards & Resources by State",
     "State-by-state barber licensing boards, regulatory agencies, and industry resources for your path to becoming a licensed barber.",
     "en", []),
    ("partners.html", "partners.html",
     "Where Do ABI Barbers End Up? Our Shop Network",
     "NYC shops that hire our graduates: Levels Barbershop, Diamond Fadez, Untouchable Cutz, Expo Gentlemen Salon, Otis & Finn and more.",
     "en", []),
    ("404.html", "404.html",
     "Lost? Let's Get You Back on the Path to Barbering",
     "This page took a wrong turn. Head back to the American Barber Institute homepage or explore how to start your barber career.",
     "en", []),
    ("programs/index.html", "programs-index.html",
     "Which Barber Program Is Right for You? Compare Your Options",
     "Compare ABI's three paths: the 500-hour Master Barber program (your route to a NY license), the 50-hour Refresher for licensed pros, and the 3-hour Contagious Diseases course.",
     "en", ["FAQ_SCHEMA"]),
    ("programs/manhattan.html", "programs-manhattan.html",
     "Manhattan Campus Programs | American Barber Institute",
     "Every barber program at our Midtown Manhattan campus: 500-Hour Master Barber, 50-Hour Refresher and Contagious Diseases. NYSED-approved, weekly payment plans.",
     "en", []),
    ("programs/bronx.html", "programs-bronx.html",
     "Bronx Campus Programs | American Barber Institute",
     "Every barber program at our Bronx campus (Westchester Square): 500-Hour Master Barber and Contagious Diseases. NYSED-approved, bilingual, weekly payment plans.",
     "en", []),
    ("programs/500-hour-master-barber.html", "program-500.html",
     "500-Hour Master Barber — Beginner to Licensed",
     "First fade to licensed Master Barber in Manhattan: 500 hours of hands-on training in ~4 months, flexible schedules, from $4,600.",
     "en", [course_schema("500 Hour Master Barber Program",
        "500-hour NYS-licensed master barber training completed in about 4 months full-time: theory, practical work on real clients, State Board exam prep and job placement.", 500, 17, 5600),
        FAQ_SCHEMA_PLACEHOLDER]),
    ("programs/500-hour-master-barber-bronx.html", "program-500-bronx.html",
     "Become a Licensed Barber in the Bronx — The 500-Hour Path",
     "Your transformation at ABI's Bronx campus: 500 hours of hands-on, bilingual training in about 4 months, flexible schedules, payment plans and job-placement support.",
     "en", [course_schema("500 Hour Master Barber Program — Bronx",
        "500-hour NYS-licensed master barber training at the Bronx campus, completed in about 4 months full-time, with bilingual instruction, State Board exam prep and job placement.", 500, 17, 5600, campus="bronx"),
        FAQ_SCHEMA_PLACEHOLDER]),
    ("programs/50-hour-barber-refresher.html", "program-50.html",
     "50-Hour Barber Refresher — Get Board-Ready Fast",
     "For cosmetologists, hairdressers and apprentices: sharpen skills and prep for the NY State Board Exam in ~2 weeks in Manhattan.",
     "en", [course_schema("50 Hour Barber Refresher Program",
        "Two-week refresher preparing licensed professionals for the New York State Barbering Licensing Examination. This course is offered only at ABI's Manhattan campus.", 50, 2, 1500),
        FAQ_SCHEMA_PLACEHOLDER]),
    ("programs/contagious-diseases.html", "program-cd.html",
     "Contagious Diseases Course — NY Barber Requirement",
     "The NY-required Contagious Diseases course for barber operators and apprentices. Complete by mail for $100 with booklet and exam.",
     "en", [course_schema("3 Hours Contagious Diseases Program",
        "Home-study course on transmission of contagious diseases, sanitation and sterilization required for NY barber licensure.", 3, 1, 100),
        FAQ_SCHEMA_PLACEHOLDER]),
    ("blog/index.html", "blog-index.html",
     "Barber Career Guides — Licensing, Money & Life Behind the Chair",
     "Practical guides for anyone weighing a barber career: what a license takes, how much barbers earn, shop ownership, and what really happens after barber school.",
     "en", []),
    # ── Hidden SEO pages (parity with the old abi.edu sitemap) ──────────────
    # Not linked from nav/footer by design: reachable by URL, listed in
    # sitemap.xml, and interlinked among themselves only.
    ("financial-aid.html", "page-financial-aid.html",
     "How Do People Pay for Barber School? Funding Options",
     "How students fund barber training: ACCES-VR, GI Bill for veterans, and $150/week payment plans. Find the option that fits.",
     "en", ["FAQ_SCHEMA"]),
    ("how-to-get-started.html", "page-how-to-get-started.html",
     "How to Start a Barber Career — Your First Steps",
     "From curious to enrolled: book a tour, gather documents, choose a schedule, and start on the first Monday at our Manhattan or Bronx campus.",
     "en", ["FAQ_SCHEMA"]),
    ("access-vr-program.html", "page-access-vr-program.html",
     "Could ACCES-VR Cover Your Barber Training?",
     "New Yorkers with a documented disability may get tuition, tools and books funded by ACCES-VR. See who qualifies and how to apply.",
     "en", ["FAQ_SCHEMA"]),
    ("veterans.html", "page-veterans.html",
     "Veterans: How to Use Your GI Bill® to Become a Barber",
     "Turn GI Bill benefits into a barber career: Post-9/11 (Ch. 33), VR&E (Ch. 31), Montgomery and DEA (Ch. 35). Licensed in about 4 months.",
     "en", ["FAQ_SCHEMA"]),
    ("privacy-and-policy.html", "page-privacy-and-policy.html",
     "Privacy Policy | American Barber Institute",
     "How ABI collects, protects and shares your information, including cookies from Google Analytics, Meta Pixel, Clarity and forms.",
     "en", []),
    ("virtual-tour.html", "page-virtual-tour.html",
     "Take a Look Inside Before You Enroll — Virtual Campus Tour",
     "See the clinic floor, the chairs and the space where you'd train, on video. Get directions and book an in-person tour of our Manhattan or Bronx campus.",
     "en", ["FAQ_SCHEMA"]),
    ("skills-and-techniques.html", "page-skills-and-techniques.html",
     "What Will You Learn? Skills Built on the Floor",
     "From first fade to razor lineups, shaves, sanitation and board-exam theory. What you master hands-on during 500 hours at ABI.",
     "en", []),
    ("shop-registration.html", "page-shop-registration.html",
     "Hiring Barbers? Connect With ABI-Trained Graduates",
     "Shop owners: register with ABI's job-placement office for free to meet trained, board-prepared graduates ready to take a chair at your NYC barbershop.",
     "en", ["FAQ_SCHEMA"]),

    # ── .com career / decision / licensing hub — net-new pages ───────────────
    # Career-journey hub pages (linked from the main nav).
    ("why-barbering.html", "page-why-barbering.html",
     "Why Barbering? The Case for a Career Behind the Chair",
     "Thinking about a career change? Why barbering offers fast licensing, real income, creativity and independence — and how to tell if it's right for you.",
     "en", ["FAQ_SCHEMA"]),
    ("training-experience.html", "page-training-experience.html",
     "The Barber Training Experience: What It Really Looks Like",
     "What hands-on barber training actually feels like — the clinic floor, real clients, and how you go from your first cut to board-ready.",
     "en", ["FAQ_SCHEMA"]),
    ("career-paths.html", "page-career-paths.html",
     "Barber Career Paths: 7 Ways to Build a Life Behind the Chair",
     "From shop employee to booth renter, owner, educator and beyond — the seven career paths a barber license can open, and how to get there.",
     "en", ["FAQ_SCHEMA"]),
    ("student-stories.html", "page-student-stories.html",
     "Student Stories: Real Barber Career Transformations",
     "How career-changers became working barbers — the paths, the turning points, and what the leap into barbering really takes.",
     "en", ["FAQ_SCHEMA"]),
    ("tuition-and-funding.html", "page-tuition-and-funding.html",
     "Tuition & Funding: How to Pay for Barber Training in New York",
     "Your options for paying for barber training — payment plans, GI Bill® and ACCES-VR — and how to figure out what fits your budget.",
     "en", ["FAQ_SCHEMA"]),
    ("landingpage.html", "landingpage.html",
     "Become a Licensed Barber in NYC — Enroll at American Barber Institute",
     "Enroll at American Barber Institute and train for your NY Master Barber license — 500 hours, about 4 months full-time, Manhattan & Bronx campuses, weekly payment plans plus GI Bill® and ACCES-VR funding. New classes start the first Monday of every month.",
     "en", ["FAQ_SCHEMA"]),
    ("is-barber-training-right-for-you.html", "page-is-barber-training-right-for-you.html",
     "Is Barber Training Right for You? A Quick Self-Assessment",
     "Not sure barbering is your move? Work through this honest self-check on fit, time, money and goals before you commit.",
     "en", ["FAQ_SCHEMA"]),
    ("ny-barber-licensing-checklist.html", "page-ny-barber-licensing-checklist.html",
     "Free NY Barber Licensing Checklist (2026)",
     "Get a free, step-by-step checklist to become a licensed barber in New York — requirements, training hours, the exam and documents in one place.",
     "en", ["FAQ_SCHEMA"]),

    # ── Location / geo-targeted SEO pages ──────────────────────────────────
    # Output slugs match abi.edu's existing URL structure exactly. Titles and
    # descriptions are differentiated to avoid cannibalization with abi.edu's
    # enrollment-focused pages (these are informational / career-hub voice).
    ("barber-school-queens-ny.html", "location-queens.html",
     "Barber School Near Queens, NY — Your Career Starts Here",
     "ABI is 30 min from Queens. NYS-licensed since 1996. 500-hour Master Barber training with $150/week plans. Tour the Manhattan campus today.",
     "en", []),
    ("barber-school-brooklyn-new-york.html", "location-brooklyn.html",
     "Barber School Near Brooklyn, NY — Start a Career",
     "Minutes from Brooklyn by subway. ABI's NYS-licensed barber school has trained pros since 1996. 500-hour program, $150/week.",
     "en", []),
    ("barber-school-yonkers-new-york.html", "location-yonkers.html",
     "Barber School Near Yonkers, New York — Build a Real Career",
     "ABI is one of the most highly regarded barber schools near Yonkers. Train at our Bronx campus at 121 Westchester Square — 500 hours, $150/week payment plans.",
     "en", []),
    ("barber-school-westchester-ny.html", "location-westchester.html",
     "Barber School Near Westchester, NY — 4-Month Program",
     "Westchester students train at ABI's Bronx campus. Licensed Master Barber in ~4 months, 500-hour NYS-approved program from $150/week.",
     "en", []),
    ("barber-school-long-island-ny.html", "location-long-island.html",
     "Barber School Near Long Island, NY — Train in Manhattan",
     "Take the LIRR to ABI's Manhattan campus and walk to class. 500-hour Master Barber program, $150/week payment plans, job placement — training barbers since 1996.",
     "en", []),
    ("barber-school-staten-island-ny.html", "location-staten-island.html",
     "Barber School Near Staten Island, NY — Own Your Future",
     "Staten Island students: ABI's Manhattan campus is a straight ferry + walk commute. 500-hour Master Barber program in about 4 months, $150/week payment plans.",
     "en", []),
    ("barber-school-mount-vernon-ny.html", "location-mount-vernon.html",
     "Barber School Near Mount Vernon, NY — Your Path to a License",
     "Mount Vernon students: ABI's Bronx campus at Westchester Square is just over the county line. 500-hour Master Barber program, $150/week plans, job placement.",
     "en", []),
    ("barber-school-port-chester-ny.html", "location-port-chester.html",
     "Barber School Near Port Chester, NY — Become a Master Barber",
     "Port Chester students train at ABI's nearby Bronx campus. Fades, shaving, the Master Barber license — all in about 4 months with $150/week payment plans.",
     "en", []),
    ("barber-school-connecticut.html", "location-connecticut.html",
     "Barber School for Connecticut — Train in NY, Transfer",
     "CT residents: earn a NY barber license in half the time and cost, then transfer via reciprocity. 500-hour program from $150/week.",
     "en", []),
    ("barber-school-pennsylvania.html", "location-pennsylvania.html",
     "Barber School for Pennsylvania — License Transfer",
     "Transfer your NY barber license to PA via reciprocity. Save ~$10,400 and 700 hours vs a full PA program. ABI guides the process.",
     "en", []),

    # Guides hub index + guide cluster (guides/<slug>.html).
    ("guides/index.html", "guides-index.html",
     "Barber Career & Licensing Guides — American Barber Institute",
     "Free, in-depth guides to becoming a barber in New York: licensing, salary, exam prep, funding, career paths and more.",
     "en", ["FAQ_SCHEMA"]),
    ("guides/how-to-become-a-barber-in-new-york.html", "guide-how-to-become-a-barber-in-new-york.html",
     "How to Become a Barber in New York: The Complete 2026 Roadmap",
     "Every step to become a licensed barber in NY — eligibility, 500 training hours, the state board exam, fees and timelines — in one plain-English 2026 guide.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/ny-barber-license-requirements.html", "guide-ny-barber-license-requirements.html",
     "NY Barber License Requirements (2026): Hours, Exam & Fees",
     "What New York actually requires for a barber license: training hours, eligibility, the exam, fees, and how to transfer a license from another state.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/how-much-do-barbers-make-nyc.html", "guide-how-much-do-barbers-make-nyc.html",
     "How Much Do Barbers Make in NYC? 2026 New York Salary Guide",
     "Real barber pay in New York — entry, median and top earnings, plus commission vs booth rent vs shop ownership — grounded in BLS wage data.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/pass-ny-barber-state-board-exam.html", "guide-pass-ny-barber-state-board-exam.html",
     "How to Pass the NY Barber State Board Exam (2026 Guide)",
     "What's on the New York barber state board exam — written and practical — plus a prep plan and the most common reasons candidates fail.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/barber-school-vs-apprenticeship.html", "guide-barber-school-vs-apprenticeship.html",
     "Barber School vs. Apprenticeship in New York: Which Path Wins?",
     "Compare barber school and apprenticeship in NY — cost, time, structure and licensing — to choose the route that fits your life.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/barber-vs-cosmetologist.html", "guide-barber-vs-cosmetologist.html",
     "Barber vs. Cosmetologist: Which License Should You Get?",
     "Barber or cosmetologist? Compare what each does, the separate licenses, earning potential and how to decide which career fits you.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/how-long-barber-school-takes.html", "guide-how-long-barber-school-takes.html",
     "How Long Does Barber School Take? A New York Timeline",
     "500 hours becomes about 4 months full-time or 6–7 months on weekends — here's the realistic enroll-to-licensed timeline in New York.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/what-barber-school-costs.html", "guide-what-barber-school-costs.html",
     "How Much Does Barber School Cost? NY Price Ranges (2026)",
     "Typical New York barber-school tuition ranges, what's included, and the funding options — payment plans, GI Bill® and ACCES-VR — that lower the cost.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/gi-bill-barber-school.html", "guide-gi-bill-barber-school.html",
     "Using Your GI Bill® for Barber School in New York",
     "How veterans can turn Post-9/11 and other GI Bill® benefits into a licensed barber career — what's covered and how to get started.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/acces-vr-barber-training.html", "guide-acces-vr-barber-training.html",
     "ACCES-VR for Barber Training: Who Qualifies & How to Apply",
     "How New York's ACCES-VR program can fund barber training for eligible residents with a disability — eligibility, coverage and the application steps.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/beginner-barber-tool-kit.html", "guide-beginner-barber-tool-kit.html",
     "The Beginner Barber Tool Kit: What You Actually Need",
     "A no-nonsense checklist of the clippers, trimmers, shears and gear a new barber needs — with a starter budget and what to skip.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/day-in-the-life-barber-student.html", "guide-day-in-the-life-barber-student.html",
     "A Day in the Life of a Barber Student",
     "What a real training day looks like on the clinic floor — from theory to live clients — so you know exactly what barber school feels like.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/is-barbering-a-good-career.html", "guide-is-barbering-a-good-career.html",
     "Is Barbering a Good Career in 2026? Outlook, Pay & Reality",
     "An honest look at barbering as a career in 2026 — job outlook, earning potential, the pros and cons, and who thrives behind the chair.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
    ("guides/barbering-glossary.html", "guide-barbering-glossary.html",
     "Barbering Terms Glossary: 40+ Words Every New Barber Should Know",
     "Fade, taper, texturize, lineup and more — a plain-English glossary of the barbering terms you'll hear from day one.",
     "en", [FAQ_SCHEMA_PLACEHOLDER]),
]

# blog posts: content partials in src/pages/blog-*.html, listed in src/blog_manifest.json.
# For each post we resolve the named instructor author + count body words so the
# BlogPosting schema carries real E-E-A-T signals (Person author, wordCount).
_blog_manifest = os.path.join(ROOT, 'src', 'blog_manifest.json')
if os.path.exists(_blog_manifest):
    for _p in json.load(open(_blog_manifest)):
        _partial_path = os.path.join(SRC, _p['partial'])
        _body = open(_partial_path, encoding='utf-8').read() if os.path.exists(_partial_path) else None
        PAGES.append((
            f"blog/{_p['slug']}.html", _p['partial'],
            f"{_p['title']} | ABI Blog",
            f"{_p['title']} — career advice and industry insight from NYC's career-focused barber school.",
            "en", [article_schema(_p['title'], f"{SITE_URL}/blog/{_p['slug']}",
                                  slug=_p['slug'], body=_body), FAQ_SCHEMA_PLACEHOLDER]))

def gallery_video_schemas(body, limit=15):
    """Build VideoObject entries for the self-hosted (Vercel Blob) 'floor-XX'
    reel videos on the gallery page -- these had zero VideoObject schema
    despite having real, distinct captions per clip (audit 2026-07-08).
    Capped at `limit` clips: schema.org VideoObject rich results only surface
    a handful of videos per page regardless of how many are marked up, so
    cataloguing all 30+ clips across 3 different hosts wouldn't add value
    proportional to the effort -- this covers the cleanest, best-captioned set."""
    pattern = (r'<video src="(https://vutumew2863lb0bx\.public\.blob\.vercel-storage\.com/[^"]+)"\s+'
               r'poster="([^"]+)"[^>]*></video><figcaption>([^<]+)</figcaption>')
    matches = re.findall(pattern, body)[:limit]
    schemas = []
    for src, poster, caption in matches:
        poster_url = poster if poster.startswith('http') else f"{SITE_URL}/{poster}"
        schemas.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": caption,
            "description": f"{caption} — real training footage from the American Barber Institute clinic floor.",
            "thumbnailUrl": [poster_url],
            "uploadDate": "2026-07-06",
            "contentUrl": src,
        })
    return schemas


def faq_schema_from(body):
    """Build FAQPage JSON-LD from a page's <summary>/answer pairs. Supports both
    markup patterns used across the site: `<div class="a">` wrapping the answer
    (faq.html, guides), or a bare `<p>` directly after `</summary>` (dark-band
    inline-styled FAQs, e.g. tuition-and-funding.html, veterans.html)."""
    qa = re.findall(
        r'<summary[^>]*>(.*?)</summary>\s*(?:<div class="a">(.*?)</div>|<p[^>]*>(.*?)</p>)',
        body, re.S)
    items = []
    for q, a_div, a_p in qa:
        clean_a = re.sub(r'<[^>]+>', ' ', a_div or a_p)
        clean_a = re.sub(r'\s+', ' ', clean_a).strip()
        items.append({"@type": "Question", "name": re.sub(r'<[^>]+>', '', q).strip(),
                      "acceptedAnswer": {"@type": "Answer", "text": clean_a}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}

# Distinct, strong per-page background image (used by the page-hero banner and
# the subtle full-page background). Each page gets its own image.
# Per-page background — uses ONLY the client-approved image set. Each main
# page gets a distinct photo; program subpages reuse from the same set.
PAGE_BG = {
    'about.html': 'gallery/grp-01.jpg',
    'instructors.html': 'gallery/team-02.jpg',
    'jobs.html': 'gallery/cut-05.jpg', 'gallery.html': 'gallery/hair-02.jpg',
    'faq.html': 'gallery/cut-09.jpg', 'contact.html': 'gallery/shop-04.jpg', 'partners.html': 'gallery/grp-04.jpg',
    'resources.html': 'gallery/team-05.jpg', 'haircuts.html': 'gallery/cut-01.jpg',
    'programs/index.html': 'gallery/cut-13.jpg',
    'programs/manhattan.html': 'gallery/cut-22.jpg',
    'programs/bronx.html': 'gallery/grp-05.jpg',
    'programs/500-hour-master-barber.html': 'gallery/cut-22.jpg',
    'programs/500-hour-master-barber-bronx.html': 'gallery/grp-05.jpg',
    'programs/50-hour-barber-refresher.html': 'gallery/cut-18.jpg',
    'programs/contagious-diseases.html': 'gallery/grp-10.jpg',
    'blog/index.html': 'gallery/grp-02.jpg',
}
_DEFAULT_BG = 'gallery/cut-05.jpg'

# ── Per-page campus context (drives header phone routing + body theme) ──
#   'bronx'     → Bronx admissions + haircut line; body.bx-gold; data-campus=bronx
#   'both'      → Haircuts page: shows BOTH campuses' admissions + haircut line
#   'manhattan' → Manhattan admissions (EN+ES) + haircut line (default/neutral;
#                 the campus switcher lets the user flip to Bronx live)
# Anything not listed defaults to 'manhattan'/neutral.
CAMPUS_BY_PAGE = {
    'programs/500-hour-master-barber-bronx.html': 'bronx',
    'programs/bronx.html': 'bronx',
    'haircuts.html': 'both',
}

# ── Pages whose campus is part of their identity (a Bronx-titled page must
#     always show Bronx info) vs. generic shared pages (blog, guides, FAQ,
#     schedules, contact, location pages, etc.) that merely default to
#     'manhattan' with no real campus identity of their own. campus.js reads
#     data-campus-locked: locked pages always show their own data-campus AND
#     persist it as the visitor's preference; unlocked pages instead read
#     that persisted preference (localStorage) so a visitor who came from a
#     Bronx page keeps seeing Bronx admissions info as they browse shared
#     pages, instead of silently reverting to Manhattan on every other page.
LOCKED_CAMPUS_PAGES = {
    'index.html', 'bronx.html',
    'programs/manhattan.html', 'programs/bronx.html',
    'programs/500-hour-master-barber.html', 'programs/500-hour-master-barber-bronx.html',
    'haircuts.html',
}

def _campus_switch(root, campus, es=False):
    """Polished segmented Manhattan ⇄ Bronx control with a sliding indicator.
    campus.js reads data-campus / .is-active and swaps the live phone numbers.
    Both segments use absolute hrefs (like /spanish/bronx) rather than a relative
    root-prefix — a relative 'root+index.html' collapsed to the ABSOLUTE
    English '/' via clean_links() on every depth-0 ES page (es/about.html,
    es/contact.html, etc.), so switching to Manhattan from an ES page bounced
    you to the English homepage instead of /spanish/. Absolute hrefs sidestep the
    relative-path/clean_links interaction entirely and stay correct at any
    page depth or language."""
    mn_active = '' if campus == 'bronx' else ' is-active'
    bx_active = ' is-active' if campus == 'bronx' else ''
    mn_href = root + 'spanish/index.html' if es else root + 'index.html'
    bronx_href = root + 'spanish/bronx.html' if es else root + 'bronx.html'
    pin = ('<svg class="seg-pin" width="12" height="12" viewBox="0 0 24 24" fill="none" '
           'stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>'
           '<circle cx="12" cy="10" r="3"/></svg>')
    return ('<div class="seg seg-campus" role="group" aria-label="Choose campus" data-seg="campus">'
            '<span class="seg-glider" aria-hidden="true"></span>'
            '<a class="seg-opt%s" data-campus-opt="manhattan" href="%s" aria-current="%s">%s<span class="seg-lab">Manhattan</span></a>'
            '<a class="seg-opt%s" data-campus-opt="bronx" href="%s" aria-current="%s">%s<span class="seg-lab">Bronx</span></a>'
            '</div>') % (
        mn_active, mn_href, ('true' if mn_active else 'false'), pin,
        bx_active, bronx_href, ('true' if bx_active else 'false'), pin)

def _header_nav(root, es, campusswitch, langtoggle, aroot=None):
    """Full <header class="hdr2">...</header> block (logo + desktop nav +
    Book-a-Tour CTA + hamburger + mobile drawer). EN/ES-aware: on Spanish
    pages every label AND every href now stays inside /spanish/ — this was a
    sitewide gap (client 2026-07-08 audit) where the shared header showed
    English nav text and linked every ES page back to its English twin.

    `root` prefixes NAV LINKS (kept relative so ES nav stays inside /spanish/).
    `aroot` prefixes ASSET paths (the logo). On ES twins the nav-link `root` is
    the EN root (one level too shallow for an asset, since the ES page lives one
    dir deeper under /spanish/), so the caller passes aroot=es_root to keep the
    logo pointing at the real /assets/ dir. Defaults to root for EN pages."""
    aroot = root if aroot is None else aroot
    L = {
        "programs": "Programas" if es else "Programs",
        "master500": "Barbero Maestro (500 Horas)" if es else "500-Hour Master Barber",
        "refresher50": "Repaso de 50 Horas" if es else "50-Hour Refresher",
        "contagious": "Enfermedades Contagiosas" if es else "Contagious Diseases",
        "schedules": "Horarios y Flexibilidad" if es else "Schedules &amp; Flexibility",
        "why": "Por Qué ABI" if es else "Why ABI",
        "why_barbering": "Por Qué la Barbería" if es else "Why Barbering",
        "about": "Sobre Nosotros" if es else "About Us",
        "instructors": "Nuestros Instructores" if es else "Our Instructors",
        "partners": "Nuestros Socios" if es else "Our Partners",
        "training_exp": "La Experiencia de Formación" if es else "The Training Experience",
        "career_paths": "Trayectorias Profesionales" if es else "Career Paths",
        "student_stories": "Historias de Estudiantes" if es else "Student Stories",
        "guides": "Guías" if es else "Guides",
        "haircuts": "Cortes de Cabello" if es else "Haircuts",
        "tuition": "Costo y Financiamiento" if es else "Tuition &amp; Funding",
        "veterans": "Veteranos y GI Bill®" if es else "Veterans &amp; GI Bill®",
        "accesvr": "ACCES-VR" if es else "ACCES-VR",
        "contact": "Contacto" if es else "Contact",
        "book": "Reserva un Tour" if es else "Book a Tour",
        "menu": "Menú" if es else "Menu",
        "home": "inicio" if es else "home",
        "home_label": "Inicio" if es else "Home",
    }
    return (
        '<header class="hdr2">\n'
        '  <div class="hdr2-in">\n'
        f'    <a class="logo2" href="{root}index.html" aria-label="American Barber Institute — {L["home"]}" title="American Barber Institute">\n'
        f'      <img class="logo2-img" src="{aroot}assets/img/logo-final.gif" alt="American Barber Institute — 48 West 39th Street, New York, NY 10018 & 121 Westchester Square, Bronx, NY 10461" width="385" height="99" fetchpriority="high">\n'
        '    </a>\n'
        '    <nav class="nav2" aria-label="Main">\n'
        f'      <div class="nav2-item"><a class="nav2-top" href="{root}index.html">{L["home_label"]}</a></div>\n'
        '      <div class="nav2-item nav2-has">\n'
        f'        <button class="nav2-top" type="button" aria-expanded="false" aria-haspopup="true">{L["programs"]}<svg class="nav2-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>\n'
        '        <div class="nav2-menu" role="menu">\n'
        f'          <a href="{root}programs/500-hour-master-barber.html" role="menuitem">{L["master500"]}</a>\n'
        f'          <a href="{root}programs/50-hour-barber-refresher.html" role="menuitem">{L["refresher50"]}</a>\n'
        f'          <a href="{root}programs/contagious-diseases.html" role="menuitem">{L["contagious"]}</a>\n'
        f'          <a href="{root}schedules.html" role="menuitem">{L["schedules"]}</a>\n'
        '        </div>\n'
        '      </div>\n'
        '      <div class="nav2-item nav2-has">\n'
        f'        <button class="nav2-top" type="button" aria-expanded="false" aria-haspopup="true">{L["why"]}<svg class="nav2-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>\n'
        '        <div class="nav2-menu" role="menu">\n'
        f'          <a href="{root}why-barbering.html" role="menuitem">{L["why_barbering"]}</a>\n'
        f'          <a href="{root}about.html" role="menuitem">{L["about"]}</a>\n'
        f'          <a href="{root}instructors.html" role="menuitem">{L["instructors"]}</a>\n'
        f'          <a href="{root}partners.html" role="menuitem">{L["partners"]}</a>\n'
        f'          <a href="{root}training-experience.html" role="menuitem">{L["training_exp"]}</a>\n'
        f'          <a href="{root}career-paths.html" role="menuitem">{L["career_paths"]}</a>\n'
        f'          <a href="{root}student-stories.html" role="menuitem">{L["student_stories"]}</a>\n'
        '        </div>\n'
        '      </div>\n'
        f'      <div class="nav2-item"><a class="nav2-top" href="{root}guides/index.html">{L["guides"]}</a></div>\n'
        f'      <div class="nav2-item"><a class="nav2-top" href="{root}haircuts.html">{L["haircuts"]}</a></div>\n'
        '      <div class="nav2-item nav2-has">\n'
        f'        <button class="nav2-top" type="button" aria-expanded="false" aria-haspopup="true">{L["tuition"]}<svg class="nav2-caret" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>\n'
        '        <div class="nav2-menu" role="menu">\n'
        f'          <a href="{root}tuition-and-funding.html" role="menuitem">{L["tuition"]}</a>\n'
        f'          <a href="{root}veterans.html" role="menuitem">{L["veterans"]}</a>\n'
        f'          <a href="{root}access-vr-program.html" role="menuitem">{L["accesvr"]}</a>\n'
        '        </div>\n'
        '      </div>\n'
        f'      <div class="nav2-item"><a class="nav2-top" href="{root}contact.html">{L["contact"]}</a></div>\n'
        '    </nav>\n'
        f'    <a class="hdr2-cta" href="{root}contact.html#request-a-call">{L["book"]}</a>\n'
        f'    <button class="hamburger" aria-label="{L["menu"]}" aria-expanded="false" aria-controls="nav-drawer"><span></span><span></span><span></span></button>\n'
        '  </div>\n'
        '  <nav class="nav-drawer" id="nav-drawer" aria-label="Mobile"><div class="container">\n'
        f'    <a class="drawer-home" href="{root}index.html">{L["home_label"]}</a>\n'
        '    <div class="drawer-group">\n'
        f'      <p class="drawer-h">{L["programs"]}</p>\n'
        f'      <a href="{root}programs/500-hour-master-barber.html">{L["master500"]}</a>\n'
        f'      <a href="{root}programs/50-hour-barber-refresher.html">{L["refresher50"]}</a>\n'
        f'      <a href="{root}programs/contagious-diseases.html">{L["contagious"]}</a>\n'
        f'      <a href="{root}schedules.html">{L["schedules"]}</a>\n'
        '    </div>\n'
        '    <div class="drawer-group">\n'
        f'      <p class="drawer-h">{L["why"]}</p>\n'
        f'      <a href="{root}why-barbering.html">{L["why_barbering"]}</a>\n'
        f'      <a href="{root}about.html">{L["about"]}</a>\n'
        f'      <a href="{root}instructors.html">{L["instructors"]}</a>\n'
        f'      <a href="{root}partners.html">{L["partners"]}</a>\n'
        f'      <a href="{root}training-experience.html">{L["training_exp"]}</a>\n'
        f'      <a href="{root}career-paths.html">{L["career_paths"]}</a>\n'
        f'      <a href="{root}student-stories.html">{L["student_stories"]}</a>\n'
        '    </div>\n'
        '    <div class="drawer-group">\n'
        f'      <p class="drawer-h">{L["tuition"]}</p>\n'
        f'      <a href="{root}tuition-and-funding.html">{L["tuition"]}</a>\n'
        f'      <a href="{root}veterans.html">{L["veterans"]}</a>\n'
        f'      <a href="{root}access-vr-program.html">{L["accesvr"]}</a>\n'
        '    </div>\n'
        '    <div class="drawer-group">\n'
        f'      <a class="drawer-solo" href="{root}guides/index.html">{L["guides"]}</a>\n'
        f'      <a class="drawer-solo" href="{root}haircuts.html">{L["haircuts"]}</a>\n'
        f'      <a class="drawer-solo" href="{root}contact.html">{L["contact"]}</a>\n'
        '    </div>\n'
        f'    <a class="drawer-cta" href="{root}contact.html#request-a-call"><b>{L["book"]}</b></a>\n'
        '  </div></nav>\n'
        '</header>'
    )

def _footer_block(root, es):
    """CTA band + <footer> + floating desk-cta + to-top button.
    EN/ES-aware, same gap class as _header_nav: the shared footer showed
    English labels/links on every Spanish page (client 2026-07-08 audit)."""
    L = {
        "kicker": "Las clases comienzan el primer lunes de cada mes" if es else "Classes begin the first Monday of each month",
        "cta_h2": "¿Listo para Convertirte en Barbero Licenciado?" if es else "Ready to Become a Licensed Barber?",
        "cta_p_a": "La próxima clase comienza" if es else "Next class starts",
        "cta_p_b": "pronto" if es else "soon",
        "cta_p_c": ("Los cupos se llenan rápido — inscríbete, solicita una llamada, o habla con admisiones en inglés o español."
                    if es else "Seats fill fast — start your barber school enrollment, request a call, or speak with admissions in English or Spanish."),
        "start": "Empieza la Escuela de Barbería" if es else "Start Barber School",
        "speak": "Habla con Admisiones" if es else "Speak With Admissions",
        "foot_h3": "Empieza la Escuela de Barbería Hoy" if es else "Start Barber School Today",
        "foot_cta_sub": "Tu nueva carrera está a una llamada de distancia. Habla con admisiones en inglés o español." if es else "Your new career is one phone call away. Talk to admissions in English or Spanish.",
        "request_call": "Solicita una Llamada" if es else "Request a Call",
        "apply_now": "Aplicar Ahora" if es else "Apply Now",
        "foot_blurb": "La escuela de barbería de Nueva York enfocada en carreras. Licenciada por el Departamento de Educación del Estado de NY. Cambiando vidas por más de 30 años." if es else "New York's career-focused barber school. Licensed by the NY State Department of Education. Changing lives for over 30 years.",
        "programs": "Programas" if es else "Programs",
        "master500": "Barbero Maestro (500 Horas)" if es else "500-Hour Master Barber",
        "refresher50": "Repaso de 50 Horas" if es else "50-Hour Refresher",
        "contagious": "Enfermedades Contagiosas" if es else "Contagious Diseases",
        "schedules": "Horarios y Flexibilidad" if es else "Schedules &amp; Flexibility",
        "explore": "Explorar" if es else "Explore",
        "why_barbering": "Por Qué la Barbería" if es else "Why Barbering",
        "career_paths": "Trayectorias Profesionales" if es else "Career Paths",
        "tuition": "Costo y Financiamiento" if es else "Tuition &amp; Funding",
        "veterans": "Veteranos y GI Bill®" if es else "Veterans &amp; GI Bill®",
        "guides_licensing": "Guías y Licencia" if es else "Guides &amp; Licensing",
        "visit_us": "Visítanos" if es else "Visit Us",
        "privacy": "Política de Privacidad" if es else "Privacy Policy",
        "rights": "Todos los derechos reservados." if es else "All rights reserved.",
        "request_a_call_from_admissions": "Solicita una llamada de admisiones" if es else "Request a call from admissions",
        "back_to_top": "Volver arriba" if es else "Back to top",
    }
    prefix = '/spanish' if es else ''
    return (
        '<section class="cta-band">\n'
        '  <div class="wrap">\n'
        f'    <p class="kicker" style="justify-content:center">{L["kicker"]}</p>\n'
        f'    <h2>{L["cta_h2"]}</h2>\n'
        f'    <p>{L["cta_p_a"]} <span data-start-date>{L["cta_p_b"]}</span>. {L["cta_p_c"]}</p>\n'
        '    <div class="hero-ctas">\n'
        f'      <a class="btn btn-gold btn-lg" href="{root}contact.html">{L["start"]}</a>\n'
        f'      <a class="btn btn-ghost btn-lg" href="{root}contact.html">{L["speak"]}</a>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n\n'
        '<footer class="site2">\n'
        '  <div class="foot2-cta">\n'
        '    <div class="wrap">\n'
        f'      <p class="foot2-kicker">{L["kicker"]}</p>\n'
        f'      <h3>{L["foot_h3"]}</h3>\n'
        f'      <p class="foot2-cta-sub">{L["foot_cta_sub"]}</p>\n'
        '      <div class="foot-cta-btns">\n'
        f'        <a class="btn btn-gold btn-lg" href="{root}contact.html#request-a-call">{L["request_call"]}</a>\n'
        f'        <a class="btn btn-ghost2 btn-lg" href="{root}contact.html#request-a-call">{L["apply_now"]}</a>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '  <div class="wrap">\n'
        '    <div class="ftr-grid">\n'
        '      <div class="foot2-brand">\n'
        '        <p class="foot-name">American Barber Institute</p>\n'
        f'        <p class="foot2-blurb">{L["foot_blurb"]}</p>\n'
        '        <div class="socials">\n'
        '          <a class="soc soc-fb" href="https://www.facebook.com/Abi.Education/" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>\n'
        '          <a class="soc soc-ig" href="https://www.instagram.com/americanbarberinstitute/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>\n'
        '          <a class="soc soc-x" href="https://twitter.com/amerbarberedu" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3zm-1 16.2h1.7L7.3 4.7H5.5l11.3 14.5z"/></svg></a>\n'
        '          <a class="soc soc-yt" href="https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.5 12 4.5 12 4.5s-7 0-8.9.6A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.6 8.9.6 8.9.6s7 0 8.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.3V8.7L15.9 12l-6.1 3.3z"/></svg></a>\n'
        '          <a class="soc soc-pin" href="https://www.pinterest.com/alexzholendz/american-barber-institute/" aria-label="Pinterest"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.6 2-2.6.9 0 1.4.7 1.4 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.6-1.9-4.4-4.5-4.4a4.7 4.7 0 0 0-4.9 4.7c0 .9.4 1.9.8 2.5l-.3 1.1c-.1.4-.3.5-.7.3-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 1.9-1.2 2.6A10 10 0 1 0 12 2z"/></svg></a>\n'
        '        </div>\n'
        '      </div>\n'
        '      <div>\n'
        f'        <h4>{L["programs"]}</h4>\n'
        '        <ul>\n'
        f'          <li><a href="{root}programs/500-hour-master-barber.html">{L["master500"]}</a></li>\n'
        f'          <li><a href="{root}programs/50-hour-barber-refresher.html">{L["refresher50"]}</a></li>\n'
        f'          <li><a href="{root}programs/contagious-diseases.html">{L["contagious"]}</a></li>\n'
        f'          <li><a href="{root}schedules.html">{L["schedules"]}</a></li>\n'
        '        </ul>\n'
        '      </div>\n'
        '      <div>\n'
        f'        <h4>{L["explore"]}</h4>\n'
        '        <ul>\n'
        f'          <li><a href="{root}why-barbering.html">{L["why_barbering"]}</a></li>\n'
        f'          <li><a href="{root}career-paths.html">{L["career_paths"]}</a></li>\n'
        f'          <li><a href="{root}tuition-and-funding.html">{L["tuition"]}</a></li>\n'
        f'          <li><a href="{root}veterans.html">{L["veterans"]}</a></li>\n'
        f'          <li><a href="{root}guides/index.html">{L["guides_licensing"]}</a></li>\n'
        '        </ul>\n'
        '      </div>\n'
        '      <div>\n'
        f'        <h4>{L["visit_us"]}</h4>\n'
        '        <ul class="foot2-visit">\n'
        '          <li class="foot2-loc"><b>Manhattan</b><a href="https://maps.google.com/?q=48+West+39th+Street,+New+York,+NY+10018">48 West 39th Street, New York, NY 10018</a></li>\n'
        '          <li class="foot2-loc"><b>Bronx</b><a href="https://maps.google.com/?q=121+Westchester+Square,+Bronx,+NY+10461">121 Westchester Square, Bronx, NY 10461</a></li>\n'
        '          <li class="foot2-phones" data-footer-phones><a href="tel:+12122902289">(212) 290-2289 · English</a><a href="tel:+12122900278">(212) 290-0278 · Español</a><a href="tel:+17186760640">(718) 676-0640 · Bronx</a></li>\n'
        '          <li><a href="mailto:admissions@americanbarberinstitute.com">admissions@americanbarberinstitute.com</a></li>\n'
        '        </ul>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n'
        '  <div class="foot-legal">\n'
        '    <div class="wrap">\n'
        f'      <div>© <span id="yr"></span> American Barber Institute (ABI). {L["rights"]}</div>\n'
        f'      <div class="foot-legal-links"><a href="{prefix}/privacy-and-policy">{L["privacy"]}</a></div>\n'
        '      <div>GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs (VA). Info: <a href="https://www.benefits.va.gov/gibill" rel="noopener">benefits.va.gov/gibill</a></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</footer>\n\n'
        f'<a class="desk-cta" href="{root}contact.html" aria-label="{L["request_a_call_from_admissions"]}">\n'
        '  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>\n'
        f'  {L["request_call"]}\n'
        '</a>\n'
        f'<button class="to-top" aria-label="{L["back_to_top"]}" title="{L["back_to_top"]}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>'
    )

def _mbar(root, es, apply_href):
    """Sticky mobile action bar — Call Now / Text Us / Apply Now.
    Exact markup/behavior match for abi.edu's `.mbar` (client 2026-07-08:
    'fetch the abi.edu footer... exact same thing... on every page').
    Call Now is a direct tel: link (no language picker, matching abi.edu's
    own simplification — the ubar/mstrip further up the page already offer
    the Spanish number). Text Us always goes to the shared GHL AI SMS line."""
    call_svg = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                '<path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1'
                'C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>')
    text_svg = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1'
                '-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>')
    apply_svg = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                 '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>'
                 '<line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/>'
                 '<line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>')
    call_label = "Llamar" if es else "Call Now"
    text_label = "Mensaje" if es else "Text Us"
    apply_label = "Aplicar" if es else "Apply Now"
    return (
        '<div class="mbar">\n'
        '  <a class="mbar-call" href="tel:+12122902289">%s <span>%s</span></a>\n'
        '  <a class="mbar-text" href="sms:+19295888448?&amp;body=Hi%%2C%%20how%%20are%%20you%%3F">%s <span>%s</span></a>\n'
        '  <a class="mbar-cta" href="%s">%s <span>%s</span></a>\n'
        '</div>'
    ) % (call_svg, call_label, text_svg, text_label, apply_href, apply_svg, apply_label)

def _lang_toggle(root, out):
    """Segmented EN | ES control with a globe icon + sliding indicator.
    Every EN page now has a Spanish twin at /spanish/<slug>, so the ES link
    points there — Spanish visitors stay on the same content, not the ES home."""
    globe = ('<svg class="seg-globe" width="12" height="12" viewBox="0 0 24 24" fill="none" '
             'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
             'aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
             '<path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18z"/></svg>')
    if out.startswith('spanish/'):
        en_href, es_href = '%s%s' % (root, out[8:]), '%s%s' % (root, out)
        en_a, es_a = '', ' is-active'
    else:
        en_href, es_href = '%s%s' % (root, out), '%sspanish/%s' % (root, out)
        en_a, es_a = ' is-active', ''
    return ('<div class="seg seg-lang" role="group" aria-label="Language" data-seg="lang">'
            '<span class="seg-glider" aria-hidden="true"></span>'
            '<a class="seg-opt%s" href="%s" aria-current="%s">%s<span class="seg-lab" data-short="EN">English</span></a>'
            '<a class="seg-opt%s" href="%s" aria-current="%s"><span class="seg-lab" data-short="ES">Español</span></a>'
            '</div>') % (
        en_a, en_href, ('true' if en_a else 'false'), globe,
        es_a, es_href, ('true' if es_a else 'false'))

# ── ES META — Spanish title + description for every EN page ─────────────
# Body content still English for now (a small Spanish banner is prepended
# via ES_BANNER at build time). Real Spanish translations are Phase 2.
ES_META = {
    'about.html': ("¿Es ABI la escuela de barbería adecuada para ti? Conoce al equipo",
                   "Cómo el American Barber Institute ayuda a quienes cambian de carrera a convertirse en barberos licenciados en NY: nuestros mentores, formación práctica y más de 30 años construyendo carreras detrás de la silla."),
    'instructors.html': ("¿Quién te enseñará a ser barbero? Conoce a los mentores de ABI",
                         "Las personas que forjan tu carrera: los instructores maestros de ABI, incluidos King David Ayeoribe y Harold “Barkim” Brown, con más de 50 años combinados detrás de la silla."),
    'jobs.html': ("¿Qué puedes hacer después de la escuela de barbería? Salidas profesionales",
                  "A dónde puede llevarte una licencia de barbero — sillas de barbería, alquiler de espacio, tu propio negocio — y cómo el apoyo de colocación laboral de ABI ayuda a los graduados."),
    'gallery.html': ("Ve cómo se ve realmente el entrenamiento — trabajos de estudiantes y sala",
                     "Un vistazo a los cortes reales de estudiantes, la clínica y el día a día del entrenamiento para ser barbero — para que sepas dónde te inscribes antes de firmar."),
    'haircuts.html': ("¿Quieres un corte a $3 — o tiempo de silla como estudiante? Cómo funciona la clínica",
                      "Por qué importa la clínica de estudiantes de $3: es donde practican horas reales con clientes reales. Reserva un corte en Manhattan o el Bronx."),
    'faq.html': ("¿Piensas en la escuela de barbería? Tus preguntas, contestadas",
                 "Respuestas directas sobre costo, duración del entrenamiento, horarios, requisitos de edad, financiamiento y colocación laboral — todo para decidir si la barbería es tu próximo paso."),
    'schedules.html': ("¿Puedes encajar el entrenamiento en tu vida? Horarios y flexibilidad",
                       "Mañana, tarde o fin de semana — cómo el programa de 500 horas de ABI cabe con un trabajo o familia. Tiempo completo termina en unos 4 meses; fines de semana en 6–7. Nuevas clases el primer lunes de cada mes."),
    'contact.html': ("¿Listo para el primer paso? Reserva un tour o habla con Admisiones",
                     "Visita el campus antes de comprometerte. Reserva un tour en 48 West 39th Street, NYC — minutos de Penn Station, Grand Central y Times Square — o habla en inglés o español."),
    'resources.html': ("Juntas de licencias de barbería y recursos por estado — comienza aquí",
                       "Los organismos reguladores, juntas estatales de barbería y cosmetología, y recursos de la industria que necesitarás al planificar tu camino como barbero licenciado."),
    'partners.html': ("¿Dónde acaban trabajando los barberos de ABI? Nuestra red de barberías",
                      "Las barberías de NYC que contratan y capacitan a nuestros graduados — Levels, Diamond Fadez, Untouchable Cutz, Expo Gentlemen, Otis & Finn y el NYC Barber Shop Museum."),
    '404.html': ("¿Perdido? Volvamos al camino de la barbería",
                 "Esta página tomó un giro equivocado. Regresa al inicio del American Barber Institute o explora cómo comenzar tu carrera."),
    'bronx.html': ("Entrenamiento en el campus del Bronx: cómo es",
                   "El programa de 500 horas en el Bronx (121 Westchester Square) — instrucción bilingüe, horarios flexibles, planes de pago semanales y apoyo de colocación laboral."),
    'why-barbering.html': ("¿Por qué la barbería? Una carrera que no puede ser reemplazada por IA",
                           "Por qué la barbería sigue siendo una carrera resistente: demanda estable, ingresos que crecen con la destreza, dueño de tu propio libro de clientes."),
    'training-experience.html': ("La experiencia de entrenamiento en ABI",
                                 "Cómo se ve realmente el entrenamiento en ABI — teoría, práctica en clientes reales, preparación para el examen — de manera que sepas qué esperar."),
    'career-paths.html': ("Trayectorias profesionales para barberos licenciados en NY",
                          "Sillas de barbería, alquiler de espacio, tu propio negocio o educador — todos los caminos que abre una licencia de barbero maestro en NY."),
    'student-stories.html': ("Historias de estudiantes: vidas transformadas detrás de la silla",
                             "Voces reales de graduados de ABI — cambios de carrera, veteranos, inmigrantes — que ahora ganan su vida con la barbería."),
    'skills-and-techniques.html': ("Habilidades y técnicas que dominarás",
                                   "Fades clásicos, mid, high y bald; taperes, pompadours, líneas con navaja, afeitados con toalla caliente — todo lo que aprenderás en las 500 horas."),
    'is-barber-training-right-for-you.html': ("¿Es el entrenamiento de barbería adecuado para ti?",
                                              "Una guía honesta para decidir si la barbería encaja con tu personalidad, tu ritmo de aprendizaje y tus metas — antes de gastar tiempo o dinero."),
    'how-to-get-started.html': ("Cómo empezar tu carrera de barbero",
                                "Los pasos claros para inscribirte: tour, elección de horario, financiamiento, matrícula y primer día en la clínica."),
    'ny-barber-licensing-checklist.html': ("Lista de verificación para la licencia de barbero en NY",
                                           "Todo lo que necesitas — documentos, horas, examen, tarifas — para obtener tu licencia de barbero maestro en el estado de Nueva York."),
    'financial-aid.html': ("Ayuda financiera para barbería en ABI",
                           "GI Bill®, ACCES-VR, planes de pago semanales y otros caminos para pagar tu entrenamiento en ABI."),
    'tuition-and-funding.html': ("Costo y ayuda financiera: cómo pagar la escuela de barbería",
                                 "Cuánto cuesta el programa de 500 horas y los caminos de financiamiento — pagos semanales, GI Bill®, ACCES-VR — que reducen el costo real."),
    'veterans.html': ("Veteranos: cómo usar tu GI Bill® para la escuela de barbería",
                      "Cómo los veteranos pueden convertir los beneficios del Post-9/11 y otras versiones del GI Bill® en una carrera de barbería licenciada."),
    'access-vr-program.html': ("¿ACCES-VR podría cubrir tu entrenamiento de barbería?",
                               "Cómo el programa ACCES-VR de Nueva York puede financiar la formación de barbero para residentes elegibles con una discapacidad — elegibilidad, cobertura y pasos."),
    'virtual-tour.html': ("Recorrido virtual del campus de ABI",
                          "Ve el interior de nuestras aulas y clínicas de Manhattan y el Bronx sin salir de casa."),
    'shop-registration.html': ("¿Necesitas registrar tu barbería? Cómo funciona",
                               "Registra tu barbería con ABI para acceder a graduados listos para contratar y publicar vacantes."),
    'privacy-and-policy.html': ("Política de privacidad | American Barber Institute",
                                "Cómo el American Barber Institute recopila, usa y protege tu información personal."),
    'programs/index.html': ("¿Qué programa de barbería es para ti? Compara tus opciones",
                            "Compara los tres caminos de ABI: 500 horas (licencia de NY), 50 horas de repaso para profesionales licenciados, y el curso de Enfermedades Contagiosas de 3 horas."),
    'programs/manhattan.html': ("Programas del campus de Manhattan | American Barber Institute",
                                "Cada programa de barbería en nuestro campus de Midtown Manhattan (48 West 39th Street): 500 horas de Barbero Maestro, 50 horas de Repaso (solo Manhattan) y 3 horas de Enfermedades Contagiosas."),
    'programs/bronx.html': ("Programas del campus del Bronx | American Barber Institute",
                            "Cada programa en nuestro campus del Bronx (121 Westchester Square, junto al tren 6): 500 horas de Barbero Maestro y 3 horas de Enfermedades Contagiosas. Aprobado por NYSED con planes de pago semanales e instrucción bilingüe."),
    'programs/500-hour-master-barber.html': ("El viaje de 500 horas — de principiante a licenciado",
                                             "Lo que se necesita para pasar del primer fade a barbero maestro licenciado en nuestro campus de Manhattan: 500 horas prácticas en unos 4 meses, mañana, tarde o fin de semana, desde $4,600."),
    'programs/500-hour-master-barber-bronx.html': ("Conviértete en barbero licenciado en el Bronx — la ruta de 500 horas",
                                                   "Tu transformación en el campus del Bronx de ABI: 500 horas de entrenamiento bilingüe y práctico en unos 4 meses, horarios flexibles, planes de pago y apoyo de colocación laboral."),
    'programs/50-hour-barber-refresher.html': ("¿Ya licenciado? Cómo el Repaso de 50 horas te prepara para el examen",
                                               "Para cosmetólogos, estilistas y aprendices: pule tus habilidades y prepárate para el examen estatal en unas 2 semanas en nuestro campus de Manhattan."),
    'programs/contagious-diseases.html': ("¿Necesitas el curso de Enfermedades Contagiosas? Cómo completarlo",
                                          "El curso requerido de Enfermedades Contagiosas para operadores de barbería y aprendices en NY, explicado. Complétalo por correo por $100."),
    'blog/index.html': ("Guías de carrera en barbería — licencia, dinero y vida detrás de la silla",
                        "La biblioteca del American Barber Institute con guías honestas sobre licencia, salario, colocación laboral y qué esperar realmente detrás de la silla."),
    'guides/index.html': ("Guías de carrera y licencia de barbería — American Barber Institute",
                          "Guías gratuitas y detalladas para convertirte en barbero en Nueva York: licencia, salario, preparación para el examen, financiamiento, trayectorias y más."),
    'guides/how-to-become-a-barber-in-new-york.html': ("Cómo convertirte en barbero en Nueva York: hoja de ruta 2026",
                                                       "Cada paso para obtener una licencia de barbero en NY — elegibilidad, 500 horas de entrenamiento, examen estatal, tarifas y tiempos — en una guía 2026 en inglés claro."),
    'guides/ny-barber-license-requirements.html': ("Requisitos de licencia de barbero en NY (2026): horas, examen y tarifas",
                                                   "Lo que Nueva York realmente exige para una licencia de barbero: horas de entrenamiento, elegibilidad, examen, tarifas y cómo transferir una licencia de otro estado."),
    'guides/how-much-do-barbers-make-nyc.html': ("¿Cuánto ganan los barberos en NYC? Guía salarial 2026",
                                                  "Pago real de barberos en Nueva York — inicial, mediano y máximo, más comisión vs alquiler de espacio vs dueño — basado en datos del BLS."),
    'guides/pass-ny-barber-state-board-exam.html': ("Cómo aprobar el examen estatal de barbería de NY (guía 2026)",
                                                    "Qué contiene el examen estatal de barbería de NY — escrito y práctico — más un plan de preparación y las razones más comunes de fracaso."),
    'guides/barber-school-vs-apprenticeship.html': ("Escuela de barbería vs aprendizaje en NY: ¿cuál gana?",
                                                    "Compara la escuela de barbería y el aprendizaje en NY — costo, tiempo, estructura y licencia — para elegir la ruta que te conviene."),
    'guides/barber-vs-cosmetologist.html': ("Barbero vs cosmetólogo: ¿qué licencia deberías obtener?",
                                            "¿Barbero o cosmetólogo? Compara qué hace cada uno, las licencias separadas, el potencial de ingresos y cómo decidir cuál carrera te conviene."),
    'guides/how-long-barber-school-takes.html': ("¿Cuánto dura la escuela de barbería? Línea de tiempo NY",
                                                 "500 horas equivalen a unos 4 meses tiempo completo o 6–7 meses fines de semana — aquí está el cronograma realista de inscripción a licencia en NY."),
    'guides/what-barber-school-costs.html': ("¿Cuánto cuesta la escuela de barbería? Rangos de precios NY (2026)",
                                             "Rangos típicos de matrícula en escuelas de barbería en NY, qué incluye, y las opciones de financiamiento — planes de pago, GI Bill® y ACCES-VR."),
    'guides/gi-bill-barber-school.html': ("Usar tu GI Bill® para la escuela de barbería en Nueva York",
                                          "Cómo los veteranos pueden convertir los beneficios Post-9/11 y otros de GI Bill® en una carrera de barbería licenciada — qué cubre y cómo empezar."),
    'guides/acces-vr-barber-training.html': ("ACCES-VR para entrenamiento de barbería: quién califica y cómo aplicar",
                                             "Cómo el programa ACCES-VR de NY puede financiar el entrenamiento de barbería para residentes elegibles con una discapacidad — elegibilidad, cobertura y pasos."),
    'guides/beginner-barber-tool-kit.html': ("El kit del barbero principiante: lo que realmente necesitas",
                                             "Una lista sin rodeos de las clippers, trimmers, tijeras y equipo que necesita un nuevo barbero — con un presupuesto inicial y qué evitar."),
    'guides/day-in-the-life-barber-student.html': ("Un día en la vida de un estudiante de barbería",
                                                   "Cómo es un día real de entrenamiento en la clínica — desde la teoría hasta clientes en vivo — para que sepas exactamente cómo se siente la escuela de barbería."),
    'guides/is-barbering-a-good-career.html': ("¿Es la barbería una buena carrera en 2026? Perspectiva y realidad",
                                               "Una mirada honesta a la barbería como carrera en 2026 — perspectiva laboral, potencial de ingresos, ventajas y desventajas, y quién prospera."),
    'guides/barbering-glossary.html': ("Glosario de barbería: 40+ términos que todo nuevo barbero debe conocer",
                                       "Fade, taper, texturize, lineup y más — un glosario en español claro de los términos de barbería que escucharás desde el primer día."),
}
# Bespoke Spanish title/desc for the 10 location pages (previously fell through
# to the English fallback -> duplicate EN meta on the ES twin) and the 11 blog
# posts (previously auto-generated). Added 2026-07-14 alongside full-body ES
# translation of these pages. Keyed by the EN `out` path, same as ES_META.
ES_META.update({
    # ── Location pages (fixes duplicate-EN-title bug on /spanish/ twins) ──
    'barber-school-queens-ny.html': ("Escuela de Barbería cerca de Queens, NY | Tu Carrera",
                                      "ABI está a 30 min de Queens. Con licencia de NY desde 1996. Maestro Barbero de 500 horas con planes de $150/semana. Visita el campus de Manhattan hoy."),
    'barber-school-brooklyn-new-york.html': ("Escuela de Barbería cerca de Brooklyn, NY — Inicia tu Carrera",
                                             "A minutos de Brooklyn en metro. La escuela de barbería de ABI, con licencia de NY, forma profesionales desde 1996. Programa de 500 horas, $150/semana."),
    'barber-school-yonkers-new-york.html': ("Escuela de Barbería cerca de Yonkers, NY — Carrera Real",
                                            "ABI es una de las escuelas de barbería más reconocidas cerca de Yonkers. Fórmate en el campus del Bronx: 500 horas y planes de pago desde $150/semana."),
    'barber-school-westchester-ny.html': ("Escuela de Barbería cerca de Westchester, NY — 4 Meses",
                                          "Estudiantes de Westchester se forman en el campus del Bronx de ABI. Barbero Maestro con licencia en ~4 meses, programa de 500 horas desde $150/semana."),
    'barber-school-long-island-ny.html': ("Escuela de Barbería en Manhattan cerca de Long Island, NY",
                                          "Toma el LIRR al campus de ABI en Manhattan. Programa Master Barber de 500 horas, planes de pago de $150/semana y colocación laboral. Desde 1996."),
    'barber-school-staten-island-ny.html': ("Escuela de Barbería cerca de Staten Island, NY",
                                            "Estudiantes de Staten Island: el campus de ABI en Manhattan queda a un ferry. Barbero Maestro de 500 horas en ~4 meses, planes de $150/semana."),
    'barber-school-mount-vernon-ny.html': ("Escuela de Barbería cerca de Mount Vernon, NY",
                                           "Estudiantes de Mount Vernon: el campus del Bronx de ABI en Westchester Square está a minutos. Master Barber de 500 h, planes de $150/semana y colocación."),
    'barber-school-port-chester-ny.html': ("Escuela de Barbería cerca de Port Chester, NY — Barbero Maestro",
                                           "Estudiantes de Port Chester se forman en el campus del Bronx de ABI. Fades, afeitado y licencia de Barbero Maestro en ~4 meses; planes de $150/semana."),
    'barber-school-connecticut.html': ("Escuela de Barbería para Connecticut — Estudia en NY y Transfiere",
                                       "Residentes de CT: obtén tu licencia de barbero de NY en mitad de tiempo y costo, luego transfiérela por reciprocidad. Programa de 500 horas desde $150/semana."),
    'barber-school-pennsylvania.html': ("Escuela de Barbería para Pensilvania — Transferir Licencia",
                                        "Transfiere tu licencia de barbero de NY a PA por reciprocidad. Ahorra ~$10,400 y 700 horas frente al programa completo de PA. ABI te guía en el proceso."),
    # ── Blog posts (upgrade from auto-generated to bespoke Spanish meta) ──
    'blog/why-should-i-go-to-barber-school.html': ("¿Vale la pena la escuela de barbería? | Blog ABI",
                                                   "¿Vale la pena la escuela de barbería? Consejos de carrera y perspectiva del sector desde una escuela de barbería de NYC enfocada en tu futuro laboral."),
    'blog/a-women-barber-the-benefits-of-barber-school.html': ("Mujer barbera: las ventajas de la escuela de barbería | Blog ABI",
                                                              "Ser mujer barbera: las ventajas de la escuela de barbería y cómo abrirte camino detrás de la silla — consejos de carrera de una escuela de NYC."),
    'blog/are-barbershops-profitable-everything-you-need-t.html': ("¿Son rentables las barberías? Todo lo que debes saber | Blog ABI",
                                                                   "¿Son rentables las barberías? Todo lo que debes saber: consejos de carrera y visión del sector desde la escuela de barbería enfocada en la carrera de NYC."),
    'blog/first-things-first-what-happens-after-barber-sch.html': ("¿Qué pasa después de la escuela de barbería? | Blog ABI",
                                                                   "Lo primero es lo primero: qué pasa después de la escuela de barbería — licencia, primer empleo y próximos pasos, según una escuela de NYC."),
    'blog/how-to-successfully-market-your-barbershop.html': ("Cómo promocionar tu barbería con éxito | Blog ABI",
                                                            "Cómo promocionar tu barbería con éxito: estrategias para atraer clientes y llenar tu silla, con consejos de una escuela de barbería de NYC."),
    'blog/modern-day-barbering-problem-overcome-them.html': ("Problemas de la barbería moderna y cómo superarlos | Blog ABI",
                                                            "Los problemas de la barbería moderna y cómo superarlos: retos reales detrás de la silla y soluciones prácticas, según una escuela de NYC."),
    'blog/diverse-haircut-training-at-american-barber-inst.html': ("Entrenamiento en cortes diversos en ABI | Blog ABI",
                                                                  "Entrenamiento en cortes diversos en American Barber Institute: consejos de carrera e ideas del sector desde una escuela de barbería de NYC."),
    'blog/barber-school-instructors-in-nyc.html': ("Instructores de escuela de barbería en NYC | Blog ABI",
                                                   "Conoce a los instructores de escuela de barbería en NYC: quién te enseña y por qué importa, desde una escuela de barbería enfocada en la carrera."),
    'blog/exploring-the-benefits-of-enrolling-in-the-ameri.html': ("Ventajas de estudiar en American Barber Institute | Blog ABI",
                                                                  "Beneficios de estudiar en American Barber Institute: consejos de carrera y visión del sector desde la escuela de barbería de NYC enfocada en tu futuro."),
    'blog/affordable-barber-school-nyc.html': ("Escuela de Barbería Económica en NYC sin Arruinarte | Blog ABI",
                                               "Escuela de barbería económica en NYC: formación de calidad con licencia de 500 horas y planes de pago semanales, sin arruinar tu presupuesto."),
    'blog/how-much-money-do-barbers-make.html': ("¿Cuánto ganan los barberos? Guía de ingresos | Blog ABI",
                                                 "Cuánto ganan los barberos en Nueva York en 2026: una guía de ingresos por etapa de carrera, de recién graduado a dueño de barbería."),
})
# Blog posts get an auto-generated ES title/desc (translation deferred).
ES_BANNER = ('<div style="background:linear-gradient(90deg,#0E8C82,#12B3A6);color:#fff;'
             'padding:.65rem 1rem;text-align:center;font-size:.92rem;font-weight:600;'
             'letter-spacing:.01em">Traducción completa en español próximamente — '
             'contenido en inglés a continuación. '
             '<a href="/contact" style="color:#fff;text-decoration:underline">Contáctanos en español al (212) 290-0278</a>.</div>')

def build():
    written = []
    for out, partial, title, desc, lang, schemas in PAGES:
        path = os.path.join(SRC, partial)
        if not os.path.exists(path):
            print(f'  !! missing partial {partial} — skipped')
            continue
        body = open(path, encoding='utf-8').read()
        # Inject a small named-author byline at the top of each blog post (E-E-A-T).
        # The same human author + role is already referenced in the BlogPosting schema.
        if out.startswith('blog/') and out != 'blog/index.html':
            _slug = out[len('blog/'):-len('.html')]
            _bname, _brole = BLOG_AUTHORS.get(_slug, ("David Ayeoribe", "Lead Senior Instructor & Director"))
            _byline = (
                '<p class="post-meta" style="margin:.4rem 0 1.6rem;font-size:.92rem;'
                'color:#5b6273;letter-spacing:.01em">'
                f'By <a href="/instructors" rel="author" style="color:inherit;text-decoration:underline">'
                f'<span itemprop="author">{_bname}</span></a> · {_brole} · '
                '<time datetime="2024-02-01" itemprop="datePublished">February 1, 2024</time>'
                '</p>'
            )
            # Drop the byline right after the first </h1> if there is one,
            # otherwise prepend to the body.
            if '</h1>' in body:
                body = body.replace('</h1>', '</h1>' + _byline, 1)
            else:
                body = _byline + body
        depth = out.count('/')
        # 404.html is served by Vercel for any unknown URL — at any depth — so its
        # asset/nav references MUST be absolute (root = '/') not relative.
        root = '/' if out == '404.html' else ('../' * depth)
        if out == '404.html':
            # 404 must not be indexed and must not claim a canonical URL of its own
            # (avoids soft-404 signals). Point self-referential meta at the home.
            canonical = f"{SITE_URL}/"
        else:
            canonical = f"{SITE_URL}/{out}".replace('/index.html', '/').replace('.html', '')
        resolved = []
        for s in schemas:
            if s == FAQ_SCHEMA_PLACEHOLDER:
                resolved.append(faq_schema_from(body))
            elif s == VIDEO_SCHEMA_PLACEHOLDER:
                resolved.extend(gallery_video_schemas(body))
            else:
                resolved.append(s)
        # BreadcrumbList for every page (entity clarity for AI/answer engines)
        crumb_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
        is_home = out in ('index.html',)
        if not is_home:
            short = re.sub(r'\s*[|—].*$', '', title).strip()
            crumb_items.append({"@type": "ListItem", "position": 2, "name": short, "item": canonical})
        resolved.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                         "itemListElement": crumb_items})
        # LocalBusiness/TradeSchool on every page (local SEO + AI grounding)
        if ORG_SCHEMA not in resolved:
            resolved.append(ORG_SCHEMA)
        # VideoObject markup for pages that embed YouTube clips (rich results)
        for vs in VIDEO_SCHEMAS.get(out, []):
            resolved.append(vs)
        schema_tags = '\n'.join(
            f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
            for s in resolved)
        # Segmented EN|ES + Manhattan⇄Bronx switchers (see helpers above).
        campus = CAMPUS_BY_PAGE.get(out.replace('spanish/', ''), 'manhattan')
        langtoggle = _lang_toggle(root, out)
        campusswitch = _campus_switch(root, campus)
        mbar = _mbar(root, False, root + 'contact.html#request-a-call')
        header_nav = _header_nav(root, False, campusswitch, langtoggle)
        footer_block = _footer_block(root, False)
        # Body theme + data-campus so campus.js renders the right phones on load.
        # 'both' (Haircuts) stays neutral/manhattan-themed but flags data-campus=both.
        bodyclass = ' bx-gold' if campus == 'bronx' else ''
        datacampus = campus
        campuslocked = 'true' if out.replace('spanish/', '') in LOCKED_CAMPUS_PAGES else 'false'
        # hreflang reciprocity: every EN page declares itself as en + x-default;
        # the home page additionally declares the ES alternate (and vice-versa).
        # Only the home page has a Spanish counterpart today.
        _en_home = SITE_URL + "/"
        _es_home = SITE_URL + "/spanish/"
        if out in ('index.html',):
            hreflang_block = (
                f'<link rel="alternate" hreflang="en" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="es" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{_en_home}">'
            )
        elif out.startswith('spanish/'):
            hreflang_block = (
                f'<link rel="alternate" hreflang="es" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="en" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{_en_home}">'
            )
        else:
            # Every EN page now has a Spanish twin at /spanish/<slug> — declare it
            _es_alt = f"{SITE_URL}/spanish/{out}".replace('/index.html', '/').replace('.html', '')
            hreflang_block = (
                f'<link rel="alternate" hreflang="en" href="{canonical}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{canonical}">\n'
                f'<link rel="alternate" hreflang="es" href="{_es_alt}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{_es_alt}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{canonical}">'
            )
        html = TEMPLATE.format(
            lang=lang, title=title, desc=desc, canonical=canonical, site=SITE_URL,
            oglocale='es_ES' if lang == 'es' else 'en_US',
            pagebg=PAGE_BG.get(out.replace('spanish/', ''), _DEFAULT_BG),
            root=root, body=body, schema=schema_tags, langtoggle=langtoggle,
            campusswitch=campusswitch, bodyclass=bodyclass, datacampus=datacampus, campuslocked=campuslocked,
            hreflang_block=hreflang_block, mbar=mbar, header_nav=header_nav, footer_block=footer_block,
            lp=root + 'programs/index.html',
            en_cur='aria-current="true"' if lang == 'en' else '',
            es_cur='aria-current="true"' if lang == 'es' else '')
        # Bake real next-class date + countdown defaults so they never render
        # as "0"/empty without JS (JS still enhances them to a live countdown).
        html = (html
                .replace('<span class="date" data-start-date>First Monday of next month</span>',
                         '<span class="date" data-start-date>%s</span>' % NEXT_START_LONG)
                .replace('<b data-d>0</b>', '<b data-d>%s</b>' % CD_D)
                .replace('<b data-h>0</b>', '<b data-h>%s</b>' % CD_H)
                .replace('<b data-m>0</b>', '<b data-m>%s</b>' % CD_M)
                .replace('<b data-s>0</b>', '<b data-s>%s</b>' % CD_S))
        # 404 page must not be indexed by search engines.
        if out == '404.html':
            html = html.replace(
                '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
                '<meta name="robots" content="noindex">')
        html = clean_links(html)
        dest = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(html)
        if out != '404.html':  # keep the error page out of the sitemap
            written.append(out)

        # ── ES TWIN — emit /spanish/<same-path> for every EN page ────────
        # Reuses the same English partial body prefixed with a Spanish
        # notification banner. <html lang="es">, ES title/desc/hreflang.
        # This guarantees every URL has a Spanish counterpart at /spanish/<slug>
        # so language toggles + Google's hreflang crawl land on real pages.
        # (URL segment is "spanish" not "es" — matches the old WordPress
        # site's existing, already-indexed Spanish URL convention.)
        if lang == 'en' and out != 'spanish/index.html':
            es_out = 'spanish/' + out
            es_meta = ES_META.get(out)
            if not es_meta and out.startswith('blog/'):
                # Blog posts without a bespoke ES_META entry fall back to a
                # templated title/desc. Previously the description was 100%
                # identical across all such posts (a duplicate-meta-description
                # SEO gap, audit 2026-07-08) -- now interpolates the post's own
                # title so each is at least unique, matching how the EN
                # description is built two lines above this block.
                _clean_title = title.replace(' | ABI Blog', '')
                es_meta = (title.replace('| ABI Blog', '| Blog ABI') if '| ABI Blog' in title else title + ' (Español)',
                           f'{_clean_title} — consejos de carrera e información de la industria '
                           'de la escuela de barbería de NYC enfocada en carreras.')
            if not es_meta:
                es_meta = (title, desc)  # last-resort fallback
            es_title, es_desc = es_meta
            es_canonical = f"{SITE_URL}/spanish/{out}".replace('/index.html', '/').replace('.html', '')
            es_en_href = canonical
            es_root = '../' + ('../' * out.count('/'))
            es_langtoggle = _lang_toggle('/' if out == 'index.html' else es_root, 'spanish/' + out)
            # apply_href uses `root` (not `es_root`) — it links to the ES-sibling
            # contact page (es/contact.html), which sits at the SAME relative
            # depth within es/ as `root` describes within the site root.
            es_mbar = _mbar(es_root, True, root + 'contact.html#request-a-call')
            # Same insight for the header/nav/drawer: use plain `root` (not
            # es_root) so every nav link stays inside the es/ subtree instead
            # of jumping back to the English page at the repo root.
            es_campusswitch = _campus_switch(es_root, campus, es=True)
            es_header_nav = _header_nav(root, True, es_campusswitch, es_langtoggle, aroot=es_root)
            es_footer_block = _footer_block(root, True)
            es_hreflang_block = (
                f'<link rel="alternate" hreflang="en" href="{es_en_href}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{es_en_href}">\n'
                f'<link rel="alternate" hreflang="es" href="{es_canonical}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{es_canonical}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{es_en_href}">'
            )
            # Body partials hardcode relative asset paths (src="assets/..." or
            # src="../assets/...") sized for THEIR OWN EN depth. The ES twin
            # always lives exactly one directory level deeper (es/<same-path>),
            # so every such relative reference needs exactly one extra '../'
            # prepended, or it 404s (e.g. es/gallery's images resolving to
            # /spanish/assets/... instead of /assets/...). Absolute (/assets/...)
            # and external (http...) references are untouched.
            #
            # REAL TRANSLATION OVERRIDE: if src/pages/es-<partial> exists,
            # use its (fully Spanish, human-translated) body instead of the
            # English-passthrough + banner. Translators keep asset paths
            # byte-identical to the English partial (same relative depth) —
            # the same depth-fix regex below normalizes them for the ES twin,
            # so translated partials never need their own path arithmetic.
            _es_override_path = os.path.join(SRC, 'es-' + partial)
            _real_translation = os.path.exists(_es_override_path)
            _source_body = open(_es_override_path, encoding='utf-8').read() if _real_translation else body
            # ES blog posts get the same author byline as EN (E-E-A-T parity),
            # rendered in Spanish and linking to the Spanish instructors page.
            if _real_translation and out.startswith('blog/') and out != 'blog/index.html':
                _es_slug = out[len('blog/'):-len('.html')]
                _es_bname, _es_brole = BLOG_AUTHORS.get(_es_slug, ("David Ayeoribe", "Lead Senior Instructor & Director"))
                _ES_ROLE = {
                    "Lead Senior Instructor & Director": "Instructor Principal Senior y Director",
                    "Lead Instructor": "Instructor Principal",
                    "Founding Director, ABI Bronx": "Director Fundador, ABI Bronx",
                }
                _es_role_es = _ES_ROLE.get(_es_brole, _es_brole)
                _es_byline = (
                    '<p class="post-meta" style="margin:.4rem 0 1.6rem;font-size:.92rem;'
                    'color:#5b6273;letter-spacing:.01em">'
                    'Por <a href="/spanish/instructors" rel="author" style="color:inherit;text-decoration:underline">'
                    f'<span itemprop="author">{_es_bname}</span></a> · {_es_role_es} · '
                    '<time datetime="2024-02-01" itemprop="datePublished">1 de febrero de 2024</time>'
                    '</p>'
                )
                if '</h1>' in _source_body:
                    _source_body = _source_body.replace('</h1>', '</h1>' + _es_byline, 1)
                else:
                    _source_body = _es_byline + _source_body
            _fixed_body = re.sub(
                r'((?:src|href)=")((?:\.\./)*)(assets/)',
                lambda m: m.group(1) + '../' + m.group(2) + m.group(3),
                _source_body
            )
            # Real translations don't need the "coming soon" banner.
            es_body = _fixed_body if _real_translation else (ES_BANNER + '\n' + _fixed_body)
            # ── ES-SPECIFIC STRUCTURED DATA (audit 2026-07-16) ───────────────
            # Previously every Spanish page reused the English `schema_tags`
            # verbatim: FAQPage answers, the BreadcrumbList name/URL, and the
            # sitewide Organization description/slogan were all English on a
            # Spanish page. Rebuilt here from the Spanish title/canonical/body
            # (the real translated body when one exists, matching what the
            # visible page actually says) instead of reusing the EN version.
            es_resolved = []
            for s in schemas:
                if s == FAQ_SCHEMA_PLACEHOLDER:
                    es_resolved.append(faq_schema_from(_fixed_body))
                elif s == VIDEO_SCHEMA_PLACEHOLDER:
                    es_resolved.extend(gallery_video_schemas(_fixed_body))
                else:
                    es_resolved.append(s)
            es_crumb_items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE_URL + "/"}]
            if not is_home:
                es_short = re.sub(r'\s*[|—].*$', '', es_title).strip()
                es_crumb_items.append({"@type": "ListItem", "position": 2, "name": es_short, "item": es_canonical})
            es_resolved.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                                "itemListElement": es_crumb_items})
            if ORG_SCHEMA_ES not in es_resolved:
                es_resolved.append(ORG_SCHEMA_ES)
            for vs in VIDEO_SCHEMAS.get(out, []):
                es_resolved.append(vs)
            es_schema_tags = '\n'.join(
                f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                for s in es_resolved)
            es_html = TEMPLATE.format(
                lang='es', title=es_title, desc=es_desc, canonical=es_canonical, site=SITE_URL,
                oglocale='es_ES',
                pagebg=PAGE_BG.get(out.replace('spanish/', ''), _DEFAULT_BG),
                root='../' + ('../' * out.count('/')),
                body=es_body, schema=es_schema_tags, langtoggle=es_langtoggle,
                campusswitch=es_campusswitch, bodyclass=bodyclass, datacampus=datacampus, campuslocked=campuslocked,
                hreflang_block=es_hreflang_block, mbar=es_mbar, header_nav=es_header_nav, footer_block=es_footer_block,
                lp='../' + ('../' * out.count('/')) + 'programs/index.html',
                en_cur='', es_cur='aria-current="true"')
            es_html = (es_html
                    .replace('<span class="date" data-start-date>First Monday of next month</span>',
                             '<span class="date" data-start-date>%s</span>' % NEXT_START_LONG)
                    .replace('<b data-d>0</b>', '<b data-d>%s</b>' % CD_D)
                    .replace('<b data-h>0</b>', '<b data-h>%s</b>' % CD_H)
                    .replace('<b data-m>0</b>', '<b data-m>%s</b>' % CD_M)
                    .replace('<b data-s>0</b>', '<b data-s>%s</b>' % CD_S))
            # ES 404 must also stay unindexed
            if out == '404.html':
                es_html = es_html.replace(
                    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
                    '<meta name="robots" content="noindex">')
            es_html = clean_links(es_html)
            # ── GHL form swap: EN → ESP on Spanish pages ──────────────────
            # Client 2026-07-17: reinstated the ESP form variant, reversing the
            # 2026-07-14 "single form per domain" decision. Spanish visitors get
            # the Spanish-language form; EN pages keep 3ghO untouched.
            # Fires here (post-template) so it catches BOTH auto-generated
            # /spanish/* twins and the hand-written es-*.html sources.
            # NOTE: campus landing funnels are NOT built by this script — they
            # keep their campus-specific forms (Manhattan 2Fv / Bronx v1S).
            es_html = (es_html
                .replace('api.leadconnectorhq.com/widget/form/3ghObGjHiLN3LgKBfKGG',
                         'api.leadconnectorhq.com/widget/form/H4C1nJmpLO3cNx4OrlK2')
                .replace('inline-3ghObGjHiLN3LgKBfKGG', 'inline-H4C1nJmpLO3cNx4OrlK2')
                .replace('data-form-id="3ghObGjHiLN3LgKBfKGG"',
                         'data-form-id="H4C1nJmpLO3cNx4OrlK2"')
                .replace('data-form-name="01.GET TRAINED WITH ABI FORM - ABI.com"',
                         'data-form-name="01.GET TRAINED WITH ABI FORM - ABI.com - ESP"')
                .replace('title="01.GET TRAINED WITH ABI FORM - ABI.com"',
                         'title="01.GET TRAINED WITH ABI FORM - ABI.com - ESP"')
                # ESP form is taller than the EN one (client-supplied heights).
                .replace('data-height="757"', 'data-height="792"'))
            es_dest = os.path.join(ROOT, es_out)
            os.makedirs(os.path.dirname(es_dest), exist_ok=True)
            open(es_dest, 'w', encoding='utf-8').write(es_html)
            if out != '404.html':
                written.append(es_out)
    # sitemap — adds priority/changefreq hints and xhtml:link hreflang annotations
    # so Google indexes the EN ↔ ES home variants as one logical URL.
    # Both hand-crafted ES twins (spanish/index.html, spanish/bronx.html) were
    # previously missing from this list entirely — fixed (client audit 2026-07-08).
    written += ['index.html', 'spanish/index.html', 'bronx.html', 'spanish/bronx.html']
    import datetime
    _today = datetime.date.today().isoformat()
    def _pri(o):
        if o in ('index.html',):                                  return ('1.0', 'weekly')
        if o == 'spanish/index.html':                             return ('0.9', 'weekly')
        if o.startswith('programs/') or o == 'contact.html':      return ('0.9', 'weekly')
        if o in ('about.html', 'haircuts.html', 'instructors.html'): return ('0.8', 'monthly')
        if o.startswith('blog/'):                                 return ('0.7', 'monthly')
        if o in ('faq.html', 'schedules.html'):                   return ('0.7', 'monthly')
        return ('0.6', 'monthly')
    def _abs(o):
        # Vercel cleanUrls + trailingSlash:false → URLs are bare (no .html, no /).
        # Root paths (index.html, spanish/index.html) are special-cased to / and /spanish .
        if o == 'index.html': return SITE_URL + '/'
        if o == 'spanish/index.html': return SITE_URL + '/spanish'
        u = f'{SITE_URL}/{o}'.replace('/index.html', '').replace('.html', '')
        return u
    def _entry(o):
        loc = _abs(o)
        pri, cf = _pri(o)
        block = [
            f'  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{_today}</lastmod>',
            f'    <changefreq>{cf}</changefreq>',
            f'    <priority>{pri}</priority>',
        ]
        # hreflang annotations only where both EN and ES counterparts exist.
        if o == 'index.html' or o == 'spanish/index.html':
            block.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/"/>')
            block.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}/spanish"/>')
            block.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/>')
        block.append('  </url>')
        return '\n'.join(block)
    # Yoast-style split: a styled sitemap index (sitemap.xml) pointing to
    # page/post/programs sub-sitemaps, each rendered human-readable via
    # /sitemap.xsl (cosmetic only — crawlers read the raw XML).
    _XML_HEAD = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>\n')
    posts = sorted(o for o in written if o.startswith('blog/') and o != 'blog/index.html')
    progs = sorted(o for o in written if o.startswith('programs/') and o != 'programs/index.html')
    pages = [o for o in written if o not in posts and o not in progs]
    pages.sort(key=lambda o: (-float(_pri(o)[0]), o))   # home first, then by priority/name
    def _write_urlset(fname, items):
        urls = '\n'.join(_entry(o) for o in items)
        open(os.path.join(ROOT, fname), 'w').write(
            _XML_HEAD +
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f'{urls}\n</urlset>\n')
    _write_urlset('page-sitemap.xml', pages)
    _write_urlset('post-sitemap.xml', posts)
    _write_urlset('programs-sitemap.xml', progs)
    subs = ''.join(
        f'  <sitemap>\n    <loc>{SITE_URL}/{n}</loc>\n    <lastmod>{_today}</lastmod>\n  </sitemap>\n'
        for n in ('page-sitemap.xml', 'post-sitemap.xml', 'programs-sitemap.xml', 'landing-sitemap.xml'))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        _XML_HEAD +
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{subs}</sitemapindex>\n')
    # robots.txt — explicitly invite AI / answer-engine crawlers so ABI can be
    # cited confidently by ChatGPT, Claude, Perplexity, Google AI Overviews, etc.
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(
        'User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /docs/\n\n'
        # OpenAI
        'User-agent: GPTBot\nAllow: /\n\n'
        'User-agent: OAI-SearchBot\nAllow: /\n\n'
        'User-agent: ChatGPT-User\nAllow: /\n\n'
        # Anthropic
        'User-agent: ClaudeBot\nAllow: /\n\n'
        'User-agent: Claude-Web\nAllow: /\n\n'
        'User-agent: anthropic-ai\nAllow: /\n\n'
        # Perplexity
        'User-agent: PerplexityBot\nAllow: /\n\n'
        'User-agent: Perplexity-User\nAllow: /\n\n'
        # Google AI (separate from Googlebot — controls AI Overviews + Gemini grounding)
        'User-agent: Google-Extended\nAllow: /\n\n'
        # Common Crawl (feeds most LLM training)
        'User-agent: CCBot\nAllow: /\n\n'
        # Amazon, Apple, Bytedance, You.com
        'User-agent: Amazonbot\nAllow: /\n\n'
        'User-agent: Applebot\nAllow: /\n\n'
        'User-agent: Applebot-Extended\nAllow: /\n\n'
        'User-agent: Bytespider\nAllow: /\n\n'
        'User-agent: YouBot\nAllow: /\n\n'
        # Bing AI / Copilot — uses Bingbot, but mirror for clarity
        'User-agent: Bingbot\nAllow: /\n\n'
        # DuckAssist
        'User-agent: DuckAssistBot\nAllow: /\n\n'
        f'Sitemap: {SITE_URL}/sitemap.xml\n')
    print(f'built {len(written)} pages + sitemap.xml + robots.txt')

if __name__ == '__main__':
    build()
