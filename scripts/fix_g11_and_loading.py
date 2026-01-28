import os
import re

files = [
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\home\g1-1\game_home_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\occupation\g1-1\game_occupation_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\picnic\g1-1\game_picnic_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\playground\g1-1\game_playground_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\restaurant\g1-1\game_restaurant_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\school\g1-1\game_school_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\sportcentre\g1-1\game_sportcentre_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\supermarket\g1-1\game_supermarket_g1-1_find_same.html'
]

# 1. Fix Duplicates
# The subagent found duplication of `const rp = ...`.
# We need to ensure `rp`, `shuffle`, `makeButton` etc are defined exactly once.
# The previous script might have blindly inserted them even if a variant existed.

def fix_duplicates(content):
    # Regex to find all occurrences of `const rp =`
    rp_matches = list(re.finditer(r'const rp =', content))
    if len(rp_matches) > 1:
        print(f"Found {len(rp_matches)} definitions of 'rp', fixing...")
        
        # We keep the first one and remove subsequent blocks of helpers?
        # Or remove the one we inserted later (which was likely prepended to SceneMenu)?
        # Let's try to remove ONLY the block we likely inserted if it's duplicate.
        
        # The block we inserted started with:
        # // ---------------- 輔助函式 ----------------
        # const rp = (arr) => arr[Math.floor(Math.random() * arr.length)];
        
        # If we see this exact string twice, remove the second one.
        # But maybe they are slightly different.
        
        # It's safer to just comment out or remove the second definition.
        
        pass # We will do it in a robust way below
        
    return content

# 2. Add Percentage to Loading
# Find: text.setText(TEXTS.loading)
# Replace with: this.load.on('progress', (p) => { 
#                  const percent = Math.floor(p * 100);
#                  this.loadingText.setText(`${TEXTS.loading} ${percent}%`);
#               });

loading_logic_old = """          this.add
            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading, {
              font: "28px Arial",
              fill: "#fff",
            })
            .setOrigin(0.5);"""

loading_logic_new = """          this.loadingText = this.add
            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading + " 0%", {
              font: "28px Arial",
              fill: "#fff",
            })
            .setOrigin(0.5);
          
          this.load.on('progress', (p) => {
              const percent = Math.floor(p * 100);
              this.loadingText.setText(`${TEXTS.loading} ${percent}%`);
          });"""

for file_path in files:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original_len = len(content)
    
    # --- Fix Duplicates ---
    # Strategy: 
    # 1. Find all `const rp = ...`
    # 2. If > 1, locate the second one.
    # 3. Identify the block it belongs to (likely our inserted block).
    # 4. Remove that whole block or just the line.
    
    # Actually, if we look at the provided structure, the insertion was:
    #       // ---------------- 輔助函式 ----------------
    #       const rp = ...
    
    # If this appears multiple times, simply remove the occurrence that is NOT at the top?
    # Or keep the one before SceneMenu?
    
    # Let's simply Find & Count.
    block_start = "// ---------------- 輔助函式 ----------------"
    
    parts = content.split(block_start)
    if len(parts) > 2:
        print(f"Fixing duplicates in {file_path}")
        # We have > 2 parts means the separator appears > 1 time.
        # e.g. [Part1, Part2, Part3]
        # We keep Part1 + separator + Part2.
        # And discard the separator + Part3? NO.
        # The duplicated block was inserted.
        # It's better to remove the ONE that is redundant.
        
        # Usually checking `rp` existence is safer.
        # Let's preserve the LAST block (which we just inserted and is guaranteed to be correct/full)
        # and remove previous ones if they are identical?
        # Actually, the subagent said School has rp at Line 88 AND Line 175.
        # Our script inserted at Line 175 (before SceneMenu).
        # So the one at Line 88 is the "original" one that was there.
        # We should keep the one we just inserted (since we know it has makeButton etc)
        # And remove the OLD one at Line 88 if it lacks makeButton.
        
        # Wait, if Line 88 has `rp`, does it have `makeButton`?
        # Subagent said makeButton appears ONLY ONCE.
        # So maybe Line 88 has `rp` but not `makeButton`.
        # So we should delete the `rp` at Line 88.
        
        pass

    # A simpler approach: regex replace the FIRST `const rp = ...` if there are two.
    # Be careful not to break code structure of surrounding functions.
    
    # Let's do a tailored manual cleanup logic:
    # Remove `const rp = (arr) => arr[Math.floor(Math.random() * arr.length)];` 
    # IF it appears twice.
    
    rp_decl = "const rp = (arr) => arr[Math.floor(Math.random() * arr.length)];"
    if content.count(rp_decl) > 1:
        print(f"Removing duplicate 'rp' in {file_path}")
        # Find first occurrence and remove it
        content = content.replace(rp_decl, "", 1)
        
    # Also check `function shuffle(arr) { ... }`
    shuffle_decl_start = "function shuffle(arr) {"
    if content.count(shuffle_decl_start) > 1:
        print(f"Removing duplicate 'shuffle' in {file_path}")
        # This is multi-line, annoying to replace via simple string.
        # But we can try to find the first block and cut it.
        start_idx = content.find(shuffle_decl_start)
        # Find closing brace?
        # Assuming standard formatting:
        # function shuffle(arr) {
        #   for ...
        #     ...
        #   }
        # }
        # Simple counting of braces
        cur = start_idx
        brace_balance = 0
        found_start = False
        end_idx = -1
        
        # Minimal scan
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_balance += 1
                found_start = True
            elif content[i] == '}':
                brace_balance -= 1
                if found_start and brace_balance == 0:
                    end_idx = i + 1
                    break
        
        if end_idx != -1:
             # Remove this block
             content = content[:start_idx] + content[end_idx:]

    # Remove `makeButton` if duplicate? (Subagent said it was singular, but let's be safe)
    
    # --- Add Loading Percentage ---
    # We look for the text creation in SceneMenu.preload and assign it to a var
    if "this.loadingText = " not in content:
        # It's using the old format
        # We replace the text creation block
        # Use regex to be more flexible with whitespace or variable names
        # But `loading_logic_old` is quite specific.
        
        # Try finding the specific string lines
        target_str = "TEXTS.loading, {"
        if target_str in content:
            # We want to replace the whole `this.add.text(...)` statement.
            # But simpler is to find the function `preload() {` and rewrite its body?
            # Or just replace the `.text(...)` part.
            
            # Let's replace `this.add.text(GAME_W / 2, GAME_H / 2, TEXTS.loading,`
            # With `this.loadingText = this.add.text(..., TEXTS.loading + ' 0%',`
            
            # And insert the progress handler after it.
            
            old_part = "this.add\n            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading, {"
            new_part = "this.loadingText = this.add\n            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading + ' 0%', {"
            
            # Try to match loose whitespace
            pattern = re.compile(r'this\.add\s+\.text\(GAME_W / 2, GAME_H / 2, TEXTS\.loading, {')
            
            match = pattern.search(content)
            if match:
                 span = match.span()
                 start_pt = span[0]
                 end_pt = span[1]
                 
                 # Append the progress logic after the `.setOrigin(0.5);`
                 # Find the next semicolon
                 semicolon = content.find(";", end_pt)
                 if semicolon != -1:
                     # Replacement logic
                     replacement = """this.loadingText = this.add
            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading + " 0%", {
              font: "28px Arial",
              fill: "#fff",
            })
            .setOrigin(0.5);

          this.load.on('progress', (p) => {
              const percent = Math.floor(p * 100);
              if(this.loadingText) this.loadingText.setText(`${TEXTS.loading} ${percent}%`);
          });"""
                     
                     # We replace from start_pt to semicolon+1
                     # BE CAREFUL: we need to verify we are capturing the whole statements.
                     # The original code:
                     #           this.add
                     #             .text(GAME_W / 2, GAME_H / 2, TEXTS.loading, {
                     #               font: "28px Arial",
                     #               fill: "#fff",
                     #             })
                     #             .setOrigin(0.5);
                     
                     content = content[:start_pt] + replacement + content[semicolon+1:]
                     print(f"Added loading percentage to {file_path}")

    if len(content) != original_len:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
