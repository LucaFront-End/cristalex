import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find all img tags that are NOT logos/small
print("=== ALL IMG TAGS ===")
for m in re.finditer(r'<img[^>]+>', h, re.DOTALL):
    tag = m.group(0)
    src = re.search(r'src="([^"]+)"', tag)
    width = re.search(r'width="(\d+)"', tag)
    if not src:
        continue
    url = src.group(1)
    w = int(width.group(1)) if width else 0
    # Skip very small images and known logos
    is_logo = any(x in url for x in ['Logo3', 'Logo4', 'logo', 'favicon', 'emoji'])
    is_local = url.startswith('img/')
    print(f"  w={w:4d}  local={is_local}  logo={is_logo}  {url.split('/')[-1][:60]}")
