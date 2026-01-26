from flask import Blueprint, request, jsonify
from ..services.score_service import score_service

bp = Blueprint("api", __name__)

@bp.post("/submit_round")
def submit_round():
    """
    遊戲結束或關卡結束時提交成績/過關資訊
    JSON 欄位範例：
    {
      "session_id": "abc",
      "game_id": "supermarket_g1-1_find_same",
      "difficulty": 1,
      "accuracy": 90.0,
      "time_taken": 25,
      "result": "win"
    }
    """
    try:
        payload = request.get_json(force=True, silent=True) or {}
        stored = score_service.submit(payload)
        return jsonify({"ok": True, "stored": stored}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@bp.get("/scores")
def scores():
    """查看最近提交紀錄（開發期方便檢查）"""
    return jsonify(score_service.list_recent())
