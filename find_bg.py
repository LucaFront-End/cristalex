import re, json

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find all data-settings with background images
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="(\{[^"]+\})"', h):
    did = m.group(1)
    try:
        s = m.group(2).replace('&quot;', '"')
        d = json.loads(s)
        if 'background_image' in d and d['background_image'].get('url'):
            url = d['background_image']['url']
            print(f'[{did}] {url.split("/")[-1]}')
            print(f'  {url}')
    except:
        pass
