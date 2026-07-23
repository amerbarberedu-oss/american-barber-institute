/* American Barber Institute — universal video sound + hover controls.
 * Adds a corner mute/unmute button to every <video> on the page,
 * plays + unmutes on hover (within browser autoplay limits),
 * re-mutes on mouseleave, click-to-toggle on touch devices. */
(function () {
  "use strict";
  if (window.__abiVideoSound) return;
  window.__abiVideoSound = true;

  var SVG_VOL  = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3.23v2.06a7 7 0 0 1 0 13.42v2.06a9 9 0 0 0 0-17.54z"/></svg>';
  var SVG_MUTE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zM19 12c0 .94-.2 1.82-.54 2.64l1.51 1.51A8.93 8.93 0 0 0 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.17v2.06a8.99 8.99 0 0 0 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>';

  /* Detect first real user interaction — required by browsers to allow audio */
  function flagInteracted() { window.__abiUserInteracted = true; }
  ["click", "keydown", "touchstart", "pointerdown"].forEach(function (ev) {
    document.addEventListener(ev, flagInteracted, { once: true, passive: true, capture: true });
  });

  function init(v) {
    if (v.dataset.vsInit) return;
    v.dataset.vsInit = "1";

    /* Find a stable wrapper for the button — closest positioned ancestor,
     * or the immediate parent (with position:relative forced). */
    var host = v.parentElement;
    if (!host) return;
    if (getComputedStyle(host).position === "static") host.style.position = "relative";

    /* Make sure attributes that allow inline autoplay are set */
    v.muted = true;
    v.setAttribute("muted", "");
    v.setAttribute("playsinline", "");
    if (!v.hasAttribute("loop")) v.setAttribute("loop", "");

    /* v16.6 — Student Voices testimonial videos use a dedicated click-to-play
     * pattern (centre play/pause + corner mute) instead of hover-autoplay. They
     * carry audio so they shouldn't ambush visitors when the cursor sweeps past. */
    var isReel = host.matches("[data-abi-reel]") || v.classList.contains("abi-reel__video");

    /* Sound button (corner) — added to every video */
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "vs-btn vs-muted";
    btn.setAttribute("aria-label", "Unmute video");
    btn.innerHTML = SVG_MUTE;
    host.appendChild(btn);

    function syncBtn() {
      var muted = v.muted || v.volume === 0;
      btn.classList.toggle("vs-muted", muted);
      btn.innerHTML = muted ? SVG_MUTE : SVG_VOL;
      btn.setAttribute("aria-label", muted ? "Unmute video" : "Mute video");
    }
    /* Centre play/pause button — exists in DOM for reel videos. Reflect state. */
    var playBtn = isReel ? host.querySelector(".abi-reel__play") : null;
    function syncPlay() {
      if (!playBtn) return;
      var playing = !v.paused && !v.ended;
      host.classList.toggle("is-playing", playing);
      playBtn.setAttribute("aria-label", playing ? "Pause video" : "Play video");
    }

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      v.muted = !v.muted;
      if (!v.muted) {
        v.volume = 1;
        v.play().catch(function () {});
      }
      syncBtn();
    });

    if (isReel) {
      /* Reel videos: click toggles PLAY/PAUSE; first play unmutes if the user
       * has interacted with the page (autoplay-with-sound policy). */
      function togglePlay() {
        if (v.paused) {
          if (window.__abiUserInteracted) { v.muted = false; v.volume = 1; }
          v.play().catch(function () {
            /* If audio is still blocked, fall back to muted playback */
            v.muted = true;
            v.play().catch(function () {});
          });
        } else {
          v.pause();
        }
        syncBtn();
        syncPlay();
      }
      if (playBtn) playBtn.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation(); togglePlay();
      });
      v.addEventListener("click", function (e) {
        if (e.target === btn || btn.contains(e.target)) return;
        if (playBtn && (e.target === playBtn || playBtn.contains(e.target))) return;
        togglePlay();
      });
      /* Pause when the reel scrolls fully out of view so audio doesn't trail
       * the visitor down the page. */
      if (typeof IntersectionObserver !== "undefined") {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (en) { if (!en.isIntersecting && !v.paused) v.pause(); });
        }, { threshold: 0 }).observe(host);
      }
    } else {
      /* All other site videos keep the original hover-autoplay UX.
       * v17 fix: ambient clips are ALSO autoplayed muted by an
       * IntersectionObserver (effects.js/upgrade.js). That observer only
       * fires on intersection CHANGES, so if mouseleave paused a clip that
       * was still in view, nothing ever restarted it — one cursor sweep
       * froze every ambient video until the user scrolled it out of view
       * and back. On leave, re-mute and keep a still-visible clip playing;
       * only pause when it has actually left the viewport (matching what
       * the observers would do anyway). */
      function onEnter() {
        if (window.__abiUserInteracted) { v.muted = false; v.volume = 1; }
        v.play().then(syncBtn).catch(function () {
          v.muted = true;
          v.play().then(syncBtn).catch(function () {});
        });
      }
      function onLeave() {
        v.muted = true;
        var r = v.getBoundingClientRect();
        var visible = r.top < window.innerHeight && r.bottom > 0 &&
                      r.left < window.innerWidth && r.right > 0;
        if (visible) {
          v.play().catch(function () {});
        } else {
          v.pause();
        }
        syncBtn();
      }
      host.addEventListener("mouseenter", onEnter);
      host.addEventListener("mouseleave", onLeave);
      v.addEventListener("click", function (e) {
        if (e.target === btn || btn.contains(e.target)) return;
        if (v.paused) {
          if (window.__abiUserInteracted) v.muted = false;
          v.play().catch(function () {});
        } else {
          v.muted = !v.muted;
        }
        syncBtn();
      });
    }

    v.addEventListener("volumechange", syncBtn);
    v.addEventListener("play", function () {
      /* v16.7 — exclusive playback for Student Voices: starting one testimonial
       * pauses any other reel that's already playing. Like Instagram Reels —
       * only one talks at a time. */
      if (isReel) {
        document.querySelectorAll("video.abi-reel__video").forEach(function (other) {
          if (other !== v && !other.paused) other.pause();
        });
      }
      syncBtn(); syncPlay();
    });
    v.addEventListener("pause", function () { syncBtn(); syncPlay(); });

    syncBtn();
    syncPlay();
  }

  function scan() {
    document.querySelectorAll("video").forEach(init);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
  /* Catch lazy-loaded clips and gallery videos that swap data-src to src */
  setTimeout(scan, 800);
  setTimeout(scan, 2500);

  /* Observe DOM for any video added after page load */
  if (typeof MutationObserver !== "undefined") {
    new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
  }
})();
