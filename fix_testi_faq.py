"""
Post-procesamiento directo del index.html generado.
Arregla testimonios y FAQ/proceso que quedaron mal.
"""
import re

path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()

# ==========================================
# 1. FIX TESTIMONIALS - Replace by data-id
# ==========================================
# Testimonial 1 is near data-id="1d6a4fa0" 
# Testimonial 2 is near data-id="4a68c725"
# The quote text is wrapped in &#8220;...&#8221;

# Replace ALL &#8220;...&#8221; blocks (there are exactly 2, both testimonials)
testi_texts = [
    'Excelente trabajo de Cristalex. Las aberturas de aluminio y el DVH que instalaron mejoraron notablemente el confort y la aislación de nuestra casa. Muy profesionales y puntuales.',
    'Contratamos a Cristalex para la fachada de vidrio de nuestro edificio comercial. Resultado impecable, calidad de materiales superior y excelente terminación en cada detalle.',
]

# Find and replace each &#8220;...&#8221; block
pattern = re.compile(r'&#8220;(.*?)&#8221;', re.DOTALL)
matches = list(pattern.finditer(h))
print(f"Found {len(matches)} testimonial quotes")

# Replace in reverse order to preserve positions
for i, m in enumerate(reversed(matches)):
    idx = len(matches) - 1 - i
    if idx < len(testi_texts):
        old = m.group(0)
        new = '&#8220;' + testi_texts[idx] + '&#8221;'
        h = h[:m.start()] + new + h[m.end():]
        print(f"  Replaced testimonial {idx+1}: {testi_texts[idx][:60]}...")

# ==========================================
# 2. FIX ACCORDION TITLES (Process section)
# ==========================================
# The accordion titles are: Discovery, Concept Design, Design Development
# These are the PROCESS steps, not FAQ
h = re.sub(r'>\s*Discovery\s*<', '>Relevamiento<', h)
# Concept Design and Design Development were already handled but let's make sure
h = re.sub(r'>\s*Concept Design\s*<', '>Diseño del Proyecto<', h)  
h = re.sub(r'>\s*Design Development\s*<', '>Desarrollo y Fabricación<', h)

# ==========================================
# 3. FIX THE REAL FAQ SECTION
# ==========================================
# The real FAQ uses a different widget. Let me find it.
# FAQ questions are: "What is the typical timeline...", etc.
# These were already translated. Let's verify the answers.

# Check what FAQ questions exist
faq_questions = [
    '¿Cuál es el tiempo estimado para un proyecto?',
    '¿Realizan diseños y soluciones personalizadas?', 
    '¿Con qué materiales trabajan?',
    '¿Cómo garantizan la calidad del trabajo?',
    '¿Qué tipo de aberturas de aluminio fabrican?',
    '¿Qué es el Doble Vidriado Hermético (DVH)?',
    '¿Realizan trabajos de herrería personalizada?',
]
for q in faq_questions:
    if q in h:
        print(f"  FAQ Q OK: {q[:50]}")
    else:
        print(f"  FAQ Q MISSING: {q[:50]}")

# ==========================================
# 4. FIX "Muy recomendables" / "Totalmente conformes" 
#    These are the short testimonial subtitles
# ==========================================
# Check if they exist
for label in ['Muy recomendables', 'Totalmente conformes']:
    count = h.count(label)
    print(f"  '{label}': {count}x")

# ==========================================
# 5. Check names
# ==========================================
for name in ['Scarlett', 'Penelope', 'Madison', 'Valentina', 'María', 'Carlos', 'Laura', 'Roberto']:
    count = h.count(name)
    if count:
        print(f"  Name '{name}': {count}x")

with open(path, 'w', encoding='utf-8') as f:
    f.write(h)

print(f"\nDone! {len(h)} chars")
