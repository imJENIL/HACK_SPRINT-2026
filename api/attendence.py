from flask import Blueprint, jsonify, session
from services.attendence_service import get_today_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/attendance/today", methods=["GET"])
def today_attendance():
    """
    Get today's attendance records (Professor only)
    """

    # 🔐 Authorization check FIRST
    if not session.get("professor"):
        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 403

    records = get_today_attendance()

    return jsonify({
        "status": "success",
        "count": len(records),
        "attendance": records
    })
