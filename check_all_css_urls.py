"""
Extract ALL image URLs from ALL Elementor CSS files (post-586, post-523, post-528, post-5)
to find which backgrounds come from remote and still show the original template images.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

css_files = [
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\586\content.md', 'post-586 (main page)'),
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\623\content.md', 'post-523'),
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\669\content.md', 'post-528'),
    (r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\715\content.md', 'post-5 (header/footer)'),
]

print("ALL image URLs from remote CSS files:")
print("=" * 80)
for cssfile, label in css_files:
    with open(cssfile, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Find ALL url() references to image files
    urls = re.findall(r'url\(["\']?([^"\')\s]+\.(jpg|jpeg|png|webp|gif))["\']?\)', css, re.IGNORECASE)
    if urls:
        print(f"\n{label}:")
        for url, ext in urls:
            fname = url.split('/')[-1]
            print(f"  {fname}")
            print(f"    {url}")
    else:
        print(f"\n{label}: No image URLs")
