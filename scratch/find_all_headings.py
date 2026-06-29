import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

content = "".join(lines)

print("=== HEADINGS ===")
# Find all h2, h3, h4
for i, line in enumerate(lines):
    line_num = i + 1
    if '<h2' in line or '<h3' in line or '<h4' in line or 'elementor-icon-list-text' in line:
        clean_line = line.strip()
        if len(clean_line) < 200:
            print(f"L{line_num:4d}: {clean_line}")
        else:
            print(f"L{line_num:4d}: {clean_line[:150]}...")
