from flask import Blueprint, jsonify
from services.camera import capture_frame
from services.face_services import encode_face, match_face
from services.attendence_service import mark_attendance
from services.session_service import is_session_active
from services.liveness_service import check_liveness
import time

identify_bp = Blueprint("identify", __name__)

@identify_bp.route("/identify", methods=["GET"])
def identify_face():

    # 1️⃣ Check if professor started attendance
    if not is_session_active():
        return jsonify({
            "status": "blocked",
            "message": "Attendance session not active"
        }), 403

    # 2️⃣ Capture frames for liveness (3 seconds)
    frames = []
    start = time.time()

    while time.time() - start < 3:
        frame = capture_frame()
        if frame is not None:
            frames.append(frame)

    if not frames:
        return jsonify({
            "status": "error",
            "message": "Camera error"
        }), 500

    # 3️⃣ Liveness detection
    live, msg = check_liveness(frames)
    if not live:
        return jsonify({
            "status": "spoof",
            "message": msg
        }), 403

    # 4️⃣ Use last frame for recognition
    frame = frames[-1]

    # 5️⃣ Encode face
    encoding, error = encode_face(frame)
    if error:
        return jsonify({
            "status": "unknown",
            "message": error
        })

    # 6️⃣ Match face
    name, distance = match_face(encoding)
    if not name:
        return jsonify({
            "status": "unknown",
            "message": "Face not recognized"
        })

    # 7️⃣ Mark attendance (anti-duplicate)
    success, msg = mark_attendance(name)
    if not success:
        return jsonify({
            "status": "duplicate",
            "name": name,
            "message": msg
        })

    # 8️⃣ Success
    return jsonify({
        "status": "found",
        "name": name,
        "confidence": round((1 - distance) * 100, 2)
    })
