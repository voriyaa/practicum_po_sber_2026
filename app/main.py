from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
APP_PORT = int(os.environ.get("APP_PORT", "5000"))
WELCOME_TITLE = os.environ.get("WELCOME_TITLE", "Welcome to the custom app")
LOG_FILE = os.environ.get("LOG_FILE", "/app/logs/app.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log(msg):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")


@app.route("/")
def index():
    log("GET /")
    return WELCOME_TITLE


@app.route("/status")
def status():
    return jsonify(status="ok")


@app.route("/log", methods=["POST"])
def add_log():
    body = request.get_json(force=True)
    if not body or "message" not in body:
        return jsonify(error="message required"), 400
    log(body["message"])
    return jsonify(result="logged", message=body["message"])


@app.route("/logs")
def get_logs():
    try:
        with open(LOG_FILE) as f:
            return f.read(), 200, {"Content-Type": "text/plain"}
    except FileNotFoundError:
        return "", 200


if __name__ == "__main__":
    log(f"starting, port={APP_PORT}")
    app.run(host="0.0.0.0", port=APP_PORT)
