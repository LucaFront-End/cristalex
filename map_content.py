import re

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find ALL Lorem ipsum occurrences and their surrounding context
lorem_pattern = re.compile(r'Lorem ipsum[^<]*')
for m in lorem_pattern.finditer(h):
    pos = m.start()
    # Get nearby section context
    before = h[max(0,pos-500):pos]
    # Find closest section label
    label_match = re.search(r'elementor-icon-list-text[^>]*>([^<]+)<', before)
    heading_match = re.search(r'heading-title[^>]*>([^<]{3,50})', before)
    data_id_match = re.findall(r'data-id="([^"]+)"', before)
    section = data_id_match[-1] if data_id_match else '?'
    label = label_match.group(1).strip() if label_match else ''
    heading = heading_match.group(1).strip()[:40] if heading_match else ''
    
    text = m.group(0)[:80]
    print(f"[{section}] {label or heading or '???'}")
    print(f"  {text}")
    print()

# Also find Archryze Vision/Mission
print("=== VISION/MISSION ===")
for keyword in ['Vission', 'Mission']:
    idx = h.find(keyword)
    if idx != -1:
        chunk = h[idx:idx+500]
        # Find the Lorem ipsum after it
        lorem = re.search(r'<p>(.*?)</p>', chunk)
        if lorem:
            print(f"{keyword}: {lorem.group(1)[:100]}")
        print()

# Find testimonials
print("=== TESTIMONIALS ===")
for m in re.finditer(r'&#8220;(.*?)&#8221;', h, re.DOTALL):
    print(f"  Review: {m.group(1)[:100]}")
