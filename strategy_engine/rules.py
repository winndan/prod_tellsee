from strategy_engine.models import StrategyDecision, ExtractedContext
from strategy_engine.enums import (
    EventType,
    Sentiment,
    Clarity,
    PriceInfo,
    StrategyType,
    Urgency,
)


def evaluate_positioning_rule(context: ExtractedContext):
    competitor = context.competitors[0]
    s = competitor.signals

    if (
        s.event == EventType.NEW_PRODUCT_LAUNCH
        and s.sentiment in {Sentiment.POSITIVE, Sentiment.MIXED_POSITIVE}
        and s.clarity == Clarity.CONFUSING
    ):
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="clarity_and_simplicity",
            urgency=Urgency.MEDIUM,
            avoid=["price_war"],
        )

    return None


def evaluate_pricing_rule(context: ExtractedContext):
    competitor = context.competitors[0]
    s = competitor.signals

    if s.price_info == PriceInfo.LOWER:
        return StrategyDecision(
            strategy_type=StrategyType.PRICING,
            focus="value_not_discount",
            urgency=Urgency.HIGH,
            avoid=["race_to_bottom"],
        )

    return None


def evaluate_wait_rule(context: ExtractedContext):
    return StrategyDecision(
        strategy_type=StrategyType.WAIT,
        focus="monitoring",
        urgency=Urgency.LOW,
        avoid=[],
    )
