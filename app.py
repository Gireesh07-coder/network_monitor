from flask import Flask, render_template, jsonify
import json
import os
from monitor import start_monitoring

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    try:
        with open("data.json") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # 🔥 Prevent duplicate thread (Flask runs twice in debug mode)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_monitoring()

    app.run(debug=True)