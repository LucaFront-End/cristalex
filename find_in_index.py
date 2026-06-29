"""
Find these 4 images in the current index.html and their context.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

images = [
    'african-woman-architect',
    'lady-using-compass',
    'house-models-and-blueprints',
    'abstract-architectural-detail',
]

print("=== Finding 4 real images in index.html ===\n")
for img_key in images:
    idx = h.find(img_key)
    if idx >= 0:
        line = h[:idx].count('\n') + 1
        # Get the full img tag
        tag_start = h.rfind('<img', 0, idx)
        tag_end = h.find('>', idx) + 1
        tag = h[tag_start:tag_end]
        # Get src
        src_m = re.search(r'src="([^"]+)"', tag)
        src = src_m.group(1) if src_m else '?'
        # Context: look back for heading
        before = h[max(0, idx-1000):idx]
        headings = re.findall(r'<h\d[^>]*>(.*?)</h\d>', before, re.DOTALL)
        heading = re.sub(r'<[^>]+>', '', headings[-1]).strip()[:60] if headings else '?'
        print(f"  [{img_key[:30]}...]")
        print(f"    line {line}, section: {heading}")
        print(f"    src: {src[:80]}...")
    else:
        print(f"  [{img_key}] NOT FOUND in index.html")
    print()

# Also check for the 2 CSS background images
print("=== Background images from CSS (post-586.css) ===")
bg_images = [
    ('79d2b749', 'sky-cloud-background', 'Hero sky background'),
    ('65a79589', 'building-canopy', 'Building canopy/about section'),
]
for did, key, desc in bg_images:
    idx = h.find(f'data-id="{did}"')
    if idx >= 0:
        line = h[:idx].count('\n') + 1
        tag_end = h.find('>', idx)
        tag = h[idx:tag_end+1]
        has_override = 'style=' in tag and 'background-image' in tag
        print(f"  [{did}] {desc}: line {line}, override={'YES' if has_override else 'NO'}")
    else:
        print(f"  [{did}] NOT FOUND")
