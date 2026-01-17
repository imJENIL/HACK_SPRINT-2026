from flask import Blueprint, request, jsonify
from services.camera import capture_frame
from services.face_services import encode_face, save_face

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register_face():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"status": "error", "message": "Name required"}), 400

    frame = capture_frame()
    if frame is None:
        return jsonify({"status": "error", "message": "Camera error"}), 500

    encoding, error = encode_face(frame)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    success, err = save_face(name, encoding)
    if not success:
        return jsonify({"status": "error", "message": err}), 500

    return jsonify({"status": "success", "message": f"{name} registered"})
