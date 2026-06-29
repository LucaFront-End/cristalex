import re

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find all accordion items
print("===== ACCORDION TITLES =====")
for m in re.finditer(r'e-n-accordion-item-title-text">\s*(.*?)\s*</div>', h):
    print(f"  Title: [{m.group(1).strip()}]")

# Find accordion answers  
print("\n===== ACCORDION ANSWERS =====")
for m in re.finditer(r'role="region"(.*?)</section>', h, re.DOTALL):
    chunk = m.group(1)
    p = re.search(r'<p>(.*?)</p>', chunk, re.DOTALL)
    if p:
        print(f"  Answer: {p.group(1).strip()[:120]}")

# Find testimonial structure
print("\n===== TESTIMONIAL STRUCTURE =====")
testi_start = h.find('&#8220;')
if testi_start > 0:
    chunk = h[testi_start-200:testi_start+500]
    # Show data-ids
    for did in re.finditer(r'data-id="([^"]+)"', chunk):
        print(f"  data-id: {did.group(1)}")
    # Show the actual quote
    quote = re.search(r'&#8220;(.*?)&#8221;', chunk, re.DOTALL)
    if quote:
        print(f"  Quote1: {quote.group(1)[:100]}")

testi2 = h.find('&#8220;', testi_start+1)
if testi2 > 0:
    chunk2 = h[testi2:testi2+300]
    quote2 = re.search(r'&#8220;(.*?)&#8221;', chunk2, re.DOTALL)
    if quote2:
        print(f"  Quote2: {quote2.group(1)[:100]}")

# Find FAQ section heading
print("\n===== FAQ HEADING =====")
faq_idx = h.find('Common')
if faq_idx > 0:
    print(f"  {h[faq_idx:faq_idx+80]}")

# Also check what headings the accordion has
print("\n===== ALL HEADINGS IN FAQ AREA =====")
faq_area_start = h.find('e-n-accordion')
if faq_area_start > 0:
    faq_area = h[faq_area_start:faq_area_start+5000]
    for m in re.finditer(r'heading-title[^>]*>(.*?)</h', faq_area):
        print(f"  Heading: {m.group(1).strip()[:80]}")
    for m in re.finditer(r'title-text">\s*(.*?)\s*</div>', faq_area):
        print(f"  AccTitle: [{m.group(1).strip()}]")
