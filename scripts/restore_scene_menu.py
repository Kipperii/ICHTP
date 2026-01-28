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

scene_menu_code = """
      // ---------------- 選單 ----------------
      class SceneMenu extends Phaser.Scene {
        constructor() {
          super("menu");
        }
        preload() {
          this.add
            .text(GAME_W / 2, GAME_H / 2, TEXTS.loading, {
              font: "28px Arial",
              fill: "#fff",
            })
            .setOrigin(0.5);
          // 使用動態獲取的圖片列表進行預加載
          ALL_IMAGES.forEach((src) => this.load.image(src, src));
        }
        async create() {
          // Initialize AI Model
          if (typeof SimilarityPipeline !== "undefined") {
            try {
              await SimilarityPipeline.loadAIModel();
            } catch (e) {
              console.warn("AI Model load failed", e);
            }
          }

          this.cameras.main.setBackgroundColor("#000");
          this.mapPointer = createPointerMapper(this.game);

          const bg = this.add.graphics();
          bg.fillStyle(PANEL_COLOR, 1).fillRoundedRect(0, 0, GAME_W, GAME_H, 6);
          bg.lineStyle(2, PANEL_BORDER, 1).strokeRoundedRect(
            2,
            2,
            GAME_W - 4,
            GAME_H - 4,
            6
          );

          this.add.text(84, 64, TEXTS.title, {
            font: "bold 48px Arial",
            fill: "#fff",
            stroke: "#000",
            strokeThickness: 8,
            lineSpacing: -8,
          });
          const play = makeButton(
            this,
            GAME_W / 2 - 120,
            GAME_H / 2 + 40,
            "遊戲開始"
          );
          const help = makeButton(
            this,
            GAME_W / 2 + 120,
            GAME_H / 2 + 40,
            "遊戲玩法"
          );

          this.input.on("pointerdown", (raw) => {
            const p = this.mapPointer(raw.event);
            const hit = (btn) =>
              Phaser.Geom.Rectangle.Contains(btn.getBounds(), p.x, p.y);
            if (hit(play)) this.scene.start("game");
            else if (hit(help)) this.showHelp();
          });
        }
        showHelp() {
          const map = this.mapPointer || createPointerMapper(this.game);

          // 背景遮罩
          const dim = this.add
            .rectangle(GAME_W / 2, GAME_H / 2, GAME_W, GAME_H, 0x000000, 0.7)
            .setDepth(100)
            .setInteractive();

          // 主面板 - 增加高度以容納所有內容且避免重疊
          const panel = this.add
            .rectangle(GAME_W / 2, GAME_H / 2, 600, 500, 0xffffff)
            .setDepth(101)
            .setStrokeStyle(4, 0x4a90e2);

          // 標題欄
          const titleBar = this.add
            .rectangle(GAME_W / 2, GAME_H / 2 - 230, 600, 60, 0x4a90e2)
            .setDepth(101);

          // 標題文字
          const title = this.add
            .text(GAME_W / 2, GAME_H / 2 - 230, "遊戲玩法", {
              font: "bold 32px Arial",
              fill: "#ffffff",
            })
            .setOrigin(0.5)
            .setDepth(102);

          // 遊戲目標 - 調整位置
          const goalHeader = this.add
            .text(GAME_W / 2 - 270, GAME_H / 2 - 180, "【遊戲目標】", {
              font: "bold 24px Arial",
              fill: "#4a90e2",
            })
            .setDepth(102);

          const goalText = this.add
            .text(
              GAME_W / 2 - 270,
              GAME_H / 2 - 140,
              "找出與上方題圖完全相同的那一張圖片。",
              {
                font: "20px Arial",
                fill: "#333333",
              }
            )
            .setDepth(102);

          // 遊戲規則 - 調整位置
          const rulesHeader = this.add
            .text(GAME_W / 2 - 270, GAME_H / 2 - 100, "【遊戲規則】", {
              font: "bold 24px Arial",
              fill: "#4a90e2",
            })
            .setDepth(102);

          // 簡化規則顯示，調整行距
          const rules = [
            "• 成功找到相同圖片會獲得10分，並增加時間",
            "• 選錯會扣除5分",
            "• 隨著你的表現，難度會自動調整",
            "• 成功答對20題即可過關",
          ];

          const ruleTexts = [];
          rules.forEach((rule, index) => {
            const ruleText = this.add
              .text(GAME_W / 2 - 270, GAME_H / 2 - 60 + index * 32, rule, {
                font: "20px Arial",
                fill: "#333333",
              })
              .setDepth(102);
            ruleTexts.push(ruleText);
          });

          // 特別關卡 - 調整位置，確保與按鈕有足夠空間
          const specialHeader = this.add
            .text(GAME_W / 2 - 270, GAME_H / 2 + 80, "【特別關卡】", {
              font: "bold 24px Arial",
              fill: "#e6a23c",
            })
            .setDepth(102);

          const specialText = this.add
            .text(
              GAME_W / 2 - 270,
              GAME_H / 2 + 120,
              "每隔幾關會出現特別挑戰關卡，其中干擾項都是\\n正確答案的變體（如變色、模糊、鏡像等）",
              {
                font: "20px Arial",
                fill: "#333333",
                lineSpacing: 8, // 增加行間距，提高可讀性
              }
            )
            .setDepth(102);

          // 按鈕 - 移動到更下方位置以避免重疊
          const btnBg = this.add
            .rectangle(GAME_W / 2, GAME_H / 2 + 210, 160, 60, 0xe56e5b)
            .setDepth(102)
            .setInteractive()
            .setStrokeStyle(2, 0xffffff);

          const btnText = this.add
            .text(GAME_W / 2, GAME_H / 2 + 210, "知道了", {
              font: "bold 24px Arial",
              fill: "#ffffff",
            })
            .setOrigin(0.5)
            .setDepth(103);

          // 點擊事件
          btnBg.on("pointerdown", () => {
            const elements = [
              dim,
              panel,
              titleBar,
              title,
              goalHeader,
              goalText,
              rulesHeader,
              ...ruleTexts,
              specialHeader,
              specialText,
              btnBg,
              btnText,
            ];

            this.tweens.add({
              targets: elements,
              alpha: 0,
              duration: 200,
              onComplete: () => {
                elements.forEach((el) => el.destroy());
              },
            });
          });

          // 確保所有元素都有初始可見狀態
          const elements = [
            panel,
            titleBar,
            title,
            goalHeader,
            goalText,
            rulesHeader,
            ...ruleTexts,
            specialHeader,
            specialText,
            btnBg,
            btnText,
          ];

          // 添加入場動畫
          elements.forEach((el) => {
            el.alpha = 0;
            el.y += 20;
          });

          this.tweens.add({
            targets: elements,
            alpha: 1,
            y: "-=20",
            duration: 200,
            ease: "Power1",
            stagger: 30,
          });
        }
      }
"""

marker = "// ---------------- 遊戲場景 ----------------"

for file_path in files:
    if not os.path.exists(file_path):
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # If SceneMenu already exists, skip
    # (Assuming my previous script didn't mess up partial cleanup)
    if "class SceneMenu extends Phaser.Scene" in content:
        print(f"Skipping {file_path}, SceneMenu already exists.")
        continue
    
    # Locate marker
    idx = content.find(marker)
    if idx == -1:
        print(f"Error: Marker not found in {file_path}")
        continue
    
    # Insert before marker
    new_content = content[:idx] + scene_menu_code + "\n" + content[idx:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Restored SceneMenu in {file_path}")
