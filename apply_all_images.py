"""
Apply inline background-image styles to ALL containers with background_background
that don't already have an inline override.

Mapping:
- About section (lines 681-820): about_meeting.png
- Stats/counters (lines 894-1090): stats_aerial.png  
- Services outer cards (lines 1223, 1284): service_windows.png / service_iron.png
- Services inner spacers (lines 1347-1476): service_curtain.png / process_workshop.png
- Process section (1476+): process_workshop.png
- Testimonials (1833-2009): testimonial_bg.png
- Contact (2329): skip (just color)
- Logo bar (603): skip (just color)
"""
import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Map: data-id -> image file
# Based on line numbers and section context
image_map = {
    # About section
    '72528a92': 'img/about_meeting.png',      # About outer
    '105e5bf9': 'img/about_meeting.png',       # About text card
    '58f1bc62': 'img/about_install.png',       # Solicitar Presupuesto
    '4d8573f4': 'img/about_install.png',       # About inner
    'e649503':  'img/about_meeting.png',        # About inner 2
    'bc61578':  'img/stats_aerial.png',         # Nuestra Vision
    
    # Stats counters section
    '47ee2dbc': 'img/stats_aerial.png',        # Stats outer (Nuestra Mision heading) 
    '618aec9b': 'img/stats_aerial.png',        # Stats counter 1
    '6a77997':  'img/stats_aerial.png',         # Stats counter 2
    '2ede37be': 'img/stats_aerial.png',        # Stats counter 3
    
    # Service cards - outer containers
    '4f2deb07': 'img/service_windows.png',     # Aluminio card outer
    'b9b782':   'img/service_iron.png',         # Herreria card outer
    
    # Service cards - additional cards in row 2
    '307060b3': 'img/service_curtain.png',     # Cortinas de cristal card
    '412cb4d4': 'img/service_curtain.png',     # Cortinas inner
    '4de24b70': 'img/process_workshop.png',    # Another service card
    '50edb326': 'img/process_workshop.png',    # Another service inner
    
    # Process section
    '5527ea53': 'img/process_workshop.png',    # Process area
    
    # Testimonials
    '388ce8dd': 'img/testimonial_bg.png',      # Testimonial section outer
    '5f9ff871': 'img/testimonial_bg.png',      # Testimonial section 
    'aa4385b':  'img/testimonial_bg.png',       # Testimonial card 1 bg
    '23cfa9b3': 'img/testimonial_bg.png',      # Testimonial card 1 inner
    '48d07f4a': 'img/testimonial_bg.png',      # Testimonial card 2 bg
    '397cb9aa': 'img/testimonial_bg.png',      # Testimonial card 2 inner
    '56b132ec': 'img/about_install.png',       # FAQ area
    '5bd6c675': 'img/about_install.png',       # FAQ area inner
}

# Skip these (just background-color, no image needed)
skip_ids = {'58d11c5e', '6278343'}

count = 0
for did, img in image_map.items():
    pattern = f'data-id="{did}"'
    idx = content.find(pattern)
    if idx < 0:
        print(f"  WARNING: data-id={did} not found!")
        continue
    
    # Find the opening tag
    tag_start = content.rfind('<', 0, idx)
    tag_end = content.find('>', idx)
    tag = content[tag_start:tag_end+1]
    
    # Check if already has inline style with background-image
    if 'style="background-image' in tag or "style='background-image" in tag:
        print(f"  [{did}] already has inline override, skipping")
        continue
    
    # Add inline style just before the closing >
    style_attr = f' style="background-image:url(\'{img}\');background-size:cover;background-position:center;"'
    
    # Insert before the closing >
    new_tag = tag[:-1] + style_attr + '>'
    content = content[:tag_start] + new_tag + content[tag_end+1:]
    count += 1
    print(f"  [{did}] added background: {img}")

print(f"\nTotal overrides applied: {count}")

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File saved!")
