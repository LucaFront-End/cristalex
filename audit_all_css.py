import re, sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\715\content.md', 'post-5 (header/footer)'),
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\623\content.md', 'post-523'),
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\669\content.md', 'post-528'),
]

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

for cssfile, label in files:
    with open(cssfile, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Find ALL background-image URLs
    bgs = list(re.finditer(r'elementor-element-([a-f0-9]+)\b[^{]*\{[^}]*background-image[^}]*url\(["\']?([^"\')\s]+)["\']?\)', css, re.DOTALL))
    
    if bgs:
        print(f"\n=== {label}: {len(bgs)} background images ===")
        for m in bgs:
            did = m.group(1)
            url = m.group(2)
            fname = url.split('/')[-1]
            
            idx = html_content.find(f'data-id="{did}"')
            if idx >= 0:
                chunk = html_content[max(0, idx-200):idx+500]
                overridden = "style=\"background-image" in chunk
                status = "DONE" if overridden else "*** NEEDS FIX ***"
            else:
                status = "NOT IN HTML"
            print(f"  [{did}]  {status}  {fname}")
    else:
        print(f"\n=== {label}: NO background images ===")

# ALSO: check ALL external CSS files referenced in post-586.css
# for any `background-image` or images referenced by data-ids that we haven't handled
print("\n\n=== FINAL CHECK: data-ids with background_background but NO inline override ===")
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="([^"]*background_background[^"]*)"', html_content):
    did = m.group(1)
    pos = m.start()
    # Check for inline style override
    tag_end = html_content.find('>', pos)
    tag = html_content[pos:tag_end+1]
    has_override = 'style="background-image' in tag or "style='background-image" in tag
    
    if not has_override:
        line = html_content[:pos].count('\n') + 1
        # Find context
        after = html_content[tag_end:tag_end+500]
        headings = re.findall(r'<h\d[^>]*>(.*?)</h\d>', after, re.DOTALL)
        head = re.sub(r'<[^>]+>', '', headings[0]).strip()[:40] if headings else ''
        texts = re.findall(r'<span[^>]*>([^<]{3,30})</span>', after)
        text = texts[0] if texts else ''
        print(f"  [{did}] line {line}: NO OVERRIDE  context: {head or text or '???'}")
