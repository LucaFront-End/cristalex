"""
Search the index.html for ALL <style> blocks and find background-image URLs.
Elementor often outputs critical CSS inline in <style> tags.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

print("=== All background-image URLs in <style> blocks ===\n")

seen = set()
for style_m in re.finditer(r'<style[^>]*>(.*?)</style>', h, re.DOTALL):
    block = style_m.group(1)
    style_line = h[:style_m.start()].count('\n') + 1
    
    for bg_m in re.finditer(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', block):
        url = bg_m.group(1)
        if not re.search(r'\.(jpg|jpeg|png|webp|gif|svg)', url, re.IGNORECASE):
            continue
        if url in seen:
            continue
        seen.add(url)
        
        fname = url.split('/')[-1].split('?')[0]
        is_local = url.startswith('img/')
        
        # Find CSS selector context
        before = block[:bg_m.start()]
        selectors = re.findall(r'[\.\#][\w\-]+([\w\-\.\s,>:]+)?(?=\s*\{)', before)
        sel = selectors[-1] if selectors else '?'
        
        # Find elementor-element data-id in selector
        id_m = re.search(r'elementor-element-([\da-f]+)', before[-300:])
        did = id_m.group(1) if id_m else '?'
        
        print(f"  [{did}]  {'LOCAL' if is_local else 'REMOTE'}")
        print(f"    file: {fname}")
        if not is_local:
            print(f"    url:  {url[:120]}")
        print()

# Also check data-settings for any background_image JSON (Elementor stores URLs here too)
print("=== data-settings with background_image ===\n")
import html as html_mod
count = 0
for m in re.finditer(r'data-settings="([^"]{50,})"', h):
    decoded = html_mod.unescape(m.group(1))
    if '"background_image"' not in decoded:
        continue
    # Find URL
    url_m = re.search(r'"url"\s*:\s*"([^"]+)"', decoded)
    if url_m:
        url = url_m.group(1)
        if url and not url.endswith('#'):
            line = h[:m.start()].count('\n') + 1
            did_m = re.search(r'data-id="([^"]+)"', h[max(0,m.start()-200):m.start()+50])
            did = did_m.group(1) if did_m else '?'
            fname = url.split('/')[-1]
            print(f"  [{did}] line {line}: {fname}")
            print(f"    {url[:120]}")
            count += 1

if count == 0:
    print("  None found")

print(f"\n\nTotal style blocks in HTML: {len(list(re.finditer('<style', h)))}")
