from services.firebase_service import db
from datetime import datetime

def save_student(student_id):
    db.collection("students").document(student_id).set({
        "name": student_id,
        "registered_at": datetime.now().isoformat()
    })

def get_students():
    docs = db.collection("students").stream()
    return [{"name": d.id} for d in docs]
