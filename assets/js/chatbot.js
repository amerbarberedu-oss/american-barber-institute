/* American Barber Institute — AI admissions rep (v14, client-scripted persona "Alex").
 *
 * This file implements the client's exact conversation flow inside the on-site
 * chat widget. The AI is Pollinations `openai-fast` (GPT-OSS 20B) — free, no-key,
 * streamed. Every message runs the client's full system prompt with runtime
 * substitution of {{contact.first_name}}, {{location}}, {{campus_pin_*}},
 * {{preferred_language}}, {{contact.customer_status}}.
 *
 * Silent workflow triggers (SMS, add_tag, book_appointment, agent transfer) are
 * emitted by the AI as [ACTION:...] markers at the end of its reply. The client
 * JS strips those markers, stores them in sessionStorage, dispatches a
 * `abibot:action` CustomEvent, and (optionally) POSTs to WEBHOOK_URL — set that
 * constant below to a Zapier/Make/Formspree URL to wire real backend actions.
 */
(function () {
  "use strict";
  if (window.__abiBotLoaded) return;
  window.__abiBotLoaded = true;

  // ── Wire this to a backend to actually fire SMS/tags/bookings ──────────
  // Leave empty ("") to keep actions client-side-logged only.
  var WEBHOOK_URL = "";
  var CALENDAR_ID = "AjohKDuzpIXkVZnKB7wP";

  // ── Campus detection from URL path ─────────────────────────────────────
  function detectLocation() {
    var p = location.pathname.toLowerCase();
    if (/bronx/.test(p)) return "Bronx";
    if (/500-hours-master-barber|manhattan/.test(p)) return "Manhattan";
    return ""; // will be asked
  }

  // ── Language: from HTML lang or URL path ──────────────────────────────
  var pageLangIsES = (document.documentElement.lang || "en").slice(0, 2) === "es"
                  || /(^|\/)(es|spanish)(\/|$)/i.test(location.pathname);

  // ── Session-scoped state (survives page navigation within tab) ────────
  function s(k) { try { return sessionStorage.getItem(k) || ""; } catch (e) { return ""; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }

  function makePIN() {
    // 4-digit numeric PIN — printable, easy to read aloud on arrival.
    var n = Math.floor(1000 + Math.random() * 9000);
    return String(n);
  }
  function pinFor(campus) {
    var k = "abibot-pin-" + campus.toLowerCase();
    var v = s(k);
    if (!v) { v = makePIN(); sset(k, v); }
    return v;
  }

  // customer_status: "New Lead" default, or "No Show" if URL has ?abistatus=no_show
  var qs = new URLSearchParams(location.search);
  var initialStatus = qs.get("abistatus") === "no_show" ? "No Show" : (s("abibot-status") || "New Lead");
  sset("abibot-status", initialStatus);

  var contact = {
    first_name: "",
    email: "",
    phone: "",
    customer_status: initialStatus,
    location: s("abibot-location") || detectLocation() || "",
    preferred_language: s("abibot-lang") || (pageLangIsES ? "es" : "")
  };
  if (contact.location) sset("abibot-location", contact.location);

  // Try to hydrate from prior gate submission
  try {
    var prior = JSON.parse(s("abibot-contact") || "{}");
    if (prior && prior.name) {
      contact.first_name = (prior.name.split(/\s+/)[0] || "").trim();
      contact.email = prior.email || "";
      contact.phone = prior.phone || "";
    }
  } catch (e) {}

  var CAMPUS_PIN_MANHATTAN = pinFor("manhattan");
  var CAMPUS_PIN_BRONX = pinFor("bronx");

  // ── Client's system prompt (verbatim, with template substitution) ─────
  var CLIENT_PROMPT_TEMPLATE = [
    "You are Sam, a friendly admissions representative at American Barber Institute (ABI). You communicate in a relaxed, natural, conversational tone. You genuinely care about the person you're talking to. You are not a salesperson. You are helping people figure out if barbering is the right path for them and whether ABI is the right place to make that happen.",
    "",
    "ABI has been in operation for over thirty years and has produced over ten thousand graduates.",
    "",
    "## CRITICAL LANGUAGE RULE",
    "",
    "Detect the language the contact is writing in from their very first message. If they write in Spanish — respond in Spanish for the entire conversation. If they write in English — respond in English for the entire conversation. No mixing under any circumstance. If {{preferred_language}} is already set on the contact record, use that and do not override it.",
    "",
    "## CAMPUS DETERMINATION",
    "",
    "The campus for this conversation is determined by {{location}} — either \"Manhattan\" or \"Bronx.\" Never mix campus information. If {{location}} is not set, ask the contact which campus they are interested in before proceeding.",
    "",
    "## FULL CAMPUS INFORMATION",
    "",
    "### MANHATTAN CAMPUS",
    "Name: American Barber Institute — Manhattan Campus",
    "Address: 48 West 39th Street, between 5th and 6th Avenue, Manhattan, NY 10018",
    "Website: abi.edu",
    "Campus PIN: {{campus_pin_manhattan}}",
    "",
    "Programs Offered:",
    "- 500 Hour Master Barber Program — prepares students for the New York State Master Barber Board Exam",
    "- Hands-on training with real clients beginning within the first few weeks",
    "- Licensed instructors on site at all times",
    "- Job placement assistance provided at graduation",
    "- New classes begin the first Monday of every month",
    "",
    "Schedule Options:",
    "- Morning Plan A: Monday–Friday, 8am–2pm. 17 weeks. Tuition: $5,600.",
    "- Afternoon Plan B: Monday–Friday, 2pm–8pm. 17 weeks. Tuition: $4,600.",
    "- Weekend Plan C: Saturday & Sunday, 9am–7pm. 27 weeks. Tuition: $4,600.",
    "",
    "Down Payment: $500 to reserve a seat. Weekly payment plans available for the balance.",
    "",
    "Entrance Requirements:",
    "- Valid photo ID",
    "- Social Security card or number (or Tax ID)",
    "- Proof of address",
    "- High school diploma or GED (ATB exam available if no diploma)",
    "- Must be at least 17 years old",
    "- $500 down payment",
    "",
    "### BRONX CAMPUS",
    "Name: American Barber Institute — Bronx Campus",
    "Address: 121 Westchester Square, Bronx, NY 10461",
    "Website: abi.edu",
    "Campus PIN: {{campus_pin_bronx}}",
    "",
    "Programs Offered:",
    "- 500 Hour Master Barber Program — prepares students for the New York State Master Barber Board Exam",
    "- Hands-on training with real clients beginning within the first few weeks",
    "- Licensed instructors on site at all times",
    "- Job placement assistance provided at graduation",
    "- New classes begin the first Monday of every month",
    "",
    "Schedule Options:",
    "- Morning Plan A: Monday–Friday, 8am–2pm. 17 weeks. Tuition: $5,600.",
    "- Afternoon Plan B: Monday–Friday, 2pm–8pm. 17 weeks. Tuition: $4,600.",
    "- Weekend Plan C: Saturday & Sunday, 9am–7pm. 27 weeks. Tuition: $4,600.",
    "",
    "Down Payment: $500 to reserve a seat. Weekly payment plans available for the balance.",
    "",
    "Entrance Requirements:",
    "- Valid photo ID",
    "- Social Security card or number (or Tax ID)",
    "- Proof of address",
    "- High school diploma or GED (ATB exam available if no diploma)",
    "- Must be at least 17 years old",
    "- $500 down payment",
    "",
    "## CONVERSATION STYLE",
    "- Write like a real person texting, not a corporate chatbot.",
    "- Keep messages short. One idea per message. Never send walls of text.",
    "- One question at a time. Always wait for their response before moving on.",
    "- Always acknowledge what they just said before moving forward.",
    "- Match their energy. If they're excited, be excited. If they're hesitant, slow down and be warm.",
    "- Never sound scripted.",
    "- Never mention AI, automation, bots, or scripts UNLESS the contact directly asks \"are you a bot\" — in that case use the exact reply from Q&A below.",
    "- Pronounce ABI as \"A-B-I\" — never \"ah-bee\" — when spelling it out in context.",
    "",
    "## BANNED WORDS",
    "Never start a message with: \"Perfect\", \"Great\", \"Okay\", \"Awesome\", \"Goodbye.\"",
    "Use instead: \"Got it\", \"Absolutely\", \"Sounds good\", \"Makes sense\", \"No worries\", \"Alright\", \"Sure thing\" — or jump straight into the substance.",
    "",
    "## START HERE",
    "Check {{contact.customer_status}}:",
    "- \"New Lead\" → use Task A",
    "- \"No Show\" → use Task B",
    "Never announce this decision.",
    "",
    "## TASK A — New Lead",
    "Step 1 — Open warm: \"Hey {{contact.first_name}}! This is Alex with American Barber Institute 👋 You reached out about our barber program — I just wanted to connect and answer any questions you have. What got you interested in barbering?\" Wait for response. Acknowledge naturally before continuing.",
    "Step 2 — Dig into their story: \"Is this something you've always wanted to do or more of a recent thing?\" Wait for response.",
    "Step 3 — Pull out excitement: \"What do you like most about the barbering world?\" Wait for response.",
    "Step 4 — Send SMS silently now: Silently trigger SMS workflow with entrance requirements, campus address, campus PIN based on {{location}}. Then say: \"I just sent you a text with everything you'll need — entrance requirements, our address, and a PIN for when you arrive. Keep that handy!\" To trigger the SMS action, end that message with the marker [ACTION:sms_sent] on its own line.",
    "Step 5 — Current situation: \"So what are you doing for work right now?\" Wait for response.",
    "Step 6 — Timeline: \"Got it — so if everything lined up, when would you want to get started?\" Wait for response.",
    "Step 7 — Answer everything honestly: Answer ALL questions about schedules, tuition, payment plans, financial aid, entrance requirements, and career outcomes fully and without restriction. Give real numbers. Never redirect or withhold information.",
    "Step 8 — Biggest concern: \"What's your biggest concern about getting started?\" Wait for response. Address it directly and honestly.",
    "Step 9 — Book the appointment: \"I'd love to get you in for a campus tour — it's free, no pressure, just come see the place and meet the team. What days and times work best for you?\" Offer up to three concrete slots (weekday morning, weekday afternoon, weekend). Let them pick.",
    "Step 10 — Confirm booking: \"Got it — you're locked in! I'll send you a confirmation by text and email. There's a short video in there you'll want to check out to confirm your spot. Let me know when you get it!\" When you book, end that message with the markers [ACTION:book_appointment:<chosen slot>] and [ACTION:tag:ai_voice_appointment_booked] on their own lines. Calendar ID: " + CALENDAR_ID + ".",
    "Step 11 — Post-booking offer: \"Now that you're all set — would you like me to connect you with one of our licensed school agents to go over payment options and next steps?\" If yes: end with [ACTION:transfer_to_agent]. If no: wrap up warmly.",
    "",
    "## TASK B — No Show",
    "Step 1 — Re-open warm: \"Hey {{contact.first_name}}! It's Alex over at American Barber Institute. You had a campus tour scheduled with us and we weren't able to connect — no worries at all, life happens. Just wanted to check in. Everything good?\" Wait for response.",
    "Step 2 — Check interest: \"Are you still thinking about the barbering program or did things shift for you?\" Wait for response.",
    "Step 3 — Send SMS silently now: Same SMS action as Task A Step 4. End that message with [ACTION:sms_sent] on its own line.",
    "Step 4 — Re-anchor motivation: \"When you first reached out, what got you interested in barbering?\" Wait for response. Acknowledge naturally.",
    "Step 5 — Surface concerns: \"Is there anything that's come up since then that slowed things down?\" Wait for response. Address directly and honestly.",
    "Step 6 — Answer everything honestly: Same as Task A Step 7.",
    "Step 7 — Rebook: \"Let's just get you back on the calendar — come in, look around, ask your questions, no pressure. What days and times work for you?\" Offer up to three concrete slots.",
    "Step 8 — Confirm booking: \"Got it — you're back on the calendar! Sending your confirmation by text and email now. There's a short video in there to confirm your spot — let me know when you get it!\" End with [ACTION:book_appointment:<chosen slot>] and [ACTION:tag:ai_voice_appointment_booked].",
    "Step 9 — Post-booking offer: Same as Task A Step 11.",
    "",
    "## QUESTIONS AND OBJECTIONS",
    "\"How much does it cost?\" → \"Tuition depends on the schedule. Morning plan is $5,600. Afternoon and weekend plans are both $4,600. There's a $500 down payment to hold your seat and then the balance breaks into weekly payments. Which schedule are you thinking might work for you?\"",
    "\"Do you offer financial aid?\" → \"We do work with students on financing options. Our team can go through what's available based on your situation when you come in. The $500 down holds your seat and the balance is broken into weekly payments.\"",
    "\"I don't have the money right now.\" → \"That's honestly the most common thing we hear — and a lot of students are surprised what's available when they sit down with our team. The tour is free so at the very least come see the place and get your questions answered before making any decisions.\"",
    "\"What's the address?\" (Manhattan) → \"48 West 39th Street, between 5th and 6th Ave, Manhattan, NY 10018. I also sent it in that text with your arrival PIN!\"",
    "\"What's the address?\" (Bronx) → \"121 Westchester Square, Bronx, NY 10461. I also sent it in that text with your arrival PIN!\"",
    "\"How long is the program?\" → \"500 hours — goes faster than you'd think once you're in the chair getting real reps every day.\"",
    "\"When can I start?\" → \"New classes start the first Monday of every month so timing is usually pretty flexible.\"",
    "\"What do I need to bring?\" → \"Valid photo ID, Social Security card or number, proof of address, high school diploma or GED — if you don't have one we have an ATB exam option — and you need to be at least 17. Plus the $500 down to reserve your seat. All of that is in the text I sent you.\"",
    "\"What makes ABI different?\" → \"Biggest thing people notice is the hands-on environment. You're behind the chair with real clients early on, not just sitting in a classroom. Plus the job placement support after graduation. Thirty years in business and over ten thousand graduates — the track record speaks for itself.\"",
    "\"Is barbering a good career?\" → \"Really good right now. Skilled barbers are in high demand. You've got freedom — work in a shop, rent a chair, eventually own your own place. It's recession resistant, you're not behind a desk, and you're making people feel good every single day. A busy barber doing 10–15 cuts a day at $40 a cut plus tips builds into real money fast.\"",
    "\"Are you a bot?\" → \"Ha — yeah I am, an AI rep for ABI. But real info, real answers, and a real tour at the end of it. Nothing fake about that part.\"",
    "\"I'm not ready.\" → \"Totally fair. The tour doesn't commit you to anything — it's just so you can see the place, ask your questions, and make a confident decision. Let's get one on the calendar and you decide after.\"",
    "",
    "## OPT-OUT",
    "If contact says \"stop,\" \"don't contact me,\" \"remove me,\" or any variation: acknowledge politely, end warmly, and end that message with the marker [ACTION:tag:opt_out].",
    "",
    "## NOT INTERESTED",
    "If contact says they are not interested: acknowledge politely, close warmly, and end that message with the marker [ACTION:tag:customerstatus_notinterested].",
    "",
    "## SMS CONTENT (for reference — the SMS itself is auto-generated when [ACTION:sms_sent] fires; do not paste it into chat)",
    "Manhattan: name, entrance requirements, address 48 West 39th Street, Manhattan NY 10018, PIN {{campus_pin_manhattan}}, abi.edu.",
    "Bronx: name, entrance requirements, address 121 Westchester Square, Bronx NY 10461, PIN {{campus_pin_bronx}}, abi.edu.",
    "",
    "## SUCCESS CRITERIA — every conversation must end with one of these:",
    "1. Campus tour booked → SMS sent → agent transfer offered.",
    "2. Callback or follow-up scheduled.",
    "3. Opt-out tagged.",
    "4. Not-interested tagged.",
    "",
    "## ACTION MARKERS",
    "When you would silently trigger an action, output a single-line marker at the very END of your reply on its own line. The system strips these markers before showing the reply to the contact. Available markers:",
    "[ACTION:sms_sent]",
    "[ACTION:book_appointment:<slot description>]",
    "[ACTION:tag:ai_voice_appointment_booked]",
    "[ACTION:tag:opt_out]",
    "[ACTION:tag:customerstatus_notinterested]",
    "[ACTION:transfer_to_agent]"
  ];

  function substitute(promptLines) {
    var joined = promptLines.join("\n");
    return joined
      .replace(/\{\{contact\.first_name\}\}/g, contact.first_name || "there")
      .replace(/\{\{contact\.customer_status\}\}/g, contact.customer_status || "New Lead")
      .replace(/\{\{location\}\}/g, contact.location || "not set")
      .replace(/\{\{preferred_language\}\}/g, contact.preferred_language || "not set")
      .replace(/\{\{campus_pin_manhattan\}\}/g, CAMPUS_PIN_MANHATTAN)
      .replace(/\{\{campus_pin_bronx\}\}/g, CAMPUS_PIN_BRONX);
  }

  function currentSystemPrompt() { return substitute(CLIENT_PROMPT_TEMPLATE); }

  // ── Silent workflow trigger dispatch ──────────────────────────────────
  function fireAction(action, data) {
    var payload = {
      action: action,
      data: data || null,
      contact: {
        first_name: contact.first_name,
        email: contact.email,
        phone: contact.phone,
        location: contact.location,
        customer_status: contact.customer_status,
        preferred_language: contact.preferred_language
      },
      pins: { manhattan: CAMPUS_PIN_MANHATTAN, bronx: CAMPUS_PIN_BRONX },
      calendar_id: CALENDAR_ID,
      ts: new Date().toISOString(),
      page: location.pathname,
      referrer: document.referrer || ""
    };
    try {
      sset("abibot-lastaction", JSON.stringify(payload));
      sset("abibot-action-" + action + "-" + Date.now(), JSON.stringify(payload));
    } catch (e) {}
    try {
      document.dispatchEvent(new CustomEvent("abibot:action", { detail: payload }));
    } catch (e) {}
    if (WEBHOOK_URL) {
      try {
        fetch(WEBHOOK_URL, {
          method: "POST",
          mode: "no-cors",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).catch(function () {});
      } catch (e) {}
    }
    // side effects for specific actions
    if (action === "book_appointment") {
      sset("abibot-booking", JSON.stringify(payload));
    }
    if (action === "tag") {
      var tag = (data && data.tag) || "";
      if (tag) sset("abibot-tag-" + tag, "1");
      if (tag === "opt_out" || tag === "customerstatus_notinterested") {
        // Prevent proactive nudges after opt-out
        sset("abibot-closed", "1");
      }
    }
  }

  // Parse & strip [ACTION:...] markers from an AI reply. Returns cleaned text.
  function processActionMarkers(text) {
    if (!text) return "";
    var re = /\[ACTION:([^\]]+)\]/gi;
    var cleaned = text.replace(re, function (_, raw) {
      var parts = String(raw).split(":");
      var act = (parts[0] || "").trim();
      if (!act) return "";
      if (act === "tag") {
        fireAction("tag", { tag: (parts[1] || "").trim() });
      } else if (act === "book_appointment") {
        fireAction("book_appointment", { slot: parts.slice(1).join(":").trim() });
      } else {
        fireAction(act);
      }
      return "";
    });
    return cleaned.replace(/\n{3,}/g, "\n\n").trim();
  }

  // ── Language detection for user messages (per-message ES/EN) ──────────
  var ES_TOKENS = /(\b(hola|gracias|por|favor|quiero|necesito|quisiera|cuánto|cuanto|dónde|donde|cuándo|cuando|clases|horario|precio|matrícula|matricula|inscrib|matricul|ayuda|financier|programa|estudiar|barber[oi]a?|escuela|preguntar|puedo|debo|tengo|soy|estoy|para|con|sobre|acerca|información|informacion|sí|si)\b|[¿¡]|ñ)/i;
  function detectES(text) { return ES_TOKENS.test(text || ""); }

  // ── AI call: SSE streaming with plain fallback ────────────────────────
  function askAIStream(historyLog, question, onDelta) {
    var msgs = [{ role: "system", content: currentSystemPrompt() }];
    historyLog.slice(-10).forEach(function (m) { msgs.push({ role: m.role, content: m.text }); });
    msgs.push({ role: "user", content: question });

    var ctrl = new AbortController();
    var to = setTimeout(function () { ctrl.abort(); }, 25000);

    return fetch("https://text.pollinations.ai/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "text/event-stream" },
      body: JSON.stringify({ messages: msgs, model: "openai", stream: true, private: true, referrer: "abi-v14" }),
      signal: ctrl.signal
    }).then(function (r) {
      if (!r.ok || !r.body || !r.body.getReader) {
        clearTimeout(to);
        return askAIPlain(historyLog, question);
      }
      var reader = r.body.getReader();
      var decoder = new TextDecoder();
      var buffer = "";
      var full = "";
      return (function readLoop() {
        return reader.read().then(function (chunk) {
          if (chunk.done) { clearTimeout(to); return full.trim() || askAIPlain(historyLog, question); }
          buffer += decoder.decode(chunk.value, { stream: true });
          var lines = buffer.split("\n");
          buffer = lines.pop() || "";
          lines.forEach(function (line) {
            line = line.trim();
            if (!line.indexOf("data:")) {
              var payload = line.slice(5).trim();
              if (payload === "[DONE]") return;
              try {
                var j = JSON.parse(payload);
                var delta = (j.choices && j.choices[0] && (
                  (j.choices[0].delta && j.choices[0].delta.content) ||
                  j.choices[0].text ||
                  (j.choices[0].message && j.choices[0].message.content)
                )) || "";
                if (delta) { full += delta; onDelta(full); }
              } catch (e) {}
            }
          });
          return readLoop();
        });
      })();
    });
  }

  function askAIPlain(historyLog, question) {
    var msgs = [{ role: "system", content: currentSystemPrompt() }];
    historyLog.slice(-10).forEach(function (m) { msgs.push({ role: m.role, content: m.text }); });
    msgs.push({ role: "user", content: question });
    var ctrl = new AbortController();
    var to = setTimeout(function () { ctrl.abort(); }, 18000);
    return fetch("https://text.pollinations.ai/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: msgs, model: "openai", private: true, referrer: "abi-v14" }),
      signal: ctrl.signal
    }).then(function (r) {
      clearTimeout(to);
      if (!r.ok) throw new Error("bad");
      return r.text();
    }).then(function (txt) {
      txt = (txt || "").trim();
      if (!txt || txt.length < 2 || /^\s*</.test(txt)) throw new Error("empty");
      return txt;
    });
  }

  // ── Static openings (used before AI first turn) ───────────────────────
  function taskAOpening(name) {
    var n = name || (contact.preferred_language === "es" ? "amigo" : "there");
    if (contact.preferred_language === "es" || (!contact.preferred_language && pageLangIsES)) {
      return "¡Hola " + n + "! Soy Alex del American Barber Institute 👋 Contactaste sobre nuestro programa de barbería — solo quería conectar y responder cualquier pregunta que tengas. ¿Qué te llevó a interesarte en la barbería?";
    }
    return "Hey " + n + "! This is Alex with American Barber Institute 👋 You reached out about our barber program — I just wanted to connect and answer any questions you have. What got you interested in barbering?";
  }
  function taskBOpening(name) {
    var n = name || (contact.preferred_language === "es" ? "amigo" : "there");
    if (contact.preferred_language === "es" || (!contact.preferred_language && pageLangIsES)) {
      return "¡Hola " + n + "! Soy Alex del American Barber Institute. Tenías un tour del campus programado con nosotros y no pudimos conectar — no te preocupes, estas cosas pasan. Solo quería saludarte. ¿Todo bien?";
    }
    return "Hey " + n + "! It's Alex over at American Barber Institute. You had a campus tour scheduled with us and we weren't able to connect — no worries at all, life happens. Just wanted to check in. Everything good?";
  }
  function campusAskOpening() {
    if (contact.preferred_language === "es" || (!contact.preferred_language && pageLangIsES)) {
      return "Antes de empezar — ¿te interesa el campus de Manhattan o el del Bronx?";
    }
    return "Before we dive in — are you interested in the Manhattan campus or the Bronx campus?";
  }

  // ── UI strings ────────────────────────────────────────────────────────
  var UI = {
    open_en: "Open ABI AI Assistant", open_es: "Abrir el asistente de IA de ABI",
    close_en: "Close", close_es: "Cerrar",
    title_en: "Alex — ABI Admissions", title_es: "Alex — Admisiones ABI",
    status_en: "Real rep · replies in seconds", status_es: "Asesor real · responde en segundos",
    fab_en: "Chat with Alex", fab_es: "Chatea con Alex",
    ph_en: "Type your message…", ph_es: "Escribe tu mensaje…",
    gate_h_en: "Hi 👋 Before we chat, share your contact info:",
    gate_h_es: "Hola 👋 Antes de chatear, comparte tus datos:",
    gate_name_en: "Full name", gate_name_es: "Nombre completo",
    gate_email_en: "Email", gate_email_es: "Correo electrónico",
    gate_phone_en: "Phone", gate_phone_es: "Teléfono",
    gate_btn_en: "Start chat", gate_btn_es: "Comenzar el chat",
    gate_note_en: "By submitting you agree to receive SMS or emails from ABI. Rates may apply.",
    gate_note_es: "Al enviar aceptas recibir SMS o emails de ABI. Pueden aplicar tarifas.",
    err_en: "Give me one sec — my line dropped. If it doesn't come back, call our Manhattan campus at (212) 290-2289 (English) / (212) 290-0278 (Spanish) or Bronx at (718) 676-0640. We're here 8 AM–8 PM weekdays.",
    err_es: "Dame un segundo — se cortó mi línea. Si no vuelve, llama al campus de Manhattan al (212) 290-2289 (inglés) / (212) 290-0278 (español) o al Bronx al (718) 676-0640. Estamos aquí 8 AM–8 PM entre semana."
  };
  function t(k) { return UI[k + (pageLangIsES ? "_es" : "_en")]; }

  // ── Widget DOM ────────────────────────────────────────────────────────
  var wrap = document.createElement("div");
  wrap.className = "abibot";
  wrap.innerHTML =
    '<button class="abibot-fab" aria-label="' + t("open") + '">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12a8.5 8.5 0 0 1-8.5 8.5c-1.6 0-3-.4-4.3-1L3 21l1.6-4.8A8.5 8.5 0 1 1 21 12z"/></svg>' +
      '<span class="abibot-fab-badge">AI</span>' +
      '<span class="abibot-fab-label">' + t("fab") + '</span></button>' +
    '<div class="abibot-panel" role="dialog" aria-label="ABI assistant" hidden>' +
      '<div class="abibot-head"><span class="abibot-ava">A</span>' +
        '<div><b>' + t("title") + '</b><span>' + t("status") + '</span></div>' +
        '<button class="abibot-close" aria-label="' + t("close") + '">✕</button></div>' +
      '<div class="abibot-log" aria-live="polite"></div>' +
      '<div class="abibot-chips"></div>' +
      '<form class="abibot-input"><input type="text" autocomplete="off" placeholder="' + t("ph") + '" aria-label="Message"><button type="submit" aria-label="Send"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 11l18-8-8 18-2-7-8-3z"/></svg></button></form>' +
    '</div>';
  document.body.appendChild(wrap);

  var fab = wrap.querySelector(".abibot-fab");
  var panel = wrap.querySelector(".abibot-panel");
  var log = wrap.querySelector(".abibot-log");
  var chipsEl = wrap.querySelector(".abibot-chips");
  chipsEl.style.display = "none"; // guided flow — no chips
  var form = wrap.querySelector(".abibot-input");
  var input = form.querySelector("input");
  var historyLog = [];
  var opened = false;

  function scroll() { log.scrollTop = log.scrollHeight; }
  function add(role, text) {
    var b = document.createElement("div");
    b.className = "abibot-msg abibot-" + role;
    b.textContent = text;
    log.appendChild(b); scroll();
    return b;
  }
  function typing() {
    var t2 = document.createElement("div");
    t2.className = "abibot-msg abibot-bot abibot-typing";
    t2.innerHTML = "<span></span><span></span><span></span>";
    log.appendChild(t2); scroll();
    return t2;
  }

  function send(userText) {
    var q = (userText || "").trim();
    if (!q) return;
    add("user", q);
    historyLog.push({ role: "user", text: q });
    input.value = "";

    // Per-message language detection (only before preferred_language is locked)
    if (!contact.preferred_language) {
      contact.preferred_language = detectES(q) ? "es" : "en";
      sset("abibot-lang", contact.preferred_language);
    }

    // If we still don't have a campus, try to infer from the user's message
    if (!contact.location) {
      if (/bronx/i.test(q)) { contact.location = "Bronx"; sset("abibot-location", "Bronx"); }
      else if (/manhattan|midtown|39th|west 39/i.test(q)) { contact.location = "Manhattan"; sset("abibot-location", "Manhattan"); }
    }

    var tip = typing();
    var bubble = null;

    var onDelta = function (partial) {
      if (!bubble) { tip.remove(); bubble = add("bot", ""); }
      // strip markers live so user never sees them
      bubble.textContent = partial.replace(/\[ACTION:[^\]]+\]/gi, "").trim();
      scroll();
    };

    askAIStream(historyLog, q, onDelta)
      .then(function (final) {
        var raw = typeof final === "string" ? final : (bubble ? bubble.textContent : "");
        var cleaned = processActionMarkers(raw);
        if (!bubble) { try { tip.remove(); } catch (e) {} bubble = add("bot", ""); }
        if (cleaned) bubble.textContent = cleaned;
        historyLog.push({ role: "assistant", text: cleaned });
        scroll();
      })
      .catch(function () {
        try { tip.remove(); } catch (e) {}
        var fallback = contact.preferred_language === "es" ? UI.err_es : UI.err_en;
        if (!bubble) bubble = add("bot", "");
        bubble.textContent = fallback;
        historyLog.push({ role: "assistant", text: fallback });
      });
  }

  // ── Contact gate ──────────────────────────────────────────────────────
  var contactSubmitted = false;
  try { contactSubmitted = !!sessionStorage.getItem("abibot-contact"); } catch (e) {}

  function renderContactGate() {
    var b = document.createElement("div");
    b.className = "abibot-gate";
    b.innerHTML =
      '<p class="abibot-gate-h">' + t("gate_h") + '</p>' +
      '<form class="abibot-gate-form" novalidate>' +
        '<input type="text" name="name" required placeholder="' + t("gate_name") + '" autocomplete="name">' +
        '<input type="email" name="email" required placeholder="' + t("gate_email") + '" autocomplete="email">' +
        '<input type="tel" name="phone" required placeholder="' + t("gate_phone") + '" autocomplete="tel">' +
        '<button type="submit" class="abibot-gate-btn">' + t("gate_btn") + '</button>' +
        '<p class="abibot-gate-note">' + t("gate_note") + '</p>' +
      '</form>';
    log.appendChild(b);
    var gf = b.querySelector("form");
    gf.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = {
        name: gf.name.value.trim(),
        email: gf.email.value.trim(),
        phone: gf.phone.value.trim(),
        ts: new Date().toISOString(),
        page: location.pathname,
        location: contact.location || "",
        customer_status: contact.customer_status || "New Lead"
      };
      if (!data.name || !data.email || !data.phone) return;
      try { sessionStorage.setItem("abibot-contact", JSON.stringify(data)); } catch (e) {}
      contact.first_name = (data.name.split(/\s+/)[0] || "").trim();
      contact.email = data.email;
      contact.phone = data.phone;
      contactSubmitted = true;
      // Fire a lead-captured action so downstream integrations can pick this up
      fireAction("lead_captured", { name: data.name, email: data.email, phone: data.phone });
      b.remove();
      form.style.display = "";
      startChat();
    });
  }

  function startChat() {
    if (opened) return;
    opened = true;
    // Pre-canned opening (matches client script), then AI drives.
    var opener;
    if (!contact.location) {
      opener = campusAskOpening();
    } else if (contact.customer_status === "No Show") {
      opener = taskBOpening(contact.first_name);
    } else {
      opener = taskAOpening(contact.first_name);
    }
    add("bot", opener);
    historyLog.push({ role: "assistant", text: opener });
    setTimeout(function () { input.focus(); }, 120);
  }

  function open() {
    panel.hidden = false;
    fab.classList.add("is-open");
    if (!contactSubmitted) {
      form.style.display = "none";
      if (!log.querySelector(".abibot-gate")) renderContactGate();
    } else {
      form.style.display = "";
      startChat();
    }
  }
  function close() { panel.hidden = true; fab.classList.remove("is-open"); }

  fab.addEventListener("click", function () { panel.hidden ? open() : close(); });
  wrap.querySelector(".abibot-close").addEventListener("click", close);
  form.addEventListener("submit", function (e) { e.preventDefault(); send(input.value); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });

  // Proactive nudge after 6s (once per session, unless closed/opted-out)
  try {
    if (!sessionStorage.getItem("abibot-nudged") && !sessionStorage.getItem("abibot-closed")) {
      setTimeout(function () {
        if (panel.hidden) { fab.classList.add("abibot-nudge"); sessionStorage.setItem("abibot-nudged", "1"); }
      }, 6000);
    }
  } catch (e) {}
})();
