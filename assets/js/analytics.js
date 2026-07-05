/* ============================================================
   ABI — Analytics loader   (v3)
   ------------------------------------------------------------
   ONE dependency: Google Tag Manager container GTM-NKLLGPC.
   GA4 (G-J6BNX36TS3), Meta Pixel (580471737041846), Microsoft
   Clarity (k5fxn2irko), CallRail (169987046), ClickCease, and
   Google Ads (AW-949292069) are all configured INSIDE the GTM
   web UI — never add/remove those tags here.

   What this file does:
     1. Sets Google Consent Mode v2 to GRANTED by default (all
        regions) so any consent-gated GTM tags fire. Per client
        decision (Jul 2026) there is NO cookie-consent banner.
     2. Boots the GTM container.
     3. Pushes semantic events into dataLayer for GTM triggers:
          - "phone_click"    (tel: taps)          → GA4/Ads call conv.
          - "email_click"    (mailto: taps)
          - "generate_lead"  (form submissions)   → GA4/Ads/Meta lead
        GHL forms are cross-origin iframes, so leads are captured via
        (a) a GHL postMessage listener (best-effort) and (b) the
        thank-you page (reliable — requires the GHL form redirect to
        point at /thank-you; see marker below).

   Trigger names to create in GTM: "CE - phone_click",
   "CE - generate_lead" (both already referenced by the container).
   ============================================================ */
(function () {
  "use strict";

  var GTM_ID = "GTM-NKLLGPC";

  var w = window,
    d = document;
  w.dataLayer = w.dataLayer || [];
  function gtag() {
    w.dataLayer.push(arguments);
  }

  // ---- Consent Mode v2 : granted by default (no banner) ----
  // security_storage/functionality_storage stay granted (essential).
  gtag("consent", "default", {
    ad_storage: "granted",
    ad_user_data: "granted",
    ad_personalization: "granted",
    analytics_storage: "granted"
  });

  // ---- GTM install (Google's official snippet, inlined) ----
  (function (w, d, s, l, i) {
    w[l] = w[l] || [];
    w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var f = d.getElementsByTagName(s)[0],
      j = d.createElement(s),
      dl = l !== "dataLayer" ? "&l=" + l : "";
    j.async = true;
    j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
    f.parentNode.insertBefore(j, f);
  })(window, document, "script", "dataLayer", GTM_ID);

  // ---- semantic click events ----
  function push(event, extra) {
    w.dataLayer.push(assign({ event: event }, extra || {}));
  }
  d.addEventListener(
    "click",
    function (e) {
      var a = e.target.closest && e.target.closest("a");
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("tel:") === 0) push("phone_click", { phone_number: href.slice(4) });
      else if (href.indexOf("mailto:") === 0) push("email_click", { email: href.slice(7) });
    },
    true
  );

  // Native <form> submit (if any page ever ships one).
  d.addEventListener(
    "submit",
    function (e) {
      var form = e.target;
      push("generate_lead", {
        form_id: (form && form.id) || "",
        form_name: (form && form.getAttribute("name")) || "",
        source: "native_form"
      });
    },
    true
  );

  // ---- GHL cross-origin lead capture ----
  var leadFired = false;
  function fireLead(source, extra) {
    if (leadFired) return; // de-dupe within a pageview
    leadFired = true;
    push("generate_lead", assign({ source: source || "ghl_form" }, extra || {}));
  }

  // (a) best-effort: listen for GoHighLevel/LeadConnector submit messages.
  //     Only fires on a clear submit signal — resize/height messages are ignored.
  w.addEventListener("message", function (e) {
    var o = e.origin || "";
    if (!/leadconnectorhq\.com|msgsndr\.com/.test(o)) return;
    var data = e.data;
    var text = typeof data === "string" ? data : "";
    if (data && typeof data === "object") {
      text = (data.type || data.event || data.action || data.eventName || "") + "";
    }
    if (/form[_-]?submit|formsubmit|submitted|onformsubmit|lead[_-]?captured|form_completed/i.test(text)) {
      fireLead("ghl_postmessage");
    }
  });

  // (b) reliable: a thank-you page fires the conversion on load.
  //     GHL form "On submit → Redirect" must point at /thank-you (or /gracias),
  //     or add data-abi-thankyou to any confirmation page.  <<EXTERNAL: set GHL redirect>>
  ready(function () {
    var p = location.pathname.replace(/\/+$/, "");
    if (/\/(thank-you|thankyou|gracias)$/i.test(p) || d.querySelector("[data-abi-thankyou]")) {
      fireLead("thank_you_page");
    }
  });

  // ---- tiny helpers ----
  function assign(target) {
    for (var i = 1; i < arguments.length; i++) {
      var s = arguments[i];
      for (var k in s) if (Object.prototype.hasOwnProperty.call(s, k)) target[k] = s[k];
    }
    return target;
  }
  function ready(fn) {
    if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
})();
