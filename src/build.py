#!/usr/bin/env python3
"""Static site builder for the American Barber Institute website.
Merges src/pages/*.html content partials into the base template.
Usage: python3 build.py
"""
import json, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'pages')
SITE_URL = 'https://www.abi.edu'

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
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/icon.png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css?v=32">
<link rel="stylesheet" href="{root}assets/css/brand.css?v=30">
<link rel="stylesheet" href="{root}assets/css/landing.css?v=148">
<link rel="stylesheet" href="{root}assets/css/upgrade.css?v=2">
<script src="{root}assets/js/analytics.js?v=3" defer></script>
<script>try{{localStorage.removeItem('abi-theme');localStorage.removeItem('abi-theme-user');}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}assets/css/effects.css?v=30">
{schema}
</head>
<body class="mhx-on" style="--page-bg:url('/assets/img/{pagebg}')">
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NKLLGPC" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
<div class="abi-deco" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">
  <div class="tb-promo">Start your barber journey today for only $150 per week*</div>
  <div class="tb-calls">
    <a class="tb-call" href="tel:+12122902289"><b class="tb-flag">EN</b><span class="tb-label">Call Admissions</span><span class="tb-num">(212) 290-2289</span></a>
    <a class="tb-call" href="tel:+12122900278"><b class="tb-flag">ES</b><span class="tb-label">En Español</span><span class="tb-num">(212) 290-0278</span></a>
  </div>
</div>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo brand-plate" href="{root}index.html" aria-label="American Barber Institute — home" title="American Barber Institute">
      <img class="logo-img" src="{root}assets/img/logo-final.gif" alt="American Barber Institute — 48 West 39th Street, New York, NY 10018 & 121 Westchester Square, Bronx, NY 10461" width="385" height="99" fetchpriority="high">
    </a>
    <nav class="mainnav" aria-label="Main"><a href="{root}index.html">Home</a><a href="{root}about.html">About</a><a href="{root}programs/index.html">Programs</a><a href="{root}instructors.html">Instructors</a><a href="{root}partners.html">Partners</a><a href="{root}gallery.html">Gallery</a><a href="{root}haircuts.html">Haircuts</a><a href="{root}blog/index.html">Blog</a><span class="nav-drop"><a href="{root}jobs.html" class="nav-drop-trigger">Jobs ▾</a><span class="nav-drop-menu"><a href="{root}jobs.html">Jobs</a><a href="{root}resources.html">Resources</a></span></span><span class="nav-drop"><a href="{root}faq.html" class="nav-drop-trigger">FAQs ▾</a><span class="nav-drop-menu"><a href="{root}faq.html">FAQs</a><a href="{root}schedules.html">Schedules</a></span></span><a href="{root}contact.html">Contact</a></nav>
    {langtoggle}
    <div class="loc-toggle" role="group" aria-label="Campus"><a class="is-active" aria-current="true" href="/manhattan">MN</a><a href="/bronx">BX</a></div>
    <a class="header-cta" href="{root}contact.html">Become a Barber</a>
    <div class="hdr-right"><button class="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button></div>
  </div>
  <nav class="nav-drawer"><div class="container"><a href="{root}index.html">Home</a><a href="{root}about.html">About</a><a href="{root}programs/index.html">Programs</a><a href="{root}instructors.html">Instructors</a><a href="{root}partners.html">Partners</a><a href="{root}gallery.html">Gallery</a><a href="{root}haircuts.html">Haircuts</a><a href="{root}blog/index.html">Blog</a><a href="{root}jobs.html">Jobs</a><a href="{root}resources.html">Resources</a><a href="{root}faq.html">FAQs</a><a href="{root}schedules.html">Schedules</a><a href="{root}contact.html">Contact</a><a href="{root}es/index.html"><b>Español</b></a></div></nav>
</header>
<div class="mhx">
  <div class="mhx-promo">START YOUR BARBER JOURNEY TODAY FOR ONLY <b>$150 PER WEEK*</b></div>
  <div class="mhx-phones">
    <a class="mhx-phone" href="tel:+12122902289"><span class="mhx-num">(212) 290-2289</span><span class="mhx-lab"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>ENGLISH</span></a>
    <a class="mhx-phone" href="tel:+18563161551"><span class="mhx-num">(856) 316-1551</span><span class="mhx-lab"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></svg>HAIRCUT</span></a>
    <a class="mhx-phone" href="tel:+12122900278"><span class="mhx-num">(212) 290-0278</span><span class="mhx-lab"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>SPANISH</span></a>
  </div>
  <div class="mhx-seats"><span class="mhx-star" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.9 6.26L21.8 9.3l-5 4.72 1.24 6.8L12 17.5l-6.04 3.32L7.2 14 2.2 9.3l6.9-1.04z"/></svg></span><span class="mhx-seats-t"><b>LIMITED SEATS AVAILABLE</b><i>ENROLLMENT NOW OPEN</i></span></div>
</div>

<main id="main">
{body}
</main>

<section class="cta-band">
  <div class="wrap">
    <p class="kicker" style="justify-content:center">Classes begin the first Monday of each month</p>
    <h2>Ready to Become a Licensed Barber?</h2>
    <p>Next class starts <span data-start-date>soon</span>. Seats fill fast — start your barber school enrollment, request a call, or speak with admissions in English or Spanish.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold btn-lg" href="{root}contact.html">Start Barber School</a>
      <a class="btn btn-ghost btn-lg" href="{root}contact.html">Speak With Admissions</a>
    </div>
  </div>
</section>

<footer class="site">
  <div class="foot-cta">
    <div class="wrap">
      <h3>Start Barber School Today</h3>
      <p>Your new career is one phone call away. Talk to admissions in English or Spanish.</p>
      <div class="foot-cta-btns">
        <a class="btn btn-gold btn-lg" href="{root}contact.html">Request a Call</a>
        <a class="btn btn-blue btn-lg" href="{root}contact.html">Apply Now</a>
        
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <p class="foot-name">American Barber Institute</p>
        <p>New York's only dedicated barber school. Licensed by the NY State Department of Education. Changing lives for over 30 years.</p>
        <div class="socials">
          <a class="soc soc-fb" href="https://www.facebook.com/Abi.Education/" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>
          <a class="soc soc-ig" href="https://www.instagram.com/americanbarberinstitute/" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>
          <a class="soc soc-x" href="https://twitter.com/amerbarberedu" aria-label="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3zm-1 16.2h1.7L7.3 4.7H5.5l11.3 14.5z"/></svg></a>
          <a class="soc soc-yt" href="https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.5 12 4.5 12 4.5s-7 0-8.9.6A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.6 8.9.6 8.9.6s7 0 8.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.3V8.7L15.9 12l-6.1 3.3z"/></svg></a>
          <a class="soc soc-pin" href="https://www.pinterest.com/alexzholendz/american-barber-institute/" aria-label="Pinterest"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.6 2-2.6.9 0 1.4.7 1.4 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.6-1.9-4.4-4.5-4.4a4.7 4.7 0 0 0-4.9 4.7c0 .9.4 1.9.8 2.5l-.3 1.1c-.1.4-.3.5-.7.3-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 1.9-1.2 2.6A10 10 0 1 0 12 2z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Links</h4>
        <ul>
          <li><a href="{root}about.html">About ABI</a></li>
          <li><a href="{root}programs/index.html">Programs</a></li>
          <li><a href="{root}instructors.html">Instructors</a></li>
          <li><a href="{root}faq.html">FAQs</a></li>
          <li><a href="{root}resources.html">Resources</a></li>
          <li><a href="{root}jobs.html">Job Placement</a></li>
          <li><a href="{root}partners.html">Partners</a></li>
          <li><a href="{root}gallery.html">Gallery</a></li>
          <li><a href="{root}haircuts.html">$3 Haircuts</a></li>
          <li><a href="{root}about.html#tour">Virtual Tour</a></li>
          <li><a href="{root}blog/index.html">Blog</a></li>
          <li><a href="{root}contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Locations</h4>
        <ul>
          <li><b>Manhattan</b><br><a href="https://maps.google.com/?q=48+West+39th+Street,+New+York,+NY+10018">48 West 39th Street<br>New York, NY 10018</a></li>
          <li><b>Bronx</b><br><a href="https://maps.google.com/?q=121+Westchester+Square,+Bronx,+NY+10461">121 Westchester Square<br>Bronx, NY 10461</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:+12122902289">(212) 290-2289 (English)</a></li>
          <li><a href="tel:+12122900278">(212) 290-0278 (Español)</a></li>
          <li><a href="mailto:admission@abi.edu">admission@abi.edu</a></li>
          <li>Monday – Friday: 8:00 AM – 8:00 PM</li>
          <li>Saturday: 9:00 AM – 7:00 PM</li>
          <li>Sunday: 9:00 AM – 7:00 PM</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-legal">
    <div class="wrap">
      <div>© <span id="yr"></span> American Barber Institute (ABI). All rights reserved.</div>
      <div class="foot-legal-links"><a href="/privacy-and-policy">Privacy Policy</a></div>
      <div>GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs (VA). Info: <a href="https://www.benefits.va.gov/gibill" rel="noopener">benefits.va.gov/gibill</a></div>
    </div>
  </div>
</footer>

<a class="desk-cta" href="{root}contact.html" aria-label="Request a call from admissions">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
  Request a Call
</a>
<button class="to-top" aria-label="Back to top" title="Back to top"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>

<div class="mobile-cta">
  <button class="call" type="button" aria-haspopup="true" aria-expanded="false" data-call-toggle>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
    <span>Call Now</span>
  </button>
  <a class="text" href="sms:+12122902289" aria-label="Text us">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
    <span>Text Us</span>
  </a>
  <a class="apply" href="{root}contact.html" aria-label="Apply now">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>
    <span>Apply Now</span>
  </a>
  <div class="call-sheet" hidden role="menu" aria-label="Choose a language to call">
    <p class="call-sheet-h">Call us — choose a language</p>
    <a href="tel:+12122902289" role="menuitem"><span class="cs-lang">English</span><span class="cs-num">(212) 290-2289</span></a>
    <a href="tel:+12122900278" role="menuitem"><span class="cs-lang">Español</span><span class="cs-num">(212) 290-0278</span></a>
  </div>
</div>
<script>(function(){{var b=document.querySelector('[data-call-toggle]'),s=document.querySelector('.call-sheet');if(!b||!s)return;function close(){{s.hidden=true;b.setAttribute('aria-expanded','false');}}b.addEventListener('click',function(e){{e.stopPropagation();var open=s.hidden;s.hidden=!open;b.setAttribute('aria-expanded',String(open));}});document.addEventListener('click',function(e){{if(!s.hidden&&!s.contains(e.target)&&e.target!==b)close();}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')close();}});s.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',close);}});}})();</script>

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{root}assets/js/main.js?v=32" defer></script>
<script src="{root}assets/js/effects.js?v=32" defer></script>
<script src="{root}assets/js/landing.js?v=32" defer></script>
<script src="{root}assets/js/upgrade.js?v=2" defer></script>
<script src="{root}assets/js/campus.js?v=1" defer></script>
<!-- GHL chat widget (VIBE AI). Alex chatbot preserved in /assets/js/chatbot.js — to restore Alex: delete this block and re-add the chatbot.js script tag. -->
<script src="https://widgets.leadconnectorhq.com/loader.js" data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="689f4917512e48b4268bf335" defer></script>
<script>(function(){{var t=setInterval(function(){{var w=document.querySelector("chat-widget");if(w&&w.shadowRoot){{clearInterval(t);var s=document.createElement("style");s.textContent="@media(max-width:768px){{.lc_text-widget,.lc_text-widget--bubble{{bottom:140px!important;right:12px!important}}}}";w.shadowRoot.appendChild(s);}}}},400);setTimeout(function(){{clearInterval(t)}},15000);}})();</script>
<script src="{root}assets/js/video-sound.js?v=3" defer></script>
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
    "description": "New York's only dedicated barber school. NYS-licensed 500-hour Master Barber program in Midtown Manhattan with financial aid, veterans GI Bill and ACCESS-VR options, and job placement.",
    "slogan": "Become a Licensed Barber in 4 Months",
    "telephone": "+1-212-290-2289",
    "email": "admission@abi.edu",
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
        {"@type": "AdministrativeArea", "name": "Westchester County"},
        {"@type": "State", "name": "New Jersey"},
        {"@type": "State", "name": "Connecticut"}
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

def course_schema(name, desc, hours, weeks, price):
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
                         "address": "48 West 39th Street, New York, NY 10018"}
        },
        "totalHistoricalEnrollment": None,
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

PAGES = [
    # (output, partial, title, description, lang, extra_schema)
    ("about.html", "about.html",
     "About Us | American Barber Institute NYC",
     "Inside ABI: our Midtown Manhattan campus, NYS-licensed curriculum, instructors who are all ABI grads, and a mission to build lifetime barber careers.",
     "en", []),
    ("instructors.html", "instructors.html",
     "Our Instructors | Master Barber Teachers in NYC",
     "Meet ABI's master instructors — including King David Ayeoribe and Emmy-featured Harold “Barkim” Brown — with 50+ years of combined barbering experience.",
     "en", [INSTRUCTORS_SCHEMA]),
    ("jobs.html", "jobs.html",
     "Job Placement & Shop Registration | American Barber Institute",
     "ABI maintains a full-time job placement office. Graduates often finish with multiple offers. Barbershop owners: register your shop to hire our trained graduates.",
     "en", []),
    ("gallery.html", "gallery.html",
     "Gallery — Student Work & Campus | ABI",
     "See our students' haircuts, our 3,000 sq ft Midtown Manhattan campus, and life at New York's only dedicated barber school.",
     "en", []),
    ("haircuts.html", "haircuts.html",
     "$3 Student Haircuts — Manhattan & Bronx | American Barber Institute",
     "Great cuts for $3 at ABI. Student barbers supervised by licensed instructors at our Manhattan and Bronx locations. Fades, tapers, beard trims and more.",
     "en", []),
    ("faq.html", "faq.html",
     "Frequently Asked Questions | American Barber Institute",
     "Answers about tuition costs, program length, schedules, age requirements, ACCESS-VR, job placement, and why students choose ABI.",
     "en", ["FAQ_SCHEMA"]),
    ("schedules.html", "schedules.html",
     "Class Schedules & Holiday Calendar | American Barber Institute",
     "Every upcoming class start date and federal-holiday closure for ABI's Manhattan and Bronx campuses through 2028.",
     "en", []),
    ("contact.html", "contact.html",
     "Contact & Directions | American Barber Institute",
     "Visit ABI at 48 West 39th Street, NYC — minutes from Penn Station, Grand Central & Times Square. Call (212) 290-2289 or book your free tour today.",
     "en", [ORG_SCHEMA]),
    ("resources.html", "resources.html",
     "Barbering Resources & State Licensing Boards | ABI",
     "Regulatory agencies, state-by-state barber and cosmetology licensing boards, education resources and industry associations.",
     "en", []),
    ("partners.html", "partners.html",
     "Our Partners | Where ABI Barbers Work in NYC",
     "Where ABI graduates work: Levels Barbershop, Diamond Fadez, Untouchable Cutz, Expo Gentlemen Salon, Otis & Finn and the NYC Barber Shop Museum.",
     "en", []),
    ("404.html", "404.html",
     "Page Not Found | American Barber Institute",
     "The page you're looking for doesn't exist. Return to American Barber Institute's homepage or browse our barber programs.",
     "en", []),
    ("programs/index.html", "programs-index.html",
     "Barber Programs in NYC | American Barber Institute",
     "ABI's NYS-licensed barber programs at our Manhattan & Bronx campuses: 500-Hour Master Barber, 50-Hour Barber Refresher (Manhattan campus only) and the 3-Hour Contagious Diseases course.",
     "en", []),
    ("programs/500-hour-master-barber.html", "program-500.html",
     "500-Hour Master Barber Program — Manhattan | ABI NYC",
     "Become a licensed Master Barber in 4 months at our Manhattan campus. Morning, afternoon or weekend schedules from $4,600 with weekly payment plans.",
     "en", [course_schema("500 Hour Master Barber Program",
        "Four-month NYS-licensed master barber training: theory, practical work on real clients, State Board exam prep and job placement.", 500, 17, 5600)]),
    ("programs/500-hour-master-barber-bronx.html", "program-500-bronx.html",
     "500-Hour Master Barber Program — Bronx | ABI NYC",
     "Become a licensed Master Barber at ABI's Bronx campus. 500-hour hands-on training, flexible schedules, payment plans, job placement and bilingual instruction.",
     "en", [course_schema("500 Hour Master Barber Program — Bronx",
        "Four-month NYS-licensed master barber training at the Bronx campus with bilingual instruction, State Board exam prep and job placement.", 500, 17, 5600)]),
    ("programs/50-hour-barber-refresher.html", "program-50.html",
     "50-Hour Barber Refresher (2 Weeks) — Manhattan | ABI",
     "Sharpen your skills and prep for the NY State Board Exam in 2 weeks at our Manhattan campus. For cosmetologists, hairdressers and barber apprentices.",
     "en", [course_schema("50 Hour Barber Refresher Program",
        "Two-week refresher preparing licensed professionals for the New York State Barbering Licensing Examination. This course is offered only at ABI's Manhattan campus.", 50, 2, 1500)]),
    ("programs/contagious-diseases.html", "program-cd.html",
     "3-Hour Contagious Diseases Home Study — $100 | ABI",
     "NY-required Contagious Diseases course for barber operators and apprentices. Complete by mail for $100 — booklet, exam and two certificates.",
     "en", [course_schema("3 Hours Contagious Diseases Program",
        "Home-study course on transmission of contagious diseases, sanitation and sterilization required for NY barber licensure.", 3, 1, 100)]),
    ("blog/index.html", "blog-index.html",
     "Blog — Barbering Career Advice & News | American Barber Institute",
     "Advice from NYC's only dedicated barber school: licensing, careers, shop ownership, marketing your barbershop, and life after barber school.",
     "en", []),
    # ── Hidden SEO pages (parity with the old abi.edu sitemap) ──────────────
    # Not linked from nav/footer by design: reachable by URL, listed in
    # sitemap.xml, and interlinked among themselves only.
    ("financial-aid.html", "page-financial-aid.html",
     "Financial Aid for Barber School NYC | ACCES-VR & GI Bill®",
     "Barber school financial assistance in NYC: ACCES-VR funding, GI Bill® for veterans and weekly payment plans from $150 at American Barber Institute.",
     "en", []),
    ("how-to-get-started.html", "page-how-to-get-started.html",
     "How to Get Started | Enroll at American Barber Institute",
     "Enroll at ABI in 4 steps: book a tour, bring your documents, pick a schedule and start on the first Monday of the month. Manhattan & Bronx campuses.",
     "en", []),
    ("va-approved-job-training-program.html", "page-va-approved-job-training-program.html",
     "VA-Approved Barber Job Training Program in NYC | ABI",
     "ABI's 500-Hour Master Barber Program is VA-approved under Title 38 USC § 3676 — hands-on training, veteran support and job placement in Manhattan & the Bronx.",
     "en", []),
    ("access-vr-program.html", "page-access-vr-program.html",
     "ACCES-VR Barber Training Program in NYC | ABI",
     "ACCES-VR can cover tuition, tools and books for New Yorkers with documented disabilities at American Barber Institute. Eligibility, services and how to apply.",
     "en", []),
    ("veterans.html", "page-veterans.html",
     "Veterans Barber Training NYC | GI Bill® Accepted | ABI",
     "Use GI Bill® benefits at ABI — Post-9/11 (Ch. 33), VR&E (Ch. 31), Montgomery GI Bill and DEA (Ch. 35). Train as a licensed Master Barber in about 4 months.",
     "en", []),
    ("privacy-and-policy.html", "page-privacy-and-policy.html",
     "Privacy Policy | American Barber Institute",
     "How American Barber Institute collects, protects and shares your information — including cookies from Google Analytics, Meta Pixel, Microsoft Clarity and LeadConnector forms.",
     "en", []),
    ("virtual-tour.html", "page-virtual-tour.html",
     "Virtual Tour | American Barber Institute NYC",
     "Take a video tour of ABI's 3,000 sq ft Manhattan barber school, get subway and bus directions, and book an in-person tour of our Manhattan or Bronx campus.",
     "en", []),
    ("skills-and-techniques.html", "page-skills-and-techniques.html",
     "Skills & Techniques Barber Students Learn | ABI NYC",
     "What ABI students master in 4 months: fades, tapers, shears, razor lineups, shaves, sanitation, barber theory and NY State Board exam prep — on real clients.",
     "en", []),
    ("shop-registration.html", "page-shop-registration.html",
     "Shop Registration — Hire ABI Graduates | ABI NYC",
     "Barbershop owners: register your shop with ABI's job placement office for free and hire trained, NYS Board-prepared barber graduates from our NYC campuses.",
     "en", []),
    ("barber-school-queens-ny.html", "loc-barber-school-queens-ny.html",
     "Barber School Queens, NY - American Barber Institute",
     "American Barber Institute is just 30 minutes from Queens. NYS-licensed since 1996 — 500-hour Master Barber training with payment plans from $150/week.",
     "en", []),
    ("barber-school-brooklyn-new-york.html", "loc-barber-school-brooklyn-new-york.html",
     "Barber School Brooklyn, NY - American Barber Institute",
     "Family-owned, NYS-licensed barber school minutes from Brooklyn. Learn tapers, fades and hot towel shaves — with job placement help after graduation.",
     "en", []),
    ("barber-school-yonkers-new-york.html", "loc-barber-school-yonkers-new-york.html",
     "Barber School Yonkers, NY - American Barber Institute",
     "One of New York's most regarded barber schools, minutes from Yonkers. Train at our Bronx campus at Westchester Square — Master Barber in about 4 months.",
     "en", []),
    ("barber-school-westchester-ny.html", "loc-barber-school-westchester-ny.html",
     "Barber School Westchester, NY - American Barber Institute",
     "Become a Master Barber in under four months. ABI's Bronx campus at 121 Westchester Square puts NYS-licensed barber training within reach of Westchester.",
     "en", []),
    ("barber-school-long-island-ny.html", "loc-barber-school-long-island-ny.html",
     "Barber School Long Island, NY - American Barber Institute",
     "ABI's Manhattan campus is minutes from Penn Station — an easy LIRR ride from Long Island. 500-hour Master Barber training with plans from $150/week.",
     "en", []),
    ("barber-school-staten-island-ny.html", "loc-barber-school-staten-island-ny.html",
     "Barber School Staten Island, NY - American Barber Institute",
     "Master Barber classes near Staten Island at ABI's Midtown Manhattan campus. Individualized training, NYS exam prep and job placement — about 4 months.",
     "en", []),
    ("barber-school-mount-vernon-ny.html", "loc-barber-school-mount-vernon-ny.html",
     "Barber School Mount Vernon NY - Westchester Barber Courses",
     "Become a Master Barber in just four months. Fade and shaving classes, NYS board exam prep and job placement — minutes from Mount Vernon at our Bronx campus.",
     "en", []),
    ("barber-school-port-chester-ny.html", "loc-barber-school-port-chester-ny.html",
     "Barber School Port Chester NY - Westchester Barber School",
     "Become a Master Barber in four months at ABI's Bronx campus — fade classes, shaving classes, NYS exam prep and job placement for Port Chester students.",
     "en", []),
    ("barber-school-connecticut.html", "loc-barber-school-connecticut.html",
     "Barber School Connecticut - Get Licensed in NY & Transfer",
     "Get your barber license in New York in half the time — and up to half the cost — then transfer it to Connecticut through reciprocity. ABI shows you how.",
     "en", []),
    ("barber-school-pennsylvania.html", "loc-barber-school-pennsylvania.html",
     "Barber School Pennsylvania - NY License Transfer",
     "Licensed NY barber heading to Pennsylvania? Reciprocity saves about $10,400 and 700 training hours versus a full PA program. ABI guides you through it.",
     "en", []),
    ("barber-school-bronx-new-york.html", "loc-barber-school-bronx-new-york.html",
     "Barber School Bronx, NY - American Barber Institute",
     "ABI's Bronx campus at 121 Westchester Square offers full barber training, NYS licensing exam prep and job placement — payment plans from $150/week.",
     "en", []),
    ("best-barber-school-in-bronx.html", "loc-best-barber-school-in-bronx.html",
     "Bronx Barber School - Best Barber School in Bronx",
     "The American Barber Institute welcomes aspiring barbers from the Bronx, Westchester, Mount Vernon, Yonkers and Port Chester. Top-notch training since 1996.",
     "en", []),
    ("barbershop-bronx.html", "loc-barbershop-bronx.html",
     "Barbershop Bronx - $3 Haircuts - American Barber Institute",
     "$3 haircuts at ABI's Bronx campus, 121 Westchester Square. Fades, classic cuts, shape-ups and hot shaves by supervised students — quality high, prices low.",
     "en", []),
    ("barber-training-program-nyc.html", "loc-barber-training-program-nyc.html",
     "Barber Training Program NYC - Become a Master Barber",
     "Rigorous, hands-on barber training in NYC that prepares you to pass the NYS Board of Barbering exam and become a Master Barber. Manhattan & Bronx campuses.",
     "en", []),
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
            f"{_p['title']} — career advice and industry insight from NYC's only dedicated barber school.",
            "en", [article_schema(_p['title'], f"{SITE_URL}/blog/{_p['slug']}",
                                  slug=_p['slug'], body=_body)]))

FAQ_SCHEMA_PLACEHOLDER = "FAQ_SCHEMA"

def faq_schema_from(body):
    """Build FAQPage JSON-LD from the faq partial's <summary>/<div class="a"> pairs."""
    qa = re.findall(r'<summary>(.*?)</summary>\s*<div class="a">(.*?)</div>', body, re.S)
    items = []
    for q, a in qa:
        clean_a = re.sub(r'<[^>]+>', ' ', a)
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
    'programs/500-hour-master-barber.html': 'gallery/cut-22.jpg',
    'programs/500-hour-master-barber-bronx.html': 'gallery/grp-05.jpg',
    'programs/50-hour-barber-refresher.html': 'gallery/cut-18.jpg',
    'programs/contagious-diseases.html': 'gallery/grp-10.jpg',
    'blog/index.html': 'gallery/grp-02.jpg',
}
_DEFAULT_BG = 'gallery/cut-05.jpg'

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
        # One-click EN/ES toggle beside the logo. Full Spanish exists for the
        # home/splash; other EN pages send Spanish visitors to the Spanish home.
        if out.startswith('es/'):
            langtoggle = ('<div class="lang-toggle" role="group" aria-label="Language">'
                          '<a href="%s%s">EN</a><a class="is-active" aria-current="true" href="%s%s">ES</a></div>'
                          % (root, out[3:], root, out))
        else:
            langtoggle = ('<div class="lang-toggle" role="group" aria-label="Language">'
                          '<a class="is-active" aria-current="true" href="%s%s">EN</a><a href="%ses/index.html">ES</a></div>'
                          % (root, out, root))
        # hreflang reciprocity: every EN page declares itself as en + x-default;
        # the home page additionally declares the ES alternate (and vice-versa).
        # Only the home page has a Spanish counterpart today.
        _en_home = SITE_URL + "/"
        _es_home = SITE_URL + "/es/"
        if out in ('index.html',):
            hreflang_block = (
                f'<link rel="alternate" hreflang="en" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="es" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{_en_home}">'
            )
        elif out.startswith('es/'):
            hreflang_block = (
                f'<link rel="alternate" hreflang="es" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="es-US" href="{_es_home}">\n'
                f'<link rel="alternate" hreflang="en" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="en-US" href="{_en_home}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{_en_home}">'
            )
        else:
            hreflang_block = (
                f'<link rel="alternate" hreflang="en" href="{canonical}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{canonical}">'
            )
        html = TEMPLATE.format(
            lang=lang, title=title, desc=desc, canonical=canonical, site=SITE_URL,
            oglocale='es_ES' if lang == 'es' else 'en_US',
            pagebg=PAGE_BG.get(out.replace('es/', ''), _DEFAULT_BG),
            root=root, body=body, schema=schema_tags, langtoggle=langtoggle,
            hreflang_block=hreflang_block,
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
    # sitemap — adds priority/changefreq hints and xhtml:link hreflang annotations
    # so Google indexes the EN ↔ ES home variants as one logical URL.
    written += ['index.html', 'es/index.html', 'bronx.html']
    import datetime
    _today = datetime.date.today().isoformat()
    def _pri(o):
        if o in ('index.html',):                                  return ('1.0', 'weekly')
        if o == 'es/index.html':                                  return ('0.9', 'weekly')
        if o.startswith('programs/') or o == 'contact.html':      return ('0.9', 'weekly')
        if o in ('about.html', 'haircuts.html', 'instructors.html'): return ('0.8', 'monthly')
        if o.startswith('blog/'):                                 return ('0.7', 'monthly')
        if o in ('faq.html', 'schedules.html'):                   return ('0.7', 'monthly')
        return ('0.6', 'monthly')
    def _abs(o):
        # Vercel cleanUrls + trailingSlash:false → URLs are bare (no .html, no /).
        # Root paths (index.html, es/index.html) are special-cased to /  and /es .
        if o == 'index.html': return SITE_URL + '/'
        if o == 'es/index.html': return SITE_URL + '/es'
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
        if o == 'index.html' or o == 'es/index.html':
            block.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}/"/>')
            block.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE_URL}/es"/>')
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
        for n in ('page-sitemap.xml', 'post-sitemap.xml', 'programs-sitemap.xml'))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        _XML_HEAD +
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{subs}</sitemapindex>\n')
    # robots.txt — explicitly invite AI / answer-engine crawlers so ABI can be
    # cited confidently by ChatGPT, Claude, Perplexity, Google AI Overviews, etc.
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(
        'User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /docs/\nDisallow: /_archive/\n\n'
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
