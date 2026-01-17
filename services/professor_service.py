from services.firebase_service import db
import hashlib

def verify_professor(pid, password):
    doc = db.collection("professors").document(pid).get()
    if not doc.exists:
        return False

    stored_hash = doc.to_dict()["password_hash"]
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()
