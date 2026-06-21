from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).parent

@app.route("/")
def home():
    return "API Server is Running!"

@app.route("/students")
def students():
    # just reading from a local json file for now, no DB needed for the API
    with open(BASE_DIR / "students.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

    