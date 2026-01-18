import hashlib
import json


def hash_context(extracted_signals: dict) -> str:
    """
    Hash structured signals, not raw text.
    Same meaning => same hash.
    """
    payload = json.dumps(extracted_signals, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
