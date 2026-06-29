import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

known_bg = {'79d2b749': 'HERO-top', '65a79589': 'HERO-building'}

parents = list(re.finditer(
    r'<div class="elementor-element elementor-element-([a-f0-9]+)[^"]*e-parent[^"]*"[^>]*data-id="([a-f0-9]+)"',
    h
))

print(f"Total e-parent sections: {len(parents)}")
for i, m in enumerate(parents):
    did = m.group(2)
    pos = m.end()
    chunk = h[pos:pos+1500]
    headings = re.findall(r'<h\d[^>]*>(.*?)</h\d>', chunk, re.DOTALL)
    head_text = re.sub(r'<[^>]+>', '', headings[0]).strip()[:60] if headings else '???'
    known = f" [BG-IMG]" if did in known_bg else ''
    label = known_bg.get(did, '')
    line = h[:m.start()].count('\n') + 1
    print(f"  [{i+1:2d}] line={line:4d}  id={did}  {head_text}{known} {label}")
