import re

file_path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# Find the logos/brands swiper section and inspect it
# ============================================================
# The original had swiper-slide items each with a logo image
# Look for swiper in general
swiper_idx = html.find('swiper-slide')
print(f"swiper-slide found at: {swiper_idx}")
if swiper_idx != -1:
    print(html[swiper_idx:swiper_idx+2000])

# Also look for the logo section by checking for data-id near the marquee/logo area
# The logo carousel section is usually near the top of the page
logo_markers = ['Logo1', 'Logo2', 'brand-logo', 'client-logo', 'partner', 'swiper']
for marker in logo_markers:
    idx = html.find(marker)
    if idx != -1:
        print(f"\n=== Found {marker!r} at {idx} ===")
        print(html[max(0,idx-100):idx+300])
