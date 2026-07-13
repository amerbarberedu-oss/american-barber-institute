#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ABI Landing Funnels — page generator (authentic-content edition).

Produces 4 conversion-focused landing pages under ``landing-funnels/``:

  500-hours-master-barber-program-landing-page/index.html       Manhattan EN
  500-hours-master-barber-program-landing-page/spanish/index.html  Manhattan ES
  master-barber-program-bronx/index.html                        Bronx EN
  master-barber-program-bronx/spanish/index.html                Bronx ES

Imports NOTHING from the main marketing site. All copy comes from data.py
(verbatim from the school's own pages). Run from inside ``landing-funnels/``::

    python3 src/build.py
"""
import os
import sys
import json
import datetime
from html import escape as h

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import data as D

SITE = "https://www.americanbarberinstitute.com"
CSS_V = "62"
JS_V  = "15"

# ── inline SVG icon library ─────────────────────────────────────────
ICONS = {
    "phone":      '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "shield":     '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 11.5 2 2 4-4.5"/>',
    "scissors":   '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>',
    "wallet":     '<rect x="2" y="6" width="20" height="13" rx="2"/><path d="M16 13a2 2 0 1 0 0-4h4v4z"/>',
    "briefcase":  '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2 13h20"/>',
    "calendar":   '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "store":      '<path d="M3 7h18l-1 5H4z"/><path d="M5 12v9h14v-9"/>',
    "check":      '<path d="M20 6 9 17l-5-5"/>',
    "pin":        '<path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>',
    "chat":       '<path d="M21 12a8.5 8.5 0 0 1-8.5 8.5c-1.6 0-3-.4-4.3-1L3 21l1.6-4.8A8.5 8.5 0 1 1 21 12z"/>',
}

def svg(name, size=22, stroke=True):
    body = ICONS.get(name, "")
    attrs = 'width="%d" height="%d" viewBox="0 0 24 24"' % (size, size)
    attrs += (' fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
              if stroke else ' fill="currentColor"')
    return '<svg %s aria-hidden="true">%s</svg>' % (attrs, body)


# ── date helpers (countdown rolls forward indefinitely) ─────────────
def first_monday_of_next_month(after=None):
    after = after or datetime.date.today()
    y, m = after.year, after.month + 1
    if m > 12:
        m, y = 1, y + 1
    d = datetime.date(y, m, 1)
    while d.weekday() != 0:
        d += datetime.timedelta(days=1)
    return d

def next_start():
    today = datetime.date.today()
    d = datetime.date(today.year, today.month, 1)
    while d.weekday() != 0:
        d += datetime.timedelta(days=1)
    if d <= today:
        d = first_monday_of_next_month(today)
    return d

NEXT_ISO = next_start().isoformat()


# ── small helpers ───────────────────────────────────────────────────
def section_head(eyebrow, title, lead=None):
    out = ('<div class="lf-section__head lf-rv">'
           '<span class="lf-eyebrow">%s</span><h2 class="lf-h2">%s</h2>' % (h(eyebrow), h(title)))
    if lead:
        out += '<p class="lf-lead">%s</p>' % h(lead)
    return out + '</div>'


# v3.0 — single brand logo across all 4 landing pages, identical to main
# marketing site header. Spinning pole + both campus addresses baked in.
LOGO_SRC = "/assets/img/logo-final.gif"
LOGO_W, LOGO_H = 385, 99
LOGO_ALT = ("American Barber Institute — "
            "48 West 39th Street, New York, NY 10018 & "
            "121 Westchester Square, Bronx, NY 10461")

# ── HEADER (slim — campus-branded logo + phone + EN/ES) ─────────────
# Each campus logo already contains the street address baked into the
# artwork, so we don't render a duplicate text address line in the header.
def header(p):
    """v46 — the actual abi.edu website header ported to landings:
    ubar (campus + language + phones) → hdr2 (logo + nav + Book) → mstrip (mobile phones)
    Then landings keep .lfx-promo + .lfx-seats below for urgency/conversion signals.
    Requires body.shell2 class + site-header.css + campus.js."""
    es = p["lang"] == "es"
    campus_slug = p["campus"]["slug"]
    is_manhattan = campus_slug == "manhattan"

    # Language toggle: same campus, other language
    en_href = "/" + (p["path"] if not es else p["alt"])
    es_href = "/" + (p["alt"] if not es else p["path"])

    # Campus toggle: other campus, same language
    mht_href = "/500-hours-master-barber-program-landing-page" + ("/spanish" if es else "")
    bx_href  = "/master-barber-program-bronx" + ("/spanish" if es else "")

    lang_label = "Idioma" if es else "Language"

    pin_svg = ('<svg class="seg-pin" width="12" height="12" viewBox="0 0 24 24" fill="none" '
               'stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>')
    globe_svg = ('<svg class="seg-globe" width="12" height="12" viewBox="0 0 24 24" fill="none" '
                 'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                 '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
                 '<path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18z"/></svg>')

    campus_switch = (
        '<div class="seg seg-campus" role="group" aria-label="Choose campus" data-seg="campus">'
        '<span class="seg-glider" aria-hidden="true"></span>'
        '<a class="seg-opt %s" data-campus-opt="manhattan" href="%s" aria-current="%s">%s<span class="seg-lab">Manhattan</span></a>'
        '<a class="seg-opt %s" data-campus-opt="bronx" href="%s" aria-current="%s">%s<span class="seg-lab">Bronx</span></a>'
        '</div>'
    ) % (
        "is-active" if is_manhattan else "", h(mht_href), "true" if is_manhattan else "false", pin_svg,
        "is-active" if not is_manhattan else "", h(bx_href), "true" if not is_manhattan else "false", pin_svg,
    )
    lang_toggle = (
        '<div class="seg seg-lang" role="group" aria-label="%s" data-seg="lang">'
        '<span class="seg-glider" aria-hidden="true"></span>'
        '<a class="seg-opt %s" href="%s" aria-current="%s">%s<span class="seg-lab">English</span></a>'
        '<a class="seg-opt %s" href="%s" aria-current="%s"><span class="seg-lab">Español</span></a>'
        '</div>'
    ) % (
        h(lang_label),
        "is-active" if not es else "", h(en_href), "true" if not es else "false", globe_svg,
        "is-active" if es else "", h(es_href), "true" if es else "false",
    )

    # Per-campus phones for ubar (desktop) and mstrip (mobile)
    phone_svg = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                 'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">'
                 '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 '
                 '2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 '
                 '6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')
    scissors_svg = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                    'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">'
                    '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>'
                    '<path d="M20 4 8.12 15.88"/><path d="M14.47 14.48 20 20"/><path d="M8.12 8.12 12 12"/></svg>')
    mphone_svg = phone_svg.replace('width="14" height="14"', 'width="12" height="12"').replace(
        'stroke-width="2.1"', 'stroke-width="2.2"').replace(' aria-hidden="true"', ' aria-hidden="true"')
    mscissors_svg = scissors_svg.replace('width="14" height="14"', 'width="12" height="12"').replace(
        'stroke-width="2.1"', 'stroke-width="2.2"')

    # Landings show ALL 3 admissions numbers regardless of campus (per client
    # 2026-07-07): Manhattan English + Manhattan Spanish + Bronx. No Haircut.
    # Visitors on either landing can reach any campus's admissions line.
    ubar_calls = (
        '<a class="ubar-call ubar-call--admis" href="tel:+12122902289"><span class="ubar-ico" aria-hidden="true">%s</span>'
        '<span class="ubar-tag">English</span><span class="ubar-num">(212) 290-2289</span></a>'
        '<a class="ubar-call ubar-call--es" href="tel:+12122900278"><span class="ubar-ico" aria-hidden="true">ES</span>'
        '<span class="ubar-tag">Spanish</span><span class="ubar-num">(212) 290-0278</span></a>'
        '<a class="ubar-call ubar-call--bx" href="tel:+17186760640"><span class="ubar-ico" aria-hidden="true">%s</span>'
        '<span class="ubar-tag">Bronx</span><span class="ubar-num">(718) 676-0640</span></a>'
    ) % (phone_svg, phone_svg)
    mstrip_phones = (
        '<a class="mstrip-phone" href="tel:+12122902289">%s<span class="mstrip-t"><b>(212) 290-2289</b><i>English</i></span></a>'
        '<a class="mstrip-phone" href="tel:+12122900278">%s<span class="mstrip-t"><b>(212) 290-0278</b><i>Spanish</i></span></a>'
        '<a class="mstrip-phone" href="tel:+17186760640">%s<span class="mstrip-t"><b>(718) 676-0640</b><i>Bronx</i></span></a>'
    ) % (mphone_svg, mphone_svg, mphone_svg)

    # Nav labels (translate for ES) + language-consistent nav hrefs.
    # ES landings link back to /es/ (Spanish site landing) so Spanish visitors
    # never bounce to an English page mid-flow. Full ES parity for /es/about,
    # /es/guides, etc. is Phase 2 — for launch we consolidate to /es/.
    if es:
        L = {"programs": "Programas", "why": "Por qué ABI", "guides": "Guías",
             "tuition": "Costo y Ayuda", "contact": "Contacto",
             "book": "Reservar Visita", "menu": "Menú",
             "prog500": "500 horas — Barbero Maestro"}
        NAV = {"home": "/spanish", "about": "/spanish", "guides": "/spanish",
               "tuition": "/spanish", "contact": "/spanish"}
        home_href = "/spanish"
    else:
        L = {"programs": "Programs", "why": "Why ABI", "guides": "Guides",
             "tuition": "Tuition & Funding", "contact": "Contact",
             "book": "Book a Tour", "menu": "Menu",
             "prog500": "500-Hour Master Barber"}
        NAV = {"home": "/", "about": "/about", "guides": "/guides",
               "tuition": "/tuition-and-funding", "contact": "/contact"}
        home_href = "/"

    # Promo strip + Limited Seats banner sit BELOW the new header — landings still need urgency.
    promo = h(p["promo_strip"])
    for price in ("$150 per week*", "$150 por semana*"):
        promo = promo.replace(price, "<b>%s</b>" % price)
    seats_kicker, seats_lead = D.SEATS_BANNER[p["lang"]]
    star_svg = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                '<path d="M12 2l2.9 6.26L21.8 9.3l-5 4.72 1.24 6.8L12 17.5l-6.04 3.32L7.2 14 2.2 9.3l6.9-1.04z"/></svg>')

    return (
        '<div class="ubar"><div class="ubar-in">'
        '<div class="ubar-left">%s%s</div>'
        '<div class="ubar-right tb-calls" data-campus-phones>%s</div>'
        '</div></div>\n'
        '<header class="hdr2"><div class="hdr2-in">'
        '<a class="logo2" href="%s" aria-label="American Barber Institute — home">'
        '<img class="logo2-img" src="/assets/img/logo-final.gif" alt="American Barber Institute" width="385" height="99" fetchpriority="high">'
        '</a>'
        '<nav class="nav2" aria-label="Main">'
        '<div class="nav2-item"><a class="nav2-top" href="%s">%s</a></div>'
        '<div class="nav2-item"><a class="nav2-top" href="%s">%s</a></div>'
        '<div class="nav2-item"><a class="nav2-top" href="%s">%s</a></div>'
        '<div class="nav2-item"><a class="nav2-top" href="%s">%s</a></div>'
        '<div class="nav2-item"><a class="nav2-top" href="%s">%s</a></div>'
        '</nav>'
        '<a class="hdr2-cta" href="#reserve">%s</a>'
        '<button class="hamburger" aria-label="%s" aria-expanded="false" aria-controls="nav-drawer"><span></span><span></span><span></span></button>'
        '</div>'
        '<nav class="nav-drawer" id="nav-drawer" aria-label="Mobile"><div class="container">'
        '<div class="drawer-group"><p class="drawer-h">%s</p><a href="%s">%s</a></div>'
        '<div class="drawer-group">'
        '<a class="drawer-solo" href="%s">%s</a>'
        '<a class="drawer-solo" href="%s">%s</a>'
        '<a class="drawer-solo" href="%s">%s</a>'
        '<a class="drawer-solo" href="%s">%s</a>'
        '</div>'
        '<a class="drawer-cta" href="#reserve"><b>%s</b></a>'
        '</div></nav>'
        '</header>\n'
        '<div class="mstrip"><div class="mstrip-phones">%s</div></div>\n'
        '<div class="lfx-promo">%s</div>\n'
        '<div class="lfx-seats" role="status"><span class="lfx-star" aria-hidden="true">%s</span>'
        '<span class="lfx-seats-t"><b>%s</b><i>%s</i></span></div>\n'
    ) % (
        campus_switch, lang_toggle, ubar_calls,
        home_href,
        NAV["home"], L["programs"],
        NAV["about"], L["why"],
        NAV["guides"], L["guides"],
        NAV["tuition"], L["tuition"],
        NAV["contact"], L["contact"],
        L["book"], L["menu"],
        L["programs"], NAV["home"], L["prog500"],
        NAV["about"], L["why"],
        NAV["guides"], L["guides"],
        NAV["tuition"], L["tuition"],
        NAV["contact"], L["contact"],
        L["book"],
        mstrip_phones, promo, star_svg, h(seats_kicker), h(seats_lead),
    )


# ── MOBILE HERO (image-led, mobile-only — hidden on desktop via CSS) ─
MHERO_BG_BY_PAGE = {
    ("manhattan", "en"): "hero-barber-clinic-2-portrait",
    ("manhattan", "es"): "hero-barber-clinic-2-portrait",
    ("bronx",     "en"): "hero-barber-clinic-2-portrait",
    ("bronx",     "es"): "hero-barber-clinic-2-portrait",
}

def mobile_hero(p):
    lang = p["lang"]; es = lang == "es"
    H_ = D.HERO[lang]
    cta_label = "Reserve Your Spot" if not es else "Reserva Tu Lugar"
    bg_file = MHERO_BG_BY_PAGE[(p["campus"]["slug"], lang)]
    # v3.6 — per-page mobile hero image (4 distinct color palettes)
    # Portrait-cropped WebP+JPEG pair pre-sized to the actual 1080x1609
    # display dimensions (69% smaller than serving the full landscape source).
    return (
        '<section class="lf-mhero" aria-label="American Barber Institute %s clinic floor">\n'
        '  <picture>\n'
        '    <source srcset="/assets/img/' + bg_file + '.webp" type="image/webp">\n'
        '    <img class="lf-mhero__bg" src="/assets/img/' + bg_file + '.jpg"'
        ' alt="ABI barber students training on the clinic floor at the %s" loading="eager"'
        ' fetchpriority="high" width="1080" height="1609">\n'
        '  </picture>\n'
        '  <div class="lf-mhero__scrim"></div>\n'
        '  <div class="lf-mhero__copy">\n'
        '    <p class="lf-mhero__h1" role="heading" aria-level="1">%s <span>%s</span> <em>%s</em></p>\n'
        '    <a class="lf-btn lf-btn--primary lf-btn--lg lf-mhero__cta" href="#reserve">%s</a>\n'
        '  </div>\n'
        '</section>\n'
    ) % (h(p["campus"]["name_en"]), h(p["campus"]["name_en"]),
         h(H_["h1_a"]), h(H_["h1_b"]), h(H_["h1_script"]), h(cta_label))


# ── HERO ─────────────────────────────────────────────────────────────
def hero(p):
    lang = p["lang"]; es = lang == "es"
    H_ = D.HERO[lang]
    is_bx = p["campus"]["slug"] == "bronx"
    sub    = H_["sub_bx"]    if is_bx else H_["sub_man"]
    def _feat(t, ic):
        # "main|subline" renders the subline as a second emphasized row
        if "|" in t:
            main, sub_ = t.split("|", 1)
            return ('<span class="lf-feature lf-feature--multi">%s<span>%s'
                    '<i class="lf-feature__sub">%s</i></span></span>'
                    % (svg(ic, 18), h(main), h(sub_)))
        return '<span class="lf-feature">%s<span>%s</span></span>' % (svg(ic, 18), h(t))
    feats = "".join(_feat(t, ic) for t, ic in D.FEATURES[lang])
    cd = D.COUNTDOWN[lang]
    cells = "".join(
        '<div class="lf-cd__cell"><b data-cd-%s>0</b><span>%s</span></div>' % (k, h(lbl))
        for k, lbl in zip("dhms", cd["cells"])
    )
    # 2-line countdown:
    #   Line 1: <icon> NEXT STARTING DATE: MONDAY, JULY 6, 2026
    #   Line 2: <icon> NEW CLASSES BEGIN THE FIRST MONDAY OF EACH MONTH.
    countdown = (
        '<div class="lf-cd" data-target="%s">\n'
        '  <p class="lf-cd__line lf-cd__line--date">'
        '<span class="lf-cd__label">%s</span> '
        '<span class="lf-cd__date"></span></p>\n'
        '  <p class="lf-cd__line lf-cd__line--sub">%s</p>\n'
        '  <div class="lf-cd__grid">%s</div>\n'
        '</div>'
    ) % (NEXT_ISO, h(cd["label"]), h(cd["sub"]), cells)
    # v3.1 — campus kicker removed per spec
    return (
        '<section class="lf-hero">\n'
        '  <div class="lf-wrap lf-hero__in">\n'
        '    <div class="lf-hero__copy lf-rv">\n'
        '      <h1 class="lf-h1">%s <span class="lf-h1__b">%s</span> '
        '<span class="lf-h1__script">%s</span></h1>\n'
        '      <p class="lf-hero__sub">%s</p>\n'
        '      <div class="lf-features">%s</div>\n'
        '      %s\n'
        '    </div>\n'
        '    %s\n'
        '  </div>\n'
        '</section>\n'
    ) % (h(H_["h1_a"]), h(H_["h1_b"]), h(H_["h1_script"]),
         sub, feats, countdown, lead_form(p))


def lead_form(p):
    lang = p["lang"]
    f = D.FORM[lang]
    # Campus dropdown is locked to the page's own campus — no cross-campus options.
    loc_opts = "".join('<option>%s</option>' % h(o)
                       for o in D.LOC_OPTS_BY_CAMPUS[(p["campus"]["slug"], lang)])
    lang_opts = "".join('<option>%s</option>' % h(o) for o in f["lang_opts"])
    return (
        '<div class="lf-hero__form lf-rv">\n'
        '<div class="lf-form lf-form--ghl" id="reserve">\n'
        '  <h3 class="lf-form__h">%(h)s</h3>\n'
        '  <p class="lf-form__sub">%(sub)s</p>\n'
        '  <div class="ghl-form-wrap">'
        '<iframe src="https://api.leadconnectorhq.com/widget/form/%(ghl_id)s" '
        'style="width:100%%;height:%(ghl_h)spx;border:none;border-radius:3px" '
        'id="inline-%(ghl_id)s" data-layout="{\'id\':\'INLINE\'}" data-trigger-type="alwaysShow" '
        'data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" '
        'data-deactivation-type="neverDeactivate" data-deactivation-value="" '
        'data-form-name="%(ghl_name)s" data-height="%(ghl_h)s" data-layout-iframe-id="inline-%(ghl_id)s" '
        'data-form-id="%(ghl_id)s" title="%(ghl_name)s"></iframe></div>\n'
        '<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>\n'
        '</div>'
    ) % {
        "id": p["id"], "campus": p["campus"]["slug"], "lang": lang,
        # GHL form IDs are per-language (unified form for all campuses).
        # EN = 01.GET TRAINED WITH ABI FORM - ABI.com
        # ES = 01.GET TRAINED WITH ABI FORM - ABI.com - ESP
        "ghl_id": "H4C1nJmpLO3cNx4OrlK2" if lang == "es" else "3ghObGjHiLN3LgKBfKGG",
        "ghl_h": 795 if lang == "es" else 757,
        "ghl_name": "01.GET TRAINED WITH ABI FORM - ABI.com - ESP" if lang == "es" else "01.GET TRAINED WITH ABI FORM - ABI.com",
        "h": h(f["h"]), "sub": h(f["sub"]),
        "first": h(f["first"]), "last": h(f["last"]),
        "phone": h(f["phone"]), "email": h(f["email"]),
        "loc_label": h(f["loc_label"]), "loc_opts": loc_opts,
        "lang_label": h(f["lang_label"]), "lang_opts": lang_opts,
        "msg_label": h(f["msg_label"]), "msg_ph": h(f["msg_ph"]),
        "submit": h(f["submit"]), "trust": h(f["trust"]),
        "consent_call": h(f["consent_call"]), "consent_sms": h(f["consent_sms"]),
        "consent": h(f["consent"]),
    }


# ── STATS ────────────────────────────────────────────────────────────
def section_stats(p):
    items = "".join(
        '<div class="lf-stat lf-rv"><div class="lf-stat__n">%s</div>'
        '<span class="lf-stat__label">%s</span></div>' % (h(n), h(l))
        for n, l in D.STATS[p["lang"]]
    )
    return ('<section class="lf-section lf-section--tight"><div class="lf-wrap">'
            '<div class="lf-stats">%s</div></div></section>\n' % items)


# ── ABOUT THE PROGRAM (verbatim, campus-specific) ────────────────────
def section_about(p):
    from urllib.parse import quote
    eb, ti = D.ABOUT_HEAD[p["lang"]]
    paras = D.ABOUT[(p["campus"]["slug"], p["lang"])]
    body = "".join('<p>%s</p>' % h(x) for x in paras)
    addr = p["campus"]["addr_full_es" if p["lang"] == "es" else "addr_full_en"]
    name = p["campus"]["name_es" if p["lang"] == "es" else "name_en"]
    map_q = quote("American Barber Institute, " + p["campus"]["addr_full_en"])
    map_src = "https://www.google.com/maps?q=%s&amp;z=16&amp;output=embed" % map_q
    reviews_href = p["campus"]["google_listing_url"]
    reviews_label = "Ver nuestras reseñas de Google →" if p["lang"] == "es" else "Read our Google reviews →"
    return (
        '<section class="lf-section lf-section--alt"><div class="lf-wrap">%s\n'
        '  <div class="lf-about">\n'
        '    <div class="lf-about__body lf-rv">%s</div>\n'
        '    <aside class="lf-about__card lf-rv">\n'
        '      <h3 class="lf-h3">%s</h3>\n'
        '      <p class="lf-about__addr">%s%s</p>\n'
        '      <p class="lf-about__phone"><a href="tel:%s">%s %s</a></p>\n'
        '      <div class="lf-map" style="margin-top:1rem;border-radius:12px;overflow:hidden;aspect-ratio:16/10"><iframe title="%s" src="%s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="width:100%%;height:100%%;border:0;display:block"></iframe></div>\n'
        '      <a class="lf-map-reviews" href="%s" target="_blank" rel="noopener" style="display:inline-block;margin-top:.7rem;font-weight:700">★ %s</a>\n'
        '    </aside>\n'
        '  </div>\n'
        '</div></section>\n'
    ) % (section_head(eb, ti), body, h(name),
         svg("pin", 14), h(addr),
         h(p["phone"][2]), svg("phone", 14), h(p["phone"][1]),
         h(name), map_src, reviews_href, reviews_label)


# ── 3 EASY STEPS (right after About) ─────────────────────────────────
def section_three_steps(p):
    lang = p["lang"]
    eb, ti = D.THREE_STEPS_HEAD[lang]
    cards = ""
    for i, (head, body) in enumerate(D.THREE_STEPS[lang], 1):
        cards += (
            '<div class="lf-step lf-rv">'
            '<div class="lf-step__n">%02d</div>'
            '<h3 class="lf-step__h">%s</h3>'
            '<p class="lf-step__p">%s</p>'
            '</div>'
        ) % (i, h(head), h(body))
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-steps">%s</div></div></section>\n'
            % (section_head(eb, ti), cards))


# ── SKILLS & TECHNIQUES ──────────────────────────────────────────────
def section_earnings(p):
    """Career Earnings — 3 tier cards. Ports the main site's sec--earnings block."""
    eb, ti = D.EARNINGS_HEAD[p["lang"]]
    cards = "".join(
        '<div class="lf-earn__card lf-rv">'
        '<div class="lf-earn__yr">%s</div>'
        '<div class="lf-earn__amt">%s</div>'
        '<p class="lf-earn__desc">%s</p>'
        '</div>'
        % (h(yr), h(amt), h(desc))
        for yr, amt, desc in D.EARNINGS_TIERS[p["lang"]]
    )
    note = D.EARNINGS_NOTE[p["lang"]]
    return ('<section class="lf-section lf-section--alt lf-section--earn"><div class="lf-wrap">%s'
            '<div class="lf-earn">%s</div>'
            '<p class="lf-earn__note lf-rv">%s</p></div></section>\n'
            % (section_head(eb, ti), cards, h(note)))


def section_techniques(p):
    eb, ti = D.TECH_HEAD[p["lang"]]
    chips = "".join('<span class="lf-tech">%s%s</span>' % (svg("check", 15), h(t))
                    for t in D.TECHNIQUES[p["lang"]])
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-tech-grid lf-rv">%s</div></div></section>\n'
            % (section_head(eb, ti), chips))


# ── COURSE MODULES (curriculum) ──────────────────────────────────────
def section_modules(p):
    eb, ti = D.MODULES_HEAD[p["lang"]]
    cards = ""
    for i, (name, items) in enumerate(D.MODULES[p["lang"]], 1):
        lis = "".join('<li>%s</li>' % h(x) for x in items)
        cards += ('<div class="lf-module lf-rv"><div class="lf-module__n">%02d</div>'
                  '<h3 class="lf-h3">%s</h3><ul class="lf-module__list">%s</ul></div>'
                  % (i, h(name), lis))
    return ('<section class="lf-section lf-section--alt"><div class="lf-wrap">%s'
            '<div class="lf-modules">%s</div></div></section>\n'
            % (section_head(eb, ti), cards))


# ── TUITION ──────────────────────────────────────────────────────────
def section_tuition(p):
    eb, ti = D.TUITION_HEAD[p["lang"]]
    note = D.TUITION_NOTE[p["lang"]]
    popular = "Más Popular" if p["lang"] == "es" else "Most Popular"
    cards = ""
    for pl in D.TUITION[p["lang"]]:
        cls = "lf-plan lf-rv" + (" lf-plan--feature" if pl["feature"] else "")
        badge = ('<span class="lf-plan__badge">%s</span>' % popular) if pl["feature"] else ""
        cards += (
            '<div class="%s">%s<div class="lf-plan__name">%s</div>'
            '<div class="lf-plan__sched">%s</div>'
            '<div class="lf-plan__hours">%s</div>'
            '<div class="lf-plan__price">%s</div>'
            '<div class="lf-plan__terms">%s</div>'
            '<a class="lf-btn lf-btn--primary lf-plan__cta" href="#reserve">%s</a></div>'
            % (cls, badge, h(pl["name"]), h(pl["sched"]), h(pl["hours"]),
               h(pl["price"]), h(pl["terms"]),
               "¡Hagámoslo!" if p["lang"] == "es" else "Let's Do It")
        )
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-tuition">%s</div>'
            '<p class="lf-tuition__note lf-rv">%s</p></div></section>\n'
            % (section_head(eb, ti, note if False else None), cards, h(note)))


# ── ENTRANCE REQUIREMENTS ────────────────────────────────────────────
def section_requirements(p):
    eb, ti = D.REQ_HEAD[p["lang"]]
    items = "".join('<li class="lf-req lf-rv">%s<span>%s</span></li>' % (svg("check", 18), h(x))
                    for x in D.REQUIREMENTS[p["lang"]])
    return ('<section class="lf-section lf-section--alt"><div class="lf-wrap">%s'
            '<ul class="lf-reqs">%s</ul></div></section>\n'
            % (section_head(eb, ti), items))


# ── INSIDE ABI (showcase clips) ──────────────────────────────────────
def section_showcase(p):
    eb, ti = D.SHOWCASE_HEAD[p["lang"]]
    lead = D.SHOWCASE_LEAD[p["lang"]]
    cards = ""
    for i, (slug, en_cap, es_cap) in enumerate(D.SHOWCASE_CLIPS, 1):
        cap = es_cap if p["lang"] == "es" else en_cap
        cards += (
            '<div class="lf-clip lf-rv">'
            '<video class="lf-clip__video" muted playsinline loop preload="none"'
            ' poster="/assets/img/lf-showcase-%d.jpg" src="%s%s.mp4"></video>'
            '<button class="lf-clip__play" type="button" aria-label="%s">'
            '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
            '</button><div class="lf-clip__cap">%s</div></div>'
            % (i, D.SHOWCASE_CDN_BASE, slug,
               "Reproducir" if p["lang"] == "es" else "Play", h(cap))
        )
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-showcase">%s</div></div></section>\n'
            % (section_head(eb, ti, lead), cards))


# ── reel video block helper (used by student voices + bronx extra) ──
PLAY_BTN = ('<button class="lf-reel__play" type="button" aria-label="Play video">'
            '<svg class="lf-reel__icon-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'
            '<svg class="lf-reel__icon-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>'
            '</button>')

def _reel_media(vid, poster, label):
    # vid is now a full URL (Vercel Blob CDN); poster remains a filename under /assets/img/.
    return ('<div class="lf-reel__media"><video class="lf-reel__video" muted loop playsinline'
            ' preload="metadata" src="%s" poster="/assets/img/%s"'
            ' aria-label="%s"></video>%s</div>' % (h(vid), h(poster), h(label), PLAY_BTN))


def section_student_voices(p):
    sv = D.STUDENT_VOICES[p["lang"]]
    media = "".join(_reel_media(v, ps, "ABI student testimonial %d" % i)
                    for i, (v, ps) in enumerate(D.STUDENT_VOICES_VIDEOS, 1))
    return (
        '<section class="lf-section lf-section--alt"><div class="lf-wrap">\n'
        '  <div class="lf-reel lf-reel--triple lf-rv">\n'
        '    <div class="lf-section__head" style="margin-bottom:1.2rem">'
        '<span class="lf-eyebrow">%s</span><h2 class="lf-h2">%s</h2>'
        '<p class="lf-lead">%s</p></div>\n'
        '    <div class="lf-reel__grid">%s</div>\n'
        '  </div>\n'
        '</div></section>\n'
    ) % (h(sv["eyebrow"]), h(sv["title"]), h(sv["sub"]), media)


def section_bronx_extra(p):
    if p["campus"]["slug"] != "bronx":
        return ""
    bx = D.BRONX_EXTRA[p["lang"]]
    media = "".join(_reel_media(v, ps, "Bronx student testimonial %d" % i)
                    for i, (v, ps) in enumerate(D.BRONX_EXTRA_VIDEOS, 1))
    return (
        '<section class="lf-section"><div class="lf-wrap">\n'
        '  <div class="lf-reel lf-reel--triple lf-rv">\n'
        '    <div class="lf-section__head" style="margin-bottom:1.2rem">'
        '<span class="lf-eyebrow">%s</span><h2 class="lf-h2">%s</h2>'
        '<p class="lf-lead">%s</p></div>\n'
        '    <div class="lf-reel__grid">%s</div>\n'
        '  </div>\n'
        '</div></section>\n'
    ) % (h(bx["eyebrow"]), h(bx["title"]), h(bx["sub"]), media)


# ── WATCH US (YouTube) ───────────────────────────────────────────────
def section_videos(p):
    eb, ti = D.YT_HEAD[p["lang"]]
    cards = ""
    for vid, en_cap, es_cap in D.YT_CLIPS:
        cap = es_cap if p["lang"] == "es" else en_cap
        cards += (
            '<div class="lf-clip lf-rv">'
            '<a href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener">'
            '<img loading="lazy" src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s"'
            ' width="480" height="360" style="width:100%%;height:100%%;object-fit:cover"></a>'
            '<div class="lf-clip__cap">▶ %s</div></div>'
            % (vid, vid, h(cap), h(cap))
        )
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-showcase">%s</div></div></section>\n'
            % (section_head(eb, ti), cards))


# ── GALLERY — horizontal "real floor" film-strip, not a static grid ──
_FLOOR_VIDEO = "https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/floor/floor-03.mp4"

def section_gallery(p):
    es = p["lang"] == "es"
    eb, ti = D.GALLERY_HEAD[p["lang"]]
    see_link = "Ver la Galería Completa &rarr;" if es else "See the Full Gallery &rarr;"
    see_more = "Ver Más Fotos" if es else "See More Photos"
    gallery_href = "/spanish/gallery" if es else "/gallery"
    alts_es = [
        "Foto real de la clínica de ABI %d" % (i + 1) for i in range(len(D.GALLERY))
    ]
    alts_en = [
        "Real photo from the ABI clinic floor %d" % (i + 1) for i in range(len(D.GALLERY))
    ]
    alts = alts_es if es else alts_en
    cards = "".join(
        '<a class="lf-floor__card" href="%s"><img loading="lazy" decoding="async" src="/assets/img/%s" alt="%s"></a>'
        % (h(gallery_href), h(g), h(a)) for g, a in zip(D.GALLERY, alts)
    )
    video_card = (
        '<div class="lf-floor__card lf-floor__card--video" '
        'onmouseenter="this.querySelector(\'video\').play()" onmouseleave="this.querySelector(\'video\').pause()">'
        '<video muted loop playsinline preload="none" poster="/assets/img/gallery/posters/floor-03.jpg" src="%s"></video>'
        '<span class="lf-floor__play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></div>'
        % h(_FLOOR_VIDEO)
    )
    end_card = (
        '<a class="lf-floor__card lf-floor__card--end" href="%s">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg><span>%s</span></a>'
        % (h(gallery_href), h(see_more))
    )
    return (
        '<section class="lf-section lf-section--alt lf-floor"><div class="lf-wrap">'
        '<div class="lf-floor__head">%s<a class="lf-floor__see" href="%s">%s</a></div>'
        '<div class="lf-floor__track">%s%s%s</div>'
        '</div></section>\n'
        % (section_head(eb, ti), h(gallery_href), see_link, cards, video_card, end_card)
    )


# ── REVIEWS (split per campus; real Google reviews, no widget) ──────
def section_reviews(p):
    eb, ti = D.REVIEWS_HEAD[p["lang"]]
    lead = D.REVIEWS_LEAD[p["lang"]]
    cards = ""
    campus_slug = p["campus"]["slug"]
    for r in D.REVIEWS_BY_CAMPUS[campus_slug][p["lang"]]:
        ini = "".join(w[0] for w in r["name"].split()[:2]).upper()
        cards += (
            '<div class="lf-review lf-rv"><div class="lf-review__stars">★★★★★</div>'
            '<p class="lf-review__q">“%s”</p>'
            '<div class="lf-review__who"><div class="lf-review__av">%s</div>'
            '<div><div class="lf-review__name">%s</div>'
            '<div class="lf-review__role">%s</div></div></div></div>'
            % (h(r["q"]), h(ini), h(r["name"]), h(r["role"]))
        )
    return ('<section class="lf-section"><div class="lf-wrap">%s'
            '<div class="lf-reviews">%s</div></div></section>\n'
            % (section_head(eb, ti, lead), cards))


# ── CONTACT BOX (campus-aware: Manhattan = 2 numbers, Bronx = 1) ─────
def section_contact(p):
    lang = p["lang"]
    eb, ti = D.CONTACT_HEAD[lang]
    L = D.CONTACT_LABELS[lang]
    campus_slug = p["campus"]["slug"]
    addr = p["campus"]["addr_full_es" if lang == "es" else "addr_full_en"]
    name = p["campus"]["name_es" if lang == "es" else "name_en"]
    # Use the client-provided Google Business Profile short URL per campus so
    # the "See on Maps" CTA lands on THIS campus's real listing (with reviews).
    maps_url = p["campus"]["google_listing_url"]

    phone_items = ""
    for ph in D.CONTACT_PHONES_BY_CAMPUS[campus_slug]:
        tag = L[ph["label_key"]]
        phone_items += (
            '<li class="lf-contact__phone">'
            '<a href="tel:%s">%s<span class="lf-contact__num">%s</span></a>'
            '<span class="lf-contact__tag">%s</span></li>'
            % (h(ph["tel"]), svg("phone", 16), h(ph["display"]), h(tag))
        )

    return (
        '<section class="lf-section lf-section--alt" id="contact"><div class="lf-wrap">%s\n'
        '  <div class="lf-contact lf-rv">\n'
        '    <div class="lf-contact__card">\n'
        '      <h3 class="lf-h3">%s</h3>\n'
        '      <p class="lf-contact__row"><span class="lf-contact__label">%s</span>'
        '<span class="lf-contact__val">%s%s · '
        '<a class="lf-contact__map" href="%s" target="_blank" rel="noopener">%s →</a></span></p>\n'
        '      <p class="lf-contact__row"><span class="lf-contact__label">%s</span>'
        '<ul class="lf-contact__phones">%s</ul></p>\n'
        '      <p class="lf-contact__row"><span class="lf-contact__label">%s</span>'
        '<a class="lf-contact__val" href="mailto:%s">%s</a></p>\n'
        '      <p class="lf-contact__row"><span class="lf-contact__label">%s</span>'
        '<span class="lf-contact__val">%s</span></p>\n'
        '    </div>\n'
        '  </div>\n'
        '</div></section>\n'
    ) % (
        section_head(eb, ti),
        h(name),
        h(L["addr"]), svg("pin", 14), h(addr), h(maps_url), h(L["directions"]),
        h(L["phone"]), phone_items,
        h(L["email"]), h(D.CONTACT_EMAIL), h(D.CONTACT_EMAIL),
        h(L["hours"]),
        "<br>".join(h(line) for line in D.CONTACT_HOURS[lang]),
    )


# ── FAQ ──────────────────────────────────────────────────────────────
def section_faq(p):
    eb, ti = D.FAQ_HEAD[p["lang"]]
    items = "".join(
        '<details class="lf-rv"><summary>%s</summary><div class="lf-faq__a">%s</div></details>'
        % (h(q), h(a)) for q, a in D.faq(p["lang"], p["phone"][1],
                                          p["campus"]["name_es" if p["lang"] == "es" else "name_en"])
    )
    return ('<section class="lf-section lf-section--alt"><div class="lf-wrap">%s'
            '<div class="lf-faq">%s</div></div></section>\n'
            % (section_head(eb, ti), items))


# ── FOOTER (3 CTAs kept here as the single sticky CTA set) ──────────
def footer(p):
    ft = D.FOOTER[p["lang"]]
    tel = p["phone"][2]
    socials = (
        '<a class="lf-soc" href="https://www.facebook.com/Abi.Education/" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>'
        '<a class="lf-soc" href="https://www.instagram.com/americanbarberinstitute/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>'
        '<a class="lf-soc" href="https://twitter.com/amerbarberedu" target="_blank" rel="noopener" aria-label="X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3z"/></svg></a>'
        '<a class="lf-soc" href="https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.5 12 4.5 12 4.5s-7 0-8.9.6A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.6 8.9.6 8.9.6s7 0 8.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.3V8.7L15.9 12z"/></svg></a>'
        '<a class="lf-soc" href="https://www.pinterest.com/alexzholendz/american-barber-institute/" target="_blank" rel="noopener" aria-label="Pinterest"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.6 2-2.6.9 0 1.4.7 1.4 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.6-1.9-4.4-4.5-4.4a4.7 4.7 0 0 0-4.9 4.7c0 .9.4 1.9.8 2.5l-.3 1.1c-.1.4-.3.5-.7.3-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 1.9-1.2 2.6A10 10 0 1 0 12 2z"/></svg></a>'
    )
    addr = p["campus"]["addr_full_es" if p["lang"] == "es" else "addr_full_en"]
    return (
        '<footer class="lf-footer"><div class="lf-wrap">\n'
        '  <h3 class="lf-h2">%s</h3>\n'
        '  <p>%s</p>\n'
        '  <p class="lf-footer__addr">%s%s · <a href="tel:%s">%s</a></p>\n'
        '  <div class="lf-footer__socials">%s</div>\n'
        '  <p class="lf-footer__fine">%s</p>\n'
        '  <p class="lf-footer__fine lf-footer__priv">%s</p>\n'
        '</div></footer>\n'
    ) % (
        h(ft["h"]), h(ft["sub"]),
        svg("pin", 14), h(addr), h(p["phone"][2]), h(p["phone"][1]),
        socials, h(ft["fine"]),
        ('<a href="/privacy-and-policy">Pol&iacute;tica de Privacidad</a>'
         if p["lang"] == "es" else
         '<a href="/privacy-and-policy">Privacy Policy</a>'),
    )


# ── Social profiles (sameAs for Organization schema) ────────────────
SAME_AS = [
    "https://www.facebook.com/Abi.Education/",
    "https://www.instagram.com/americanbarberinstitute/",
    "https://twitter.com/amerbarberedu",
    "https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ",
    "https://www.pinterest.com/alexzholendz/american-barber-institute/",
]


# ── HEAD ─────────────────────────────────────────────────────────────
def page_head(p):
    es = p["lang"] == "es"
    canonical = SITE + "/" + p["path"]
    alt_url   = SITE + "/" + p["alt"]
    en_url, es_url = (alt_url, canonical) if es else (canonical, alt_url)
    campus_slug = p["campus"]["slug"]
    campus_name = p["campus"]["name_es" if es else "name_en"]

    # 1) Primary: TradeSchool + LocalBusiness + EducationalOrganization
    ld_org = {
        "@context": "https://schema.org",
        "@type": ["TradeSchool", "LocalBusiness", "EducationalOrganization"],
        "@id": canonical + "#org",
        "name": "American Barber Institute — " + p["campus"]["name_en"],
        "url": canonical,
        "telephone": p["phone"][2],
        "email": "admission@abi.edu",
        "image": SITE + "/assets/img/lf-og-cover.jpg",
        "logo": SITE + LOGO_SRC,
        "description": p["desc"],
        "foundingDate": "1996",
        "priceRange": "$4,600–$5,600",
        "sameAs": SAME_AS,
        "address": {"@type": "PostalAddress",
                    "streetAddress": p["campus"]["addr_full_en"].split(",")[0].strip(),
                    "addressLocality": "Bronx" if campus_slug == "bronx" else "New York",
                    "addressRegion": "NY",
                    "postalCode": "10461" if campus_slug == "bronx" else "10018",
                    "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates",
                "latitude": p["campus"]["latlng"][0], "longitude": p["campus"]["latlng"][1]},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
             "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday","Sunday"],
             "opens": "09:00", "closes": "19:00"},
        ],
        "aggregateRating": {
            "@type": "AggregateRating", "ratingValue": "4.6",
            "reviewCount": "100", "bestRating": "5", "worstRating": "1"
        },
        "review": [
            {"@type": "Review",
             "author": {"@type": "Person", "name": r["name"]},
             "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
             "reviewBody": r["q"]}
            for r in D.REVIEWS_BY_CAMPUS[campus_slug][p["lang"]]
        ],
        "paymentAccepted": ["Cash", "Credit Card", "Financial Aid", "GI Bill", "ACCES-VR"],
    }

    # 2) Course
    ld_course = {
        "@context": "https://schema.org", "@type": "Course",
        "name": "500-Hour Master Barber Program",
        "description": p["desc"],
        "provider": {"@type": "TradeSchool", "@id": canonical + "#org",
                     "name": "American Barber Institute",
                     "sameAs": "https://www.americanbarberinstitute.com/"},
        "educationalCredentialAwarded": "Eligibility for New York State Master Barber license",
        "occupationalCredentialAwarded": "NY State Master Barber license (after passing State Board Exam)",
        "timeRequired": "PT500H",
        "inLanguage": ["en", "es"],
        "hasCourseInstance": [{
            "@type": "CourseInstance",
            "courseMode": "in-person",
            "name": "500-Hour Master Barber Program — " + campus_name,
            "location": {"@type": "Place", "name": campus_name,
                         "address": ld_org["address"]},
            "courseWorkload": "PT30H",  # 30 hrs/week full-time
            "instructor": {"@type": "Person", "name": "King David Ayeoribe"}
        }],
        "offers": [
            {"@type": "Offer", "name": "Plan A — Morning",   "price": "5600", "priceCurrency": "USD", "category": "Tuition"},
            {"@type": "Offer", "name": "Plan B — Afternoon", "price": "4600", "priceCurrency": "USD", "category": "Tuition"},
            {"@type": "Offer", "name": "Plan C — Weekend",   "price": "4600", "priceCurrency": "USD", "category": "Tuition"},
        ]
    }

    # 3) FAQPage — every page's 8 FAQs as structured data
    ld_faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in D.faq(p["lang"], p["phone"][1], campus_name)
        ]
    }

    # 4) BreadcrumbList
    ld_bc = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "American Barber Institute", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "500-Hour Master Barber Program — " + campus_name, "item": canonical},
        ]
    }

    # 5) VideoObject (one per testimonial) so video clips are AEO-friendly
    student_voices_videos = D.STUDENT_VOICES_VIDEOS
    ld_videos = [
        {"@context": "https://schema.org", "@type": "VideoObject",
         "name": "ABI Student Testimonial " + str(i + 1),
         "description": "Student of the American Barber Institute (ABI) sharing their experience at the " + campus_name + ".",
         "thumbnailUrl": SITE + "/assets/img/" + ps,
         "uploadDate": "2024-09-01",
         "contentUrl": vid,
         "publisher": {"@type": "Organization", "name": "American Barber Institute",
                       "logo": {"@type": "ImageObject", "url": SITE + LOGO_SRC}}}
        for i, (vid, ps) in enumerate(student_voices_videos)
    ]

    # Combine into one ordered list; emit each as its own <script>
    ld_blocks = [ld_org, ld_course, ld_faq, ld_bc] + ld_videos
    return (
'<!DOCTYPE html>\n<html lang="%(lang)s">\n<head>\n'
'<meta charset="utf-8">\n'
'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
'<title>%(title)s</title>\n'
'<meta name="description" content="%(desc)s">\n'
'<link rel="canonical" href="%(canonical)s">\n'
'<link rel="alternate" hreflang="en" href="%(en_url)s">\n'
'<link rel="alternate" hreflang="en-US" href="%(en_url)s">\n'
'<link rel="alternate" hreflang="es" href="%(es_url)s">\n'
'<link rel="alternate" hreflang="es-US" href="%(es_url)s">\n'
'<link rel="alternate" hreflang="x-default" href="%(en_url)s">\n'
'<meta property="og:title" content="%(title)s">\n'
'<meta property="og:description" content="%(desc)s">\n'
'<meta property="og:type" content="website">\n'
'<meta property="og:site_name" content="American Barber Institute">\n'
'<meta property="og:url" content="%(canonical)s">\n'
'<meta property="og:image" content="%(site)s/assets/img/lf-og-cover.jpg">\n'
'<meta property="og:image:width" content="1200">\n'
'<meta property="og:image:height" content="630">\n'
'<meta property="og:locale" content="%(oglocale)s">\n'
'<meta name="twitter:card" content="summary_large_image">\n'
'<meta name="twitter:title" content="%(title)s">\n'
'<meta name="twitter:description" content="%(desc)s">\n'
'<meta name="twitter:image" content="%(site)s/assets/img/lf-og-cover.jpg">\n'
'<meta name="robots" content="index, follow, max-image-preview:large">\n'
'<meta name="theme-color" content="%(theme_color)s">\n'
'<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n'
'<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
'<link rel="manifest" href="/site.webmanifest">\n'
'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
'<link rel="preconnect" href="https://text.pollinations.ai" crossorigin>\n'
'<link rel="preload" href="/assets/img/logo-final.gif" as="image" fetchpriority="high">\n'
'<link rel="preload" href="/assets/img/%(mhero_bg)s.webp" as="image" type="image/webp" media="(max-width:768px)" fetchpriority="high">\n'
'<link rel="preload" href="/assets/img/hero-barber-clinic-2.webp" as="image" type="image/webp" media="(min-width:769px)">\n'
'<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&display=swap" rel="stylesheet">\n'
'<link rel="stylesheet" href="/assets/css/site-header.min.css?v=%(cssv)s">\n'
'<link rel="stylesheet" href="/assets/css/funnels.min.css?v=%(cssv)s">\n'
'<link rel="stylesheet" href="/assets/css/chatbot.min.css?v=%(cssv)s">\n'
'%(ld_scripts)s'
'<script src="/assets/js/analytics.js?v=7" defer></script>\n'
'<script defer src="/_vercel/insights/script.js"></script>\n'
'<script src="/assets/js/campus.js?v=2" defer></script>\n'
'<script src="/assets/js/landing.js?v=32" defer></script>\n'
'</head>\n<body class="shell2 lf-page %(theme)s" data-campus="%(campus_slug)s">\n'
'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NKLLGPC" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n'
    ) % {
        "lang": p["lang"], "title": h(p["title"]), "desc": h(p["desc"]),
        "canonical": h(canonical), "en_url": h(en_url), "es_url": h(es_url),
        "site": SITE, "oglocale": "es_US" if es else "en_US", "cssv": CSS_V,
        "mhero_bg": MHERO_BG_BY_PAGE[(p["campus"]["slug"], p["lang"])],
        "theme_color": p.get("theme_color", "#0E4D5C"),
        "ld_scripts": "".join(
            '<script type="application/ld+json">%s</script>\n' % json.dumps(b, ensure_ascii=False)
            for b in ld_blocks
        ),
        "theme": p["theme_class"],
        "campus_slug": p["campus"]["slug"],
    }


CHAT_ICON  = '<path d="M21 12a8.5 8.5 0 0 1-8.5 8.5c-1.6 0-3-.4-4.3-1L3 21l1.6-4.8A8.5 8.5 0 1 1 21 12z"/>'
SCISSORS_I = '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>'

def mobile_cta_bar(p):
    es = p["lang"] == "es"
    tel = p["phone"][2]            # +1XXXXXXXXXX
    sms_target = tel               # SMS goes to same campus number
    labels = {
        "call":  "Llamar" if es else "Call Now",
        "text":  "Mensaje" if es else "Text Us",
        "apply": "Aplicar" if es else "Apply Now",
    }
    return (
        '<nav class="lf-mcta" aria-label="%s">\n'
        '  <a class="lf-mcta__btn lf-mcta__btn--call" href="tel:%s">'
        '%s<span>%s</span></a>\n'
        '  <a class="lf-mcta__btn lf-mcta__btn--text" href="sms:%s">'
        '%s<span>%s</span></a>\n'
        '  <a class="lf-mcta__btn lf-mcta__btn--apply" href="#reserve">'
        '%s<span>%s</span></a>\n'
        '</nav>\n'
    ) % (
        "Acciones rápidas" if es else "Quick actions",
        h(tel),       svg("phone", 16),    h(labels["call"]),
        h(sms_target),
        ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
         ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         + CHAT_ICON + '</svg>'),
        h(labels["text"]),
        ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
         ' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         + SCISSORS_I + '</svg>'),
        h(labels["apply"]),
    )


def page_tail():
    return (
        '<script src="/assets/js/funnels.js?v=%s" defer></script>\n'
        '<!-- GHL chat widget (VIBE AI). Alex chatbot preserved in /assets/js/chatbot.js '
        '— to restore Alex: delete this block and re-add the chatbot.js script tag. -->\n'
        ''
        '<script src="https://widgets.leadconnectorhq.com/loader.js" '
        'data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" '
        'data-widget-id="689f4917512e48b4268bf335"></script>\n'
        '<script>(function(){var t=setInterval(function(){var w=document.querySelector("chat-widget");if(w&&w.shadowRoot){clearInterval(t);var s=document.createElement("style");s.textContent=".lc_text-widget--prompt{display:none!important}@media(max-width:768px){.lc_text-widget,.lc_text-widget--bubble{bottom:140px!important;right:12px!important}}";w.shadowRoot.appendChild(s);}},400);setTimeout(function(){clearInterval(t)},15000);})();</script>\n'
        '</body>\n</html>\n'
    ) % (JS_V,)


# ── ASSEMBLE ─────────────────────────────────────────────────────────
def build_page(p):
    skip_link = ('<a class="lf-skip" href="#content">'
                 + ('Saltar al contenido' if p["lang"] == "es" else 'Skip to content')
                 + '</a>\n')
    parts = [
        page_head(p),
        skip_link,
        header(p),
        '<main id="content">\n',
        mobile_hero(p),
        hero(p),
        section_student_voices(p),
        section_stats(p),
        section_about(p),
        section_three_steps(p),
        section_earnings(p),
        section_techniques(p),
        section_tuition(p),
        section_requirements(p),
        section_showcase(p),
    ]
    # Removed: section_modules (Course Modules), section_videos
    # (See ABI in Action — YouTube clips), section_bronx_extra (duplicated
    # Student Voices). Per content spec — no replacements.
    parts += [
        section_gallery(p),
        section_reviews(p),
        section_contact(p),
        section_faq(p),
        '</main>\n',
        footer(p),
        mobile_cta_bar(p),
        page_tail(),
    ]
    out_dir = os.path.join(ROOT, p["path"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    return out_path


def _write_landing_sitemap():
    """These 4 pages are real ad-landing pages but were never in any sitemap
    (audit finding 2026-07-08) — write a dedicated sub-sitemap for them at the
    true repo root (one level above landing-funnels/) and reference it from
    the main site's sitemap.xml index."""
    repo_root = os.path.dirname(ROOT)
    today = datetime.date.today().isoformat()
    entries = []
    for p in D.PAGES:
        loc = f"{SITE}/{p['path']}"
        alt_lang = 'es' if p['lang'] == 'en' else 'en'
        alt_loc = f"{SITE}/{p['alt']}"
        block = [
            '  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{today}</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.9</priority>',
            f'    <xhtml:link rel="alternate" hreflang="{p["lang"]}" href="{loc}"/>',
            f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{alt_loc}"/>',
            '  </url>',
        ]
        entries.append('\n'.join(block))
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + '\n'.join(entries) + '\n</urlset>\n'
    )
    dest = os.path.join(repo_root, 'landing-sitemap.xml')
    open(dest, 'w', encoding='utf-8').write(xml)
    print("✓ landing-sitemap.xml (%d URLs)" % len(D.PAGES))


def main():
    written = [build_page(p) for p in D.PAGES]
    for w in written:
        print("✓", os.path.relpath(w, ROOT))
    print("%d landing pages generated." % len(written))
    _write_landing_sitemap()


if __name__ == "__main__":
    main()
