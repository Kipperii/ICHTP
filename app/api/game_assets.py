import os
import uuid
from pathlib import Path
from typing import List, Tuple
from flask import Blueprint, jsonify, current_app, request

bp = Blueprint('game_assets', __name__)

# 允許副檔名與限制
ALLOWED_EXT = {'.png', '.jpg', '.jpeg'}
PER_FILE_LIMIT = 2 * 1024 * 1024  # 2MB 與前端一致

# 預設場景 / 遊戲 → 對應內建資源相對路徑（相對於 static）
DEFAULT_SCENE_GAME_DIRS = {
    ('supermarket', 'find_same'): 'games/supermarket/g1-1/images',
    # 新增記憶遊戲的預設資源資料夾 (請建立對應資料夾)
    ('supermarket', 'memory'): 'games/supermarket/g1-2/images'
}

def _static_root() -> Path:
    return Path(current_app.static_folder)

def _uploads_root() -> Path:
    root = _static_root() / 'uploads'
    root.mkdir(parents=True, exist_ok=True)
    return root

def _default_dirs_for(scene: str, game: str) -> List[Path]:
    rel = DEFAULT_SCENE_GAME_DIRS.get((scene, game))
    if not rel:
        return []
    p = _static_root() / rel
    return [p] if p.exists() else []

def _upload_dir(scene: str, game: str) -> Path:
    p = _uploads_root() / scene / game
    p.mkdir(parents=True, exist_ok=True)
    return p

def _safe_filename(name: str) -> str:
    name = name.strip()
    if not name:
        name = uuid.uuid4().hex
    name = name.lower().replace(' ', '_')
    name = ''.join(c if (c.isalnum() or c in '._-') else '_' for c in name)
    if len(name) > 80:
        stem, ext = os.path.splitext(name)
        name = f"{stem[:60]}_{uuid.uuid4().hex[:6]}{ext}"
    return name

def _collect_files(scene: str, game: str) -> List[str]:
    urls: List[str] = []
    # 內建
    for d in _default_dirs_for(scene, game):
        for fn in sorted(d.iterdir()):
            if fn.is_file() and fn.suffix.lower() in ALLOWED_EXT:
                rel = fn.relative_to(_static_root()).as_posix()
                urls.append(f"/static/{rel}")
    # 上傳
    up_dir = _upload_dir(scene, game)
    for fn in sorted(up_dir.iterdir()):
        if fn.is_file() and fn.suffix.lower() in ALLOWED_EXT:
            rel = fn.relative_to(_static_root()).as_posix()
            urls.append(f"/static/{rel}")
    return urls

# ---------------- 舊路徑 (保留兼容) ----------------
@bp.route('/games/supermarket/images')
def get_supermarket_images():
    return jsonify(_collect_files('supermarket', 'find_same'))

# ---------------- 新 API: List ----------------
@bp.route('/api/games/<scene>/images', methods=['GET'])
@bp.route('/api/games/<scene>/<game>/images', methods=['GET'])
def list_images(scene: str, game: str = None):
    if game is None:
        game = request.args.get('game') or 'find_same'
    return jsonify(_collect_files(scene, game))

# ---------------- 新 API: Upload ----------------
@bp.route('/api/games/<scene>/upload', methods=['POST'])
@bp.route('/api/games/<scene>/<game>/upload', methods=['POST'])
def upload_images(scene: str, game: str = None):
    if game is None:
        game = request.form.get('game') or 'find_same'
    files = request.files.getlist('files')
    if not files:
        return jsonify({"ok": False, "message": "沒有檔案"}), 400

    target = _upload_dir(scene, game)
    saved = []
    errors = []

    for fs in files:
        orig = fs.filename or ''
        ext = os.path.splitext(orig)[1].lower()
        if ext not in ALLOWED_EXT:
            errors.append({"name": orig, "error": "副檔名不允許"})
            continue
        data = fs.read()
        size = len(data)
        if size > PER_FILE_LIMIT:
            errors.append({"name": orig, "error": f"超過大小限制 {PER_FILE_LIMIT // 1024}KB"})
            continue
        fname = _safe_filename(orig) or (uuid.uuid4().hex + ext)
        out_path = target / fname
        if out_path.exists():
            stem, ext2 = os.path.splitext(fname)
            fname = f"{stem}_{uuid.uuid4().hex[:6]}{ext2}"
            out_path = target / fname
        try:
            with open(out_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            errors.append({"name": orig, "error": f"寫入失敗: {e}"})
            continue
        saved.append({
            "name": fname,
            "url": f"/static/uploads/{scene}/{game}/{fname}",
            "size": size
        })

    status = 200 if saved else 400
    return jsonify({"ok": bool(saved), "saved": saved, "errors": errors}), status

# ---------------- 新 API: Delete ----------------
@bp.route('/api/games/<scene>/delete', methods=['POST', 'DELETE'])
@bp.route('/api/games/<scene>/<game>/delete', methods=['POST', 'DELETE'])
def delete_image(scene: str, game: str = None):
    if game is None:
        body = request.get_json(silent=True) or {}
        game = body.get('game') or 'find_same'
    payload = request.get_json(silent=True) or {}
    path_url = payload.get('path')
    if not path_url:
        return jsonify({"ok": False, "message": "缺少 path"}), 400

    prefix = f"/static/uploads/{scene}/{game}/"
    if not path_url.startswith(prefix):
        return jsonify({"ok": False, "message": "非法路徑"}), 400

    fname = path_url[len(prefix):]
    fpath = _upload_dir(scene, game) / fname
    if not fpath.exists():
        return jsonify({"ok": False, "message": "檔案不存在"}), 404
    try:
        fpath.unlink()
    except Exception as e:
        return jsonify({"ok": False, "message": f"刪除失敗: {e}"}), 500
    return jsonify({"ok": True, "deleted": path_url}), 200