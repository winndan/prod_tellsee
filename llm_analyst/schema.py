from pydantic import BaseModel
from typing import List, Literal


class CompetitorSignalsSchema(BaseModel):
    event: Literal["new_product_launch", "price_change", "none"]

    sentiment: Literal[
        "positive",
        "mixed_positive",
        "neutral",
        "negative",
        "unknown",
    ]

    clarity: Literal["clear", "confusing", "unknown"]

    price_info: Literal["lower", "higher", "same", "unknown"]

    # 🔥 NEW competitive edge signals (LLM-facing)
    execution_quality: Literal["strong", "average", "weak", "unknown"]
    messaging_strength: Literal["clear", "generic", "confusing", "unknown"]
    market_confusion: Literal["high", "medium", "low", "unknown"]


class CompetitorSchema(BaseModel):
    name: str
    signals: CompetitorSignalsSchema


class ExtractedContextSchema(BaseModel):
    competitors: List[CompetitorSchema]
    market_signals: List[str]

    user_intent: Literal[
        "seeking_response",
        "monitoring",
        "comparison",
    ]
