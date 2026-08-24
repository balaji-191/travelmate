"""
firebase_config.py
-------------------
Handles connecting to Firebase. Firebase is OPTIONAL — if the
credentials file is missing or invalid, the app should keep working
without chat history persistence.

Other files should call get_firestore_client() and check for None
before using it.
"""

import os

import config

_db = None          # cached Firestore client (or None if unavailable)
_initialized = False  # tracks whether we already tried to connect


def get_firestore_client():
    """
    Return a Firestore client, or None if Firebase isn't set up.

    Safe to call many times — it only tries to connect once.
    """
    global _db, _initialized

    if _initialized:
        return _db

    _initialized = True

    if not os.path.exists(config.FIREBASE_CREDENTIALS_PATH):
        print("[Firestore] Not initialized, persistence disabled.")
        print(
            f"  (No credentials file found at "
            f"'{config.FIREBASE_CREDENTIALS_PATH}')"
        )
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        _db = firestore.client()
        print("[Firestore] Connected - chat history will be persisted.")
    except Exception as error:
        print(f"[Firestore] Not initialized, persistence disabled. ({error})")
        _db = None

    return _db
