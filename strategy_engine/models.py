from dataclasses import dataclass
from typing import List
from strategy_engine.enums import (
    EventType,
    Sentiment,
    Clarity,
    PriceInfo,
    ExecutionQuality,
    MessagingStrength,
    MarketConfusion,
    StrategyType,
    Urgency,
)


@dataclass(frozen=True)
class CompetitorSignals:
    """
    Structured competitive signals extracted from raw text.
    All fields use enums for type safety and determinism.
    """
    event: EventType
    sentiment: Sentiment
    clarity: Clarity
    price_info: PriceInfo
    
    # Competitive edge signals
    execution_quality: ExecutionQuality
    messaging_strength: MessagingStrength
    market_confusion: MarketConfusion


@dataclass(frozen=True)
class Competitor:
    """
    Represents a single competitor with their signals.
    """
    name: str
    signals: CompetitorSignals


@dataclass(frozen=True)
class ExtractedContext:
    """
    Complete context from Phase 2 (LLM Analyst).
    This is the input to Phase 1 (Strategy Engine).
    """
    competitors: List[Competitor]
    market_signals: List[str]
    user_intent: str


@dataclass(frozen=True)
class StrategyDecision:
    """
    Final strategy decision from Phase 1.
    This is deterministic and repeatable.
    """
    strategy_type: StrategyType
    focus: str
    urgency: Urgency
    avoid: List[str]