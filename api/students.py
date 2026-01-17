from flask import Blueprint, jsonify
from services.face_services import get_registered_faces, delete_face

students_bp = Blueprint("students", __name__)


@students_bp.route("/students", methods=["GET"])
def list_students():
    """
    Get all registered students
    """
    students = get_registered_faces()
    return jsonify({
        "status": "success",
        "count": len(students),
        "students": students
    })


@students_bp.route("/students/<name>", methods=["DELETE"])
def remove_student(name):
    """
    Delete a registered student
    """
    success = delete_face(name)
    if not success:
        return jsonify({
            "status": "error",
            "message": f"{name} not found"
        }), 404

    return jsonify({
        "status": "success",
        "message": f"{name} deleted"
    })
