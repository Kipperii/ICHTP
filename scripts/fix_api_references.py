import os

# Define path relative to this script
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "templates", "games")

# List of themes to fix (excluding restaurant, which is the source)
THEMES = ['home', 'occupation', 'picnic', 'playground', 'school', 'sportcentre', 'supermarket']

def fix_theme_api(theme):
    # Path to the specific game file
    file_path = os.path.join(BASE_DIR, theme, "g1-1", f"game_{theme}_g1-1_find_same.html")
    
    if not os.path.exists(file_path):
        print(f"[SKIP] {theme}: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The incorrect line copied from restaurant looks like:
    # const response = await fetch('/api/games/restaurant/images');
    
    incorrect_str = "fetch('/api/games/restaurant/images')"
    correct_str = f"fetch('/api/games/{theme}/images')"
    
    if incorrect_str in content:
        new_content = content.replace(incorrect_str, correct_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[FIXED] {theme}: Updated API reference to {correct_str}")
    
    elif correct_str in content:
        print(f"[OK] {theme}: API reference is already correct.")
    else:
        # Fallback for single quotes or spaces variations if strict match fails (though grep showed strict match)
        print(f"[WARNING] {theme}: Could not find the expected fetch string. Manual check required.")

if __name__ == "__main__":
    print(f"Scanning for incorrect API references in: {BASE_DIR}")
    for theme in THEMES:
        fix_theme_api(theme)
    print("Done.")
