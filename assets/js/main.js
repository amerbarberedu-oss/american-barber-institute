/* American Barber Institute — site JS (vanilla, no deps) */
(function () {
  'use strict';

  document.documentElement.classList.add('js');

  /* ---------- Theme init (clicks handled by landing.js .tdot) ---------- */
  var THEMES = ['midnight', 'classic', 'emerald', 'noir'];
  var saved = null;
  try { if (localStorage.getItem('abi-theme-user')) saved = localStorage.getItem('abi-theme'); } catch (e) {}
  if (saved && THEMES.indexOf(saved) > -1) document.documentElement.setAttribute('data-theme', saved);
  else if (saved !== null || true) { if (!saved) document.documentElement.removeAttribute('data-theme'); }

  /* Mobile nav is handled by landing.js (.hamburger/.nav-drawer); the old
     .menu-btn/.nav markup no longer exists, so no wiring is needed here. */

  /* ---------- Next start date: first Monday of next month (always current) ---------- */
  function firstMonday(year, month) {
    var d = new Date(year, month, 1);
    var day = d.getDay();
    var offset = (8 - day) % 7; // days until Monday
    d.setDate(1 + offset);
    return d;
  }
  function nextStartDate(now) {
    // first Monday of current month if still ahead, else next month
    var fm = firstMonday(now.getFullYear(), now.getMonth());
    if (fm <= now) fm = firstMonday(now.getFullYear(), now.getMonth() + 1);
    return fm;
  }
  var now = new Date();
  var start = nextStartDate(now);
  var fmt = { weekday: 'short', month: 'long', day: 'numeric', year: 'numeric' };
  document.querySelectorAll('[data-start-date]').forEach(function (el) {
    el.textContent = start.toLocaleDateString(document.documentElement.lang === 'es' ? 'es-US' : 'en-US', fmt);
  });

  /* ---------- Countdown ---------- */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var units = {
      d: cd.querySelector('[data-d]'), h: cd.querySelector('[data-h]'),
      m: cd.querySelector('[data-m]'), s: cd.querySelector('[data-s]')
    };
    var classStart = new Date(start); classStart.setHours(8, 0, 0, 0);
    function tick() {
      var diff = Math.max(0, classStart - new Date());
      var s = Math.floor(diff / 1000);
      if (units.d) units.d.textContent = Math.floor(s / 86400);
      if (units.h) units.h.textContent = Math.floor((s % 86400) / 3600);
      if (units.m) units.m.textContent = Math.floor((s % 3600) / 60);
      if (units.s) units.s.textContent = s % 60;
    }
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- Reveal on scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0, rootMargin: "0px 0px 15% 0px" });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Stat count-up ---------- */
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var dur = 1400, t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); io2.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { io2.observe(el); });
  }

  /* ---------- Lite YouTube embeds ---------- */
  document.querySelectorAll('.yt[data-yt]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = btn.getAttribute('aria-label') || 'Video';
      iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      btn.innerHTML = '';
      btn.appendChild(iframe);
    }, { once: true });
  });

  /* ---------- Gallery lightbox ---------- */
  var galLinks = Array.prototype.slice.call(document.querySelectorAll('.gallery-grid a'));
  if (galLinks.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML = '<img alt="Enlarged gallery image"><button class="lb-close" aria-label="Close">✕</button>' +
      '<button class="lb-prev" aria-label="Previous">‹</button><button class="lb-next" aria-label="Next">›</button>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), idx = 0;
    function show(i) {
      idx = (i + galLinks.length) % galLinks.length;
      lbImg.src = galLinks[idx].getAttribute('href');
      lbImg.alt = (galLinks[idx].querySelector('img') && galLinks[idx].querySelector('img').alt) || 'Enlarged gallery image';
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function hide() { lb.classList.remove('open'); document.body.style.overflow = ''; }
    galLinks.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); show(i); });
    });
    lb.querySelector('.lb-close').addEventListener('click', hide);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) hide(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') hide();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---------- Forms (mailto fallback handler) ---------- */
  document.querySelectorAll('form[data-mailform]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var lines = [];
      data.forEach(function (v, k) { if (v) lines.push(k.replace(/_/g, ' ') + ': ' + v); });
      var subject = form.getAttribute('data-subject') || 'Website inquiry';
      window.location.href = 'mailto:admission@abi.edu?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(lines.join('\n'));
      var ok = form.querySelector('.form-ok');
      if (ok) ok.hidden = false;
    });
  });

  /* ---------- Current nav highlight ---------- */
  var path = location.pathname.replace(/index\.html$/, '');
  document.querySelectorAll('.nav a[href]').forEach(function (a) {
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#') return;
    var resolved = new URL(href, location.href).pathname.replace(/index\.html$/, '');
    if (resolved === path && resolved !== '/') a.setAttribute('aria-current', 'page');
  });
})();
