"""
app.py
------
TravelMate AI - Flask Web Server

Flow:

Browser
   ↓
Flask
   ↓
chatbot.py
   ↓
Gemini AI
   ↓
TravelMate Response
"""

import uuid

from dotenv import load_dotenv

# Load .env variables before importing config.py
load_dotenv()

from flask import Flask, jsonify, render_template, request, session

import config
from chatbot import Chatbot


# --------------------------------------------------
# Flask App
# --------------------------------------------------

app = Flask(__name__)

# Secret key is used for browser sessions
app.secret_key = config.FLASK_SECRET_KEY


# --------------------------------------------------
# TravelMate Chatbot
# --------------------------------------------------

bot = Chatbot()


# --------------------------------------------------
# Session ID
# --------------------------------------------------

def get_session_id():
    """
    Create a unique session ID for each browser session.

    This allows TravelMate to remember the conversation
    during the current session.
    """

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    return session["session_id"]


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    """
    Open TravelMate AI webpage.
    """

    return render_template("index.html")


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():
    """
    Receive a message from the frontend
    and return TravelMate's response.

    Request:
        {
            "message": "Plan a 3 day trip to Ooty"
        }

    Response:
        {
            "response": "Here is your Ooty travel plan..."
        }
    """

    data = request.get_json(silent=True)

    # Check request data
    if not data or "message" not in data:
        return jsonify({
            "error": "Please provide a message."
        }), 400

    # Get user message
    user_message = str(data["message"]).strip()

    # Check empty message
    if not user_message:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    # Get current browser session
    session_id = get_session_id()

    try:
        # Send message to TravelMate AI
        bot_reply = bot.get_response(
            session_id,
            user_message
        )

        return jsonify({
            "response": bot_reply
        })

    except Exception as e:

        print("TravelMate Error:", e)

        return jsonify({
            "error": "Sorry, TravelMate is temporarily unavailable."
        }), 500


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    if not config.GEMINI_API_KEY:
        print(
            "[Warning] GEMINI_API_KEY is not set."
        )
        print(
            "Please add GEMINI_API_KEY to your .env file."
        )

    print()
    print("=" * 50)
    print("        ✈️  TRAVELMATE AI")
    print("=" * 50)
    print("Travel Assistant is starting...")
    print()
    print("Open in browser:")
    print("http://127.0.0.1:5000")
    print()
    print("Travel-related questions only.")
    print("=" * 50)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )