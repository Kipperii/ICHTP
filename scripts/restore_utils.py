import os

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

helper_functions = """
      // ---------------- 輔助函式 ----------------
      const rp = (arr) => arr[Math.floor(Math.random() * arr.length)];
      function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [arr[i], arr[j]] = [arr[j], arr[i]];
        }
      }

      function makeButton(scene, x, y, text) {
        const btn = scene.add.container(x, y);
        const bg = scene.add.text(0, 0, text, {
          font: "24px Arial",
          backgroundColor: "#4a90e2",
          padding: { left: 20, right: 20, top: 10, bottom: 10 },
          fill: "#fff",
        }).setOrigin(0.5);
        btn.add(bg);
        btn.setSize(bg.width, bg.height);
        btn.setInteractive({ useHandCursor: true });
        
        // Hover effect
        btn.on('pointerover', () => bg.setStyle({ backgroundColor: '#357abd' }));
        btn.on('pointerout', () => bg.setStyle({ backgroundColor: '#4a90e2' }));
        
        return btn;
      }

      function makeCard(scene, key, isQuestion, letter) {
        const cont = scene.add.container(0, 0);
        const W = 210, H = 210;
        
        // 背景卡片
        const bg = scene.add.rectangle(0, 0, W, H, CARD_BG).setStrokeStyle(4, CARD_BORDER);
        cont.add(bg);
        
        // 圖片
        if (scene.textures.exists(key)) {
            const img = scene.add.image(0, 0, key);
            // 縮放以適應卡片
            const scale = Math.min((W - 20) / img.width, (H - 20) / img.height);
            img.setScale(scale);
            cont.add(img);
        } else {
            console.warn(`Missing texture: ${key}`);
            const txt = scene.add.text(0, 0, "?", { fontSize: "64px", color: "#000" }).setOrigin(0.5);
            cont.add(txt);
        }

        if (letter) {
            const tag = scene.add.text(-W/2 + 10, -H/2 + 10, letter, {
                font: "bold 24px Arial",
                fill: "#fff",
                backgroundColor: "#000",
                padding: { x: 4, y: 0 }
            }).setOrigin(0);
            cont.add(tag);
        }
        
        cont.setSize(W, H);
        cont.setInteractive();
        
        // 用於動畫的引用
        cont.__inner = bg; 
        
        return cont;
      }

      function fxCorrect(scene, target) {
         // 簡單的正確動畫：綠色閃爍 + 打勾
         const check = scene.add.text(target.x, target.y, "✔", {
             fontSize: "120px",
             color: "#00ff00",
             stroke: "#fff",
             strokeThickness: 6
         }).setOrigin(0.5).setDepth(100);
         
         scene.tweens.add({
             targets: check,
             scale: { from: 0.5, to: 1.2 },
             alpha: { from: 1, to: 0 },
             duration: 600,
             onComplete: () => check.destroy()
         });
         
         scene.sound.play('correct_sfx', { volume: 0.5 }); // 若有音效
      }

      function fxWrong(scene, target) {
         // 錯誤動畫：紅色叉叉 + 搖晃
         const cross = scene.add.text(target.x, target.y, "✘", {
             fontSize: "120px",
             color: "#ff0000",
             stroke: "#fff",
             strokeThickness: 6
         }).setOrigin(0.5).setDepth(100);

         scene.tweens.add({
             targets: cross,
             scale: { from: 0.5, to: 1.2 },
             alpha: { from: 1, to: 0 },
             duration: 600,
             onComplete: () => cross.destroy()
         });
         
         scene.tweens.add({
             targets: target,
             x: target.x + 10,
             duration: 50,
             yoyo: true,
             repeat: 5
         });
      }

      function spawnPlusOne(scene, x, y) {
          const txt = scene.add.text(x, y, "+10", {
              font: "bold 40px Arial",
              color: "#ffff00",
              stroke: "#000",
              strokeThickness: 4
          }).setOrigin(0.5).setDepth(200);
          
          scene.tweens.add({
              targets: txt,
              y: y - 50,
              alpha: 0,
              duration: 800,
              onComplete: () => txt.destroy()
          });
      }
      
      function createStar(scene, x, y, index) {
        // 簡單的星星粒子
        const star = scene.add.rectangle(x, y, 8, 8, 0xffff00);
        const angle = Math.random() * Math.PI * 2;
        const vel = 100 + Math.random() * 100;
        
        scene.tweens.add({
            targets: star,
            x: x + Math.cos(angle) * 50,
            y: y + Math.sin(angle) * 50,
            alpha: 0,
            duration: 600,
            onComplete: () => star.destroy()
        });
      }
"""

marker = "// ---------------- 選單 ----------------"

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if makeButton is missing
    if "function makeButton" in content:
        print(f"Skipping {file_path}, makeButton already exists.")
        continue
        
    # Find insertion point: BEFORE SceneMenu
    idx = content.find(marker)
    if idx == -1:
        print(f"Error: Marker not found in {file_path}")
        continue
        
    # Insert helper functions
    new_content = content[:idx] + helper_functions + "\n" + content[idx:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Restored Helper Functions in {file_path}")
