import os
import json
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from llm_analyst.prompts import ANALYST_SYSTEM_PROMPT
from llm_analyst.schema import ExtractedContextSchema

from strategy_engine.enums import (
    EventType,
    Sentiment,
    Clarity,
    PriceInfo,
    ExecutionQuality,
    MessagingStrength,
    MarketConfusion,
)
from strategy_engine.models import (
    Competitor,
    CompetitorSignals,
    ExtractedContext,
)

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

model = GoogleModel(
    "gemini-2.5-flash",
    provider=GoogleProvider(api_key=google_api_key),
)

analyst_agent = Agent(
    model=model,
    system_prompt=ANALYST_SYSTEM_PROMPT,
)


# ----------------------------
# Helpers
# ----------------------------

def extract_json_block(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def safe_enum(enum_cls, value, default):
    try:
        return enum_cls(value)
    except Exception:
        return default


# ----------------------------
# Main extractor
# ----------------------------

def extract_signals(raw_text: str) -> ExtractedContext:
    """
    Phase 2 — LLM Analyst

    Converts raw competitor text into a domain-safe ExtractedContext
    using strict enums and validated structure.
    """

    if not raw_text or len(raw_text) > 3000:
        raise ValueError("Input exceeds 3000 characters")

    # 1️⃣ Run LLM
    result = analyst_agent.run_sync(raw_text)
    raw_output = result.output
    clean_output = extract_json_block(raw_output)

    # 2️⃣ Parse JSON
    try:
        parsed = json.loads(clean_output)
    except json.JSONDecodeError:
        raise ValueError(
            f"LLM did not return valid JSON.\nRaw output:\n{raw_output}"
        )

    # 3️⃣ Validate LLM-facing schema (strings only)
    try:
        validated = ExtractedContextSchema(**parsed)
    except Exception as e:
        raise ValueError(f"LLM output failed schema validation: {e}")

    # 4️⃣ Convert to domain models with enum safety
    competitors = []

    for c in validated.competitors:
        s = c.signals

        signals = CompetitorSignals(
            event=safe_enum(EventType, s.event, EventType.NONE),
            sentiment=safe_enum(Sentiment, s.sentiment, Sentiment.UNKNOWN),
            clarity=safe_enum(Clarity, s.clarity, Clarity.UNKNOWN),
            price_info=safe_enum(PriceInfo, s.price_info, PriceInfo.UNKNOWN),
            execution_quality=safe_enum(
                ExecutionQuality,
                getattr(s, "execution_quality", None),
                ExecutionQuality.UNKNOWN,
            ),
            messaging_strength=safe_enum(
                MessagingStrength,
                getattr(s, "messaging_strength", None),
                MessagingStrength.UNKNOWN,
            ),
            market_confusion=safe_enum(
                MarketConfusion,
                getattr(s, "market_confusion", None),
                MarketConfusion.UNKNOWN,
            ),
        )

        competitors.append(
            Competitor(
                name=c.name,
                signals=signals,
            )
        )

    return ExtractedContext(
        competitors=competitors,
        market_signals=validated.market_signals,
        user_intent=validated.user_intent,
    )
