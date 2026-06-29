"""
Find ONLY actual image URLs in the scraped.html - both <img> tags and 
CSS background-image with url() that point to actual .jpg/.png/.webp files.
Skip logos as instructed.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    scraped = f.read()

print("=" * 80)
print("ACTUAL IMAGES IN ORIGINAL TEMPLATE (scraped.html)")
print("=" * 80)

# 1. <img> tags with real image URLs
print("\n=== <img> TAGS ===")
for m in re.finditer(r'<img[^>]+src="([^"]+)"[^>]*>', scraped, re.DOTALL):
    src = m.group(1)
    fname = src.split('/')[-1].split('?')[0]
    line = scraped[:m.start()].count('\n') + 1
    
    if 'Logo' in fname or 'logo' in fname or 'favicon' in fname:
        kind = 'LOGO (skip)'
    else:
        kind = '*** IMAGE ***'
    
    # Get width if available
    w_m = re.search(r'width="(\d+)"', m.group(0))
    w = w_m.group(1) if w_m else '?'
    
    print(f"  line {line:4d}  w={w:>4s}  {kind}  {fname}")
    if kind == '*** IMAGE ***':
        print(f"            {src[:120]}")

# 2. Inline style background-image
print("\n=== INLINE STYLE background-image ===")
for m in re.finditer(r'style="[^"]*background-image:\s*url\([\'"]?([^\'")]+)[\'"]?\)', scraped):
    url = m.group(1)
    if not re.search(r'\.(jpg|jpeg|png|webp|gif)', url):
        continue
    line = scraped[:m.start()].count('\n') + 1
    fname = url.split('/')[-1].split('?')[0]
    print(f"  line {line:4d}  {fname}")
    print(f"            {url[:120]}")

# 3. data-settings with background_image containing actual URLs
print("\n=== data-settings background_image URLs ===")
import html as html_mod
for m in re.finditer(r'data-settings="([^"]+)"', scraped):
    raw = html_mod.unescape(m.group(1))
    if '"background_image"' not in raw:
        continue
    url_m = re.search(r'"url":"([^"]+)"', raw)
    if url_m:
        url = url_m.group(1)
        line = scraped[:m.start()].count('\n') + 1
        fname = url.split('/')[-1].split('?')[0]
        print(f"  line {line:4d}  {fname}")
        print(f"            {url[:120]}")
