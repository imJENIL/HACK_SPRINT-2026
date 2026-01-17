from flask import Blueprint, jsonify, session
from services.session_service import start_session

session_bp = Blueprint("session", __name__)

@session_bp.route("/start-attendance", methods=["POST"])
def start_attendance():
    if not session.get("professor"):
        return jsonify({"error": "Unauthorized"}), 403

    start_session()
    return jsonify({"status": "attendance started"})
