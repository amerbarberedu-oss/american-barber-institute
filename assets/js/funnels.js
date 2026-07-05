/* =========================================================================
   ABI Landing Funnels — fresh JS
   ─────────────────────────────────────────────────────────────────────────
   Self-contained, zero-dependency. Handles:
     • Countdown timer (live, rolls forward indefinitely)
     • Reveal-on-scroll
     • Reel video controls (center play/pause + corner mute + exclusive playback)
     • Off-screen pause via IntersectionObserver
     • Form submission via Formspree (graceful fallback if endpoint missing)
   ========================================================================= */
(function () {
  'use strict';

  /* ───── helpers ───── */
  var qs  = function (sel, root) { return (root || document).querySelector(sel); };
  var qsa = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var on  = function (el, ev, fn, opts) { el.addEventListener(ev, fn, opts || false); };

  /* Flag the first real user interaction so we can unmute videos (autoplay-policy gate) */
  var userInteracted = false;
  ['click','keydown','touchstart','pointerdown'].forEach(function (e) {
    document.addEventListener(e, function once () { userInteracted = true; }, { once: true, passive: true, capture: true });
  });

  /* ───── COUNTDOWN ─────────────────────────────────────────────────────
     Each .lf-cd element carries data-target="YYYY-MM-DD" for the date that
     starts everything. We additionally roll the target forward to the
     first Monday of the NEXT month if today is past it — that's how the
     "5-year" promise is met: pure date math, never hard-coded.
  */
  function firstMondayOfNextMonth(after) {
    var y = after.getFullYear(), m = after.getMonth() + 1;
    if (m > 11) { m = 0; y += 1; }
    var d = new Date(y, m, 1);
    while (d.getDay() !== 1) d.setDate(d.getDate() + 1);
    return d;
  }
  function resolveTarget(el) {
    var attr = el.getAttribute('data-target');
    var t = attr ? new Date(attr + 'T00:00:00') : null;
    var now = new Date();
    if (!t || isNaN(+t) || t <= now) t = firstMondayOfNextMonth(now);
    return t;
  }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function startCountdown(el) {
    var target = resolveTarget(el);
    var dEl = qs('[data-cd-d]', el), hEl = qs('[data-cd-h]', el);
    var mEl = qs('[data-cd-m]', el), sEl = qs('[data-cd-s]', el);
    var dateEl = qs('.lf-cd__date', el);
    if (dateEl && !dateEl.textContent.trim()) {
      var lang = document.documentElement.lang || 'en';
      try {
        dateEl.textContent = target.toLocaleDateString(lang === 'es' ? 'es-ES' : 'en-US', {
          weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
        });
      } catch (e) {}
    }
    function tick() {
      var diff = Math.max(0, target - new Date());
      var d = Math.floor(diff / 86400000);
      var h = Math.floor((diff % 86400000) / 3600000);
      var m = Math.floor((diff % 3600000) / 60000);
      var s = Math.floor((diff % 60000) / 1000);
      if (dEl) dEl.textContent = pad(d);
      if (hEl) hEl.textContent = pad(h);
      if (mEl) mEl.textContent = pad(m);
      if (sEl) sEl.textContent = pad(s);
      if (diff <= 0) {
        /* roll target forward */
        target = firstMondayOfNextMonth(new Date());
        if (dateEl) {
          var lng = document.documentElement.lang || 'en';
          try {
            dateEl.textContent = target.toLocaleDateString(lng === 'es' ? 'es-ES' : 'en-US', {
              weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
            });
          } catch (e) {}
        }
      }
    }
    tick();
    setInterval(tick, 1000);
  }

  /* ───── REVEAL-ON-SCROLL ───────────────────────────────────────────── */
  function initReveal() {
    var els = qsa('.lf-rv');
    if (!els.length) return;
    if (typeof IntersectionObserver === 'undefined') {
      els.forEach(function (e) { e.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ───── REEL VIDEO CONTROLS ────────────────────────────────────────── */
  var SVG_PLAY  = '<svg viewBox="0 0 24 24" class="lf-reel__icon-play" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
  var SVG_PAUSE = '<svg viewBox="0 0 24 24" class="lf-reel__icon-pause" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
  var SVG_VOL   = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z"/></svg>';
  var SVG_MUTE  = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.17v2.06a8.99 8.99 0 0 0 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>';

  function initReel(media) {
    if (media.dataset.lfInit) return;
    media.dataset.lfInit = '1';
    var video = qs('video', media);
    if (!video) return;
    video.muted = true; video.setAttribute('muted', '');
    video.setAttribute('playsinline', ''); video.setAttribute('webkit-playsinline', '');
    if (!video.hasAttribute('loop')) video.setAttribute('loop', '');

    /* center play/pause button */
    var playBtn = qs('.lf-reel__play', media);
    if (!playBtn) {
      playBtn = document.createElement('button');
      playBtn.className = 'lf-reel__play';
      playBtn.type = 'button';
      playBtn.setAttribute('aria-label', 'Play video');
      playBtn.innerHTML = SVG_PLAY + SVG_PAUSE;
      media.appendChild(playBtn);
    }
    /* corner mute toggle */
    var muteBtn = document.createElement('button');
    muteBtn.className = 'lf-mute';
    muteBtn.type = 'button';
    muteBtn.setAttribute('aria-label', 'Unmute');
    muteBtn.innerHTML = SVG_MUTE;
    media.appendChild(muteBtn);

    function syncMute() {
      var muted = video.muted || video.volume === 0;
      muteBtn.innerHTML = muted ? SVG_MUTE : SVG_VOL;
      muteBtn.setAttribute('aria-label', muted ? 'Unmute' : 'Mute');
    }
    function syncPlay() {
      var playing = !video.paused && !video.ended;
      media.classList.toggle('is-playing', playing);
      playBtn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
    }

    function togglePlay() {
      if (video.paused) {
        if (userInteracted) { video.muted = false; video.volume = 1; }
        video.play().catch(function () {
          /* audio still blocked → fall back to muted playback */
          video.muted = true;
          video.play().catch(function () {});
        });
      } else {
        video.pause();
      }
      syncMute(); syncPlay();
    }

    on(playBtn, 'click', function (e) { e.preventDefault(); e.stopPropagation(); togglePlay(); });
    on(video, 'click', function (e) {
      if (e.target === playBtn || playBtn.contains(e.target)) return;
      if (e.target === muteBtn || muteBtn.contains(e.target)) return;
      togglePlay();
    });
    on(muteBtn, 'click', function (e) {
      e.preventDefault(); e.stopPropagation();
      video.muted = !video.muted;
      if (!video.muted) { video.volume = 1; if (video.paused) video.play().catch(function () {}); }
      syncMute();
    });

    /* exclusive playback — playing one reel pauses any others */
    on(video, 'play', function () {
      qsa('.lf-reel__media video').forEach(function (other) {
        if (other !== video && !other.paused) other.pause();
      });
      syncMute(); syncPlay();
    });
    on(video, 'pause', function () { syncMute(); syncPlay(); });
    on(video, 'volumechange', syncMute);

    /* auto-pause when scrolled out of view */
    if (typeof IntersectionObserver !== 'undefined') {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (!en.isIntersecting && !video.paused) video.pause(); });
      }, { threshold: 0 }).observe(media);
    }
    syncMute(); syncPlay();
  }

  /* ───── INIT ───── */
  function init() {
    qsa('.lf-cd[data-target]').forEach(startCountdown);
    qsa('.lf-reel__media').forEach(initReel);
    initReveal();

    /* showcase clip — click toggles play/pause; hover (desktop) starts play */
    qsa('.lf-clip').forEach(function (host) {
      var v = qs('video', host);
      var pb = qs('.lf-clip__play', host);
      if (!v) return;
      v.muted = true; v.loop = true;
      function syncPlaying() { host.classList.toggle('is-playing', !v.paused && !v.ended); }
      function toggle() {
        if (v.paused) v.play().catch(function () {});
        else v.pause();
      }
      if (pb) on(pb, 'click', function (e) { e.preventDefault(); e.stopPropagation(); toggle(); });
      on(host, 'click', function (e) {
        if (pb && (e.target === pb || pb.contains(e.target))) return;
        toggle();
      });
      /* desktop hover-preview */
      on(host, 'mouseenter', function () { if (window.matchMedia('(hover:hover)').matches) v.play().catch(function () {}); });
      on(host, 'mouseleave', function () { if (window.matchMedia('(hover:hover)').matches) v.pause(); });
      on(v, 'play',  syncPlaying);
      on(v, 'pause', syncPlaying);
      /* autoplay muted when in view, pause when off-screen (so clips visibly play) */
      if (typeof IntersectionObserver !== 'undefined') {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) { v.muted = true; v.play().catch(function () {}); }
            else if (!v.paused) { v.pause(); }
          });
        }, { threshold: 0.35 }).observe(host);
      } else {
        v.muted = true; v.play().catch(function () {});
      }
    });

    /* 3D micro-tilt on cards — perspective-based, vanilla, mouse-only */
    var TILT_TARGETS = '.lf-pill, .lf-plan, .lf-earn-card, .lf-review, .lf-step';
    qsa(TILT_TARGETS).forEach(function (el) {
      el.classList.add('lf-tilt');
      on(el, 'mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width  - 0.5;
        var y = (e.clientY - r.top)  / r.height - 0.5;
        el.style.setProperty('--rx', (x * 7).toFixed(2) + 'deg');
        el.style.setProperty('--ry', (-y * 7).toFixed(2) + 'deg');
      });
      on(el, 'mouseleave', function () {
        el.style.setProperty('--rx', '0deg');
        el.style.setProperty('--ry', '0deg');
      });
    });

    /* Animated stat counters — count up when scrolled into view */
    function animateNumber(el) {
      var raw = el.textContent.trim();
      // Parse "10,000+" or "$45k – $60k" type values — just animate the first integer found.
      var m = raw.match(/(\$?)([\d,]+)(.*)/);
      if (!m) return;
      var prefix = m[1] || '';
      var target = parseInt(m[2].replace(/,/g, ''), 10);
      var suffix = m[3] || '';
      if (!target) return;
      var dur = 1200, t0 = null;
      function tick(ts) {
        if (!t0) t0 = ts;
        var k = Math.min(1, (ts - t0) / dur);
        var eased = 1 - Math.pow(1 - k, 3);    // ease-out cubic
        var n = Math.floor(target * eased);
        el.textContent = prefix + n.toLocaleString() + suffix;
        if (k < 1) requestAnimationFrame(tick); else el.textContent = raw;
      }
      requestAnimationFrame(tick);
    }
    if (typeof IntersectionObserver !== 'undefined') {
      var statIo = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add('is-in');
            qsa('.lf-stat__n', en.target).forEach(animateNumber);
            statIo.unobserve(en.target);
          }
        });
      }, { threshold: 0.4 });
      qsa('.lf-stat').forEach(function (el) { statIo.observe(el); });
    }

    /* Stagger reveal — set --rv-delay per item index inside each section */
    qsa('.lf-section, .lf-hero, .lf-pills, .lf-footer').forEach(function (sec) {
      var items = qsa('.lf-rv', sec);
      items.forEach(function (el, i) {
        el.style.setProperty('--rv-delay', (i * 0.07).toFixed(2) + 's');
      });
    });

    /* simple form handler (Formspree) — graceful no-op if action missing */
    qsa('form.lf-form').forEach(function (form) {
      on(form, 'submit', function (e) {
        if (!form.action || form.action.indexOf('formspree.io') < 0) return;
        e.preventDefault();
        var btn = qs('button[type="submit"]', form);
        if (btn) { btn.disabled = true; btn.dataset.orig = btn.textContent; btn.textContent = '…'; }
        fetch(form.action, {
          method: 'POST', body: new FormData(form),
          headers: { Accept: 'application/json' }
        }).then(function (r) {
          if (r.ok) {
            form.innerHTML = '<div class="lf-form__h">' +
              (document.documentElement.lang === 'es'
                ? '¡Gracias! Te contactaremos pronto.'
                : 'Thanks! We\'ll be in touch shortly.') + '</div>';
          } else {
            if (btn) { btn.disabled = false; btn.textContent = btn.dataset.orig || 'Submit'; }
            alert(document.documentElement.lang === 'es'
              ? 'No se pudo enviar — vuelve a intentarlo o llama directamente.'
              : 'Could not submit — please try again or call us directly.');
          }
        }).catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.orig || 'Submit'; }
        });
      });
    });
  }

  // ── Play button: hide instantly when a video starts playing ─────────
  // Targets:
  //   .lf-clip          (showcase + YouTube tiles) → button.lf-clip__play
  //   .lf-reel__media   (student-voices reels)     → button.lf-reel__play
  function wirePlayHide() {
    qsa('.lf-clip video, .lf-reel__media video').forEach(function (v) {
      on(v, 'play', function () {
        var wrap = v.closest('.lf-clip') || v.closest('.lf-reel__media');
        if (wrap) wrap.classList.add('is-playing');
      });
      on(v, 'pause', function () {
        if (v.ended || v.currentTime === 0) {
          var wrap = v.closest('.lf-clip') || v.closest('.lf-reel__media');
          if (wrap) wrap.classList.remove('is-playing');
        }
      });
      on(v, 'ended', function () {
        var wrap = v.closest('.lf-clip') || v.closest('.lf-reel__media');
        if (wrap) wrap.classList.remove('is-playing');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { init(); wirePlayHide(); });
  } else {
    init();
    wirePlayHide();
  }
})();
