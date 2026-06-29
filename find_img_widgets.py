"""
Find all image-related widgets in index.html:
- elementor-widget-image
- qi_addons image widgets
- jkit image widgets
- Any img tags that aren't logos
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

print("=== All img tags (non-logo) in index.html ===\n")
for m in re.finditer(r'<img[^>]+>', h, re.DOTALL):
    tag = m.group(0)
    src_m = re.search(r'src="([^"]+)"', tag)
    if not src_m:
        continue
    src = src_m.group(1)
    if any(x in src for x in ['Logo', 'logo', 'emoji', 'gravatar']):
        continue
    line = h[:m.start()].count('\n') + 1
    fname = src.split('/')[-1].split('?')[0][:60]
    # Find nearby data-id
    before = h[max(0,m.start()-500):m.start()]
    ids = re.findall(r'data-id="([^"]+)"', before)
    did = ids[-1] if ids else '?'
    print(f"  [{did}] line {line}: {fname}")
    print(f"    {src[:120]}")
    print()

print("=== elementor-widget-image sections ===\n")
for m in re.finditer(r'elementor-widget-image[^>]*>.*?</div>\s*</div>', h, re.DOTALL):
    widget = m.group(0)
    if len(widget) > 2000:
        continue
    imgs = re.findall(r'src="([^"]+)"', widget)
    line = h[:m.start()].count('\n') + 1
    before = h[max(0,m.start()-300):m.start()]
    ids = re.findall(r'data-id="([^"]+)"', before)
    did = ids[-1] if ids else '?'
    print(f"  [{did}] line {line}: {imgs}")

print("\n=== Service section around lines 1169-1475 ===\n")
# Look at the about section (lines 681-890)
about_chunk = h.split('\n')[680:890]
for i, line in enumerate(about_chunk):
    if 'src=' in line or 'background' in line.lower() or 'image' in line.lower():
        print(f"  line {681+i}: {line.strip()[:120]}")

print("\n=== About/Nosotros img and bg patterns ===")
# Find all sections about line 681-1100
lines = h.split('\n')
for i, ln in enumerate(lines[680:1100], start=681):
    if any(x in ln for x in ['src="http', 'background-image', 'elementor-widget-image']):
        print(f"  line {i}: {ln.strip()[:120]}")
