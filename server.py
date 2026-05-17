import os

from flask import Flask, jsonify, render_template, request

from friday import LOCAL_COMMANDS, get_friday_response, local_fallback, PROJECT_NAME
import database

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static",
    template_folder="templates",
)

database.init_db()



@app.route("/")
def index():
    return render_template("index.html", project=PROJECT_NAME)

@app.route("/api/sessions", methods=["GET", "DELETE"])
def sessions():
    if request.method == "DELETE":
        database.clear_all_history()
        return jsonify({"status": "success"})
        
    sessions_list = database.get_sessions()
    return jsonify({"sessions": sessions_list})

@app.route("/api/sessions", methods=["POST"])
def create_session():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "New Chat")
    session_id = database.create_session(title)
    return jsonify({"id": session_id, "title": title})

@app.route("/api/sessions/<int:session_id>/messages", methods=["GET"])
def get_session_messages(session_id):
    messages = database.get_session_messages(session_id)
    return jsonify({"messages": messages})


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400

    message = data["message"].strip()
    session_id = data.get("session_id")

    if not message:
        return jsonify({"reply": "", "source": "empty"})

    if not session_id:
        title = message[:30] + ("..." if len(message) > 30 else "")
        session_id = database.create_session(title)

    if session_id:
        database.save_message(session_id, "user", message)
        history = database.get_session_messages(session_id)
        history = history[:-1] if history else []
    else:
        history = None

    normalized = message.lower()
    if normalized in LOCAL_COMMANDS:
        reply = local_fallback(message)
        if reply == "exit":
            reply = "Goodbye."
        if session_id:
            database.save_message(session_id, "bot", reply)
        return jsonify({"reply": reply, "source": "local", "session_id": session_id})

    reply = get_friday_response(message, history)
    source = "api" if os.environ.get("OPENAI_API_KEY") else "local"

    if session_id:
        database.save_message(session_id, "bot", reply)

    return jsonify({"reply": reply, "source": source, "session_id": session_id})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
