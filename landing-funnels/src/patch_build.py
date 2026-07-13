import re

with open('build.py', 'r') as f:
    content = f.read()

# 1. Replace campus_switch
campus_switch_pattern = r'''    campus_switch = \(\s*'<div class="seg seg-campus" role="group".*?\) % \([^)]*\)'''
content = re.sub(campus_switch_pattern, '    campus_switch = ""', content, flags=re.DOTALL)

# 2. Replace ubar_calls and mstrip_phones
ubar_pattern = r'''    ubar_calls = \(\s*'<a class="ubar-call ubar-call--admis".*?\) % \(mphone_svg, mphone_svg, mphone_svg\)'''
new_ubar = '''    if is_manhattan:
        ubar_calls = (
            '<a class="ubar-call ubar-call--admis" href="tel:+12122902289"><span class="ubar-ico" aria-hidden="true">%s</span>'
            '<span class="ubar-tag">English</span><span class="ubar-num">(212) 290-2289</span></a>'
            '<a class="ubar-call ubar-call--es" href="tel:+12122900278"><span class="ubar-ico" aria-hidden="true">ES</span>'
            '<span class="ubar-tag">Spanish</span><span class="ubar-num">(212) 290-0278</span></a>'
        ) % (phone_svg,)
        mstrip_phones = (
            '<a class="mstrip-phone" href="tel:+12122902289">%s<span class="mstrip-t"><b>(212) 290-2289</b><i>English</i></span></a>'
            '<a class="mstrip-phone" href="tel:+12122900278">%s<span class="mstrip-t"><b>(212) 290-0278</b><i>Spanish</i></span></a>'
        ) % (mphone_svg, mphone_svg)
    else:
        ubar_calls = (
            '<a class="ubar-call ubar-call--bx" href="tel:+17186760640"><span class="ubar-ico" aria-hidden="true">%s</span>'
            '<span class="ubar-tag">Bronx</span><span class="ubar-num">(718) 676-0640</span></a>'
        ) % (phone_svg,)
        mstrip_phones = (
            '<a class="mstrip-phone" href="tel:+17186760640">%s<span class="mstrip-t"><b>(718) 676-0640</b><i>Bronx</i></span></a>'
        ) % (mphone_svg,)'''
content = re.sub(ubar_pattern, new_ubar, content, flags=re.DOTALL)

# 3. Replace hero and lead_form functions
hero_pattern = r'''# ── HERO ─────────────────────────────────────────────────────────────.*?def lead_form\(p\):.*?    \) % \{.*?\}'''

new_hero = '''# ── HERO ─────────────────────────────────────────────────────────────
def hero(p):
    lang = p["lang"]; es = lang == "es"
    is_bx = p["campus"]["slug"] == "bronx"
    ghl_id = "2FvHzLvYji1iSmNmCP46" if not is_bx else "v1SNzWsAZZVodCsnsDbe"
    ghl_h = 734 if not is_bx else 794
    ghl_name = "02.GET TRAINED WITH ABI FORM -  Manhattan " if not is_bx else "02.GET TRAINED WITH ABI FORM - Bronx"
    
    # Text from home page hero
    h1 = '500 Hours. <span>Barber Program.</span> <em>Start Today.</em>'
    sub = 'Become a licensed Master Barber in New York in as little as 4 months. Train hands-on with real clients, get full State Board Exam prep, and land your first chair with our job-placement help.'
    if es:
        h1 = '500 Horas. <span>Programa de Barbería.</span> <em>Empieza Hoy.</em>'
        sub = 'Conviértete en un Barbero Maestro con licencia en Nueva York en solo 4 meses. Entrena en forma práctica con clientes reales, obtén preparación completa para el Examen de la Junta Estatal, y consigue tu primera silla con nuestra ayuda de colocación laboral.'
    
    why_title = 'Why Train at ABI?' if not es else '¿Por qué estudiar en ABI?'
    why_sub = 'Everything you need to go from beginner to licensed professional.' if not es else 'Todo lo que necesitas para pasar de principiante a profesional con licencia.'
    
    feats = [
        ('Fits your life — day, evening & weekend tracks' if not es else 'Se adapta a tu vida — clases de día, tarde y fines de semana', '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'),
        ('Hands-on training on real clients from your first weeks' if not es else 'Entrenamiento práctico con clientes reales desde las primeras semanas', '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1M12 18v4M8 22h8"/></svg>'),
        ('Funding that fits — ACCES-VR, GI Bill®, weekly plans|Figure out what works for your budget' if not es else 'Financiamiento a tu medida — ACCES-VR, GI Bill®, planes semanales|Descubre lo que funciona para tu presupuesto', '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="6" r="3.4"/><path d="M12 4.6v2.8M10.9 5.4h2.2"/><path d="M3 15.5c2-1.6 4-1.6 5.6-.6l3 1.8c.9.6.9 1.9-.2 2.2H8M11.4 18.9l5.2.1c2 0 3.4-.9 4.4-2.3"/></svg>'),
        ('Career support & job-placement help when you graduate' if not es else 'Apoyo profesional y ayuda para encontrar empleo al graduarte', '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2M2 13h20"/></svg>'),
        ('Two NYC campuses — Manhattan and the Bronx' if not es else 'Dos sedes en NYC — Manhattan y el Bronx', '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 21v-4h6v4M8 7h2M14 7h2M8 11h2M14 11h2"/></svg>')
    ]
    
    feats_html = ""
    for txt, svg in feats:
        if "|" in txt:
            main, sub_ = txt.split("|", 1)
            feats_html += f\'\'\'            <div class="hx-featbox-item">
              {svg}
              <span>
                <b>{main}</b>
                <i>{sub_}</i>
              </span>
            </div>\'\'\'
        else:
            feats_html += f\'\'\'            <div class="hx-featbox-item">
              {svg}
              <span>{txt}</span>
            </div>\'\'\'

    form_title = "Reserve Your Spot Today" if not es else "Reserva Tu Lugar Hoy"
    form_sub = "Fill out the form and an Admissions Advisor will contact you.<br><i>Kindly fill out the form to receive a call from one of AI Agents</i>" if not es else "Completa el formulario y un asesor de admisiones te contactará.<br><i>Por favor, completa el formulario para recibir una llamada de nuestros Agentes de IA</i>"

    html = f\'\'\'<section class="hx reveal">
  <div class="hx-in">
    <div class="hx-copy">
      <h1 class="hx-h1">{h1}</h1>
      <p class="hx-sub">{sub}</p>
      
      <div class="hx-featbox">
        <div class="hx-featbox-head">
          <div class="hx-featbox-title">{why_title}</div>
          <p>{why_sub}</p>
        </div>
        <div class="hx-featbox-grid">
          <div class="hx-featbox-col">
{feats_html}
          </div>
        </div>
      </div>
    </div>
    <div class="formcard" id="reserve">
      <div class="formcard-head">
        <div class="formcard-ico"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c0-3.6 3.1-6 7-6s7 2.4 7 6"/></svg></div>
        <div>
          <div class="formcard-title">{form_title}</div>
          <div class="formcard-sub">{form_sub}</div>
        </div>
      </div>
      <div class="ghl-form-wrap">
      <iframe
        src="https://api.leadconnectorhq.com/widget/form/{ghl_id}"
        style="width:100%;height:100%;border:none;border-radius:3px"
        id="inline-{ghl_id}"
        data-layout="{{'id':'INLINE'}}"
        data-trigger-type="alwaysShow"
        data-trigger-value=""
        data-activation-type="alwaysActivated"
        data-activation-value=""
        data-deactivation-type="neverDeactivate"
        data-deactivation-value=""
        data-form-name="{ghl_name}"
        data-height="{ghl_h}"
        data-layout-iframe-id="inline-{ghl_id}"
        data-form-id="{ghl_id}"
        title="{ghl_name}"></iframe>
    </div>
    <script src="https://link.msgsndr.com/js/form_embed.js"></script>
    </div>
  </div>
</section>\'\'\'
    return html

def lead_form(p):
    return ""
'''
content = re.sub(hero_pattern, new_hero, content, flags=re.DOTALL)

with open('build.py', 'w') as f:
    f.write(content)

print("Patched build.py")
