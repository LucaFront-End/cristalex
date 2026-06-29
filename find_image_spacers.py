"""
Identify ONLY the containers that are true "image spacer" containers.
These are containers with background_background:classic that contain ONLY a spacer widget.
These are the ones that show images from remote Elementor CSS.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find all containers with background_background:classic
bg_containers = []
for m in re.finditer(r'(<div[^>]*data-id="([^"]+)"[^>]*data-settings="[^"]*background_background[^"]*"[^>]*>)', h):
    did = m.group(2)
    pos = m.end()
    line = h[:m.start()].count('\n') + 1
    
    # Find the matching closing tag by counting div opens/closes
    depth = 1
    i = pos
    while i < len(h) and depth > 0:
        next_open = h.find('<div', i)
        next_close = h.find('</div>', i)
        if next_open < 0:
            next_open = len(h)
        if next_close < 0:
            next_close = len(h)
        if next_open < next_close:
            depth += 1
            i = next_open + 1
        else:
            depth -= 1
            i = next_close + 1
    
    inner = h[pos:i]
    
    # Count widget types inside
    widgets = re.findall(r'data-widget_type="([^"]+)"', inner)
    has_spacer = 'spacer.default' in widgets
    only_spacer = all(w == 'spacer.default' for w in widgets) if widgets else False
    has_text = any(w in widgets for w in ['text-editor.default', 'heading.default', 'jkit_heading.default', 'icon-list.default'])
    
    # Is there an inline override already?
    tag = m.group(1)
    has_override = 'style="background-image' in tag
    
    bg_containers.append({
        'did': did, 'line': line, 'widgets': widgets,
        'has_spacer': has_spacer, 'only_spacer': only_spacer,
        'has_text': has_text, 'has_override': has_override
    })

print("=== ALL background_background containers ===\n")
print("Legend: [S]=has spacer, [O]=only spacer, [T]=has text, [DONE]=already overridden\n")

print("--- IMAGE SPACER containers (S + O, no text) ---")
for c in bg_containers:
    if c['only_spacer'] and not c['has_text']:
        override = ' [DONE]' if c['has_override'] else ' *** NEEDS IMAGE ***'
        print(f"  [{c['did']}] line {c['line']:4d}  widgets:{c['widgets']}{override}")

print("\n--- Mixed containers (have spacer + text or just background_color) ---")
for c in bg_containers:
    if not (c['only_spacer'] and not c['has_text']):
        override = ' [DONE]' if c['has_override'] else ''
        print(f"  [{c['did']}] line {c['line']:4d}  widgets:{c['widgets'][:3]}{override}")
