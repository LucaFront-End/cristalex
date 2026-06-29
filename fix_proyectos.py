with open('proyectos.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix case study heading text
content = content.replace(
    'color: var(--color-white); margin-bottom: 15px;',
    'color: #111; margin-bottom: 15px;'
)
content = content.replace(
    'color: var(--color-white); margin: 0;',
    'color: #111; margin: 0;'
)
content = content.replace(
    'font-size: 13px; color: var(--color-white);',
    'font-size: 13px; color: #111;'
)
content = content.replace(
    'border-top: 1px solid rgba(255,255,255,0.06)',
    'border-top: 1px solid rgba(0,0,0,0.08)'
)

with open('proyectos.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated proyectos.html case study text colors')
