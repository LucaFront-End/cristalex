import re

file_path = r'd:\Workspace\Assets\Cristalex\index.html'
with open(file_path, 'rb') as f:
    data = f.read()

text = data.decode('utf-8', errors='replace')

# Check file stats
print(f"File size: {len(data)} bytes, {len(text)} chars")
print(f"Total lines: {text.count(chr(10))}")

# Find the â€œ sequences (curly quotes showing as mojibake)
# In UTF-8: left curly quote = 0xE2 0x80 0x9C
# In Latin-1 misread as: â€œ
# But our file is UTF-8 - so if we see these chars it means the source had
# latin-1 curly quotes that got treated as something else

bad_seqs = [
    (b'\xe2\x80\x9c', 'LEFT CURLY QUOTE'),
    (b'\xe2\x80\x9d', 'RIGHT CURLY QUOTE'),
    (b'\xe2\x80\x99', 'RIGHT SINGLE QUOTE'),
    (b'\xe2\x80\x94', 'EM DASH'),
    (b'\xe2\x80\x93', 'EN DASH'),
]

for seq, name in bad_seqs:
    count = data.count(seq)
    if count > 0:
        idx = data.find(seq)
        ctx = data[max(0,idx-50):idx+100].decode('utf-8', errors='replace').replace('\n', ' ')
        print(f"{name} x{count}: {ctx[:150]}")

# Find testimonials area
testi_pos = text.find('Testimoni')
if testi_pos != -1:
    chunk = text[testi_pos:testi_pos+4000]
    print("\n=== TESTIMONIAL CHUNK (first 2000 chars) ===")
    print(chunk[:2000])

# Check if images broke things - look for img src patterns
print("\n=== IMAGE SRCS ===")
for m in re.finditer(r'src="([^"]{0,120})"', text):
    src = m.group(1)
    if 'unsplash' in src or 'templatekit' in src or 'wp-content' in src:
        print(src[:100])
