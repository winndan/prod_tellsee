def build_response(strategy, advisor):
    return {
        "best_move": strategy.strategy_type.value,
        "focus": strategy.focus,
        "urgency": strategy.urgency.value,
        "avoid": strategy.avoid,
        "advice": advisor.advice,
        "reason": advisor.reason,
        "confidence": advisor.confidence,
    }
