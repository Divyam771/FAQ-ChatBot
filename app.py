"""
app.py
------
Flask web application that serves a simple chat UI for the FAQ chatbot.

Routes:
  GET  /            -> renders the chat interface
  POST /get_response -> accepts {"message": "..."} JSON and returns the bot's reply
"""

import os
from flask import Flask, render_template, request, jsonify
from chatbot_engine import FAQChatbot

app = Flask(__name__)

FAQ_PATH = os.path.join(os.path.dirname(__file__), "faqs.json")
bot = FAQChatbot(FAQ_PATH, similarity_threshold=0.25)


@app.route("/")
def index():
    sample_questions = bot.all_questions()[:6]
    return render_template("index.html", sample_questions=sample_questions)


@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    result = bot.get_response(user_message)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
