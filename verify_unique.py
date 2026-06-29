import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

print(f"Lorem count: {h.count('Lorem')}")
print(f"ipsum count: {h.count('ipsum')}")

# Vision vs Mission
vis = h.find('Visión//')
mis = h.find('Misión//')
if vis > 0:
    chunk = h[vis:vis+500]
    m = re.search(r'<p>(.*?)</p>', chunk)
    if m:
        print(f"\nVision text: {m.group(1)[:100]}")
if mis > 0:
    chunk = h[mis:mis+500]
    m = re.search(r'<p>(.*?)</p>', chunk)
    if m:
        print(f"Mission text: {m.group(1)[:100]}")

# Testimonial reviews
for m in re.finditer(r'"(.*?)"', h):
    t = m.group(1)
    if len(t) > 50 and ('Cristalex' in t or 'trabajo' in t or 'aberturas' in t):
        print(f"\nReview: {t[:100]}")

# Names
for name in ['Scarlett', 'Penelope', 'Madison', 'Valentina', 'María', 'Carlos', 'Laura', 'Roberto']:
    count = h.count('>' + name)
    if count:
        print(f"  Name '{name}': {count}x")
