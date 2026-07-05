/* ABI — Premium interactions upgrade layer (vanilla, no deps, defer-loaded)
 *
 * Self-contained, namespaced IIFE that ADDS four new behaviors on top of the
 * existing site JS (effects.js / landing.js). It deliberately does NOT touch or
 * re-bind anything those files already own:
 *
 *   - Theme switcher (.tdot / data-theme)         -> owned by landing.js + inline head script
 *   - EN/ES language toggle                       -> owned by markup / existing pages
 *   - Live class countdown ([data-countdown])     -> owned by landing.js / main.js
 *   - Animated count-up stats ([data-count])      -> owned by effects.js / landing.js
 *   - Mobile nav drawer + sticky CTA (.hamburger) -> owned by landing.js
 *   - Generic scroll reveals (.reveal / .rv / .in-view) -> owned by effects.js / landing.js
 *
 * To avoid clobbering the existing reveal systems, this layer uses its OWN, new
 * hooks only: video[data-src], .abi-tilt, [data-reveal] (+ .is-in), .abi-deco.
 * None of these selectors exist in the current markup, so there is zero overlap.
 *
 * Everything is guarded: each feature no-ops gracefully when its elements are
 * absent, and every motion-bearing feature respects prefers-reduced-motion.
 */
(function () {
  'use strict';

  /* ---------- Shared environment probes (evaluated once) ---------- */
  function mq(query) {
    // matchMedia can be missing in very old engines; degrade to "false".
    return (window.matchMedia && window.matchMedia(query)) || { matches: false, addListener: function () {} };
  }

  var REDUCED = mq('(prefers-reduced-motion: reduce)').matches;
  var COARSE = mq('(pointer: coarse)').matches;          // touch-primary devices
  var HAS_IO = 'IntersectionObserver' in window;

  // Pointer-driven effects (tilt, deco parallax) are desktop-only:
  // not touch, not narrow, not reduced-motion.
  function pointerEffectsAllowed() {
    return !REDUCED && !COARSE && window.innerWidth >= 768;
  }

  /* =====================================================================
   * 1) LAZY AUTOPLAY VIDEO  —  video[data-src]
   *    Loads the real source only when the clip nears the viewport, then
   *    plays muted/looped; pauses when it scrolls away to save CPU.
   *    Under reduced-motion we still load the src (so a poster/first frame
   *    shows) but never autoplay.
   *    Drives: .abi-clip__video, .abi-brandband__video
   * =================================================================== */
  function initLazyVideo() {
    var vids = [].slice.call(document.querySelectorAll('video[data-src]'));
    if (!vids.length) return;

    // Ensure the attributes that make inline autoplay legal are present.
    function prime(video) {
      if (!video.hasAttribute('muted')) { video.muted = true; video.setAttribute('muted', ''); }
      if (!video.hasAttribute('playsinline')) video.setAttribute('playsinline', '');
      if (!video.hasAttribute('loop')) video.setAttribute('loop', '');
    }

    function load(video) {
      if (!video.dataset.src) return;
      if (video.getAttribute('src') !== video.dataset.src) {
        video.src = video.dataset.src;
      }
    }

    function play(video) {
      // .play() returns a promise that can reject (autoplay policy, no gesture).
      // Swallow the rejection — there is nothing useful to do about it.
      var p = video.play();
      if (p && typeof p.catch === 'function') p.catch(function () {});
    }

    // No IntersectionObserver: load everything up front, autoplay if allowed.
    if (!HAS_IO) {
      vids.forEach(function (video) {
        prime(video);
        load(video);
        if (!REDUCED) play(video);
      });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var video = e.target;
        if (e.isIntersecting) {
          prime(video);
          load(video);
          if (!REDUCED) play(video);
        } else if (!REDUCED && !video.paused) {
          // Out of view: pause to free the decoder. (Skip when reduced-motion
          // because we never started playback in the first place.)
          try { video.pause(); } catch (err) {}
        }
      });
    }, { rootMargin: '200px 0px', threshold: 0.01 });

    vids.forEach(function (video) { io.observe(video); });
  }

  /* =====================================================================
   * 2) POINTER 3D TILT  —  .abi-tilt
   *    Writes clamped rotateX/rotateY into CSS custom properties
   *    (--abi-rx / --abi-ry) on pointermove, rAF-throttled. Resets on leave.
   *    Disabled on touch, narrow viewports, and reduced-motion. The CSS is
   *    expected to consume the vars, e.g.:
   *      .abi-tilt { transform: perspective(900px)
   *                  rotateX(var(--abi-rx,0)) rotateY(var(--abi-ry,0)); }
   * =================================================================== */
  function initTilt() {
    if (!pointerEffectsAllowed()) return;

    var cards = [].slice.call(document.querySelectorAll('.abi-tilt'));
    if (!cards.length) return;

    var MAX_DEG = 8; // clamp tilt to a tasteful ±8deg

    cards.forEach(function (card) {
      var raf = null;
      var pendingEvent = null;

      function apply() {
        raf = null;
        var e = pendingEvent;
        if (!e) return;
        var r = card.getBoundingClientRect();
        if (!r.width || !r.height) return;
        // Cursor position relative to card center, normalized to -0.5..0.5.
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        // Tilt "toward" the cursor: vertical pos -> rotateX, horizontal -> rotateY.
        var rx = (-py * 2 * MAX_DEG).toFixed(2);
        var ry = (px * 2 * MAX_DEG).toFixed(2);
        card.style.setProperty('--abi-rx', rx + 'deg');
        card.style.setProperty('--abi-ry', ry + 'deg');
      }

      card.addEventListener('pointermove', function (e) {
        // Ignore touch/pen pointers — keep this mouse-only even on hybrids.
        if (e.pointerType && e.pointerType !== 'mouse') return;
        pendingEvent = e;
        if (raf === null) raf = requestAnimationFrame(apply);
      });

      card.addEventListener('pointerleave', function () {
        if (raf !== null) { cancelAnimationFrame(raf); raf = null; }
        pendingEvent = null;
        card.style.setProperty('--abi-rx', '0deg');
        card.style.setProperty('--abi-ry', '0deg');
      });
    });
  }

  /* =====================================================================
   * 3) SCROLL REVEAL  —  [data-reveal]  (adds .is-in)
   *    Adds .is-in once when an element enters view, then unobserves it.
   *    Under reduced-motion, mark everything visible immediately.
   * =================================================================== */
  function initReveal() {
    var els = [].slice.call(document.querySelectorAll('[data-reveal]'));
    if (!els.length) return;

    if (REDUCED || !HAS_IO) {
      // No animation — just make them visible.
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px 15% 0px' });

    els.forEach(function (el) { io.observe(el); });
  }

  /* =====================================================================
   * 4) DECO PARALLAX (subtle, optional)  —  .abi-deco
   *    On document pointermove, writes a small offset (-12px..12px) into
   *    --abi-px / --abi-py on every .abi-deco element for gentle parallax.
   *    rAF-throttled. Pointer-effects gating applies (no touch / no narrow /
   *    no reduced-motion).
   * =================================================================== */
  function initDecoParallax() {
    if (!pointerEffectsAllowed()) return;

    var deco = [].slice.call(document.querySelectorAll('.abi-deco'));
    if (!deco.length) return;

    var RANGE = 12; // px of travel in each direction
    var raf = null;
    var pendingEvent = null;

    function apply() {
      raf = null;
      var e = pendingEvent;
      if (!e) return;
      // Cursor position across the viewport, normalized to -0.5..0.5.
      var nx = (e.clientX / window.innerWidth) - 0.5;
      var ny = (e.clientY / window.innerHeight) - 0.5;
      var px = (nx * 2 * RANGE).toFixed(1) + 'px';
      var py = (ny * 2 * RANGE).toFixed(1) + 'px';
      for (var i = 0; i < deco.length; i++) {
        deco[i].style.setProperty('--abi-px', px);
        deco[i].style.setProperty('--abi-py', py);
      }
    }

    document.addEventListener('pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      pendingEvent = e;
      if (raf === null) raf = requestAnimationFrame(apply);
    }, { passive: true });
  }

  /* ---------- Boot ---------- */
  function setup() {
    // Each guard is internal, so a failure in one feature can't block the rest.
    try { initLazyVideo(); } catch (e) {}
    try { initTilt(); } catch (e) {}
    try { initReveal(); } catch (e) {}
    try { initDecoParallax(); } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup, { once: true });
  } else {
    setup();
  }

  /* ---------- Optional public namespace (the only intentional global) ---------- */
  window.ABIUpgrade = {
    version: '1.0.0',
    init: setup,
    initLazyVideo: initLazyVideo,
    initTilt: initTilt,
    initReveal: initReveal,
    initDecoParallax: initDecoParallax
  };
})();
