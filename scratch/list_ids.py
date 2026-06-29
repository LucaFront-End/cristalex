import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

print("=== IDS ===")
for m in re.finditer(r'id="([^"]+)"', h):
    line = h[:m.start()].count('\n') + 1
    print(f"Line {line}: id=\"{m.group(1)}\"")

print("\n=== HEADINGS ===")
for m in re.finditer(r'<h([1-6])[^>]*>(.*?)</h\1>', h, re.DOTALL):
    line = h[:m.start()].count('\n') + 1
    text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    print(f"Line {line}: H{m.group(1)} -> {text}")
