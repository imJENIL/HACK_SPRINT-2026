import hashlib

PROFESSOR_ID = "prof123"
PROFESSOR_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

def verify_professor(pid, password):
    return (
        pid == PROFESSOR_ID and
        hashlib.sha256(password.encode()).hexdigest() == PROFESSOR_PASSWORD_HASH
    )
