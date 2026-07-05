/* ABI — Motion & Effects engine (vanilla, no deps, rAF-driven) */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) return; // respect the user — style.css already silences CSS animations

  /* ---------- Scroll progress bar ---------- */
  var bar = document.createElement('div');
  bar.className = 'scroll-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  /* ---------- Header morph ---------- */
  var head = document.querySelector('.hdr');

  /* ---------- Parallax targets ---------- */
  var heroBg = document.querySelector('.hero-bg');
  var splitImgs = Array.prototype.slice.call(document.querySelectorAll('.split-media img'));

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY;
      var max = document.documentElement.scrollHeight - innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
      if (head) head.classList.toggle('scrolled', y > 40);
      if (heroBg) heroBg.style.translate = '0 ' + Math.min(y * 0.28, 260) + 'px';
      for (var i = 0; i < splitImgs.length; i++) {
        var r = splitImgs[i].getBoundingClientRect();
        if (r.bottom > 0 && r.top < innerHeight) {
          var p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight; // -0.5..0.5
          splitImgs[i].style.translate = '0 ' + (p * -26).toFixed(1) + 'px';
        }
      }
      ticking = false;
    });
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Section heads: in-view class (kicker draw + h2 mask) ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
      });
    }, { threshold: 0.35 });
    document.querySelectorAll('.section-head, .split > div').forEach(function (el) { io.observe(el); });
  }

  /* ---------- Stagger reveals: per-sibling delay ---------- */
  document.querySelectorAll('.cards, .quotes, .steps, .gallery-grid, .videos, .tuition-grid').forEach(function (group) {
    var idx = 0;
    Array.prototype.forEach.call(group.children, function (child) {
      if (child.classList.contains('reveal')) {
        child.style.setProperty('--d', (Math.min(idx, 7) * 0.09).toFixed(2) + 's');
        idx++;
      }
    });
  });

  /* ---------- Card 3D tilt + glare ---------- */
  if (window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.card').forEach(function (card) {
      var glare = document.createElement('span');
      glare.className = 'glare';
      card.appendChild(glare);
      var raf = null;
      card.addEventListener('mousemove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width;
          var py = (e.clientY - r.top) / r.height;
          card.classList.add('tilting');
          card.style.transform = 'perspective(900px) rotateY(' + ((px - 0.5) * 7).toFixed(2) + 'deg) rotateX(' + ((0.5 - py) * 6).toFixed(2) + 'deg) translateY(-5px)';
          card.style.setProperty('--gx', (px * 100).toFixed(1) + '%');
          card.style.setProperty('--gy', (py * 100).toFixed(1) + '%');
          raf = null;
        });
      });
      card.addEventListener('mouseleave', function () {
        card.classList.remove('tilting');
        card.style.transform = '';
      });
    });

    /* ---------- Magnetic buttons ---------- */
    document.querySelectorAll('.btn').forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var dx = (e.clientX - r.left - r.width / 2) / r.width;
        var dy = (e.clientY - r.top - r.height / 2) / r.height;
        btn.style.translate = (dx * 6).toFixed(1) + 'px ' + (dy * 5).toFixed(1) + 'px';
      });
      btn.addEventListener('mouseleave', function () { btn.style.translate = ''; });
    });
  }

  /* ---------- Ripple on press ---------- */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.btn');
    if (!btn) return;
    var r = btn.getBoundingClientRect();
    var d = Math.max(r.width, r.height);
    var rip = document.createElement('span');
    rip.className = 'ripple';
    rip.style.width = rip.style.height = d + 'px';
    rip.style.left = (e.clientX - r.left - d / 2) + 'px';
    rip.style.top = (e.clientY - r.top - d / 2) + 'px';
    btn.appendChild(rip);
    setTimeout(function () { rip.remove(); }, 600);
  });

  /* ---------- Countdown tick pulse ---------- */
  var sec = document.querySelector('[data-countdown] [data-s]');
  if (sec) {
    new MutationObserver(function () {
      sec.classList.remove('tick');
      void sec.offsetWidth; // restart animation
      sec.classList.add('tick');
    }).observe(sec, { childList: true, characterData: true, subtree: true });
  }

  /* ---------- Hero particles: drifting gold flecks ---------- */
  var hero = document.querySelector('.hero');
  if (hero) {
    var canvas = document.createElement('canvas');
    canvas.className = 'hero-particles';
    canvas.setAttribute('aria-hidden', 'true');
    hero.insertBefore(canvas, hero.querySelector('.wrap'));
    var ctx = canvas.getContext('2d');
    var parts = [], running = false, W = 0, H = 0;

    function accent() {
      return getComputedStyle(document.documentElement).getPropertyValue('--gold-soft').trim() || '#f0d896';
    }
    var color = accent();
    new MutationObserver(function () { color = accent(); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    function size() {
      W = canvas.width = hero.offsetWidth;
      H = canvas.height = hero.offsetHeight;
    }
    function spawn(n) {
      parts = [];
      for (var i = 0; i < n; i++) {
        parts.push({
          x: Math.random() * W, y: Math.random() * H,
          r: Math.random() * 1.9 + 0.5,
          vy: -(Math.random() * 0.34 + 0.08),
          vx: (Math.random() - 0.5) * 0.22,
          a: Math.random() * 0.5 + 0.12,
          tw: Math.random() * 0.02 + 0.004,
          ph: Math.random() * Math.PI * 2
        });
      }
    }
    function frame(t) {
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = color;
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        p.x += p.vx; p.y += p.vy; p.ph += p.tw;
        if (p.y < -8) { p.y = H + 8; p.x = Math.random() * W; }
        if (p.x < -8) p.x = W + 8; else if (p.x > W + 8) p.x = -8;
        ctx.globalAlpha = p.a * (0.6 + 0.4 * Math.sin(p.ph * 40));
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, 6.2832);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(frame);
    }
    function start() { if (!running) { running = true; requestAnimationFrame(frame); } }
    function stop() { running = false; }

    size();
    spawn(Math.min(70, Math.round(W / 18)));
    addEventListener('resize', function () { size(); spawn(Math.min(70, Math.round(W / 18))); }, { passive: true });
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries[0].isIntersecting ? start() : stop();
      }).observe(hero);
    } else { start(); }
  }

  /* ---------- Animated number counters ([data-count]) ---------- */
  (function () {
    var els = [].slice.call(document.querySelectorAll('[data-count]'));
    if (!els.length) return;
    // Respect reduced-motion: keep the real (baked-in) values, skip the count-up.
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    function run(el) {
      var target = parseFloat(el.getAttribute('data-count')) || 0;
      var suffix = el.getAttribute('data-suffix') || '';
      var dur = 1400, t0 = null;
      function step(ts) {
        if (!t0) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        var val = Math.round(target * eased);
        el.textContent = val.toLocaleString('en-US') + suffix;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
        });
      }, { threshold: 0.4 });
      els.forEach(function (el) { io.observe(el); });
    } else { els.forEach(run); }
  })();

  /* ---------- Back-to-top button ---------- */
  (function () {
    var btn = document.querySelector('.to-top');
    if (!btn) return;
    function tog() { btn.classList.toggle('show', window.scrollY > 600); }
    addEventListener('scroll', tog, { passive: true }); tog();
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  })();

  /* ---------- Gallery lightbox ---------- */
  (function () {
    var links = [].slice.call(document.querySelectorAll('.gallery-grid a, .gal a'));
    if (!links.length) return;
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button>'
      + '<button class="lb-prev" aria-label="Previous">&#8249;</button>'
      + '<img alt="Enlarged gallery image"><button class="lb-next" aria-label="Next">&#8250;</button>'
      + '<div class="lb-count"></div>';
    document.body.appendChild(box);
    var img = box.querySelector('img'), count = box.querySelector('.lb-count'), i = 0;
    function show(n) {
      i = (n + links.length) % links.length;
      img.src = links[i].getAttribute('href');
      count.textContent = (i + 1) + ' / ' + links.length;
    }
    function open(n) { show(n); box.classList.add('open'); document.body.style.overflow = 'hidden'; }
    function close() { box.classList.remove('open'); document.body.style.overflow = ''; }
    links.forEach(function (a, n) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(n); });
    });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(i + 1); });
    box.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(i - 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(i + 1);
      else if (e.key === 'ArrowLeft') show(i - 1);
    });
  })();
})();
