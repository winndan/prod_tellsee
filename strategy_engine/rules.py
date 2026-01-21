from typing import Optional
from strategy_engine.models import StrategyDecision, ExtractedContext
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


def evaluate_positioning_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 1: Positioning Response
    
    Triggers when competitor launches a confusing product with positive sentiment.
    Strategy: Capitalize on confusion with clear messaging.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    # Primary positioning trigger: confusing product launch with positive buzz
    if (
        s.event == EventType.NEW_PRODUCT_LAUNCH
        and s.sentiment in {Sentiment.POSITIVE, Sentiment.MIXED_POSITIVE}
        and s.clarity == Clarity.CONFUSING
    ):
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="clarity_and_simplicity",
            urgency=Urgency.MEDIUM,
            avoid=["price_war", "feature_matching"],
        )
    
    # Secondary positioning trigger: weak execution with generic messaging
    if (
        s.execution_quality == ExecutionQuality.WEAK
        and s.messaging_strength == MessagingStrength.GENERIC
        and s.market_confusion == MarketConfusion.HIGH
    ):
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="differentiation_and_quality",
            urgency=Urgency.MEDIUM,
            avoid=["price_war"],
        )

    return None


def evaluate_pricing_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 2: Pricing Response
    
    Triggers when competitor drops price.
    Strategy: Emphasize value, avoid race to bottom.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    # Primary pricing trigger: competitor goes lower
    if s.price_info == PriceInfo.LOWER:
        # High urgency if execution is strong (serious threat)
        if s.execution_quality == ExecutionQuality.STRONG:
            return StrategyDecision(
                strategy_type=StrategyType.PRICING,
                focus="value_not_discount",
                urgency=Urgency.HIGH,
                avoid=["race_to_bottom", "panic_discounting"],
            )
        
        # Medium urgency if execution is weak (wait and see)
        return StrategyDecision(
            strategy_type=StrategyType.PRICING,
            focus="value_not_discount",
            urgency=Urgency.MEDIUM,
            avoid=["race_to_bottom"],
        )

    return None


def evaluate_aggressive_positioning_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 3: Aggressive Positioning Response
    
    Triggers when competitor has strong execution but confusing messaging.
    Strategy: Strike while they're vulnerable with clear counter-messaging.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    if (
        s.execution_quality == ExecutionQuality.STRONG
        and s.messaging_strength == MessagingStrength.CONFUSING
        and s.market_confusion == MarketConfusion.HIGH
    ):
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="exploit_messaging_weakness",
            urgency=Urgency.HIGH,
            avoid=["feature_matching", "wait"],
        )

    return None


def evaluate_defensive_wait_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 4: Strategic Wait (Defensive)
    
    Triggers when competitor launches but market is confused and sentiment is negative.
    Strategy: Let them fail, monitor closely.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    if (
        s.event == EventType.NEW_PRODUCT_LAUNCH
        and s.sentiment == Sentiment.NEGATIVE
        and s.market_confusion == MarketConfusion.HIGH
    ):
        return StrategyDecision(
            strategy_type=StrategyType.WAIT,
            focus="let_competitor_fail_first",
            urgency=Urgency.LOW,
            avoid=["early_reaction", "price_changes"],
        )

    return None


def evaluate_wait_rule(context: ExtractedContext) -> StrategyDecision:
    """
    Default Rule: Wait and Observe
    
    Conservative fallback when no other rule matches.
    Always returns a decision (never None).
    """
    return StrategyDecision(
        strategy_type=StrategyType.WAIT,
        focus="monitoring",
        urgency=Urgency.LOW,
        avoid=["hasty_reactions"],
    )


# Advanced rules for edge cases

def evaluate_price_increase_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 5: Price Increase Opportunity
    
    Triggers when competitor raises prices.
    Strategy: Maintain current pricing, highlight value.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    if s.price_info == PriceInfo.HIGHER:
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="value_at_current_price",
            urgency=Urgency.MEDIUM,
            avoid=["price_increases", "complacency"],
        )

    return None


def evaluate_market_leader_rule(context: ExtractedContext) -> Optional[StrategyDecision]:
    """
    Rule 6: Market Leader Defense
    
    Triggers when competitor has strong execution AND clear messaging.
    Strategy: Defensive positioning, protect market share.
    """
    if not context.competitors:
        return None
    
    competitor = context.competitors[0]
    s = competitor.signals

    if (
        s.execution_quality == ExecutionQuality.STRONG
        and s.messaging_strength == MessagingStrength.CLEAR
        and s.sentiment == Sentiment.POSITIVE
    ):
        return StrategyDecision(
            strategy_type=StrategyType.POSITIONING,
            focus="defend_differentiation",
            urgency=Urgency.HIGH,
            avoid=["ignore", "price_war"],
        )

    return None