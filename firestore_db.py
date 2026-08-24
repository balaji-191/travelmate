"""
firestore_db.py
----------------
Simple helper functions for saving and reading chat history in
Firestore. If Firestore isn't available, these functions quietly do
nothing (or return an empty list) instead of crashing the app.

Firestore structure used:

conversations/{session_id}/messages/{auto_id}
    user_message: str
    bot_reply: str
    timestamp: server timestamp
"""

import config
from firebase_config import get_firestore_client


def save_message(session_id, user_message, bot_reply):
    """Save one user/bot exchange to Firestore. Fails silently."""
    db = get_firestore_client()
    if db is None:
        return  # Firebase not configured — nothing to do.

    try:
        from firebase_admin import firestore

        (
            db.collection(config.FIRESTORE_COLLECTION)
            .document(session_id)
            .collection("messages")
            .add(
                {
                    "user_message": user_message,
                    "bot_reply": bot_reply,
                    "timestamp": firestore.SERVER_TIMESTAMP,
                }
            )
        )
    except Exception as error:
        print(f"[Firestore] Failed to save message: {error}")


def get_conversation(session_id):
    """
    Return this session's saved messages as a list of dicts, ordered
    oldest to newest. Returns an empty list if Firestore isn't
    available or the session has no history yet.
    """
    db = get_firestore_client()
    if db is None:
        return []

    try:
        docs = (
            db.collection(config.FIRESTORE_COLLECTION)
            .document(session_id)
            .collection("messages")
            .order_by("timestamp")
            .stream()
        )
        return [doc.to_dict() for doc in docs]
    except Exception as error:
        print(f"[Firestore] Failed to read conversation: {error}")
        return []
