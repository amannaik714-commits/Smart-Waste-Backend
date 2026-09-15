from flask import Flask, jsonify, request

import firebase_connection
from firebase_admin import db
import firebase_connection
from datetime import datetime, timezone

app = Flask(__name__)


@app.route("/")
def home():
    return "Smart Waste Management Backend is running!"


@app.route("/bins")
def get_bins():
    data = db.reference("bins").get() or {}
    return jsonify(list(data.values()))


@app.route("/sensor", methods=["POST"])
def sensor():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    bin_id = data.get("binId")
    distance = data.get("distance")
    percentage = data.get("percentage")

    if not bin_id or distance is None or percentage is None:
        return jsonify({
            "error": "binId, distance and percentage are required"
        }), 400

    try:
        distance = float(distance)
        percentage = float(percentage)

    except (TypeError, ValueError):
        return jsonify({
            "error": "distance and percentage must be numbers"
        }), 400

    # Check if the bin exists
    bin_ref = db.reference(f"bins/{bin_id}")

    if bin_ref.get() is None:
        return jsonify({
            "error": f"Bin {bin_id} not found"
        }), 404

    # Use the percentage calculated by the ESP32
    fill = max(0, min(100, percentage))
    fill = round(fill, 1)

    # Update Firebase
    bin_ref.update({
        "fillLevel": fill,
         "lastUpdated": datetime.now(timezone.utc).isoformat()
    })

    return jsonify({
        "message": "Bin updated successfully",
        "binId": bin_id,
        "distance": distance,
        "fillLevel": fill
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )