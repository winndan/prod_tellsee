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
    event: EventType
    sentiment: Sentiment
    clarity: Clarity
    price_info: PriceInfo

    # 🔥 NEW competitive edge signals
    execution_quality: ExecutionQuality
    messaging_strength: MessagingStrength
    market_confusion: MarketConfusion


@dataclass(frozen=True)
class Competitor:
    name: str
    signals: CompetitorSignals


@dataclass(frozen=True)
class ExtractedContext:
    competitors: List[Competitor]
    market_signals: List[str]
    user_intent: str


@dataclass(frozen=True)
class StrategyDecision:
    strategy_type: StrategyType
    focus: str
    urgency: Urgency
    avoid: List[str]
