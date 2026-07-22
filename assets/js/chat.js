/*!
 * Multi-channel "Chat" launcher — mobile slide-up panel + desktop left rail.
 * Self-contained: injects its own CSS + DOM, no dependencies.
 * Load site-wide via <script src="/assets/js/chat.js" defer> before </body>.
 * Edit CFG below, then bump the ?v= on the <script> tag.
 */
(function () {
  "use strict";
  if (window.__abiChatInit) return;      // guard against double-load
  window.__abiChatInit = true;

  /* ---- Config: change these to update where the buttons go ---- */
  var CFG = {
    smsNumber: "+19295888448",
    smsBody: "Hi! I would like more information about your barber programs.",
    instagram: "https://ig.me/m/americanbarberinstitute",
    whatsapp: "https://wa.me/19295888448",
    messenger: "https://m.me/Abi.Education",
    avatar: "/apple-touch-icon.png"
  };

  /* ---- Localized copy (Spanish on lang="es" pages) ---- */
  var lang = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
  var es = lang.indexOf("es") === 0;
  var T = es ? {
    chat: "Chat",
    heading: "¿Cómo te gustaría conectar?",
    sub: "Elige una opción y nuestro equipo te atenderá en breve.",
    hi: "American Barber Institute",
    help: "¡Estamos aquí para ayudar!",
    close: "Cerrar",
    reply: "Normalmente respondemos en pocos minutos.",
    sms_t: "Envíanos un mensaje (SMS)", sms_s: "Texto a tu teléfono",
    ig_t: "Instagram", ig_s: "Escríbenos por Instagram",
    wa_t: "WhatsApp", wa_s: "Chatea con nosotros por WhatsApp",
    fb_t: "Facebook Messenger", fb_s: "Escríbenos por Messenger"
  } : {
    chat: "Chat",
    heading: "How would you like to connect?",
    sub: "Choose an option below and our team will be with you shortly.",
    hi: "American Barber Institute",
    help: "We’re here to help!",
    close: "Close",
    reply: "We typically reply within a few minutes.",
    sms_t: "Text Us (SMS)", sms_s: "Text us on your phone",
    ig_t: "Instagram", ig_s: "Message us on Instagram",
    wa_t: "WhatsApp", wa_s: "Chat with us on WhatsApp",
    fb_t: "Facebook Messenger", fb_s: "Message us on Messenger"
  };

  var smsHref = "sms:" + CFG.smsNumber + "?&body=" + encodeURIComponent(CFG.smsBody);

  /* ---- Icons ---- */
  var IC = {
    sms: '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    ig: '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.2" fill="#fff" stroke="none"/></svg>',
    wa: '<svg viewBox="0 0 24 24" fill="#fff" stroke="none"><path d="M17.5 14.4c-.3-.15-1.73-.85-2-.95-.27-.1-.46-.15-.65.15-.19.28-.74.94-.9 1.13-.17.19-.33.21-.62.07-.29-.15-1.23-.46-2.35-1.45-.87-.78-1.46-1.74-1.63-2.03-.17-.29-.02-.44.13-.59.13-.13.29-.34.44-.51.14-.17.19-.29.29-.48.1-.19.05-.36-.02-.51-.08-.15-.65-1.56-.89-2.13-.23-.55-.47-.48-.65-.49h-.55c-.19 0-.5.07-.76.36-.26.29-1 .98-1 2.38 0 1.4 1.03 2.76 1.17 2.95.14.19 2.01 3.08 4.88 4.32.68.29 1.21.47 1.63.6.68.22 1.31.19 1.8.11.55-.08 1.69-.69 1.93-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.19-.55-.34zM12.05 21.5a9.5 9.5 0 0 1-4.85-1.33l-.34-.2-3.6.94.96-3.51-.23-.36a9.44 9.44 0 0 1-1.45-5.03c0-5.23 4.26-9.48 9.5-9.48 2.54 0 4.92 1 6.71 2.79a9.4 9.4 0 0 1 2.78 6.7c0 5.22-4.26 9.48-9.5 9.48z"/></svg>',
    fb: '<svg viewBox="0 0 24 24" fill="#fff" stroke="none"><path d="M12 2C6.5 2 2 6.1 2 11.3c0 2.9 1.4 5.5 3.7 7.2V22l3.4-1.9c.9.3 1.9.4 2.9.4 5.5 0 10-4.1 10-9.2S17.5 2 12 2zm1 12.1-2.6-2.7-5 2.7 5.4-5.7L13.5 11l4.9-2.7-5.4 5.8z"/></svg>',
    chev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>',
    x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.4-3 8.3-7 9.5C8 19.3 5 15.4 5 11V6l7-3z"/></svg>'
  };

  /* ---- Styles ---- */
  var CSS = '' +
    '.abichat-bd{position:fixed;inset:0;background:rgba(10,12,14,.55);opacity:0;visibility:hidden;transition:opacity .22s ease,visibility .22s ease;z-index:2147482800;-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)}' +
    '.abichat-bd.is-open{opacity:1;visibility:visible}' +
    '.abichat{position:fixed;left:12px;right:12px;bottom:12px;margin:0 auto;max-width:420px;background:#fff;border-radius:20px;box-shadow:0 24px 60px rgba(0,0,0,.4);z-index:2147482801;overflow:hidden;transform:translateY(20px) scale(.98);opacity:0;visibility:hidden;transition:opacity .22s ease,transform .22s ease,visibility .22s ease;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-height:86vh;display:flex;flex-direction:column}' +
    '.abichat.is-open{opacity:1;visibility:visible;transform:none}' +
    '.abichat-hd{position:relative;background:#101316;color:#fff;padding:18px 18px 20px;display:flex;align-items:center;gap:13px;border-radius:0 0 24px 24px;box-shadow:0 4px 0 0 #f4a01a;margin-bottom:4px}' +
    '.abichat-av{width:52px;height:52px;border-radius:50%;object-fit:cover;flex:0 0 auto;border:2.5px solid #f4a01a;background:#fff}' +
    '.abichat-hdt{flex:1 1 auto;min-width:0}' +
    '.abichat-hdt b{display:block;font-family:Oswald,Inter,sans-serif;font-weight:600;font-size:18px;line-height:1.2;letter-spacing:.2px}' +
    '.abichat-hdt span{display:block;font-size:13.5px;opacity:.82;margin-top:2px}' +
    '.abichat-x{position:absolute;top:12px;right:12px;width:30px;height:30px;border:0;background:transparent;color:#fff;cursor:pointer;padding:5px;border-radius:8px;opacity:.85}' +
    '.abichat-x:hover{opacity:1;background:rgba(255,255,255,.12)}' +
    '.abichat-x svg{width:20px;height:20px;display:block}' +
    '.abichat-bd-in{padding:20px 16px 8px;overflow-y:auto;-webkit-overflow-scrolling:touch}' +
    '.abichat-h{margin:2px 0 4px;text-align:center;font-family:Oswald,Inter,sans-serif;font-weight:600;font-size:21px;color:#14171a;line-height:1.2}' +
    '.abichat-s{margin:0 auto 16px;text-align:center;font-size:14px;color:#5c6570;max-width:300px;line-height:1.45}' +
    '.abichat-opt{display:flex;align-items:center;gap:14px;padding:13px 14px;margin:0 0 12px;background:#fff;border:1px solid #e8ebee;border-radius:15px;text-decoration:none;color:inherit;box-shadow:0 2px 8px rgba(0,0,0,.05);transition:transform .12s ease,box-shadow .12s ease,border-color .12s ease}' +
    '.abichat-opt:hover,.abichat-opt:focus{transform:translateY(-1px);box-shadow:0 6px 16px rgba(0,0,0,.1);border-color:#d7dbdf;outline:none}' +
    '.abichat-ic{width:46px;height:46px;border-radius:12px;flex:0 0 auto;display:flex;align-items:center;justify-content:center}' +
    '.abichat-ic svg{width:26px;height:26px;display:block}' +
    '.abichat-ic--sms{background:#25d366}' +
    '.abichat-ic--ig{background:linear-gradient(45deg,#feda75,#fa7e1e 30%,#d62976 55%,#962fbf 80%,#4f5bd5)}' +
    '.abichat-ic--wa{background:#25d366}' +
    '.abichat-ic--fb{background:linear-gradient(45deg,#0a7cff,#0af 60%,#8ad4ff)}' +
    '.abichat-ot{flex:1 1 auto;min-width:0}' +
    '.abichat-ot b{display:block;font-weight:700;font-size:15.5px;color:#14171a;line-height:1.25}' +
    '.abichat-ot span{display:block;font-size:13px;color:#68727d;margin-top:2px}' +
    '.abichat-chev{flex:0 0 auto;color:#b6bdc4}' +
    '.abichat-chev svg{width:18px;height:18px;display:block}' +
    '.abichat-ft{display:flex;align-items:center;justify-content:center;gap:7px;padding:12px 16px 16px;font-size:12.5px;color:#7a828b}' +
    '.abichat-ft svg{width:15px;height:15px;flex:0 0 auto;color:#f4a01a}' +
    '.abichat-rail{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:2147482000;display:none;flex-direction:column;gap:8px}' +
    '@media (min-width:1081px){.abichat-rail{display:flex}}' +
    '.abichat-rail a{display:flex;align-items:center;text-decoration:none;color:#fff;border-radius:0 10px 10px 0;overflow:hidden;box-shadow:2px 3px 12px rgba(0,0,0,.28);transition:transform .16s ease;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
    '.abichat-rail a:hover{transform:translateX(3px)}' +
    '.abichat-rail-ic{width:34px;height:34px;flex:0 0 auto;display:flex;align-items:center;justify-content:center}' +
    '.abichat-rail-ic svg{width:22px;height:22px;display:block}' +
    '.abichat-rail-lb{max-width:0;white-space:nowrap;overflow:hidden;font-size:13px;font-weight:700;transition:max-width .22s ease,padding .22s ease}' +
    '.abichat-rail a:hover .abichat-rail-lb,.abichat-rail a:focus .abichat-rail-lb{max-width:170px;padding-right:16px;padding-left:2px}' +
    '.abichat-rail--sms{background:#25d366}' +
    '.abichat-rail--ig{background:linear-gradient(45deg,#feda75,#fa7e1e 30%,#d62976 55%,#962fbf 80%,#4f5bd5)}' +
    '.abichat-rail--wa{background:#25d366}' +
    '.abichat-rail--fb{background:linear-gradient(135deg,#0a7cff,#00b2ff)}' +
    '@media (min-width:560px){.abichat{bottom:auto;top:50%;transform:translateY(-46%) scale(.98)}.abichat.is-open{transform:translateY(-50%)}}' +
    '@media (prefers-reduced-motion:reduce){.abichat,.abichat-bd{transition:none}}';

  function opt(cls, ic, title, sub, href, ext, channel) {
    return '<a class="abichat-opt" data-ch="' + channel + '" href="' + href + '"' +
      (ext ? ' target="_blank" rel="noopener"' : '') + '>' +
      '<span class="abichat-ic abichat-ic--' + cls + '">' + ic + '</span>' +
      '<span class="abichat-ot"><b>' + title + '</b><span>' + sub + '</span></span>' +
      '<span class="abichat-chev" aria-hidden="true">' + IC.chev + '</span></a>';
  }

  function build() {
    var st = document.createElement("style");
    st.id = "abichat-css";
    st.textContent = CSS;
    document.head.appendChild(st);

    var bd = document.createElement("div");
    bd.className = "abichat-bd";
    bd.setAttribute("hidden", "");

    var p = document.createElement("div");
    p.className = "abichat";
    p.setAttribute("role", "dialog");
    p.setAttribute("aria-modal", "true");
    p.setAttribute("aria-label", T.hi + " chat");
    p.setAttribute("hidden", "");
    p.innerHTML =
      '<div class="abichat-hd">' +
        '<img class="abichat-av" src="' + CFG.avatar + '" alt="" width="52" height="52">' +
        '<span class="abichat-hdt"><b>' + T.hi + '</b><span>' + T.help + '</span></span>' +
        '<button class="abichat-x" type="button" aria-label="' + T.close + '">' + IC.x + '</button>' +
      '</div>' +
      '<div class="abichat-bd-in">' +
        '<h2 class="abichat-h">' + T.heading + '</h2>' +
        '<p class="abichat-s">' + T.sub + '</p>' +
        opt("sms", IC.sms, T.sms_t, T.sms_s, smsHref, false, "sms") +
        opt("ig", IC.ig, T.ig_t, T.ig_s, CFG.instagram, true, "instagram") +
        opt("wa", IC.wa, T.wa_t, T.wa_s, CFG.whatsapp, true, "whatsapp") +
        opt("fb", IC.fb, T.fb_t, T.fb_s, CFG.messenger, true, "messenger") +
      '</div>' +
      '<div class="abichat-ft">' + IC.shield + '<span>' + T.reply + '</span></div>';

    document.body.appendChild(bd);
    document.body.appendChild(p);
    return { bd: bd, p: p };
  }

  function track(action, label) {
    try {
      (window.dataLayer = window.dataLayer || []).push({ event: "chat_widget", chat_action: action, chat_channel: label || "" });
      if (typeof window.gtag === "function") window.gtag("event", "chat_" + action, { channel: label || "" });
    } catch (e) {}
  }

  function buildRail() {
    var items = [
      { cls: "sms", ic: IC.sms, href: smsHref,       ext: false, ch: "sms",       lb: (es ? "Texto" : "Text Us"), al: T.sms_t },
      { cls: "ig",  ic: IC.ig,  href: CFG.instagram, ext: true,  ch: "instagram", lb: "Instagram",                al: T.ig_t },
      { cls: "wa",  ic: IC.wa,  href: CFG.whatsapp,  ext: true,  ch: "whatsapp",  lb: "WhatsApp",                 al: T.wa_t },
      { cls: "fb",  ic: IC.fb,  href: CFG.messenger, ext: true,  ch: "messenger", lb: "Messenger",                al: T.fb_t }
    ];
    var rail = document.createElement("div");
    rail.className = "abichat-rail";
    rail.setAttribute("aria-label", es ? "Contáctanos" : "Contact us");
    rail.innerHTML = items.map(function (it) {
      return '<a class="abichat-rail--' + it.cls + '" href="' + it.href + '" data-ch="' + it.ch + '"' +
        (it.ext ? ' target="_blank" rel="noopener"' : '') + ' aria-label="' + it.al + '">' +
        '<span class="abichat-rail-ic">' + it.ic + '</span>' +
        '<span class="abichat-rail-lb">' + it.lb + '</span></a>';
    }).join("");
    document.body.appendChild(rail);
    Array.prototype.forEach.call(rail.querySelectorAll("a"), function (a) {
      a.addEventListener("click", function () { track("channel", a.getAttribute("data-ch")); });
    });
  }

  function init() {
    buildRail();   // desktop channel rail (shown via CSS only >=1081px)

    var triggers = document.querySelectorAll("a.mbar-text, .lf-mcta__btn--text");
    if (!triggers.length) return;

    var els = build();
    var bd = els.bd, p = els.p, lastFocus = null;

    function open(e) {
      if (e) e.preventDefault();
      lastFocus = document.activeElement;
      bd.hidden = false; p.hidden = false;
      void p.offsetWidth;
      bd.classList.add("is-open"); p.classList.add("is-open");
      document.documentElement.style.overflow = "hidden";
      var x = p.querySelector(".abichat-x");
      if (x) x.focus();
      track("open", "");
    }
    function close() {
      bd.classList.remove("is-open"); p.classList.remove("is-open");
      document.documentElement.style.overflow = "";
      setTimeout(function () { bd.hidden = true; p.hidden = true; }, 240);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    Array.prototype.forEach.call(triggers, function (t) {
      var s = t.querySelector("span");
      if (s) s.textContent = T.chat;
      t.setAttribute("aria-haspopup", "dialog");
      t.setAttribute("role", "button");
      t.addEventListener("click", open);
    });

    bd.addEventListener("click", close);
    p.querySelector(".abichat-x").addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && p.classList.contains("is-open")) close();
    });
    Array.prototype.forEach.call(p.querySelectorAll(".abichat-opt"), function (a) {
      a.addEventListener("click", function () { track("channel", a.getAttribute("data-ch")); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
