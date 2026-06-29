import os, re

files = ['index.html', 'nosotros.html', 'servicios.html', 'proyectos.html', 'contacto.html']
base_dir = r'd:\Workspace\Assets\Cristalex'

print("=== AUDITING HTML FILES ===")
errors = 0

for file_name in files:
    path = os.path.join(base_dir, file_name)
    if not os.path.exists(path):
        print(f"ERROR: File {file_name} does not exist!")
        errors += 1
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nAuditing {file_name} ({len(content)} chars):")
    
    # Check for linked CSS
    if 'cristalex-custom.css' not in content:
        print(f"  WARNING: cristalex-custom.css not linked in {file_name}")
    else:
        print("  [OK] cristalex-custom.css linked")
        
    # Check for the updated address
    if 'San Nicolás 4148' not in content and 'San Nicolas 4148' not in content:
        print(f"  ERROR: Address not found or outdated in {file_name}")
        errors += 1
    else:
        print("  [OK] Address updated successfully")
        
    # Check for social links
    if 'tiktok.com/@cristalex.aberturas' not in content:
        print(f"  WARNING: TikTok link outdated or missing in {file_name}")
    else:
        print("  [OK] TikTok link correct")
        
    if 'facebook.com/construccionesvidriadas' not in content:
        print(f"  WARNING: Facebook link outdated or missing in {file_name}")
    else:
        print("  [OK] Facebook link correct")
        
    # Check navigation links
    nav_links = re.findall(r'href="([^"]+\.html)"', content)
    unique_nav = set(nav_links)
    print(f"  [OK] Found navigation links: {unique_nav}")
    
    # Check if there are hash links that might be broken
    hash_links = re.findall(r'href="(#[a-zA-Z0-9_-]+)"', content)
    for hl in hash_links:
        target_id = hl[1:]
        if f'id="{target_id}"' not in content and f"id='{target_id}'" not in content:
            print(f"  WARNING: Broken hash link {hl} (id=\"{target_id}\" not found in this file)")

if errors == 0:
    print("\n[SUCCESS] Audit completed successfully with NO ERRORS!")
else:
    print(f"\nAudit completed with {errors} errors.")

