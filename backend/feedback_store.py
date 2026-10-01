import json
from datetime import datetime, timezone
from pathlib import Path

FEEDBACK_FILE = Path(__file__).resolve().parent / "feedback.json"

def load_feedback():
    if not FEEDBACK_FILE.exists():
        return []
    try:
        return json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_feedback(feedback):
    FEEDBACK_FILE.write_text(
        json.dumps(feedback, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def add_feedback(prompt, response, rating, comment):
    feedback = load_feedback()
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "response": response,
        "rating": rating,
        "comment": comment
    }
    feedback.append(entry)
    save_feedback(feedback)
    return entry

def get_stats():
    feedback = load_feedback()
    total = len(feedback)
    positive = sum(item["rating"] == "positive" for item in feedback)
    negative = sum(item["rating"] == "negative" for item in feedback)
    return {
        "total_feedback": total,
        "positive": positive,
        "negative": negative,
        "positive_rate": round(positive / total * 100, 2) if total else 0,
        "negative_rate": round(negative / total * 100, 2) if total else 0
    }
