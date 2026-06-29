import re

for cssfile, label in [
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\623\content.md', 'post-523'),
]:
    with open(cssfile, 'r', encoding='utf-8') as f:
        css = f.read()
    print(f"=== {label} ===")
    for m in re.finditer(r'elementor-element-([a-f0-9]+)[^{]*\{[^}]*background-image[^}]*url\("?([^")\s]+)"?', css):
        print(f"  [{m.group(1)}] {m.group(2).split('/')[-1]}")
