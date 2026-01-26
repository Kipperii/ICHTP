import os
from flask import Flask

def create_app():
    app = Flask(__name__, static_folder="../static", template_folder="templates")

    # 簡單 Secret Key（正式環境請改用 os.environ 注入）
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # 載入路由
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # API
    from .api.submit_round import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # 新增：載入遊戲資源 API
    from .api.game_assets import bp as game_assets_bp
    app.register_blueprint(game_assets_bp)

    return app