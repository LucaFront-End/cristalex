import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find sections with classic background (these are the ones with images)
# Also look for large img tags
print("=== SECTIONS WITH BACKGROUND (data-id) ===")
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="[^"]*background_background[^"]*"', h):
    did = m.group(1)
    # Get next 300 chars for context
    after = h[m.end():m.end()+600]
    # Find first meaningful text
    texts = re.findall(r'>[A-Za-záéíóúñÁÉÍÓÚÑ][^<]{3,40}<', after)
    label = texts[0].strip('<>') if texts else '???'
    print(f"  [{did}] {label[:50]}")

print()
print("=== LARGE IMG TAGS ===")
for m in re.finditer(r'<img[^>]+width="(\d+)"[^>]+src="([^"]+)"', h):
    w = int(m.group(1))
    url = m.group(2)
    if w >= 400 and 'Logo' not in url and 'logo' not in url and 'favicon' not in url:
        print(f"  w={w} {url.split('/')[-1][:60]}")
        print(f"       {url[:100]}")
