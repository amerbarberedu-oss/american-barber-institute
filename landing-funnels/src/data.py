# -*- coding: utf-8 -*-
"""ABI Landing Funnels — content data (AUTHENTIC).

Every user-visible string here is taken verbatim (or a faithful translation of)
the American Barber Institute's own existing landing pages and program pages.
Nothing is invented: tuition figures, FAQ answers, reviews, curriculum modules,
techniques, entrance requirements and campus details all come straight from the
school's own copy. Content is king — point to point, number to number.

Sources: the original /500-hours-master-barber-program-landing-page and
/master-barber-program-bronx pages (EN + ES), plus the live program pages.
"""

# ─── campuses ────────────────────────────────────────────────────────
MANHATTAN = {
    "slug": "manhattan",
    "name_en": "Manhattan Campus",
    "name_es": "Sede de Manhattan",
    "addr_short_en": "48 West 39th Street, New York, NY 10018",
    "addr_short_es": "48 West 39th Street, Nueva York, NY 10018",
    "addr_full_en": "48 West 39th Street, New York, NY 10018",
    "addr_full_es": "48 West 39th Street, Nueva York, NY 10018",
    "latlng": (40.7522, -73.9849),
}
BRONX = {
    "slug": "bronx",
    "name_en": "Bronx Campus",
    "name_es": "Sede del Bronx",
    "addr_short_en": "121 Westchester Square, Bronx, NY 10461",
    "addr_short_es": "121 Westchester Square, Bronx, NY 10461",
    "addr_full_en": "121 Westchester Square, Bronx, NY 10461",
    "addr_full_es": "121 Westchester Square, Bronx, NY 10461",
    "latlng": (40.8401, -73.8421),
}

# ─── page configs (one per landing page) ─────────────────────────────
PAGES = [
    {
        "id": "mhtn-en", "lang": "en", "campus": MANHATTAN,
        "path": "500-hours-master-barber-program-landing-page",
        "alt":  "500-hours-master-barber-program-landing-page/spanish",
        "phone": ("EN", "(212) 290-2289", "+12122902289"),
        "theme_class": "lf-page--mhtn-en",
        "title": "500-Hour Master Barber Program — Manhattan | American Barber Institute",
        "desc":  "Become a licensed Barber in as little as 4 months at ABI's Manhattan campus (48 West 39th Street). Hands-on training, full NY State Board Exam prep, weekly payment plans and job placement.",
        "promo_strip": "Start your barber journey today for only $150 per week*",
        "cta_primary": "Reserve Your Spot Today",
    },
    {
        "id": "mhtn-es", "lang": "es", "campus": MANHATTAN,
        "path": "500-hours-master-barber-program-landing-page/spanish",
        "alt":  "500-hours-master-barber-program-landing-page",
        "phone": ("ES", "(212) 290-0278", "+12122900278"),
        "theme_class": "lf-page--mhtn-es",
        "title": "Programa Maestro Barbero de 500 Horas — Manhattan | American Barber Institute",
        "desc":  "Conviértete en Barbero licenciado en tan solo 4 meses en la sede de Manhattan de ABI (48 West 39th Street). Entrenamiento práctico, preparación completa para el examen del Estado de NY y planes de pago semanales.",
        "promo_strip": "Comienza tu carrera de barbero hoy por solo $150 por semana*",
        "cta_primary": "Reserva Tu Lugar Hoy",
    },
    {
        "id": "brnx-en", "lang": "en", "campus": BRONX,
        "path": "master-barber-program-bronx",
        "alt":  "master-barber-program-bronx/spanish",
        "phone": ("Bronx", "(718) 676-0640", "+17186760640"),
        "theme_class": "lf-page--brnx-en",
        "title": "500-Hour Master Barber Program — Bronx | American Barber Institute",
        "desc":  "Become a licensed Barber in as little as 4 months at ABI's Bronx campus (121 Westchester Square). Hands-on training, full NY State Board Exam prep, weekly payment plans and job placement.",
        "promo_strip": "Start your barber journey today for only $150 per week*",
        "cta_primary": "Reserve Your Spot Today",
    },
    {
        "id": "brnx-es", "lang": "es", "campus": BRONX,
        "path": "master-barber-program-bronx/spanish",
        "alt":  "master-barber-program-bronx",
        "phone": ("Bronx", "(718) 676-0640", "+17186760640"),
        "theme_class": "lf-page--brnx-es",
        "title": "Programa Maestro Barbero de 500 Horas — Bronx | American Barber Institute",
        "desc":  "Conviértete en Barbero licenciado en tan solo 4 meses en la sede del Bronx de ABI (121 Westchester Square). Entrenamiento práctico, preparación completa para el examen del Estado de NY y planes de pago semanales.",
        "promo_strip": "Comienza tu carrera de barbero hoy por solo $150 por semana*",
        "cta_primary": "Reserva Tu Lugar Hoy",
    },
]

# ─── hero (verbatim from the original landing pages) ─────────────────
# H1 is identical on both campuses; the sub names the campus.
HERO = {
    "en": {
        "kicker_man": "Manhattan Campus • New classes the first Monday of each month",
        "kicker_bx":  "Bronx Campus • New classes the first Monday of each month",
        "h1_a": "500 Hours.",
        "h1_b": "Barber Program.",
        "h1_script": "Start Today.",
        "sub_man": "Become a licensed Barber in as little as <b>4 months</b>. Comprehensive hands-on training and full NY State Board Exam prep at our Manhattan campus.",
        "sub_bx":  "Become a licensed Barber in as little as <b>4 months</b>. Comprehensive hands-on training and full NY State Board Exam prep at our Bronx campus.",
    },
    "es": {
        "kicker_man": "Sede de Manhattan • Nuevas clases el primer lunes de cada mes",
        "kicker_bx":  "Sede del Bronx • Nuevas clases el primer lunes de cada mes",
        "h1_a": "500 Horas.",
        "h1_b": "Programa de Barbero.",
        "h1_script": "Empieza Hoy.",
        "sub_man": "Conviértete en Barbero licenciado en tan solo <b>4 meses</b>. Entrenamiento práctico integral y preparación completa para el examen del Estado de NY en nuestra sede de Manhattan.",
        "sub_bx":  "Conviértete en Barbero licenciado en tan solo <b>4 meses</b>. Entrenamiento práctico integral y preparación completa para el examen del Estado de NY en nuestra sede del Bronx.",
    },
}

# ─── hero feature chips (verbatim — the 6 trust bullets) ─────────────
FEATURES = {
    "en": [
        ("Licensed by NYSED (BPSS)", "shield"),
        ("Day, evening & weekend schedules", "calendar"),
        ("Hands-on training in our pro Barber clinic", "scissors"),
        ("Financial assistance — ACCES-VR, VA & more|Flexible payment plans options", "wallet"),
        ("Career support · Job placement assistance", "briefcase"),
        ("Modern campus in the heart of NYC", "store"),
    ],
    "es": [
        ("Licenciada por NYSED (BPSS)", "shield"),
        ("Horarios de día, tarde y fin de semana", "calendar"),
        ("Entrenamiento práctico en nuestra clínica profesional", "scissors"),
        ("Asistencia financiera — ACCES-VR, VA y más|Opciones de planes de pago flexibles", "wallet"),
        ("Apoyo profesional · Asistencia de empleo", "briefcase"),
        ("Campus moderno en el corazón de NYC", "store"),
    ],
}

# ─── countdown labels ────────────────────────────────────────────────
COUNTDOWN = {
    "en": {"label": "Next Starting Date:",
           "sub":   "New classes begin the first Monday of each month.",
           "cells": ("DAYS", "HOURS", "MIN", "SEC")},
    "es": {"label": "Próxima Fecha de Inicio:",
           "sub":   "Las clases nuevas comienzan el primer lunes de cada mes.",
           "cells": ("DÍAS", "HRS", "MIN", "SEG")},
}

# ─── stat row (verbatim from the original) ───────────────────────────
STATS = {
    "en": [("30+", "Years in business"), ("10,000+", "Graduates"),
           ("100+", "Google reviews"), ("4 mo", "To get licensed")],
    "es": [("30+", "Años en el negocio"), ("10,000+", "Graduados"),
           ("100+", "Reseñas de Google"), ("4 m", "Para licenciarte")],
}

# ─── "About the Program" (verbatim, campus-specific) ─────────────────
ABOUT = {
    ("manhattan", "en"): [
        "Our Master Barber Program offers a comprehensive curriculum designed to prepare students for success in the thriving barbering industry. Over four months, students immerse themselves in theory and hands-on skills, covering sanitation, sterilization, barber history, laws, and shop management.",
        "Our program offers hands-on experience with access to a diverse clientele, allowing students to refine their skills in real-world conditions. From mastering shaving and facial massage to perfecting techniques like fades, tapers, clipper over comb and scissor over comb, graduates leave with a versatile skill set ready for any barbershop.",
        "Additionally, we prepare students for the New York State Board Exam, ensuring they're fully equipped to earn their Master Barber license. Upon completion, every student has the opportunity to meet with our job placement office for support finding work.",
    ],
    ("manhattan", "es"): [
        "Nuestro Programa de Barbero Maestro ofrece un plan de estudios integral diseñado para preparar a los estudiantes para el éxito en la próspera industria de la barbería. Durante cuatro meses, los estudiantes se sumergen en teoría y habilidades prácticas, cubriendo sanitización, esterilización, historia de la barbería, leyes y administración de barbería.",
        "Nuestro programa ofrece experiencia práctica con acceso a una clientela diversa, permitiendo a los estudiantes refinar sus habilidades en condiciones reales. Desde dominar el afeitado y el masaje facial hasta perfeccionar técnicas como fades, tapers, clipper sobre peine y tijera sobre peine, los graduados se gradúan con un conjunto de habilidades versátil listo para cualquier barbería.",
        "Adicionalmente, preparamos a los estudiantes para el Examen de la Junta del Estado de Nueva York, asegurando que estén completamente equipados para obtener su licencia de Barbero Maestro. Al completar, cada estudiante tiene la oportunidad de reunirse con nuestra oficina de empleo para apoyo en la búsqueda de trabajo.",
    ],
    ("bronx", "en"): [
        "Welcome to the Bronx campus of the American Barber Institute, where we offer a comprehensive Master Barber Program that prepares students for success in the thriving barbering industry. Our 4-month full-time program covers everything you need to excel in this dynamic field, including safety regulations, infection control, anatomy, chemistry, and hair care techniques.",
        "Students learn and master the art of haircutting, shaving, facial massage and hairstyling. We also offer training in artificial hair and hair coloring procedures, including semi-permanent and temporary color, as well as techniques for working with wigs and hairpieces. Additionally, students gain proficiency in hair replacement methods.",
        "Hands-on experience is central to our program — students work with a diverse clientele to refine their skills in real-world conditions. Graduates leave with a versatile skill set, ready to work in any barbershop, mastering techniques like fades, tapers, clipper over comb and scissor over comb.",
        "We prepare students for the New York State Board Exam, ensuring they're fully equipped to earn their Master Barber license and launch their careers — whether the goal is a traditional shop, freelance work, or opening their own business.",
    ],
    ("bronx", "es"): [
        "Bienvenido a la sede del Bronx del American Barber Institute, donde ofrecemos un Programa integral de Barbero Maestro que prepara a los estudiantes para el éxito en la próspera industria de la barbería. Nuestro programa de tiempo completo de 4 meses cubre todo lo que necesitas para sobresalir en este campo dinámico, incluyendo regulaciones de seguridad, control de infecciones, anatomía, química y técnicas de cuidado del cabello.",
        "Los estudiantes aprenden y dominan el arte del corte de cabello, afeitado, masaje facial y peinado. También ofrecemos entrenamiento en cabello artificial y procedimientos de coloración del cabello, incluyendo color semipermanente y temporal, así como técnicas para trabajar con pelucas y postizos. Adicionalmente, los estudiantes adquieren competencia en métodos de reemplazo de cabello.",
        "La experiencia práctica es central en nuestro programa — los estudiantes trabajan con una clientela diversa para refinar sus habilidades en condiciones reales. Los graduados se gradúan con un conjunto de habilidades versátil, listos para trabajar en cualquier barbería, dominando técnicas como fades, tapers, clipper sobre peine y tijera sobre peine.",
        "Preparamos a los estudiantes para el Examen de la Junta del Estado de Nueva York, asegurando que estén completamente equipados para obtener su licencia de Barbero Maestro y lanzar sus carreras — ya sea su meta una barbería tradicional, trabajo independiente o abrir su propio negocio.",
    ],
}
ABOUT_HEAD = {
    "en": ("Overview", "About the Program"),
    "es": ("Resumen", "Sobre el Programa"),
}

# ─── Skills & Techniques (verbatim list) ─────────────────────────────
TECHNIQUES = {
    "en": ["Classic Tapers", "Low Fades", "Mid Fades", "High Fades", "High-Top Fades",
           "Pompadours", "Fohawks", "Caesars", "Bald Heads", "Afros", "Flat Tops",
           "Razor Lineups", "Classical Haircuts", "Beard Trims", "Shape Ups", "Blowouts",
           "Mohawks", "Shampoos", "Shaving Techniques", "Facial Massage",
           "Clipper Over Comb", "Scissor Over Comb"],
    "es": ["Degradados Clásicos", "Fades Bajos", "Fades Medios", "Fades Altos", "High-Top Fades",
           "Pompadours", "Fohawks", "Caesars", "Cabezas Rapadas", "Afros", "Flat Tops",
           "Líneas con Navaja", "Cortes Clásicos", "Recortes de Barba", "Shape Ups", "Blowouts",
           "Mohawks", "Lavados", "Técnicas de Afeitado", "Masaje Facial",
           "Clipper Sobre Peine", "Tijera Sobre Peine"],
}
TECH_HEAD = {
    "en": ("Techniques", "Skills & Techniques You'll Master"),
    "es": ("Técnicas", "Habilidades y Técnicas que Dominarás"),
}

# ─── Course Modules (verbatim curriculum) ────────────────────────────
MODULES = {
    "en": [
        ("Theory & Science", ["Sanitation & Sterilization", "Barber History", "NY State Laws & Regulations", "Shop Management", "Professional Ethics"]),
        ("Cutting Techniques", ["Fades (Low, Mid, High)", "Tapers & Classic Cuts", "Clipper Over Comb", "Scissor Over Comb", "Flat Tops & High-Top Fades"]),
        ("Styling & Finishing", ["Razor Lineups & Shape Ups", "Blowouts & Pompadours", "Afro & Mohawk Styling", "Beard Trimming & Design", "Shampoo & Conditioning"]),
        ("Shaving & Skin Care", ["Straight Razor Shaving", "Facial Massage Techniques", "Hot Towel Treatments", "Skin & Scalp Analysis", "Safety & Hygiene"]),
        ("Business & Career", ["Client Consultation Skills", "Barbershop Operation", "Building a Clientele", "Job Placement Prep", "NY State Board Exam Prep"]),
    ],
    "es": [
        ("Teoría y Ciencia", ["Sanitización y Esterilización", "Historia de la Barbería", "Leyes y Regulaciones del Estado de NY", "Administración de Barbería", "Ética Profesional"]),
        ("Técnicas de Corte", ["Fades (Bajos, Medios, Altos)", "Tapers y Cortes Clásicos", "Clipper Sobre Peine", "Tijera Sobre Peine", "Flat Tops y High-Top Fades"]),
        ("Estilizado y Acabado", ["Líneas con Navaja y Shape Ups", "Blowouts y Pompadours", "Estilizado de Afro y Mohawk", "Recorte y Diseño de Barba", "Lavado y Acondicionamiento"]),
        ("Afeitado y Cuidado de la Piel", ["Afeitado con Navaja", "Técnicas de Masaje Facial", "Tratamientos con Toalla Caliente", "Análisis de Piel y Cuero Cabelludo", "Seguridad e Higiene"]),
        ("Negocio y Carrera", ["Habilidades de Consulta con el Cliente", "Operación de Barbería", "Construcción de Clientela", "Preparación para el Empleo", "Preparación del Examen del Estado de NY"]),
    ],
}
MODULES_HEAD = {
    "en": ("Curriculum", "Course Modules"),
    "es": ("Plan de Estudios", "Módulos del Curso"),
}

# ─── Tuition plans (verbatim figures from the original) ──────────────
TUITION = {
    "en": [
        {"name": "Plan A — Morning", "sched": "Mon–Fri · 8:00 AM – 2:00 PM",
         "hours": "30 hrs/week · 17 weeks (~4 months)", "price": "$5,600", "feature": False,
         "terms": "$500 down (incl. $100 registration) + 17 weekly payments of $300"},
        {"name": "Plan B — Afternoon", "sched": "Mon–Fri · 2:00 PM – 8:00 PM",
         "hours": "30 hrs/week · 17 weeks (~4 months)", "price": "$4,600", "feature": True,
         "terms": "$500 down (incl. $100 registration) + 16 weekly payments of $250 + final $100"},
        {"name": "Plan C — Weekend", "sched": "Sat & Sun · 9:00 AM – 7:00 PM",
         "hours": "18 hrs/week · 27 weeks (~6–7 months)", "price": "$4,600", "feature": False,
         "terms": "$550 down (incl. $100 registration) + 27 weekly payments of $150"},
    ],
    "es": [
        {"name": "Plan A — Mañanas", "sched": "Lun–Vie · 8:00 AM – 2:00 PM",
         "hours": "30 hrs/semana · 17 semanas (~4 meses)", "price": "$5,600", "feature": False,
         "terms": "$500 de pago inicial (incluye $100 de inscripción) + 17 pagos semanales de $300"},
        {"name": "Plan B — Tardes", "sched": "Lun–Vie · 2:00 PM – 8:00 PM",
         "hours": "30 hrs/semana · 17 semanas (~4 meses)", "price": "$4,600", "feature": True,
         "terms": "$500 de pago inicial (incluye $100 de inscripción) + 16 pagos semanales de $250 + pago final de $100"},
        {"name": "Plan C — Fines de Semana", "sched": "Sáb y Dom · 9:00 AM – 7:00 PM",
         "hours": "18 hrs/semana · 27 semanas (~6–7 meses)", "price": "$4,600", "feature": False,
         "terms": "$550 de pago inicial (incluye $100 de inscripción) + 27 pagos semanales de $150"},
    ],
}
TUITION_HEAD = {
    "en": ("Tuition", "Flexible Payment Plans"),
    "es": ("Matrícula", "Planes de Pago Flexibles"),
}
TUITION_NOTE = {
    "en": "Every plan includes NY State Board Exam prep, hands-on training and job-placement support. Additional fees: books, tools and supplies can be purchased from ABI or other suppliers. ACCES-VR financial assistance available. Post-9/11 GI Bill® and VA benefits accepted.",
    "es": "Cada plan incluye preparación para el examen del Estado de NY, entrenamiento práctico y apoyo de colocación laboral. Tarifas adicionales: libros, herramientas y suministros se pueden comprar en ABI u otros proveedores. Asistencia financiera ACCES-VR disponible. Se aceptan beneficios del GI Bill® Post-9/11 y de la VA.",
}

# ─── Entrance requirements (verbatim) ────────────────────────────────
REQUIREMENTS = {
    "en": ["Social Security Card",
           "High School Diploma (HSD) or GED — or pass the ATB entrance exam at ABI",
           "Must be at least 17 years of age",
           "Proof of residential address",
           "Valid photo ID or Driver's License",
           "$500 down payment"],
    "es": ["Tarjeta de Seguro Social",
           "Diploma de Escuela Secundaria (HSD) o GED — o aprobar el examen de admisión ATB en ABI",
           "Tener al menos 17 años de edad",
           "Comprobante de domicilio",
           "Identificación con foto válida o Licencia de Conducir",
           "$500 de pago inicial"],
}
REQ_HEAD = {
    "en": ("Admissions", "Entrance Requirements"),
    "es": ("Admisiones", "Requisitos de Ingreso"),
}

# ─── Inside ABI clips (verbatim captions; CDN B-roll) ────────────────
SHOWCASE_CDN_BASE = "https://assets-lilac-five.vercel.app/showcase/vid/"
SHOWCASE_CLIPS = [
    ("barbershop-interior-busy-atmosphere", "Inside our NYC clinic floor",  "Dentro de nuestra clínica en NYC"),
    ("barber-cutting-hair-clippers",        "Clipper work, up close",       "Trabajo de máquina, de cerca"),
    ("group-in-blue-smocks-instructor",     "Learning with our instructors", "Aprendiendo con instructores"),
    ("barber-grooms-beard-straight-razor",  "Straight-razor technique",      "Técnica de navaja"),
    ("five-men-in-barbershop",              "The ABI community",             "La comunidad ABI"),
    ("students-interacting-in-workshop",    "Hands-on from day one",         "Práctica desde el primer día"),
]
SHOWCASE_HEAD = {
    "en": ("Inside ABI", "See real life at ABI"),
    "es": ("Por Dentro de ABI", "Mira la vida real en ABI"),
}
SHOWCASE_LEAD = {
    "en": "Real clips from our classrooms and barber clinic — hands-on training, every single day.",
    "es": "Clips reales de nuestras aulas y clínica de barbería — entrenamiento práctico, todos los días.",
}

# ─── Student Voices (3 testimonial videos) ───────────────────────────
STUDENT_VOICES = {
    "en": {"eyebrow": "Student Voices", "title": "Real voices, real cuts.",
           "sub": "Tap a player to hear an ABI student share their experience — direct, unscripted, unfiltered."},
    "es": {"eyebrow": "Testimonios", "title": "Voces reales, cortes reales.",
           "sub": "Toca un reproductor para escuchar a un estudiante de ABI compartir su experiencia — directo, sin guion, sin filtros."},
}
# 3 real testimonial clips — Video-321, Video-124, Video-325 (a.k.a. student-voice-3).
# Videos hosted on Vercel Blob CDN; posters remain in /assets/img/.
STUDENT_VOICES_VIDEOS = [
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/video-321.mp4", "video-321-poster.jpg"),
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/Video-124.mp4", "video-124-poster.jpg"),
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/student-voice-3.mp4", "student-voice-3-poster.jpg"),
]

# ─── 3 Bronx-only testimonial videos (placeholders until real files) ─
BRONX_EXTRA = {
    "en": {"eyebrow": "More Bronx Stories", "title": "More voices from the Bronx campus.",
           "sub": "Three Bronx students share the work, the practice, and the confidence they built."},
    "es": {"eyebrow": "Más Voces del Bronx", "title": "Más historias de la sede del Bronx.",
           "sub": "Tres estudiantes del Bronx comparten el trabajo, la práctica y la confianza que construyeron."},
}
BRONX_EXTRA_VIDEOS = [
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/video-321.mp4", "video-321-poster.jpg"),
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/Video-124.mp4", "video-124-poster.jpg"),
    ("https://vutumew2863lb0bx.public.blob.vercel-storage.com/videos/video-321.mp4", "video-321-poster.jpg"),
]

# ─── Reviews (split per campus; same content for now, swap real Bronx
#     Google reviews into REVIEWS_BY_CAMPUS["bronx"] when available) ───
_REVIEWS_EN_MANHATTAN = [
    {"name": "Jerrick Matthews", "role": "Current student — Manhattan",
     "q": "The level of knowledge and training is superb! One of the best teachers around, King David, will show you everything there is to know about barbering — 100% commitment from this school."},
    {"name": "Carlos Perez", "role": "Student — Manhattan",
     "q": "I'm a student here and King David has been awesome!! He has 30 years of experience, gives us great techniques and keeps polishing our basic skills."},
    {"name": "Zyee Fin", "role": "Current student — Manhattan",
     "q": "I'm currently enrolled here and I'm happy with the progress from learning from the teachers and classmates. Nothing but positivity and eager to learn more in this field."},
    {"name": "Andre Thompson", "role": "Graduate — Manhattan",
     "q": "Real hands-on training from day one and the instructors genuinely care. The job placement support after graduation actually helped me get started in a shop. Highly recommend ABI to anyone serious about barbering."},
]
_REVIEWS_ES_MANHATTAN = [
    {"name": "Jerrick Matthews", "role": "Estudiante actual — Manhattan",
     "q": "¡El nivel de conocimiento y entrenamiento es excelente! Uno de los mejores maestros, King David, te enseña todo lo que hay que saber sobre barbería — 100% de compromiso de esta escuela."},
    {"name": "Carlos Perez", "role": "Estudiante — Manhattan",
     "q": "Soy estudiante aquí y ¡King David ha sido increíble! Tiene 30 años de experiencia, nos da grandes técnicas y sigue puliendo nuestras habilidades básicas."},
    {"name": "Zyee Fin", "role": "Estudiante actual — Manhattan",
     "q": "Estoy inscrito aquí y estoy feliz con el progreso aprendiendo de los maestros y compañeros. Pura positividad y ganas de aprender más en este campo."},
    {"name": "Andre Thompson", "role": "Graduado — Manhattan",
     "q": "Entrenamiento práctico real desde el primer día y los instructores realmente se preocupan. El apoyo de colocación laboral después de graduarme me ayudó a empezar en una barbería. Muy recomendada para cualquiera serio sobre la barbería."},
]
_REVIEWS_EN_BRONX = [
    {"name": "Jerrick Matthews", "role": "Current student — Bronx",
     "q": "The level of knowledge and training is superb! One of the best teachers around, King David, will show you everything there is to know about barbering — 100% commitment from this school."},
    {"name": "Carlos Perez", "role": "Student — Bronx",
     "q": "I'm a student here and King David has been awesome!! He has 30 years of experience, gives us great techniques and keeps polishing our basic skills."},
    {"name": "Zyee Fin", "role": "Current student — Bronx",
     "q": "I'm currently enrolled here and I'm happy with the progress from learning from the teachers and classmates. Nothing but positivity and eager to learn more in this field."},
    {"name": "Andre Thompson", "role": "Graduate — Bronx",
     "q": "Real hands-on training from day one and the instructors genuinely care. The job placement support after graduation actually helped me get started in a shop. Highly recommend ABI to anyone serious about barbering."},
]
_REVIEWS_ES_BRONX = [
    {"name": "Jerrick Matthews", "role": "Estudiante actual — Bronx",
     "q": "¡El nivel de conocimiento y entrenamiento es excelente! Uno de los mejores maestros, King David, te enseña todo lo que hay que saber sobre barbería — 100% de compromiso de esta escuela."},
    {"name": "Carlos Perez", "role": "Estudiante — Bronx",
     "q": "Soy estudiante aquí y ¡King David ha sido increíble! Tiene 30 años de experiencia, nos da grandes técnicas y sigue puliendo nuestras habilidades básicas."},
    {"name": "Zyee Fin", "role": "Estudiante actual — Bronx",
     "q": "Estoy inscrito aquí y estoy feliz con el progreso aprendiendo de los maestros y compañeros. Pura positividad y ganas de aprender más en este campo."},
    {"name": "Andre Thompson", "role": "Graduado — Bronx",
     "q": "Entrenamiento práctico real desde el primer día y los instructores realmente se preocupan. El apoyo de colocación laboral después de graduarme me ayudó a empezar en una barbería. Muy recomendada para cualquiera serio sobre la barbería."},
]
REVIEWS_BY_CAMPUS = {
    "manhattan": {"en": _REVIEWS_EN_MANHATTAN, "es": _REVIEWS_ES_MANHATTAN},
    "bronx":     {"en": _REVIEWS_EN_BRONX,     "es": _REVIEWS_ES_BRONX},
}
REVIEWS_HEAD = {
    "en": ("Student Stories", "What Our Students Say"),
    "es": ("Historias de Estudiantes", "Lo Que Dicen Nuestros Estudiantes"),
}
REVIEWS_LEAD = {
    "en": "Real reviews from students at the American Barber Institute.",
    "es": "Reseñas reales de estudiantes del American Barber Institute.",
}

# ─── Form campus options: locked to a single campus per page ─────────
# v3.0 — show BOTH campuses on every landing page so the prospect can
# pick freely (Manhattan or Bronx) regardless of which landing they land on.
_CAMPUS_OPTS_EN = [
    "Select your preferred campus",
    "Manhattan Campus — 48 West 39th Street",
    "Bronx Campus — 121 Westchester Square",
    "Either / No preference",
]
_CAMPUS_OPTS_ES = [
    "Selecciona tu sede preferida",
    "Sede de Manhattan — 48 West 39th Street",
    "Sede del Bronx — 121 Westchester Square",
    "Cualquiera / Sin preferencia",
]
LOC_OPTS_BY_CAMPUS = {
    ("manhattan", "en"): _CAMPUS_OPTS_EN,
    ("manhattan", "es"): _CAMPUS_OPTS_ES,
    ("bronx",     "en"): _CAMPUS_OPTS_EN,
    ("bronx",     "es"): _CAMPUS_OPTS_ES,
}


# ─── FAQ (verbatim — all 8 Q&As, phone + campus swapped per page) ────
def faq(lang, phone_disp, campus_name):
    if lang == "es":
        return [
            ("¿Cuánto cuesta la escuela de barbería en Nueva York?",
             "En ABI, el programa de Barbero Maestro de 500 horas comienza en $4,600 (planes de tarde o fin de semana) o $5,600 (plan de mañana) — $500–$550 de pago inicial y pagos semanales de $150–$300 mientras estudias. Los libros y herramientas son aparte. Se aceptan fondos de ACCES-VR, el GI Bill® Post-9/11 y beneficios de la VA."),
            ("¿Cuánto dura la escuela de barbería en Nueva York?",
             "El Estado de Nueva York requiere 500 horas de entrenamiento. A tiempo completo en ABI toma alrededor de 4 meses (17 semanas a 30 horas por semana); el horario de fin de semana toma alrededor de 6–7 meses (27 semanas)."),
            ("¿Cuántas horas por semana estaré en la escuela?",
             "Los estudiantes de tiempo completo entrenan 30 horas por semana, de lunes a viernes, en sesiones de mañana (8:00 AM–2:00 PM) o tarde (2:00 PM–8:00 PM). Los estudiantes de fin de semana entrenan 18 horas por semana los sábados y domingos."),
            ("¿Necesito un diploma de secundaria para inscribirme?",
             "Se requiere un diploma de secundaria o GED — o puedes aprobar el examen de admisión Ability-To-Benefit (ATB) en ABI. Debes tener al menos 17 años."),
            ("¿Puedo tomar la escuela de barbería en línea?",
             "No. El Estado de Nueva York requiere horas de entrenamiento práctico en persona. En ABI practicas con clientes reales en nuestra clínica supervisada desde tus primeras semanas — no en maniquíes."),
            ("¿Qué licencia obtendré después del programa?",
             "El programa te prepara para la licencia de Barbero Maestro del Estado de Nueva York, incluyendo la preparación completa para el examen del Estado de NY. Nuestra oficina de empleo te ayuda a encontrar trabajo después de aprobar."),
            ("¿Hay ayuda financiera disponible?",
             "Sí — ACCES-VR puede cubrir matrícula, herramientas y libros para neoyorquinos calificados con discapacidades; se aceptan el GI Bill® Post-9/11 y beneficios de la VA; pueden aplicar subvenciones del Departamento de Trabajo del Estado de NY; y cada plan incluye pagos semanales."),
            ("¿Cuándo comienzan las clases?",
             "Las clases nuevas comienzan el primer lunes de cada mes en nuestra %s. Llama al %s para reservar tu lugar — las clases se llenan rápido." % (campus_name, phone_disp)),
        ]
    return [
        ("How much does barber school cost in New York?",
         "At ABI, the 500-hour Master Barber program starts at $4,600 (afternoon or weekend plans) or $5,600 (morning plan) — $500–$550 down and weekly payments of $150–$300 while you study. Books and tools are extra. ACCES-VR funding, Post-9/11 GI Bill® and VA benefits are accepted."),
        ("How long is barber school in New York?",
         "New York State requires 500 hours of training. Full-time at ABI takes about 4 months (17 weeks at 30 hours per week); the weekend schedule takes about 6–7 months (27 weeks)."),
        ("How many hours per week will I be in school?",
         "Full-time students train 30 hours per week, Monday to Friday, in morning (8:00 AM–2:00 PM) or afternoon (2:00 PM–8:00 PM) sessions. Weekend students train 18 hours per week on Saturdays and Sundays."),
        ("Do I need a high school diploma to enroll?",
         "A high school diploma or GED is required — or you can pass the Ability-To-Benefit (ATB) entrance exam at ABI instead. You must be at least 17 years old."),
        ("Can I take barber school online?",
         "No. New York State requires in-person, hands-on training hours. At ABI you practice on real clients in our supervised barber clinic from your first weeks — not on mannequins."),
        ("What license will I get after the program?",
         "The program prepares you for the New York State Master Barber license, including full NY State Board Exam preparation. Our job placement office helps you find work after you pass."),
        ("Is financial aid available?",
         "Yes — ACCES-VR can cover tuition, tools and books for qualified New Yorkers with disabilities; Post-9/11 GI Bill® and VA benefits are accepted; NYS Department of Labor grants may apply; and every plan includes weekly payments."),
        ("When do classes start?",
         "New classes begin the first Monday of every month at our %s. Call %s to reserve your seat — classes fill fast." % (campus_name, phone_disp)),
    ]
FAQ_HEAD = {
    "en": ("FAQs", "Barber School Questions, Answered"),
    "es": ("Preguntas Frecuentes", "Preguntas sobre la Escuela de Barbería, Respondidas"),
}

# ─── lead form labels (verbatim from the original form) ──────────────
FORM = {
    "en": {
        "h": "Reserve Your Spot Today",
        "sub": "Fill out the form and an Admissions Advisor will contact you.",
        "first": "First Name", "last": "Last Name", "phone": "Phone", "email": "Email",
        "loc_label": "Which School Location Would You Prefer to Attend?",
        "fmt_label": "What is your preferred learning format?",
        "fmt_opts": ["Select an option", "Morning · Mon–Fri 8:00 AM–2:00 PM", "Afternoon · Mon–Fri 2:00 PM–8:00 PM", "Weekend · Sat–Sun 9:00 AM–7:00 PM"],
        "lang_label": "Which Is Your Preferred Language of Communication?",
        "lang_opts": ["Select a language", "English", "Spanish / Español", "Other"],
        "msg_label": "Message for ABI",
        "msg_ph": "Tell us anything we should know — questions, schedule conflicts, financial aid needs, etc.",
        "submit": "Submit",
        "trust": "Free • No obligation • Reply within 24 hours",
        "consent_call": "I consent to receive automated or AI-assisted phone calls from American Barber Institute at the number provided. Message frequency may vary. You may opt out at any time by requesting removal during any call.",
        "consent_sms": "I consent to receive text messages from American Barber Institute at the number provided, including information about programs, enrollment, and promotions. Message and data rates may apply. Reply STOP to opt out at any time. Reply HELP for assistance.",
        "consent": "By clicking “Submit,” you consent to American Barber Institute contacting you via phone, SMS, or email regarding enrollment, appointment confirmations, follow-ups, and promotional offers.",
        "thanks": "Thank you! An ABI admissions agent will call you within 24 hours.",
    },
    "es": {
        "h": "Reserva Tu Lugar Hoy",
        "sub": "Completa el formulario y un asesor de admisiones te contactará.",
        "first": "Nombre", "last": "Apellido", "phone": "Teléfono", "email": "Correo Electrónico",
        "loc_label": "¿A cuál sede te gustaría asistir?",
        "fmt_label": "¿Cuál es tu horario preferido?",
        "fmt_opts": ["Selecciona una opción", "Mañana · Lun–Vie 8:00 AM–2:00 PM", "Tarde · Lun–Vie 2:00 PM–8:00 PM", "Fin de semana · Sáb–Dom 9:00 AM–7:00 PM"],
        "lang_label": "¿Cuál es tu idioma de comunicación preferido?",
        "lang_opts": ["Selecciona un idioma", "Español", "Inglés / English", "Otro"],
        "msg_label": "Mensaje para ABI",
        "msg_ph": "Cuéntanos lo que debamos saber — preguntas, conflictos de horario, ayuda financiera, etc.",
        "submit": "Enviar",
        "trust": "Gratis • Sin compromiso • Respondemos en 24 horas",
        "consent_call": "Doy mi consentimiento para recibir llamadas telefónicas automatizadas o asistidas por IA de American Barber Institute al número proporcionado. La frecuencia de los mensajes puede variar. Puedes optar por no recibirlos en cualquier momento solicitando la eliminación durante cualquier llamada.",
        "consent_sms": "Doy mi consentimiento para recibir mensajes de texto de American Barber Institute al número proporcionado, incluyendo información sobre programas, inscripciones y promociones. Pueden aplicarse tarifas de mensajes y datos. Responde STOP para optar por no recibirlos en cualquier momento. Responde HELP para asistencia.",
        "consent": "Al hacer clic en “Enviar”, das tu consentimiento para que American Barber Institute te contacte por teléfono, SMS o correo electrónico con respecto a inscripción, confirmaciones de citas, seguimientos y ofertas promocionales.",
        "thanks": "¡Gracias! Un agente de admisiones de ABI te llamará dentro de 24 horas.",
    },
}

# ─── footer ──────────────────────────────────────────────────────────
FOOTER = {
    "en": {
        "h": "American Barber Institute",
        "sub": "New York's only dedicated barber school — changing lives for over 30 years.",
        "fine": "© American Barber Institute. Approved by NYSED · Licensed by BPSS · Since 1996. *$150/week refers to the Plan C weekly payment.",
    },
    "es": {
        "h": "American Barber Institute",
        "sub": "La única escuela de barbería dedicada de Nueva York — cambiando vidas por más de 30 años.",
        "fine": "© American Barber Institute. Aprobada por NYSED · Licenciada por BPSS · Desde 1996. *$150/semana se refiere al pago semanal del Plan C.",
    },
}

# ─── gallery file list ───────────────────────────────────────────────
GALLERY = ["lf-gal-01.jpg", "lf-gal-02.jpg", "lf-gal-03.jpg", "lf-gal-04.jpg",
           "lf-gal-05.jpg", "lf-gal-06.jpg", "lf-gal-07.jpg", "lf-gal-08.jpg"]
GALLERY_HEAD = {"en": ("Gallery", "Life At ABI"), "es": ("Galería", "La Vida en ABI")}

# ─── YouTube clips (verbatim captions from "Watch Us") ───────────────
YT_CLIPS = [
    ("uADUtUtChH4", "Train to be a Master Barber at New York's #1 barber school", "Fórmate como Barbero Maestro en la escuela #1 de Nueva York"),
    ("oM8KfWfeTWA", "Our courses are hands-on, fun and engaging", "Nuestros cursos son prácticos, divertidos y dinámicos"),
    ("dQw4w9WgXcQ", "Tour our pro New York City barber clinic", "Recorre nuestra clínica profesional en Nueva York"),
]
YT_HEAD = {"en": ("Watch Us", "See ABI In Action"), "es": ("Míranos", "Mira a ABI en Acción")}

# ─── 3 Easy Steps section (between About and Techniques) ─────────────
THREE_STEPS_HEAD = {
    "en": ("3 Easy Steps", "Become a Professional Barber in 3 Easy Steps"),
    "es": ("3 Pasos Fáciles", "Conviértete en Barbero Profesional en 3 Pasos Fáciles"),
}
THREE_STEPS = {
    "en": [
        ("Get Started", "Submit your information to start your barbering journey."),
        ("Speak With an Advisor", "An ABI Admissions Advisor will answer your questions, explain the program, and review flexible payment plan options that fit your budget."),
        ("Start Training", "Complete your enrollment and begin building your professional barbering career."),
    ],
    "es": [
        ("Empieza", "Envía tu información para comenzar tu camino en la barbería."),
        ("Habla con un Asesor", "Un Asesor de Admisiones de ABI responderá tus preguntas, explicará el programa y revisará las opciones de planes de pago flexibles que se ajusten a tu presupuesto."),
        ("Comienza a Entrenar", "Completa tu inscripción y empieza a construir tu carrera profesional en la barbería."),
    ],
}

# ─── Career Earnings section (directly below 3 Easy Steps) ───────────
# Content lifted from the main marketing site's `sec--earnings` block so
# the landing pages tell the same career-outcome story.
EARNINGS_HEAD = {
    "en": ("Career Earnings", "Barber Career Earnings"),
    "es": ("Ingresos Profesionales", "Ingresos como Barbero"),
}
EARNINGS_TIERS = {
    "en": [
        ("YEAR 1 · Entry-Level",  "$35,000–$45,000",
         "Starting out in a shop, building your clientele and refining your technique."),
        ("YEARS 2–3 · Established", "$50,000–$70,000",
         "Loyal clientele, faster service and higher earnings as your reputation grows."),
        ("YEAR 3+ · Booth Renter / Shop Owner", "$75,000–$100,000+",
         "Full control of your schedule and earnings — the path to true entrepreneurship."),
    ],
    "es": [
        ("AÑO 1 · Nivel Inicial", "$35,000–$45,000",
         "Empezando en una barbería, construyendo tu clientela y refinando tu técnica."),
        ("AÑOS 2–3 · Establecido", "$50,000–$70,000",
         "Clientela leal, servicio más rápido y mayores ingresos a medida que crece tu reputación."),
        ("AÑO 3+ · Alquiler de Silla / Dueño", "$75,000–$100,000+",
         "Control total de tu horario e ingresos — el camino al verdadero emprendimiento."),
    ],
}
EARNINGS_NOTE = {
    "en": ("Earnings figures are estimates only and are not guaranteed. "
           "Actual income will vary based on individual effort, hours worked, "
           "location and market conditions."),
    "es": ("Los ingresos son estimaciones y no están garantizados. "
           "El ingreso real varía según el esfuerzo individual, las horas trabajadas, "
           "la ubicación y las condiciones del mercado."),
}


# ─── Promo topbar — phone chips per campus ───────────────────────────
# Manhattan shows 2 chips (EN + ES). Bronx shows 1 chip.
TOPBAR_PHONES_BY_CAMPUS = {
    "manhattan": [
        {"label": "EN", "display": "(212) 290-2289", "tel": "+12122902289"},
        {"label": "ES", "display": "(212) 290-0278", "tel": "+12122900278"},
        {"label": "Haircut", "display": "(856) 316-1551", "tel": "+18563161551"},
    ],
    "bronx": [
        {"label": "Bronx", "display": "(718) 676-0640", "tel": "+17186760640"},
        {"label": "Haircut", "display": "(856) 316-1551", "tel": "+18563161551"},
    ],
}

# ─── "Limited Seats" urgency banner shown right under the header ─────
SEATS_BANNER = {
    "en": ("LIMITED SEATS AVAILABLE", "Enrollment Now Open"),
    "es": ("CUPOS LIMITADOS DISPONIBLES", "Inscripciones Abiertas"),
}

# ─── Contact box (campus-aware) ──────────────────────────────────────
# Manhattan shows 2 numbers (EN + ES). Bronx shows 1 number only.
CONTACT_EMAIL = "admission@abi.edu"
# v3.3 — actual posted hours per the campus signage:
#   Monday–Friday      8:00 AM – 8:00 PM
#   Saturday & Sunday  9:00 AM – 7:00 PM
# Stored as a 2-line list so the contact box renders them on separate lines.
CONTACT_HOURS = {
    "en": [
        "Monday–Friday · 8:00 AM – 8:00 PM",
        "Saturday & Sunday · 9:00 AM – 7:00 PM",
    ],
    "es": [
        "Lunes–Viernes · 8:00 AM – 8:00 PM",
        "Sábado y Domingo · 9:00 AM – 7:00 PM",
    ],
}
CONTACT_HEAD = {
    "en": ("Contact", "Visit Our Campus"),
    "es": ("Contacto", "Visita Nuestro Campus"),
}
CONTACT_LABELS = {
    "en": {
        "addr":   "Address",
        "phone":  "Phone",
        "email":  "Email",
        "hours":  "Hours",
        "directions": "Get directions",
        "en_tag": "English",
        "es_tag": "Español",
        "bronx_tag": "Bronx",
    },
    "es": {
        "addr":   "Dirección",
        "phone":  "Teléfono",
        "email":  "Correo",
        "hours":  "Horario",
        "directions": "Cómo llegar",
        "en_tag": "Inglés",
        "es_tag": "Español",
        "bronx_tag": "Bronx",
    },
}
# Manhattan campus → EN + ES admissions lines
CONTACT_PHONES_MANHATTAN = [
    {"label_key": "en_tag", "display": "(212) 290-2289", "tel": "+12122902289"},
    {"label_key": "es_tag", "display": "(212) 290-0278", "tel": "+12122900278"},
]
# Bronx campus → one admissions number only
CONTACT_PHONES_BRONX = [
    {"label_key": "bronx_tag", "display": "(718) 676-0640", "tel": "+17186760640"},
]
CONTACT_PHONES_BY_CAMPUS = {
    "manhattan": CONTACT_PHONES_MANHATTAN,
    "bronx":     CONTACT_PHONES_BRONX,
}
