import os
from flask import Blueprint, render_template, jsonify, current_app
from .services.content_loader import load_levels_seed, ensure_levels_seed

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/games/supermarket/g1-1")
def supermarket_g1_1():
    """
    返回 Supermarket G1-1 的遊戲頁面。
    遊戲本體使用你提供的 HTML 單檔，放在 templates/games/supermarket/g1-1/ 內。
    """
    return render_template("games/supermarket/g1-1/game_supermarket_g1-1_find_same.html")

@bp.route("/games/supermarket/g1-1/levels")
def supermarket_g1_1_levels():
    """
    返回題庫（若存在 static/games/supermarket/g1-1/data/levels_seed.json 則載入，
    否則嘗試 ensure_levels_seed 建立一份基礎資料或回傳空陣列）
    """
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "supermarket", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/supermarket")
def supermarket_hub():
    # 將這個模板檔放在 app/templates/games/supermarket/index.html
    return render_template("games/supermarket/index.html")

@bp.route('/admin/supermarket')
def admin_supermarket():
    """渲染超級市場遊戲的管理面板頁面"""
    return render_template('admin/supermarket/authoring.html')

@bp.route("/games/supermarket/g1-2")
def supermarket_g1_2():
    """
    記憶遊戲（考考你記性） Supermarket G1-2
    """
    return render_template("games/supermarket/g1-2/game_supermarket_g1-2_memory.html")

@bp.route("/games/supermarket/g1-3")
def supermarket_g1_3():
    """
    找出全相遊戲 Supermarket G1-3
    """
    return render_template("games/supermarket/g1-3/game_supermarket_g1-3_find_the_whole_image.html")



# --- Generated Routes for Themes ---

@bp.route("/games/home/g1-1")
def home_g1_1():
    return render_template("games/home/g1-1/game_home_g1-1_find_same.html")

@bp.route("/games/home/g1-1/levels")
def home_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "home", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/home")
def home_hub():
    return render_template("games/home/index.html")

@bp.route("/games/home/g1-2")
def home_g1_2():
    return render_template("games/home/g1-2/game_home_g1-2_memory.html")

@bp.route("/games/home/g1-3")
def home_g1_3():
    return render_template("games/home/g1-3/game_home_g1-3_find_the_whole_image.html")

@bp.route("/games/occupation/g1-1")
def occupation_g1_1():
    return render_template("games/occupation/g1-1/game_occupation_g1-1_find_same.html")

@bp.route("/games/occupation/g1-1/levels")
def occupation_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "occupation", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/occupation")
def occupation_hub():
    return render_template("games/occupation/index.html")

@bp.route("/games/occupation/g1-2")
def occupation_g1_2():
    return render_template("games/occupation/g1-2/game_occupation_g1-2_memory.html")

@bp.route("/games/occupation/g1-3")
def occupation_g1_3():
    return render_template("games/occupation/g1-3/game_occupation_g1-3_find_the_whole_image.html")

@bp.route("/games/picnic/g1-1")
def picnic_g1_1():
    return render_template("games/picnic/g1-1/game_picnic_g1-1_find_same.html")

@bp.route("/games/picnic/g1-1/levels")
def picnic_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "picnic", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/picnic")
def picnic_hub():
    return render_template("games/picnic/index.html")

@bp.route("/games/picnic/g1-2")
def picnic_g1_2():
    return render_template("games/picnic/g1-2/game_picnic_g1-2_memory.html")

@bp.route("/games/picnic/g1-3")
def picnic_g1_3():
    return render_template("games/picnic/g1-3/game_picnic_g1-3_find_the_whole_image.html")

@bp.route("/games/playground/g1-1")
def playground_g1_1():
    return render_template("games/playground/g1-1/game_playground_g1-1_find_same.html")

@bp.route("/games/playground/g1-1/levels")
def playground_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "playground", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/playground")
def playground_hub():
    return render_template("games/playground/index.html")

@bp.route("/games/playground/g1-2")
def playground_g1_2():
    return render_template("games/playground/g1-2/game_playground_g1-2_memory.html")

@bp.route("/games/playground/g1-3")
def playground_g1_3():
    return render_template("games/playground/g1-3/game_playground_g1-3_find_the_whole_image.html")

@bp.route("/games/restaurant/g1-1")
def restaurant_g1_1():
    return render_template("games/restaurant/g1-1/game_restaurant_g1-1_find_same.html")

@bp.route("/games/restaurant/g1-1/levels")
def restaurant_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "restaurant", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/restaurant")
def restaurant_hub():
    return render_template("games/restaurant/index.html")

@bp.route("/games/restaurant/g1-2")
def restaurant_g1_2():
    return render_template("games/restaurant/g1-2/game_restaurant_g1-2_memory.html")

@bp.route("/games/restaurant/g1-3")
def restaurant_g1_3():
    return render_template("games/restaurant/g1-3/game_restaurant_g1-3_find_the_whole_image.html")

@bp.route("/games/school/g1-1")
def school_g1_1():
    return render_template("games/school/g1-1/game_school_g1-1_find_same.html")

@bp.route("/games/school/g1-1/levels")
def school_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "school", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/school")
def school_hub():
    return render_template("games/school/index.html")

@bp.route("/games/school/g1-2")
def school_g1_2():
    return render_template("games/school/g1-2/game_school_g1-2_memory.html")

@bp.route("/games/school/g1-3")
def school_g1_3():
    return render_template("games/school/g1-3/game_school_g1-3_find_the_whole_image.html")

@bp.route("/games/sportcentre/g1-1")
def sportcentre_g1_1():
    return render_template("games/sportcentre/g1-1/game_sportcentre_g1-1_find_same.html")

@bp.route("/games/sportcentre/g1-1/levels")
def sportcentre_g1_1_levels():
    static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "static")
    levels_path = os.path.join(static_root, "games", "sportcentre", "g1-1", "data", "levels_seed.json")
    data = load_levels_seed(levels_path)
    if data is None:
        data = ensure_levels_seed(static_root)
    return jsonify(data or [])

@bp.route("/games/sportcentre")
def sportcentre_hub():
    return render_template("games/sportcentre/index.html")

@bp.route("/games/sportcentre/g1-2")
def sportcentre_g1_2():
    return render_template("games/sportcentre/g1-2/game_sportcentre_g1-2_memory.html")

@bp.route("/games/sportcentre/g1-3")
def sportcentre_g1_3():
    return render_template("games/sportcentre/g1-3/game_sportcentre_g1-3_find_the_whole_image.html")
