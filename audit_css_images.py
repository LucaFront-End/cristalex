"""
Extract ALL background-image URLs from the remote Elementor CSS (post-586.css)
and match them to their data-id containers to identify which sections still
show remote images.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

cssfile = r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\586\content.md'
with open(cssfile, 'r', encoding='utf-8') as f:
    css = f.read()

# Find ALL background-image URLs in the CSS
print("=== ALL background-image in post-586.css ===")
for m in re.finditer(r'elementor-element-([a-f0-9]+)\b[^{]*\{[^}]*background-image[^}]*url\(["\']?([^"\')\s]+)["\']?\)', css, re.DOTALL):
    did = m.group(1)
    url = m.group(2)
    fname = url.split('/')[-1]
    print(f"  [{did}]  {fname}")
    print(f"    {url}")
    print()

# Now check which of these data-ids have inline style overrides in the HTML
print("\n=== CHECKING WHICH ARE OVERRIDDEN IN HTML ===")
with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

for m in re.finditer(r'elementor-element-([a-f0-9]+)\b[^{]*\{[^}]*background-image[^}]*url\(["\']?([^"\')\s]+)["\']?\)', css, re.DOTALL):
    did = m.group(1)
    url = m.group(2)
    fname = url.split('/')[-1]
    
    # Check if this data-id has an inline style override
    pattern = f'data-id="{did}"'
    idx = html_content.find(pattern)
    if idx < 0:
        status = "NOT IN HTML"
    else:
        # Check nearby for inline style with background-image
        chunk = html_content[max(0, idx-200):idx+500]
        if "style=\"background-image" in chunk or "style='background-image" in chunk:
            status = "OVERRIDDEN (OK)"
        else:
            status = "*** STILL REMOTE - NEEDS OVERRIDE ***"
    
    print(f"  [{did}]  {status}  {fname}")
