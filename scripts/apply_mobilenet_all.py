import os

files = [
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\home\g1-1\game_home_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\occupation\g1-1\game_occupation_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\picnic\g1-1\game_picnic_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\playground\g1-1\game_playground_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\restaurant\g1-1\game_restaurant_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\school\g1-1\game_school_g1-1_find_same.html',
    r'c:\Users\kckwok\Desktop\ICHTP\app\templates\games\supermarket\g1-1\game_supermarket_g1-1_find_same.html'
]

# Replacement 1: Head scripts
head_search = """<script src="https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.min.js"></script>
    <style>"""
head_replace = """<script src="https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.min.js"></script>
    <!-- TFJS & MobileNet for SimilarityPipeline -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.15.0/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@2.1.1/dist/mobilenet.min.js"></script>
    <script src="/static/lib/similarity-pipeline.js"></script>
    <style>"""

# Replacement 2: SceneMenu init
menu_search = """        async create() {
          this.cameras.main.setBackgroundColor(\"#000\");"""
menu_replace = """        async create() {
          // Initialize AI Model
          if (typeof SimilarityPipeline !== "undefined") {
            try {
              await SimilarityPipeline.loadAIModel();
            } catch (e) {
              console.warn("AI Model load failed", e);
            }
          }

          this.cameras.main.setBackgroundColor("#000");"""

# Replacement 3: SceneGame loadLevel usage logic
# This one is tricky because of indentation.
# We will look for:
#           if (isBonus) {
#             // 特別關：3個干擾都是獨立變體
# ... (lines)
#             this.tempKeys.push(...varKeys);
#             distractors.push(...varKeys);

# And replace with the updated logic.

bonus_logic_start = """          if (isBonus) {
            // 特別關：3個干擾都是獨立變體"""

bonus_logic_end = """            this.tempKeys.push(...varKeys);
            distractors.push(...varKeys);"""

bonus_logic_new = """          if (isBonus) {
            // 特別關：使用 AI 生成相似度變體
            let varKeys = [];
            if (typeof SimilarityPipeline !== "undefined") {
              try {
                 varKeys = await SimilarityPipeline.generateVariants(
                    this,
                    correctKey,
                    3,
                    this.ddm.d
                 );
              } catch(e) {
                console.error("SimilarityPipeline error", e);
              }
            }
            this.tempKeys.push(...varKeys);
            distractors.push(...varKeys);"""

for file_path in files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # 1. Head
    content = content.replace(head_search, head_replace)

    # 2. Menu
    content = content.replace(menu_search, menu_replace)
    
    # 3. Bonus Logic
    # We define a regex or just find the block start and find specific end lines.
    # Since we can't easily rely on exact string match for a large block due to variable whitespace/formatting potentially,
    # let's try to locate the start and the *immediate* following lines if they are consistent.
    
    # In the file viewed (school), it is:
    #           if (isBonus) {
    #             // 特別關：3個干擾都是獨立變體
    #             const variantTypes = [
    #               ["blur", "color"],
    #               ["flipH", "blend"],
    #               ["flipV", "crop"],
    #             ];
    #             shuffle(variantTypes);
    #             let varKeys = await makeAnswerVariantsAsync(
    #               this.textures,
    #               correctKey,
    #               variantTypes,
    #               this.ddm.d
    #             );
    #             this.tempKeys.push(...varKeys);
    #             distractors.push(...varKeys);
    
    start_idx = content.find("if (isBonus) {")
    if start_idx != -1:
        # Check if the next line contains "特別關：3個干擾都是獨立變體"
        # We need to be careful not to replace wrong blocks.
        # But this code is unique enough.
        
        # Let's target the exact block we saw in school file.
        block_to_replace = """          if (isBonus) {
            // 特別關：3個干擾都是獨立變體
            const variantTypes = [
              ["blur", "color"],
              ["flipH", "blend"],
              ["flipV", "crop"],
            ];
            shuffle(variantTypes);
            let varKeys = await makeAnswerVariantsAsync(
              this.textures,
              correctKey,
              variantTypes,
              this.ddm.d
            );
            this.tempKeys.push(...varKeys);
            distractors.push(...varKeys);"""
        
        if block_to_replace in content:
            content = content.replace(block_to_replace, bonus_logic_new)
        else:
             # Try slightly different formatting if strict match failed?
             # Or just print warning
             print(f"Warning: Bonus logic block match failed for {file_path}")
             
    # 4. Remove helper functions
    # We can remove the block from "function rgbToHsv(r, g, b) {" down to end of "makeAnswerVariantsAsync"
    # Or just replace specific function definitions with empty string?
    # Better to find:
    # Start: // ---------------- 變體生成（獨立效果） ----------------
    # End: A known point after makeAnswerVariantsAsync. 
    # In school file:
    #       }
    #
    #       // ---------------- 遊戲場景 ----------------
    
    start_marker = "// ---------------- 變體生成（獨立效果） ----------------"
    end_marker = "// ---------------- 遊戲場景 ----------------"
    
    s_idx = content.find(start_marker)
    e_idx = content.find(end_marker, s_idx)
    
    if s_idx != -1 and e_idx != -1:
        # Check if makeAnswerVariantsAsync is actually inside this block
        if "makeAnswerVariantsAsync" in content[s_idx:e_idx]:
             content = content[:s_idx] + content[e_idx:]
             print(f"Removed helper functions in {file_path}")
        else:
             print(f"Helper function block found but didn't contain target function in {file_path}")

    if len(content) != original_len:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes made to {file_path}")
