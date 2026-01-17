from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint("auth", __name__)

PROF_ID = "prof123"
PROF_PASS = "secret123"

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["id"] == PROF_ID and data["password"] == PROF_PASS:
        session["professor"] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401
