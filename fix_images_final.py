import re

file_path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# PLAN: Replace each occurrence of repeated images with
# contextually appropriate, varied Unsplash images
# ============================================================

# High quality glass/aluminum/construction Unsplash images
IMAGES = {
    # Hero / background
    'hero':     'https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1920&q=85&auto=format',
    # About section - glass facade closeup
    'about':    'https://images.unsplash.com/photo-1519999482648-25049ddd37b1?w=900&q=85&auto=format',
    # Stats - workers/construction
    'stats':    'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=900&q=85&auto=format',
    # Service 1 - glass windows
    'srv_glass': 'https://images.unsplash.com/photo-1486912500284-6dae7af1f1bd?w=800&q=85&auto=format',
    # Service 2 - aluminum curtain wall
    'srv_alum':  'https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=85&auto=format',
    # Service 3 - iron/metal gate
    'srv_iron':  'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800&q=85&auto=format',
    # Projects - residential
    'proj1':    'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=85&auto=format',
    # Projects - commercial building
    'proj2':    'https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=800&q=85&auto=format',
    # Projects - interior windows
    'proj3':    'https://images.unsplash.com/photo-1600566753086-00f18efc2291?w=800&q=85&auto=format',
    # Projects - glass facade building
    'proj4':    'https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=85&auto=format',
    # Projects - modern villa
    'proj5':    'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=85&auto=format',
    # Projects - aluminum pergola/canopy
    'proj6':    'https://images.unsplash.com/photo-1523413651479-597eb2da0ad6?w=800&q=85&auto=format',
    # Testimonial / contact background
    'contact':  'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=85&auto=format',
}

# ============================================================
# Replace images position by position using regex substitution
# with a counter to assign different images to each occurrence
# ============================================================

# Track what images are used where
img_pattern = re.compile(r'(src=")(https://images\.unsplash\.com/[^"]+)(")')

# Get all match positions and their surrounding context
matches = list(img_pattern.finditer(html))
print(f"Found {len(matches)} Unsplash image references")

# Build replacement map based on position/context
# We'll do targeted replacements based on surrounding HTML context
def get_section_context(pos, html, window=500):
    """Get surrounding HTML to determine what section an image is in"""
    before = html[max(0, pos-window):pos]
    after  = html[pos:pos+window]
    return before + after

replacements = {}
proj_counter = 0
proj_keys = ['proj1', 'proj2', 'proj3', 'proj4', 'proj5', 'proj6']

for m in matches:
    pos = m.start()
    ctx = get_section_context(pos, html)
    ctx_lower = ctx.lower()
    
    # Determine which image to use based on context
    if 'testimonial' in ctx_lower or 'review' in ctx_lower:
        key = 'contact'
    elif 'stats' in ctx_lower or 'achievement' in ctx_lower or 'logro' in ctx_lower or 'counter' in ctx_lower:
        key = 'stats'
    elif 'about' in ctx_lower or 'sobre' in ctx_lower or 'nosotros' in ctx_lower:
        key = 'about'
    elif 'hero' in ctx_lower or 'banner' in ctx_lower or 'header' in ctx_lower:
        key = 'hero'
    elif 'project' in ctx_lower or 'proyecto' in ctx_lower or 'portfolio' in ctx_lower or 'portafolio' in ctx_lower:
        key = proj_keys[proj_counter % len(proj_keys)]
        proj_counter += 1
    elif 'srv' in ctx_lower or 'servic' in ctx_lower or 'alumin' in ctx_lower or 'cristal' in ctx_lower or 'herrer' in ctx_lower:
        # Rotate through service images
        srv_idx = proj_counter % 3
        key = ['srv_glass', 'srv_alum', 'srv_iron'][srv_idx]
        proj_counter += 1
    elif 'contact' in ctx_lower or 'footer' in ctx_lower or 'contacto' in ctx_lower:
        key = 'contact'
    else:
        # Default: use position-based assignment
        key = proj_keys[proj_counter % len(proj_keys)]
        proj_counter += 1
    
    replacements[pos] = IMAGES[key]
    print(f"  [{pos}] -> {key}: {IMAGES[key][:60]}")

# Apply replacements (in reverse order to preserve positions)
result = html
offset = 0
for pos in sorted(replacements.keys()):
    m = img_pattern.search(result, pos + offset)
    if m and abs(m.start() - (pos + offset)) < 100:
        new_src = replacements[pos]
        old = m.group(0)
        new = m.group(1) + new_src + m.group(3)
        result = result[:m.start()] + new + result[m.end():]
        offset += len(new) - len(old)

# ============================================================
# Restore the brand logo section (Logo1-5.png)
# Use architecture/brand partner logos from templatekit CDN
# They should still be accessible since they're .png (not .jpg)
# ============================================================
base_url = 'https://templatekit.kitprostudio.com/archryze/wp-content/uploads/sites/65/2026/03/'
logo_files = [
    'Logo1.png', 'Logo2.png', 'Logo3.png', 'Logo4.png', 'Logo5.png'
]

# Find the logos section - it's a swiper/slider of logo images
# If logos are completely gone, the section will have broken img tags
# Let's check if there's a swiper-slide with no image
for logo in logo_files:
    full_url = base_url + logo
    if full_url not in result:
        print(f"Logo {logo} NOT in html - may need manual restoration")
    else:
        print(f"Logo {logo} OK")

# ============================================================
# Fix testimonial curly quotes one more time just in case
# ============================================================
result = result.replace('\u201c', '"').replace('\u201d', '"')
result = result.replace('\u2018', "'").replace('\u2019', "'")
result = result.replace('\u2014', ' - ').replace('\u2013', '-')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(result)

print(f"\nDone. File: {len(result)} chars")
