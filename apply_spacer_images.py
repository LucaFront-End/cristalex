"""
Apply inline background-image ONLY to the 10 true image-spacer containers.
These are containers identified as containing ONLY a spacer.default widget.
"""
import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Only true image-spacer containers and their images
image_map = {
    # About section
    'e649503':  'img/about_vision.png',     # Nuestra Vision thumbnail
    'bc61578':  'img/about_mission.png',    # Nuestra Mision thumbnail
    
    # Stats section - right side large image
    '2ede37be': 'img/stats_right.png',      # Stats large image
    
    # Service cards - ONLY the inner image spacers
    '5d6cda97': 'img/service_windows.png',  # Service 1 (aluminum) image
    '5b218d5a': 'img/service_iron.png',     # Service 2 (iron) image
    '412cb4d4': 'img/service_curtain.png',  # Service 3 image
    '50edb326': 'img/process_workshop.png', # Service 4 image
    
    # Testimonial avatars
    'aa4385b':  'img/testimonial_person.png',  # Testimonial 1 avatar
    '48d07f4a': 'img/testimonial_person.png',  # Testimonial 2 avatar
    
    # FAQ left image
    '56b132ec': 'img/faq_building.png',     # FAQ left side image
}

count = 0
for did, img in image_map.items():
    pattern = f'data-id="{did}"'
    idx = content.find(pattern)
    if idx < 0:
        print(f"  WARNING: data-id={did} not found!")
        continue
    
    # Find the opening tag that contains this data-id
    tag_start = content.rfind('<', 0, idx)
    tag_end = content.find('>', idx)
    tag = content[tag_start:tag_end+1]
    
    # Skip if already has inline background-image override
    if 'style="background-image' in tag:
        print(f"  [{did}] already overridden, skipping")
        continue
    
    # Add inline style before the closing >
    style = f' style="background-image:url(\'{img}\');background-size:cover;background-position:center center;"'
    new_tag = tag[:-1] + style + '>'
    content = content[:tag_start] + new_tag + content[tag_end+1:]
    count += 1
    print(f"  [{did}] -> {img}")

print(f"\nApplied: {count} image overrides")

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved!")
