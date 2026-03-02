"""
propagate_g13.py
將 supermarket 的 G1-3 找出全相 遊戲複製到其他 7 個主題，
同時替換主題名稱、API 路徑、頁面標題等。
"""
import os, re, shutil

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MASTER = os.path.join(
    BASE,
    "app", "templates", "games", "supermarket", "g1-3",
    "game_supermarket_g1-3_find_the_whole_image.html",
)

THEMES = {
    "restaurant":  {"title": "餐廳篇",    "label": "餐廳"},
    "playground":  {"title": "遊樂場篇",  "label": "遊樂場"},
    "occupation":  {"title": "職業篇",    "label": "職業"},
    "picnic":      {"title": "野餐篇",    "label": "野餐"},
    "home":        {"title": "家居篇",    "label": "家居"},
    "sportcentre": {"title": "體育中心篇", "label": "體育中心"},
    "school":      {"title": "學校篇",    "label": "學校"},
}

def propagate():
    with open(MASTER, "r", encoding="utf-8") as f:
        master_src = f.read()

    for theme, info in THEMES.items():
        src = master_src

        # 1. HTML <title>
        src = src.replace(
            "<title>超級市場篇 G1-3 找出全相</title>",
            f"<title>{info['title']} G1-3 找出全相</title>",
        )

        # 2. JS 頂部註解
        src = src.replace(
            "超級市場篇 G1-3 — 找出全相",
            f"{info['title']} G1-3 — 找出全相",
        )

        # 3. TEXTS.title
        src = src.replace(
            'title: "超級市場篇\\n找出全相"',
            f'title: "{info["title"]}\\n找出全相"',
        )

        # 4. THEME_URL
        src = src.replace(
            'const THEME_URL = "/games/supermarket"',
            f'const THEME_URL = "/games/{theme}"',
        )

        # 5. API endpoint
        src = src.replace(
            'fetch("/api/games/supermarket/images")',
            f'fetch("/api/games/{theme}/images")',
        )

        # 6. gameType in logGameData
        # (keep as g1-3_find_whole_image, no theme-specific change needed)

        # Write to destination
        dest_dir = os.path.join(
            BASE, "app", "templates", "games", theme, "g1-3"
        )
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(
            dest_dir, f"game_{theme}_g1-3_find_the_whole_image.html"
        )
        with open(dest_file, "w", encoding="utf-8") as f:
            f.write(src)
        print(f"  ✅ {theme}: {dest_file}")

    print(f"\n完成！已將 G1-3 傳播到 {len(THEMES)} 個主題。")


if __name__ == "__main__":
    propagate()
