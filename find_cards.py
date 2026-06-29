import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the service card spacer containers and project items
targets = ['5d6cda97', '5b218d5a', '4f2deb07', 'b9b782']
for did in targets:
    idx = h.find(f'data-id="{did}"')
    if idx >= 0:
        line = h[:idx].count('\n') + 1
        snippet = h[idx:idx+150].replace('\r','').replace('\n',' ')
        print(f"[{did}] line {line}: {snippet[:120]}")
    else:
        print(f"[{did}] NOT FOUND")

# Also find the projects gallery items  
print()
print("=== PROJECT items (around section 48f0e5bd) ===")
proj_idx = h.find('data-id="48f0e5bd"')
if proj_idx >= 0:
    chunk = h[proj_idx:proj_idx+3000]
    # Find background_background containers within projects
    for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="[^"]*background_background[^"]*"', chunk):
        did = m.group(1)
        pos = m.end()
        after = h[proj_idx+pos:proj_idx+pos+200].replace('\r','').replace('\n',' ')
        print(f"  [{did}]: {after[:100]}")
