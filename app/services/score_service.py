from datetime import datetime

class ScoreService:
    """
    極簡 in-memory 成績暫存（可替換為 DB 或檔案）
    """
    def __init__(self):
        self._records = []

    def submit(self, payload: dict):
        data = {
            "ts": datetime.utcnow().isoformat() + "Z",
            **payload
        }
        self._records.append(data)
        return data

    def list_recent(self, limit=50):
        return list(reversed(self._records[-limit:]))

score_service = ScoreService()
