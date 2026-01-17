from services.firebase_service import db
from datetime import datetime, timedelta

SESSION_DURATION_MINUTES = 10

def start_session():
    db.collection("session").document("current").set({
        "active": True,
        "started_at": datetime.now().isoformat()
    })

def is_session_active():
    doc = db.collection("session").document("current").get()
    if not doc.exists:
        return False

    data = doc.to_dict()
    if not data["active"]:
        return False

    started = datetime.fromisoformat(data["started_at"])
    if datetime.now() - started > timedelta(minutes=SESSION_DURATION_MINUTES):
        stop_session()
        return False

    return True

def stop_session():
    db.collection("session").document("current").set({
        "active": False
    })
