import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Extract all visible text between > and <
texts = re.findall(r'>([^<]{3,300})<', h)
problems = []
for t in texts:
    s = t.strip()
    if not s or len(s) < 3:
        continue
    # Skip JS/CSS/code/markup
    if any(x in s for x in ['{', '}', '//', '/*', '.css', '.js', 'elementor', 'data-', 'class=',
                             'style=', 'http', 'width:', 'height:', 'margin', 'padding', 'border',
                             'color:', 'font-', 'display:', 'position:', 'content:', '@media',
                             'background', '0px', 'calc(', 'rgba', 'wp-', 'plugin', 'assets',
                             'script', 'function', 'var ', 'const ', 'let ', 'return', 'window.',
                             'document.', 'jQuery', 'true', 'false', 'null', 'undefined',
                             'querySelector', 'addEventListener', 'classList', 'innerHTML',
                             'breakpoints', 'swiper', 'config', 'rest_', 'nonce',
                             'sourceURL', 'use strict', 'ready(', '.on(', 'animate']):
        continue
    # Skip if all numbers/symbols
    if not any(c.isalpha() for c in s):
        continue
    # Check for English/Lorem
    english_words = ['the', 'and', 'for', 'with', 'that', 'from', 'our', 'your', 'this',
                     'are', 'have', 'has', 'will', 'can', 'all', 'each', 'how', 'what',
                     'when', 'where', 'which', 'who', 'about', 'into', 'through',
                     'Lorem', 'ipsum', 'dolor', 'amet', 'consectetur', 'adipiscing',
                     'elit', 'sed', 'eiusmod', 'tempor', 'incididunt', 'labore',
                     'magna', 'aliqua', 'enim', 'minim', 'veniam', 'quis', 'nostrud',
                     'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip',
                     'Design', 'Architecture', 'Building', 'Project', 'Client',
                     'Read', 'More', 'Learn', 'View', 'See', 'Get', 'Started',
                     'Subscribe', 'Newsletter', 'Follow', 'Quick', 'Links',
                     'Privacy', 'Policy', 'Terms', 'Rights', 'Reserved',
                     'Submit', 'Send', 'Message', 'Name', 'Email', 'Phone',
                     'Address', 'Search', 'Menu', 'Close', 'Open', 'Next', 'Previous',
                     'innovative', 'modern', 'creative', 'spaces', 'timeless',
                     'sustainable', 'excellence', 'commitment', 'crafting',
                     'We ', 'Our ', 'An ', 'The ', 'In ', 'At ', 'On ', 'To ',
                     'By ', 'Is ', 'It ', 'As ', 'If ', 'Or ', 'So ',
                     'architectural', 'residential', 'commercial',
                     'every', 'combines', 'reflects', 'ensure', 'seamless',
                     'provides', 'offers', 'includes', 'features',
                     'process', 'approach', 'strategy', 'solution', 'service',
                     'quality', 'experience', 'professional', 'expert',
                     'answer', 'question', 'asked', 'frequently',
                     'testimonial', 'feedback', 'review', 'rating']
    
    s_lower = s.lower()
    # Check if has Spanish accents -> likely already translated
    has_spanish = any(c in s for c in 'áéíóúñü¿¡')
    
    found_english = []
    for ew in english_words:
        ew_l = ew.lower()
        if ew_l in s_lower.split() or (len(ew_l) > 4 and ew_l in s_lower):
            found_english.append(ew)
    
    if found_english and not has_spanish:
        problems.append((s[:120], found_english[:5]))

# Deduplicate
seen = set()
for text, words in problems:
    if text not in seen:
        seen.add(text)
        print(f"  [{', '.join(words[:3])}] {text}")

print(f"\nTotal: {len(seen)} texts still in English/Lorem")
