import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the exact line numbers for the two hero containers
for did in ['79d2b749', '65a79589']:
    idx = h.find(f'data-id="{did}"')
    if idx >= 0:
        line_num = h[:idx].count('\n') + 1
        snippet = h[idx:idx+120].replace('\n', ' ').replace('\r', '')
        print(f"[{did}] line {line_num}: {snippet[:100]}")
