"""
Match each un-overridden data-id to its section context by reading surrounding HTML.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Get all un-overridden background containers
no_override = []
for m in re.finditer(r'data-id="([^"]+)"[^>]*data-settings="([^"]*background_background[^"]*)"', html_content):
    did = m.group(1)
    pos = m.start()
    tag_end = html_content.find('>', pos)
    tag = html_content[pos:tag_end+1]
    has_override = 'style="background-image' in tag
    if not has_override:
        line = html_content[:pos].count('\n') + 1
        no_override.append((did, line, pos))

# For each, find nearest heading/text to identify section
for did, line, pos in no_override:
    # Look forward 800 chars for headings, spans, text
    chunk = html_content[pos:pos+800]
    headings = re.findall(r'<h\d[^>]*>(.*?)</h\d>', chunk, re.DOTALL)
    heading_text = re.sub(r'<[^>]+>', '', headings[0]).strip()[:60] if headings else ''
    
    spans = re.findall(r'class="elementor-icon-list-text">([^<]+)<', chunk)
    span_text = spans[0] if spans else ''
    
    # Look backward to find parent section
    before = html_content[max(0, pos-1500):pos]
    parent_headings = re.findall(r'<h\d[^>]*>(.*?)</h\d>', before, re.DOTALL)
    parent_text = re.sub(r'<[^>]+>', '', parent_headings[-1]).strip()[:40] if parent_headings else ''
    
    context = heading_text or span_text or parent_text or '???'
    print(f"[{did}] line {line:4d}  ->  {context}")
