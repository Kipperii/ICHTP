import os
import re

SOURCE_FILE = "app/templates/games/restaurant/g1-1/game_restaurant_g1-1_find_same.html"
TARGET_DIR = "app/templates/games"

def read_source():
    print(f"Reading source: {SOURCE_FILE}")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Header Part 1 (Start -> <title>)
    title_start = content.find("<title>")
    if title_start == -1: raise Exception("No title tag in source")
    header_part_1 = content[:title_start + 7] # Include <title>
    
    # 2. Header Part 2 (</title> -> const RESTAURANT_THEME_URL)
    title_end = content.find("</title>")
    # Find start of theme url line
    theme_url_match = re.search(r'const RESTAURANT_THEME_URL = .*?;', content)
    if not theme_url_match: raise Exception("No RESTAURANT_THEME_URL in source")
    
    header_part_2 = content[title_end:theme_url_match.start()]
    
    # 3. Logic Block (Start after ALL_IMAGES commented block -> End)
    # We look for "const rp =" as the reliable start marker of logic
    # Note: earlier we found duplicating const rp, so we must be careful. 
    # But restaurant file is clean now.
    logic_start_match = re.search(r'const rp =', content)
    if not logic_start_match: raise Exception("No logic start (const rp) in source")
    
    logic_block = content[logic_start_match.start():]
    
    # Replace RESTAURANT_THEME_URL with generic THEME_URL in logic block
    logic_block = logic_block.replace("RESTAURANT_THEME_URL", "THEME_URL")
    
    return header_part_1, header_part_2, logic_block

def process_theme(theme, header1, header2, logic_block):
    filepath = os.path.join(TARGET_DIR, theme, "g1-1", f"game_{theme}_g1-1_find_same.html")
    if not os.path.exists(filepath):
        print(f"Skipping {theme} (File not found)")
        return
        
    print(f"Processing {theme}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract Title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title_text = title_match.group(1) if title_match else f"{theme} G1-1"
    
    # Extract Theme URL Value
    # Look for const X_THEME_URL = "/games/X";
    url_match = re.search(r'const \w+_THEME_URL = "(.*?)";', content)
    if not url_match:
        print(f"  [Warning] Could not find theme URL variable in {theme}. Using default.")
        theme_url_value = f"/games/{theme}"
    else:
        theme_url_value = url_match.group(1)
        
    # Extract TEXTS object
    texts_match = re.search(r'const TEXTS = \{[\s\S]*?\};', content)
    if not texts_match:
        print(f"  [Error] Could not find TEXTS object in {theme}")
        return
    texts_block = texts_match.group(0)
    
    # Assemble New Content
    # We use header1 (Start..<title>) + title_text + header2 (</title>...before URL)
    # Then inject standard THEME_URL
    # Then inject original TEXTS
    # Then inject logic
    
    new_content = (
        header1 + 
        title_text + 
        header2 + 
        f'const THEME_URL = "{theme_url_value}";\n\n      ' + 
        texts_block + 
        '\n\n      // 素材清單 (此陣列將由 API 動態填充)\n      let ALL_IMAGES = [];\n      /*\n      const ALL_IMAGES = [\n        "images/41.jpg", ...\n      ];\n      */\n\n      ' +
        logic_block
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  [Success] Updated {theme}")

def main():
    try:
        h1, h2, logic = read_source()
        themes = ["school", "home", "occupation", "picnic", "playground", "sportcentre", "supermarket"]
        
        for theme in themes:
            process_theme(theme, h1, h2, logic)
    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    main()
