import re

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find all <i> tags with class attributes
icons = set()
for m in re.finditer(r'<i\s[^>]*class="([^"]*)"[^>]*>\s*</i>', h):
    cls = m.group(1).strip()
    icons.add(cls)

print("=== ALL <i> ICON CLASSES ===")
for ic in sorted(icons):
    print(f"  {ic}")
    # Count occurrences
    count = h.count(f'class="{ic}"')
    print(f"    count: {count}")
