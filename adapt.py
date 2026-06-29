"""
Adapta scraped.html (plantilla original perfecta) a Cristalex.
Solo cambia textos visibles e imágenes. No toca estructura HTML/CSS/JS.
"""
import re, shutil

SRC = r'd:\Workspace\Assets\Cristalex\scraped.html'
DST = r'd:\Workspace\Assets\Cristalex\index.html'

with open(SRC, 'r', encoding='utf-8') as f:
    h = f.read()

# ==================== TITLE ====================
h = h.replace('<title></title>', '<title>Cristalex - Construcciones Vidriadas</title>')

# Inject icon font CDNs right before </head> so icons work locally
icon_cdns = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
<style>
@font-face { font-family: "jkiticon"; src: url("https://templatekit.kitprostudio.com/archryze/wp-content/plugins/jeg-elementor-kit/assets/fonts/jkiticon/jkiticon.woff2") format("woff2"); font-weight: normal; font-style: normal; font-display: swap; }
@font-face { font-family: "ekiticons"; src: url("https://templatekit.kitprostudio.com/archryze/wp-content/plugins/elementskit-lite/modules/elementskit-icon-pack/assets/fonts/ekiticons.woff2") format("woff2"); font-weight: normal; font-style: normal; font-display: swap; }
.jki, [class^="jki-"], [class*=" jki-"] { font-family: "jkiticon" !important; font-style: normal; font-weight: normal; font-variant: normal; text-transform: none; line-height: 1; -webkit-font-smoothing: antialiased; }
.ekiticon, [class^="icon-"], [class*=" icon-"] { font-family: "ekiticons" !important; font-style: normal; font-weight: normal; font-variant: normal; text-transform: none; line-height: 1; -webkit-font-smoothing: antialiased; }
</style>
'''
h = h.replace('</head>', icon_cdns + '</head>')

# ==================== BRANDING ====================
# Main hero name
h = h.replace('>archryze<', '>CRISTALEX<')
h = h.replace('>Archryze<', '>CRISTALEX<')

# Copyright line
h = h.replace('©2025 Architecture Design', '©2025 Cristalex Construcciones Vidriadas')

# Logo image -> use the local logo
h = re.sub(
    r'src="https://templatekit\.kitprostudio\.com/archryze/wp-content/uploads/sites/65/2026/03/Logo-Ar3-01\.png"[^/]*/?>',
    'src="img/logo.jpg" alt="Cristalex" style="height:38px;width:auto;object-fit:contain" />',
    h, flags=re.DOTALL
)
# Remove srcset for logo
h = re.sub(r'srcset="[^"]*Logo-Ar3-01[^"]*"', '', h)

# ==================== MARQUEE TEXT ====================
h = h.replace('>Building Ideas <', '>Cristalería Moderna <')
h = h.replace('>Precision Structure.<', '>Aberturas de Aluminio.<')
h = h.replace('>Crafting Spaces <', '>Herrería de Calidad <')

# ==================== NAV MENU ====================
# Replace menu text (keep structure/links intact)
h = h.replace('>Home<', '>Inicio<')
h = h.replace('>About Us<', '>Nosotros<')
h = h.replace('>Services<', '>Servicios<')
h = h.replace('>Page<', '>Más<')
h = h.replace('>Contact Us<', '>Contacto<')
h = h.replace('>Pricing<', '>Presupuestos<')
h = h.replace('>Project<', '>Proyectos<')
h = h.replace('>Testimonials<', '>Testimonios<')
h = h.replace('>FAQs<', '>Preguntas Frecuentes<')
h = h.replace('>Blog<', '>Novedades<')
h = h.replace('>Team<', '>Equipo<')

# ==================== HERO SECTION ====================
h = h.replace(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis.',
    'Más de 17 años creando soluciones en cristalería, carpintería de aluminio y herrería para Buenos Aires y alrededores.'
)
h = h.replace('>Learn More<', '>Saber Más<')
h = h.replace('>Schedule Visit<', '>Solicitar Presupuesto<')

# ==================== ABOUT US ====================
h = h.replace('>About Us<', '>Sobre Nosotros<')  # section label
h = h.replace(
    'Where creativity, structure, and innovation shape',
    'Donde la experiencia, la calidad y la innovación crean'
)
h = h.replace('remarkable environments.', 'espacios extraordinarios.')
h = h.replace(
    'Innovative <span class="style-color"><span>architectural</span></span> design that blends creativity, <span class="style-color"><span>functionality</span></span>, and lasting value.',
    'Soluciones de <span class="style-color"><span>cristalería</span></span> y aberturas para casas, edificios y <span class="style-color"><span>proyectos comerciales</span></span>.'
)
h = h.replace('>symmetry<', '>Diseño<')
h = h.replace('>Build<', '>Calidad<')

# Vision / Mission
h = h.replace(
    'Archryze <span class="style-color"><span>Vission//</span></span>',
    'Nuestra <span class="style-color"><span>Visión//</span></span>'
)
h = h.replace(
    'Archryze <span class="style-color"><span>Mission//</span></span>',
    'Nuestra <span class="style-color"><span>Misión//</span></span>'
)

# ==================== POSITIONAL LOREM REPLACEMENTS ====================
# The template reuses "Lorem ipsum..." everywhere. We need to replace each
# occurrence with UNIQUE text based on its position in the file.
# Strategy: find all Lorem occurrences, determine their section by nearby
# data-id, and assign unique content.

# Process descriptions (no data-id, matched by unique text variants)
process_texts = [
    'Nos reunimos para entender tu proyecto, tomamos medidas y definimos materiales.',
    'Elaboramos planos, cotización detallada y planificación de obra.',
    'Diseñamos cada solución a medida según las necesidades del cliente.',
    'Fabricamos e instalamos con nuestro equipo de 20+ profesionales.',
]

# Blog post descriptions (sed do eiusmod tempor)
blog_texts = [
    'Cortinas de cristal: la tendencia que suma luz y elegancia a tu hogar.',
    'DVH: cómo el doble vidriado hermético mejora el aislamiento de tu casa.',
    'Ventajas del aluminio módena A30New frente a otras líneas del mercado.',
    'Herrería moderna: portones automáticos y fachadas que marcan la diferencia.',
]

# Now do sequential replacement of all Lorem ipsum patterns
import re as _re

# 1. Replace <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
#    These appear in: Vision, Mission, Footer, and other short descriptions
short_lorem = '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>'
short_replacements = [
    '<p>Ser la empresa líder en cristalería y carpintería de aluminio en Argentina, reconocida por la innovación y la calidad de cada proyecto.</p>',
    '<p>Brindar soluciones integrales en aberturas y herrería, acompañando a nuestros clientes desde el diseño hasta la instalación final.</p>',
    '<p>Más de 17 años brindando soluciones en cristalería y carpintería de aluminio.</p>',
    '<p>Calidad y confianza en cada instalación que realizamos.</p>',
    '<p>Soluciones a medida para cada tipo de proyecto.</p>',
]
for i, repl in enumerate(short_replacements):
    h = h.replace(short_lorem, repl, 1)  # replace ONE at a time

# 2. Replace long Lorem with pulvinar (services, testimonials, etc.)
long_lorem_pulvinar = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis, pulvinar dapibus leo.'
long_pulvinar_replacements = [
    'Fabricamos e instalamos ventanas, puertas y cerramientos en líneas módena A30New y A40 con los mejores herrajes del mercado.',
    'Pérgolas, fachadas, portones automáticos, rejas y parrillas. Diseños personalizados en hierro y acero de alta calidad.',
]
for repl in long_pulvinar_replacements:
    h = h.replace(long_lorem_pulvinar, repl, 1)

# 3. Testimonial quotes with HTML entities
testi_quote = '&#8220;Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis, pulvinar dapibus leo.&#8221;'
testi_replacements = [
    '"Excelente trabajo de Cristalex. Las aberturas de aluminio y el DVH que instalaron mejoraron notablemente el confort de nuestra casa. Muy profesionales."',
    '"Contratamos a Cristalex para la fachada de nuestro edificio comercial. El resultado fue impecable: puntualidad, calidad de materiales y excelente terminación."',
]
for repl in testi_replacements:
    h = h.replace(testi_quote, repl, 1)

# Also try with unicode curly quotes
testi_quote2 = '\u201cLorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis, pulvinar dapibus leo.\u201d'
for repl in testi_replacements:
    h = h.replace(testi_quote2, repl, 1)

# 4. Long Lorem without "leo." at end (various endings)
long_lorem_mattis = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis, pulvinar dapibus'
long_mattis_replacements = [
    'Contáctanos para solicitar presupuesto sin cargo. Atendemos en toda Buenos Aires y alrededores',
    'Más de 5.000 obras finalizadas acompañando a constructoras, arquitectos y clientes particulares en Buenos Aires y alrededores',
]
for repl in long_mattis_replacements:
    h = h.replace(long_lorem_mattis, repl, 1)

# 5. Short "Lorem ipsum" (testimonial names)
h = h.replace('>Lorem ipsum<', '>Muy recomendables<', 1)
h = h.replace('>Lorem ipsum<', '>Totalmente conformes<', 1)

# 6. Testimonial names - have space before <span>, e.g. ">Scarlett <span..."
h = h.replace('Scarlett <span', 'María G. <span')
h = h.replace('Penelope <span', 'Carlos R. <span')
h = h.replace('Madison <span', 'Laura P. <span')
h = h.replace('Valentina <span', 'Roberto M. <span')
h = h.replace('>Scarlett<', '>María G.<')
h = h.replace('>Penelope<', '>Carlos R.<')
h = h.replace('>Madison<', '>Laura P.<')
h = h.replace('>Valentina<', '>Roberto M.<')

# 7. Process step descriptions with typos in original
h = h.replace(
    'Lorem ipsum dolor sit , consectetur adipiscing elit',
    'Nos reunimos para entender tu proyecto, tomamos medidas y definimos materiales.'
)
h = h.replace(
    'sed do eiusmod tempor incididunt ut labore',
    'Elaboramos planos, cotización detallada y planificación de obra.'
)
h = h.replace(
    'minim veniam, quis nostrud exercitation ullamco',
    'Fabricamos e instalamos con nuestro equipo de 20+ profesionales.'
)
h = h.replace(
    'Lorem ipsum dolor sit t, consectetur adipiscing elit',
    'Diseñamos cada solución a medida según las necesidades del cliente.'
)
h = h.replace(
    'Lorem ipsum dolor sit, consectetur adipiscing elit',
    'Verificamos cada detalle y entregamos la obra terminada con garantía.'
)

# 8. Blog post descriptions (sed do eiusmod tempor)
sed_lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.'
sed_replacements = [
    'Cortinas de cristal: la tendencia que suma luz y elegancia a tu hogar.',
    'DVH: cómo el doble vidriado hermético mejora el aislamiento de tu casa.',
    'Ventajas del aluminio módena A30New frente a otras líneas del mercado.',
    'Herrería moderna: portones automáticos y fachadas que marcan la diferencia.',
]
for repl in sed_replacements:
    h = h.replace(sed_lorem, repl, 1)

# 9. Service subtitle with "pulvinar."
h = h.replace(
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut elit tellus, luctus nec ullamcorper mattis pulvinar.',
    'Trabajamos con carpintería de aluminio líneas módena A30New, A40, doble vidriado hermético, cortinas de cristal y herrería moderna.'
)

# 10. Any remaining Lorem ipsum (catch-all, one at a time with unique text)
remaining_lorem_texts = [
    'Combinamos experiencia técnica con los mejores herrajes y materiales importados del mercado.',
    'Nuestro equipo de más de 20 profesionales capacitados garantiza resultados de primera.',
    'Soluciones integrales para constructoras, arquitectos y clientes particulares.',
    'Calidad, confianza y compromiso en cada obra que realizamos.',
    'Asesoramiento técnico personalizado para cada tipo de proyecto.',
]
for repl in remaining_lorem_texts:
    if 'Lorem ipsum' in h:
        # Find and replace first remaining occurrence
        h = _re.sub(r'Lorem ipsum[^<]*', repl, h, count=1)
    else:
        break

# 11. Footer remaining short text with tabs
h = _re.sub(r'Lorem ipsum dolor sit amet, consectetur adipiscing elit\.\s*', 
            'Más de 17 años brindando soluciones en cristalería y carpintería de aluminio.', h)

# ==================== STATS ====================
h = h.replace(
    'Our journey is defined by <span class="style-color"><span>meaningful</span></span> milestones and successful <span class="style-color"><span>accomplishments.</span></span>',
    'Nuestra trayectoria se define por <span class="style-color"><span>resultados reales</span></span> y clientes verdaderamente <span class="style-color"><span>satisfechos.</span></span>'
)
h = h.replace('>Achievement<', '>Logros<')
h = h.replace('>Years of Experience<', '>Años de Experiencia<')
h = h.replace('data-to-value="26"', 'data-to-value="17"')
h = h.replace('>26<', '>17<')
h = h.replace('>Projects Completed<', '>Obras Realizadas<')
h = h.replace('data-to-value="120"', 'data-to-value="5000"')
h = h.replace('>120<', '>5000<')
h = h.replace('>Client Satisfaction<', '>Satisfacción del Cliente<')
h = h.replace('data-to-value="97"', 'data-to-value="100"')
h = h.replace('>97<', '>100<')
h = h.replace('>Skilled Professionals<', '>Profesionales Capacitados<')
h = h.replace('data-to-value="50"', 'data-to-value="20"')
h = h.replace('>50<', '>20<')

# ==================== SERVICES ====================
h = h.replace(
    'Designing Functional and <span class="style-color"><span>Inspiring Spaces.</span></span>',
    'Soluciones en cristal y aluminio con <span class="style-color"><span>Aberturas de Calidad.</span></span>'
)
# Service 1
h = h.replace(
    'Environmental <span class="style-color"><span>Design.</span></span>',
    'Carpintería de <span class="style-color"><span>Aluminio.</span></span>'
)
h = h.replace('>furniture.<', '>Módena A30New<')
h = h.replace('>Flow.<', '>DVH / A40<')

# Service 2
h = h.replace(
    'Design <span class="style-color"><span>Consultation.</span></span>',
    'Herrería <span class="style-color"><span>Moderna.</span></span>'
)
h = h.replace('>Architectural Drawing.<', '>Portones.<')
h = h.replace('>3D Modeling.<', '>DVH / A40<')

# ==================== PROCESS ====================
h = h.replace('>Our Working Process<', '>Nuestro Proceso<')
h = h.replace(
    'From concept to completion, we ensure a seamless and collaborative journey.',
    'Desde el concepto hasta la instalación, garantizamos un proceso eficiente y profesional.'
)
h = h.replace('>Consultation<', '>Consulta<')
h = h.replace('>Design<', '>Diseño<')
h = h.replace('>Construction<', '>Fabricación<')
h = h.replace('>Finishing<', '>Instalación<')

# ==================== TESTIMONIALS ====================
h = h.replace(
    'Client <span class="style-color"><span>feedback</span></span> that reflects our commitment to architectural <span class="style-color"><span>excellence.</span></span>',
    'Opiniones de <span class="style-color"><span>clientes</span></span> que reflejan nuestro compromiso con la <span class="style-color"><span>calidad.</span></span>'
)
# Replace curly quotes to simple quotes
h = h.replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u2019', "'")
h = h.replace('\u2014', ' - ').replace('\u2013', '-')

# ==================== FAQ ====================
h = h.replace(
    'Common <span class="style-color"><span>Questions</span></span> About Our Architectural Services.',
    'Preguntas <span class="style-color"><span>Frecuentes</span></span> Sobre Nuestros Servicios.'
)
h = h.replace('Find answers to common queries about our process, services, and expertise.',
              'Encuentre respuestas a consultas comunes sobre nuestros servicios.')
h = h.replace('What is the typical timeline for a project?', '¿Cuál es el tiempo estimado para un proyecto?')
h = h.replace('Do you provide customized design solutions?', '¿Realizan diseños y soluciones personalizadas?')
h = h.replace('What materials do you specialize in?', '¿Con qué materiales trabajan?')
h = h.replace('How do you ensure project quality?', '¿Cómo garantizan la calidad del trabajo?')

# FAQ answers (each one starts with p tag and has lorem ipsum)
faq_answers = [
    'El tiempo depende del tipo y tamaño del proyecto. Un trabajo estándar de aberturas puede llevar de 2 a 4 semanas desde la medición hasta la instalación.',
    'Sí, cada proyecto es único. Trabajamos con arquitectos y clientes para diseñar soluciones a medida en aluminio, vidrio y herrería.',
    'Utilizamos aluminio de primera calidad, vidrios de seguridad, doble vidriado hermético (DVH), herrajes importados y perfilería módena A30New y A40.',
    'Contamos con más de 17 años de experiencia y un equipo de 20+ profesionales. Cada obra pasa por controles de calidad antes de la entrega final.'
]

# Replace FAQ answer bodies
faq_pattern = r'(<div[^>]*class="e-n-accordion-item-title[^"]*"[^>]*>.*?</summary>\s*<div[^>]*role="region"[^>]*>\s*<div[^>]*>\s*<div[^>]*>\s*<div[^>]*text-editor[^>]*>\s*)(.*?)(</div>)'
faq_idx = [0]
def replace_faq_answer(m):
    idx = faq_idx[0]
    if idx < len(faq_answers):
        faq_idx[0] += 1
        return m.group(1) + '<p>' + faq_answers[idx] + '</p>' + m.group(3)
    return m.group(0)
h = re.sub(faq_pattern, replace_faq_answer, h, flags=re.DOTALL)

# ==================== PROJECTS ====================
h = h.replace(
    'Designing <span class="style-color"><span>Projects</span></span> with Purpose and Precision.',
    'Realizando <span class="style-color"><span>Proyectos</span></span> con Calidad y Precisión.'
)
h = h.replace('>Our Projects<', '>Nuestros Proyectos<')
h = h.replace('>All<', '>Todos<')
h = h.replace('>Architecture<', '>Arquitectura<')
h = h.replace('>Interior<', '>Interiores<')

# ==================== BLOG ====================
h = h.replace(
    'Stay informed with our latest insights and updates',
    'Mantente al tanto de nuestras últimas novedades'
)
h = h.replace('>Latest News &amp; Articles<', '>Últimas Novedades<')
h = h.replace('>Read More<', '>Leer Más<')

# ==================== CONTACT / FOOTER ====================
h = h.replace(
    "Let\u2019s Make Things Happen \u2014 Contact Us!",
    'Hagamos realidad tu proyecto - ¡Contáctanos!'
)
h = h.replace(
    "Let&#8217;s Make Things Happen &#8212; Contact Us!",
    'Hagamos realidad tu proyecto - ¡Contáctanos!'
)
h = h.replace('>Quick Links<', '>Enlaces Rápidos<')
h = h.replace('>Follow Us<', '>Síguenos<')
h = h.replace('>Home<', '>Inicio<')
h = h.replace('>Services<', '>Servicios<')
h = h.replace('>Email Address<', '>Correo Electrónico<')
h = h.replace('>Phone Number<', '>Número de Teléfono<')
h = h.replace('>Location<', '>Ubicación<')
h = h.replace('>Get In Touch<', '>Ponete en Contacto<')
h = h.replace('>Your Name<', '>Tu Nombre<')
h = h.replace('>Your Email<', '>Tu Correo<')
h = h.replace('>Your Message<', '>Tu Mensaje<')
h = h.replace('>Send Message<', '>Enviar Mensaje<')

# Footer about paragraph
h = re.sub(
    r'(<div[^>]*data-id="6278343"[^>]*>.*?<p>)(.*?)(</p>)',
    r'\1Acompañamos a constructoras, arquitectos y particulares en toda la planificación e instalación de carpintería y cristalería de alta gama.\3',
    h, count=1, flags=re.DOTALL
)

# Footer logo -> local logo
h = re.sub(
    r'(data-id="ad670ef"[^>]*>.*?)<img[^>]+/?>',
    r'\1<img src="img/logo.jpg" alt="Cristalex" style="height:38px;width:auto;object-fit:contain" />',
    h, count=1, flags=re.DOTALL
)

# ==================== REMAINING TEXT FIXES ====================
h = h.replace('>Our Services<', '>Nuestros Servicios<')
h = h.replace('>Creative Architecture<', '>Cristalería Moderna<')
h = h.replace('>Design.<', '>Diseño.<')
h = h.replace('>Project.<', '>Proyecto.<')

# Process/FAQ accordion titles with whitespace
h = h.replace('>Our Process<', '>Nuestro Proceso<')
h = re.sub(r'>\s*Concept Design\s*<', '>Diseño del Proyecto<', h)
h = re.sub(r'>\s*Design Development\s*<', '>Desarrollo y Fabricación<', h)
h = re.sub(r'>\s*How to Change my Photo from Admin Dashboard\?\s*<', '>¿Qué tipo de aberturas de aluminio fabrican?<', h)
h = re.sub(r'>\s*How to Change my Password easily\?\s*<', '>¿Qué es el Doble Vidriado Hermético (DVH)?<', h)
h = re.sub(r'>\s*How to Change my Subscription Plan using PayPal\s*<', '>¿Realizan trabajos de herrería personalizada?<', h)
h = re.sub(r'Far far away, behind the word mountains.*?right at the\.',
           'Fabricamos aberturas de aluminio en líneas módena A30New y A40, incluyendo ventanas, puertas, mamparas, cortinas de cristal y cerramientos. Todo con doble vidriado hermético (DVH) y los mejores herrajes del mercado.',
           h, flags=re.DOTALL)




# ==================== REMOVE BLOG SECTION ====================
# Find data-id="59386109" parent section and remove it
blog_match = re.search(r'(<div[^>]*data-id="59386109"[^>]*data-element_type="container"[^>]*>)', h)
if blog_match:
    start = blog_match.start()
    depth = 0
    i = start
    while i < len(h):
        if h[i:i+4] == '<div':
            depth += 1
        elif h[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                h = h[:start] + h[i+6:]
                print(f"Removed blog section ({i+6-start} chars)")
                break
        i += 1

# ==================== FIX ICONS (SVG inline) ====================
# Font files get CORS-blocked on local file://. Replace <i> tags with SVGs.
icon_svgs = {
    'icon icon-burger-menu':
        '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>',
    'icon icon-calendar3':
        '<svg viewBox="0 0 16 16" width="1em" height="1em" fill="currentColor"><path d="M14 1h-1V0h-2v1H5V0H3v1H2C.9 1 0 1.9 0 3v11c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V3c0-1.1-.9-2-2-2zm0 13H2V5h12v9z"/></svg>',
    'icon icon-quote2':
        '<svg viewBox="0 0 32 32" width="1em" height="1em" fill="currentColor"><path d="M7.031 14c3.866 0 7 3.134 7 7s-3.134 7-7 7-7-3.134-7-7l-0.031-1c0-7.732 6.268-14 14-14v4c-3.326 0-6.357 1.326-8.565 3.473 0.517-0.101 1.043-0.157 1.565-0.173l0.031-0.3zM25.031 14c3.866 0 7 3.134 7 7s-3.134 7-7 7-7-3.134-7-7l-0.031-1c0-7.732 6.268-14 14-14v4c-3.326 0-6.357 1.326-8.565 3.473 0.517-0.101 1.043-0.157 1.565-0.173l0.031-0.3z"/></svg>',
    'icon icon-user':
        '<svg viewBox="0 0 16 16" width="1em" height="1em" fill="currentColor"><path d="M8 8a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0 1c-2.67 0-8 1.34-8 4v1h16v-1c0-2.66-5.33-4-8-4z"/></svg>',
    'jki jki-diagonal-arrow-13':
        '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>',
    'jki jki-diagonal-arrow-5':
        '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>',
    'jki jki-magnifying-glass-search-light':
        '<svg viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor"><path d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"/></svg>',
    'jki jki-percent-solid':
        '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="currentColor"><path d="M7.5 11a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7zm0-5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zm9 14a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7zm0-5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM5.29 19.29a1 1 0 0 1 0-1.41l12.6-12.6a1 1 0 1 1 1.41 1.41l-12.6 12.6a1 1 0 0 1-1.41 0z"/></svg>',
    'jki jki-plus-line':
        '<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    'jki jki-toggle-on-solid':
        '<svg viewBox="0 0 576 512" width="1em" height="1em" fill="currentColor"><path d="M384 64H192C86 64 0 150 0 256s86 192 192 192h192c106 0 192-86 192-192S490 64 384 64zm0 320c-70.8 0-128-57.2-128-128s57.2-128 128-128 128 57.2 128 128-57.2 128-128 128z"/></svg>',
}

for cls, svg in icon_svgs.items():
    pattern = f'<i aria-hidden="true" class="{cls}"></i>'
    count = h.count(pattern)
    if count > 0:
        h = h.replace(pattern, svg)
        print(f"  Replaced {count}x {cls}")
    # Also try without aria-hidden
    pattern2 = f'<i class="{cls}"></i>'
    count2 = h.count(pattern2)
    if count2 > 0:
        h = h.replace(pattern2, svg)
        print(f"  Replaced {count2}x {cls} (no aria)")
    # Try with extra whitespace / tabindex
    pattern3 = re.compile(rf'<i\s[^>]*class="{re.escape(cls)}"[^>]*>\s*</i>')
    matches = pattern3.findall(h)
    if matches:
        h = pattern3.sub(svg, h)
        print(f"  Replaced {len(matches)}x {cls} (regex)")

# Also handle the <i class='fa'></i> submenu arrows
h = re.sub(r"<i class='fa'></i>", '<i class="fa fa-chevron-down" style="font-size:0.6em"></i>', h)

# ==================== WRITE ====================
with open(DST, 'w', encoding='utf-8') as f:
    f.write(h)

print(f"Done! {DST} -> {len(h)} chars, {h.count(chr(10))} lines")
