from flask import Flask, request, jsonify
from datetime import datetime
import threading
import json
import os
app = Flask(__name__)
file_lock = threading.Lock()

@app.route('/api/create_session', methods=['POST'])
def create_session():
    data = request.get_json() or {}
    session_id = data.get('session')
    if not session_id:
        session_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = f"logs_{session_id}.txt"
    with file_lock:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"Session {session_id} started at {datetime.utcnow().isoformat()}\n\n")
    return jsonify({"message": "Session created", "session": session_id}), 200


@app.route('/api/log', methods=['POST'])
def receive_log():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No log data provided"}), 400

    log_data = data.get('log', data)
    session_id = data.get('session')
    if session_id:
        file_name = f"logs_{session_id}.txt"
        with file_lock:
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data) + "\n\n")
    print("Received log:", log_data, "Session:", session_id if session_id else "No session")
    return jsonify({"message": "Log received"}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, threaded=True)

