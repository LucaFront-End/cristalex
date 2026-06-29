import re, sys
sys.stdout.reconfigure(encoding='utf-8')

cssfile = r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\586\content.md'
with open(cssfile, 'r', encoding='utf-8') as f:
    css = f.read()

# Search for the service card data-ids
search_ids = ['4f2deb07', '5d6cda97', 'b9b782', '5b218d5a', '307060b3', '412cb4d4', '4de24b70', '50edb326']
for did in search_ids:
    idx = css.find(f'elementor-element-{did}')
    if idx >= 0:
        chunk = css[idx:idx+300]
        bg = 'HAS BG-IMAGE' if 'background-image' in chunk else ('has bg-color' if 'background-color' in chunk else 'no bg')
        url_m = re.search(r'url\("?([^")\s]+)"?\)', chunk)
        url = url_m.group(1).split('/')[-1] if url_m else ''
        print(f"[{did}]  {bg}  {url}")
    else:
        print(f"[{did}]  NOT IN CSS")
