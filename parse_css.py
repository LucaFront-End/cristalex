import re

with open(r'C:\Users\lucad\.gemini\antigravity-ide\brain\18244748-0808-49f9-b8ac-b0ae5bfd77d4\.system_generated\steps\586\content.md', 'r', encoding='utf-8') as f:
    css = f.read()

# Find all background-image rules with their selector
pattern = re.compile(r'\.elementor-element\.elementor-element-([a-f0-9]+)\s*\{[^}]*background-image:\s*url\("([^"]+)"', re.DOTALL)
for m in pattern.finditer(css):
    print(f'[{m.group(1)}]')
    print(f'  {m.group(2)}')
    print()
