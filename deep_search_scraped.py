"""
Search scraped.html for:
1. All <img> tags (not logos)
2. All data-ids with their nearby context to identify the visual sections
3. Look for Elementor image widget structure
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    scraped = f.read()

print("=== ALL non-logo <img> tags in scraped.html ===\n")
for m in re.finditer(r'<img[^>]+>', scraped, re.DOTALL):
    tag = m.group(0)
    src_m = re.search(r'src="([^"]+)"', tag)
    if not src_m:
        continue
    src = src_m.group(1)
    fname = src.split('/')[-1].split('?')[0]
    line = scraped[:m.start()].count('\n') + 1
    
    # Skip logos and emoji
    if any(x in src for x in ['Logo', 'logo', 'emoji', 'gravatar', 'blank.gif']):
        continue
    
    print(f"  line {line:4d}: {fname}")
    print(f"           {src[:120]}")
    print()

print("\n=== Elementor image WIDGETS (widget-image) ===\n")
for m in re.finditer(r'elementor-widget-image[^>]*>.*?</div>', scraped, re.DOTALL):
    widget = m.group(0)
    imgs = re.findall(r'src="([^"]+)"', widget)
    line = scraped[:m.start()].count('\n') + 1
    # Find nearby data-id
    before = scraped[max(0, m.start()-200):m.start()]
    did_m = re.search(r'data-id="([^"]+)"', before[-200:])
    did = did_m.group(1) if did_m else '?'
    for img in imgs:
        fname = img.split('/')[-1][:60]
        if 'Logo' not in fname and 'logo' not in fname:
            print(f"  [{did}] line {line}: {fname}")
            print(f"           {img[:120]}")

print("\n=== All CSS URLs referenced in <link> tags ===\n")
for m in re.finditer(r"<link[^>]+href=['\"]([^'\"]+\.css[^'\"]*)['\"]", scraped):
    href = m.group(1)
    if 'elementor' in href or 'uploads' in href:
        fname = href.split('/')[-1].split('?')[0]
        print(f"  {fname}")
        print(f"  {href[:100]}")
