"""
Remove ALL wrongly added inline background-image styles from containers.
KEEP ONLY the 2 correct hero overrides:
- 79d2b749 (hero sky)
- 65a79589 (building canopy)
"""
import re

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# IDs to KEEP (correct hero overrides)
keep_ids = {'79d2b749', '65a79589'}

# Also remove the wrongly added service card overrides from inner spacers
# that we set on 5d6cda97 and 5b218d5a

count_removed = 0

def remove_inline_bg(tag, did):
    """Remove style="background-image:..." from a tag if present."""
    new_tag = re.sub(r'\s+style="background-image:[^"]*"', '', tag)
    return new_tag

# Find all tags that have inline background-image style
# Pattern: any opening tag containing data-id="..." AND style="background-image:..."
pattern = re.compile(
    r'(<[a-zA-Z][^>]*data-id="([^"]+)"[^>]*style="background-image:[^"]*"[^>]*>)',
    re.DOTALL
)

def replacer(m):
    global count_removed
    full_tag = m.group(1)
    did = m.group(2)
    
    if did in keep_ids:
        return full_tag  # Keep hero overrides
    
    # Remove the style attribute
    new_tag = re.sub(r'\s*style="background-image:[^"]*"', '', full_tag)
    count_removed += 1
    print(f"  Removed style from [{did}]")
    return new_tag

new_content = pattern.sub(replacer, content)

# Also handle tags where style comes BEFORE data-id
pattern2 = re.compile(
    r'(<[a-zA-Z][^>]*style="background-image:[^"]*"[^>]*data-id="([^"]+)"[^>]*>)',
    re.DOTALL
)

def replacer2(m):
    global count_removed
    full_tag = m.group(1)
    did = m.group(2)
    
    if did in keep_ids:
        return full_tag
    
    new_tag = re.sub(r'\s*style="background-image:[^"]*"', '', full_tag)
    count_removed += 1
    print(f"  Removed style from [{did}] (style before data-id)")
    return new_tag

new_content = pattern2.sub(replacer2, new_content)

print(f"\nTotal inline bg styles removed: {count_removed}")
print("Kept: 79d2b749 (hero), 65a79589 (building canopy)")

with open(r'd:\Workspace\Assets\Cristalex\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("File saved!")

# Verify
remaining = re.findall(r'data-id="([^"]+)"[^>]*style="background-image', new_content)
remaining += re.findall(r'style="background-image[^"]*"[^>]*data-id="([^"]+)"', new_content)
print(f"\nRemaining inline bg-image overrides: {remaining}")
