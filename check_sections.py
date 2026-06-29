import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# ===== TESTIMONIALS =====
print("===== TESTIMONIALS =====")
# Find the testimonial section
testi_idx = h.find('Opiniones de')
if testi_idx < 0:
    testi_idx = h.find('feedback')
if testi_idx < 0:
    testi_idx = h.find('testimonial')
print(f"Testimonial heading at: {testi_idx}")

# Find all review quotes (look for text between quote marks or in review containers)
# The original uses &#8220; and &#8221; for curly quotes
for marker in ['&#8220;', '\u201c', '"Excelente', '"Contratamos']:
    positions = []
    idx = 0
    while True:
        idx = h.find(marker, idx)
        if idx < 0: break
        positions.append(idx)
        idx += 1
    if positions:
        print(f"\n  '{marker[:20]}' found {len(positions)}x")
        for pos in positions[:3]:
            print(f"    at {pos}: {h[pos:pos+120]}")

# Look for the actual testimonial text containers
print("\n--- Testimonial text containers ---")
for m in re.finditer(r'data-widget_type="text-editor\.default"', h):
    pos = m.end()
    # Get next 500 chars
    chunk = h[pos:pos+500]
    # Find <p> content
    p = re.search(r'<p>(.*?)</p>', chunk, re.DOTALL)
    if p:
        text = p.group(1).strip()
        if len(text) > 20:
            # Check if near testimonials
            before = h[max(0,pos-2000):pos]
            if 'testimonial' in before.lower() or 'review' in before.lower() or 'feedback' in before.lower() or 'quote' in before.lower() or 'Opiniones' in before:
                print(f"  TESTI TEXT: {text[:100]}")

# ===== FAQ =====
print("\n\n===== FAQ =====")
# Find accordion items
for m in re.finditer(r'e-n-accordion-item-title-text">\s*(.*?)\s*</div>', h):
    print(f"  Q: {m.group(1).strip()[:80]}")

# Find accordion answer content
for m in re.finditer(r'role="region".*?<p>(.*?)</p>', h, re.DOTALL):
    text = m.group(1).strip()
    if len(text) > 10:
        print(f"  A: {text[:100]}")
