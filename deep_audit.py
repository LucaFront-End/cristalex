"""
For each data-id with background_background, check ALL CSS files for
background-image rules. Those with only background-color are fine (just colors).
Those with background-image from remote need overrides.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load ALL CSS content
css_files = [
    r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\586\content.md',
    r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\623\content.md',
    r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\669\content.md',
    r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\715\content.md',
]

all_css = ''
for f in css_files:
    with open(f, 'r', encoding='utf-8') as fh:
        all_css += fh.read() + '\n'

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# data-ids with background_background but no inline override
no_override = []
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="([^"]*background_background[^"]*)"', html_content):
    did = m.group(1)
    pos = m.start()
    tag_end = html_content.find('>', pos)
    tag = html_content[pos:tag_end+1]
    has_override = 'style="background-image' in tag or "style='background-image" in tag
    if not has_override:
        no_override.append((did, html_content[:pos].count('\n') + 1))

print(f"Containers with background_background but NO inline override: {len(no_override)}")
print()

# For each, check if any CSS has a background-image rule for it
for did, line in no_override:
    # Search CSS for this element
    pattern = f'elementor-element-{did}'
    idx = all_css.find(pattern)
    if idx < 0:
        print(f"  [{did}] line {line}: NOT IN ANY CSS -> uses Elementor dynamic styles (probably has IMAGE)")
        continue
    
    # Get the full rule block
    block_start = all_css.rfind('{', 0, idx)
    block_end = all_css.find('}', idx)
    if block_start < 0 or block_end < 0:
        continue
    
    # Actually we need to find ALL rules for this element
    rules = []
    for rm in re.finditer(f'elementor-element-{did}[^{{]*\\{{([^}}]+)\\}}', all_css):
        rules.append(rm.group(1))
    
    has_bg_image = any('background-image' in r and 'url(' in r for r in rules)
    has_bg_color = any('background-color' in r for r in rules)
    
    if has_bg_image:
        # Extract the URL
        for r in rules:
            url_m = re.search(r'background-image[^;]*url\(["\']?([^"\')\s]+)["\']?\)', r)
            if url_m:
                print(f"  [{did}] line {line}: HAS REMOTE IMAGE -> {url_m.group(1).split('/')[-1]}")
                break
    elif has_bg_color:
        print(f"  [{did}] line {line}: ONLY background-color (no image needed)")
    else:
        print(f"  [{did}] line {line}: IN CSS but no bg-image or bg-color found -> probably dynamic")

# ALSO check: which containers might get images from Elementor JS at runtime
# by looking at the data-settings for background_image references
print("\n\n=== Containers with background_image in data-settings ===")
import html as html_mod
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="([^"]+)"', html_content):
    did = m.group(1)
    settings = html_mod.unescape(m.group(2))
    if '"background_image"' in settings:
        print(f"  [{did}]: {settings[:200]}")
