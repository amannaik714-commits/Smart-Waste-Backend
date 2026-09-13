from flask import Flask, jsonify
import firebase_connection
from firebase_admin import db

app = Flask(__name__)


@app.route("/")
def home():
    return "Smart Waste Management Backend is running!"


@app.route("/bins")
def get_bins():
    data = db.reference("bins").get() or {}

    return jsonify(list(data.values()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)