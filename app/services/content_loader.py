import os
import json
from glob import glob

def load_levels_seed(json_path: str):
    """
    嘗試載入預先產生的 levels_seed.json
    """
    try:
        if os.path.isfile(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print("[content_loader] load_levels_seed error:", e)
    return None

def ensure_levels_seed(static_root: str):
    """
    若無題庫，嘗試根據 images 目錄生成「極簡」題庫（僅用於 fallback）
    將會把四張圖一組當作一題（question=第一張，options=四張，correct=0）
    """
    images_dir = os.path.join(static_root, "games", "supermarket", "g1-1", "images")
    if not os.path.isdir(images_dir):
        print("[content_loader] images dir not found:", images_dir)
        return []

    files = sorted([os.path.basename(p) for p in glob(os.path.join(images_dir, "*.jpg"))])
    levels = []
    for i in range(0, len(files), 4):
        chunk = files[i:i+4]
        if len(chunk) < 4:
            break
        level = {
            "question": f"images/{chunk[0]}",
            "options": [f"images/{c}" for c in chunk],
            "correct": 0
        }
        levels.append(level)

    print(f"[content_loader] fallback levels generated: {len(levels)}")
    return levels
