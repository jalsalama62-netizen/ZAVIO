import os

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if client is None:
        return jsonify({
            "error": "ضع OPENAI_API_KEY داخل ملف .env أولاً."
        }), 500

    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    web_search = bool(payload.get("web_search", False))

    if not message:
        return jsonify({
            "error": "اكتب سؤالاً أولاً."
        }), 400

    tools = []
    if web_search:
        tools.append({"type": "web_search_preview"})

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=message,
            tools=tools,
        )

        answer = getattr(response, "output_text", None)
        if not answer:
            answer = "لم أستطع توليد رد مناسب في هذه اللحظة."

        return jsonify({"answer": answer})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
