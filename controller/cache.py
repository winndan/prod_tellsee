import json
import os
from typing import Optional
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

# TTL in seconds (default: 1 hour)
REDIS_TTL_SECONDS = int(os.getenv("REDIS_TTL_SECONDS", 3600))

# Upstash client (reads env vars automatically)
redis = Redis.from_env()


def get_cached(context_hash: str) -> Optional[dict]:
    """
    Retrieve cached final response.

    Fail-open behavior on:
    - Redis unavailable
    - Corrupted data
    - JSON decode failure
    """
    try:
        value = redis.get(context_hash)
        if value is None:
            return None

        # Upstash may return already-parsed JSON
        if isinstance(value, dict):
            return value

        # Handle string response
        if isinstance(value, str):
            return json.loads(value)
        
        # Handle bytes response
        if isinstance(value, bytes):
            return json.loads(value.decode('utf-8'))

        return None

    except Exception as e:
        # Cache must NEVER break the pipeline
        print(f"Cache read error (ignoring): {e}")
        return None


def set_cached(context_hash: str, value: dict) -> None:
    """
    Store final response with TTL.
    
    Fail-silent on errors.
    """
    try:
        redis.set(
            context_hash,
            json.dumps(value),
            ex=REDIS_TTL_SECONDS,
        )
    except Exception as e:
        # Ignore cache write failures
        print(f"Cache write error (ignoring): {e}")
        pass