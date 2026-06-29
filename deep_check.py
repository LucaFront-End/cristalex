import re

file_path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. Find all sections missing images (img tags with broken src)
# ============================================================
print("=== SECTIONS WITHOUT IMAGES ===")
# Find elementor containers and check if they have an img inside
section_pattern = re.compile(
    r'<div[^>]*data-id="([^"]+)"[^>]*data-element_type="container"[^>]*>'
)
for m in section_pattern.finditer(html):
    data_id = m.group(1)
    # Get the section content (roughly 3000 chars)
    content = html[m.start():m.start()+3000]
    # Check for images
    has_img = 'src="http' in content or 'src="img/' in content
    # Look for section label
    label = re.search(r'elementor-icon-list-text[^>]*>([^<]+)<', content)
    heading = re.search(r'heading-title[^>]*>([^<]+)', content)
    section_name = label.group(1).strip() if label else (heading.group(1).strip()[:40] if heading else f'id={data_id}')
    if not has_img and len(content) > 1000:  # substantial section without image
        print(f"  No img: {section_name} (data-id={data_id})")

# ============================================================
# 2. Check the title tag
# ============================================================
title_m = re.search(r'<title>(.*?)</title>', html)
print(f"\n=== TITLE: {title_m.group(1) if title_m else 'MISSING'} ===")

# ============================================================
# 3. Check testimonials for bad chars
# ============================================================
testi_idx = html.find('Testimoni')
if testi_idx != -1:
    chunk = html[testi_idx:testi_idx+5000]
    bad = [c for c in ['\u00e2', '\u0080', '\u009c', '\u009d'] if c in chunk]
    print(f"\n=== TESTIMONIALS bad chars: {bad} ===")
    # Extract all text content
    texts = re.findall(r'>([^<]{5,300})<', chunk)
    for t in texts:
        t = t.strip()
        if t and not t.startswith('{') and not t.startswith('//') and any(c.isalpha() for c in t):
            print(f"  TEXT: {t[:100]}")

# ============================================================
# 4. Logo section - find the swiper/logo area  
# ============================================================
# In the original the logos were near the hero section
# Look for qi-addons-for-elementor slider or ekit-wid-con
logo_section_markers = ['qi-image-gallery', 'ekit-testimonial', 'qodef-e-testimonials']
for marker in logo_section_markers:
    idx = html.find(marker)
    if idx != -1:
        print(f"\n=== FOUND: {marker} at {idx} ===")
        print(html[idx:idx+200])
