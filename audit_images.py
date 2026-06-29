import re, sys, html
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("COMPREHENSIVE IMAGE AUDIT")
print("=" * 80)

# 1. Find ALL <img> tags
print("\n=== <img> TAGS ===")
for i, m in enumerate(re.finditer(r'<img[^>]+>', content, re.DOTALL)):
    tag = m.group(0)
    src_m = re.search(r'src="([^"]+)"', tag)
    if not src_m:
        continue
    src = src_m.group(1)
    line = content[:m.start()].count('\n') + 1
    is_local = src.startswith('img/') or src.startswith('./')
    # Classify
    if 'Logo' in src or 'logo' in src:
        cat = 'LOGO (skip)'
    elif is_local:
        cat = 'LOCAL (already done)'
    else:
        cat = '*** EXTERNAL - NEEDS CHANGE ***'
    print(f"  [{i+1}] line {line}: {cat}")
    print(f"       src={src[:100]}")

# 2. Find ALL background-image in inline styles
print("\n=== INLINE style background-image ===")
for m in re.finditer(r'style="[^"]*background-image:\s*url\([\'"]?([^\'")]+)[\'"]?\)', content):
    url = m.group(1)
    line = content[:m.start()].count('\n') + 1
    is_local = url.startswith('img/')
    cat = 'LOCAL (done)' if is_local else '*** EXTERNAL ***'
    print(f"  line {line}: {cat}  {url[:100]}")

# 3. Find ALL background-image in CSS blocks within <style> tags
print("\n=== CSS <style> background-image ===")
for m in re.finditer(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', content):
    url = m.group(1)
    line = content[:m.start()].count('\n') + 1
    is_local = url.startswith('img/')
    if 'cristalex-bg-override' in content[max(0,m.start()-500):m.start()]:
        cat = 'CSS OVERRIDE (done)'
    elif is_local:
        cat = 'LOCAL (done)'
    else:
        cat = '*** EXTERNAL ***'
    print(f"  line {line}: {cat}  {url[:100]}")

# 4. Find ALL data-settings with background_image containing URLs
print("\n=== data-settings background_image URLs ===")
for m in re.finditer(r'data-settings="([^"]+)"', content):
    settings_raw = html.unescape(m.group(1))
    if 'background_image' not in settings_raw:
        continue
    url_m = re.search(r'"url":"([^"]+)"', settings_raw)
    if url_m:
        url = url_m.group(1)
        line = content[:m.start()].count('\n') + 1
        print(f"  line {line}: {url[:100]}")

# 5. Find ALL external URLs that look like images
print("\n=== ALL external image URLs (any context) ===")
seen = set()
for m in re.finditer(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp|gif)', content):
    url = m.group(0)
    if url in seen:
        continue
    seen.add(url)
    line = content[:m.start()].count('\n') + 1
    fname = url.split('/')[-1]
    # classify
    if any(x in url for x in ['.css', '.js', 'elementor/css', 'assets/css', 'assets/lib', 'assets/fonts', 'plugins/']):
        continue  # skip CSS/JS assets
    if 'Logo' in fname or 'logo' in fname:
        cat = 'LOGO (skip)'
    else:
        cat = '*** NEEDS CHANGE ***'
    print(f"  line {line}: {cat}  {fname}")
    print(f"       {url[:120]}")
