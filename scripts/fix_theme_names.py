import os

# Mapping of theme directory name -> (English Title from previous script, Chinese Name)
THEME_MAP = {
    'home': ('Home', '家中'),
    'occupation': ('Occupation', '職業'),
    'picnic': ('Picnic', '野餐'),
    'playground': ('Playground', '遊樂場'),
    'restaurant': ('Restaurant', '餐廳'),
    'school': ('School', '學校'),
    'sportcentre': ('Sportcentre', '運動中心'),
    # For supermarket, we ensure consistency.
    'supermarket': ('Supermarket', '超級市場') 
}

BASE_DIR = r"c:\Users\kckwok\Desktop\ICHTP\app\templates\games"

def fix_file(file_path, eng_name, chi_name):
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}, not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content
    
    # Update Welcome Message
    # Current state: Most files generated from Supermarket template still say "歡迎來到超級市場".
    # We want: "歡迎來到{chi_name}篇"
    
    if 'supermarket' in file_path.lower():
        # Specifically for the Supermarket theme file
        # If it says "歡迎來到超級市場。", update to "歡迎來到超級市場篇。" for consistency
        # Avoid double "篇" if run multiple times
        if "歡迎來到超級市場。" in new_content:
             new_content = new_content.replace("歡迎來到超級市場。", "歡迎來到超級市場篇。")
    else:
        # For other themes (home, school, etc.)
        # They currently have "歡迎來到超級市場" (inherited from template).
        # We replace it with the correct theme name.
        if "歡迎來到超級市場" in new_content:
            new_content = new_content.replace("歡迎來到超級市場", f"歡迎來到{chi_name}篇")
            
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes for {file_path}")

for theme_dir, (eng, chi) in THEME_MAP.items():
    # Only index.html has the "Welcome" message needed for this fix.
    # Game files were verified to be correct in previous steps.
    fix_file(os.path.join(BASE_DIR, theme_dir, "index.html"), eng, chi)
