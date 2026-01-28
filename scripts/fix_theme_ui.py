import os
import re

# The "Good" implementation from Restaurant
# Includes makeButton, makeCard, fxCorrect, createStar, fxWrong, spawnPlusOne, logGameData
NEW_UI_CODE = r"""
      // ---------------- UI ----------------
      function makeButton(scene, centerX, centerY, text) {
        const w = 180,
          h = 90;
        const g = scene.add.graphics();
        g.fillStyle(0x000000, 0.15).fillRoundedRect(4, 6, w, h, 18);
        g.fillStyle(0xe56e5b, 1).fillRoundedRect(0, 0, w, h, 18);
        g.lineStyle(3, 0xffffff, 1).strokeRoundedRect(0, 0, w, h, 18);
        const t = scene.add
          .text(w / 2, h / 2, text, {
            font: "bold 28px Arial",
            fill: "#fff",
            stroke: "#000",
            strokeThickness: 6,
          })
          .setOrigin(0.5);
        const inner = scene.add.container(0, 0, [g, t]);
        const cont = scene.add.container(centerX - w / 2, centerY - h / 2, [
          inner,
        ]);
        cont.setSize(w, h);
        cont.setInteractive(
          new Phaser.Geom.Rectangle(0, 0, w, h),
          Phaser.Geom.Rectangle.Contains
        );
        cont.input.useHandCursor = true;
        cont.__inner = inner;
        return cont;
      }

      function makeCard(scene, key, isQuestion, label) {
        const w = isQuestion ? 320 : 210,
          h = isQuestion ? 220 : 170;
        const pad = 10,
          boxW = w - 2 * pad,
          boxH = h - 2 * pad;

        const g = scene.add.graphics();
        g.fillStyle(0x000000, 0.28).fillRoundedRect(4, 6, w, h, 10);
        g.fillStyle(CARD_BG, 1).fillRoundedRect(0, 0, w, h, 10);
        g.lineStyle(2, CARD_BORDER, 0.95).strokeRoundedRect(
          2,
          2,
          w - 4,
          h - 4,
          8
        );

        const img = scene.add.image(0, 0, key).setOrigin(0.5);
        const sx = boxW / (img.width || boxW),
          sy = boxH / (img.height || boxH);
        const s = Math.max(sx, sy);
        img.setScale(s);
        img.x = pad + boxW / 2;
        img.y = pad + boxH / 2;

        const inner = scene.add.container(0, 0, [g, img]);
        if (!isQuestion && label) {
          const lt = scene.add
            .text(10, h - 10, label + ".", {
              font: "bold 22px Arial",
              fill: "#fff",
              stroke: "#000",
              strokeThickness: 5,
            })
            .setOrigin(0, 1);
          inner.add(lt);
        }
        const cont = scene.add.container(0, 0, [inner]);
        cont.setSize(w, h);
        cont.setInteractive(
          new Phaser.Geom.Rectangle(0, 0, w, h),
          Phaser.Geom.Rectangle.Contains
        );
        cont.input.useHandCursor = true;
        cont.__inner = inner;
        cont.__img = img;
        cont.__size = { w, h, boxW, boxH, pad };
        return cont;
      }

      // 改進的正確反饋效果，提供更生動的視覺反饋
      function fxCorrect(scene, cont) {
        const inner = cont.__inner;
        const cx = cont.x + cont.width / 2;
        const cy = cont.y + cont.height / 2;

        // 立即視覺反饋 - 閃光和波紋效果
        // 閃光效果
        const flash = scene.add
          .rectangle(cx, cy, cont.width + 20, cont.height + 20, 0xffff00, 0.7)
          .setDepth(30);

        // 波紋效果 - 多層同時展開
        const rings = [];
        for (let i = 0; i < 3; i++) {
          const ring = scene.add
            .circle(cx, cy, 10 + i * 15, 0x00ff88, 0.7 - i * 0.2)
            .setDepth(31);
          rings.push(ring);
          scene.tweens.add({
            targets: ring,
            radius: 80 + i * 20,
            alpha: 0,
            duration: 350 + i * 100,
            ease: "Sine.easeOut",
            onComplete: () => ring.destroy(),
          });
        }

        // 卡片彈跳效果
        scene.tweens.add({
          targets: inner,
          scaleX: 1.15,
          scaleY: 1.15,
          duration: 120,
          yoyo: true,
          ease: "Back.easeOut",
          onComplete: () => {
            // 添加星星效果
            for (let i = 0; i < 8; i++) {
              createStar(scene, cx, cy, i);
            }
          },
        });

        // 閃光消失
        scene.tweens.add({
          targets: flash,
          alpha: 0,
          scale: 1.3,
          duration: 250,
          onComplete: () => flash.destroy(),
        });

        // 光暈效果
        const glow = scene.add
          .rectangle(cx, cy, cont.width + 10, cont.height + 10, 0xffff00, 0)
          .setDepth(29);
        scene.tweens.add({
          targets: glow,
          alpha: 0.4,
          duration: 150,
          yoyo: true,
          onComplete: () => glow.destroy(),
        });
      }

      // 創建星星效果
      function createStar(scene, x, y, index) {
        // 每個星星往不同方向發射
        const angle = (index / 8) * Math.PI * 2;
        const distance = 50 + Math.random() * 30;
        const duration = 300 + Math.random() * 200;

        // 創建星形
        const points = [];
        const outerRadius = 8;
        const innerRadius = 4;
        let rot = (Math.PI / 2) * 3;
        const step = Math.PI / 5;

        for (let i = 0; i < 10; i++) {
          const radius = i % 2 === 0 ? outerRadius : innerRadius;
          points.push({
            x: x + Math.cos(rot) * radius,
            y: y + Math.sin(rot) * radius,
          });
          rot += step;
        }

        const star = scene.add.polygon(x, y, points, 0xffff00).setDepth(32);

        // 設置發射路徑
        scene.tweens.add({
          targets: star,
          x: x + Math.cos(angle) * distance,
          y: y + Math.sin(angle) * distance,
          angle: 180 + Math.random() * 180,
          alpha: 0,
          scale: 0.5 + Math.random() * 0.5,
          duration: duration,
          ease: "Cubic.easeOut",
          onComplete: () => star.destroy(),
        });
      }

      // 改進的錯誤反饋效果
      function fxWrong(scene, cont) {
        // 震動效果
        scene.cameras.main.shake(150, 0.006);

        // 紅色閃爍覆蓋
        const overlay = scene.add
          .rectangle(
            cont.x + cont.width / 2,
            cont.y + cont.height / 2,
            cont.width + 4,
            cont.height + 4,
            0xff0000,
            0.5
          )
          .setDepth(30);

        // X符號
        const crossSize = Math.min(cont.width, cont.height) * 0.6;
        const cx = cont.x + cont.width / 2;
        const cy = cont.y + cont.height / 2;
        const thickness = 6;

        const cross1 = scene.add.graphics().setDepth(31);
        cross1.lineStyle(thickness, 0xff0000, 0.8);
        cross1.beginPath();
        cross1.moveTo(cx - crossSize / 2, cy - crossSize / 2);
        cross1.lineTo(cx + crossSize / 2, cy + crossSize / 2);
        cross1.strokePath();
        cross1.setAlpha(0);

        const cross2 = scene.add.graphics().setDepth(31);
        cross2.lineStyle(thickness, 0xff0000, 0.8);
        cross2.beginPath();
        cross2.moveTo(cx + crossSize / 2, cy - crossSize / 2);
        cross2.lineTo(cx - crossSize / 2, cy + crossSize / 2);
        cross2.strokePath();
        cross2.setAlpha(0);

        // 動畫序列
        scene.tweens.add({
          targets: [cross1, cross2],
          alpha: 1,
          duration: 80,
          onComplete: () => {
            scene.tweens.add({
              targets: cont,
              x: cont.x + 5,
              duration: 50,
              yoyo: true,
              repeat: 2,
              ease: "Sine.easeInOut",
              onComplete: () => {
                scene.tweens.add({
                  targets: [overlay, cross1, cross2],
                  alpha: 0,
                  duration: 150,
                  onComplete: () => {
                    overlay.destroy();
                    cross1.destroy();
                    cross2.destroy();
                  },
                });
              },
            });
          },
        });
      }

      function spawnPlusOne(scene, x, y) {
        const container = scene.add.container(x, y).setDepth(1000);

        // 添加發光背景
        const glow = scene.add.circle(0, 0, 18, 0x00ff88, 0.3);

        // 添加文字
        const t = scene.add
          .text(0, 0, "+1s", {
            font: "bold 28px Arial",
            fill: "#00ff88",
            stroke: "#001a0f",
            strokeThickness: 6,
          })
          .setOrigin(0.5);

        container.add([glow, t]);

        // 動畫效果
        scene.tweens.add({
          targets: container,
          y: y - 50,
          alpha: 0,
          scale: 1.2,
          duration: 600,
          ease: "Back.easeOut",
          onComplete: () => container.destroy(),
        });
      }

      // ---------------- 數據收集 ----------------
      async function logGameData(gameData) {
        // 收集詳細的遊戲數據以支持研究和分析
        const sessionData = {
          timestamp: new Date().toISOString(),
          sessionId: gameData.sessionId || `session_${Date.now()}`,
          playerData: {
            accuracy: gameData.correctCount / Math.max(1, gameData.totalRounds),
            avgResponseTime:
              gameData.responseTimeTotal / Math.max(1, gameData.totalRounds),
            finalDifficulty: gameData.difficulty,
            difficultyHistory: gameData.difficultyHistory || [],
            performanceByRound: gameData.roundStats || [],
          },
          gameSettings: {
            timeLimit: TIME_START,
            targetCorrect: TARGET_CORRECT,
            bonusRoundInterval: BONUS_ROUND_INTERVAL,
          },
          deviceInfo: {
            screenWidth: window.innerWidth,
            screenHeight: window.innerHeight,
            userAgent: navigator.userAgent,
          },
        };

        // 將數據存到本地存儲
        try {
          const offlineData = JSON.parse(
            localStorage.getItem("offlineGameData") || "[]"
          );
          offlineData.push(sessionData);
          localStorage.setItem("offlineGameData", JSON.stringify(offlineData));
          console.log("Game data logged to local storage");
        } catch (err) {
          console.error("Error logging game data:", err);
        }

        return sessionData;
      }
      
"""

def update_ui_code(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to find the block to replace.
    # It starts roughly at "function makeButton" (or the comment before it)
    # And ends at "class SceneMenu"
    
    # Try finding the start marker. 
    # The files might have "// ---------------- 輔助函式 ----------------" OR "// ---------------- UI ----------------"
    
    start_match = re.search(r'// -+ (?:輔助函式|UI) -+', content)
    if not start_match:
        # Fallback: search for function makeButton
        start_match = re.search(r'function makeButton', content)
        if not start_match:
             print(f"  [Error] Could not find start of UI section in {filepath}")
             return

    start_idx = start_match.start()
    
    # Find end marker: "class SceneMenu"
    end_match = re.search(r'class SceneMenu', content)
    if not end_match:
        print(f"  [Error] Could not find 'class SceneMenu' in {filepath}")
        return
        
    end_idx = end_match.start()
    
    if start_idx >= end_idx:
        print(f"  [Error] Start index >= End index in {filepath}")
        return
        
    # Check what we are replacing
    old_block = content[start_idx:end_idx]
    # print(f"Replacing block of length {len(old_block)}")
    
    # Construct new content
    new_content = content[:start_idx] + NEW_UI_CODE + content[end_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("  [Success] Updated UI code.")

def main():
    root_dir = "app/templates/games"
    themes = ["school", "home", "occupation", "picnic", "playground", "sportcentre", "supermarket"]
    # restaurant is excluded as it is the source
    
    for theme in themes:
        path = os.path.join(root_dir, theme, "g1-1", f"game_{theme}_g1-1_find_same.html")
        if os.path.exists(path):
            update_ui_code(path)
        else:
            print(f"File not found: {path}")

if __name__ == "__main__":
    main()
