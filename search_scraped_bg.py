"""
Search scraped.html for ALL background-image inline styles and CSS blocks.
The live-rendered scraped HTML should have Elementor's inline styles applied.
Also look for <img> tags we might have missed.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\Workspace\Assets\Cristalex\scraped.html', 'r', encoding='utf-8') as f:
    scraped = f.read()

print("=== ALL background-image in scraped.html ===\n")

seen_urls = set()
found = []

# In inline style attributes
for m in re.finditer(r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', scraped):
    url = m.group(1)
    if not re.search(r'\.(jpg|jpeg|png|webp|gif)', url, re.IGNORECASE):
        continue
    if url in seen_urls:
        continue
    seen_urls.add(url)
    
    line = scraped[:m.start()].count('\n') + 1
    fname = url.split('/')[-1].split('?')[0]
    
    # Get surrounding context - look for data-id
    before = scraped[max(0, m.start()-500):m.start()]
    data_ids = re.findall(r'data-id="([^"]+)"', before)
    did = data_ids[-1] if data_ids else '?'
    
    # Is it a logo?
    is_logo = 'Logo' in fname or 'logo' in fname
    
    found.append((line, did, fname, url, is_logo))
    print(f"  [{did}] line {line}: {'LOGO' if is_logo else '*** IMAGE ***'}")
    print(f"    file: {fname}")
    if not is_logo:
        print(f"    url:  {url[:120]}")
    print()

print(f"\nTotal image backgrounds found: {len(found)}")
print(f"Non-logo images: {sum(1 for f in found if not f[4])}")

# Now also look in <style> blocks within the HTML
print("\n=== background-image in <style> blocks ===\n")
for style_m in re.finditer(r'<style[^>]*>(.*?)</style>', scraped, re.DOTALL):
    style_content = style_m.group(1)
    for m in re.finditer(r'\.elementor-element-([\w]+)[^{]*\{[^}]*background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)', style_content):
        did = m.group(1)
        url = m.group(2)
        fname = url.split('/')[-1].split('?')[0]
        if fname not in seen_urls:
            seen_urls.add(fname)
            is_logo = 'Logo' in fname or 'logo' in fname
            print(f"  [{did}] {'LOGO' if is_logo else '*** IMAGE ***'}: {fname}")
            if not is_logo:
                print(f"    {url[:120]}")
