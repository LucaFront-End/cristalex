import re, sys

file_path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(file_path, 'rb') as f:
    data = f.read()

# Print as ASCII safe
def safe_print(s):
    print(s.encode('ascii', 'replace').decode('ascii'))

text = data.decode('utf-8', errors='replace')

safe_print(f"File size: {len(data)} bytes, {len(text.splitlines())} lines")

# Count how many times key sections appear - check for duplication
key_markers = ['elementor-586', 'elementor-523', 'elementor-528', '<html', '<body', '<head']
for m in key_markers:
    c = text.count(m)
    safe_print(f"  {m}: {c} occurrences")

# Find the curly quotes in bytes
for seq, name in [
    (b'\xe2\x80\x9c', 'LEFT_DQ'),
    (b'\xe2\x80\x9d', 'RIGHT_DQ'),
    (b'\xe2\x80\x99', 'RIGHT_SQ'),
]:
    idx = 0
    while True:
        idx = data.find(seq, idx)
        if idx == -1:
            break
        ctx = data[max(0,idx-60):idx+80].decode('ascii', errors='replace').replace('\n', ' ')
        safe_print(f"{name} at {idx}: {ctx[:150]}")
        idx += 1

# Check images
safe_print("\n=== IMG SRCS (first 20) ===")
count = 0
for m in re.finditer(rb'src="([^"]+)"', data):
    src = m.group(1).decode('ascii', errors='replace')
    if count < 20:
        safe_print(f"  {src[:100]}")
    count += 1
safe_print(f"  ... total img/src attributes: {count}")

# Check what testimonial text looks like
testi_idx = text.find('Testimoni')
if testi_idx != -1:
    chunk = text[testi_idx:testi_idx+2000]
    chunk_safe = chunk.encode('ascii', 'replace').decode('ascii').replace('\r','').replace('\t','')
    # Print only lines with actual text content
    for line in chunk_safe.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('<') and not stripped.startswith('//') and len(stripped) > 3:
            safe_print(f"  TESTI_TEXT: {stripped[:100]}")
