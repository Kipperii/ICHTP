"""
propagate_g11_fixes.py
======================
Propagates the fully-updated supermarket G1-1 file to all other themes,
substituting only the theme-specific strings (page title, TEXTS.title,
THEME_URL constant, API endpoint, and comment label).

Theme-specific variables that are preserved per file:
  - <title>...</title>
  - TEXTS.title
  - const THEME_URL = "/games/<theme>";
  - fetch('/api/games/<theme>/images')
  - The comment "// 返回<label>主題頁的路徑"

Restaurant is a special case: it historically used RESTAURANT_THEME_URL
instead of THEME_URL. This script normalises it to THEME_URL.
"""

import os
import re

BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES  = os.path.join(BASE, "app", "templates", "games")
SRC    = os.path.join(GAMES, "supermarket", "g1-1", "game_supermarket_g1-1_find_same.html")

# theme slug → (page_title_prefix, texts_title, comment_label, old_var_name_if_different)
THEMES = {
    "restaurant":  ("餐廳篇",     "餐廳篇\\n找出相同",   "餐廳",     "RESTAURANT_THEME_URL"),
    "playground":  ("遊樂場篇",   "遊樂場篇\\n找出相同", "遊樂場",   None),
    "occupation":  ("職業篇",     "職業篇\\n找出相同",   "職業",     None),
    "picnic":      ("野餐篇",     "野餐篇\\n找出相同",   "野餐",     None),
    "home":        ("家中篇",     "家中篇\\n找出相同",   "家居",     None),
    "sportcentre": ("運動中心篇", "運動中心篇\\n找出相同","運動中心", None),
    "school":      ("學校篇",     "學校篇\\n找出相同",   "學校",     None),
}

SRC_THEME         = "supermarket"
SRC_PAGE_TITLE    = "超級市場篇 G1-1 找相同"
SRC_TEXTS_TITLE   = "超級市場篇\\n找出相同"
SRC_COMMENT_LABEL = "超市"
SRC_VAR_NAME      = "THEME_URL"

with open(SRC, encoding="utf-8") as f:
    src_content = f.read()

updated = 0
for slug, (page_pfx, texts_title, comment_label, old_var) in THEMES.items():
    content = src_content

    # 1. <title>
    content = content.replace(
        f"<title>{SRC_PAGE_TITLE}</title>",
        f"<title>{page_pfx} G1-1 找相同</title>"
    )

    # 2. TEXTS.title (the raw string inside the JS object)
    content = content.replace(
        f'title: "{SRC_TEXTS_TITLE}",',
        f'title: "{texts_title}",'
    )

    # 3. Comment above THEME_URL constant
    content = content.replace(
        f"// 返回{SRC_COMMENT_LABEL}主題頁的路徑",
        f"// 返回{comment_label}主題頁的路徑"
    )

    # 4. THEME_URL value
    content = content.replace(
        f'const {SRC_VAR_NAME} = "/games/{SRC_THEME}";',
        f'const THEME_URL = "/games/{slug}";'
    )

    # 5. API fetch endpoint
    content = content.replace(
        f"fetch('/api/games/{SRC_THEME}/images')",
        f"fetch('/api/games/{slug}/images')"
    )

    # 6. Normalise old variable names (e.g. RESTAURANT_THEME_URL → THEME_URL)
    if old_var and old_var != "THEME_URL":
        content = content.replace(old_var, "THEME_URL")

    dest = os.path.join(GAMES, slug, "g1-1", f"game_{slug}_g1-1_find_same.html")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] {slug}: {dest}")
    updated += 1

print(f"\nDone. {updated} files updated.")
