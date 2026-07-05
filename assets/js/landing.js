/* ABI Landing Pages — shared behavior */
(function () {
  'use strict';

  var LANG = document.documentElement.lang === 'es' ? 'es' : 'en';
  document.documentElement.classList.add('js');

  /* ── CONFIG ──────────────────────────────────────────────
     Lead form endpoint. Posts to FormSubmit's AJAX endpoint, which
     delivers submissions to admission@abi.edu (the same inbox the
     site's mailto forms use). Returns JSON; the submit handler shows
     success only on response.ok and an error message otherwise.      */
  var FORM_ENDPOINT = 'https://formsubmit.co/ajax/admission@abi.edu';

  /* ── Next start date: first Monday of next month ───────── */
  function nextFirstMonday() {
    var now = new Date();
    var d = new Date(now.getFullYear(), now.getMonth(), 1);
    // first Monday of current month
    while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
    if (d <= now) {
      d = new Date(now.getFullYear(), now.getMonth() + 1, 1);
      while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
    }
    return d;
  }
  var startDate = nextFirstMonday();
  var fmt = new Intl.DateTimeFormat(LANG === 'es' ? 'es-US' : 'en-US', {
    weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
  });
  var dateStr = fmt.format(startDate);
  if (LANG === 'es') dateStr = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
  document.querySelectorAll('[data-next-start]').forEach(function (el) {
    el.textContent = dateStr;
  });

  /* ── Countdown ──────────────────────────────────────────── */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var cells = {
      d: cd.querySelector('[data-cd-d]'), h: cd.querySelector('[data-cd-h]'),
      m: cd.querySelector('[data-cd-m]'), s: cd.querySelector('[data-cd-s]')
    };
    if (cells.d && cells.h && cells.m && cells.s) {
      var tick = function () {
        var diff = startDate.getTime() - Date.now();
        if (diff < 0) diff = 0;
        var s = Math.floor(diff / 1000);
        cells.d.textContent = Math.floor(s / 86400);
        cells.h.textContent = Math.floor((s % 86400) / 3600);
        cells.m.textContent = Math.floor((s % 3600) / 60);
        cells.s.textContent = s % 60;
      };
      tick(); setInterval(tick, 1000);
    }
  }

  /* ── Hamburger ──────────────────────────────────────────── */
  var burger = document.querySelector('.hamburger');
  var drawer = document.querySelector('.nav-drawer');
  if (burger && drawer) {
    // Cap the drawer to the space between its top and the viewport bottom so it always
    // fits on screen and scrolls internally (the inner padding clears the sticky CTA).
    function sizeDrawer() {
      var top = drawer.getBoundingClientRect().top;
      drawer.style.maxHeight = Math.max(180, window.innerHeight - top - 6) + 'px';
    }
    function closeDrawer() {
      drawer.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
    }
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('nav-open', open);
      if (open) sizeDrawer();
    });
    drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeDrawer); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });
    window.addEventListener('resize', function () { if (drawer.classList.contains('open')) sizeDrawer(); });
  }

  /* ── Accordion ──────────────────────────────────────────── */
  document.querySelectorAll('.acc-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.parentElement.classList.toggle('open');
    });
  });

  /* ── Reveal on scroll ───────────────────────────────────── */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0, rootMargin: "0px 0px 15% 0px" });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
  }

  /* ── Lead form submit (AJAX) ────────────────────────────── */
  document.querySelectorAll('form.leadform').forEach(function (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('.btn-submit');
      var err = form.querySelector('.form-error');
      btn.disabled = true;
      btn.textContent = LANG === 'es' ? 'ENVIANDO…' : 'SENDING…';
      err.style.display = 'none';

      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      }).then(function (r) {
        if (!r.ok) throw new Error('bad status');
        form.style.display = 'none';
        var ok = form.parentElement.querySelector('.form-success');
        if (ok) ok.classList.add('show');
        // GTM-based tracking: push to dataLayer (GTM tags handle GA4/Ads/Meta).
        try { (window.dataLayer = window.dataLayer || []).push({ event: 'generate_lead', source: 'native_form' }); } catch (e) {}
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = LANG === 'es' ? 'ENVIAR' : 'SUBMIT';
        err.style.display = 'block';
      });
    });
  });

  /* ── Chat-style bubble → scroll to form ─────────────────── */
  var bubble = document.querySelector('.bubble');
  var tip = document.querySelector('.bubble-tip');
  if (bubble) {
    setTimeout(function () { if (tip) tip.classList.add('show'); }, 6000);
    bubble.addEventListener('click', function () {
      if (tip) tip.classList.remove('show');
      var f = document.querySelector('.formcard');
      if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'center' });
        var first = f.querySelector('input'); if (first) setTimeout(function(){ first.focus(); }, 600); }
    });
    var x = document.querySelector('.bubble-tip .tip-x');
    if (x) x.addEventListener('click', function () { tip.classList.remove('show'); });
  }

  /* ── Exit intent (desktop, once per session) ────────────── */
  var exit = document.querySelector('.exit');
  if (exit && !sessionStorage.getItem('abiExitShown') && window.matchMedia('(pointer:fine)').matches) {
    document.addEventListener('mouseout', function handler(e) {
      if (e.clientY <= 0 && !e.relatedTarget) {
        exit.classList.add('show');
        sessionStorage.setItem('abiExitShown', '1');
        document.removeEventListener('mouseout', handler);
      }
    });
    exit.addEventListener('click', function (e) {
      if (e.target === exit || e.target.closest('.exit-x')) exit.classList.remove('show');
    });
    var go = exit.querySelector('[data-exit-cta]');
    if (go) go.addEventListener('click', function () {
      exit.classList.remove('show');
      var f = document.querySelector('.formcard');
      if (f) f.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
})();

/* ── Theme switcher (synced with interior pages) ── */
(function () {
  var KEY = 'abi-theme';
  function apply(t) {
    if (!t || t === 'blue' || t === 'midnight-default') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', t);
    document.querySelectorAll('.tdot').forEach(function (d) {
      d.setAttribute('aria-pressed', d.getAttribute('data-set-theme') === (t || 'blue') ? 'true' : 'false');
    });
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  apply(saved);
  function themeSweep(d) {
    try {
      var r = d.getBoundingClientRect();
      var sw = document.createElement('div');
      sw.className = 'theme-sweep';
      sw.style.setProperty('--sx', (r.left + r.width / 2) + 'px');
      document.body.appendChild(sw);
      setTimeout(function () { sw.remove(); }, 640);
    } catch (e) {}
  }
  document.querySelectorAll('.tdot').forEach(function (d) {
    d.addEventListener('click', function () {
      var t = d.getAttribute('data-set-theme');
      themeSweep(d);
      apply(t);
      try { localStorage.setItem(KEY, t); localStorage.setItem('abi-theme-user', '1'); } catch (e) {}
    });
  });
})();

/* ── YouTube click-to-play facades ── */
document.querySelectorAll('.yt').forEach(function (f) {
  f.addEventListener('click', function () {
    var id = f.getAttribute('data-yt');
    var ifr = document.createElement('iframe');
    ifr.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
    ifr.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
    ifr.allowFullscreen = true;
    f.innerHTML = ''; f.appendChild(ifr);
  }, { once: true });
});

/* ── Upcoming start dates (first Monday of each month) ── */
(function () {
  var host = document.querySelector('[data-start-dates]');
  if (!host) return;
  var lang = document.documentElement.lang === 'es' ? 'es-US' : 'en-US';
  var fmt = new Intl.DateTimeFormat(lang, { weekday: 'short', month: 'short', day: 'numeric' });
  var out = [], d = new Date(), m = d.getMonth(), y = d.getFullYear();
  while (out.length < 6) {
    var c = new Date(y, m, 1);
    while (c.getDay() !== 1) c.setDate(c.getDate() + 1);
    if (c > new Date()) out.push(c);
    m++; if (m > 11) { m = 0; y++; }
  }
  host.innerHTML = out.map(function (c, i) {
    var t = fmt.format(c);
    return '<span class="date-pill' + (i === 0 ? ' next' : '') + '">' + t + (i === 0 ? ' ★' : '') + '</span>';
  }).join('');
})();

/* ── Count-up stats on scroll ── */
(function () {
  var els = document.querySelectorAll('[data-count]');
  if (!els.length || !('IntersectionObserver' in window)) return;
  // Respect reduced-motion: leave the real (baked-in) values, skip the count-up.
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      var el = e.target, target = parseInt(el.getAttribute('data-count'), 10);
      var suffix = el.getAttribute('data-suffix') || '';
      var t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / 1400, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString() + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold: 0.4 });
  els.forEach(function (el) { io.observe(el); });
})();
