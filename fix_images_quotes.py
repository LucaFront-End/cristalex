import re

file_path = r'd:\Workspace\Assets\Cristalex\index.html'

with open(file_path, 'rb') as f:
    data = f.read()

# ============================================================
# 1. FIX CURLY QUOTES (â€œ / â€ and â€™)
#    These are valid UTF-8 curly quotes: \xe2\x80\x9c -> "  \xe2\x80\x9d -> "
#    Replace with straight quotes to avoid rendering issues
# ============================================================
data = data.replace(b'\xe2\x80\x9c', b'"')   # LEFT DOUBLE QUOTATION MARK -> "
data = data.replace(b'\xe2\x80\x9d', b'"')   # RIGHT DOUBLE QUOTATION MARK -> "
data = data.replace(b'\xe2\x80\x99', b"'")   # RIGHT SINGLE QUOTATION MARK -> '
data = data.replace(b'\xe2\x80\x98', b"'")   # LEFT SINGLE QUOTATION MARK -> '
data = data.replace(b'\xe2\x80\x93', b'-')   # EN DASH -> -
data = data.replace(b'\xe2\x80\x94', b' - ') # EM DASH -> -

# ============================================================
# 2. FIX BROKEN LOCAL IMAGE PATHS
#    Replace img/xxx.png paths with proper Unsplash images
# ============================================================
text = data.decode('utf-8', errors='replace')

# Architecture & glass-related Unsplash images
image_map = {
    'img/hero.png':
        'https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1600&q=80',
    'img/about.png':
        'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=900&q=80',
    'img/stats.png':
        'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=900&q=80',
    'img/srv_glass.png':
        'https://images.unsplash.com/photo-1486912500284-6dae7af1f1bd?w=800&q=80',
    'img/srv_aluminum.png':
        'https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=800&q=80',
    'img/proj_res.png':
        'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&q=80',
    'img/proj_com.png':
        'https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80',
    'img/proj_int.png':
        'https://images.unsplash.com/photo-1600566753086-00f18efc2291?w=800&q=80',
    'img/process1.png':
        'https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80',
    'img/process2.png':
        'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=600&q=80',
    'img/process3.png':
        'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=600&q=80',
    'img/process4.png':
        'https://images.unsplash.com/photo-1590725140246-20acddc1ec6d?w=600&q=80',
    'img/testimonial.png':
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80',
}

for local_path, unsplash_url in image_map.items():
    text = text.replace(f'src="{local_path}"', f'src="{unsplash_url}"')
    text = text.replace(f"src='{local_path}'", f"src='{unsplash_url}'")

# Also replace any remaining img/ paths that weren't mapped
# (catch-all: any src="img/xxx" that isn't img/logo.jpg)
def replace_unmapped_img(m):
    src = m.group(1)
    if src == 'img/logo.jpg' or src.startswith('http') or not src.startswith('img/'):
        return m.group(0)
    print(f"  Replacing unmapped: {src}")
    return 'src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80"'

text = re.sub(r'src="(img/[^"]+)"', replace_unmapped_img, text)

# ============================================================
# 3. ALSO RESTORE any templatekit images that got broken
#    The regex in fix_more.py was too broad - it replaced ALL
#    jpg images from the CDN with the same Unsplash URL.
#    Let's restore the logos and hero images that came from templatekit
# ============================================================
# The archryze logos (Logo1.png - Logo5.png) should point back to templatekit
# Check if any are broken
logo_base = 'https://templatekit.kitprostudio.com/archryze/wp-content/uploads/sites/65/2026/03/'

# These should remain as templatekit logos:
logo_files = ['Logo1.png', 'Logo2.png', 'Logo3.png', 'Logo4.png', 'Logo5.png',
              'archryze-logo.png', 'building-canopy-2026-01-08-02-11-40-utc-2.png',
              'sky-cloud-background-blue-skyline-summer-2026-01-08-05-53-37-utc.jpg']

# Check if they got replaced
for logo in logo_files:
    if logo in text:
        print(f"OK: {logo} still referenced")
    else:
        print(f"MISSING: {logo}")

with open(file_path, 'wb') as f:
    f.write(text.encode('utf-8'))

print(f"\nDone. File size: {len(text)} chars")
