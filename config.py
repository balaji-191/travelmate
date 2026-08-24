"""
config.py
--------
TravelMate AI configuration.
"""

import os


# --------------------------------------------------
# Gemini API Key
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# --------------------------------------------------
# Gemini Model
# --------------------------------------------------

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


# --------------------------------------------------
# Conversation History
# --------------------------------------------------

# Number of previous conversation turns
# TravelMate will remember.

MAX_HISTORY_TURNS = int(
    os.getenv(
        "MAX_HISTORY_TURNS",
        "10"
    )
)


# --------------------------------------------------
# Flask Secret Key
# --------------------------------------------------

FLASK_SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY",
    "travelmate-secret-key-change-this"
)