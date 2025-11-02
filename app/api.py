from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/check", methods=["POST"])
def check_progress():
    data = request.get_json()
    # TODO: compare data to FAA requirements
    return jsonify({
        "status": "ok",
        "message": "Progress calculated",
        "percent_complete": 0.42
    })
