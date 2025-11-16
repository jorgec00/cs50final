from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/progress", methods=["GET"])
def progress():
    # temporary hardcoded data for front-end testing
    return jsonify({
        "certifications": [
            {
                "code": "PRIVATE_ASEL",
                "name": "Private Pilot – Airplane SEL",
                "percent_complete": 72
            },
            {
                "code": "INSTRUMENT_AIRPLANE",
                "name": "Instrument Rating – Airplane",
                "percent_complete": 35
            },
            {
                "code": "COMM_ASEL",
                "name": "Commercial – Airplane SEL",
                "percent_complete": 18
            }
        ]
    })
