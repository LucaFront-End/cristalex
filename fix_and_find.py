"""
1. Fix testimonial 2 avatar to use a different image
2. Find exact lines for the projects GRID section (394a0e70) to replace
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Fix testimonial 2 (48d07f4a) - change from testimonial_person.png to testimonial_female2.png
# The tag is something like: data-id="48d07f4a" ... style="background-image:url('img/testimonial_person.png')..."
old = "data-id=\"48d07f4a\""
idx = h.find(old)
if idx >= 0:
    tag_start = h.rfind('<', 0, idx)
    tag_end = h.find('>', idx)
    tag = h[tag_start:tag_end+1]
    new_tag = tag.replace("url('img/testimonial_person.png')", "url('img/testimonial_female2.png')")
    h = h[:tag_start] + new_tag + h[tag_end+1:]
    print("Fixed testimonial 2 avatar")

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'w', encoding='utf-8') as f:
    f.write(h)

# Now find the exact lines for the projects grid section (394a0e70)
idx2 = h.find('data-id="394a0e70"')
if idx2 >= 0:
    line_start = h[:idx2].count('\n') + 1
    # Find its parent opening tag
    parent_start = h.rfind('<div', 0, idx2)
    # Count to closing tag
    depth = 1
    i = h.find('>', idx2) + 1
    while i < len(h) and depth > 0:
        no = h.find('<div', i)
        nc = h.find('</div>', i)
        if no < 0: no = len(h)
        if nc < 0: nc = len(h)
        if no < nc:
            depth += 1
            i = no + 1
        else:
            depth -= 1
            i = nc + 6
    line_end = h[:i].count('\n') + 1
    print(f"Projects grid section 394a0e70: lines {line_start} to {line_end}")
    print(f"(parent <div from line {h[:parent_start].count(chr(10)) + 1})")
