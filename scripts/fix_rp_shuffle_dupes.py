import os
import re

HEADER_PATH = "app/templates/games"

def fix_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    rp_count = 0
    in_function_shuffle = False
    brace_depth = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 1. Handle duplicate 'const rp ='
        if stripped.startswith("const rp ="):
            rp_count += 1
            if rp_count > 1:
                print(f"  [Fix] Removing duplicate 'const rp' at line {i+1}")
                continue # Skip writing this line
        
        # 2. Handle 'function shuffle(arr)' which conflicts with 'const shuffle'
        # Only if it appears later in the file (the original is usually near top)
        if stripped.startswith("function shuffle(arr) {") and i > 100:
            print(f"  [Fix] Found 'function shuffle' at line {i+1}. Removing block.")
            in_function_shuffle = True
            brace_depth = 1
            continue
            
        if in_function_shuffle:
            # Count braces to find end of function
            brace_depth += line.count('{')
            brace_depth -= line.count('}')
            if brace_depth <= 0:
                in_function_shuffle = False
                print(f"  [Fix] 'function shuffle' block ended at line {i+1}")
            continue # Skip the lines inside the function
            
        new_lines.append(line)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    # Scan all themes to be sure
    for theme in os.listdir(HEADER_PATH):
        theme_path = os.path.join(HEADER_PATH, theme)
        if not os.path.isdir(theme_path):
            continue
            
        g1_path = os.path.join(theme_path, "g1-1")
        if not os.path.isdir(g1_path):
            continue
            
        for fname in os.listdir(g1_path):
            if fname.endswith("find_same.html"):
                full_path = os.path.join(g1_path, fname)
                fix_file(full_path)

if __name__ == "__main__":
    main()
