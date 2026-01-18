from strategy_engine.models import ExtractedContext, StrategyDecision
from strategy_engine.rules import (
    evaluate_positioning_rule,
    evaluate_pricing_rule,
    evaluate_wait_rule,
)


RULES = [
    evaluate_positioning_rule,
    evaluate_pricing_rule,
]


def decide_strategy(context: ExtractedContext) -> StrategyDecision:
    for rule in RULES:
        decision = rule(context)
        if decision:
            return decision

    return evaluate_wait_rule(context)
