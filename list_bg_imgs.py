import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find background images in data-settings JSON
imgs = re.findall(r'"url":"(https?://[^"]+\.(jpg|jpeg|png|webp))"', h)
seen = set()
for url, ext in imgs:
    if url in seen:
        continue
    seen.add(url)
    skip_words = ['Logo', 'logo', 'icon', 'favicon', 'Logo3', 'Logo4']
    if any(x in url for x in skip_words):
        continue
    # Get context (which section)
    idx = h.find(url)
    before = h[max(0, idx-500):idx]
    data_ids = re.findall(r'data-id="([^"]+)"', before)
    data_id = data_ids[-1] if data_ids else '?'
    print(f"[{data_id}] {url.split('/')[-1]}")
    print(f"  {url}")
    print()
