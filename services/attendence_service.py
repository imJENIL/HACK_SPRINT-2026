from services.firebase_service import db
from datetime import datetime

def mark_attendance(student_id, confidence=None):
    today = datetime.now().strftime("%Y-%m-%d")

    doc_ref = (
        db.collection("attendance")
        .document(today)
        .collection("records")
        .document(student_id)
    )

    if doc_ref.get().exists:
        return False, "Attendance already marked"

    doc_ref.set({
        "time": datetime.now().isoformat(),
        "confidence": confidence
    })

    return True, "Attendance marked"
